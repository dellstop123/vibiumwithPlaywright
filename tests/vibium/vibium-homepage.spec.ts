import { test, expect } from '@playwright/test';
import { createVibium } from '../../src/vibium';
import { vibiumTestData, vibiumSelectors } from '../fixtures/vibium-test-data';

test.describe('Vibium Homepage Tests', () => {
  let vibium: any;

  test.beforeEach(async ({ page }, testInfo) => {
    vibium = createVibium(page, testInfo);
    await vibium.navigation.goto('https://ecommercepracticeportal.netlify.app/', 'FashionHub');
  });

  test('should load homepage successfully', async ({ page }) => {
    await vibium.assertions.urlContains('ecommercepracticeportal.netlify.app');
    await expect(page).toHaveTitle(/FashionHub/);
    await expect(page.url()).toBe('https://ecommercepracticeportal.netlify.app/');
  });

  test('should display hero section with correct content', async ({ page }) => {
    // Verify hero section text content
    await vibium.assertions.containsText('h1', 'Discover Your Style');
    await vibium.assertions.containsText('p', 'Explore our latest collection');
    
    // Verify hero section elements are visible
    await vibium.assertions.isVisible('a:has-text("Shop Now"), button:has-text("Shop Now")');
    await vibium.assertions.isVisible('a:has-text("Browse Categories"), button:has-text("Browse Categories")');
  });

  test('should display all main navigation menu items', async ({ page }) => {
    for (const menuItem of vibiumTestData.navigation.mainMenu) {
      const menuLocator = page.locator(`text=${menuItem}`);
      await expect(menuLocator).toBeVisible();
    }
  });

  test('should display category section with correct categories', async ({ page }) => {
    // Verify category section is visible
    await vibium.assertions.isVisible('section:has-text("Shop by Category")');
    
    // Verify specific categories exist
    await vibium.assertions.containsText('section:has-text("Shop by Category")', 'Men');
    await vibium.assertions.containsText('section:has-text("Shop by Category")', 'Women');
    await vibium.assertions.containsText('section:has-text("Shop by Category")', 'Footwear');
    await vibium.assertions.containsText('section:has-text("Shop by Category")', 'Accessories');
  });

  test('should display featured products section', async ({ page }) => {
    // Verify featured products section is visible
    await vibium.assertions.isVisible('section:has-text("Featured Products")');
    
    // Verify products are displayed
    const productItems = page.locator(vibiumSelectors.products.item);
    const productCount = await productItems.count();
    expect(productCount).toBeGreaterThan(0);
    
    // Verify specific products exist
    await vibium.assertions.containsText('section:has-text("Featured Products")', 'Classic White T-Shirt');
    await vibium.assertions.containsText('section:has-text("Featured Products")', 'Floral Summer Dress');
  });

  test('should have working search functionality', async ({ page }) => {
    // Verify search elements are visible
    await vibium.assertions.isVisible('input[placeholder*="Search"]');
    await vibium.assertions.isVisible('button:has-text("Search")');
    
    // Test search with valid query
    const searchQuery = 'shirt';
    await vibium.ecommerce.searchProducts(searchQuery);
    
    // Verify search results or redirect
    await vibium.assertions.urlContains('search') || await vibium.assertions.isVisible('.search-results, .products');
  });

  test('should display newsletter subscription section', async ({ page }) => {
    // Verify newsletter section elements are visible
    await vibium.assertions.isVisible('section:has-text("Stay Updated")');
    await vibium.assertions.isVisible('input[placeholder*="email"], input[type="email"]');
    await vibium.assertions.isVisible('button:has-text("Subscribe")');
    
    // Verify newsletter content
    await vibium.assertions.containsText('h3', 'Stay Updated');
  });

  test('should subscribe to newsletter with valid email', async ({ page }) => {
    const validEmail = vibiumTestData.newsletter.validEmails[0];
    await vibium.ecommerce.subscribeToNewsletter(validEmail);
    
    // Verify success message or redirect
    await vibium.assertions.isVisible(vibiumSelectors.common.successMessage);
  });

  test('should display footer with all links', async ({ page }) => {
    // Scroll to footer
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    
    for (const footerLink of vibiumTestData.navigation.footerLinks) {
      const linkLocator = page.locator(`text=${footerLink}`);
      await expect(linkLocator).toBeVisible();
    }
  });

  test('should display feature highlights', async ({ page }) => {
    for (const feature of vibiumTestData.content.features) {
      const featureLocator = page.locator(`text=${feature}`);
      await expect(featureLocator).toBeVisible();
    }
  });

  test('should have working Shop Now button', async ({ page }) => {
    await vibium.assertions.isVisible('a:has-text("Shop Now"), button:has-text("Shop Now")');
    
    // Click Shop Now button
    await vibium.elements.clickWithRetry('a:has-text("Shop Now"), button:has-text("Shop Now")');
    
    // Should navigate to products page
    await vibium.assertions.urlContains('products') || await vibium.assertions.isVisible('.products');
  });

  test('should have working Browse Categories button', async ({ page }) => {
    await vibium.assertions.isVisible('a:has-text("Browse Categories"), button:has-text("Browse Categories")');
    
    // Click Browse Categories button
    await vibium.elements.clickWithRetry('a:has-text("Browse Categories"), button:has-text("Browse Categories")');
    
    // Should navigate to categories page
    await vibium.assertions.urlContains('categories') || await vibium.assertions.isVisible('.categories');
  });

  test('should display product ratings and prices correctly', async ({ page }) => {
    const productItems = page.locator(vibiumSelectors.products.item);
    const count = await productItems.count();
    
    for (let i = 0; i < Math.min(count, 3); i++) {
      const productItem = productItems.nth(i);
      
      // Check for price
      const price = productItem.locator(vibiumSelectors.products.price);
      await expect(price).toBeVisible();
      
      // Check for rating if available
      const rating = productItem.locator(vibiumSelectors.products.rating);
      if (await rating.isVisible()) {
        const ratingText = await rating.textContent();
        expect(ratingText).toMatch(/[\d.]+/);
      }
    }
  });

  test('should handle responsive design on different viewports', async ({ page }) => {
    // Test mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    await vibium.assertions.isVisible('header');
    await vibium.assertions.isVisible('nav');
    
    // Test tablet viewport
    await page.setViewportSize({ width: 768, height: 1024 });
    await vibium.assertions.isVisible('header');
    await vibium.assertions.isVisible('nav');
    
    // Test desktop viewport
    await page.setViewportSize({ width: 1920, height: 1080 });
    await vibium.assertions.isVisible('header');
    await vibium.assertions.isVisible('nav');
  });

  test('should maintain navigation state across page loads', async ({ page }) => {
    // Navigate to a category
    await vibium.ecommerce.navigateToCategory('Men');
    
    // Refresh the page
    await page.reload();
    
    // Should still be on the same page
    await vibium.assertions.urlContains('men') || await vibium.assertions.isVisible('text=Men');
  });

  test('should display loading states appropriately', async ({ page }) => {
    // Navigate to a new page to trigger loading
    await vibium.ecommerce.navigateToCategory('Women');
    
    // Check for loading spinner (if implemented)
    const loadingSpinner = page.locator(vibiumSelectors.common.loadingSpinner);
    if (await loadingSpinner.isVisible()) {
      await vibium.assertions.isVisible(vibiumSelectors.common.loadingSpinner);
      // Wait for loading to complete
      await vibium.wait.forNetworkIdle();
      await expect(loadingSpinner).not.toBeVisible();
    }
  });

  test('should capture screenshot on test completion', async ({ page }) => {
    // Take a screenshot using Vibium
    await vibium.screenshots.capture('homepage-test');
    
    // Verify page is still functional
    await vibium.assertions.isVisible('header');
  });
});
