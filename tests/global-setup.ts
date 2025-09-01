import { chromium, FullConfig } from '@playwright/test';

async function globalSetup(config: FullConfig) {
  const { baseURL, storageState } = config.projects[0].use;
  
  // Skip if no storage state is configured
  if (!storageState) return;
  
  // Launch browser and create authenticated state
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  try {
    // Navigate to the application
    await page.goto(baseURL || 'http://localhost:3000');
    
    // Wait for page to load
    await page.waitForLoadState('networkidle');
    
    // Perform any authentication or setup steps here
    // For example, login with test credentials
    // await page.fill('[data-testid="email"]', 'test@example.com');
    // await page.fill('[data-testid="password"]', 'password123');
    // await page.click('[data-testid="login-button"]');
    // await page.waitForURL('**/dashboard');
    
    // Save signed-in state
    await page.context().storageState({ path: storageState as string });
    
    console.log('Global setup completed successfully');
  } catch (error) {
    console.error('Global setup failed:', error);
    throw error;
  } finally {
    await browser.close();
  }
}

export default globalSetup;
