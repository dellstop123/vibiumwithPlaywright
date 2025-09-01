"""
Screenshots Vibium functionality
"""

import os
import time
from typing import Optional, Dict, Any
from ..core.vibium_core import VibiumCore

class VibiumScreenshots:
    """
    Screenshot and visual testing methods
    """
    
    def __init__(self, device='default', browser_type='chromium', core=None):
        self.device = device
        self.browser_type = browser_type
        # Use the passed core instance instead of creating a new one
        self.core = core if core else VibiumCore(device, browser_type)
        self.screenshot_dir = "screenshots"
        self._ensure_screenshot_dir()
    
    def _ensure_screenshot_dir(self):
        """Ensure screenshot directory exists"""
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)
            print(f"[{self.device}] Created screenshot directory: {self.screenshot_dir}")
    
    def capture(self, filename: str = None, full_page: bool = True) -> Optional[str]:
        """
        Capture a screenshot
        
        Args:
            filename (str): Custom filename for screenshot
            full_page (bool): Whether to capture full page
            
        Returns:
            str: Path to screenshot file or None if failed
        """
        try:
            if not filename:
                timestamp = int(time.time())
                filename = f"screenshot_{timestamp}.png"
            
            # Ensure filename has .png extension
            if not filename.endswith('.png'):
                filename += '.png'
            
            filepath = os.path.join(self.screenshot_dir, filename)
            
            # Check if core is initialized and has a page
            if not self.core.is_initialized or not self.core.page:
                print(f"[{self.device}] Cannot take screenshot: Browser not initialized")
                return None
            
            # Take screenshot
            self.core.page.screenshot(path=filepath, full_page=full_page)
            
            print(f"[{self.device}] Screenshot captured: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"[{self.device}] Failed to capture screenshot: {str(e)}")
            return None
    
    def capture_element(self, selector: str, filename: str = None) -> Optional[str]:
        """
        Capture screenshot of specific element
        
        Args:
            selector (str): Element selector
            filename (str): Custom filename for screenshot
            
        Returns:
            str: Path to screenshot file or None if failed
        """
        try:
            if not filename:
                timestamp = int(time.time())
                filename = f"element_{timestamp}.png"
            
            # Ensure filename has .png extension
            if not filename.endswith('.png'):
                filename += '.png'
            
            filepath = os.path.join(self.screenshot_dir, filename)
            
            # Find element and take screenshot
            element = self.core.page.locator(selector)
            element.screenshot(path=filepath)
            
            print(f"[{self.device}] Element screenshot captured: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"[{self.device}] Failed to capture element screenshot: {str(e)}")
            return None
    
    def capture_on_failure(self, test_name: str = "test") -> Optional[str]:
        """
        Capture screenshot on test failure
        
        Args:
            test_name (str): Name of the test
            
        Returns:
            str: Path to screenshot file or None if failed
        """
        try:
            timestamp = int(time.time())
            filename = f"failure_{test_name}_{timestamp}.png"
            filepath = os.path.join(self.screenshot_dir, filename)
            
            # Take screenshot
            self.core.page.screenshot(path=filepath, full_page=True)
            
            print(f"[{self.device}] Failure screenshot captured: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"[{self.device}] Failed to capture failure screenshot: {str(e)}")
            return None
    
    def capture_before_after(self, action_name: str, before_action: callable, after_action: callable) -> Dict[str, str]:
        """
        Capture before and after screenshots of an action
        
        Args:
            action_name (str): Name of the action
            before_action (callable): Function to execute before screenshot
            after_action (callable): Function to execute after screenshot
            
        Returns:
            Dict[str, str]: Paths to before and after screenshots
        """
        try:
            timestamp = int(time.time())
            
            # Execute before action and take screenshot
            before_action()
            before_filename = f"before_{action_name}_{timestamp}.png"
            before_path = self.capture(before_filename)
            
            # Execute after action and take screenshot
            after_action()
            after_filename = f"after_{action_name}_{timestamp}.png"
            after_path = self.capture(after_filename)
            
            result = {
                'before': before_path,
                'after': after_path
            }
            
            print(f"[{self.device}] Before/after screenshots captured for {action_name}")
            return result
            
        except Exception as e:
            print(f"[{self.device}] Failed to capture before/after screenshots: {str(e)}")
            return {'before': None, 'after': None}
    
    def capture_viewport_sizes(self, sizes: list) -> Dict[str, str]:
        """
        Capture screenshots at different viewport sizes
        
        Args:
            sizes (list): List of viewport sizes as (width, height) tuples
            
        Returns:
            Dict[str, str]: Paths to screenshots for each size
        """
        try:
            results = {}
            
            for width, height in sizes:
                # Set viewport size
                self.core.page.set_viewport_size({'width': width, 'height': height})
                
                # Wait for resize
                time.sleep(1)
                
                # Take screenshot
                filename = f"viewport_{width}x{height}_{int(time.time())}.png"
                filepath = self.capture(filename)
                
                if filepath:
                    results[f"{width}x{height}"] = filepath
            
            print(f"[{self.device}] Viewport screenshots captured for {len(sizes)} sizes")
            return results
            
        except Exception as e:
            print(f"[{self.device}] Failed to capture viewport screenshots: {str(e)}")
            return {}
    
    def compare_screenshots(self, screenshot1: str, screenshot2: str, threshold: float = 0.95) -> bool:
        """
        Compare two screenshots for similarity
        
        Args:
            screenshot1 (str): Path to first screenshot
            screenshot2 (str): Path to second screenshot
            threshold (float): Similarity threshold (0-1)
            
        Returns:
            bool: True if screenshots are similar
        """
        try:
            # This is a placeholder for actual image comparison
            # In a real implementation, you would use PIL or similar library
            
            print(f"[{self.device}] Screenshot comparison requested: {screenshot1} vs {screenshot2}")
            print(f"[{self.device}] Threshold: {threshold}")
            
            # For now, just check if files exist
            if os.path.exists(screenshot1) and os.path.exists(screenshot2):
                print(f"[{self.device}] Both screenshot files exist")
                return True
            else:
                print(f"[{self.device}] One or both screenshot files missing")
                return False
                
        except Exception as e:
            print(f"[{self.device}] Failed to compare screenshots: {str(e)}")
            return False
    
    def cleanup_old_screenshots(self, max_age_hours: int = 24):
        """
        Clean up old screenshot files
        
        Args:
            max_age_hours (int): Maximum age of screenshots in hours
        """
        try:
            current_time = time.time()
            max_age_seconds = max_age_hours * 3600
            
            deleted_count = 0
            
            for filename in os.listdir(self.screenshot_dir):
                if filename.endswith('.png'):
                    filepath = os.path.join(self.screenshot_dir, filename)
                    file_age = current_time - os.path.getmtime(filepath)
                    
                    if file_age > max_age_seconds:
                        os.remove(filepath)
                        deleted_count += 1
            
            if deleted_count > 0:
                print(f"[{self.device}] Cleaned up {deleted_count} old screenshots")
            else:
                print(f"[{self.device}] No old screenshots to clean up")
                
        except Exception as e:
            print(f"[{self.device}] Failed to cleanup old screenshots: {str(e)}")
    
    def get_screenshot_info(self, filepath: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a screenshot file
        
        Args:
            filepath (str): Path to screenshot file
            
        Returns:
            Dict[str, Any]: Screenshot information
        """
        try:
            if not os.path.exists(filepath):
                return None
            
            stat = os.stat(filepath)
            
            info = {
                'filename': os.path.basename(filepath),
                'size_bytes': stat.st_size,
                'created_time': stat.st_ctime,
                'modified_time': stat.st_mtime,
                'file_path': filepath
            }
            
            print(f"[{self.device}] Screenshot info: {info}")
            return info
            
        except Exception as e:
            print(f"[{self.device}] Failed to get screenshot info: {str(e)}")
            return None
