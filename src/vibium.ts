import { Page, Locator, expect, TestInfo } from '@playwright/test';

/**
 * Vibium - E-commerce Testing Library for Playwright
 * A comprehensive library for testing e-commerce websites with Playwright
 */
export class Vibium {
  private page: Page;
  private testInfo: TestInfo;

  constructor(page: Page, testInfo: TestInfo) {
    this.page = page;
    this.testInfo = testInfo;
  }

  /**
   * E-commerce specific testing utilities
   */
  ecommerce = {
    /**
     * Add product to cart with validation
     */
    addToCart: async (productSelector: string, expectedCartCount?: number) => {
      const addButton = this.page.locator(productSelector);
      await addButton.click();
      
      // Wait for cart update
      await this.page.waitForLoadState('networkidle');
      
      if (expectedCartCount !== undefined) {
        const cartCount = await this.getCartItemCount();
        expect(cartCount).toBe(expectedCartCount);
      }
      
      return true;
    },

    /**
     * Get current cart item count
     */
    getCartItemCount: async (): Promise<number> => {
      const cartBadge = this.page.locator('[data-testid="cart-badge"], .cart-badge, .cart-count');
      if (await cartBadge.isVisible()) {
        const text = await cartBadge.textContent();
        return parseInt(text || '0', 10);
      }
      return 0;
    },

    /**
     * Search for products
     */
    searchProducts: async (query: string) => {
      const searchInput = this.page.locator('input[placeholder*="Search"], input[name="search"]');
      await searchInput.fill(query);
      
      const searchButton = this.page.locator('button:has-text("Search"), button[type="submit"]');
      await searchButton.click();
      
      await this.page.waitForLoadState('networkidle');
    },

    /**
     * Navigate to category
     */
    navigateToCategory: async (categoryName: string) => {
      const categoryLink = this.page.locator(`a:has-text("${categoryName}"), [data-testid="category-${categoryName}"]`);
      await categoryLink.click();
      await this.page.waitForLoadState('networkidle');
    },

    /**
     * Subscribe to newsletter
     */
    subscribeToNewsletter: async (email: string) => {
      const emailInput = this.page.locator('input[type="email"], input[placeholder*="email"]');
      await emailInput.fill(email);
      
      const subscribeButton = this.page.locator('button:has-text("Subscribe"), button[type="submit"]');
      await subscribeButton.click();
      
      await this.page.waitForLoadState('networkidle');
    },

    /**
     * Complete checkout process
     */
    checkout: async (userData: {
      firstName: string;
      lastName: string;
      email: string;
      address: string;
      city: string;
      zipCode: string;
      cardNumber: string;
      expiryDate: string;
      cvv: string;
    }) => {
      // Fill shipping information
      await this.page.locator('input[name="firstName"]').fill(userData.firstName);
      await this.page.locator('input[name="lastName"]').fill(userData.lastName);
      await this.page.locator('input[name="email"]').fill(userData.email);
      await this.page.locator('input[name="address"]').fill(userData.address);
      await this.page.locator('input[name="city"]').fill(userData.city);
      await this.page.locator('input[name="zipCode"]').fill(userData.zipCode);

      // Fill payment information
      await this.page.locator('input[name="cardNumber"]').fill(userData.cardNumber);
      await this.page.locator('input[name="expiryDate"]').fill(userData.expiryDate);
      await this.page.locator('input[name="cvv"]').fill(userData.cvv);

      // Complete checkout
      await this.page.locator('button:has-text("Place Order"), button:has-text("Complete Purchase")').click();
      await this.page.waitForLoadState('networkidle');
    }
  };

  /**
   * Form testing utilities
   */
  forms = {
    /**
     * Fill form with data object
     */
    fillForm: async (formData: Record<string, string>) => {
      for (const [fieldName, value] of Object.entries(formData)) {
        const selector = `input[name="${fieldName}"], input[placeholder*="${fieldName}"], textarea[name="${fieldName}"]`;
        const field = this.page.locator(selector);
        if (await field.isVisible()) {
          await field.fill(value);
        }
      }
    },

    /**
     * Submit form
     */
    submitForm: async (submitButtonText?: string) => {
      const submitButton = submitButtonText 
        ? this.page.locator(`button:has-text("${submitButtonText}"), button[type="submit"]`)
        : this.page.locator('button[type="submit"]');
      
      await submitButton.click();
      await this.page.waitForLoadState('networkidle');
    },

    /**
     * Validate form errors
     */
    validateFormErrors: async (expectedErrors: string[]) => {
      for (const error of expectedErrors) {
        const errorElement = this.page.locator(`text=${error}, .error-message:has-text("${error}")`);
        await expect(errorElement).toBeVisible();
      }
    }
  };

  /**
   * Navigation utilities
   */
  navigation = {
    /**
     * Navigate to page with validation
     */
    goto: async (url: string, expectedTitle?: string) => {
      await this.page.goto(url);
      await this.page.waitForLoadState('networkidle');
      
      if (expectedTitle) {
        await expect(this.page).toHaveTitle(new RegExp(expectedTitle, 'i'));
      }
    },

    /**
     * Click navigation item
     */
    clickNavItem: async (itemText: string) => {
      const navItem = this.page.locator(`nav a:has-text("${itemText}"), [data-testid="nav-${itemText}"]`);
      await navItem.click();
      await this.page.waitForLoadState('networkidle');
    },

    /**
     * Verify current page
     */
    verifyPage: async (expectedUrl: string, expectedTitle?: string) => {
      await expect(this.page.url()).toContain(expectedUrl);
      
      if (expectedTitle) {
        await expect(this.page).toHaveTitle(new RegExp(expectedTitle, 'i'));
      }
    }
  };

