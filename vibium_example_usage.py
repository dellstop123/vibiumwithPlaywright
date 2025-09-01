#!/usr/bin/env python3
"""
Vibium Example Usage
Demonstrating the exact syntax requested by the user
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from python_vibium import Vibium

def main():
    """Main function demonstrating Vibium usage"""
    print("🚀 Vibium Example Usage")
    print("=" * 40)
    
    try:
        # Create Vibium instance with desktop device
        print("1️⃣ Creating Vibium instance...")
        vibe = Vibium(device='desktop')
        
        # Initialize the browser
        print("2️⃣ Initializing browser...")
        if not vibe.core.initialize(headless=False):
            print("❌ Failed to initialize browser")
            return False
        
        print("✅ Browser initialized successfully!")
        
        # Use the exact syntax requested
        print("3️⃣ Opening example.com...")
        vibe.do("open example.com")
        
        print("4️⃣ Checking for 'Example Domain' heading...")
        result = vibe.check("do you see the Example Domain heading?")
        
        if result:
            print("✅ 'Example Domain' heading found!")
        else:
            print("❌ 'Example Domain' heading not found")
        
        # Take a screenshot
        print("5️⃣ Taking screenshot...")
        screenshot_path = vibe.screenshots.capture("example_domain_page")
        print(f"📸 Screenshot saved: {screenshot_path}")
        
        # Wait a bit to see the page
        print("⏳ Waiting 3 seconds to view the page...")
        import time
        time.sleep(3)
        
        # Close browser
        print("6️⃣ Closing browser...")
        vibe.core.close()
        print("✅ Browser closed successfully!")
        
        print("\n🎉 Vibium example completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Example failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
