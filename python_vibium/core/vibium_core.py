"""
Core Vibium functionality for UI automation
"""

import time
from typing import Optional, Any, Dict
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext

class VibiumCore:
    """
    Core Vibium class providing basic automation capabilities
    """
    
    def __init__(self, device='default', browser_type='chromium'):
        self.device = device
        self.browser_type = browser_type
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.is_initialized = False
    
    def initialize(self, headless=True):
        """
        Initialize the browser and create a new page
        
        Args:
            headless (bool): Whether to run browser in headless mode
        """
        try:
            self.playwright = sync_playwright().start()
            
            if self.browser_type == 'chromium':
                self.browser = self.playwright.chromium.launch(headless=headless)
            elif self.browser_type == 'firefox':
                self.browser = self.playwright.firefox.launch(headless=headless)
            elif self.browser_type == 'webkit':
                self.browser = self.playwright.webkit.launch(headless=headless)
            else:
                raise ValueError(f"Unsupported browser type: {self.browser_type}")
            
            self.context = self.browser.new_context()
            self.page = self.context.new_page()
            self.is_initialized = True
            
            print(f"[{self.device}] Browser {self.browser_type} initialized successfully")
            return True
            
        except Exception as e:
            print(f"[{self.device}] Failed to initialize browser: {str(e)}")
            return False
    
    def goto(self, url: str, wait_for_load=True):
        """
        Navigate to a URL
        
        Args:
            url (str): URL to navigate to
            wait_for_load (bool): Whether to wait for page load
        """
        if not self.is_initialized:
            raise RuntimeError("Browser not initialized. Call initialize() first.")
        
        try:
            self.page.goto(url)
            if wait_for_load:
                self.page.wait_for_load_state('networkidle')
            print(f"[{self.device}] Navigated to: {url}")
            return True
        except Exception as e:
            print(f"[{self.device}] Failed to navigate to {url}: {str(e)}")
            return False
    
    def do(self, command: str):
        """
        Execute a command
        
        Args:
            command (str): Command to execute
        """
        print(f"[{self.device}] Doing: {command}")
        
        # Parse and execute common commands
        if command.startswith('goto '):
            url = command[5:]
            return self.goto(url)
        elif command.startswith('click '):
            selector = command[6:]
            return self.click(selector)
        elif command.startswith('type '):
            parts = command[5:].split(' in ')
            if len(parts) == 2:
                text, selector = parts
                return self.type(selector, text)
        elif command.startswith('wait '):
            seconds = float(command[5:])
            return self.wait(seconds)
        
        return f"Command '{command}' not recognized"
    
    def check(self, question: str):
        """
        Check a condition or question
        
        Args:
            question (str): Question or condition to check
        """
        print(f"[{self.device}] Checking: {question}")
        
        if not self.is_initialized:
            return "Browser not initialized"
        
        # Parse and check common questions
        if question.startswith('title contains '):
            text = question[15:]
            return self.page.title().lower().find(text.lower()) != -1
        elif question.startswith('element visible '):
            selector = question[16:]
            try:
                element = self.page.locator(selector)
                return element.is_visible()
            except:
                return False
        elif question.startswith('url contains '):
            text = question[13:]
            return self.page.url.find(text) != -1
        
        return f"Question '{question}' not recognized"
    
    def click(self, selector: str):
        """Click an element"""
        try:
            self.page.click(selector)
            print(f"[{self.device}] Clicked: {selector}")
            return True
        except Exception as e:
            print(f"[{self.device}] Failed to click {selector}: {str(e)}")
            return False
    
    def type(self, selector: str, text: str):
        """Type text into an element"""
        try:
            self.page.fill(selector, text)
            print(f"[{self.device}] Typed '{text}' into: {selector}")
            return True
        except Exception as e:
            print(f"[{self.device}] Failed to type into {selector}: {str(e)}")
            return False
    
    def wait(self, seconds: float):
        """Wait for specified seconds"""
        time.sleep(seconds)
        print(f"[{self.device}] Waited for {seconds} seconds")
        return True
    
    def screenshot(self, path: str = None):
        """Take a screenshot"""
        if not path:
            path = f"screenshot_{int(time.time())}.png"
        
        try:
            self.page.screenshot(path=path)
            print(f"[{self.device}] Screenshot saved to: {path}")
            return path
        except Exception as e:
            print(f"[{self.device}] Failed to take screenshot: {str(e)}")
            return None
    
    def close(self):
        """Close browser and cleanup"""
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        
        self.is_initialized = False
        print(f"[{self.device}] Browser closed and cleaned up")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
