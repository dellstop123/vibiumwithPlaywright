"""
Wait Vibium functionality
"""

import time
from typing import Optional, Callable
from ..core.vibium_core import VibiumCore

class VibiumWait:
    """
    Wait and timing methods
    """
    
    def __init__(self, device='default', browser_type='chromium', core=None):
        self.device = device
        self.browser_type = browser_type
        # Use the passed core instance instead of creating a new one
        self.core = core if core else VibiumCore(device, browser_type)
    
    def for_network_idle(self, timeout: int = 30):
        """
        Wait for network to be idle
        
        Args:
            timeout (int): Timeout in seconds
        """
        try:
            self.core.page.wait_for_load_state('networkidle', timeout=timeout * 1000)
            print(f"[{self.device}] Network is idle")
            return True
            
        except Exception as e:
            print(f"[{self.device}] Failed to wait for network idle: {str(e)}")
            return False
    
    def for_dom_content_loaded(self, timeout: int = 30):
        """
        Wait for DOM content to be loaded
        
        Args:
            timeout (int): Timeout in seconds
        """
        try:
            self.core.page.wait_for_load_state('domcontentloaded', timeout=timeout * 1000)
            print(f"[{self.device}] DOM content loaded")
            return True
            
        except Exception as e:
            print(f"[{self.device}] Failed to wait for DOM content loaded: {str(e)}")
            return False
    
    def for_timeout(self, seconds: float):
        """
        Wait for specified number of seconds
        
        Args:
            seconds (float): Seconds to wait
        """
        time.sleep(seconds)
        print(f"[{self.device}] Waited for {seconds} seconds")
        return True
    
    def for_element_visible(self, selector: str, timeout: int = 10):
        """
        Wait for element to be visible
        
        Args:
            selector (str): Element selector
            timeout (int): Timeout in seconds
        """
        try:
            element = self.core.page.locator(selector)
            element.wait_for({ state: 'visible', timeout: timeout * 1000 })
            
            print(f"[{self.device}] Element is visible: {selector}")
            return True
            
        except Exception as e:
            print(f"[{self.device}] Failed to wait for element visibility: {str(e)}")
            return False
    
    def for_element_hidden(self, selector: str, timeout: int = 10):
        """
        Wait for element to be hidden
        
        Args:
            selector (str): Element selector
            timeout (int): Timeout in seconds
        """
        try:
            element = self.core.page.locator(selector)
            element.wait_for({ state: 'hidden', timeout: timeout * 1000 })
            
            print(f"[{self.device}] Element is hidden: {selector}")
            return True
            
        except Exception as e:
            print(f"[{self.device}] Failed to wait for element to be hidden: {str(e)}")
            return False
    
    def for_element_stable(self, selector: str, timeout: int = 10):
        """
        Wait for element to be stable
        
        Args:
            selector (str): Element selector
            timeout (int): Timeout in seconds
        """
        try:
            element = self.core.page.locator(selector)
            element.wait_for({ state: 'visible', timeout: timeout * 1000 })
            element.wait_for({ state: 'stable', timeout: timeout * 1000 })
            
            print(f"[{self.device}] Element is stable: {selector}")
            return True
            
        except Exception as e:
            print(f"[{self.device}] Failed to wait for element stability: {str(e)}")
            return False
    
    def for_url_change(self, current_url: str, timeout: int = 10):
        """
        Wait for URL to change from current URL
        
        Args:
            current_url (str): Current URL to wait for change from
            timeout (int): Timeout in seconds
        """
        try:
            start_time = time.time()
            
            while time.time() - start_time < timeout:
                if self.core.page.url != current_url:
                    print(f"[{self.device}] URL changed from '{current_url}' to '{self.core.page.url}'")
                    return True
                time.sleep(0.5)
            
            print(f"[{self.device}] URL did not change within {timeout} seconds")
            return False
            
        except Exception as e:
            print(f"[{self.device}] Failed to wait for URL change: {str(e)}")
            return False
    
    def for_url_contains(self, expected_text: str, timeout: int = 10):
        """
        Wait for URL to contain expected text
        
        Args:
            expected_text (str): Expected text in URL
            timeout (int): Timeout in seconds
        """
        try:
            start_time = time.time()
            
            while time.time() - start_time < timeout:
                if expected_text.lower() in self.core.page.url.lower():
                    print(f"[{self.device}] URL contains expected text: '{expected_text}'")
                    return True
                time.sleep(0.5)
            
            print(f"[{self.device}] URL did not contain '{expected_text}' within {timeout} seconds")
            return False
            
        except Exception as e:
            print(f"[{self.device}] Failed to wait for URL text: {str(e)}")
            return False
    
    def for_title_contains(self, expected_text: str, timeout: int = 10):
        """
        Wait for page title to contain expected text
        
        Args:
            expected_text (str): Expected text in title
            timeout (int): Timeout in seconds
        """
        try:
            start_time = time.time()
            
            while time.time() - start_time < timeout:
                current_title = self.core.page.title()
                if expected_text.lower() in current_title.lower():
                    print(f"[{self.device}] Title contains expected text: '{expected_text}'")
                    return True
                time.sleep(0.5)
            
            print(f"[{self.device}] Title did not contain '{expected_text}' within {timeout} seconds")
            return False
            
        except Exception as e:
            print(f"[{self.device}] Failed to wait for title text: {str(e)}")
            return False
    
    def for_condition(self, condition: Callable[[], bool], timeout: int = 10, interval: float = 0.5):
        """
        Wait for a custom condition to be true
        
        Args:
            condition (Callable[[], bool]): Function that returns boolean
            timeout (int): Timeout in seconds
            interval (float): Check interval in seconds
            
        Returns:
            bool: True if condition met, False if timeout
        """
        try:
            start_time = time.time()
            
            while time.time() - start_time < timeout:
                if condition():
                    print(f"[{self.device}] Custom condition met")
                    return True
                time.sleep(interval)
            
            print(f"[{self.device}] Custom condition not met within {timeout} seconds")
            return False
            
        except Exception as e:
            print(f"[{self.device}] Failed to wait for custom condition: {str(e)}")
            return False
    
    def for_page_load(self, timeout: int = 30):
        """
        Wait for complete page load
        
        Args:
            timeout (int): Timeout in seconds
        """
        try:
            # Wait for multiple load states
            self.core.page.wait_for_load_state('domcontentloaded', timeout=timeout * 1000)
            self.core.page.wait_for_load_state('networkidle', timeout=timeout * 1000)
            
            print(f"[{self.device}] Page fully loaded")
            return True
            
        except Exception as e:
            print(f"[{self.device}] Failed to wait for page load: {str(e)}")
            return False
    
    def for_animation_complete(self, selector: str, timeout: int = 10):
        """
        Wait for CSS animation to complete
        
        Args:
            selector (str): Element selector
            timeout (int): Timeout in seconds
        """
        try:
            # Wait for animation to complete by checking CSS properties
            element = self.core.page.locator(selector)
            
            start_time = time.time()
            while time.time() - start_time < timeout:
                # Check if animation is still running
                animation_state = element.evaluate("""
                    (el) => {
                        const style = window.getComputedStyle(el);
                        return style.animation || style.transition;
                    }
                """)
                
                if not animation_state or animation_state == 'none':
                    print(f"[{self.device}] Animation completed for: {selector}")
                    return True
                
                time.sleep(0.1)
            
            print(f"[{self.device}] Animation did not complete within {timeout} seconds")
            return False
            
        except Exception as e:
            print(f"[{self.device}] Failed to wait for animation: {str(e)}")
            return False
    
    def for_file_download(self, timeout: int = 30):
        """
        Wait for file download to complete
        
        Args:
            timeout (int): Timeout in seconds
        """
        try:
            # This is a placeholder - in real implementation you'd monitor download directory
            print(f"[{self.device}] Waiting for file download (placeholder)")
            time.sleep(2)  # Simulate wait
            return True
            
        except Exception as e:
            print(f"[{self.device}] Failed to wait for file download: {str(e)}")
            return False
