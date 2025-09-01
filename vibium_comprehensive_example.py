#!/usr/bin/env python3
"""
Vibium Comprehensive Example
Showing various Vibium commands and syntax patterns
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from python_vibium import Vibium
import time

def main():
    """Main function demonstrating comprehensive Vibium usage"""
    print("🚀 Vibium Comprehensive Example")
    print("=" * 50)
    
    try:
        # Create Vibium instance
        print("1️⃣ Creating Vibium instance...")
        vibe = Vibium(device='desktop', browser_type='chromium')
        
        # Initialize the browser
        print("2️⃣ Initializing browser...")
        if not vibe.core.initialize(headless=False):
            print("❌ Failed to initialize browser")
            return False
        
        print("✅ Browser initialized successfully!")
        
        # Basic navigation commands
        print("\n3️⃣ Basic Navigation Commands")
        print("-" * 30)
        
        vibe.do("open https://ecommercepracticeportal.netlify.app/")
        vibe.wait.for_page_load()
        print("✅ Opened e-commerce portal")
        
        # Check page elements
        print("\n4️⃣ Element Checking Commands")
        print("-" * 30)
        
        # Check if page loaded
        vibe.check("is the page loaded?")
        print("✅ Page load check completed")
        
        # Check for specific elements
        vibe.check("do you see a header?")
        vibe.check("do you see a main content area?")
        vibe.check("do you see a footer?")
        print("✅ Element visibility checks completed")
        
        # Take screenshots
        print("\n5️⃣ Screenshot Commands")
        print("-" * 30)
        
        vibe.screenshots.capture("homepage_full")
        vibe.screenshots.capture("homepage_viewport")
        print("✅ Screenshots captured")
        
        # Generate test data
        print("\n6️⃣ Data Generation Commands")
        print("-" * 30)
        
        user_data = vibe.data.generate_user_data()
        print(f"👤 Generated user: {user_data['first_name']} {user_data['last_name']}")
        
        address_data = vibe.data.generate_address_data()
        print(f"📍 Generated address: {address_data['city']}, {address_data['state']}")
        
        # Form interactions
        print("\n7️⃣ Form Interaction Commands")
        print("-" * 30)
        
        # Look for forms
        vibe.check("are there any forms on the page?")
        
        # Try to fill a form if found
        try:
            vibe.forms.fill_form(user_data, "form")
            print("✅ Form filled with generated data")
        except:
            print("⚠️ No suitable form found to fill")
        
        # E-commerce specific commands
        print("\n8️⃣ E-commerce Commands")
        print("-" * 30)
        
        # Search for products
        vibe.ecommerce.search_products("laptop")
        vibe.wait.for_network_idle()
        print("✅ Searched for laptops")
        
        # Check search results
        vibe.check("are there search results displayed?")
        
        # Add to cart
        vibe.ecommerce.add_to_cart(".product-item, .product-card", quantity=1)
        print("✅ Added product to cart")
        
        # Check cart
        cart_count = vibe.ecommerce.get_cart_count()
        print(f"🛒 Cart count: {cart_count}")
        
        # Performance testing
        print("\n9️⃣ Performance Commands")
        print("-" * 30)
        
        load_time = vibe.performance.measure_page_load_time()
        print(f"⏱️ Page load time: {load_time:.2f} seconds")
        
        # Wait to see results
        print("\n⏳ Waiting 3 seconds to view the results...")
        time.sleep(3)
        
        # Final screenshot
        vibe.screenshots.capture("comprehensive_example_final")
        print("📸 Final screenshot captured")
        
        # Close browser
        print("\n🔚 Closing browser...")
        vibe.core.close()
        print("✅ Browser closed successfully!")
        
        print("\n🎉 Comprehensive Vibium example completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Comprehensive example failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

