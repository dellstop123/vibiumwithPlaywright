# Vibium Playwright Test Automation Framework

A comprehensive Playwright test automation framework specifically designed for the **Vibium E-commerce Platform** at [https://ecommercepracticeportal.netlify.app/](https://ecommercepracticeportal.netlify.app/).

## 🎯 **Project Overview**

This framework provides complete UI automation coverage for the Vibium e-commerce website, including:
- **Homepage functionality** - Hero sections, categories, featured products, newsletter
- **Product management** - Browsing, searching, filtering, adding to cart
- **Shopping cart** - Add/remove items, quantity updates, total calculations
- **User authentication** - Login, signup, password reset
- **E2E workflows** - Complete user journeys from browsing to checkout
- **Cross-browser testing** - Chrome, Firefox, Safari, and mobile devices

## 🏗️ **Architecture**

### **Vibium Library Structure**
```
vibium-playwright/
├── src/
│   ├── vibium.ts         # Main Vibium testing library
│   ├── vibium.d.ts       # TypeScript declarations
│   └── package.json      # Vibium library package
├── tests/
│   ├── vibium/           # Vibium-specific test files
│   │   ├── vibium-homepage.spec.ts      # Homepage tests using Vibium
│   │   ├── vibium-shopping-cart.spec.ts # Cart tests using Vibium
│   │   ├── vibium-e2e.spec.ts           # E2E tests using Vibium
│   │   └── vibium-simple-example.spec.ts # Basic Vibium examples
│   ├── fixtures/         # Test data and selectors
│   └── utils/            # Common utility functions
├── playwright.config.ts  # Playwright configuration
├── package.json          # Dependencies and scripts
└── VIBIUM_README.md      # This file
```

### **Key Design Principles**
1. **Library-First Approach** - Uses the actual Vibium library for all testing operations
2. **Modular Design** - Organized into logical modules (ecommerce, forms, navigation, etc.)
3. **Type Safety** - Full TypeScript support with proper interfaces
4. **E-commerce Focused** - Built specifically for e-commerce testing scenarios

## 🚀 **Quick Start**

### **Prerequisites**
- Node.js 16+
- npm or yarn
- Git

### **Installation**
```bash
# Clone the repository
git clone <repository-url>
cd vibium-playwright

# Install dependencies
npm install

# Install Playwright browsers
npm run test:install

# Install system dependencies (macOS/Linux)
npm run test:install-deps
```

### **Running Tests**

#### **Run All Vibium Tests**
```bash
npm test
```

#### **Run Specific Test Categories**
```bash
# Homepage tests only
npx playwright test tests/vibium/vibium-homepage.spec.ts

# Shopping cart tests only
npx playwright test tests/vibium/vibium-shopping-cart.spec.ts

# E2E tests only
npx playwright test tests/vibium/vibium-e2e.spec.ts
```

#### **Run with Different Browsers**
```bash
# Chrome only
npx playwright test --project=chromium

# Firefox only
npx playwright test --project=firefox

# Safari only
npx playwright test --project=webkit

# Mobile testing
npx playwright test --project="Mobile Chrome"
```

#### **Run with UI Mode**
```bash
npm run test:ui
```

## 📋 **Test Coverage**

### **Homepage Tests (`vibium-homepage.spec.ts`)**
- ✅ Page loading and responsiveness
- ✅ Hero section content verification
- ✅ Navigation menu functionality
- ✅ Category section display
- ✅ Featured products section
- ✅ Search functionality
- ✅ Newsletter subscription
- ✅ Footer links and features
- ✅ Responsive design across viewports

### **Shopping Cart Tests (`vibium-shopping-cart.spec.ts`)**
- ✅ Add products to cart
- ✅ Multiple product addition
- ✅ Cart item management
- ✅ Quantity updates
- ✅ Item removal
- ✅ Total calculations
- ✅ Cart persistence
- ✅ Checkout flow initiation

### **E2E Tests (`vibium-e2e.spec.ts`)**
- ✅ Complete user journey workflows
- ✅ User registration and purchase flow
- ✅ Product search and filtering
- ✅ Category browsing
- ✅ Cart management workflows
- ✅ Newsletter and user engagement
- ✅ Responsive design testing
- ✅ Error handling and edge cases
- ✅ Performance testing
- ✅ Cross-browser compatibility

## 🔧 **Configuration**

### **Playwright Config (`playwright.config.ts`)**
```typescript
export default defineConfig({
  testDir: './tests',
  baseURL: 'https://ecommercepracticeportal.netlify.app',
  fullyParallel: true,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  
  use: {
    actionTimeout: 10000,
    navigationTimeout: 30000,
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
    { name: 'Mobile Chrome', use: { ...devices['Pixel 5'] } },
    { name: 'Mobile Safari', use: { ...devices['iPhone 12'] } },
  ],
});
```

### **Environment Variables**
Create a `.env` file for environment-specific settings:
```env
BASE_URL=https://ecommercepracticeportal.netlify.app
TEST_USER_EMAIL=test@vibium.com
TEST_USER_PASSWORD=TestPassword123!
API_BASE_URL=https://ecommercepracticeportal.netlify.app/api
```

## 📊 **Test Data Management**

### **Test Data Structure (`vibium-test-data.ts`)**
```typescript
export const vibiumTestData = {
  users: {
    validUser: { email: 'test@vibium.com', password: 'TestPassword123!' },
    newUser: { firstName: 'John', lastName: 'Doe', email: 'john@vibium.com' }
  },
  products: {
    classicWhiteTshirt: { name: 'Classic White T-Shirt', price: '$29.99' },
    floralSummerDress: { name: 'Floral Summer Dress', price: '$89.99' }
  },
  categories: ['Men', 'Women', 'Footwear', 'Accessories'],
  search: { validQueries: ['shirt', 'dress', 'jeans'], invalidQueries: ['xyz123'] }
};
```

### **Selector Management (`vibiumSelectors`)**
```typescript
export const vibiumSelectors = {
  products: {
    grid: '.product-grid, [data-testid="product-grid"]',
    item: '.product-item, [data-testid="product-item"]',
    addToCart: '.add-to-cart, [data-testid="add-to-cart"]'
  },
  cart: {
    icon: '[data-testid="cart-icon"], .cart-icon',
    items: '.cart-item, [data-testid="cart-item"]'
  }
};
```

## 🧪 **Writing New Tests**

### **Adding a New Page Object**
```typescript
import { Page, Locator, expect } from '@playwright/test';
import { VibiumBasePage } from './vibium-base-page';

export class VibiumNewPage extends VibiumBasePage {
  readonly newElement: Locator;
  
  constructor(page: Page) {
    super(page);
    this.newElement = page.locator('.new-element');
  }
  
  async expectPageLoaded() {
    await super.expectPageLoaded();
    await expect(this.newElement).toBeVisible();
  }
  
  async performAction() {
    await this.newElement.click();
    await this.page.waitForLoadState('networkidle');
  }
}
```

### **Adding New Test Scenarios**
```typescript
import { test, expect } from '@playwright/test';
import { VibiumNewPage } from '../pages/vibium-new-page';

test.describe('New Feature Tests', () => {
  let newPage: VibiumNewPage;
  
  test.beforeEach(async ({ page }) => {
    newPage = new VibiumNewPage(page);
  });
  
  test('should perform new action', async ({ page }) => {
    await newPage.goto('/new-feature');
    await newPage.expectPageLoaded();
    await newPage.performAction();
    
    // Add assertions
    await expect(page.locator('.result')).toBeVisible();
  });
});
```

## 📈 **Test Execution and Reporting**

### **Test Reports**
```bash
# HTML Report
npm run test:html

# JSON Report
npx playwright test --reporter=json

# JUnit Report
npx playwright test --reporter=junit
```

### **Screenshots and Videos**
- **Screenshots**: Automatically captured on test failure
- **Videos**: Recorded on test failure for debugging
- **Traces**: Collected on first retry for detailed analysis

### **CI/CD Integration**
```yaml
# GitHub Actions example
- name: Run Playwright Tests
  run: npm test
  
- name: Upload Test Results
  uses: actions/upload-artifact@v2
  with:
    name: playwright-report
    path: playwright-report/
```

## 🐛 **Troubleshooting**

### **Common Issues**

#### **Element Not Found**
```typescript
// Use multiple selector strategies
readonly element = page.locator('.primary-selector, [data-testid="fallback"], .fallback-selector');
```

#### **Timing Issues**
```typescript
// Wait for element stability
await this.waitForElementStable(locator, 10000);

// Wait for network idle
await this.page.waitForLoadState('networkidle');
```

#### **Cross-browser Compatibility**
```typescript
// Test specific browser behavior
test('should work on mobile', async ({ page, browserName }) => {
  if (browserName === 'webkit') {
    // Safari-specific logic
  }
});
```

### **Debug Mode**
```bash
# Run tests in debug mode
npm run test:debug

# Run specific test with debug
npx playwright test --debug tests/vibium/vibium-homepage.spec.ts
```

## 📝 **Writing Tests with Vibium Library**

### **Basic Vibium Usage**

```typescript
import { test, expect } from '@playwright/test';
import { createVibium } from '../../src/vibium';

test.describe('Vibium Tests', () => {
  let vibium: any;

  test.beforeEach(async ({ page }, testInfo) => {
    vibium = createVibium(page, testInfo);
  });

  test('should navigate and verify page', async ({ page }) => {
    // Navigate using Vibium
    await vibium.navigation.goto('https://ecommercepracticeportal.netlify.app/', 'FashionHub');
    
    // Verify using Vibium assertions
    await vibium.assertions.urlContains('ecommercepracticeportal.netlify.app');
    await vibium.assertions.isVisible('header');
  });
});
```

### **Vibium Library Modules**

#### **E-commerce Functions**
```typescript
// Add product to cart
await vibium.ecommerce.addProductToCart('button:has-text("Add to Cart")', 1);

// Navigate to category
await vibium.ecommerce.navigateToCategory('Men');

// Search products
await vibium.ecommerce.searchProducts('shirt');

// Subscribe to newsletter
await vibium.ecommerce.subscribeToNewsletter('test@example.com');
```

#### **Form Handling**
```typescript
// Fill form with data object
await vibium.forms.fillForm({
  firstName: 'John',
  lastName: 'Doe',
  email: 'john@example.com'
});

// Submit form
await vibium.forms.submitForm('Sign Up');

// Validate form errors
await vibium.forms.validateFormErrors(['Email is required']);
```

#### **Navigation & Assertions**
```typescript
// Navigate with title validation
await vibium.navigation.goto('/products', 'Products');

// Click navigation item
await vibium.navigation.clickNavItem('Cart');

// Verify page
await vibium.navigation.verifyPage('/cart', 'Shopping Cart');
```

#### **Element Interactions**
```typescript
// Wait for element stability
await vibium.elements.waitForStable('.product-grid');

// Click with retry
await vibium.elements.clickWithRetry('.add-to-cart');

// Fill input with validation
await vibium.elements.fillInput('input[name="email"]', 'test@example.com');
```

#### **Performance & Screenshots**
```typescript
// Measure load time
const loadTime = await vibium.performance.measureLoadTime();

// Check Core Web Vitals
const webVitals = await vibium.performance.checkCoreWebVitals();

// Take screenshot
await vibium.screenshots.capture('test-completion');
```

#### **Data Generation**
```typescript
// Generate test user data
const userData = vibium.data.generateUserData();

// Generate random email
const email = vibium.data.generateEmail('test');

// Generate random string
const randomString = vibium.data.generateString(10);
```

## 📚 **Best Practices**

### **Test Design**
1. **Use descriptive test names** - Clear indication of what is being tested
2. **Follow AAA pattern** - Arrange, Act, Assert
3. **Test one thing at a time** - Single responsibility per test
4. **Use data-driven testing** - Leverage test data fixtures

### **Vibium Library Best Practices**
1. **Initialize Vibium in beforeEach** - Create fresh instance for each test
2. **Use Vibium methods consistently** - Leverage the library's built-in functionality
3. **Handle errors gracefully** - Use Vibium's retry and wait mechanisms
4. **Maintain test data** - Use Vibium's data generation utilities

### **Selectors**
1. **Use data-testid when available** - Most reliable selector strategy
2. **Fallback to semantic selectors** - CSS classes, text content
3. **Avoid brittle selectors** - Don't rely on implementation details
4. **Centralize selector management** - Single source of truth

## 🔄 **Maintenance**

### **Regular Updates**
- Update Playwright version monthly
- Review and update selectors as needed
- Update test data for new products/features
- Monitor test stability and performance

### **Test Maintenance**
- Remove obsolete tests
- Update test data regularly
- Refactor common patterns
- Optimize test execution time

## 🤝 **Contributing**

### **Development Workflow**
1. Create feature branch
2. Add tests for new functionality
3. Update existing tests if needed
4. Ensure all tests pass
5. Submit pull request

### **Code Standards**
- Follow TypeScript best practices
- Use consistent naming conventions
- Add proper documentation
- Include error handling

## 📞 **Support**

### **Getting Help**
- Check existing documentation
- Review test examples
- Check Playwright documentation
- Create issue for bugs

### **Resources**
- [Playwright Documentation](https://playwright.dev/)
- [Vibium Website](https://ecommercepracticeportal.netlify.app/)
- [Vibium Library Source](./src/vibium.ts)
- [Test Examples](./tests/vibium/)
- [Vibium Type Definitions](./src/vibium.d.ts)

---

**Vibium Playwright Framework** - Empowering reliable e-commerce testing automation! 🚀
