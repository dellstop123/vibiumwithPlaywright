import { test, expect } from '@playwright/test';

test.describe('Visual Regression Tests', () => {
  test('should match homepage screenshot', async ({ page }) => {
    await page.goto('/');
    
    // Wait for page to be fully loaded
    await page.waitForLoadState('networkidle');
    
    // Take screenshot and compare with baseline
    await expect(page).toHaveScreenshot('homepage.png');
  });

  test('should match navigation menu screenshot', async ({ page }) => {
    await page.goto('/');
    
    // Ensure navigation is visible
    await page.locator('nav').waitFor({ state: 'visible' });
    
    // Take screenshot of navigation area
    await expect(page.locator('nav')).toHaveScreenshot('navigation.png');
  });

  test('should match mobile viewport screenshot', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    
    // Take mobile screenshot
    await expect(page).toHaveScreenshot('homepage-mobile.png');
  });

  test('should match tablet viewport screenshot', async ({ page }) => {
    // Set tablet viewport
    await page.setViewportSize({ width: 768, height: 1024 });
    
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    
    // Take tablet screenshot
    await expect(page).toHaveScreenshot('homepage-tablet.png');
  });

  test('should match desktop viewport screenshot', async ({ page }) => {
    // Set desktop viewport
    await page.setViewportSize({ width: 1920, height: 1080 });
    
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    
    // Take desktop screenshot
    await expect(page).toHaveScreenshot('homepage-desktop.png');
  });

  test('should handle dynamic content changes', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    
    // Wait for any animations or dynamic content to settle
    await page.waitForTimeout(2000);
    
    // Take screenshot after content settles
    await expect(page).toHaveScreenshot('homepage-settled.png');
  });
});
