# Python Vibium Library

A comprehensive Python testing framework for UI automation built on top of Playwright and Selenium. The Python Vibium Library provides a modular, extensible architecture for web testing with a focus on e-commerce applications.

## 🚀 Features

- **Modular Architecture**: Organized into specialized modules for different testing needs
- **Multi-Browser Support**: Chromium, Firefox, and WebKit support
- **E-commerce Focused**: Built-in methods for common e-commerce testing scenarios
- **Data Generation**: Comprehensive test data generation for various scenarios
- **Performance Testing**: Built-in performance monitoring and Core Web Vitals
- **Screenshot Management**: Advanced screenshot capture and comparison
- **Wait Utilities**: Intelligent waiting mechanisms for dynamic content
- **Form Handling**: Comprehensive form testing and validation
- **CLI Interface**: Command-line interface for automation tasks

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

### Install Python Vibium Library

```bash
# Install in development mode
cd python_vibium
pip install -e .

# Or install directly
pip install python-vibium
```

## 🏗️ Architecture

The Python Vibium Library is organized into the following modules:

### Core Modules

- **`core`**: Basic browser management and initialization
- **`ecommerce`**: E-commerce specific testing methods
- **`forms`**: Form handling and validation
- **`navigation`**: Page navigation and verification
- **`elements`**: Element interaction and manipulation
- **`assertions`**: Verification and assertion methods
- **`performance`**: Performance testing and monitoring
- **`screenshots`**: Screenshot capture and management
- **`data`**: Test data generation
- **`wait`**: Wait utilities and synchronization

## 🚀 Quick Start

### Basic Usage

```python
from python_vibium import create_vibium

# Create Vibium instance
vibium = create_vibium(device="test", browser_type="chromium")

# Initialize browser
vibium.core.initialize(headless=False)

try:
    # Navigate to website
    vibium.navigation.goto("https://ecommercepracticeportal.netlify.app/")
    
    # Wait for page load
    vibium.wait.for_page_load()
    
    # Take screenshot
    screenshot_path = vibium.screenshots.capture("homepage")
    
    # Search for products
    vibium.ecommerce.search_products("laptop")
    
    # Verify elements
    vibium.assertions.is_visible("header")
    vibium.assertions.title_contains("E-commerce")
    
finally:
    # Cleanup
    vibium.core.close()
```

### Using the Vibium Class

```python
from python_vibium import Vibium

# Create Vibium instance
vibium = Vibium(device="demo", browser_type="firefox")

# Initialize browser
vibium.core.initialize(headless=True)

try:
    # Use various modules
    vibium.navigation.goto("https://example.com")
    vibium.ecommerce.search_products("smartphone")
    vibium.forms.fill_form({"email": "test@example.com"})
    
finally:
    vibium.core.close()
```

## 📚 Module Examples

### E-commerce Testing

```python
# Add product to cart
vibium.ecommerce.add_to_cart(".product-item", quantity=2)

# Search products
vibium.ecommerce.search_products("wireless headphones")

# Navigate to category
vibium.ecommerce.navigate_to_category("Electronics")

# Get product price
price = vibium.ecommerce.get_product_price(".product-card")

# Get cart count
cart_count = vibium.ecommerce.get_cart_count()
```

### Form Handling

```python
# Fill form with data
form_data = {
    'first_name': 'John',
    'last_name': 'Doe',
    'email': 'john.doe@example.com',
    'password': 'securepass123'
}

vibium.forms.fill_form(form_data, ".signup-form")
vibium.forms.submit_form(".signup-form")

# Validate form errors
expected_errors = {
    'email': 'Invalid email format',
    'password': 'Password too short'
}

vibium.forms.validate_form_errors(expected_errors)
```

### Data Generation

```python
# Generate test data
user_data = vibium.data.generate_user_data()
product_data = vibium.data.generate_product_data()
address_data = vibium.data.generate_address_data()
credit_card_data = vibium.data.generate_credit_card_data()

# Generate multiple items
emails = vibium.data.generate_newsletter_emails(10)
search_queries = vibium.data.generate_search_queries(5)
coupon_codes = vibium.data.generate_coupon_codes(3)
```

### Performance Testing

