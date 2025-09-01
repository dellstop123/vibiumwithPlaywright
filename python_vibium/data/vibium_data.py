"""
Data Vibium functionality
"""

import random
import string
import time
from typing import Dict, Any, List
from ..core.vibium_core import VibiumCore

class VibiumData:
    """
    Test data generation methods
    """
    
    def __init__(self, device='default', browser_type='chromium', core=None):
        self.device = device
        self.browser_type = browser_type
        # Use the passed core instance instead of creating a new one
        self.core = core if core else VibiumCore(device, browser_type)
    
    def generate_email(self, domain: str = "example.com", prefix: str = "test") -> str:
        """
        Generate a random email address
        
        Args:
            domain (str): Email domain
            prefix (str): Email prefix
            
        Returns:
            str: Generated email address
        """
        timestamp = int(time.time())
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        email = f"{prefix}-{timestamp}@{domain}"
        print(f"[{self.device}] Generated email: {email}")
        return email
    
    def generate_user_data(self) -> Dict[str, Any]:
        """
        Generate random user data
        
        Returns:
            Dict[str, Any]: User data dictionary
        """
        first_names = ["John", "Jane", "Mike", "Sarah", "David", "Lisa", "Tom", "Emma"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller"]
        
        user_data = {
            'first_name': random.choice(first_names),
            'last_name': random.choice(last_names),
            'email': self.generate_email(),
            'phone': f"+1-{random.randint(200, 999)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}",
            'password': ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%", k=12))
        }
        
        print(f"[{self.device}] Generated user data for: {user_data['first_name']} {user_data['last_name']}")
        return user_data
    
    def generate_address_data(self) -> Dict[str, Any]:
        """
        Generate random address data
        
        Returns:
            Dict[str, Any]: Address data dictionary
        """
        streets = ["123 Main St", "456 Oak Ave", "789 Pine Rd", "321 Elm St", "654 Maple Dr"]
        cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia"]
        states = ["NY", "CA", "IL", "TX", "AZ", "PA", "FL", "OH", "GA", "NC"]
        
        address_data = {
            'street': random.choice(streets),
            'city': random.choice(cities),
            'state': random.choice(states),
            'zip_code': f"{random.randint(10000, 99999)}",
            'country': "United States"
        }
        
        print(f"[{self.device}] Generated address data for: {address_data['city']}, {address_data['state']}")
        return address_data
    
    def generate_product_data(self) -> Dict[str, Any]:
        """
        Generate random product data
        
        Returns:
            Dict[str, Any]: Product data dictionary
        """
        product_names = ["Laptop", "Smartphone", "Headphones", "Tablet", "Monitor", "Keyboard"]
        categories = ["Electronics", "Computers", "Mobile", "Audio", "Accessories"]
        
        product_data = {
            'name': random.choice(product_names),
            'category': random.choice(categories),
            'price': round(random.uniform(50.0, 2000.0), 2),
            'description': f"High-quality {random.choice(product_names).lower()} with excellent features",
            'sku': f"SKU-{random.randint(10000, 99999)}"
        }
        
        print(f"[{self.device}] Generated product data for: {product_data['name']}")
        return product_data
    
    def generate_credit_card_data(self) -> Dict[str, Any]:
        """
        Generate random credit card data
        
        Returns:
            Dict[str, Any]: Credit card data dictionary
        """
        card_types = ["Visa", "MasterCard", "American Express", "Discover"]
        
        card_data = {
            'card_type': random.choice(card_types),
            'card_number': f"{random.randint(4000, 4999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}",
            'cardholder_name': f"{random.choice(['John', 'Jane', 'Mike', 'Sarah'])} {random.choice(['Smith', 'Johnson', 'Williams', 'Brown'])}",
            'expiry_month': random.randint(1, 12),
            'expiry_year': random.randint(2025, 2030),
            'cvv': random.randint(100, 999)
        }
        
        print(f"[{self.device}] Generated credit card data for: {card_data['cardholder_name']}")
        return card_data
    
    def generate_coupon_codes(self, count: int = 1) -> List[str]:
        """
        Generate random coupon codes
        
        Args:
            count (int): Number of coupon codes to generate
            
        Returns:
            List[str]: List of coupon codes
        """
        coupons = []
        for i in range(count):
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            coupons.append(code)
            print(f"[{self.device}] Generated coupon code: {code}")
        
        return coupons
    
    def generate_order_data(self) -> Dict[str, Any]:
        """
        Generate random order data
        
        Returns:
            Dict[str, Any]: Order data dictionary
        """
        order_data = {
            'order_id': f"ORD-{int(time.time())}",
            'status': random.choice(['pending', 'processing', 'shipped', 'delivered']),
            'total_amount': round(random.uniform(100.0, 1500.0), 2),
            'shipping_method': random.choice(['standard', 'express', 'overnight']),
            'payment_method': random.choice(['credit_card', 'paypal', 'bank_transfer'])
        }
        
        print(f"[{self.device}] Generated order data: {order_data['order_id']}")
        return order_data
    
    def generate_search_queries(self, count: int = 5) -> List[str]:
        """
        Generate search query test data
        
        Args:
            count (int): Number of queries to generate
            
        Returns:
            List[str]: Generated search queries
        """
        search_terms = [
            "laptop", "smartphone", "headphones", "tablet", "camera",
            "wireless", "bluetooth", "gaming", "professional", "budget",
            "high-end", "portable", "compact", "durable", "fast"
        ]
        
        queries = []
        for _ in range(count):
            query = ' '.join(random.sample(search_terms, random.randint(1, 3)))
            queries.append(query)
        
        print(f"[{self.device}] Generated search queries: {queries}")
        return queries
    
    def generate_newsletter_emails(self, count: int = 10) -> List[str]:
        """
        Generate newsletter email test data
        
        Args:
            count (int): Number of emails to generate
            
        Returns:
            List[str]: Generated email addresses
        """
        emails = []
        for _ in range(count):
            emails.append(self.generate_email())
        
        print(f"[{self.device}] Generated newsletter emails: {emails}")
        return emails
    
    def generate_coupon_codes(self, count: int = 5) -> List[str]:
        """
        Generate coupon code test data
        
        Args:
            count (int): Number of codes to generate
            
        Returns:
            List[str]: Generated coupon codes
        """
        codes = []
        for _ in range(count):
            code = f"{random.choice(['SAVE', 'DISCOUNT', 'OFFER', 'DEAL'])}{random.randint(10, 99)}"
            codes.append(code)
        
        print(f"[{self.device}] Generated coupon codes: {codes}")
        return codes
    
    def generate_test_scenarios(self) -> List[Dict[str, Any]]:
        """
        Generate test scenario data
        
        Returns:
            List[Dict[str, Any]]: Generated test scenarios
        """
        scenarios = [
            {
                'name': 'Guest Checkout',
                'user_type': 'guest',
                'products': 2,
                'payment_method': 'credit_card',
                'shipping': 'standard'
            },
            {
                'name': 'Registered User Checkout',
                'user_type': 'registered',
                'products': 1,
                'payment_method': 'paypal',
                'shipping': 'express'
            },
            {
                'name': 'Large Order',
                'user_type': 'guest',
                'products': 5,
                'payment_method': 'credit_card',
                'shipping': 'overnight'
            }
        ]
        
        print(f"[{self.device}] Generated test scenarios: {scenarios}")
        return scenarios
