import { Page, Locator, expect } from '@playwright/test';
import { VibiumBasePage } from './vibium-base-page';

export class VibiumAuthPage extends VibiumBasePage {
  // Authentication page specific selectors
  readonly loginForm: Locator;
  readonly signupForm: Locator;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly confirmPasswordInput: Locator;
  readonly firstNameInput: Locator;
  readonly lastNameInput: Locator;
  readonly loginButton: Locator;
  readonly signupButton: Locator;
  readonly forgotPasswordLink: Locator;
  readonly switchToSignupLink: Locator;
  readonly switchToLoginLink: Locator;
  readonly errorMessage: Locator;
  readonly successMessage: Locator;
  readonly rememberMeCheckbox: Locator;
  readonly termsCheckbox: Locator;

  constructor(page: Page) {
    super(page);
    
    // Initialize authentication page specific locators
    this.loginForm = page.locator('.login-form, [data-testid="login-form"], form:has-text("Login")');
    this.signupForm = page.locator('.signup-form, [data-testid="signup-form"], form:has-text("Sign Up")');
    this.emailInput = page.locator('input[type="email"], input[name="email"], input[placeholder*="email"]');
    this.passwordInput = page.locator('input[type="password"], input[name="password"], input[placeholder*="password"]');
    this.confirmPasswordInput = page.locator('input[name="confirmPassword"], input[placeholder*="confirm"], input[placeholder*="confirm password"]');
    this.firstNameInput = page.locator('input[name="firstName"], input[placeholder*="first name"], input[placeholder*="first"]');
    this.lastNameInput = page.locator('input[name="lastName"], input[placeholder*="last name"], input[placeholder*="last"]');
    this.loginButton = page.locator('button[type="submit"]:has-text("Login"), button:has-text("Sign In")');
    this.signupButton = page.locator('button[type="submit"]:has-text("Sign Up"), button:has-text("Create Account")');
    this.forgotPasswordLink = page.locator('a:has-text("Forgot Password"), a:has-text("Forgot?")');
    this.switchToSignupLink = page.locator('a:has-text("Sign Up"), a:has-text("Create Account")');
    this.switchToLoginLink = page.locator('a:has-text("Login"), a:has-text("Sign In")');
    this.errorMessage = page.locator('.error-message, [data-testid="error-message"], .alert-error');
    this.successMessage = page.locator('.success-message, [data-testid="success-message"], .alert-success');
    this.rememberMeCheckbox = page.locator('input[type="checkbox"][name="remember"], input[type="checkbox"]:has-text("Remember me")');
    this.termsCheckbox = page.locator('input[type="checkbox"][name="terms"], input[type="checkbox"]:has-text("I agree")');
  }

  async gotoLogin() {
    await super.goto('/login');
  }

  async gotoSignup() {
    await super.goto('/signup');
  }

  async expectLoginFormLoaded() {
    await super.expectPageLoaded();
    await expect(this.loginForm).toBeVisible();
    await expect(this.emailInput).toBeVisible();
    await expect(this.passwordInput).toBeVisible();
    await expect(this.loginButton).toBeVisible();
  }

  async expectSignupFormLoaded() {
    await super.expectPageLoaded();
    await expect(this.signupForm).toBeVisible();
    await expect(this.emailInput).toBeVisible();
    await expect(this.passwordInput).toBeVisible();
    await expect(this.confirmPasswordInput).toBeVisible();
    await expect(this.signupButton).toBeVisible();
  }

  async login(email: string, password: string, rememberMe: boolean = false) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    
    if (rememberMe && await this.rememberMeCheckbox.isVisible()) {
      await this.rememberMeCheckbox.check();
    }
    
