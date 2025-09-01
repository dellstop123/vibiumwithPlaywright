"""
Forms Vibium functionality
"""

import time
from typing import Optional, Dict, Any, List
from ..core.vibium_core import VibiumCore

class VibiumForms:
    """
    Form automation methods
    """
    
    def __init__(self, device='default', browser_type='chromium', core=None):
        self.device = device
        self.browser_type = browser_type
        # Use the passed core instance instead of creating a new one
        self.core = core if core else VibiumCore(device, browser_type)
    
    def fill_form(self, form_data: Dict[str, str], form_selector: str = "form"):
        """
        Fill a form with data
        
        Args:
            form_data (Dict[str, str]): Dictionary of field names and values
            form_selector (str): Selector for the form
        """
        try:
            form = self.core.page.locator(form_selector)
            
            for field_name, value in form_data.items():
                # Try different selectors for the field
                field_selectors = [
                    f"input[name='{field_name}']",
                    f"input[id='{field_name}']",
                    f"textarea[name='{field_name}']",
                    f"textarea[id='{field_name}']",
                    f"[data-testid='{field_name}']",
                    f".{field_name}-input"
                ]
                
                field = None
                for selector in field_selectors:
                    try:
                        field = form.locator(selector)
                        if field.is_visible():
                            break
                    except:
                        continue
                
                if field and field.is_visible():
                    field.fill(value)
                    print(f"[{self.device}] Filled field '{field_name}' with '{value}'")
                else:
                    print(f"[{self.device}] Warning: Field '{field_name}' not found")
            
            print(f"[{self.device}] Form filled successfully")
            return True
            
        except Exception as e:
            print(f"[{self.device}] Failed to fill form: {str(e)}")
            return False
    
    def submit_form(self, form_selector: str = "form", submit_button_selector: str = None):
        """
        Submit a form
        
        Args:
            form_selector (str): Selector for the form
            submit_button_selector (str): Selector for submit button
        """
        try:
            if submit_button_selector:
                submit_btn = self.core.page.locator(submit_button_selector)
            else:
                # Try to find submit button automatically
                submit_btn = self.core.page.locator(f"{form_selector} input[type='submit'], {form_selector} button[type='submit'], {form_selector} .submit-btn")
            
            submit_btn.click()
            
            # Wait for form submission
            time.sleep(2)
            
            print(f"[{self.device}] Form submitted successfully")
            return True
            
        except Exception as e:
            print(f"[{self.device}] Failed to submit form: {str(e)}")
            return False
    
    def validate_form_errors(self, expected_errors: Dict[str, str]) -> bool:
        """
        Validate form error messages
        
        Args:
            expected_errors (Dict[str, str]): Dictionary of field names and expected error messages
            
        Returns:
            bool: True if all errors match, False otherwise
        """
        try:
            all_valid = True
            
            for field_name, expected_error in expected_errors.items():
                # Try different selectors for error messages
                error_selectors = [
                    f"#{field_name}-error",
                    f".{field_name}-error",
                    f"[data-testid='{field_name}-error']",
                    f"span:has-text('{expected_error}')"
                ]
                
                error_found = False
                for selector in error_selectors:
                    try:
                        error_element = self.core.page.locator(selector)
                        if error_element.is_visible():
                            actual_error = error_element.text_content()
                            if expected_error.lower() in actual_error.lower():
                                print(f"[{self.device}] Error validation passed for '{field_name}': {actual_error}")
                                error_found = True
                                break
                    except:
                        continue
                
                if not error_found:
                    print(f"[{self.device}] Error validation failed for '{field_name}': Expected '{expected_error}'")
                    all_valid = False
            
            return all_valid
            
        except Exception as e:
            print(f"[{self.device}] Failed to validate form errors: {str(e)}")
            return False
    
    def login(self, email: str, password: str, login_form_selector: str = "form"):
        """
        Perform login action
        
        Args:
            email (str): User email
            password (str): User password
            login_form_selector (str): Selector for login form
        """
        try:
            login_data = {
                'email': email,
                'password': password
            }
            
            # Fill login form
            self.fill_form(login_data, login_form_selector)
            
            # Submit form
            self.submit_form(login_form_selector)
            
            print(f"[{self.device}] Login attempted for: {email}")
            return True
            
        except Exception as e:
            print(f"[{self.device}] Failed to perform login: {str(e)}")
            return False
    
    def signup(self, user_data: Dict[str, str], signup_form_selector: str = "form"):
        """
        Perform signup action
        
        Args:
            user_data (Dict[str, str]): User registration data
            signup_form_selector (str): Selector for signup form
        """
        try:
            # Fill signup form
            self.fill_form(user_data, signup_form_selector)
            
            # Submit form
            self.submit_form(signup_form_selector)
            
            print(f"[{self.device}] Signup attempted for: {user_data.get('email', 'unknown')}")
            return True
            
        except Exception as e:
            print(f"[{self.device}] Failed to perform signup: {str(e)}")
            return False
    
    def subscribe_to_newsletter(self, email: str, newsletter_form_selector: str = ".newsletter-form"):
        """
        Subscribe to newsletter
        
        Args:
            email (str): Email address
            newsletter_form_selector (str): Selector for newsletter form
        """
        try:
            newsletter_data = {'email': email}
            
            # Fill newsletter form
            self.fill_form(newsletter_data, newsletter_form_selector)
            
            # Submit form
            self.submit_form(newsletter_form_selector)
            
            print(f"[{self.device}] Newsletter subscription attempted for: {email}")
            return True
            
        except Exception as e:
            print(f"[{self.device}] Failed to subscribe to newsletter: {str(e)}")
            return False
    
    def clear_form(self, form_selector: str = "form"):
        """
        Clear all form fields
        
        Args:
            form_selector (str): Selector for the form
        """
        try:
            form = self.core.page.locator(form_selector)
            
            # Find all input and textarea elements
            inputs = form.locator("input, textarea")
            
            # Get count of inputs
            input_count = inputs.count()
            for i in range(input_count):
                input_element = inputs.nth(i)
                input_element.clear()
            
            print(f"[{self.device}] Form cleared successfully")
            return True
            
        except Exception as e:
            print(f"[{self.device}] Failed to clear form: {str(e)}")
            return False
    
    def is_form_valid(self, form_selector: str = "form") -> bool:
        """
        Check if form is valid (no validation errors)
        
        Args:
            form_selector (str): Selector for the form
            
        Returns:
            bool: True if form is valid, False otherwise
        """
        try:
            form = self.core.page.locator(form_selector)
            
            # Check for error messages
            error_elements = form.locator(".error, .validation-error, [data-testid*='error']")
            
            if error_elements.count() > 0:
                print(f"[{self.device}] Form has validation errors")
                return False
            
            print(f"[{self.device}] Form is valid")
            return True
            
        except Exception as e:
            print(f"[{self.device}] Failed to check form validity: {str(e)}")
            return False
