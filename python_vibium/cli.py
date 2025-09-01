#!/usr/bin/env python3
"""
Command Line Interface for Python Vibium Library
"""

import argparse
import sys
import time
from typing import Optional
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from python_vibium import create_vibium, Vibium

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Python Vibium Library - UI Automation Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  vibium run --url https://example.com --headless
  vibium test --browser firefox --screenshot
  vibium demo --device mobile
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Run command
    run_parser = subparsers.add_parser('run', help='Run automation tasks')
    run_parser.add_argument('--url', required=True, help='URL to automate')
    run_parser.add_argument('--browser', default='chromium', choices=['chromium', 'firefox', 'webkit'], help='Browser to use')
    run_parser.add_argument('--headless', action='store_true', help='Run in headless mode')
    run_parser.add_argument('--device', default='default', help='Device identifier')
    run_parser.add_argument('--screenshot', action='store_true', help='Take screenshot')
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Run tests')
    test_parser.add_argument('--browser', default='chromium', choices=['chromium', 'firefox', 'webkit'], help='Browser to use')
    test_parser.add_argument('--headless', action='store_true', help='Run in headless mode')
    test_parser.add_argument('--screenshot', action='store_true', help='Take screenshots during tests')
    test_parser.add_argument('--performance', action='store_true', help='Run performance tests')
    
    # Demo command
    demo_parser = subparsers.add_parser('demo', help='Run demonstration')
    demo_parser.add_argument('--browser', default='chromium', choices=['chromium', 'firefox', 'webkit'], help='Browser to use')
    demo_parser.add_argument('--headless', action='store_true', help='Run in headless mode')
    demo_parser.add_argument('--device', default='demo', help='Device identifier')
    
    # Version command
    version_parser = subparsers.add_parser('version', help='Show version information')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        if args.command == 'run':
            return run_automation(args)
        elif args.command == 'test':
            return run_tests(args)
        elif args.command == 'demo':
            return run_demo(args)
        elif args.command == 'version':
            return show_version()
        else:
            parser.print_help()
            return 1
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return 1
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1

def run_automation(args) -> int:
    """Run automation tasks"""
    print(f"Starting automation for: {args.url}")
    print(f"Browser: {args.browser}")
    print(f"Device: {args.device}")
    print(f"Headless: {args.headless}")
    
    vibium = create_vibium(device=args.device, browser_type=args.browser)
    
    if not vibium.core.initialize(headless=args.headless):
        print("Failed to initialize browser")
        return 1
    
    try:
        # Navigate to URL
        print(f"Navigating to: {args.url}")
        vibium.navigation.goto(args.url)
        
        # Wait for page load
        vibium.wait.for_page_load()
        
        # Take screenshot if requested
        if args.screenshot:
            screenshot_path = vibium.screenshots.capture("automation_run")
            print(f"Screenshot saved to: {screenshot_path}")
        
        # Basic page verification
        print("Verifying page elements...")
        vibium.assertions.is_visible("body")
        
        # Get page info
        title = vibium.navigation.get_page_title()
        url = vibium.navigation.get_current_url()
        
        print(f"Page title: {title}")
        print(f"Current URL: {url}")
        
        print("Automation completed successfully!")
        return 0
        
    except Exception as e:
        print(f"Automation failed: {str(e)}")
        return 1
        
    finally:
        vibium.core.close()

def run_tests(args) -> int:
    """Run tests"""
    print("Starting test execution...")
    print(f"Browser: {args.browser}")
    print(f"Headless: {args.headless}")
    
    vibium = create_vibium(device="test", browser_type=args.browser)
    
    if not vibium.core.initialize(headless=args.headless):
        print("Failed to initialize browser")
        return 1
    
    try:
        # Test data generation
        print("Testing data generation...")
        user_data = vibium.data.generate_user_data()
        product_data = vibium.data.generate_product_data()
        address_data = vibium.data.generate_address_data()
        
        print(f"Generated user: {user_data}")
        print(f"Generated product: {product_data}")
        print(f"Generated address: {address_data}")
        
        # Test navigation
        print("Testing navigation...")
        vibium.navigation.goto("https://ecommercepracticeportal.netlify.app/")
        vibium.wait.for_page_load()
        
        # Test assertions
        print("Testing assertions...")
        vibium.assertions.is_visible("body")
        vibium.assertions.title_contains("E-commerce")
        
        # Test e-commerce functions
        print("Testing e-commerce functions...")
        vibium.ecommerce.search_products("laptop")
        vibium.wait.for_network_idle()
        
        # Performance tests if requested
        if args.performance:
            print("Running performance tests...")
            load_time = vibium.performance.measure_load_time("https://ecommercepracticeportal.netlify.app/")
            web_vitals = vibium.performance.check_core_web_vitals()
            
            print(f"Load time: {load_time:.2f} seconds")
            print(f"Core Web Vitals: {web_vitals}")
        
        # Screenshots if requested
        if args.screenshot:
            print("Taking screenshots...")
            vibium.screenshots.capture("test_run")
        
        print("All tests passed!")
        return 0
        
    except Exception as e:
        print(f"Tests failed: {str(e)}")
        return 1
        
    finally:
        vibium.core.close()

def run_demo(args) -> int:
    """Run demonstration"""
    print("Starting Vibium demonstration...")
    print(f"Browser: {args.browser}")
    print(f"Device: {args.device}")
    print(f"Headless: {args.headless}")
    
    vibium = create_vibium(device=args.device, browser_type=args.browser)
    
    if not vibium.core.initialize(headless=args.headless):
        print("Failed to initialize browser")
        return 1
    
    try:
        # Demo 1: Basic navigation
        print("\n=== Demo 1: Basic Navigation ===")
        vibium.navigation.goto("https://ecommercepracticeportal.netlify.app/")
        vibium.wait.for_page_load()
        
        # Demo 2: Data generation
        print("\n=== Demo 2: Data Generation ===")
        email = vibium.data.generate_email()
        random_string = vibium.data.generate_string(10)
        user_data = vibium.data.generate_user_data()
        
        print(f"Generated email: {email}")
        print(f"Generated string: {random_string}")
        print(f"Generated user: {user_data}")
        
        # Demo 3: E-commerce functions
        print("\n=== Demo 3: E-commerce Functions ===")
        vibium.ecommerce.search_products("smartphone")
        vibium.wait.for_network_idle()
        
        # Demo 4: Form handling
        print("\n=== Demo 4: Form Handling ===")
        test_email = vibium.data.generate_email()
        vibium.forms.subscribe_to_newsletter(test_email)
        
        # Demo 5: Screenshots
        print("\n=== Demo 5: Screenshots ===")
        screenshot_path = vibium.screenshots.capture("demo_run")
        print(f"Screenshot saved to: {screenshot_path}")
        
        # Demo 6: Performance
        print("\n=== Demo 6: Performance ===")
        load_time = vibium.performance.measure_load_time("https://ecommercepracticeportal.netlify.app/")
        print(f"Page load time: {load_time:.2f} seconds")
        
        print("\n=== Demonstration completed successfully! ===")
        return 0
        
    except Exception as e:
        print(f"Demonstration failed: {str(e)}")
        return 1
        
    finally:
        vibium.core.close()

def show_version() -> int:
    """Show version information"""
    print("Python Vibium Library v1.0.0")
    print("A comprehensive testing framework for UI automation")
    print("Built on top of Playwright and Selenium")
    return 0

if __name__ == "__main__":
    sys.exit(main())