  /**
   * Element interaction utilities
   */
  elements = {
    /**
     * Wait for element to be stable
     */
    waitForStable: async (selector: string, timeout = 5000) => {
      const element = this.page.locator(selector);
      await element.waitFor({ state: 'visible', timeout });
      await element.waitFor({ state: 'stable', timeout });
    },

    /**
     * Click element with retry
     */
    clickWithRetry: async (selector: string, maxAttempts = 3) => {
      for (let attempt = 1; attempt <= maxAttempts; attempt++) {
        try {
          const element = this.page.locator(selector);
          await element.click();
          return;
        } catch (error) {
          if (attempt === maxAttempts) throw error;
          await this.page.waitForTimeout(1000);
        }
      }
    },

    /**
     * Fill input with validation
     */
    fillInput: async (selector: string, value: string, validate = true) => {
      const input = this.page.locator(selector);
      await input.fill(value);
      
      if (validate) {
        const actualValue = await input.inputValue();
        expect(actualValue).toBe(value);
      }
    }
  };

  /**
   * Assertion utilities
   */
  assertions = {
    /**
     * Assert element contains text
     */
    containsText: async (selector: string, expectedText: string) => {
      const element = this.page.locator(selector);
      await expect(element).toContainText(expectedText);
    },

    /**
     * Assert element is visible
     */
    isVisible: async (selector: string) => {
      const element = this.page.locator(selector);
      await expect(element).toBeVisible();
    },

    /**
     * Assert element count
     */
    hasCount: async (selector: string, expectedCount: number) => {
      const elements = this.page.locator(selector);
      const actualCount = await elements.count();
      expect(actualCount).toBe(expectedCount);
    },

    /**
     * Assert URL contains
     */
    urlContains: async (expectedUrl: string) => {
      await expect(this.page.url()).toContain(expectedUrl);
    }
  };

  /**
   * Performance utilities
   */
  performance = {
    /**
     * Measure page load time
     */
    measureLoadTime: async (): Promise<number> => {
      const startTime = Date.now();
      await this.page.waitForLoadState('networkidle');
      return Date.now() - startTime;
    },

    /**
     * Check Core Web Vitals
     */
    checkCoreWebVitals: async () => {
      const lcp = await this.page.evaluate(() => {
        return new Promise((resolve) => {
          new PerformanceObserver((list) => {
            const entries = list.getEntries();
            const lastEntry = entries[entries.length - 1];
            resolve(lastEntry.startTime);
          }).observe({ entryTypes: ['largest-contentful-paint'] });
        });
      });
      
      return { lcp };
    }
  };

  /**
   * Screenshot utilities
   */
  screenshots = {
    /**
     * Take screenshot with timestamp
     */
    capture: async (name: string) => {
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
      const filename = `vibium-${name}-${timestamp}.png`;
      
      await this.page.screenshot({ 
        path: `test-results/screenshots/${filename}`,
        fullPage: true 
      });
      
      // Attach to test report
      await this.testInfo.attach(`screenshot-${name}`, {
        path: `test-results/screenshots/${filename}`,
        contentType: 'image/png'
      });
      
      return filename;
    },

    /**
     * Take screenshot on failure
     */
    captureOnFailure: async (name: string) => {
      if (this.testInfo.status !== 'passed') {
        await this.screenshots.capture(`failure-${name}`);
      }
    }
  };

  /**
   * Data utilities
   */
  data = {
    /**
     * Generate random email
     */
    generateEmail: (prefix = 'test') => {
      const timestamp = Date.now();
      return `${prefix}-${timestamp}@example.com`;
    },

    /**
     * Generate random string
     */
    generateString: (length = 8) => {
      const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
      let result = '';
      for (let i = 0; i < length; i++) {
        result += chars.charAt(Math.floor(Math.random() * chars.length));
      }
      return result;
    },

    /**
     * Generate test user data
     */
    generateUserData: () => ({
      firstName: this.data.generateString(6),
      lastName: this.data.generateString(8),
      email: this.data.generateEmail(),
      password: `TestPass${this.data.generateString(8)}!`
    })
  };

  /**
   * Wait utilities
   */
  wait = {
    /**
     * Wait for network idle
     */
    forNetworkIdle: async () => {
      await this.page.waitForLoadState('networkidle');
    },

    /**
     * Wait for DOM content loaded
     */
    forDOMContentLoaded: async () => {
      await this.page.waitForLoadState('domcontentloaded');
    },

    /**
     * Wait for specific timeout
     */
    forTimeout: async (ms: number) => {
      await this.page.waitForTimeout(ms);
    }
  };
}

/**
 * Create Vibium instance
 */
export const createVibium = (page: Page, testInfo: TestInfo): Vibium => {
  return new Vibium(page, testInfo);
};

/**
 * Export Vibium class for direct usage
 */
export default Vibium;
