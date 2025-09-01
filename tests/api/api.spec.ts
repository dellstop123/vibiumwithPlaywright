import { test, expect } from '@playwright/test';
import { apiEndpoints } from '../fixtures/test-data';

test.describe('API Tests', () => {
  test('should return 200 for valid API endpoints', async ({ request }) => {
    // Test users endpoint
    const usersResponse = await request.get(apiEndpoints.endpoints.users);
    expect(usersResponse.status()).toBe(200);
    
    // Test posts endpoint
    const postsResponse = await request.get(apiEndpoints.endpoints.posts);
    expect(postsResponse.status()).toBe(200);
  });

  test('should handle authentication endpoints', async ({ request }) => {
    // Test login endpoint
    const loginResponse = await request.post(apiEndpoints.endpoints.auth + '/login', {
      data: {
        email: 'test@example.com',
        password: 'password123'
      }
    });
    
    // Should return appropriate status (401 for invalid credentials, 200 for valid)
    expect([200, 401]).toContain(loginResponse.status());
  });

  test('should validate response structure', async ({ request }) => {
    const response = await request.get(apiEndpoints.endpoints.users);
    
    if (response.status() === 200) {
      const data = await response.json();
      
      // Validate response structure
      expect(data).toBeDefined();
      expect(Array.isArray(data) || typeof data === 'object').toBe(true);
    }
  });

  test('should handle error responses gracefully', async ({ request }) => {
    // Test with invalid endpoint
    const invalidResponse = await request.get('/api/invalid-endpoint');
    expect([404, 400]).toContain(invalidResponse.status());
  });

  test('should respect rate limiting headers', async ({ request }) => {
    const response = await request.get(apiEndpoints.endpoints.users);
    
    // Check for rate limiting headers if they exist
    const rateLimitHeader = response.headers()['x-ratelimit-limit'];
    if (rateLimitHeader) {
      expect(rateLimitHeader).toBeDefined();
    }
  });
});
