"""
Navigation Vibium functionality
"""

import time
from typing import Optional, List
from ..core.vibium_core import VibiumCore

class VibiumNavigation:
    """
    Navigation and URL management methods
    """
    
    def __init__(self, device='default', browser_type='chromium', core=None):
        self.device = device
        self.browser_type = browser_type
        # Use the passed core instance instead of creating a new one
        self.core = core if core else VibiumCore(device, browser_type)
    
    def goto(self, url: str, expected_title: str = None, wait_for_load: bool = True):
        """
        Navigate to a URL and optionally verify title
        
        Args:
            url (str): URL to navigate to
            expected_title (str): Expected page title
            wait_for_load (bool): Whether to wait for page load
        """
        try:
            self.core.goto(url, wait_for_load)
            
            if expected_title:
                actual_title = self.core.page.title()
                if expected_title.lower() in actual_title.lower():
                    print(f"[{self.device}] Title verification passed: '{expected_title}' found in '{actual_title}'")
                else:
                    print(f"[{self.device}] Title verification failed: Expected '{expected_title}', got '{actual_title}'")
            
            return True
            
        except Exception as e:
            print(f"[{self.device}] Failed to navigate to {url}: {str(e)}")
            return False
    
    def click_nav_item(self, nav_text: str, nav_selector: str = "nav"):
        """
        Click on a navigation item
        
        Args:
            nav_text (str): Text of the navigation item
            nav_selector (str): Selector for navigation container
        """
        try:
            nav = self.core.page.locator(nav_selector)
            nav_item = nav.locator(f"a:has-text('{nav_text}'), [data-testid='nav-{nav_text}'], .nav-{nav_text}")
            
            nav_item.click()
            
            # Wait for navigation
            time.sleep(2)
            
            print(f"[{self.device}] Clicked navigation item: {nav_text}")
            return True
            
        except Exception as e:
            print(f"[{self.device}] Failed to click navigation item '{nav_text}': {str(e)}")
            return False
    
    def verify_page(self, expected_elements: List[str], page_name: str = "current page"):
        """
        Verify that expected elements are present on the page
        
        Args:
            expected_elements (List[str]): List of element selectors to verify
            page_name (str): Name of the page for logging
        """
        try:
            all_found = True
            
            for element_selector in expected_elements:
                try:
                    element = self.core.page.locator(element_selector)
                    if element.is_visible():
                        print(f"[{self.device}] Element found on {page_name}: {element_selector}")
                    else:
                        print(f"[{self.device}] Element not visible on {page_name}: {element_selector}")
                        all_found = False
                except:
                    print(f"[{self.device}] Element not found on {page_name}: {element_selector}")
                    all_found = False
            
            if all_found:
                print(f"[{self.device}] All expected elements found on {page_name}")
            else:
                print(f"[{self.device}] Some expected elements missing on {page_name}")
            
            return all_found
            
        except Exception as e:
            print(f"[{self.device}] Failed to verify page {page_name}: {str(e)}")
            return False
    
    def go_back(self):
        """Go back to previous page"""
        try:
            self.core.page.go_back()
            time.sleep(2)
            
            print(f"[{self.device}] Navigated back to previous page")
            return True
            
        except Exception as e:
            print(f"[{self.device}] Failed to go back: {str(e)}")
            return False
    
    def go_forward(self):
        """Go forward to next page"""
        try:
            self.core.page.go_forward()
            time.sleep(2)
            
            print(f"[{self.device}] Navigated forward to next page")
            return True
            
        except Exception as e:
            print(f"[{self.device}] Failed to go forward: {str(e)}")
            return False
    
    def refresh_page(self):
        """Refresh the current page"""
        try:
            self.core.page.reload()
            self.core.page.wait_for_load_state('networkidle')
            
            print(f"[{self.device}] Page refreshed")
            return True
            
        except Exception as e:
            print(f"[{self.device}] Failed to refresh page: {str(e)}")
            return False
    
    def wait_for_url_change(self, timeout: int = 10):
        """
        Wait for URL to change
        
        Args:
            timeout (int): Timeout in seconds
        """
        try:
            start_time = time.time()
            initial_url = self.core.page.url
            
            while time.time() - start_time < timeout:
                current_url = self.core.page.url
                if current_url != initial_url:
                    print(f"[{self.device}] URL changed from '{initial_url}' to '{current_url}'")
                    return True
                time.sleep(0.5)
            
            print(f"[{self.device}] URL did not change within {timeout} seconds")
            return False
            
        except Exception as e:
            print(f"[{self.device}] Failed to wait for URL change: {str(e)}")
            return False
    
    def get_current_url(self) -> str:
        """Get the current page URL"""
        try:
            url = self.core.page.url
            print(f"[{self.device}] Current URL: {url}")
            return url
        except Exception as e:
            print(f"[{self.device}] Failed to get current URL: {str(e)}")
            return ""
    
    def get_page_title(self) -> str:
        """Get the current page title"""
        try:
            title = self.core.page.title()
            print(f"[{self.device}] Page title: {title}")
            return title
        except Exception as e:
            print(f"[{self.device}] Failed to get page title: {str(e)}")
            return ""
