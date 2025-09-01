import { test, expect } from '@playwright/test';
import { createVibium } from '../../src/vibium';

test.describe('Vibium Simple Examples', () => {
  let vibium: any;

  test.beforeEach(async ({ page }, testInfo) => {
    vibium = createVibium(page, testInfo);
  });

  test('Basic Vibium usage - Navigate and verify', async ({ page }) => {
    // Navigate to website using Vibium
    await vibium.navigation.goto('https://ecommercepracticeportal.netlify.app/', 'FashionHub');
    
    // Verify page loaded using Vibium assertions
    await vibium.assertions.urlContains('ecommercepracticeportal.netlify.app');
    await vibium.assertions.isVisible('header');
    await vibium.assertions.isVisible('nav');
    
    // Verify page title
    await expect(page).toHaveTitle(/FashionHub/);
  });

  test('Vibium e-commerce functions - Add to cart', async ({ page }) => {
    // Navigate to homepage
    await vibium.navigation.goto('https://ecommercepracticeportal.netlify.app/', 'FashionHub');
    
    // Add product to cart using Vibium
    await vibium.ecommerce.addProductToCart('button:has-text("Add to Cart")', 1);
    
    // Verify cart count increased
    const cartCount = await vibium.ecommerce.getCartItemCount();
    expect(cartCount).toBeGreaterThan(0);
  });

  test('Vibium form handling - Newsletter subscription', async ({ page }) => {
    // Navigate to homepage
    await vibium.navigation.goto('https://ecommercepracticeportal.netlify.app/', 'FashionHub');
    
    // Subscribe to newsletter using Vibium
    const email = vibium.data.generateEmail('newsletter');
    await vibium.ecommerce.subscribeToNewsletter(email);
    
    // Verify success (this might show a message or redirect)
    console.log(`Subscribed with email: ${email}`);
  });

  test('Vibium navigation - Browse categories', async ({ page }) => {
    // Navigate to homepage
    await vibium.navigation.goto('https://ecommercepracticeportal.netlify.app/', 'FashionHub');
    
    // Navigate to different categories using Vibium
    await vibium.ecommerce.navigateToCategory('Men');
    await vibium.assertions.urlContains('men') || await vibium.assertions.isVisible('text=Men');
    
    await vibium.ecommerce.navigateToCategory('Women');
    await vibium.assertions.urlContains('women') || await vibium.assertions.isVisible('text=Women');
  });

  test('Vibium search functionality', async ({ page }) => {
    // Navigate to homepage
    await vibium.navigation.goto('https://ecommercepracticeportal.netlify.app/', 'FashionHub');
    
    // Search for products using Vibium
    await vibium.ecommerce.searchProducts('shirt');
    
    // Verify search results
    await vibium.assertions.urlContains('search') || await vibium.assertions.isVisible('.search-results, .products');
  });

  test('Vibium performance testing', async ({ page }) => {
    // Navigate to homepage
    await vibium.navigation.goto('https://ecommercepracticeportal.netlify.app/', 'FashionHub');
    
    // Measure load time using Vibium
    const loadTime = await vibium.performance.measureLoadTime();
    console.log(`Page load time: ${loadTime}ms`);
    
    // Check Core Web Vitals
    const webVitals = await vibium.performance.checkCoreWebVitals();
    console.log(`LCP: ${webVitals.lcp}ms`);
  });

  test('Vibium screenshot capture', async ({ page }) => {
    // Navigate to homepage
    await vibium.navigation.goto('https://ecommercepracticeportal.netlify.app/', 'FashionHub');
    
    // Take screenshot using Vibium
    const screenshotName = await vibium.screenshots.capture('homepage-example');
    console.log(`Screenshot saved: ${screenshotName}`);
    
    // Verify page is still functional
    await vibium.assertions.isVisible('header');
  });

  test('Vibium data generation', async ({ page }) => {
    // Generate test data using Vibium
    const userData = vibium.data.generateUserData();
    const randomString = vibium.data.generateString(10);
    const randomEmail = vibium.data.generateEmail('test');
    
    console.log('Generated test data:');
    console.log(`User: ${userData.firstName} ${userData.lastName}`);
    console.log(`Email: ${userData.email}`);
    console.log(`Password: ${userData.password}`);
    console.log(`Random string: ${randomString}`);
    console.log(`Random email: ${randomEmail}`);
    
    // Navigate to homepage to verify everything works
    await vibium.navigation.goto('https://ecommercepracticeportal.netlify.app/', 'FashionHub');
    await vibium.assertions.isVisible('header');
  });

  test('Vibium element interactions', async ({ page }) => {
    // Navigate to homepage
    await vibium.navigation.goto('https://ecommercepracticeportal.netlify.app/', 'FashionHub');
    
    // Test element interactions using Vibium
    await vibium.elements.waitForStable('header');
    
    // Click with retry
    await vibium.elements.clickWithRetry('a:has-text("Products")');
    
    // Wait for navigation
    await vibium.wait.forNetworkIdle();
    
    // Verify navigation worked
    await vibium.assertions.urlContains('products') || await vibium.assertions.isVisible('.products');
  });

  test('Vibium form validation', async ({ page }) => {
    // Navigate to login page
    await vibium.navigation.goto('https://ecommercepracticeportal.netlify.app/login', 'Login');
    
    // Try to submit empty form
    await vibium.forms.submitForm('Login');
    
    // Should show validation errors
    await vibium.assertions.isVisible('.error-message, .alert-error, [data-testid="error-message"]');
  });
});
