# Vibium Playwright Test Suite

A comprehensive Playwright test automation project for the **Vibium E-commerce Platform** at [https://ecommercepracticeportal.netlify.app/](https://ecommercepracticeportal.netlify.app/).

> **📖 For detailed Vibium-specific documentation, see [VIBIUM_README.md](./VIBIUM_README.md)**

## 🚀 Features

- **Cross-browser testing** - Chrome, Firefox, Safari, and mobile browsers
- **Page Object Model** - Organized and maintainable test structure
- **Visual regression testing** - Screenshot comparison across viewports
- **Performance testing** - Core Web Vitals and load time measurements
- **API testing** - REST API endpoint validation
- **E2E testing** - Complete user journey testing
- **Test utilities** - Helper functions and common test operations

## 📁 Project Structure

```
vibium-playwright/
├── tests/
│   ├── e2e/              # End-to-end test scenarios
│   ├── api/              # API endpoint tests
│   ├── visual/           # Visual regression tests
│   ├── performance/      # Performance and metrics tests
│   ├── pages/            # Page Object Model classes
│   ├── utils/            # Test utility functions
│   ├── fixtures/         # Test data and selectors
│   └── example.spec.ts   # Example test file
├── playwright.config.ts  # Playwright configuration
├── package.json          # Dependencies and scripts
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## 🛠️ Setup

### Prerequisites

- Node.js 16+ 
- npm or yarn

### Installation

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Install Playwright browsers:**
   ```bash
   npm run test:install
   ```

3. **Install system dependencies (macOS/Linux):**
   ```bash
   npm run test:install-deps
   ```

## 🧪 Running Tests

### Basic Commands

```bash
# Run all tests
npm test

# Run tests in headed mode (visible browser)
npm run test:headed

# Run tests with UI mode
npm run test:ui

# Run tests in debug mode
npm run test:debug

# Generate tests from user actions
npm run test:codegen
```

### Specific Test Categories

```bash
# Run only E2E tests
npx playwright test tests/e2e/

# Run only API tests
npx playwright test tests/api/

# Run only visual tests
npx playwright test tests/visual/

# Run only performance tests
npx playwright test tests/performance/
```

### Browser-Specific Testing

```bash
# Run tests only in Chrome
npx playwright test --project=chromium

# Run tests only in Firefox
npx playwright test --project=firefox

# Run tests only in Safari
npx playwright test --project=webkit

# Run tests only on mobile
npx playwright test --project="Mobile Chrome"
```

## 📊 Test Reports

### HTML Report
```bash
npm run test:html
```
View detailed test results in your browser.

### JSON Report
```bash
npx playwright test --reporter=json
```
Generate JSON report for CI/CD integration.

### JUnit Report
```bash
npx playwright test --reporter=junit
```
Generate JUnit XML report for CI/CD systems.

## 🔧 Configuration

### Playwright Config (`playwright.config.ts`)

- **Base URL**: Configured for `http://localhost:3000`
- **Browsers**: Chrome, Firefox, Safari, and mobile devices
- **Parallel execution**: Enabled for faster test runs
- **Retries**: 2 retries on CI, 0 locally
- **Screenshots**: Captured on test failure
- **Videos**: Recorded on test failure
- **Traces**: Collected on first retry

### Environment Variables

Create a `.env` file for environment-specific configurations:

```env
BASE_URL=http://localhost:3000
API_BASE_URL=http://localhost:3000/api
TEST_USER_EMAIL=test@example.com
TEST_USER_PASSWORD=password123
```

## 📝 Writing Tests

### Page Object Model

```typescript
import { Page, Locator, expect } from '@playwright/test';

export class HomePage {
  readonly page: Page;
  readonly header: Locator;
  
  constructor(page: Page) {
    this.page = page;
    this.header = page.locator('header');
  }
  
  async goto() {
    await this.page.goto('/');
  }
  
  async expectPageLoaded() {
    await expect(this.header).toBeVisible();
  }
}
```

### Test Structure

```typescript
import { test, expect } from '@playwright/test';
import { HomePage } from '../pages/home-page';

test.describe('Home Page Tests', () => {
  let homePage: HomePage;
  
  test.beforeEach(async ({ page }) => {
    homePage = new HomePage(page);
    await homePage.goto();
  });
  
  test('should display header', async ({ page }) => {
    await homePage.expectPageLoaded();
  });
});
```

## 🎯 Best Practices

1. **Use Page Object Model** - Keep tests maintainable and reusable
2. **Data-driven testing** - Use fixtures for test data
3. **Meaningful assertions** - Test behavior, not implementation
4. **Proper waiting** - Use built-in waiting mechanisms
5. **Test isolation** - Each test should be independent
6. **Descriptive names** - Use clear test and describe names

## 🚨 Troubleshooting

### Common Issues

1. **Browser installation failed**
   ```bash
   npm run test:install-deps
   ```

2. **Tests failing on CI**
   - Check browser installation
   - Verify system dependencies
   - Review CI environment setup

3. **Screenshot comparison failures**
   - Update baseline screenshots: `npx playwright test --update-snapshots`
   - Check viewport sizes match

4. **Performance test failures**
   - Verify network conditions
   - Check performance budgets in config

## 📚 Resources

- [Playwright Documentation](https://playwright.dev/)
- [Playwright Test API](https://playwright.dev/docs/api/class-test)
- [Page Object Model](https://playwright.dev/docs/pom)
- [Visual Testing](https://playwright.dev/docs/screenshots)
- [API Testing](https://playwright.dev/docs/api-testing)

## 🤝 Contributing

1. Follow the existing test structure
2. Use Page Object Model for new pages
3. Add appropriate test data to fixtures
4. Update documentation as needed
5. Ensure all tests pass before submitting

## 📄 License

MIT License - see LICENSE file for details.
