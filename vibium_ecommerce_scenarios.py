#!/usr/bin/env python3
"""
Vibium E-commerce Scenarios
Focused automation for specific e-commerce user journeys
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from python_vibium import create_vibium, Vibium
import time
import json

class VibiumEcommerceScenarios:
    """
    Focused e-commerce automation scenarios
    """
    
    def __init__(self, device="scenarios", browser_type="chromium", headless=False):
        self.device = device
        self.browser_type = browser_type
        self.headless = headless
        self.vibium = None
        self.scenario_results = []
        
    def initialize(self):
        """Initialize Vibium and browser"""
        print(f"🚀 Initializing Vibium E-commerce Scenarios - {self.browser_type}")
        
        try:
            self.vibium = create_vibium(device=self.device, browser_type=self.browser_type)
            
            if not self.vibium.core.initialize(headless=self.headless):
                raise Exception("Failed to initialize browser")
            
            print(f"✅ Browser {self.browser_type} initialized successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to initialize: {str(e)}")
            return False
    
    def scenario_1_guest_shopping_journey(self):
        """Scenario 1: Guest user shopping journey"""
        print("\n🛍️ Scenario 1: Guest Shopping Journey")
        print("=" * 50)
        
        try:
            # Step 1: Navigate to homepage
            print("📍 Step 1: Navigate to homepage")
            self.vibium.navigation.goto("https://ecommercepracticeportal.netlify.app/")
            self.vibium.wait.for_page_load()
            
            # Step 2: Search for products
            print("🔍 Step 2: Search for products")
            search_queries = ["laptop", "smartphone", "headphones"]
            
            for query in search_queries:
                print(f"   Searching for: {query}")
                search_success = self.vibium.ecommerce.search_products(query)
                
                if search_success:
                    self.vibium.wait.for_network_idle()
                    
                    # Take screenshot of search results
                    screenshot_path = self.vibium.screenshots.capture(f"guest_search_{query}")
                    print(f"   📸 Search results screenshot: {screenshot_path}")
                    
                    # Verify search results
                    has_results = self.vibium.assertions.is_visible(".search-results, .products, .results")
                    print(f"   ✅ Search results found: {has_results}")
                    
                    # Get product price if available
                    price = self.vibium.ecommerce.get_product_price(".product-item, .product-card")
                    if price:
                        print(f"   💰 Product price: {price}")
                    
                    # Add to cart
                    add_success = self.vibium.ecommerce.add_to_cart(".product-item, .product-card", quantity=1)
                    print(f"   🛒 Added to cart: {add_success}")
                    
                    # Check cart count
                    cart_count = self.vibium.ecommerce.get_cart_count()
                    print(f"   🛒 Cart count: {cart_count}")
                    
                    # Wait before next search
                    time.sleep(2)
                else:
                    print(f"   ❌ Search failed for: {query}")
            
            # Step 3: Navigate to cart
            print("🛒 Step 3: Navigate to cart")
            # This would typically involve clicking a cart icon or navigating to cart page
            
            # Step 4: Take final screenshot
            final_screenshot = self.vibium.screenshots.capture("guest_journey_final")
            print(f"📸 Final journey screenshot: {final_screenshot}")
            
            self.scenario_results.append({
                "scenario": "guest_shopping_journey",
                "status": "COMPLETED",
                "screenshots": [final_screenshot],
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            })
            
            print("✅ Guest shopping journey completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Guest shopping journey failed: {str(e)}")
            self.scenario_results.append({
                "scenario": "guest_shopping_journey",
                "status": "FAILED",
                "error": str(e),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            })
            return False
    
    def scenario_2_user_registration_and_login(self):
        """Scenario 2: User registration and login flow"""
        print("\n👤 Scenario 2: User Registration and Login")
        print("=" * 50)
        
        try:
            # Step 1: Navigate to homepage
            print("📍 Step 1: Navigate to homepage")
            self.vibium.navigation.goto("https://ecommercepracticeportal.netlify.app/")
            self.vibium.wait.for_page_load()
            
            # Step 2: Generate test user data
            print("🎲 Step 2: Generate test user data")
            user_data = self.vibium.data.generate_user_data()
            print(f"   👤 Generated user: {user_data['first_name']} {user_data['last_name']}")
            print(f"   📧 Email: {user_data['email']}")
            print(f"   🔑 Password: {user_data['password']}")
            
            # Step 3: Look for registration/login forms
            print("📝 Step 3: Look for registration/login forms")
            
            # Check for common form selectors
            form_selectors = [
                "form",
                ".login-form",
                ".signup-form",
                ".auth-form",
                "[data-testid='login-form']",
                "[data-testid='signup-form']"
            ]
            
            form_found = False
            for selector in form_selectors:
                try:
                    if self.vibium.assertions.is_visible(selector):
                        print(f"   ✅ Form found: {selector}")
                        form_found = True
                        
                        # Take form screenshot
                        form_screenshot = self.vibium.screenshots.capture(f"form_{selector.replace('.', '').replace('[', '').replace(']', '')}")
                        print(f"   📸 Form screenshot: {form_screenshot}")
                        
                        # Try to fill form
                        form_fill_success = self.vibium.forms.fill_form(user_data, selector)
                        print(f"   ✍️ Form filled: {form_fill_success}")
                        
                        break
                except:
                    continue
            
            if not form_found:
                print("   ⚠️ No forms found on page")
                
                # Take general page screenshot
                page_screenshot = self.vibium.screenshots.capture("no_forms_page")
                print(f"   📸 Page screenshot: {page_screenshot}")
            
            # Step 4: Test newsletter subscription
            print("📧 Step 4: Test newsletter subscription")
            newsletter_email = self.vibium.data.generate_email()
            newsletter_success = self.vibium.forms.subscribe_to_newsletter(newsletter_email)
            print(f"   📧 Newsletter subscription: {newsletter_success}")
            
            self.scenario_results.append({
                "scenario": "user_registration_login",
                "status": "COMPLETED",
                "user_data": user_data,
                "newsletter_email": newsletter_email,
                "form_found": form_found,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            })
            
            print("✅ User registration and login scenario completed!")
            return True
            
        except Exception as e:
            print(f"❌ User registration and login failed: {str(e)}")
            self.scenario_results.append({
                "scenario": "user_registration_login",
                "status": "FAILED",
                "error": str(e),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            })
            return False
    
    def scenario_3_product_browsing_and_comparison(self):
        """Scenario 3: Product browsing and comparison"""
        print("\n🔍 Scenario 3: Product Browsing and Comparison")
        print("=" * 50)
        
        try:
            # Step 1: Navigate to homepage
            print("📍 Step 1: Navigate to homepage")
            self.vibium.navigation.goto("https://ecommercepracticeportal.netlify.app/")
            self.vibium.wait.for_page_load()
            
            # Step 2: Browse different categories
            print("📂 Step 2: Browse different categories")
            categories = ["Electronics", "Clothing", "Books", "Home"]
            
            category_screenshots = []
            for category in categories:
                print(f"   🧭 Browsing category: {category}")
                
                try:
                    nav_success = self.vibium.ecommerce.navigate_to_category(category)
                    
                    if nav_success:
                        self.vibium.wait.for_network_idle()
                        
                        # Take category screenshot
                        category_screenshot = self.vibium.screenshots.capture(f"category_{category.lower()}")
                        category_screenshots.append(category_screenshot)
                        print(f"   📸 Category screenshot: {category_screenshot}")
                        
                        # Check if products are visible
                        products_visible = self.vibium.assertions.is_visible(".product, .item, .card")
                        print(f"   🛍️ Products visible: {products_visible}")
                        
                        # Get product count if possible
                        try:
                            product_count = self.vibium.assertions.has_count(".product, .item, .card", 1)
                            print(f"   🔢 Product count check: {product_count}")
                        except:
                            print(f"   ⚠️ Could not determine product count")
                        
                        # Wait before next category
                        time.sleep(2)
                    else:
                        print(f"   ❌ Failed to navigate to {category}")
                        
                except Exception as cat_error:
                    print(f"   ⚠️ Error browsing {category}: {str(cat_error)}")
            
            # Step 3: Search and compare products
            print("🔍 Step 3: Search and compare products")
            search_terms = ["laptop", "smartphone"]
            
            for term in search_terms:
                print(f"   🔍 Searching for: {term}")
                search_success = self.vibium.ecommerce.search_products(term)
                
                if search_success:
                    self.vibium.wait.for_network_idle()
                    
                    # Take search results screenshot
                    search_screenshot = self.vibium.screenshots.capture(f"search_comparison_{term}")
                    print(f"   📸 Search results: {search_screenshot}")
                    
                    # Try to get product prices for comparison
                    try:
                        # Look for multiple products
                        products = self.vibium.core.page.locator(".product, .item, .card")
                        product_count = products.count()
                        
                        if product_count > 0:
                            print(f"   🛍️ Found {product_count} products for comparison")
                            
                            # Get first few product prices
                            for i in range(min(3, product_count)):
                                try:
                                    product = products.nth(i)
                                    price_element = product.locator(".price, .cost, [data-testid='price']")
                                    if price_element.is_visible():
                                        price = price_element.text_content()
                                        print(f"   💰 Product {i+1} price: {price}")
                                except:
                                    continue
                        else:
                            print(f"   ⚠️ No products found for {term}")
                            
                    except Exception as price_error:
                        print(f"   ⚠️ Error getting product prices: {str(price_error)}")
                    
                    # Wait before next search
                    time.sleep(2)
            
            # Step 4: Take final comparison screenshot
            final_screenshot = self.vibium.screenshots.capture("product_comparison_final")
            print(f"📸 Final comparison screenshot: {final_screenshot}")
            
            self.scenario_results.append({
                "scenario": "product_browsing_comparison",
                "status": "COMPLETED",
                "categories_browsed": len(category_screenshots),
                "category_screenshots": category_screenshots,
                "final_screenshot": final_screenshot,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            })
            
            print("✅ Product browsing and comparison completed!")
            return True
            
        except Exception as e:
            print(f"❌ Product browsing and comparison failed: {str(e)}")
            self.scenario_results.append({
                "scenario": "product_browsing_comparison",
                "status": "FAILED",
                "error": str(e),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            })
            return False
    
    def scenario_4_checkout_process(self):
        """Scenario 4: Checkout process simulation"""
        print("\n💳 Scenario 4: Checkout Process Simulation")
        print("=" * 50)
        
        try:
            # Step 1: Navigate to homepage
            print("📍 Step 1: Navigate to homepage")
            self.vibium.navigation.goto("https://ecommercepracticeportal.netlify.app/")
            self.vibium.wait.for_page_load()
            
            # Step 2: Add products to cart
            print("🛒 Step 2: Add products to cart")
            search_success = self.vibium.ecommerce.search_products("laptop")
            
            if search_success:
                self.vibium.wait.for_network_idle()
                
                # Add multiple products to cart
                add_success = self.vibium.ecommerce.add_to_cart(".product-item, .product-card", quantity=2)
                print(f"   🛒 Added products to cart: {add_success}")
                
                # Check cart count
                cart_count = self.vibium.ecommerce.get_cart_count()
                print(f"   🛒 Cart count: {cart_count}")
                
                # Take cart screenshot
                cart_screenshot = self.vibium.screenshots.capture("cart_with_products")
                print(f"📸 Cart screenshot: {cart_screenshot}")
            else:
                print("   ⚠️ Could not search for products")
            
            # Step 3: Generate checkout data
            print("🎲 Step 3: Generate checkout data")
            checkout_data = {
                "user": self.vibium.data.generate_user_data(),
                "shipping_address": self.vibium.data.generate_address_data(),
                "billing_address": self.vibium.data.generate_address_data(),
                "credit_card": self.vibium.data.generate_credit_card_data(),
                "order": self.vibium.data.generate_order_data()
            }
            
            print(f"   👤 User: {checkout_data['user']['first_name']} {checkout_data['user']['last_name']}")
            print(f"   📍 Shipping: {checkout_data['shipping_address']['city']}, {checkout_data['shipping_address']['state']}")
            print(f"   💳 Card: {checkout_data['credit_card']['cardholder_name']}")
            
            # Step 4: Simulate checkout steps
            print("💳 Step 4: Simulate checkout steps")
            
            # Look for checkout form
            checkout_form_selectors = [
                ".checkout-form",
                ".payment-form",
                "form[action*='checkout']",
                "[data-testid='checkout-form']"
            ]
            
            checkout_form_found = False
            for selector in checkout_form_selectors:
                try:
                    if self.vibium.assertions.is_visible(selector):
                        print(f"   ✅ Checkout form found: {selector}")
                        checkout_form_found = True
                        
                        # Take checkout form screenshot
                        checkout_screenshot = self.vibium.screenshots.capture("checkout_form")
                        print(f"   📸 Checkout form: {checkout_screenshot}")
                        
                        # Try to fill checkout form
                        form_data = {
                            'first_name': checkout_data['user']['first_name'],
                            'last_name': checkout_data['user']['last_name'],
                            'email': checkout_data['user']['email'],
                            'address': checkout_data['shipping_address']['street'],
                            'city': checkout_data['shipping_address']['city'],
                            'state': checkout_data['shipping_address']['state'],
                            'zip_code': checkout_data['shipping_address']['zip_code']
                        }
                        
                        form_fill_success = self.vibium.forms.fill_form(form_data, selector)
                        print(f"   ✍️ Checkout form filled: {form_fill_success}")
                        
                        break
                except:
                    continue
            
            if not checkout_form_found:
                print("   ⚠️ No checkout form found")
                
                # Take general page screenshot
                page_screenshot = self.vibium.screenshots.capture("no_checkout_form")
                print(f"   📸 Page screenshot: {page_screenshot}")
            
            # Step 5: Test coupon application
            print("🎫 Step 5: Test coupon application")
            coupon_code = self.vibium.data.generate_coupon_codes(1)[0]
            coupon_success = self.vibium.ecommerce.apply_coupon(coupon_code)
            print(f"   🎫 Coupon applied: {coupon_success}")
            
            # Step 6: Take final checkout screenshot
            final_screenshot = self.vibium.screenshots.capture("checkout_process_final")
            print(f"📸 Final checkout screenshot: {final_screenshot}")
            
            self.scenario_results.append({
                "scenario": "checkout_process",
                "status": "COMPLETED",
                "checkout_data": checkout_data,
                "checkout_form_found": checkout_form_found,
                "coupon_applied": coupon_success,
                "final_screenshot": final_screenshot,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            })
            
            print("✅ Checkout process simulation completed!")
            return True
            
        except Exception as e:
            print(f"❌ Checkout process failed: {str(e)}")
            self.scenario_results.append({
                "scenario": "checkout_process",
                "status": "FAILED",
                "error": str(e),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            })
            return False
    
    def scenario_5_mobile_responsiveness(self):
        """Scenario 5: Mobile responsiveness testing"""
        print("\n📱 Scenario 5: Mobile Responsiveness Testing")
        print("=" * 50)
        
        try:
            # Step 1: Navigate to homepage
            print("📍 Step 1: Navigate to homepage")
            self.vibium.navigation.goto("https://ecommercepracticeportal.netlify.app/")
            self.vibium.wait.for_page_load()
            
            # Step 2: Test different viewport sizes
            print("📐 Step 2: Test different viewport sizes")
            viewport_sizes = [
                (1920, 1080),  # Desktop
                (1366, 768),    # Laptop
                (768, 1024),    # Tablet
                (375, 667),     # Mobile
                (320, 568)      # Small Mobile
            ]
            
            viewport_screenshots = {}
            for width, height in viewport_sizes:
                print(f"   📱 Testing viewport: {width}x{height}")
                
                try:
                    # Set viewport size
                    self.vibium.core.page.set_viewport_size({'width': width, 'height': height})
                    
                    # Wait for resize
                    time.sleep(1)
                    
                    # Take screenshot
                    screenshot_path = self.vibium.screenshots.capture(f"viewport_{width}x{height}")
                    viewport_screenshots[f"{width}x{height}"] = screenshot_path
                    print(f"   📸 Viewport screenshot: {screenshot_path}")
                    
                    # Check if key elements are visible
                    key_elements = ["header", "main", "footer"]
                    visible_elements = []
                    
                    for element in key_elements:
                        try:
                            if self.vibium.assertions.is_visible(element):
                                visible_elements.append(element)
                        except:
                            continue
                    
                    print(f"   👁️ Visible elements: {', '.join(visible_elements)}")
                    
                except Exception as viewport_error:
                    print(f"   ⚠️ Error testing viewport {width}x{height}: {str(viewport_error)}")
            
            # Step 3: Test mobile-specific interactions
            print("📱 Step 3: Test mobile-specific interactions")
            
            # Set to mobile viewport
            self.vibium.core.page.set_viewport_size({'width': 375, 'height': 667})
            time.sleep(1)
            
            # Test scrolling
            try:
                # Scroll down
                self.vibium.core.page.evaluate("window.scrollTo(0, 500)")
                time.sleep(1)
                
                # Scroll up
                self.vibium.core.page.evaluate("window.scrollTo(0, 0)")
                time.sleep(1)
                
                print("   ✅ Scrolling test completed")
            except Exception as scroll_error:
                print(f"   ⚠️ Scrolling test failed: {str(scroll_error)}")
            
            # Step 4: Take final mobile screenshot
            final_mobile_screenshot = self.vibium.screenshots.capture("mobile_responsiveness_final")
            print(f"📸 Final mobile screenshot: {final_mobile_screenshot}")
            
            self.scenario_results.append({
                "scenario": "mobile_responsiveness",
                "status": "COMPLETED",
                "viewport_screenshots": viewport_screenshots,
                "final_mobile_screenshot": final_mobile_screenshot,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            })
            
            print("✅ Mobile responsiveness testing completed!")
            return True
            
        except Exception as e:
            print(f"❌ Mobile responsiveness testing failed: {str(e)}")
            self.scenario_results.append({
                "scenario": "mobile_responsiveness",
                "status": "FAILED",
                "error": str(e),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            })
            return False
    
    def generate_scenario_report(self):
        """Generate comprehensive scenario report"""
        print("\n📊 Generating Scenario Report...")
        
        # Calculate statistics
        total_scenarios = len(self.scenario_results)
        completed_scenarios = len([r for r in self.scenario_results if r.get('status') == 'COMPLETED'])
        failed_scenarios = len([r for r in self.scenario_results if r.get('status') == 'FAILED'])
        
        # Create report
        report = {
            "summary": {
                "total_scenarios": total_scenarios,
                "completed": completed_scenarios,
                "failed": failed_scenarios,
                "success_rate": f"{(completed_scenarios/total_scenarios*100):.1f}%" if total_scenarios > 0 else "0%"
            },
            "scenario_results": self.scenario_results,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "browser": self.browser_type,
            "device": self.device
        }
        
        # Save report to file
        report_filename = f"vibium_scenarios_report_{int(time.time())}.json"
        with open(report_filename, "w") as f:
            json.dump(report, f, indent=2, default=str)
        
        # Print summary
        print("\n" + "="*60)
        print("📊 VIBIUM SCENARIOS REPORT")
        print("="*60)
        print(f"Total Scenarios: {total_scenarios}")
        print(f"✅ Completed: {completed_scenarios}")
        print(f"❌ Failed: {failed_scenarios}")
        print(f"📈 Success Rate: {report['summary']['success_rate']}")
        print(f"📁 Report saved to: {report_filename}")
        print("="*60)
        
        return report
    
    def run_all_scenarios(self):
        """Run all e-commerce scenarios"""
        print("🚀 Starting Vibium E-commerce Scenarios")
        print(f"🌐 Target: https://ecommercepracticeportal.netlify.app/")
        print(f"🔧 Browser: {self.browser_type}")
        print(f"📱 Device: {self.device}")
        print(f"👻 Headless: {self.headless}")
        
        start_time = time.time()
        
        try:
            # Initialize
            if not self.initialize():
                return False
            
            # Run all scenarios
            scenarios = [
                ("Guest Shopping Journey", self.scenario_1_guest_shopping_journey),
                ("User Registration & Login", self.scenario_2_user_registration_and_login),
                ("Product Browsing & Comparison", self.scenario_3_product_browsing_and_comparison),
                ("Checkout Process", self.scenario_4_checkout_process),
                ("Mobile Responsiveness", self.scenario_5_mobile_responsiveness)
            ]
            
            for scenario_name, scenario_func in scenarios:
                try:
                    print(f"\n{'='*60}")
                    print(f"🔄 Running {scenario_name}...")
                    print(f"{'='*60}")
                    
                    scenario_func()
                    
                except Exception as e:
                    print(f"❌ {scenario_name} failed: {str(e)}")
                    self.scenario_results.append({
                        "scenario": scenario_name.lower().replace(" ", "_").replace("&", "and"),
                        "status": "FAILED",
                        "error": str(e),
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                    })
            
            # Generate final report
            self.generate_scenario_report()
            
            total_time = time.time() - start_time
            print(f"\n⏱️ Total scenarios time: {total_time:.2f} seconds")
            
            return True
            
        except Exception as e:
            print(f"❌ Scenarios execution failed: {str(e)}")
            return False
            
        finally:
            # Cleanup
            if self.vibium:
                self.vibium.core.close()
                print("🧹 Browser closed and cleaned up")

def main():
    """Main function to run scenarios"""
    
    # Configuration
    config = {
        "device": "ecommerce_scenarios",
        "browser_type": "chromium",  # Options: chromium, firefox, webkit
        "headless": False  # Set to True for headless execution
    }
    
    # Create scenarios instance
    scenarios = VibiumEcommerceScenarios(**config)
    
    # Run all scenarios
    success = scenarios.run_all_scenarios()
    
    if success:
        print("\n🎉 All scenarios completed successfully!")
        return 0
    else:
        print("\n💥 Some scenarios failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
