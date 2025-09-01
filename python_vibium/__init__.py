"""
Python Vibium Library for UI Automation
A comprehensive testing framework built on top of Playwright and Selenium
"""

from .core.vibium_core import VibiumCore
from .ecommerce.vibium_ecommerce import VibiumEcommerce
from .forms.vibium_forms import VibiumForms
from .navigation.vibium_navigation import VibiumNavigation
from .elements.vibium_elements import VibiumElements
from .assertions.vibium_assertions import VibiumAssertions
from .performance.vibium_performance import VibiumPerformance
from .screenshots.vibium_screenshots import VibiumScreenshots
from .data.vibium_data import VibiumData
from .wait.vibium_wait import VibiumWait

__version__ = "1.0.0"
__author__ = "Vibium Team"

def create_vibium(device='default', browser_type='chromium'):
    """
    Create a new Vibium instance for UI automation
    
    Args:
        device (str): Device identifier
        browser_type (str): Browser type (chromium, firefox, webkit)
    
    Returns:
        Vibium: Configured Vibium instance
    """
    return Vibium(device, browser_type)

class Vibium:
    """
    Main Vibium class that provides access to all automation modules
    """
    
    def __init__(self, device='default', browser_type='chromium'):
        # Create the core instance first
        self.core = VibiumCore(device, browser_type)
        
        # Pass the core instance to all modules so they can access the initialized page
        self.ecommerce = VibiumEcommerce(device, browser_type, self.core)
        self.forms = VibiumForms(device, browser_type, self.core)
        self.navigation = VibiumNavigation(device, browser_type, self.core)
        self.elements = VibiumElements(device, browser_type, self.core)
        self.assertions = VibiumAssertions(device, browser_type, self.core)
        self.performance = VibiumPerformance(device, browser_type, self.core)
        self.screenshots = VibiumScreenshots(device, browser_type, self.core)
        self.data = VibiumData(device, browser_type, self.core)
        self.wait = VibiumWait(device, browser_type, self.core)
    
    def do(self, command):
        """Execute a command using the core Vibium instance"""
        return self.core.do(command)
    
    def check(self, question):
        """Check a condition using the core Vibium instance"""
        return self.core.check(question)