```python
# Measure page load time
load_time = vibium.performance.measure_load_time("https://example.com")

# Check Core Web Vitals
web_vitals = vibium.performance.check_core_web_vitals()

# Run performance audit
audit_results = vibium.performance.performance_audit("https://example.com")

# Compare performance across URLs
comparison = vibium.performance.compare_performance([
    "https://example.com",
    "https://example.org"
], iterations=3)
```

### Screenshots

```python
# Take full page screenshot
screenshot_path = vibium.screenshots.capture("full_page")

# Take element screenshot
element_screenshot = vibium.screenshots.capture_element(".hero-section")

# Take before/after screenshots
def before_action():
    vibium.elements.click_element(".button")

def after_action():
    vibium.wait.for_element_visible(".modal")

screenshots = vibium.screenshots.capture_before_after(
    "button_click", before_action, after_action
)

# Capture at different viewport sizes
viewport_screenshots = vibium.screenshots.capture_viewport_sizes([
    (1920, 1080),
    (1366, 768),
    (768, 1024)
])
```

### Wait Utilities

```python
# Wait for network idle
vibium.wait.for_network_idle(timeout=30)

# Wait for element visibility
vibium.wait.for_element_visible(".loading-spinner", timeout=10)

# Wait for URL change
vibium.wait.for_url_change("https://example.com", timeout=15)

# Wait for custom condition
def custom_condition():
    return vibium.elements.is_element_visible(".success-message")

vibium.wait.for_condition(custom_condition, timeout=20)
```

## 🖥️ Command Line Interface

The Python Vibium Library includes a comprehensive CLI:

### Basic Commands

```bash
# Show help
vibium --help

# Show version
vibium version

# Run automation
vibium run --url https://example.com --browser chromium --headless

# Run tests
vibium test --browser firefox --screenshot --performance

# Run demonstration
vibium demo --browser webkit --device mobile
```

### CLI Examples

```bash
# Run automation with screenshots
vibium run --url https://ecommercepracticeportal.netlify.app/ --screenshot

# Run tests in Firefox with performance monitoring
vibium test --browser firefox --performance --headless

# Run demo in mobile viewport
vibium demo --browser chromium --device mobile --headless
```

## 🧪 Testing

### Run Tests with Pytest

```bash
# Install test dependencies
pip install -r requirements.txt

# Run all tests
pytest test_python_vibium.py -v

# Run with coverage
pytest test_python_vibium.py --cov=python_vibium --cov-report=html

# Run specific test class
pytest test_python_vibium.py::TestVibiumLibrary -v
```

### Test Examples

```python
import pytest
from python_vibium import create_vibium

class TestEcommerce:
    def test_product_search(self):
        vibium = create_vibium(device="test")
        vibium.core.initialize(headless=True)
        
        try:
            vibium.navigation.goto("https://example.com")
            vibium.ecommerce.search_products("laptop")
            
            # Verify search results
            assert vibium.assertions.is_visible(".search-results")
            
        finally:
            vibium.core.close()
```

## 🔧 Configuration

### Browser Configuration

```python
# Configure different browsers
vibium = create_vibium(device="test", browser_type="firefox")

# Initialize with custom options
vibium.core.initialize(
    headless=True,
    viewport_size={'width': 1920, 'height': 1080}
)
```

### Screenshot Configuration

```python
# Custom screenshot directory
vibium.screenshots.screenshot_dir = "custom_screenshots"

# Custom screenshot naming
screenshot_path = vibium.screenshots.capture("custom_name")
```

## 📁 Project Structure

```
python_vibium/
├── __init__.py                 # Main package initialization
├── cli.py                      # Command line interface
├── setup.py                    # Package setup and configuration
├── core/                       # Core functionality
│   ├── __init__.py
│   └── vibium_core.py
├── ecommerce/                  # E-commerce testing
│   ├── __init__.py
│   └── vibium_ecommerce.py
├── forms/                      # Form handling
│   ├── __init__.py
│   └── vibium_forms.py
├── navigation/                 # Navigation utilities
│   ├── __init__.py
│   └── vibium_navigation.py
├── elements/                   # Element interactions
│   ├── __init__.py
│   └── vibium_elements.py
├── assertions/                 # Assertions and verifications
│   ├── __init__.py
│   └── vibium_assertions.py
├── performance/                # Performance testing
│   ├── __init__.py
│   └── vibium_performance.py
├── screenshots/                # Screenshot management
│   ├── __init__.py
│   └── vibium_screenshots.py
├── data/                       # Test data generation
│   ├── __init__.py
│   └── vibium_data.py
└── wait/                       # Wait utilities
    ├── __init__.py
    └── vibium_wait.py
```

