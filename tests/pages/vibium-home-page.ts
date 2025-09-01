import { Page, Locator, expect } from '@playwright/test';
import { VibiumBasePage } from './vibium-base-page';

export class VibiumHomePage extends VibiumBasePage {
  // Homepage specific selectors
  readonly heroSection: Locator;
  readonly heroTitle: Locator;
  readonly heroSubtitle: Locator;
  readonly shopNowButton: Locator;
  readonly browseCategoriesButton: Locator;
  readonly categorySection: Locator;
  readonly featuredProductsSection: Locator;
  readonly newsletterSection: Locator;
  readonly newsletterInput: Locator;
  readonly subscribeButton: Locator;

  constructor(page: Page) {
    super(page);
    
    // Initialize homepage specific locators
    this.heroSection = page.locator('section:has-text("Discover Your Style")');
    this.heroTitle = page.locator('h1:has-text("Discover Your Style")');
    this.heroSubtitle = page.locator('p:has-text("Explore our latest collection")');
    this.shopNowButton = page.locator('a:has-text("Shop Now"), button:has-text("Shop Now")');
    this.browseCategoriesButton = page.locator('a:has-text("Browse Categories"), button:has-text("Browse Categories")');
    this.categorySection = page.locator('section:has-text("Shop by Category")');
    this.featuredProductsSection = page.locator('section:has-text("Featured Products")');
    this.newsletterSection = page.locator('section:has-text("Stay Updated")');
    this.newsletterInput = page.locator('input[placeholder*="email"], input[type="email"]');
    this.subscribeButton = page.locator('button:has-text("Subscribe")');
  }

  async goto() {
    await super.goto('/');
  }

  async expectHomePageLoaded() {
    await super.expectPageLoaded();
    await expect(this.heroSection).toBeVisible();
    await expect(this.heroTitle).toBeVisible();
    await expect(this.categorySection).toBeVisible();
    await expect(this.featuredProductsSection).toBeVisible();
  }

  async clickShopNow() {
    await this.shopNowButton.click();
    await this.page.waitForLoadState('networkidle');
  }

  async clickBrowseCategories() {
    await this.browseCategoriesButton.click();
    await this.page.waitForLoadState('networkidle');
  }

  async getCategoryCount(): Promise<number> {
    const categoryItems = this.page.locator('.category-item, [data-testid="category-item"], .category');
    return await categoryItems.count();
  }

  async getFeaturedProductCount(): Promise<number> {
    const productItems = this.page.locator('.product-item, [data-testid="product-item"], .product');
    return await productItems.count();
  }

  async subscribeToNewsletter(email: string) {
    await this.newsletterInput.fill(email);
    await this.subscribeButton.click();
    await this.page.waitForLoadState('networkidle');
  }

  async getCategoryNames(): Promise<string[]> {
    const categoryElements = this.page.locator('.category-name, [data-testid="category-name"], .category h3');
    const count = await categoryElements.count();
    const names: string[] = [];
    
    for (let i = 0; i < count; i++) {
      const text = await categoryElements.nth(i).textContent();
      if (text) names.push(text.trim());
    }
    
    return names;
  }

  async getFeaturedProductNames(): Promise<string[]> {
    const productElements = this.page.locator('.product-name, [data-testid="product-name"], .product h3');
    const count = await productElements.count();
    const names: string[] = [];
    
    for (let i = 0; i < count; i++) {
      const text = await productElements.nth(i).textContent();
      if (text) names.push(text.trim());
    }
    
    return names;
  }

  async scrollToSection(sectionName: string) {
    const section = this.page.locator(`section:has-text("${sectionName}")`);
    await section.scrollIntoViewIfNeeded();
    await this.page.waitForTimeout(500); // Wait for scroll animation
  }

  async verifyHeroSectionContent() {
    await expect(this.heroTitle).toContainText('Discover Your Style');
    await expect(this.heroSubtitle).toContainText('Explore our latest collection');
    await expect(this.shopNowButton).toBeVisible();
    await expect(this.browseCategoriesButton).toBeVisible();
  }

  async verifyCategorySection() {
    await expect(this.categorySection).toBeVisible();
    const categoryCount = await this.getCategoryCount();
    expect(categoryCount).toBeGreaterThan(0);
    
    // Verify specific categories exist
    const categoryNames = await this.getCategoryNames();
    expect(categoryNames).toContain('Men');
    expect(categoryNames).toContain('Women');
  }

  async verifyFeaturedProductsSection() {
    await expect(this.featuredProductsSection).toBeVisible();
    const productCount = await this.getFeaturedProductCount();
    expect(productCount).toBeGreaterThan(0);
  }
}
