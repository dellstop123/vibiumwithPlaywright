"""
E-commerce Vibium functionality
"""

import time
from typing import Optional, List, Dict, Any
from ..core.vibium_core import VibiumCore

class VibiumEcommerce:
    """
    E-commerce specific automation methods
    """
    
    def __init__(self, device='default', browser_type='chromium', core=None):
        self.device = device
        self.browser_type = browser_type
        # Use the passed core instance instead of creating a new one
        self.core = core if core else VibiumCore(device, browser_type)
    
    def add_to_cart(self, product_selector: str, quantity: int = 1):
        """
        Add a product to cart
        
        Args:
            product_selector (str): Selector for the product
            quantity (int): Quantity to add
        """
        try:
            # Find and click add to cart button
            add_to_cart_btn = self.core.page.locator(f"{product_selector} .add-to-cart, {product_selector} [data-testid='add-to-cart'], {product_selector} button")
            add_to_cart_btn.click()
            
            # Wait for cart update
            time.sleep(2)
            
            print(f"[{self.device}] Added product to cart: {product_selector}")
            return True
            
        except Exception as e:
            print(f"[{self.device}] Failed to add product to cart: {str(e)}")
            return False
    
    def search_products(self, query: str):
        """
        Search for products
        
        Args:
            query (str): Search query
        """
        try:
            # Find search input and type query
            search_input = self.core.page.locator("input[type='search'], .search-input, [data-testid='search-input']")
            search_input.fill(query)
            
            # Submit search
            search_input.press("Enter")
            
            # Wait for results
            self.core.page.wait_for_load_state('networkidle')
            
            print(f"[{self.device}] Searched for products: {query}")
            return True
            
        except Exception as e:
            print(f"[{self.device}] Failed to search products: {str(e)}")
            return False
    
    def navigate_to_category(self, category_name: str):
        """
        Navigate to a product category
        
        Args:
            category_name (str): Name of the category
        """
        try:
            # Find and click category link
            category_link = self.core.page.locator(f"a:has-text('{category_name}'), [data-testid='category-{category_name}'], .category-{category_name}")
            category_link.click()
            
            # Wait for page load
            self.core.page.wait_for_load_state('networkidle')
            
            print(f"[{self.device}] Navigated to category: {category_name}")
            return True
            
        except Exception as e:
            print(f"[{self.device}] Failed to navigate to category: {str(e)}")
            return False
    
    def view_product_details(self, product_selector: str):
        """
        View detailed information about a product
        
        Args:
            product_selector (str): Selector for the product
        """
        try:
            # Click on product to view details
            product_link = self.core.page.locator(f"{product_selector} a, {product_selector} .product-link")
            product_link.click()
            
            # Wait for product page load
            self.core.page.wait_for_load_state('networkidle')
            
            print(f"[{self.device}] Viewed product details: {product_selector}")
            return True
            
        except Exception as e:
            print(f"[{self.device}] Failed to view product details: {str(e)}")
            return False
    
    def add_to_wishlist(self, product_selector: str):
        """
        Add a product to wishlist
        
        Args:
            product_selector (str): Selector for the product
        """
        try:
            # Find and click wishlist button
            wishlist_btn = self.core.page.locator(f"{product_selector} .wishlist-btn, {product_selector} [data-testid='wishlist'], {product_selector} .heart")
            wishlist_btn.click()
            
            # Wait for wishlist update
            time.sleep(1)
            
            print(f"[{self.device}] Added product to wishlist: {product_selector}")
            return True
            
        except Exception as e:
            print(f"[{self.device}] Failed to add product to wishlist: {str(e)}")
            return False
    
    def get_product_price(self, product_selector: str) -> Optional[str]:
        """
        Get the price of a product
        
        Args:
            product_selector (str): Selector for the product
            
        Returns:
            str: Product price or None if not found
        """
        try:
            price_element = self.core.page.locator(f"{product_selector} .price, {product_selector} [data-testid='price'], {product_selector} .product-price")
            price = price_element.text_content()
            
            print(f"[{self.device}] Got product price: {price}")
            return price.strip() if price else None
            
        except Exception as e:
            print(f"[{self.device}] Failed to get product price: {str(e)}")
            return None
    
    def get_cart_count(self) -> int:
        """
        Get the number of items in cart
        
        Returns:
            int: Number of items in cart
        """
        try:
            cart_count = self.core.page.locator(".cart-count, [data-testid='cart-count'], .cart-badge")
            count_text = cart_count.text_content()
            
            count = int(count_text) if count_text and count_text.isdigit() else 0
            print(f"[{self.device}] Cart count: {count}")
            return count
            
        except Exception as e:
            print(f"[{self.device}] Failed to get cart count: {str(e)}")
            return 0
    
    def clear_cart(self):
        """Clear all items from cart"""
        try:
            # Find and click clear cart button
            clear_btn = self.core.page.locator(".clear-cart, [data-testid='clear-cart'], .empty-cart")
            clear_btn.click()
            
            # Confirm clear action if dialog appears
            try:
                confirm_btn = self.core.page.locator(".confirm-clear, [data-testid='confirm-clear'], .yes")
                confirm_btn.click()
            except:
                pass
            
            # Wait for cart update
            time.sleep(2)
            
            print(f"[{self.device}] Cart cleared")
            return True
            
        except Exception as e:
            print(f"[{self.device}] Failed to clear cart: {str(e)}")
            return False
    
    def apply_coupon(self, coupon_code: str):
        """
        Apply a coupon code
        
        Args:
            coupon_code (str): Coupon code to apply
        """
        try:
            # Find coupon input and apply button
            coupon_input = self.core.page.locator("input[name='coupon'], .coupon-input, [data-testid='coupon-input']")
            apply_btn = self.core.page.locator(".apply-coupon, [data-testid='apply-coupon'], .coupon-apply")
            
            # Enter coupon code
            coupon_input.fill(coupon_code)
            
            # Click apply
            apply_btn.click()
            
            # Wait for coupon application
            time.sleep(2)
            
            print(f"[{self.device}] Applied coupon: {coupon_code}")
            return True
            
        except Exception as e:
            print(f"[{self.device}] Failed to apply coupon: {str(e)}")
            return False
