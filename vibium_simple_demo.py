#!/usr/bin/env python3
"""
Vibium Simple Demo
Basic demonstration of Vibium library capabilities
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from python_vibium import create_vibium, Vibium
import time

def demo_basic_usage():
    """Demonstrate basic Vibium usage"""
    print("🚀 Vibium Basic Demo")
    print("=" * 40)
    
    try:
        # Create Vibium instance
        print("1️⃣ Creating Vibium instance...")
        vibium = create_vibium(device="demo", browser_type="chromium")
        
        # Initialize browser
        print("2️⃣ Initializing browser...")
        if not vibium.core.initialize(headless=False):
            print("❌ Failed to initialize browser")
            return False
        
        print("✅ Browser initialized successfully!")
        
        # Navigate to website
        print("3️⃣ Navigating to website...")
        vibium.navigation.goto("https://ecommercepracticeportal.netlify.app/")
        vibium.wait.for_page_load()
        
        print("✅ Website loaded successfully!")
        
        # Take screenshot
        print("4️⃣ Taking screenshot...")
        screenshot_path = vibium.screenshots.capture("demo_homepage")
        print(f"📸 Screenshot saved: {screenshot_path}")
        
        # Generate some test data
        print("5️⃣ Generating test data...")
        user_data = vibium.data.generate_user_data()
        print(f"👤 User: {user_data['first_name']} {user_data['last_name']}")
        print(f"📧 Email: {user_data['email']}")
        
        address_data = vibium.data.generate_address_data()
        print(f"📍 Address: {address_data['street']}, {address_data['city']}")
        
        # Wait a bit to see the page
        print("⏳ Waiting 3 seconds to view the page...")
        time.sleep(3)
        
        # Close browser
        print("6️⃣ Closing browser...")
        vibium.core.close()
        print("✅ Browser closed successfully!")
        
        print("\n🎉 Basic demo completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        return False

def demo_data_generation():
    """Demonstrate data generation capabilities"""
    print("\n🎲 Vibium Data Generation Demo")
    print("=" * 40)
    
    try:
        # Create Vibium instance (no browser needed for data generation)
        vibium = create_vibium(device="data_demo", browser_type="chromium")
        
        print("1️⃣ Generating user data...")
        user = vibium.data.generate_user_data()
        print(f"   👤 {user['first_name']} {user['last_name']}")
        print(f"   📧 {user['email']}")
        print(f"   🔑 {user['password']}")
        print(f"   📱 {user['phone']}")
        
        print("\n2️⃣ Generating address data...")
        address = vibium.data.generate_address_data()
        print(f"   🏠 {address['street']}")
        print(f"   🏙️ {address['city']}, {address['state']} {address['zip_code']}")
        print(f"   🌍 {address['country']}")
        
        print("\n3️⃣ Generating product data...")
        product = vibium.data.generate_product_data()
        print(f"   📦 {product['name']}")
        print(f"   💰 ${product['price']}")
        print(f"   📝 {product['description'][:50]}...")
        
        print("\n4️⃣ Generating credit card data...")
        card = vibium.data.generate_credit_card_data()
        print(f"   💳 {card['cardholder_name']}")
        print(f"   🔢 {card['card_number']}")
        print(f"   📅 {card['expiry_month']}/{card['expiry_year']}")
        
        print("\n5️⃣ Generating coupon codes...")
        coupons = vibium.data.generate_coupon_codes(3)
        for i, coupon in enumerate(coupons, 1):
            print(f"   🎫 Coupon {i}: {coupon}")
        
        print("\n6️⃣ Generating order data...")
        order = vibium.data.generate_order_data()
        print(f"   🛒 Order ID: {order['order_id']}")
        print(f"   📊 Status: {order['status']}")
        print(f"   💵 Total: ${order['total_amount']}")
        
        print("\n✅ Data generation demo completed!")
        return True
        
    except Exception as e:
        print(f"❌ Data generation demo failed: {str(e)}")
        return False

def demo_form_automation():
    """Demonstrate form automation capabilities"""
    print("\n📝 Vibium Form Automation Demo")
    print("=" * 40)
    
    try:
        # Create Vibium instance
        print("1️⃣ Creating Vibium instance...")
        vibium = create_vibium(device="form_demo", browser_type="chromium")
        
        # Initialize browser
        print("2️⃣ Initializing browser...")
        if not vibium.core.initialize(headless=False):
            print("❌ Failed to initialize browser")
            return False
        
        print("✅ Browser initialized successfully!")
        
        # Navigate to website
        print("3️⃣ Navigating to website...")
        vibium.navigation.goto("https://ecommercepracticeportal.netlify.app/")
        vibium.wait.for_page_load()
        
        print("✅ Website loaded successfully!")
        
        # Generate test data
        print("4️⃣ Generating test data...")
        user_data = vibium.data.generate_user_data()
        address_data = vibium.data.generate_address_data()
        
        # Look for forms on the page
        print("5️⃣ Looking for forms...")
        form_selectors = ["form", ".form", "[data-testid*='form']"]
        
        form_found = False
        for selector in form_selectors:
            try:
                if vibium.assertions.is_visible(selector):
                    print(f"✅ Form found: {selector}")
                    form_found = True
                    
                    # Take screenshot of form
                    form_screenshot = vibium.screenshots.capture(f"form_{selector.replace('.', '').replace('[', '').replace(']', '')}")
                    print(f"📸 Form screenshot: {form_screenshot}")
                    
                    # Try to fill the form
                    print("6️⃣ Attempting to fill form...")
                    form_data = {
                        'first_name': user_data['first_name'],
                        'last_name': user_data['last_name'],
                        'email': user_data['email'],
                        'phone': user_data['phone'],
                        'address': address_data['street'],
                        'city': address_data['city'],
                        'state': address_data['state'],
                        'zip_code': address_data['zip_code']
                    }
                    
                    fill_success = vibium.forms.fill_form(form_data, selector)
                    print(f"✍️ Form filled: {fill_success}")
                    
                    break
            except:
                continue
        
        if not form_found:
            print("⚠️ No forms found on the page")
            
            # Take general page screenshot
            page_screenshot = vibium.screenshots.capture("no_forms_page")
            print(f"📸 Page screenshot: {page_screenshot}")
        
        # Test newsletter subscription
        print("7️⃣ Testing newsletter subscription...")
        newsletter_email = vibium.data.generate_email()
        newsletter_success = vibium.forms.subscribe_to_newsletter(newsletter_email)
        print(f"📧 Newsletter subscription: {newsletter_success}")
        
        # Wait to see the results
        print("⏳ Waiting 3 seconds to view the results...")
        time.sleep(3)
        
        # Close browser
        print("8️⃣ Closing browser...")
        vibium.core.close()
        print("✅ Browser closed successfully!")
        
        print("\n🎉 Form automation demo completed!")
        return True
        
    except Exception as e:
        print(f"❌ Form automation demo failed: {str(e)}")
        return False

def main():
    """Main function to run demos"""
    print("🎯 Vibium Library Demo Suite")
    print("=" * 50)
    
    demos = [
        ("Basic Usage", demo_basic_usage),
        ("Data Generation", demo_data_generation),
        ("Form Automation", demo_form_automation)
    ]
    
    success_count = 0
    total_demos = len(demos)
    
    for demo_name, demo_func in demos:
        print(f"\n{'='*60}")
        print(f"🔄 Running {demo_name} Demo...")
        print(f"{'='*60}")
        
        try:
            if demo_func():
                success_count += 1
                print(f"✅ {demo_name} demo completed successfully!")
            else:
                print(f"❌ {demo_name} demo failed!")
        except Exception as e:
            print(f"💥 {demo_name} demo crashed: {str(e)}")
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 DEMO SUMMARY")
    print(f"{'='*60}")
    print(f"Total Demos: {total_demos}")
    print(f"✅ Successful: {success_count}")
    print(f"❌ Failed: {total_demos - success_count}")
    print(f"📈 Success Rate: {(success_count/total_demos*100):.1f}%")
    print(f"{'='*60}")
    
    if success_count == total_demos:
        print("🎉 All demos completed successfully!")
        return 0
    else:
        print("💥 Some demos failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
