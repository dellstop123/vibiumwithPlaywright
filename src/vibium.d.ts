import { Page, TestInfo } from '@playwright/test';

export interface CheckoutUserData {
  firstName: string;
  lastName: string;
  email: string;
  address: string;
  city: string;
  zipCode: string;
  cardNumber: string;
  expiryDate: string;
  cvv: string;
}

export interface CoreWebVitals {
  lcp: number;
}

export interface GeneratedUserData {
  firstName: string;
  lastName: string;
  email: string;
  password: string;
}

export class Vibium {
  constructor(page: Page, testInfo: TestInfo);
  
  ecommerce: {
    addToCart(productSelector: string, expectedCartCount?: number): Promise<boolean>;
    getCartItemCount(): Promise<number>;
    searchProducts(query: string): Promise<void>;
    navigateToCategory(categoryName: string): Promise<void>;
    subscribeToNewsletter(email: string): Promise<void>;
    checkout(userData: CheckoutUserData): Promise<void>;
  };
  
  forms: {
    fillForm(formData: Record<string, string>): Promise<void>;
    submitForm(submitButtonText?: string): Promise<void>;
    validateFormErrors(expectedErrors: string[]): Promise<void>;
  };
  
  navigation: {
    goto(url: string, expectedTitle?: string): Promise<void>;
    clickNavItem(itemText: string): Promise<void>;
    verifyPage(expectedUrl: string, expectedTitle?: string): Promise<void>;
  };
  
  elements: {
    waitForStable(selector: string, timeout?: number): Promise<void>;
    clickWithRetry(selector: string, maxAttempts?: number): Promise<void>;
    fillInput(selector: string, value: string, validate?: boolean): Promise<void>;
  };
  
  assertions: {
    containsText(selector: string, expectedText: string): Promise<void>;
    isVisible(selector: string): Promise<void>;
    hasCount(selector: string, expectedCount: number): Promise<void>;
    urlContains(expectedUrl: string): Promise<void>;
  };
  
  performance: {
    measureLoadTime(): Promise<number>;
    checkCoreWebVitals(): Promise<CoreWebVitals>;
  };
  
  screenshots: {
    capture(name: string): Promise<string>;
    captureOnFailure(name: string): Promise<void>;
  };
  
  data: {
    generateEmail(prefix?: string): string;
    generateString(length?: number): string;
    generateUserData(): GeneratedUserData;
  };
  
  wait: {
    forNetworkIdle(): Promise<void>;
    forDOMContentLoaded(): Promise<void>;
    forTimeout(ms: number): Promise<void>;
  };
}

export function createVibium(page: Page, testInfo: TestInfo): Vibium;

export default Vibium;
