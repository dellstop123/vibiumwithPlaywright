# Vibium Usage Guide

This guide shows you how to write automation code using the Vibium library with the exact syntax you requested.

## Basic Syntax

The Vibium library follows this simple pattern:

```python
from python_vibium import Vibium

# Create a Vibium instance
vibe = Vibium(device='desktop')

# Use simple commands
vibe.do("open example.com")
vibe.check("do you see the Example Domain heading?")
```

## Installation and Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   playwright install
   ```

2. **Import the Library:**
   ```python
   from python_vibium import Vibium
   ```

## Core Commands

### 1. Creating Vibium Instance

```python
# Basic usage
vibe = Vibium(device='desktop')

# With browser specification
vibe = Vibium(device='mobile', browser_type='firefox')

# Available devices: 'desktop', 'mobile', 'tablet', 'automation'
# Available browsers: 'chromium', 'firefox', 'webkit'
```

### 2. Browser Operations

```python
# Initialize browser
vibe.core.initialize(headless=False)

# Navigate to URL
vibe.do("open https://example.com")
# or
vibe.navigation.goto("https://example.com")

# Close browser
vibe.core.close()
```

### 3. Element Checking

```python
# Check if elements are visible
vibe.check("do you see the header?")
vibe.check("do you see a login button?")
vibe.check("are there any products displayed?")

# Check specific elements
vibe.assertions.is_visible(".product-item")
vibe.assertions.contains_text("h1", "Welcome")
```

### 4. Form Interactions

```python
# Fill forms with data
user_data = vibe.data.generate_user_data()
vibe.forms.fill_form(user_data, "form")

# Subscribe to newsletter
vibe.forms.subscribe_to_newsletter("user@example.com")
```

### 5. E-commerce Operations

```python
# Search for products
vibe.ecommerce.search_products("laptop")

# Add to cart
vibe.ecommerce.add_to_cart(".product-item", quantity=2)

# Get cart count
cart_count = vibe.ecommerce.get_cart_count()

# Navigate categories
vibe.ecommerce.navigate_to_category("Electronics")
```

### 6. Screenshots

```python
# Take screenshots
vibe.screenshots.capture("homepage")
vibe.screenshots.capture("search_results")
vibe.screenshots.capture("checkout_form")
```

### 7. Data Generation

```python
# Generate test data
user = vibe.data.generate_user_data()
address = vibe.data.generate_address_data()
product = vibe.data.generate_product_data()
credit_card = vibe.data.generate_credit_card_data()
coupon = vibe.data.generate_coupon_codes(1)[0]
```

### 8. Performance Testing

```python
# Measure page load time
load_time = vibe.performance.measure_page_load_time()

# Get Core Web Vitals
web_vitals = vibe.performance.get_core_web_vitals()
```

## Complete Examples

### Example 1: Basic Website Testing

```python
from python_vibium import Vibium

def test_example_website():
    vibe = Vibium(device='desktop')
    
    try:
        # Initialize browser
        vibe.core.initialize(headless=False)
        
        # Navigate and test
        vibe.do("open https://example.com")
        vibe.check("do you see the Example Domain heading?")
        
        # Take screenshot
        vibe.screenshots.capture("example_page")
        
        # Close browser
        vibe.core.close()
        
    except Exception as e:
        print(f"Test failed: {e}")
        vibe.core.close()
```

### Example 2: E-commerce Automation

```python
from python_vibium import Vibium

def test_ecommerce_site():
    vibe = Vibium(device='desktop', browser_type='chromium')
    
    try:
        vibe.core.initialize(headless=False)
        
        # Navigate to e-commerce site
        vibe.do("open https://ecommercepracticeportal.netlify.app/")
        vibe.wait.for_page_load()
        
        # Search for products
        vibe.ecommerce.search_products("laptop")
        vibe.check("are there search results?")
        
        # Add to cart
        vibe.ecommerce.add_to_cart(".product-item")
        
        # Generate test user data
        user_data = vibe.data.generate_user_data()
        
        # Fill checkout form if available
        try:
            vibe.forms.fill_form(user_data, "form")
        except:
            print("No checkout form found")
        
        # Take final screenshot
        vibe.screenshots.capture("ecommerce_test")
        
        vibe.core.close()
        
    except Exception as e:
        print(f"E-commerce test failed: {e}")
        vibe.core.close()
```

### Example 3: Mobile Testing

```python
from python_vibium import Vibium

