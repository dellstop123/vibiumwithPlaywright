export const vibiumTestData = {
  // User credentials for testing
  users: {
    validUser: {
      email: 'test@vibium.com',
      password: 'TestPassword123!',
      firstName: 'Test',
      lastName: 'User'
    },
    invalidUser: {
      email: 'invalid@vibium.com',
      password: 'wrongpassword',
      firstName: 'Invalid',
      lastName: 'User'
    },
    newUser: {
      firstName: 'John',
      lastName: 'Doe',
      email: 'john.doe@vibium.com',
      password: 'SecurePass123!',
      confirmPassword: 'SecurePass123!'
    }
  },

  // Product data
  products: {
    classicWhiteTshirt: {
      name: 'Classic White T-Shirt',
      category: 'Men',
      brand: 'Nike',
      price: '$29.99',
      originalPrice: '$39.99',
      rating: '4.5'
    },
    floralSummerDress: {
      name: 'Floral Summer Dress',
      category: 'Women',
      brand: 'Zara',
      price: '$89.99',
      originalPrice: '$119.99',
      rating: '4.8'
    },
    slimFitJeans: {
      name: 'Slim Fit Jeans',
      category: 'Men',
      brand: 'Levi\'s',
      price: '$79.99',
      originalPrice: '$99.99',
      rating: '4.6'
    },
    leatherCrossbodyBag: {
      name: 'Leather Crossbody Bag',
      category: 'Accessories',
      brand: 'Coach',
      price: '$129.99',
      originalPrice: '$159.99',
      rating: '4.7'
    }
  },

  // Category data
  categories: {
    men: {
      name: 'Men',
      productCount: 3,
      path: '/categories/men'
    },
    women: {
      name: 'Women',
      productCount: 3,
      path: '/categories/women'
    },
    footwear: {
      name: 'Footwear',
      productCount: 1,
      path: '/categories/footwear'
    },
    accessories: {
      name: 'Accessories',
      productCount: 1,
      path: '/categories/accessories'
    }
  },

  // Search queries
  search: {
    validQueries: ['shirt', 'dress', 'jeans', 'bag', 'nike', 'zara'],
    invalidQueries: ['xyz123nonexistent', '!@#$%^&*()'],
    categorySpecific: {
      men: ['shirt', 'jeans', 't-shirt'],
      women: ['dress', 'summer', 'floral'],
      accessories: ['bag', 'leather', 'crossbody']
    }
  },

  // Newsletter data
  newsletter: {
    validEmails: [
      'test@vibium.com',
      'user@example.com',
      'newsletter@test.org'
    ],
    invalidEmails: [
      'invalid-email',
      'test@',
      '@vibium.com',
      'test.vibium.com'
    ]
  },

  // Cart scenarios
  cart: {
    singleItem: [0],
    multipleItems: [0, 1, 2],
    allItems: [0, 1, 2, 3],
    quantities: [1, 2, 3, 5]
  },

  // Form validation data
  forms: {
    login: {
      validCredentials: {
        email: 'test@vibium.com',
        password: 'TestPassword123!'
      },
      invalidCredentials: [
        { email: '', password: 'password' },
        { email: 'test@vibium.com', password: '' },
        { email: 'invalid-email', password: 'password' },
        { email: 'test@vibium.com', password: '123' }
      ]
    },
    signup: {
      validData: {
        firstName: 'Jane',
        lastName: 'Smith',
        email: 'jane.smith@vibium.com',
        password: 'SecurePass123!',
        confirmPassword: 'SecurePass123!',
        agreeToTerms: true
      },
      invalidData: [
        { firstName: '', lastName: 'Smith', email: 'jane@vibium.com', password: 'pass', confirmPassword: 'pass' },
        { firstName: 'Jane', lastName: '', email: 'jane@vibium.com', password: 'pass', confirmPassword: 'pass' },
        { firstName: 'Jane', lastName: 'Smith', email: '', password: 'pass', confirmPassword: 'pass' },
        { firstName: 'Jane', lastName: 'Smith', email: 'jane@vibium.com', password: '', confirmPassword: '' },
        { firstName: 'Jane', lastName: 'Smith', email: 'jane@vibium.com', password: 'pass', confirmPassword: 'different' }
      ]
    }
  },

  // Navigation data
  navigation: {
    mainMenu: ['Home', 'Products', 'Categories', 'About', 'Contact'],
    footerLinks: ['Privacy Policy', 'Terms of Service', 'Shipping Info'],
    quickLinks: ['Home', 'Products', 'Categories', 'Cart']
  },

  // Expected content
  content: {
    hero: {
      title: 'Discover Your Style',
      subtitle: 'Explore our latest collection of trendy fashion items. From casual wear to formal attire, we have everything you need to express your unique style.'
    },
    features: [
      'Free Shipping',
      'Quality Guarantee',
      '24/7 Support',
      'Secure Payment'
    ],
    newsletter: {
      title: 'Stay Updated',
      subtitle: 'Subscribe to our newsletter for the latest fashion trends and exclusive offers.'
    }
  },

  // API endpoints
  api: {
    baseUrl: 'https://ecommercepracticeportal.netlify.app',
    endpoints: {
      products: '/api/products',
      categories: '/api/categories',
      auth: '/api/auth',
      cart: '/api/cart',
      orders: '/api/orders'
    }
  },

  // Test scenarios
  scenarios: {
    e2e: {
      browseAndPurchase: {
        description: 'Complete user journey from browsing to purchase',
        steps: ['browse_categories', 'view_products', 'add_to_cart', 'checkout']
      },
      userRegistration: {
        description: 'New user registration and first purchase',
        steps: ['signup', 'login', 'browse', 'purchase']
      },
      searchAndFilter: {
        description: 'Product search and filtering functionality',
        steps: ['search_products', 'apply_filters', 'sort_results', 'view_filtered']
      }
    }
  }
};

