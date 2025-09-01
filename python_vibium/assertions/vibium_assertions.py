"""
Assertions Vibium functionality
"""

from typing import Optional, List
from ..core.vibium_core import VibiumCore

class VibiumAssertions:
    """
    Assertion and verification methods
    """
    
    def __init__(self, device='default', browser_type='chromium', core=None):
        self.device = device
        self.browser_type = browser_type
        # Use the passed core instance instead of creating a new one
        self.core = core if core else VibiumCore(device, browser_type)
    
    def contains_text(self, selector: str, expected_text: str) -> bool:
        """
        Assert that element contains expected text
        
        Args:
            selector (str): Element selector
            expected_text (str): Expected text to find
            
        Returns:
            bool: True if text is found
        """
        try:
            element = self.core.page.locator(selector)
            actual_text = element.text_content()
            
            if expected_text.lower() in actual_text.lower():
                print(f"[{self.device}] Text assertion passed: '{expected_text}' found in '{actual_text}'")
                return True
            else:
                print(f"[{self.device}] Text assertion failed: Expected '{expected_text}', got '{actual_text}'")
                return False
                
        except Exception as e:
            print(f"[{self.device}] Failed to verify text: {str(e)}")
            return False
    
    def is_visible(self, selector: str) -> bool:
        """
        Assert that element is visible
        
        Args:
            selector (str): Element selector
            
        Returns:
            bool: True if element is visible
        """
        try:
            element = self.core.page.locator(selector)
            is_visible = element.is_visible()
            
            if is_visible:
                print(f"[{self.device}] Visibility assertion passed: '{selector}' is visible")
            else:
                print(f"[{self.device}] Visibility assertion failed: '{selector}' is not visible")
            
            return is_visible
            
        except Exception as e:
            print(f"[{self.device}] Failed to check visibility: {str(e)}")
            return False
    
    def has_count(self, selector: str, expected_count: int) -> bool:
        """
        Assert that elements have expected count
        
        Args:
            selector (str): Element selector
            expected_count (int): Expected number of elements
            
        Returns:
            bool: True if count matches
        """
        try:
            elements = self.core.page.locator(selector)
            actual_count = elements.count()
            
            if actual_count == expected_count:
                print(f"[{self.device}] Count assertion passed: Found {actual_count} elements")
                return True
            else:
                print(f"[{self.device}] Count assertion failed: Expected {expected_count}, got {actual_count}")
                return False
                
        except Exception as e:
            print(f"[{self.device}] Failed to verify count: {str(e)}")
            return False
    
    def url_contains(self, expected_text: str) -> bool:
        """
        Assert that URL contains expected text
        
        Args:
            expected_text (str): Expected text in URL
            
        Returns:
            bool: True if URL contains text
        """
        try:
            current_url = self.core.page.url
            
            if expected_text.lower() in current_url.lower():
                print(f"[{self.device}] URL assertion passed: '{expected_text}' found in '{current_url}'")
                return True
            else:
                print(f"[{self.device}] URL assertion failed: Expected '{expected_text}' in '{current_url}'")
                return False
                
        except Exception as e:
            print(f"[{self.device}] Failed to verify URL: {str(e)}")
            return False
    
    def title_contains(self, expected_text: str) -> bool:
        """
        Assert that page title contains expected text
        
        Args:
            expected_text (str): Expected text in title
            
        Returns:
            bool: True if title contains text
        """
        try:
            current_title = self.core.page.title()
            
            if expected_text.lower() in current_title.lower():
                print(f"[{self.device}] Title assertion passed: '{expected_text}' found in '{current_title}'")
                return True
            else:
                print(f"[{self.device}] Title assertion failed: Expected '{expected_text}' in '{current_title}'")
                return False
                
        except Exception as e:
            print(f"[{self.device}] Failed to verify title: {str(e)}")
            return False
    
    def element_enabled(self, selector: str) -> bool:
        """
        Assert that element is enabled
        
        Args:
            selector (str): Element selector
            
        Returns:
            bool: True if element is enabled
        """
        try:
            element = self.core.page.locator(selector)
            is_enabled = element.is_enabled()
            
            if is_enabled:
                print(f"[{self.device}] Enabled assertion passed: '{selector}' is enabled")
            else:
                print(f"[{self.device}] Enabled assertion failed: '{selector}' is disabled")
            
            return is_enabled
            
        except Exception as e:
            print(f"[{self.device}] Failed to check if enabled: {str(e)}")
            return False
    
    def element_disabled(self, selector: str) -> bool:
        """
        Assert that element is disabled
        
        Args:
            selector (str): Element selector
            
        Returns:
            bool: True if element is disabled
        """
        try:
            element = self.core.page.locator(selector)
            is_disabled = not element.is_enabled()
            
            if is_disabled:
                print(f"[{self.device}] Disabled assertion passed: '{selector}' is disabled")
            else:
                print(f"[{self.device}] Disabled assertion failed: '{selector}' is enabled")
            
            return is_disabled
            
        except Exception as e:
            print(f"[{self.device}] Failed to check if disabled: {str(e)}")
            return False
    
    def all_elements_visible(self, selectors: List[str]) -> bool:
        """
        Assert that all elements are visible
        
        Args:
            selectors (List[str]): List of element selectors
            
        Returns:
            bool: True if all elements are visible
        """
        try:
            all_visible = True
            
            for selector in selectors:
                if not self.is_visible(selector):
                    all_visible = False
            
            if all_visible:
                print(f"[{self.device}] All elements visibility assertion passed")
            else:
                print(f"[{self.device}] All elements visibility assertion failed")
            
            return all_visible
            
        except Exception as e:
            print(f"[{self.device}] Failed to verify all elements visibility: {str(e)}")
            return False
