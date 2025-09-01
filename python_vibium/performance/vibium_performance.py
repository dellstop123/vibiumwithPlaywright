"""
Performance Vibium functionality
"""

import time
from typing import Optional, Dict, Any
from ..core.vibium_core import VibiumCore

class VibiumPerformance:
    """
    Performance testing methods
    """
    
    def __init__(self, device='default', browser_type='chromium', core=None):
        self.device = device
        self.browser_type = browser_type
        # Use the passed core instance instead of creating a new one
        self.core = core if core else VibiumCore(device, browser_type)
    
    def measure_load_time(self, url: str) -> Optional[float]:
        """
        Measure page load time
        
        Args:
            url (str): URL to measure
            
        Returns:
            float: Load time in seconds or None if failed
        """
        try:
            start_time = time.time()
            
            self.core.goto(url)
            
            end_time = time.time()
            load_time = end_time - start_time
            
            print(f"[{self.device}] Page load time: {load_time:.2f} seconds")
            return load_time
            
        except Exception as e:
            print(f"[{self.device}] Failed to measure load time: {str(e)}")
            return None
    
    def check_core_web_vitals(self) -> Dict[str, Any]:
        """
        Check Core Web Vitals metrics
        
        Returns:
            Dict[str, Any]: Core Web Vitals data
        """
        try:
            # Get performance metrics from browser
            metrics = self.core.page.evaluate("""
                () => {
                    const navigation = performance.getEntriesByType('navigation')[0];
                    const paint = performance.getEntriesByType('paint');
                    
                    return {
                        domContentLoaded: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
                        loadComplete: navigation.loadEventEnd - navigation.loadEventStart,
                        firstPaint: paint.find(p => p.name === 'first-paint')?.startTime || 0,
                        firstContentfulPaint: paint.find(p => p.name === 'first-contentful-paint')?.startTime || 0
                    };
                }
            """)
            
            print(f"[{self.device}] Core Web Vitals: {metrics}")
            return metrics
            
        except Exception as e:
            print(f"[{self.device}] Failed to get Core Web Vitals: {str(e)}")
            return {}
    
    def measure_scroll_performance(self, scroll_distance: int = 1000) -> Optional[float]:
        """
        Measure scroll performance
        
        Args:
            scroll_distance (int): Distance to scroll in pixels
            
        Returns:
            float: Scroll time in seconds or None if failed
        """
        try:
            start_time = time.time()
            
            self.core.page.evaluate(f"window.scrollTo(0, {scroll_distance})")
            
            # Wait for scroll to complete
            time.sleep(0.5)
            
            end_time = time.time()
            scroll_time = end_time - start_time
            
            print(f"[{self.device}] Scroll performance: {scroll_time:.3f} seconds for {scroll_distance}px")
            return scroll_time
            
        except Exception as e:
            print(f"[{self.device}] Failed to measure scroll performance: {str(e)}")
            return None
    
    def check_memory_usage(self) -> Optional[Dict[str, Any]]:
        """
        Check memory usage metrics
        
        Returns:
            Dict[str, Any]: Memory usage data
        """
        try:
            memory_info = self.core.page.evaluate("""
                () => {
                    if (performance.memory) {
                        return {
                            usedJSHeapSize: performance.memory.usedJSHeapSize,
                            totalJSHeapSize: performance.memory.totalJSHeapSize,
                            jsHeapSizeLimit: performance.memory.jsHeapSizeLimit
                        };
                    }
                    return null;
                }
            """)
            
            if memory_info:
                print(f"[{self.device}] Memory usage: {memory_info}")
                return memory_info
            else:
                print(f"[{self.device}] Memory metrics not available")
                return None
                
        except Exception as e:
            print(f"[{self.device}] Failed to get memory usage: {str(e)}")
            return None
    
    def measure_network_requests(self) -> Optional[Dict[str, Any]]:
        """
        Measure network request metrics
        
        Returns:
            Dict[str, Any]: Network request data
        """
        try:
            network_data = self.core.page.evaluate("""
                () => {
                    const navigation = performance.getEntriesByType('navigation')[0];
                    const resources = performance.getEntriesByType('resource');
                    
                    return {
                        totalRequests: resources.length,
                        totalSize: resources.reduce((sum, r) => sum + (r.transferSize || 0), 0),
                        domContentLoaded: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
                        loadComplete: navigation.loadEventEnd - navigation.loadEventStart
                    };
                }
            """)
            
            print(f"[{self.device}] Network metrics: {network_data}")
            return network_data
            
        except Exception as e:
            print(f"[{self.device}] Failed to get network metrics: {str(e)}")
            return None
    
    def performance_audit(self, url: str) -> Dict[str, Any]:
        """
        Run a comprehensive performance audit
        
        Args:
            url (str): URL to audit
            
        Returns:
            Dict[str, Any]: Performance audit results
        """
        try:
            print(f"[{self.device}] Starting performance audit for: {url}")
            
            audit_results = {
                'url': url,
                'timestamp': time.time(),
                'load_time': None,
                'core_web_vitals': {},
                'memory_usage': {},
                'network_metrics': {},
                'scroll_performance': None
            }
            
            # Measure load time
            audit_results['load_time'] = self.measure_load_time(url)
            
            # Check Core Web Vitals
            audit_results['core_web_vitals'] = self.check_core_web_vitals()
            
            # Check memory usage
            audit_results['memory_usage'] = self.check_memory_usage() or {}
            
            # Check network metrics
            audit_results['network_metrics'] = self.measure_network_requests() or {}
            
            # Measure scroll performance
            audit_results['scroll_performance'] = self.measure_scroll_performance()
            
            print(f"[{self.device}] Performance audit completed")
            return audit_results
            
        except Exception as e:
            print(f"[{self.device}] Failed to complete performance audit: {str(e)}")
            return {'error': str(e)}
    
    def compare_performance(self, urls: list, iterations: int = 3) -> Dict[str, Any]:
        """
        Compare performance across multiple URLs
        
        Args:
            urls (list): List of URLs to compare
            iterations (int): Number of iterations per URL
            
        Returns:
            Dict[str, Any]: Performance comparison results
        """
        try:
            print(f"[{self.device}] Starting performance comparison across {len(urls)} URLs")
            
            comparison_results = {}
            
            for url in urls:
                url_results = []
                
                for i in range(iterations):
                    print(f"[{self.device}] Testing {url} - iteration {i+1}/{iterations}")
                    
                    load_time = self.measure_load_time(url)
                    if load_time:
                        url_results.append(load_time)
                    
                    # Wait between iterations
                    if i < iterations - 1:
                        time.sleep(2)
                
                if url_results:
                    avg_load_time = sum(url_results) / len(url_results)
                    comparison_results[url] = {
                        'iterations': url_results,
                        'average': avg_load_time,
                        'min': min(url_results),
                        'max': max(url_results)
                    }
            
            print(f"[{self.device}] Performance comparison completed")
            return comparison_results
            
        except Exception as e:
            print(f"[{self.device}] Failed to complete performance comparison: {str(e)}")
            return {'error': str(e)}