export const vibiumSelectors = {
  // Common selectors
  common: {
    header: 'header',
    footer: 'footer',
    navigation: 'nav',
    mainContent: 'main',
    loadingSpinner: '[data-testid="loading-spinner"], .loading, .spinner',
    errorMessage: '[data-testid="error-message"], .error-message, .alert-error',
    successMessage: '[data-testid="success-message"], .success-message, .alert-success'
  },

  // Product selectors
  products: {
    grid: '.product-grid, [data-testid="product-grid"], .products',
    item: '.product-item, [data-testid="product-item"], .product',
    name: '.product-name, [data-testid="product-name"], .product h3',
    price: '.product-price, [data-testid="product-price"], .price',
    image: '.product-image, [data-testid="product-image"], .product img',
    addToCart: '.add-to-cart, [data-testid="add-to-cart"], button:has-text("Add to Cart")',
    viewProduct: '.view-product, [data-testid="view-product"], a:has-text("View")',
    rating: '.product-rating, [data-testid="product-rating"], .rating',
    brand: '.product-brand, [data-testid="product-brand"], .brand'
  },

  // Category selectors
  categories: {
    section: '.category-section, [data-testid="category-section"], section:has-text("Shop by Category")',
    item: '.category-item, [data-testid="category-item"], .category',
    name: '.category-name, [data-testid="category-name"], .category h3',
    count: '.category-count, [data-testid="category-count"], .count',
    link: '.category-link, [data-testid="category-link"], .category a'
  },

  // Cart selectors
  cart: {
    icon: '[data-testid="cart-icon"], .cart-icon, a:has-text("Cart")',
    badge: '[data-testid="cart-badge"], .cart-badge, .cart-count',
    items: '.cart-item, [data-testid="cart-item"], .item',
    itemName: '.cart-item-name, [data-testid="cart-item-name"], .item-name',
    itemPrice: '.cart-item-price, [data-testid="cart-item-price"], .item-price',
    itemQuantity: '.cart-item-quantity, [data-testid="cart-item-quantity"], .item-quantity',
    removeButton: '.remove-item, [data-testid="remove-item"], button:has-text("Remove")',
    subtotal: '.subtotal, [data-testid="subtotal"], .cart-subtotal',
    total: '.total, [data-testid="total"], .cart-total',
    checkout: '.checkout, [data-testid="checkout"], button:has-text("Checkout")'
  },

  // Form selectors
  forms: {
    input: 'input',
    textarea: 'textarea',
    select: 'select',
    checkbox: 'input[type="checkbox"]',
    radio: 'input[type="radio"]',
    submit: 'button[type="submit"]',
    button: 'button'
  },

  // Authentication selectors
  auth: {
    loginForm: '.login-form, [data-testid="login-form"], form:has-text("Login")',
    signupForm: '.signup-form, [data-testid="signup-form"], form:has-text("Sign Up")',
    emailInput: 'input[type="email"], input[name="email"], input[placeholder*="email"]',
    passwordInput: 'input[type="password"], input[name="password"], input[placeholder*="password"]',
    loginButton: 'button:has-text("Login"), button:has-text("Sign In")',
    signupButton: 'button:has-text("Sign Up"), button:has-text("Create Account")'
  }
};
