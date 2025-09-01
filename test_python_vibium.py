#!/usr/bin/env python3
"""
Pytest tests for Python Vibium Library
"""

import pytest
from python_vibium import create_vibium, Vibium

class TestVibiumLibrary:
    """Test class for Vibium library functionality"""
    
    def test_create_vibium(self):
        """Test creating Vibium instance"""
        vibium = create_vibium(device="test", browser_type="chromium")
        assert vibium is not None
        assert hasattr(vibium, 'core')
        assert hasattr(vibium, 'ecommerce')
        assert hasattr(vibium, 'forms')
        assert hasattr(vibium, 'navigation')
        assert hasattr(vibium, 'elements')
        assert hasattr(vibium, 'assertions')
        assert hasattr(vibium, 'performance')
        assert hasattr(vibium, 'screenshots')
        assert hasattr(vibium, 'data')
        assert hasattr(vibium, 'wait')
    
    def test_vibium_class(self):
        """Test Vibium class instantiation"""
        vibium = Vibium(device="test", browser_type="firefox")
        assert vibium is not None
        assert hasattr(vibium, 'core')
        assert hasattr(vibium, 'ecommerce')
        assert hasattr(vibium, 'forms')
        assert hasattr(vibium, 'navigation')
        assert hasattr(vibium, 'elements')
        assert hasattr(vibium, 'assertions')
        assert hasattr(vibium, 'performance')
        assert hasattr(vibium, 'screenshots')
        assert hasattr(vibium, 'data')
        assert hasattr(vibium, 'wait')
    
    def test_data_generation(self):
        """Test data generation methods"""
        vibium = create_vibium(device="test")
        
        # Test email generation
        email = vibium.data.generate_email()
        assert email is not None
        assert "@" in email
        assert "example.com" in email
        
        # Test string generation
        random_string = vibium.data.generate_string(15)
        assert random_string is not None
        assert len(random_string) == 15
        
        # Test user data generation
        user_data = vibium.data.generate_user_data()
        assert user_data is not None
        assert 'first_name' in user_data
        assert 'last_name' in user_data
        assert 'email' in user_data
        assert 'password' in user_data
        
        # Test product data generation
        product_data = vibium.data.generate_product_data()
        assert product_data is not None
        assert 'name' in product_data
        assert 'category' in product_data
        assert 'price' in product_data
        
        # Test address data generation
        address_data = vibium.data.generate_address_data()
        assert address_data is not None
        assert 'street' in address_data
        assert 'city' in address_data
        assert 'state' in address_data
        assert 'zip_code' in address_data
        
        # Test credit card data generation
        credit_card_data = vibium.data.generate_credit_card_data()
        assert credit_card_data is not None
        assert 'number' in credit_card_data
        assert 'expiry_month' in credit_card_data
        assert 'expiry_year' in credit_card_data
        assert 'cvv' in credit_card_data
    
    def test_search_queries_generation(self):
        """Test search queries generation"""
        vibium = create_vibium(device="test")
        
        queries = vibium.data.generate_search_queries(3)
        assert len(queries) == 3
        assert all(isinstance(q, str) for q in queries)
        assert all(len(q) > 0 for q in queries)
    
    def test_newsletter_emails_generation(self):
        """Test newsletter emails generation"""
        vibium = create_vibium(device="test")
        
        emails = vibium.data.generate_newsletter_emails(5)
        assert len(emails) == 5
        assert all("@" in email for email in emails)
        assert all("example.com" in email for email in emails)
    
    def test_coupon_codes_generation(self):
        """Test coupon codes generation"""
        vibium = create_vibium(device="test")
        
        codes = vibium.data.generate_coupon_codes(3)
        assert len(codes) == 3
        assert all(len(code) > 0 for code in codes)
        assert all(any(prefix in code for prefix in ['SAVE', 'DISCOUNT', 'OFFER', 'DEAL']) for code in codes)
    
    def test_test_scenarios_generation(self):
        """Test test scenarios generation"""
        vibium = create_vibium(device="test")
        
        scenarios = vibium.data.generate_test_scenarios()
        assert len(scenarios) > 0
        assert all('name' in scenario for scenario in scenarios)
        assert all('user_type' in scenario for scenario in scenarios)
        assert all('products' in scenario for scenario in scenarios)
    
    def test_order_data_generation(self):
        """Test order data generation"""
        vibium = create_vibium(device="test")
        
        order_data = vibium.data.generate_order_data()
        assert order_data is not None
        assert 'order_number' in order_data
        assert 'items' in order_data
        assert 'shipping_address' in order_data
        assert 'billing_address' in order_data
        assert 'payment_method' in order_data
        assert 'subtotal' in order_data
        assert 'tax' in order_data
        assert 'shipping' in order_data
        assert 'total' in order_data
        
        # Verify calculations
        assert order_data['subtotal'] == sum(item['price'] for item in order_data['items'])
        assert order_data['total'] == order_data['subtotal'] + order_data['tax'] + order_data['shipping']

