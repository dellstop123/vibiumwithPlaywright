"""
Elements interaction Vibium functionality
"""

import time
from typing import Optional
from ..core.vibium_core import VibiumCore

class VibiumElements:
    """
    Element interaction methods
    """
    
    def __init__(self, device='default', browser_type='chromium'):
        self.device = device
        self.browser_type = browser_type
        self.core = VibiumCore(device, browser_type)
    
    def wait_for_stable(self, selector: str, timeout: int = 5000):
        """
        Wait for element to be stable
        
        Args:
            selector (str): Element selector
            timeout (int): Timeout in milliseconds
        """
        try:
            element = self.core.page.locator(selector)
            element.wait_for(state='visible', timeout=timeout)
            element.wait_for(state='stable', timeout=timeout)
            
            print(f"[{self.device}] Element is stable: {selector}")
            return True
            
        except Exception as e:
            print(f"[{self.device}] Failed to wait for element stability: {str(e)}")
            return False
    
    def click_with_retry(self, selector: str, max_retries: int = 3, delay: float = 1.0):
        """
        Click element with retry mechanism
        
        Args:
            selector (str): Element selector
            max_retries (int): Maximum number of retries
            delay (float): Delay between retries in seconds
        """
        for attempt in range(max_retries):
            try:
                element = self.core.page.locator(selector)
                element.click()
                print(f"[{self.device}] Element clicked successfully: {selector}")
                return True
                
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"[{self.device}] Click attempt {attempt + 1} failed, retrying: {str(e)}")
                    time.sleep(delay)
                else:
                    print(f"[{self.device}] Failed to click element after {max_retries} attempts: {str(e)}")
                    return False
        
        return False
    
    def fill_input(self, selector: str, text: str, clear_first: bool = True):
        """
        Fill input field with text
        
        Args:
            selector (str): Input element selector
            text (str): Text to fill
            clear_first (bool): Whether to clear field first
        """
        try:
            element = self.core.page.locator(selector)
            
            if clear_first:
                element.clear()
            
            element.fill(text)
            print(f"[{self.device}] Filled input '{selector}' with '{text}'")
            return True
            
        except Exception as e:
            print(f"[{self.device}] Failed to fill input '{selector}': {str(e)}")
            return False
    
    def select_option(self, selector: str, option_value: str):
        """
        Select an option from dropdown
        
        Args:
            selector (str): Select element selector
            option_value (str): Value of option to select
        """
        try:
            element = self.core.page.locator(selector)
            element.select_option(value=option_value)
            
            print(f"[{self.device}] Selected option '{option_value}' from '{selector}'")
            return True
            
        except Exception as e:
            print(f"[{self.device}] Failed to select option from '{selector}': {str(e)}")
            return False
    
    def hover_element(self, selector: str):
        """
        Hover over an element
        
        Args:
            selector (str): Element selector
        """
        try:
            element = self.core.page.locator(selector)
            element.hover()
            
            print(f"[{self.device}] Hovered over element: {selector}")
            return True
            
        except Exception as e:
            print(f"[{self.device}] Failed to hover over element '{selector}': {str(e)}")
            return False
    
    def drag_and_drop(self, source_selector: str, target_selector: str):
        """
        Drag and drop an element
        
        Args:
            source_selector (str): Source element selector
            target_selector (str): Target element selector
        """
        try:
            source = self.core.page.locator(source_selector)
            target = self.core.page.locator(target_selector)
            
            source.drag_to(target)
            
            print(f"[{self.device}] Dragged '{source_selector}' to '{target_selector}'")
            return True
            
        except Exception as e:
            print(f"[{self.device}] Failed to drag and drop: {str(e)}")
            return False
    
    def scroll_to_element(self, selector: str):
        """
        Scroll to element
        
        Args:
            selector (str): Element selector
        """
        try:
            element = self.core.page.locator(selector)
            element.scroll_into_view_if_needed()
            
            print(f"[{self.device}] Scrolled to element: {selector}")
            return True
            
        except Exception as e:
            print(f"[{self.device}] Failed to scroll to element '{selector}': {str(e)}")
            return False
    
    def get_element_text(self, selector: str) -> Optional[str]:
        """
        Get element text content
        
        Args:
            selector (str): Element selector
            
        Returns:
            str: Element text or None if not found
        """
        try:
            element = self.core.page.locator(selector)
            text = element.text_content()
            
            print(f"[{self.device}] Got text from '{selector}': {text}")
            return text.strip() if text else None
            
        except Exception as e:
            print(f"[{self.device}] Failed to get text from '{selector}': {str(e)}")
            return None
    
    def is_element_visible(self, selector: str) -> bool:
        """
        Check if element is visible
        
        Args:
            selector (str): Element selector
            
        Returns:
            bool: True if element is visible
        """
        try:
            element = self.core.page.locator(selector)
            is_visible = element.is_visible()
            
            print(f"[{self.device}] Element '{selector}' visibility: {is_visible}")
            return is_visible
            
        except Exception as e:
            print(f"[{self.device}] Failed to check visibility of '{selector}': {str(e)}")
            return False