def test_mobile_responsiveness():
    vibe = Vibium(device='mobile', browser_type='chromium')
    
    try:
        vibe.core.initialize(headless=False)
        
        # Test different viewport sizes
        viewports = [(375, 667), (768, 1024), (1920, 1080)]
        
        for width, height in viewports:
            vibe.core.page.set_viewport_size({'width': width, 'height': height})
            vibe.do("open https://example.com")
            vibe.screenshots.capture(f"viewport_{width}x{height}")
        
        vibe.core.close()
        
    except Exception as e:
        print(f"Mobile test failed: {e}")
        vibe.core.close()
```

## Available Methods by Module

### Core Module (`vibe.core`)
- `initialize(headless=False)` - Start browser
- `goto(url)` - Navigate to URL
- `close()` - Close browser
- `page` - Access Playwright page object

### Navigation Module (`vibe.navigation`)
- `goto(url)` - Navigate to URL
- `verify_url(expected_url)` - Check current URL
- `verify_title(expected_title)` - Check page title

### Elements Module (`vibe.elements`)
- `wait_for_stable(selector, timeout=5000)` - Wait for element to stabilize
- `click_with_retry(selector, max_attempts=3)` - Click with retry logic
- `fill_input(selector, value)` - Fill input field

### Forms Module (`vibe.forms`)
- `fill_form(data, form_selector)` - Fill form with data
- `submit_form(form_selector)` - Submit form
- `validate_form(form_selector)` - Validate form fields
- `subscribe_to_newsletter(email)` - Newsletter subscription

### E-commerce Module (`vibe.ecommerce`)
- `search_products(query)` - Search for products
- `add_to_cart(selector, quantity=1)` - Add product to cart
- `get_cart_count()` - Get number of items in cart
- `navigate_to_category(category)` - Navigate to product category

### Screenshots Module (`vibe.screenshots`)
- `capture(name, full_page=True)` - Take screenshot
- `capture_element(selector, name)` - Screenshot specific element
- `capture_viewport(name)` - Screenshot visible area

### Data Module (`vibe.data`)
- `generate_user_data()` - Generate user information
- `generate_address_data()` - Generate address data
- `generate_product_data()` - Generate product data
- `generate_credit_card_data()` - Generate credit card data
- `generate_coupon_codes(count)` - Generate coupon codes

### Performance Module (`vibe.performance`)
- `measure_page_load_time()` - Measure page load time
- `get_core_web_vitals()` - Get Core Web Vitals metrics
- `measure_memory_usage()` - Measure memory usage

### Wait Module (`vibe.wait`)
- `for_page_load()` - Wait for page to load
- `for_network_idle()` - Wait for network to be idle
- `for_element_visibility(selector)` - Wait for element to be visible

## Best Practices

1. **Always initialize and close the browser:**
   ```python
   vibe = Vibium(device='desktop')
   try:
       vibe.core.initialize()
       # Your automation code here
   finally:
       vibe.core.close()
   ```

2. **Use descriptive names for screenshots:**
   ```python
   vibe.screenshots.capture("login_page_before_submit")
   vibe.screenshots.capture("login_page_after_submit")
   ```

3. **Generate test data for forms:**
   ```python
   user_data = vibe.data.generate_user_data()
   vibe.forms.fill_form(user_data, "form")
   ```

4. **Check for elements before interacting:**
   ```python
   if vibe.check("do you see the login button?"):
       vibe.do("click the login button")
   ```

5. **Handle errors gracefully:**
   ```python
   try:
       vibe.ecommerce.add_to_cart(".product-item")
   except Exception as e:
       print(f"Could not add to cart: {e}")
   ```

## Running Your Code

1. **Save your script** (e.g., `my_vibium_test.py`)
2. **Run with Python 3.9:**
   ```bash
   python3.9 my_vibium_test.py
   ```

3. **Use the CLI for quick tests:**
   ```bash
   python3.9 python_vibium/cli.py demo
   ```

## Troubleshooting

- **Browser won't start:** Make sure Playwright is installed (`playwright install`)
- **Import errors:** Check that you're using Python 3.9 and all dependencies are installed
- **Element not found:** Use multiple selectors with fallbacks (`.button, [data-testid='button'], button`)
- **Screenshots not saving:** Check file permissions and disk space

## Next Steps

1. Try the simple examples in `vibium_example_usage.py`
2. Explore the comprehensive example in `vibium_comprehensive_example.py`
3. Run the demo suite with `python3.9 vibium_simple_demo.py`
4. Create your own automation scripts using the patterns shown above

The Vibium library makes automation simple and readable with its intuitive command structure!