    await this.loginButton.click();
    await this.page.waitForLoadState('networkidle');
  }

  async signup(userData: {
    firstName: string;
    lastName: string;
    email: string;
    password: string;
    confirmPassword: string;
    agreeToTerms: boolean;
  }) {
    await this.firstNameInput.fill(userData.firstName);
    await this.lastNameInput.fill(userData.lastName);
    await this.emailInput.fill(userData.email);
    await this.passwordInput.fill(userData.password);
    await this.confirmPasswordInput.fill(userData.confirmPassword);
    
    if (userData.agreeToTerms && await this.termsCheckbox.isVisible()) {
      await this.termsCheckbox.check();
    }
    
    await this.signupButton.click();
    await this.page.waitForLoadState('networkidle');
  }

  async switchToSignup() {
    await this.switchToSignupLink.click();
    await this.page.waitForLoadState('networkidle');
    await this.expectSignupFormLoaded();
  }

  async switchToLogin() {
    await this.switchToLoginLink.click();
    await this.page.waitForLoadState('networkidle');
    await this.expectLoginFormLoaded();
  }

  async forgotPassword(email: string) {
    await this.forgotPasswordLink.click();
    await this.page.waitForLoadState('networkidle');
    
    // Fill email for password reset
    const resetEmailInput = this.page.locator('input[type="email"], input[name="email"]');
    await resetEmailInput.fill(email);
    
    const resetButton = this.page.locator('button:has-text("Reset Password"), button:has-text("Send Reset Link")');
    await resetButton.click();
    await this.page.waitForLoadState('networkidle');
  }

  async verifyLoginSuccess() {
    // Check for success message or redirect to dashboard
    const hasSuccessMessage = await this.successMessage.isVisible();
    const isOnDashboard = this.page.url().includes('/dashboard') || this.page.url().includes('/account');
    
    expect(hasSuccessMessage || isOnDashboard).toBe(true);
  }

  async verifySignupSuccess() {
    // Check for success message or redirect to login
    const hasSuccessMessage = await this.successMessage.isVisible();
    const isOnLogin = this.page.url().includes('/login');
    
    expect(hasSuccessMessage || isOnLogin).toBe(true);
  }

  async verifyErrorMessage(expectedMessage?: string) {
    await expect(this.errorMessage).toBeVisible();
    
    if (expectedMessage) {
      const actualMessage = await this.errorMessage.textContent();
      expect(actualMessage).toContain(expectedMessage);
    }
  }

  async verifyFormValidation() {
    // Try to submit empty form
    await this.loginButton.click();
    
    // Should show validation errors
    await expect(this.errorMessage).toBeVisible();
  }

  async verifyPasswordStrength(password: string) {
    await this.passwordInput.fill(password);
    
    // Look for password strength indicator
    const strengthIndicator = this.page.locator('.password-strength, [data-testid="password-strength"], .strength-meter');
    
    if (await strengthIndicator.isVisible()) {
      const strength = await strengthIndicator.textContent();
      expect(strength).toBeTruthy();
    }
  }

  async verifyEmailFormat(email: string) {
    await this.emailInput.fill(email);
    await this.emailInput.blur();
    
    // Wait for validation
    await this.page.waitForTimeout(500);
    
    // Check for email format error
    const emailError = this.page.locator('.email-error, [data-testid="email-error"]');
    if (await emailError.isVisible()) {
      const errorText = await emailError.textContent();
      expect(errorText).toContain('valid email');
    }
  }

  async logout() {
    // Look for logout button in user menu
    const userMenu = this.page.locator('.user-menu, [data-testid="user-menu"], .profile-menu');
    if (await userMenu.isVisible()) {
      await userMenu.click();
      
      const logoutButton = this.page.locator('a:has-text("Logout"), button:has-text("Logout")');
      if (await logoutButton.isVisible()) {
        await logoutButton.click();
        await this.page.waitForLoadState('networkidle');
      }
    }
  }

  async isLoggedIn(): Promise<boolean> {
    // Check if user is logged in by looking for user-specific elements
    const userMenu = this.page.locator('.user-menu, [data-testid="user-menu"], .profile-menu');
    const loginButton = this.page.locator('a:has-text("Login")');
    
    return await userMenu.isVisible() && !(await loginButton.isVisible());
  }
}
