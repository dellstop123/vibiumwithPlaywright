import { test, expect } from '@playwright/test';
import { HomePage } from '../pages/home-page';
import { testData, selectors } from '../fixtures/test-data';

test.describe('Navigation Tests', () => {
  let homePage: HomePage;

  test.beforeEach(async ({ page }) => {
    homePage = new HomePage(page);
    await homePage.goto();
  });

  test('should display header navigation', async ({ page }) => {
    await expect(page.locator(selectors.common.header)).toBeVisible();
    await expect(page.locator(selectors.common.navigation)).toBeVisible();
  });

  test('should have all main navigation menu items', async ({ page }) => {
    for (const menuItem of testData.navigation.menuItems) {
      const menuLocator = page.locator(`text=${menuItem}`);
      await expect(menuLocator).toBeVisible();
    }
  });

  test('should navigate to different pages', async ({ page }) => {
    // Test navigation to About page
    await page.click('text=About');
    await expect(page).toHaveURL(/.*about/);
    
    // Test navigation to Services page
    await page.click('text=Services');
    await expect(page).toHaveURL(/.*services/);
    
    // Test navigation to Contact page
    await page.click('text=Contact');
    await expect(page).toHaveURL(/.*contact/);
  });

  test('should have working footer links', async ({ page }) => {
    // Scroll to footer
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    
    for (const footerLink of testData.navigation.footerLinks) {
      const linkLocator = page.locator(`text=${footerLink}`);
      await expect(linkLocator).toBeVisible();
    }
  });

  test('should maintain navigation state across page loads', async ({ page }) => {
    // Navigate to a page
    await page.click('text=About');
    await expect(page).toHaveURL(/.*about/);
    
    // Refresh the page
    await page.reload();
    
    // Should still be on the same page
    await expect(page).toHaveURL(/.*about/);
  });
});
