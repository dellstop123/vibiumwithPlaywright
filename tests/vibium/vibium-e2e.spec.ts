import { test, expect } from '@playwright/test';
import { createVibium } from '../../src/vibium';
import { vibiumTestData, vibiumSelectors } from '../fixtures/vibium-test-data';

test.describe('Vibium End-to-End Tests', () => {
  let vibium: any;

  test.beforeEach(async ({ page }, testInfo) => {
    vibium = createVibium(page, testInfo);
  });

  test('Complete user journey: Browse, Add to Cart, and Checkout', async ({ page }) => {
    // Step 1: Navigate to homepage
    await vibium.navigation.goto('https://ecommercepracticeportal.netlify.app/', 'FashionHub');
    await vibium.assertions.urlContains('ecommercepracticeportal.netlify.app');
    
    // Step 2: Browse categories
    await vibium.ecommerce.navigateToCategory('Men');
    await vibium.assertions.urlContains('men') || await vibium.assertions.isVisible('text=Men');
    
    // Step 3: View products
    await vibium.assertions.isVisible(vibiumSelectors.products.grid);
    const productCount = await page.locator(vibiumSelectors.products.item).count();
    expect(productCount).toBeGreaterThan(0);
    
    // Step 4: Add product to cart
    await vibium.ecommerce.addProductToCart(vibiumSelectors.products.addToCart, 1);
    
    // Step 5: Return to homepage
    await vibium.navigation.goto('https://ecommercepracticeportal.netlify.app/', 'FashionHub');
    
    // Step 6: Open cart
    await vibium.navigation.clickNavItem('Cart');
    await vibium.assertions.urlContains('cart') || await vibium.assertions.isVisible('.cart, .cart-items');
    
    // Step 7: Verify cart contents
    const cartItemCount = await vibium.ecommerce.getCartItemCount();
    expect(cartItemCount).toBeGreaterThan(0);
    
    // Step 8: Proceed to checkout
    await vibium.elements.clickWithRetry(vibiumSelectors.cart.checkout);
    
    // Verify checkout page or form is displayed
    await vibium.assertions.urlContains('checkout') || await vibium.assertions.isVisible('.checkout-form, .checkout');
  });

  test('User registration and first purchase flow', async ({ page }) => {
    // Step 1: Navigate to homepage
    await vibium.navigation.goto('https://ecommercepracticeportal.netlify.app/', 'FashionHub');
    
    // Step 2: Open signup modal/form
    await vibium.elements.clickWithRetry('a:has-text("Sign Up")');
    
    // Step 3: Fill registration form using Vibium
    const userData = vibium.data.generateUserData();
    const formData = {
      firstName: userData.firstName,
      lastName: userData.lastName,
      email: userData.email,
      password: userData.password,
      confirmPassword: userData.password
    };
    
    await vibium.forms.fillForm(formData);
    
    // Check terms checkbox if available
    const termsCheckbox = page.locator('input[type="checkbox"][name="terms"], input[type="checkbox"]:has-text("I agree")');
    if (await termsCheckbox.isVisible()) {
      await termsCheckbox.check();
    }
    
    // Step 4: Submit form
    await vibium.forms.submitForm('Sign Up');
    
    // Step 5: Verify signup success
    await vibium.assertions.isVisible(vibiumSelectors.common.successMessage);
    
    // Step 6: Login with new credentials
    await vibium.elements.clickWithRetry('a:has-text("Login")');
    await vibium.forms.fillForm({
      email: userData.email,
      password: userData.password
    });
    await vibium.forms.submitForm('Login');
    
    // Step 7: Verify login success
    await vibium.assertions.isVisible(vibiumSelectors.common.successMessage);
    
    // Step 8: Browse and add product to cart
    await vibium.navigation.goto('https://ecommercepracticeportal.netlify.app/', 'FashionHub');
    await vibium.ecommerce.addProductToCart(vibiumSelectors.products.addToCart, 1);
    
    // Step 9: Complete purchase
    await vibium.navigation.clickNavItem('Cart');
    await vibium.elements.clickWithRetry(vibiumSelectors.cart.checkout);
    
    // Verify checkout process
    await vibium.assertions.urlContains('checkout') || await vibium.assertions.isVisible('.checkout-form, .checkout');
  });

  test('Product search and filtering workflow', async ({ page }) => {
    // Step 1: Navigate to homepage
    await vibium.navigation.goto('https://ecommercepracticeportal.netlify.app/', 'FashionHub');
    
    // Step 2: Search for products
    const searchQuery = 'shirt';
    await vibium.ecommerce.searchProducts(searchQuery);
    
    // Step 3: Verify search results
    await vibium.assertions.urlContains('search') || await vibium.assertions.isVisible('.search-results, .products');
    
    // Step 4: Apply category filter
    await vibium.ecommerce.navigateToCategory('Men');
    
    // Step 5: Sort products (if available)
    const sortDropdown = page.locator('select, [data-testid="sort-dropdown"], .sort-select');
    if (await sortDropdown.isVisible()) {
      await sortDropdown.selectOption('Price: Low to High');
      await vibium.wait.forNetworkIdle();
    }
    
    // Step 6: Verify filtered results
    const productCount = await page.locator(vibiumSelectors.products.item).count();
    expect(productCount).toBeGreaterThan(0);
    
    // Step 7: Add filtered product to cart
    await vibium.ecommerce.addProductToCart(vibiumSelectors.products.addToCart, 1);
    
    // Step 8: Verify cart update
    const cartCount = await vibium.ecommerce.getCartItemCount();
    expect(cartCount).toBeGreaterThan(0);
  });

  test('Category browsing and product exploration', async ({ page }) => {
    // Step 1: Navigate to homepage
    await vibium.navigation.goto('https://ecommercepracticeportal.netlify.app/', 'FashionHub');
    
    // Step 2: Browse different categories
    const categories = ['Men', 'Women', 'Accessories'];
    
    for (const category of categories) {
      await vibium.ecommerce.navigateToCategory(category);
      
      // Verify category page loaded
      await vibium.assertions.urlContains(category.toLowerCase()) || await vibium.assertions.isVisible(`text=${category}`);
      
      // Verify products are displayed
      await vibium.assertions.isVisible(vibiumSelectors.products.grid);
      const productCount = await page.locator(vibiumSelectors.products.item).count();
      expect(productCount).toBeGreaterThan(0);
      
      // Return to homepage for next category
      await vibium.navigation.goto('https://ecommercepracticeportal.netlify.app/', 'FashionHub');
    }
  });

  test('Shopping cart management workflow', async ({ page }) => {
    // Step 1: Navigate to homepage
    await vibium.navigation.goto('https://ecommercepracticeportal.netlify.app/', 'FashionHub');
    
    // Step 2: Add multiple products to cart
    const addToCartButtons = page.locator(vibiumSelectors.products.addToCart);
    const productCount = await addToCartButtons.count();
    
    for (let i = 0; i < Math.min(productCount, 3); i++) {
      await addToCartButtons.nth(i).click();
      await vibium.wait.forTimeout(1000);
    }
    
    // Step 3: Open cart
    await vibium.navigation.clickNavItem('Cart');
    await vibium.assertions.urlContains('cart') || await vibium.assertions.isVisible('.cart, .cart-items');
    
    // Step 4: Update quantities
    const quantityInputs = page.locator('input[type="number"], [data-testid="quantity-input"]');
    if (await quantityInputs.count() > 0) {
      await vibium.elements.fillInput('input[type="number"], [data-testid="quantity-input"]', '2');
      await vibium.elements.fillInput('input[type="number"]:nth-child(2)', '3');
    }
    
    // Step 5: Verify cart summary elements
    await vibium.assertions.isVisible(vibiumSelectors.cart.subtotal);
    await vibium.assertions.isVisible(vibiumSelectors.cart.total);
    
    // Step 6: Remove one item
    const initialCount = await vibium.ecommerce.getCartItemCount();
    await vibium.elements.clickWithRetry(vibiumSelectors.cart.removeButton);
    const newCount = await vibium.ecommerce.getCartItemCount();
    expect(newCount).toBe(initialCount - 1);
    
    // Step 7: Continue shopping
    await vibium.elements.clickWithRetry('a:has-text("Continue Shopping")');
    await vibium.assertions.urlContains('/') || await vibium.assertions.isVisible('.products');
  });

  test('Newsletter subscription and user engagement', async ({ page }) => {
    // Step 1: Navigate to homepage
    await vibium.navigation.goto('https://ecommercepracticeportal.netlify.app/', 'FashionHub');
    
    // Step 2: Subscribe to newsletter
    const validEmail = vibiumTestData.newsletter.validEmails[0];
    await vibium.ecommerce.subscribeToNewsletter(validEmail);
    
    // Step 3: Verify subscription success
    await vibium.assertions.isVisible(vibiumSelectors.common.successMessage);
    
    // Step 4: Browse products
    await vibium.ecommerce.navigateToCategory('Women');
    await vibium.assertions.isVisible(vibiumSelectors.products.grid);
    
    // Step 5: Add product to cart
    await vibium.ecommerce.addProductToCart(vibiumSelectors.products.addToCart, 1);
    
    // Step 6: Return to homepage
    await vibium.navigation.goto('https://ecommercepracticeportal.netlify.app/', 'FashionHub');
    
    // Step 7: Verify cart state maintained
    const cartCount = await vibium.ecommerce.getCartItemCount();
    expect(cartCount).toBeGreaterThan(0);
  });

  test('Responsive design and mobile experience', async ({ page }) => {
    // Test different viewport sizes
    const viewports = [
      { width: 375, height: 667, name: 'Mobile' },
      { width: 768, height: 1024, name: 'Tablet' },
      { width: 1920, height: 1080, name: 'Desktop' }
    ];
    
    for (const viewport of viewports) {
      await page.setViewportSize(viewport);
      
      // Step 1: Navigate to homepage
      await vibium.navigation.goto('https://ecommercepracticeportal.netlify.app/', 'FashionHub');
      await vibium.assertions.isVisible('header');
      await vibium.assertions.isVisible('nav');
      
      // Step 2: Browse categories
      await vibium.ecommerce.navigateToCategory('Men');
      await vibium.assertions.isVisible(vibiumSelectors.products.grid);
      
      // Step 3: Add product to cart
      await vibium.ecommerce.addProductToCart(vibiumSelectors.products.addToCart, 1);
      
      // Step 4: Return to homepage
      await vibium.navigation.goto('https://ecommercepracticeportal.netlify.app/', 'FashionHub');
      
      // Step 5: Verify cart functionality
      const cartCount = await vibium.ecommerce.getCartItemCount();
      expect(cartCount).toBeGreaterThan(0);
    }
  });

  test('Error handling and edge cases', async ({ page }) => {
    // Step 1: Test invalid search
    await vibium.navigation.goto('https://ecommercepracticeportal.netlify.app/', 'FashionHub');
    const invalidQuery = vibiumTestData.search.invalidQueries[0];
    await vibium.ecommerce.searchProducts(invalidQuery);
    
    // Step 2: Test newsletter with invalid email
    const invalidEmail = vibiumTestData.newsletter.invalidEmails[0];
    await vibium.ecommerce.subscribeToNewsletter(invalidEmail);
    
    // Step 3: Test form validation
    await vibium.navigation.goto('https://ecommercepracticeportal.netlify.app/login', 'Login');
    await vibium.forms.submitForm('Login');
    await vibium.assertions.isVisible(vibiumSelectors.common.errorMessage);
    
    // Step 4: Test cart edge cases
    await vibium.navigation.goto('https://ecommercepracticeportal.netlify.app/cart', 'Cart');
    
    // Try to checkout with empty cart
    const checkoutButton = page.locator(vibiumSelectors.cart.checkout);
    if (await checkoutButton.isVisible()) {
      await checkoutButton.click();
      // Should show error or redirect back
      await vibium.assertions.urlContains('cart') || await vibium.assertions.isVisible(vibiumSelectors.common.errorMessage);
    }
  });

  test('Performance and user experience', async ({ page }) => {
    // Step 1: Measure homepage load time
    const startTime = Date.now();
    await vibium.navigation.goto('https://ecommercepracticeportal.netlify.app/', 'FashionHub');
    const loadTime = await vibium.performance.measureLoadTime();
    
    // Load time should be reasonable
    expect(loadTime).toBeLessThan(10000); // 10 seconds
    
    // Step 2: Test navigation responsiveness
    const navStartTime = Date.now();
    await vibium.ecommerce.navigateToCategory('Women');
    await vibium.assertions.isVisible(vibiumSelectors.products.grid);
    const navTime = Date.now() - navStartTime;
    
    // Navigation should be fast
    expect(navTime).toBeLessThan(5000); // 5 seconds
    
    // Step 3: Test cart operations
    await vibium.ecommerce.addProductToCart(vibiumSelectors.products.addToCart, 1);
    await vibium.navigation.clickNavItem('Cart');
    
    // Cart should load quickly
    await vibium.assertions.urlContains('cart') || await vibium.assertions.isVisible('.cart, .cart-items');
    
    // Step 4: Verify smooth user experience
    await vibium.assertions.isVisible(vibiumSelectors.common.loadingSpinner, false);
  });

  test('Cross-browser compatibility', async ({ page, browserName }) => {
    // Step 1: Navigate to homepage
    await vibium.navigation.goto('https://ecommercepracticeportal.netlify.app/', 'FashionHub');
    await vibium.assertions.isVisible('header');
    
    // Step 2: Test core functionality
    await vibium.ecommerce.navigateToCategory('Men');
    await vibium.assertions.isVisible(vibiumSelectors.products.grid);
    
    // Step 3: Add product to cart
    await vibium.ecommerce.addProductToCart(vibiumSelectors.products.addToCart, 1);
    
    // Step 4: Verify cart functionality
    await vibium.navigation.clickNavItem('Cart');
    await vibium.assertions.urlContains('cart') || await vibium.assertions.isVisible('.cart, .cart-items');
    
    // Step 5: Test responsive behavior
    await page.setViewportSize({ width: 375, height: 667 });
    await vibium.assertions.isVisible('header');
    
    // Log browser-specific behavior
    console.log(`Test completed successfully on ${browserName}`);
  });

  test('Complete checkout process with Vibium', async ({ page }) => {
    // Step 1: Navigate to homepage and add product
    await vibium.navigation.goto('https://ecommercepracticeportal.netlify.app/', 'FashionHub');
    await vibium.ecommerce.addProductToCart(vibiumSelectors.products.addToCart, 1);
    
    // Step 2: Go to cart and checkout
    await vibium.navigation.clickNavItem('Cart');
    await vibium.elements.clickWithRetry(vibiumSelectors.cart.checkout);
    
    // Step 3: Fill checkout form using Vibium
    const userData = vibium.data.generateUserData();
    const checkoutData = {
      firstName: userData.firstName,
      lastName: userData.lastName,
      email: userData.email,
      address: '123 Test Street',
      city: 'Test City',
      zipCode: '12345',
      cardNumber: '4111111111111111',
      expiryDate: '12/25',
      cvv: '123'
    };
    
    // Fill form if checkout form is available
    if (await page.locator('input[name="firstName"]').isVisible()) {
      await vibium.forms.fillForm(checkoutData);
      await vibium.forms.submitForm('Place Order');
      
      // Verify order completion
      await vibium.assertions.isVisible(vibiumSelectors.common.successMessage);
    }
    
    // Take screenshot of checkout process
    await vibium.screenshots.capture('checkout-complete');
  });
});
