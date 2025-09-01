import { test, expect } from '@playwright/test';

test.describe('Example Test Suite', () => {
  test('should navigate to homepage', async ({ page }) => {
    // Navigate to the homepage
    await page.goto('/');
    
    // Verify the page title
    await expect(page).toHaveTitle(/Vibium/);
  });

  test('should have basic page structure', async ({ page }) => {
    await page.goto('/');
    
    // Check if page loads without errors
    await expect(page.locator('body')).toBeVisible();
    
    // Add more specific assertions based on your app structure
    // await expect(page.locator('header')).toBeVisible();
    // await expect(page.locator('main')).toBeVisible();
  });
});
