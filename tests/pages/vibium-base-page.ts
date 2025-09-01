import { Page, Locator, expect } from '@playwright/test';

export class VibiumBasePage {
  readonly page: Page;
  
  // Common selectors
  readonly header: Locator;
  readonly footer: Locator;
  readonly navigation: Locator;
  readonly searchInput: Locator;
  readonly searchButton: Locator;
  readonly loginButton: Locator;
  readonly signUpButton: Locator;
  readonly cartIcon: Locator;
  readonly userMenu: Locator;

  constructor(page: Page) {
    this.page = page;
    
    // Initialize common locators
    this.header = page.locator('header');
    this.footer = page.locator('footer');
    this.navigation = page.locator('nav');
    this.searchInput = page.locator('input[placeholder="Search"]');
    this.searchButton = page.locator('button:has-text("Search")');
    this.loginButton = page.locator('a:has-text("Login")');
    this.signUpButton = page.locator('a:has-text("Sign Up")');
    this.cartIcon = page.locator('[data-testid="cart-icon"], .cart-icon, a:has-text("Cart")');
    this.userMenu = page.locator('[data-testid="user-menu"], .user-menu');
  }

  async goto(path: string = '/') {
    await this.page.goto(`https://ecommercepracticeportal.netlify.app${path}`);
    await this.waitForPageLoad();
  }

  async waitForPageLoad() {
    await this.page.waitForLoadState('networkidle');
    await this.page.waitForLoadState('domcontentloaded');
  }

  async expectPageLoaded() {
    await expect(this.header).toBeVisible();
    await expect(this.navigation).toBeVisible();
  }

  async searchProduct(query: string) {
    await this.searchInput.fill(query);
    await this.searchButton.click();
    await this.page.waitForLoadState('networkidle');
  }

  async navigateToCategory(categoryName: string) {
    const categoryLink = this.page.locator(`a:has-text("${categoryName}")`);
    await categoryLink.click();
    await this.waitForPageLoad();
  }

  async openLoginModal() {
    await this.loginButton.click();
    await this.page.waitForSelector('[data-testid="login-modal"], .login-modal, form');
  }

  async openSignUpModal() {
    await this.signUpButton.click();
    await this.page.waitForSelector('[data-testid="signup-modal"], .signup-modal, form');
  }

  async openCart() {
    await this.cartIcon.click();
    await this.page.waitForLoadState('networkidle');
  }

  async getCartItemCount(): Promise<number> {
    const cartBadge = this.page.locator('[data-testid="cart-badge"], .cart-badge, .cart-count');
    if (await cartBadge.isVisible()) {
      const text = await cartBadge.textContent();
      return parseInt(text || '0', 10);
    }
    return 0;
  }

  async waitForElementStable(locator: Locator, timeout = 5000) {
    await locator.waitFor({ state: 'visible', timeout });
    await locator.waitFor({ state: 'stable', timeout });
  }

  async takeScreenshot(name: string) {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    await this.page.screenshot({ 
      path: `test-results/screenshots/vibium-${name}-${timestamp}.png`,
      fullPage: true 
    });
  }
}
