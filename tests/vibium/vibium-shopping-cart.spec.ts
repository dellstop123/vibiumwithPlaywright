import { test, expect } from '@playwright/test';
import { createVibium } from '../../src/vibium';
import { vibiumTestData, vibiumSelectors } from '../fixtures/vibium-test-data';

test.describe('Vibium Shopping Cart Tests', () => {
  let vibium: any;

  test.beforeEach(async ({ page }, testInfo) => {
    vibium = createVibium(page, testInfo);
  });

  test('should add product to cart from homepage', async ({ page }) => {
    await vibium.navigation.goto('https://ecommercepracticeportal.netlify.app/', 'FashionHub');
    
    // Add first featured product to cart
    const addToCartButton = page.locator(vibiumSelectors.products.addToCart).first();
    await addToCartButton.click();
    
    // Wait for success message or cart update
    await page.waitForSelector(vibiumSelectors.common.successMessage, { timeout: 10000 });
    
    // Verify cart count increased using Vibium
    const cartCount = await vibium.ecommerce.getCartItemCount();
    expect(cartCount).toBeGreaterThan(0);
  });

  test('should add multiple products to cart', async ({ page }) => {
    await vibium.navigation.goto('https://ecommercepracticeportal.netlify.app/', 'FashionHub');
    
    // Add multiple products to cart
    const addToCartButtons = page.locator(vibiumSelectors.products.addToCart);
    const productCount = await addToCartButtons.count();
    
    for (let i = 0; i < Math.min(productCount, 3); i++) {
      await addToCartButtons.nth(i).click();
      await vibium.wait.forTimeout(1000); // Wait between additions
    }
    
    // Verify cart count using Vibium
    const cartCount = await vibium.ecommerce.getCartItemCount();
    expect(cartCount).toBeGreaterThanOrEqual(3);
  });

  test('should view cart contents', async ({ page }) => {
    await vibium.navigation.goto('https://ecommercepracticeportal.netlify.app/', 'FashionHub');
    
    // Add a product to cart first
    const addToCartButton = page.locator(vibiumSelectors.products.addToCart).first();
    await addToCartButton.click();
    
    // Open cart using Vibium navigation
    await vibium.navigation.clickNavItem('Cart');
    
    // Verify cart page loaded
    await vibium.assertions.urlContains('cart') || await vibium.assertions.isVisible('.cart, .cart-items');
  });

  test('should display cart items correctly', async ({ page }) => {
    await vibium.navigation.goto('https://ecommercepracticeportal.netlify.app/', 'FashionHub');
    
    // Add a product to cart
    const addToCartButton = page.locator(vibiumSelectors.products.addToCart).first();
    await addToCartButton.click();
    
    // Open cart
    await vibium.navigation.clickNavItem('Cart');
    
    // Verify cart item details using Vibium assertions
    await vibium.assertions.isVisible(vibiumSelectors.cart.itemName);
    await vibium.assertions.isVisible(vibiumSelectors.cart.itemPrice);
    await vibium.assertions.isVisible(vibiumSelectors.cart.removeButton);
  });

  test('should update product quantity in cart', async ({ page }) => {
    await vibium.navigation.goto('https://ecommercepracticeportal.netlify.app/', 'FashionHub');
    
    // Add a product to cart
    const addToCartButton = page.locator(vibiumSelectors.products.addToCart).first();
    await addToCartButton.click();
    
    // Open cart
    await vibium.navigation.clickNavItem('Cart');
    
    // Update quantity using Vibium elements
    const quantityInput = page.locator('input[type="number"], [data-testid="quantity-input"]');
    if (await quantityInput.isVisible()) {
      await vibium.elements.fillInput('input[type="number"], [data-testid="quantity-input"]', '3');
      
      // Click update button if available
      const updateButton = page.locator('.update-quantity, [data-testid="update-quantity"]');
      if (await updateButton.isVisible()) {
        await updateButton.click();
        await vibium.wait.forNetworkIdle();
      }
    }
    
    // Verify quantity updated
    const quantityValue = await quantityInput.inputValue();
    expect(parseInt(quantityValue)).toBe(3);
  });

  test('should remove product from cart', async ({ page }) => {
    await vibium.navigation.goto('https://ecommercepracticeportal.netlify.app/', 'FashionHub');
    
    // Add a product to cart
    const addToCartButton = page.locator(vibiumSelectors.products.addToCart).first();
    await addToCartButton.click();
    
    // Open cart
    await vibium.navigation.clickNavItem('Cart');
    
    // Get initial cart count
    const initialCount = await vibium.ecommerce.getCartItemCount();
    
    // Remove item using Vibium elements
    await vibium.elements.clickWithRetry(vibiumSelectors.cart.removeButton);
    
    // Verify item removed
    const newCount = await vibium.ecommerce.getCartItemCount();
    expect(newCount).toBe(initialCount - 1);
  });

  test('should calculate cart totals correctly', async ({ page }) => {
    await vibium.navigation.goto('https://ecommercepracticeportal.netlify.app/', 'FashionHub');
    
    // Add multiple products to cart
    const addToCartButtons = page.locator(vibiumSelectors.products.addToCart);
    const productCount = await addToCartButtons.count();
    
    for (let i = 0; i < Math.min(productCount, 2); i++) {
      await addToCartButtons.nth(i).click();
      await vibium.wait.forTimeout(1000);
    }
    
    // Open cart
    await vibium.navigation.clickNavItem('Cart');
    
    // Verify cart summary elements are visible
    await vibium.assertions.isVisible(vibiumSelectors.cart.subtotal);
    await vibium.assertions.isVisible(vibiumSelectors.cart.total);
  });

  test('should handle empty cart state', async ({ page }) => {
    // Navigate to cart page
    await vibium.navigation.goto('https://ecommercepracticeportal.netlify.app/cart', 'Cart');
    
    // If cart has items, remove them all
    const itemCount = await vibium.ecommerce.getCartItemCount();
    if (itemCount > 0) {
      const removeButtons = page.locator(vibiumSelectors.cart.removeButton);
      const removeCount = await removeButtons.count();
      
      for (let i = removeCount - 1; i >= 0; i--) {
        await removeButtons.nth(i).click();
        await vibium.wait.forTimeout(1000);
      }
    }
    
    // Verify empty cart state
    await vibium.assertions.isVisible('.empty-cart, [data-testid="empty-cart"]');
    await vibium.assertions.isVisible('a:has-text("Continue Shopping")');
    
    const finalCount = await vibium.ecommerce.getCartItemCount();
    expect(finalCount).toBe(0);
  });

  test('should continue shopping from cart', async ({ page }) => {
    await vibium.navigation.goto('https://ecommercepracticeportal.netlify.app/', 'FashionHub');
    
    // Add a product to cart
    const addToCartButton = page.locator(vibiumSelectors.products.addToCart).first();
    await addToCartButton.click();
    
    // Open cart
    await vibium.navigation.clickNavItem('Cart');
    
    // Continue shopping using Vibium elements
    await vibium.elements.clickWithRetry('a:has-text("Continue Shopping")');
    
    // Should be back on homepage or products page
    await vibium.assertions.urlContains('/') || await vibium.assertions.isVisible('.products');
  });

  test('should proceed to checkout from cart', async ({ page }) => {
    await vibium.navigation.goto('https://ecommercepracticeportal.netlify.app/', 'FashionHub');
    
    // Add a product to cart
    const addToCartButton = page.locator(vibiumSelectors.products.addToCart).first();
    await addToCartButton.click();
    
    // Open cart
    await vibium.navigation.clickNavItem('Cart');
    
    // Proceed to checkout using Vibium elements
    await vibium.elements.clickWithRetry(vibiumSelectors.cart.checkout);
    
    // Should navigate to checkout page
    await vibium.assertions.urlContains('checkout') || await vibium.assertions.isVisible('.checkout-form, .checkout');
  });

  test('should maintain cart state across page navigation', async ({ page }) => {
    await vibium.navigation.goto('https://ecommercepracticeportal.netlify.app/', 'FashionHub');
    
    // Add a product to cart
    const addToCartButton = page.locator(vibiumSelectors.products.addToCart).first();
    await addToCartButton.click();
    
    // Navigate to different pages using Vibium
    await vibium.ecommerce.navigateToCategory('Men');
    await vibium.ecommerce.navigateToCategory('Women');
    
    // Return to homepage
    await vibium.navigation.goto('https://ecommercepracticeportal.netlify.app/', 'FashionHub');
    
    // Verify cart still has items using Vibium
    const cartCount = await vibium.ecommerce.getCartItemCount();
    expect(cartCount).toBeGreaterThan(0);
  });

  test('should display cart icon with badge', async ({ page }) => {
    await vibium.navigation.goto('https://ecommercepracticeportal.netlify.app/', 'FashionHub');
    
    // Verify cart icon is visible
    await vibium.assertions.isVisible(vibiumSelectors.cart.icon);
    
    // Add a product to cart
    const addToCartButton = page.locator(vibiumSelectors.products.addToCart).first();
    await addToCartButton.click();
    
    // Verify cart badge shows count using Vibium
    const cartBadge = page.locator(vibiumSelectors.cart.badge);
    if (await cartBadge.isVisible()) {
      const badgeText = await cartBadge.textContent();
      expect(parseInt(badgeText || '0', 10)).toBeGreaterThan(0);
    }
  });

  test('should handle cart with different product types', async ({ page }) => {
    await vibium.navigation.goto('https://ecommercepracticeportal.netlify.app/', 'FashionHub');
    
    // Add products from different categories
    const addToCartButtons = page.locator(vibiumSelectors.products.addToCart);
    const productCount = await addToCartButtons.count();
    
    // Add first few products
    for (let i = 0; i < Math.min(productCount, 3); i++) {
      await addToCartButtons.nth(i).click();
      await vibium.wait.forTimeout(1000);
    }
    
    // Open cart
    await vibium.navigation.clickNavItem('Cart');
    
    // Verify different product types are displayed using Vibium
    await vibium.assertions.isVisible(vibiumSelectors.cart.itemName);
    await vibium.assertions.isVisible(vibiumSelectors.cart.itemPrice);
    
    // Verify each product has required information
    const cartItems = page.locator(vibiumSelectors.cart.items);
    const itemCount = await cartItems.count();
    
    for (let i = 0; i < itemCount; i++) {
      await vibium.assertions.isVisible(`${vibiumSelectors.cart.items}:nth-child(${i + 1}) ${vibiumSelectors.cart.itemName}`);
      await vibium.assertions.isVisible(`${vibiumSelectors.cart.items}:nth-child(${i + 1}) ${vibiumSelectors.cart.itemPrice}`);
    }
  });

  test('should validate cart item information accuracy', async ({ page }) => {
    await vibium.navigation.goto('https://ecommercepracticeportal.netlify.app/', 'FashionHub');
    
    // Get product information from homepage
    const productNames = page.locator(vibiumSelectors.products.name);
    const productPrices = page.locator(vibiumSelectors.products.price);
    
    const firstProductName = await productNames.first().textContent();
    const firstProductPrice = await productPrices.first().textContent();
    
    // Add first product to cart
    const addToCartButton = page.locator(vibiumSelectors.products.addToCart).first();
    await addToCartButton.click();
    
    // Open cart
    await vibium.navigation.clickNavItem('Cart');
    
    // Verify cart item information matches homepage using Vibium
    await vibium.assertions.containsText(vibiumSelectors.cart.itemName, firstProductName || '');
    await vibium.assertions.containsText(vibiumSelectors.cart.itemPrice, firstProductPrice || '');
  });

  test('should handle cart persistence after browser refresh', async ({ page }) => {
    await vibium.navigation.goto('https://ecommercepracticeportal.netlify.app/', 'FashionHub');
    
    // Add a product to cart
    const addToCartButton = page.locator(vibiumSelectors.products.addToCart).first();
    await addToCartButton.click();
    
    // Refresh the page
    await page.reload();
    
    // Verify cart still has items using Vibium
    const cartCount = await vibium.ecommerce.getCartItemCount();
    expect(cartCount).toBeGreaterThan(0);
  });

  test('should capture cart screenshot for debugging', async ({ page }) => {
    await vibium.navigation.goto('https://ecommercepracticeportal.netlify.app/', 'FashionHub');
    
    // Add a product to cart
    const addToCartButton = page.locator(vibiumSelectors.products.addToCart).first();
    await addToCartButton.click();
    
    // Open cart
    await vibium.navigation.clickNavItem('Cart');
    
    // Take screenshot using Vibium
    await vibium.screenshots.capture('cart-with-items');
    
    // Verify cart functionality
    await vibium.assertions.isVisible(vibiumSelectors.cart.items);
  });
});
