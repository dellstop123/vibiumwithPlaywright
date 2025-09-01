import { Page, Locator, expect } from '@playwright/test';
import { VibiumBasePage } from './vibium-base-page';

export class VibiumCartPage extends VibiumBasePage {
  // Cart page specific selectors
  readonly cartItems: Locator;
  readonly cartItemName: Locator;
  readonly cartItemPrice: Locator;
  readonly cartItemQuantity: Locator;
  readonly cartItemImage: Locator;
  readonly removeButton: Locator;
  readonly updateQuantityInput: Locator;
  readonly updateQuantityButton: Locator;
  readonly subtotal: Locator;
  readonly tax: Locator;
  readonly shipping: Locator;
  readonly total: Locator;
  readonly checkoutButton: Locator;
  readonly continueShoppingButton: Locator;
  readonly emptyCartMessage: Locator;
  readonly cartSummary: Locator;

  constructor(page: Page) {
    super(page);
    
    // Initialize cart page specific locators
    this.cartItems = page.locator('.cart-item, [data-testid="cart-item"], .item');
    this.cartItemName = page.locator('.cart-item-name, [data-testid="cart-item-name"], .item-name');
    this.cartItemPrice = page.locator('.cart-item-price, [data-testid="cart-item-price"], .item-price');
    this.cartItemQuantity = page.locator('.cart-item-quantity, [data-testid="cart-item-quantity"], .item-quantity');
    this.cartItemImage = page.locator('.cart-item-image, [data-testid="cart-item-image"], .item-image');
    this.removeButton = page.locator('.remove-item, [data-testid="remove-item"], button:has-text("Remove")');
    this.updateQuantityInput = page.locator('input[type="number"], [data-testid="quantity-input"], .quantity-input');
    this.updateQuantityButton = page.locator('.update-quantity, [data-testid="update-quantity"], button:has-text("Update")');
    this.subtotal = page.locator('.subtotal, [data-testid="subtotal"], .cart-subtotal');
    this.tax = page.locator('.tax, [data-testid="tax"], .cart-tax');
    this.shipping = page.locator('.shipping, [data-testid="shipping"], .cart-shipping');
    this.total = page.locator('.total, [data-testid="total"], .cart-total');
    this.checkoutButton = page.locator('.checkout, [data-testid="checkout"], button:has-text("Checkout")');
    this.continueShoppingButton = page.locator('.continue-shopping, [data-testid="continue-shopping"], a:has-text("Continue Shopping")');
    this.emptyCartMessage = page.locator('.empty-cart, [data-testid="empty-cart"], .cart-empty');
    this.cartSummary = page.locator('.cart-summary, [data-testid="cart-summary"], .summary');
  }

  async gotoCart() {
    await super.goto('/cart');
  }

  async expectCartPageLoaded() {
    await super.expectPageLoaded();
    // Cart page might be empty, so we check for either cart items or empty message
    const hasItems = await this.cartItems.count() > 0;
    const hasEmptyMessage = await this.emptyCartMessage.isVisible();
    
    if (!hasItems && !hasEmptyMessage) {
      throw new Error('Cart page not properly loaded');
    }
  }

  async getCartItemCount(): Promise<number> {
    return await this.cartItems.count();
  }

  async getCartItemNames(): Promise<string[]> {
    const count = await this.cartItems.count();
    const names: string[] = [];
    
    for (let i = 0; i < count; i++) {
      const text = await this.cartItemName.nth(i).textContent();
      if (text) names.push(text.trim());
    }
    
    return names;
  }

  async getCartItemPrices(): Promise<string[]> {
    const count = await this.cartItems.count();
    const prices: string[] = [];
    
    for (let i = 0; i < count; i++) {
      const text = await this.cartItemPrice.nth(i).textContent();
      if (text) prices.push(text.trim());
    }
    
    return prices;
  }

  async getCartItemQuantities(): Promise<number[]> {
    const count = await this.cartItems.count();
    const quantities: number[] = [];
    
    for (let i = 0; i < count; i++) {
      const text = await this.cartItemQuantity.nth(i).textContent();
      if (text) {
        const quantity = parseInt(text.trim(), 10);
        quantities.push(isNaN(quantity) ? 1 : quantity);
      } else {
        quantities.push(1);
      }
    }
    
    return quantities;
  }

  async updateItemQuantity(itemIndex: number, newQuantity: number) {
    const quantityInput = this.updateQuantityInput.nth(itemIndex);
    const updateButton = this.updateQuantityButton.nth(itemIndex);
    
    await quantityInput.fill(newQuantity.toString());
    await updateButton.click();
    await this.page.waitForLoadState('networkidle');
  }

  async removeItem(itemIndex: number) {
    const removeBtn = this.removeButton.nth(itemIndex);
    await removeBtn.click();
    await this.page.waitForLoadState('networkidle');
  }

  async removeAllItems() {
    const itemCount = await this.getCartItemCount();
    for (let i = itemCount - 1; i >= 0; i--) {
      await this.removeItem(i);
      await this.page.waitForTimeout(1000); // Wait between removals
    }
  }

  async getSubtotal(): Promise<string> {
    const text = await this.subtotal.textContent();
    return text ? text.trim() : '';
  }

  async getTax(): Promise<string> {
    const text = await this.tax.textContent();
    return text ? text.trim() : '';
  }

  async getShipping(): Promise<string> {
    const text = await this.shipping.textContent();
    return text ? text.trim() : '';
  }

  async getTotal(): Promise<string> {
    const text = await this.total.textContent();
    return text ? text.trim() : '';
  }

  async proceedToCheckout() {
    await this.checkoutButton.click();
    await this.page.waitForLoadState('networkidle');
  }

  async continueShopping() {
    await this.continueShoppingButton.click();
    await this.page.waitForLoadState('networkidle');
  }

  async verifyCartItemDetails(itemIndex: number = 0) {
    await expect(this.cartItemName.nth(itemIndex)).toBeVisible();
    await expect(this.cartItemPrice.nth(itemIndex)).toBeVisible();
    await expect(this.cartItemQuantity.nth(itemIndex)).toBeVisible();
    await expect(this.cartItemImage.nth(itemIndex)).toBeVisible();
    await expect(this.removeButton.nth(itemIndex)).toBeVisible();
  }

  async verifyCartSummary() {
    if (await this.cartSummary.isVisible()) {
      await expect(this.subtotal).toBeVisible();
      await expect(this.total).toBeVisible();
      
      // Verify total calculation
      const subtotalText = await this.getSubtotal();
      const totalText = await this.getTotal();
      
      expect(subtotalText).toBeTruthy();
      expect(totalText).toBeTruthy();
    }
  }

  async verifyEmptyCart() {
    await expect(this.emptyCartMessage).toBeVisible();
    await expect(this.continueShoppingButton).toBeVisible();
    
    const itemCount = await this.getCartItemCount();
    expect(itemCount).toBe(0);
  }

  async calculateExpectedTotal(): Promise<number> {
    const prices = await this.getCartItemPrices();
    const quantities = await this.getCartItemQuantities();
    
    let total = 0;
    for (let i = 0; i < prices.length; i++) {
      const price = parseFloat(prices[i].replace(/[^\d.]/g, ''));
      const quantity = quantities[i];
      total += price * quantity;
    }
    
    return total;
  }

  async verifyTotalCalculation() {
    const expectedTotal = await this.calculateExpectedTotal();
    const actualTotalText = await this.getTotal();
    const actualTotal = parseFloat(actualTotalText.replace(/[^\d.]/g, ''));
    
    expect(actualTotal).toBeCloseTo(expectedTotal, 2);
  }
}