class TestVibiumCore:
    """Test class for Vibium core functionality"""
    
    def test_vibium_core_initialization(self):
        """Test VibiumCore initialization"""
        from python_vibium.core.vibium_core import VibiumCore
        
        core = VibiumCore(device="test", browser_type="chromium")
        assert core.device == "test"
        assert core.browser_type == "chromium"
        assert core.is_initialized == False
        assert core.page is None
        assert core.browser is None
        assert core.context is None
        assert core.playwright is None

class TestVibiumEcommerce:
    """Test class for Vibium e-commerce functionality"""
    
    def test_vibium_ecommerce_initialization(self):
        """Test VibiumEcommerce initialization"""
        from python_vibium.ecommerce.vibium_ecommerce import VibiumEcommerce
        
        ecommerce = VibiumEcommerce(device="test", browser_type="chromium")
        assert ecommerce.device == "test"
        assert ecommerce.browser_type == "chromium"
        assert hasattr(ecommerce, 'core')

class TestVibiumForms:
    """Test class for Vibium forms functionality"""
    
    def test_vibium_forms_initialization(self):
        """Test VibiumForms initialization"""
        from python_vibium.forms.vibium_forms import VibiumForms
        
        forms = VibiumForms(device="test", browser_type="chromium")
        assert forms.device == "test"
        assert forms.browser_type == "chromium"
        assert hasattr(forms, 'core')

class TestVibiumNavigation:
    """Test class for Vibium navigation functionality"""
    
    def test_vibium_navigation_initialization(self):
        """Test VibiumNavigation initialization"""
        from python_vibium.navigation.vibium_navigation import VibiumNavigation
        
        navigation = VibiumNavigation(device="test", browser_type="chromium")
        assert navigation.device == "test"
        assert navigation.browser_type == "chromium"
        assert hasattr(navigation, 'core')

class TestVibiumElements:
    """Test class for Vibium elements functionality"""
    
    def test_vibium_elements_initialization(self):
        """Test VibiumElements initialization"""
        from python_vibium.elements.vibium_elements import VibiumElements
        
        elements = VibiumElements(device="test", browser_type="chromium")
        assert elements.device == "test"
        assert elements.browser_type == "chromium"
        assert hasattr(elements, 'core')

class TestVibiumAssertions:
    """Test class for Vibium assertions functionality"""
    
    def test_vibium_assertions_initialization(self):
        """Test VibiumAssertions initialization"""
        from python_vibium.assertions.vibium_assertions import VibiumAssertions
        
        assertions = VibiumAssertions(device="test", browser_type="chromium")
        assert assertions.device == "test"
        assert assertions.browser_type == "chromium"
        assert hasattr(assertions, 'core')

class TestVibiumPerformance:
    """Test class for Vibium performance functionality"""
    
    def test_vibium_performance_initialization(self):
        """Test VibiumPerformance initialization"""
        from python_vibium.performance.vibium_performance import VibiumPerformance
        
        performance = VibiumPerformance(device="test", browser_type="chromium")
        assert performance.device == "test"
        assert performance.browser_type == "chromium"
        assert hasattr(performance, 'core')

class TestVibiumScreenshots:
    """Test class for Vibium screenshots functionality"""
    
    def test_vibium_screenshots_initialization(self):
        """Test VibiumScreenshots initialization"""
        from python_vibium.screenshots.vibium_screenshots import VibiumScreenshots
        
        screenshots = VibiumScreenshots(device="test", browser_type="chromium")
        assert screenshots.device == "test"
        assert screenshots.browser_type == "chromium"
        assert hasattr(screenshots, 'core')
        assert screenshots.screenshot_dir == "screenshots"

class TestVibiumWait:
    """Test class for Vibium wait functionality"""
    
    def test_vibium_wait_initialization(self):
        """Test VibiumWait initialization"""
        from python_vibium.wait.vibium_wait import VibiumWait
        
        wait = VibiumWait(device="test", browser_type="chromium")
        assert wait.device == "test"
        assert wait.browser_type == "chromium"
        assert hasattr(wait, 'core')

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