## 🚀 Advanced Usage

### Context Manager

```python
from python_vibium import create_vibium

# Use as context manager for automatic cleanup
with create_vibium(device="test") as vibium:
    vibium.core.initialize()
    vibium.navigation.goto("https://example.com")
    # Browser automatically closed when exiting context
```

### Custom Extensions

```python
from python_vibium.core.vibium_core import VibiumCore

class CustomVibiumCore(VibiumCore):
    def custom_method(self):
        """Custom functionality"""
        return self.page.evaluate("() => document.title")

# Use custom core
vibium = create_vibium(device="custom")
vibium.core = CustomVibiumCore("custom", "chromium")
```

### Error Handling

```python
try:
    vibium.navigation.goto("https://example.com")
    vibium.assertions.is_visible(".main-content")
    
except Exception as e:
    # Take failure screenshot
    failure_screenshot = vibium.screenshots.capture_on_failure("test_name")
    print(f"Test failed: {str(e)}")
    print(f"Failure screenshot: {failure_screenshot}")
    
finally:
    vibium.core.close()
```

## 📊 Performance Monitoring

### Core Web Vitals

```python
# Monitor Core Web Vitals
web_vitals = vibium.performance.check_core_web_vitals()

# Access specific metrics
fcp = web_vitals.get('firstContentfulPaint')
lcp = web_vitals.get('largestContentfulPaint')
fid = web_vitals.get('firstInputDelay')
```

### Load Time Analysis

```python
# Measure multiple page loads
urls = [
    "https://example.com",
    "https://example.org",
    "https://example.net"
]

for url in urls:
    load_time = vibium.performance.measure_load_time(url)
    print(f"{url}: {load_time:.2f}s")
```

## 🔍 Debugging

### Verbose Logging

```python
# Enable verbose logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Vibium provides detailed logging for all operations
vibium.navigation.goto("https://example.com")
# Output: [test] Navigated to: https://example.com
```

### Screenshot Debugging

```python
# Take screenshots at key points
vibium.screenshots.capture("before_action")
vibium.elements.click_element(".button")
vibium.screenshots.capture("after_action")
```

## 🤝 Contributing

### Development Setup

```bash
# Clone repository
git clone https://github.com/vibium/python-vibium.git
cd python-vibium

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest test_python_vibium.py -v

# Run linting
flake8 python_vibium/
black python_vibium/
```

### Code Style

- Follow PEP 8 guidelines
- Use type hints for all function parameters and return values
- Include comprehensive docstrings
- Write unit tests for all new functionality

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

### Documentation

- [API Reference](docs/api.md)
- [Examples](examples/)
- [Troubleshooting](docs/troubleshooting.md)

### Issues

- Report bugs: [GitHub Issues](https://github.com/vibium/python-vibium/issues)
- Feature requests: [GitHub Discussions](https://github.com/vibium/python-vibium/discussions)

### Community

- Join our [Discord Server](https://discord.gg/vibium)
- Follow us on [Twitter](https://twitter.com/vibium_ai)

## 🔮 Roadmap

### Upcoming Features

- **Visual Regression Testing**: Automated visual comparison
- **Mobile Testing**: Enhanced mobile device simulation
- **API Testing**: REST API testing integration
- **Database Testing**: Database state verification
- **Parallel Execution**: Multi-threaded test execution
- **Cloud Integration**: AWS, Azure, and GCP support

### Version History

- **v1.0.0**: Initial release with core functionality
- **v1.1.0**: Enhanced performance monitoring
- **v1.2.0**: Advanced screenshot capabilities
- **v2.0.0**: Major architecture improvements

---

**Built with ❤️ by the Vibium Team**

For more information, visit [https://vibium.com](https://vibium.com)
