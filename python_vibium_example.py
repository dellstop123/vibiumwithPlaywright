#!/usr/bin/env python3
"""
Python Vibium Library Example
Demonstrates usage of the custom Vibium testing framework
"""

from python_vibium import create_vibium, Vibium
import time

def main():
    """Main function demonstrating Vibium usage"""
    
    print("=== Python Vibium Library Demo ===\n")
    
    # Create Vibium instance
    print("1. Creating Vibium instance...")
    vibium = create_vibium(device="demo", browser_type="chromium")
    
    # Initialize browser
    print("2. Initializing browser...")
    if not vibium.core.initialize(headless=False):
        print("Failed to initialize browser")
        return
    
    try:
        # Basic navigation
        print("\n3. Testing basic navigation...")
        vibium.navigation.goto("https://ecommercepracticeportal.netlify.app/", "E-commerce")
        
        # Wait for page load
        vibium.wait.for_page_load()
        
        # Take screenshot
        print("\n4. Taking screenshot...")
        screenshot_path = vibium.screenshots.capture("homepage_demo")
        print(f"Screenshot saved to: {screenshot_path}")
        
        # Test e-commerce functionality
        print("\n5. Testing e-commerce functions...")
        
        # Search for products
        vibium.ecommerce.search_products("laptop")
        vibium.wait.for_network_idle()
        
        # Navigate to category
        vibium.ecommerce.navigate_to_category("Electronics")
        vibium.wait.for_network_idle()
        
        # Test form handling
        print("\n6. Testing form handling...")
        
        # Generate test data
        user_data = vibium.data.generate_user_data()
        newsletter_email = vibium.data.generate_email()
        
        # Test newsletter subscription
        vibium.forms.subscribe_to_newsletter(newsletter_email)
        
        # Test assertions
        print("\n7. Testing assertions...")
        
        # Check if elements are visible
        vibium.assertions.is_visible("header")
        vibium.assertions.is_visible("footer")
        
        # Check page title
        vibium.assertions.title_contains("E-commerce")
        
        # Test performance
        print("\n8. Testing performance...")
        
        # Measure load time
        load_time = vibium.performance.measure_load_time("https://ecommercepracticeportal.netlify.app/")
        print(f"Page load time: {load_time:.2f} seconds")
        
        # Check Core Web Vitals
        web_vitals = vibium.performance.check_core_web_vitals()
        print(f"Core Web Vitals: {web_vitals}")
        
        # Test element interactions
        print("\n9. Testing element interactions...")
        
        # Wait for element stability
        vibium.elements.wait_for_stable("header")
        
        # Test data generation
        print("\n10. Testing data generation...")
        
        # Generate various test data
        product_data = vibium.data.generate_product_data()
        address_data = vibium.data.generate_address_data()
        credit_card_data = vibium.data.generate_credit_card_data()
        
        print(f"Generated product: {product_data}")
        print(f"Generated address: {address_data}")
        print(f"Generated credit card: {credit_card_data}")
        
        # Test wait utilities
        print("\n11. Testing wait utilities...")
        
        # Wait for specific conditions
        vibium.wait.for_network_idle(10)
        vibium.wait.for_timeout(2)
        
        print("\n=== Demo completed successfully! ===")
        
    except Exception as e:
        print(f"Error during demo: {str(e)}")
        
    finally:
        # Cleanup
        print("\nCleaning up...")
        vibium.core.close()

def demo_vibium_class():
    """Demonstrate using the Vibium class directly"""
    
    print("\n=== Vibium Class Demo ===\n")
    
    # Create Vibium instance using the class
    vibium = Vibium(device="class_demo", browser_type="chromium")
    
    # Initialize browser
    if not vibium.core.initialize(headless=False):
        print("Failed to initialize browser")
        return
    
    try:
        # Test basic commands
        print("1. Testing basic commands...")
        vibium.do("goto https://ecommercepracticeportal.netlify.app/")
        
        # Test basic checks
        print("2. Testing basic checks...")
        vibium.check("title contains E-commerce")
        vibium.check("element visible header")
        
        # Test e-commerce functions
        print("3. Testing e-commerce functions...")
        vibium.ecommerce.search_products("smartphone")
        
        # Test form functions
        print("4. Testing form functions...")
        test_email = vibium.data.generate_email()
        vibium.forms.subscribe_to_newsletter(test_email)
        
        print("\n=== Vibium Class Demo completed! ===")
        
    except Exception as e:
        print(f"Error during class demo: {str(e)}")
        
    finally:
        # Cleanup
        print("\nCleaning up...")
        vibium.core.close()

if __name__ == "__main__":
    # Run the main demo
    main()
    
    # Run the class demo
    demo_vibium_class()
    
    print("\nAll demos completed!")
