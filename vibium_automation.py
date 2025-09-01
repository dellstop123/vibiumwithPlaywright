#!/usr/bin/env python3
"""
Vibium Automation Script for E-commerce Portal
Comprehensive automation using Python Vibium Library
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from python_vibium import create_vibium, Vibium
import time
import json

class VibiumEcommerceAutomation:
    """
    Comprehensive e-commerce automation using Vibium
    """
    
    def __init__(self, device="automation", browser_type="chromium", headless=False):
        self.device = device
        self.browser_type = browser_type
        self.headless = headless
        self.vibium = None
        self.test_results = []
        
    def initialize(self):
        """Initialize Vibium and browser"""
        print(f"🚀 Initializing Vibium Automation - {self.browser_type}")
        
        try:
            # Create Vibium instance
            self.vibium = create_vibium(device=self.device, browser_type=self.browser_type)
            
            # Initialize browser
            if not self.vibium.core.initialize(headless=self.headless):
                raise Exception("Failed to initialize browser")
            
            print(f"✅ Browser {self.browser_type} initialized successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to initialize: {str(e)}")
            return False
    
    def run_homepage_automation(self):
        """Automate homepage testing"""
        print("\n🏠 Running Homepage Automation...")
        
        try:
            # Navigate to homepage
            self.vibium.navigation.goto("https://ecommercepracticeportal.netlify.app/")
            self.vibium.wait.for_page_load()
            
            # Take homepage screenshot
            screenshot_path = self.vibium.screenshots.capture("homepage_automation")
            print(f"📸 Homepage screenshot: {screenshot_path}")
            
            # Verify essential elements
            essential_elements = ["header", "footer", "main", "nav"]
            for element in essential_elements:
                is_visible = self.vibium.assertions.is_visible(element)
                self.test_results.append({
                    "test": "homepage_elements",
                    "element": element,
                    "result": "PASS" if is_visible else "FAIL"
                })
            
            # Check page title
            title_contains = self.vibium.assertions.title_contains("E-commerce")
            self.test_results.append({
                "test": "homepage_title",
                "result": "PASS" if title_contains else "FAIL"
            })
            
            # Measure performance
            load_time = self.vibium.performance.measure_load_time("https://ecommercepracticeportal.netlify.app/")
            self.test_results.append({
                "test": "homepage_performance",
                "load_time": load_time,
                "result": "PASS" if load_time and load_time < 10 else "FAIL"
            })
            
            print("✅ Homepage automation completed")
            return True
            
        except Exception as e:
            print(f"❌ Homepage automation failed: {str(e)}")
            self.test_results.append({
                "test": "homepage_automation",
                "result": "FAIL",
                "error": str(e)
            })
            return False
    
    def run_search_automation(self):
        """Automate search functionality"""
        print("\n🔍 Running Search Automation...")
        
        try:
            # Generate search queries
            search_queries = self.vibium.data.generate_search_queries(3)
            
            for query in search_queries:
                print(f"🔍 Testing search: {query}")
                
                # Perform search
                search_success = self.vibium.ecommerce.search_products(query)
                
                if search_success:
                    # Wait for results
                    self.vibium.wait.for_network_idle()
                    
                    # Take search results screenshot
                    screenshot_path = self.vibium.screenshots.capture(f"search_{query.replace(' ', '_')}")
                    
                    # Verify search results
                    has_results = self.vibium.assertions.is_visible(".search-results, .products, .results")
                    
                    self.test_results.append({
                        "test": "search_functionality",
                        "query": query,
                        "search_success": search_success,
                        "has_results": has_results,
                        "screenshot": screenshot_path,
                        "result": "PASS" if search_success and has_results else "FAIL"
                    })
                else:
                    self.test_results.append({
                        "test": "search_functionality",
                        "query": query,
                        "result": "FAIL",
                        "error": "Search failed"
                    })
            
            print("✅ Search automation completed")
            return True
            
        except Exception as e:
            print(f"❌ Search automation failed: {str(e)}")
            self.test_results.append({
                "test": "search_automation",
                "result": "FAIL",
                "error": str(e)
            })
            return False
    
    def run_navigation_automation(self):
        """Automate navigation testing"""
        print("\n🧭 Running Navigation Automation...")
        
        try:
            # Navigate to homepage first
            self.vibium.navigation.goto("https://ecommercepracticeportal.netlify.app/")
            self.vibium.wait.for_page_load()
            
            # Test category navigation
            categories = ["Electronics", "Clothing", "Books", "Home"]
            
            for category in categories:
                print(f"🧭 Testing category: {category}")
                
                # Try to navigate to category
                nav_success = self.vibium.ecommerce.navigate_to_category(category)
                
                if nav_success:
                    # Wait for page load
                    self.vibium.wait.for_network_idle()
                    
                    # Take category page screenshot
                    screenshot_path = self.vibium.screenshots.capture(f"category_{category.lower()}")
                    
                    # Verify category page
                    page_loaded = self.vibium.assertions.url_contains(category.lower())
                    
                    self.test_results.append({
                        "test": "category_navigation",
                        "category": category,
                        "navigation_success": nav_success,
                        "page_loaded": page_loaded,
                        "screenshot": screenshot_path,
                        "result": "PASS" if nav_success and page_loaded else "FAIL"
                    })
                else:
                    self.test_results.append({
                        "test": "category_navigation",
                        "category": category,
                        "result": "FAIL",
                        "error": "Navigation failed"
                    })
            
            print("✅ Navigation automation completed")
            return True
            
        except Exception as e:
            print(f"❌ Navigation automation failed: {str(e)}")
            self.test_results.append({
                "test": "navigation_automation",
                "result": "FAIL",
                "error": str(e)
            })
            return False
    
    def run_form_automation(self):
        """Automate form testing"""
        print("\n📝 Running Form Automation...")
        
        try:
            # Navigate to homepage
            self.vibium.navigation.goto("https://ecommercepracticeportal.netlify.app/")
            self.vibium.wait.for_page_load()
            
            # Generate test user data
            user_data = self.vibium.data.generate_user_data()
            newsletter_email = self.vibium.data.generate_email()
            
            print(f"👤 Generated user: {user_data['first_name']} {user_data['last_name']}")
            print(f"📧 Generated email: {newsletter_email}")
            
            # Test newsletter subscription
            newsletter_success = self.vibium.forms.subscribe_to_newsletter(newsletter_email)
            
            self.test_results.append({
                "test": "newsletter_subscription",
                "email": newsletter_email,
                "success": newsletter_success,
                "result": "PASS" if newsletter_success else "FAIL"
            })
            
            # Test form validation (if forms exist)
            try:
                # Look for any forms on the page
                forms_exist = self.vibium.assertions.is_visible("form")
                
                if forms_exist:
                    # Generate form data
                    form_data = {
                        'email': self.vibium.data.generate_email(),
                        'name': self.vibium.data.generate_string(10),
                        'message': self.vibium.data.generate_string(50)
                    }
                    
                    # Try to fill form
                    form_fill_success = self.vibium.forms.fill_form(form_data)
                    
                    self.test_results.append({
                        "test": "form_filling",
                        "form_data": form_data,
                        "fill_success": form_fill_success,
                        "result": "PASS" if form_fill_success else "FAIL"
                    })
                else:
                    self.test_results.append({
                        "test": "form_filling",
                        "result": "SKIP",
                        "note": "No forms found on page"
                    })
                    
            except Exception as form_error:
                self.test_results.append({
                    "test": "form_filling",
                    "result": "FAIL",
                    "error": str(form_error)
                })
            
            print("✅ Form automation completed")
            return True
            
        except Exception as e:
            print(f"❌ Form automation failed: {str(e)}")
            self.test_results.append({
                "test": "form_automation",
                "result": "FAIL",
                "error": str(e)
            })
            return False
    
    def run_performance_automation(self):
        """Automate performance testing"""
        print("\n⚡ Running Performance Automation...")
        
        try:
            # Test URLs for performance
            test_urls = [
                "https://ecommercepracticeportal.netlify.app/",
                "https://ecommercepracticeportal.netlify.app/products",
                "https://ecommercepracticeportal.netlify.app/about"
            ]
            
            performance_results = {}
            
            for url in test_urls:
                print(f"⚡ Testing performance: {url}")
                
                try:
                    # Measure load time
                    load_time = self.vibium.performance.measure_load_time(url)
                    
                    # Check Core Web Vitals
                    web_vitals = self.vibium.performance.check_core_web_vitals()
                    
                    # Check memory usage
                    memory_usage = self.vibium.performance.check_memory_usage()
                    
                    # Check network metrics
                    network_metrics = self.vibium.performance.measure_network_requests()
                    
                    performance_results[url] = {
                        "load_time": load_time,
                        "web_vitals": web_vitals,
                        "memory_usage": memory_usage,
                        "network_metrics": network_metrics
                    }
                    
                    # Take performance screenshot
                    screenshot_path = self.vibium.screenshots.capture(f"performance_{url.split('/')[-1] or 'home'}")
                    
                    # Evaluate performance
                    performance_score = self._evaluate_performance(load_time, web_vitals)
                    
                    self.test_results.append({
                        "test": "performance_testing",
                        "url": url,
                        "load_time": load_time,
                        "performance_score": performance_score,
                        "screenshot": screenshot_path,
                        "result": "PASS" if performance_score >= 7 else "FAIL"
                    })
                    
                except Exception as url_error:
                    print(f"⚠️ Performance test failed for {url}: {str(url_error)}")
                    self.test_results.append({
                        "test": "performance_testing",
                        "url": url,
                        "result": "FAIL",
                        "error": str(url_error)
                    })
            
            print("✅ Performance automation completed")
            return True
            
        except Exception as e:
            print(f"❌ Performance automation failed: {str(e)}")
            self.test_results.append({
                "test": "performance_automation",
                "result": "FAIL",
                "error": str(e)
            })
            return False
    
    def run_ecommerce_automation(self):
        """Automate e-commerce specific functionality"""
        print("\n🛒 Running E-commerce Automation...")
        
        try:
            # Navigate to homepage
            self.vibium.navigation.goto("https://ecommercepracticeportal.netlify.app/")
            self.vibium.wait.for_page_load()
            
            # Test product search
            search_success = self.vibium.ecommerce.search_products("laptop")
            
            if search_success:
                self.vibium.wait.for_network_idle()
                
                # Test adding product to cart
                add_to_cart_success = self.vibium.ecommerce.add_to_cart(".product-item, .product-card", quantity=1)
                
                self.test_results.append({
                    "test": "add_to_cart",
                    "success": add_to_cart_success,
                    "result": "PASS" if add_to_cart_success else "FAIL"
                })
                
                # Get cart count
                cart_count = self.vibium.ecommerce.get_cart_count()
                
                self.test_results.append({
                    "test": "cart_count",
                    "count": cart_count,
                    "result": "PASS" if cart_count >= 0 else "FAIL"
                })
                
                # Test product details view
                view_details_success = self.vibium.ecommerce.view_product_details(".product-item, .product-card")
                
                self.test_results.append({
                    "test": "view_product_details",
                    "success": view_details_success,
                    "result": "PASS" if view_details_success else "FAIL"
                })
                
                # Test wishlist functionality
                wishlist_success = self.vibium.ecommerce.add_to_wishlist(".product-item, .product-card")
                
                self.test_results.append({
                    "test": "add_to_wishlist",
                    "success": wishlist_success,
                    "result": "PASS" if wishlist_success else "FAIL"
                })
                
                # Test coupon application
                coupon_code = self.vibium.data.generate_coupon_codes(1)[0]
                coupon_success = self.vibium.ecommerce.apply_coupon(coupon_code)
                
                self.test_results.append({
                    "test": "apply_coupon",
                    "coupon": coupon_code,
                    "success": coupon_success,
                    "result": "PASS" if coupon_success else "FAIL"
                })
            
            print("✅ E-commerce automation completed")
            return True
            
        except Exception as e:
            print(f"❌ E-commerce automation failed: {str(e)}")
            self.test_results.append({
                "test": "ecommerce_automation",
                "result": "FAIL",
                "error": str(e)
            })
            return False
    
    def run_data_generation_automation(self):
        """Automate data generation testing"""
        print("\n🎲 Running Data Generation Automation...")
        
        try:
            # Generate various types of test data
            test_data = {}
            
            # User data
            test_data['user'] = self.vibium.data.generate_user_data()
            test_data['product'] = self.vibium.data.generate_product_data()
            test_data['address'] = self.vibium.data.generate_address_data()
            test_data['credit_card'] = self.vibium.data.generate_credit_card_data()
            test_data['order'] = self.vibium.data.generate_order_data()
            
            # Multiple items
            test_data['emails'] = self.vibium.data.generate_newsletter_emails(5)
            test_data['search_queries'] = self.vibium.data.generate_search_queries(5)
            test_data['coupon_codes'] = self.vibium.data.generate_coupon_codes(5)
            test_data['test_scenarios'] = self.vibium.data.generate_test_scenarios()
            
            # Save test data to file
            with open("generated_test_data.json", "w") as f:
                json.dump(test_data, f, indent=2, default=str)
            
            print(f"💾 Test data saved to: generated_test_data.json")
            
            # Verify data generation
            all_data_generated = all([
                test_data['user'],
                test_data['product'],
                test_data['address'],
                test_data['credit_card'],
                test_data['order'],
                test_data['emails'],
                test_data['search_queries'],
                test_data['coupon_codes'],
                test_data['test_scenarios']
            ])
            
            self.test_results.append({
                "test": "data_generation",
                "data_types": list(test_data.keys()),
                "all_generated": all_data_generated,
                "result": "PASS" if all_data_generated else "FAIL"
            })
            
            print("✅ Data generation automation completed")
            return True
            
        except Exception as e:
            print(f"❌ Data generation automation failed: {str(e)}")
            self.test_results.append({
                "test": "data_generation_automation",
                "result": "FAIL",
                "error": str(e)
            })
            return False
    
    def run_screenshot_automation(self):
        """Automate screenshot testing"""
        print("\n📸 Running Screenshot Automation...")
        
        try:
            # Navigate to homepage
            self.vibium.navigation.goto("https://ecommercepracticeportal.netlify.app/")
            self.vibium.wait.for_page_load()
            
            # Take various types of screenshots
            screenshots = {}
            
            # Full page screenshot
            screenshots['full_page'] = self.vibium.screenshots.capture("automation_full_page")
            
            # Element screenshot (if header exists)
            try:
                header_screenshot = self.vibium.screenshots.capture_element("header", "automation_header")
                screenshots['header'] = header_screenshot
            except:
                screenshots['header'] = None
            
            # Viewport screenshots at different sizes
            viewport_sizes = [(1920, 1080), (1366, 768), (768, 1024)]
            viewport_screenshots = self.vibium.screenshots.capture_viewport_sizes(viewport_sizes)
            screenshots['viewport'] = viewport_screenshots
            
            # Before/after screenshot (simulate action)
            def before_action():
                print("📸 Taking 'before' screenshot")
            
            def after_action():
                print("📸 Taking 'after' screenshot")
                # Simulate some action
                time.sleep(1)
            
            before_after_screenshots = self.vibium.screenshots.capture_before_after(
                "automation_action", before_action, after_action
            )
            screenshots['before_after'] = before_after_screenshots
            
            # Verify screenshots were taken
            screenshot_count = len([s for s in screenshots.values() if s])
            
            self.test_results.append({
                "test": "screenshot_automation",
                "screenshots_taken": screenshot_count,
                "screenshot_types": list(screenshots.keys()),
                "result": "PASS" if screenshot_count > 0 else "FAIL"
            })
            
            print(f"📸 Screenshot automation completed - {screenshot_count} screenshots taken")
            return True
            
        except Exception as e:
            print(f"❌ Screenshot automation failed: {str(e)}")
            self.test_results.append({
                "test": "screenshot_automation",
                "result": "FAIL",
                "error": str(e)
            })
            return False
    
    def _evaluate_performance(self, load_time, web_vitals):
        """Evaluate performance and return score (0-10)"""
        score = 0
        
        # Load time scoring (0-4 points)
        if load_time:
            if load_time < 2:
                score += 4
            elif load_time < 4:
                score += 3
            elif load_time < 6:
                score += 2
            elif load_time < 8:
                score += 1
        
        # Web Vitals scoring (0-6 points)
        if web_vitals:
            # Check if Core Web Vitals are within acceptable ranges
            if web_vitals.get('firstContentfulPaint', 0) < 1800:
                score += 2
            if web_vitals.get('domContentLoaded', 0) < 2000:
                score += 2
            if web_vitals.get('loadComplete', 0) < 3000:
                score += 2
        
        return score
    
    def generate_report(self):
        """Generate comprehensive test report"""
        print("\n📊 Generating Test Report...")
        
        # Calculate statistics
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r.get('result') == 'PASS'])
        failed_tests = len([r for r in self.test_results if r.get('result') == 'FAIL'])
        skipped_tests = len([r for r in self.test_results if r.get('result') == 'SKIP'])
        
        # Create report
        report = {
            "summary": {
                "total_tests": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "skipped": skipped_tests,
                "success_rate": f"{(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "0%"
            },
            "test_results": self.test_results,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "browser": self.browser_type,
            "device": self.device
        }
        
        # Save report to file
        report_filename = f"vibium_automation_report_{int(time.time())}.json"
        with open(report_filename, "w") as f:
            json.dump(report, f, indent=2, default=str)
        
        # Print summary
        print("\n" + "="*60)
        print("📊 VIBIUM AUTOMATION REPORT")
        print("="*60)
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"⏭️ Skipped: {skipped_tests}")
        print(f"📈 Success Rate: {report['summary']['success_rate']}")
        print(f"📁 Report saved to: {report_filename}")
        print("="*60)
        
        return report
    
    def run_full_automation(self):
        """Run complete automation suite"""
        print("🚀 Starting Full Vibium Automation Suite")
        print(f"🌐 Target: https://ecommercepracticeportal.netlify.app/")
        print(f"🔧 Browser: {self.browser_type}")
        print(f"📱 Device: {self.device}")
        print(f"👻 Headless: {self.headless}")
        
        start_time = time.time()
        
        try:
            # Initialize
            if not self.initialize():
                return False
            
            # Run all automation modules
            automation_modules = [
                ("Homepage", self.run_homepage_automation),
                ("Search", self.run_search_automation),
                ("Navigation", self.run_navigation_automation),
                ("Forms", self.run_form_automation),
                ("Performance", self.run_performance_automation),
                ("E-commerce", self.run_ecommerce_automation),
                ("Data Generation", self.run_data_generation_automation),
                ("Screenshots", self.run_screenshot_automation)
            ]
            
            for module_name, module_func in automation_modules:
                try:
                    print(f"\n{'='*50}")
                    print(f"🔄 Running {module_name} Module...")
                    print(f"{'='*50}")
                    
                    module_func()
                    
                except Exception as e:
                    print(f"❌ {module_name} module failed: {str(e)}")
                    self.test_results.append({
                        "test": f"{module_name}_module",
                        "result": "FAIL",
                        "error": str(e)
                    })
            
            # Generate final report
            self.generate_report()
            
            total_time = time.time() - start_time
            print(f"\n⏱️ Total automation time: {total_time:.2f} seconds")
            
            return True
            
        except Exception as e:
            print(f"❌ Full automation failed: {str(e)}")
            return False
            
        finally:
            # Cleanup
            if self.vibium:
                self.vibium.core.close()
                print("🧹 Browser closed and cleaned up")

def main():
    """Main function to run automation"""
    
    # Configuration
    config = {
        "device": "automation_demo",
        "browser_type": "chromium",  # Options: chromium, firefox, webkit
        "headless": False  # Set to True for headless execution
    }
    
    # Create automation instance
    automation = VibiumEcommerceAutomation(**config)
    
    # Run full automation
    success = automation.run_full_automation()
    
    if success:
        print("\n🎉 Automation completed successfully!")
        return 0
    else:
        print("\n💥 Automation completed with errors!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
