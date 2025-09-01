import { test, expect } from '@playwright/test';

test.describe('Performance Tests', () => {
  test('should load homepage within performance budget', async ({ page }) => {
    // Start performance monitoring
    await page.goto('/');
    
    // Wait for page to be fully loaded
    await page.waitForLoadState('networkidle');
    
    // Get performance metrics
    const performanceMetrics = await page.evaluate(() => {
      const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
      return {
        domContentLoaded: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
        loadComplete: navigation.loadEventEnd - navigation.loadEventStart,
        totalLoadTime: navigation.loadEventEnd - navigation.fetchStart,
        firstContentfulPaint: performance.getEntriesByName('first-contentful-paint')[0]?.startTime || 0
      };
    });
    
    // Assert performance metrics are within acceptable ranges
    expect(performanceMetrics.domContentLoaded).toBeLessThan(1000); // 1 second
    expect(performanceMetrics.loadComplete).toBeLessThan(2000); // 2 seconds
    expect(performanceMetrics.totalLoadTime).toBeLessThan(5000); // 5 seconds
    
    if (performanceMetrics.firstContentfulPaint > 0) {
      expect(performanceMetrics.firstContentfulPaint).toBeLessThan(2000); // 2 seconds
    }
  });

  test('should have acceptable Core Web Vitals', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    
    // Measure Largest Contentful Paint (LCP)
    const lcp = await page.evaluate(() => {
      return new Promise((resolve) => {
        new PerformanceObserver((list) => {
          const entries = list.getEntries();
          const lastEntry = entries[entries.length - 1];
          resolve(lastEntry.startTime);
        }).observe({ entryTypes: ['largest-contentful-paint'] });
      });
    });
    
    // LCP should be under 2.5 seconds for good performance
    expect(lcp).toBeLessThan(2500);
  });

  test('should handle multiple page loads efficiently', async ({ page }) => {
    const loadTimes: number[] = [];
    
    // Load the page multiple times to measure consistency
    for (let i = 0; i < 3; i++) {
      const startTime = Date.now();
      await page.goto('/');
      await page.waitForLoadState('networkidle');
      const endTime = Date.now();
      
      loadTimes.push(endTime - startTime);
    }
    
    // Calculate average load time
    const averageLoadTime = loadTimes.reduce((a, b) => a + b, 0) / loadTimes.length;
    
    // Average load time should be under 3 seconds
    expect(averageLoadTime).toBeLessThan(3000);
    
    // Load times should be consistent (within 50% of average)
    const variance = loadTimes.map(time => Math.abs(time - averageLoadTime) / averageLoadTime);
    const maxVariance = Math.max(...variance);
    expect(maxVariance).toBeLessThan(0.5);
  });

  test('should optimize resource loading', async ({ page }) => {
    await page.goto('/');
    
    // Get resource loading information
    const resourceMetrics = await page.evaluate(() => {
      const resources = performance.getEntriesByType('resource');
      return {
        totalResources: resources.length,
        imageResources: resources.filter(r => r.initiatorType === 'img').length,
        scriptResources: resources.filter(r => r.initiatorType === 'script').length,
        cssResources: resources.filter(r => r.initiatorType === 'css').length
      };
    });
    
    // Assert reasonable resource counts
    expect(resourceMetrics.totalResources).toBeLessThan(50); // Not too many resources
    expect(resourceMetrics.scriptResources).toBeLessThan(20); // Reasonable script count
    expect(resourceMetrics.cssResources).toBeLessThan(10); // Reasonable CSS count
  });

  test('should handle network throttling gracefully', async ({ page, context }) => {
    // Simulate slow network
    await context.route('**/*', route => {
      route.continue();
    });
    
    // Set network conditions (slow 3G)
    await context.setExtraHTTPHeaders({
      'X-Playwright-Network-Conditions': 'slow-3g'
    });
    
    const startTime = Date.now();
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    const endTime = Date.now();
    
    const loadTime = endTime - startTime;
    
    // Even with slow network, page should load within reasonable time
    expect(loadTime).toBeLessThan(15000); // 15 seconds for slow 3G
  });
});
