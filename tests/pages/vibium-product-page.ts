import { Page, Locator, expect } from '@playwright/test';
import { VibiumBasePage } from './vibium-base-page';

export class VibiumProductPage extends VibiumBasePage {
  // Product page specific selectors
  readonly productGrid: Locator;
  readonly productItems: Locator;
  readonly productName: Locator;
  readonly productPrice: Locator;
  readonly productImage: Locator;
  readonly addToCartButton: Locator;
  readonly viewProductButton: Locator;
  readonly filterSection: Locator;
  readonly sortDropdown: Locator;
  readonly pagination: Locator;
  readonly productCount: Locator;

  constructor(page: Page) {
    super(page);
    
    // Initialize product page specific locators
    this.productGrid = page.locator('.product-grid, [data-testid="product-grid"], .products');
    this.productItems = page.locator('.product-item, [data-testid="product-item"], .product');
    this.productName = page.locator('.product-name, [data-testid="product-name"], .product h3');
    this.productPrice = page.locator('.product-price, [data-testid="product-price"], .price');
    this.productImage = page.locator('.product-image, [data-testid="product-image"], .product img');
    this.addToCartButton = page.locator('.add-to-cart, [data-testid="add-to-cart"], button:has-text("Add to Cart")');
    this.viewProductButton = page.locator('.view-product, [data-testid="view-product"], a:has-text("View")');
    this.filterSection = page.locator('.filters, [data-testid="filters"], .filter-section');
    this.sortDropdown = page.locator('select, [data-testid="sort-dropdown"], .sort-select');
    this.pagination = page.locator('.pagination, [data-testid="pagination"], .page-nav');
    this.productCount = page.locator('.product-count, [data-testid="product-count"], .results-count');
  }

  async gotoProducts() {
    await super.goto('/products');
  }

  async gotoCategory(categoryName: string) {
    await super.goto(`/categories/${categoryName.toLowerCase()}`);
  }

  async expectProductPageLoaded() {
    await super.expectPageLoaded();
    await expect(this.productGrid).toBeVisible();
  }

  async getProductCount(): Promise<number> {
    return await this.productItems.count();
  }

  async getProductNames(): Promise<string[]> {
    const count = await this.productItems.count();
    const names: string[] = [];
    
    for (let i = 0; i < count; i++) {
      const text = await this.productName.nth(i).textContent();
      if (text) names.push(text.trim());
    }
    
    return names;
  }

  async getProductPrices(): Promise<string[]> {
    const count = await this.productItems.count();
    const prices: string[] = [];
    
    for (let i = 0; i < count; i++) {
      const text = await this.productPrice.nth(i).textContent();
      if (text) prices.push(text.trim());
    }
    
    return prices;
  }

  async addProductToCart(productIndex: number = 0) {
    const addToCartBtn = this.addToCartButton.nth(productIndex);
    await addToCartBtn.click();
    await this.page.waitForLoadState('networkidle');
    
    // Wait for success message or cart update
    await this.page.waitForSelector('.success-message, .added-to-cart, [data-testid="success-message"]', { timeout: 5000 });
  }

  async viewProduct(productIndex: number = 0) {
    const viewBtn = this.viewProductButton.nth(productIndex);
    await viewBtn.click();
    await this.page.waitForLoadState('networkidle');
  }

  async filterByCategory(categoryName: string) {
    const categoryFilter = this.page.locator(`input[type="checkbox"][value="${categoryName}"], [data-testid="filter-${categoryName}"]`);
    await categoryFilter.check();
    await this.page.waitForLoadState('networkidle');
  }

  async sortProducts(sortOption: string) {
    if (await this.sortDropdown.isVisible()) {
      await this.sortDropdown.selectOption(sortOption);
      await this.page.waitForLoadState('networkidle');
    }
  }

  async setPriceRange(minPrice: number, maxPrice: number) {
    const minInput = this.page.locator('input[placeholder*="min"], input[name*="min"]');
    const maxInput = this.page.locator('input[placeholder*="max"], input[name*="max"]');
    
    if (await minInput.isVisible()) {
      await minInput.fill(minPrice.toString());
    }
    if (await maxInput.isVisible()) {
      await maxInput.fill(maxPrice.toString());
    }
    
    // Apply filter
    const applyButton = this.page.locator('button:has-text("Apply"), button:has-text("Filter")');
    if (await applyButton.isVisible()) {
      await applyButton.click();
      await this.page.waitForLoadState('networkidle');
    }
  }

  async searchProducts(query: string) {
    await super.searchProduct(query);
  }

  async verifyProductDisplay() {
    const productCount = await this.getProductCount();
    expect(productCount).toBeGreaterThan(0);
    
    // Verify product structure
    for (let i = 0; i < Math.min(productCount, 3); i++) {
      await expect(this.productName.nth(i)).toBeVisible();
      await expect(this.productPrice.nth(i)).toBeVisible();
      await expect(this.productImage.nth(i)).toBeVisible();
      await expect(this.addToCartButton.nth(i)).toBeVisible();
    }
  }

  async verifyProductDetails(productIndex: number = 0) {
    const productName = await this.productName.nth(productIndex).textContent();
    const productPrice = await this.productPrice.nth(productIndex).textContent();
    
    expect(productName).toBeTruthy();
    expect(productPrice).toBeTruthy();
    
    // Verify price format (should contain currency symbol)
    expect(productPrice).toMatch(/[\$€£¥]/);
  }

  async addMultipleProductsToCart(productIndices: number[]) {
    for (const index of productIndices) {
      await this.addProductToCart(index);
      await this.page.waitForTimeout(1000); // Wait between additions
    }
  }

  async verifyCartUpdate(expectedCount: number) {
    const actualCount = await super.getCartItemCount();
    expect(actualCount).toBe(expectedCount);
  }
}
