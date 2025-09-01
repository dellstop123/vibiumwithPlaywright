export const testData = {
  users: {
    validUser: {
      email: 'test@example.com',
      password: 'TestPassword123!',
      name: 'Test User'
    },
    invalidUser: {
      email: 'invalid@example.com',
      password: 'wrongpassword',
      name: 'Invalid User'
    }
  },
  
  forms: {
    contactForm: {
      name: 'John Doe',
      email: 'john.doe@example.com',
      message: 'This is a test message for contact form testing.'
    },
    
    registrationForm: {
      firstName: 'Jane',
      lastName: 'Smith',
      email: 'jane.smith@example.com',
      password: 'SecurePass123!',
      confirmPassword: 'SecurePass123!'
    }
  },
  
  search: {
    validSearch: 'vibium',
    invalidSearch: 'xyz123nonexistent',
    specialCharacters: '!@#$%^&*()'
  },
  
  navigation: {
    menuItems: ['Home', 'About', 'Services', 'Contact'],
    footerLinks: ['Privacy Policy', 'Terms of Service', 'FAQ']
  }
};

export const apiEndpoints = {
  baseUrl: 'http://localhost:3000',
  endpoints: {
    users: '/api/users',
    auth: '/api/auth',
    posts: '/api/posts'
  }
};

export const selectors = {
  common: {
    header: 'header',
    footer: 'footer',
    navigation: 'nav',
    mainContent: 'main',
    loadingSpinner: '[data-testid="loading-spinner"]',
    errorMessage: '[data-testid="error-message"]',
    successMessage: '[data-testid="success-message"]'
  },
  
  forms: {
    submitButton: 'button[type="submit"]',
    inputField: 'input',
    textarea: 'textarea',
    select: 'select'
  },
  
  navigation: {
    menuToggle: '[data-testid="menu-toggle"]',
    menuItems: '[data-testid="menu-item"]',
    breadcrumb: '[data-testid="breadcrumb"]'
  }
};
