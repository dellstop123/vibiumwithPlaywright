import { Page, Locator, expect } from '@playwright/test';

export class HomePage {
  readonly page: Page;
  readonly header: Locator;
  readonly mainContent: Locator;
  readonly navigation: Locator;

  constructor(page: Page) {
    this.page = page;
    this.header = page.locator('header');
    this.mainContent = page.locator('main');
    this.navigation = page.locator('nav');
  }

  async goto() {
    await this.page.goto('/');
  }

  async expectPageLoaded() {
    await expect(this.page).toHaveTitle(/Vibium/);
    await expect(this.header).toBeVisible();
    await expect(this.mainContent).toBeVisible();
  }

  async getPageTitle(): Promise<string> {
    return await this.page.title();
  }

  async isNavigationVisible(): Promise<boolean> {
    return await this.navigation.isVisible();
  }
}
