"""
Optimized Async Helper - Non-blocking API calls with caching and retry logic
Makes any API call non-blocking with intelligent caching and error recovery
"""
from PyQt6.QtCore import QThread, pyqtSignal, QTimer
import requests
from typing import Callable, Optional, Dict, Any
import time
import hashlib


class RequestCache:
    """Simple in-memory cache for API responses"""
    def __init__(self):
        self.cache = {}
        self.timestamps = {}
    
    def get(self, key: str, ttl: int = 300) -> Optional[Any]:
        """Get cached value if not expired"""
        if key not in self.cache:
            return None
        
        if time.time() - self.timestamps[key] > ttl:
            del self.cache[key]
            del self.timestamps[key]
            return None
        
        return self.cache[key]
    
    def set(self, key: str, value: Any):
        """Set cache value with timestamp"""
        self.cache[key] = value
        self.timestamps[key] = time.time()
    
    def clear(self):
        """Clear all cache"""
        self.cache.clear()
        self.timestamps.clear()
    
    def invalidate(self, pattern: str = None):
        """Invalidate cache by pattern (e.g., '/api/patients/' invalidates all patient caches)"""
        if not pattern:
            self.clear()
            return
        
        keys_to_delete = [k for k in self.cache.keys() if pattern in k]
        for k in keys_to_delete:
            del self.cache[k]
            del self.timestamps[k]


class AsyncAPICall(QThread):
    """Generic worker for any API call with retry logic"""
    finished = pyqtSignal(bool, object)  # (success, data)
    error = pyqtSignal(str)
    
    def __init__(self, method: str, url: str, json_data: Optional[Dict] = None, 
                 params: Optional[Dict] = None, timeout: int = 30, 
                 max_retries: int = 2, use_cache: bool = False, cache_ttl: int = 300):
        super().__init__()
        self.method = method.upper()
        self.url = url
        self.json_data = json_data
        self.params = params
        self.timeout = timeout
        self.max_retries = max_retries if method == 'GET' else 0  # Only retry GET requests
        self.use_cache = use_cache and method == 'GET'  # Only cache GET requests
        self.cache_ttl = cache_ttl
        self.cache_key = self._generate_cache_key() if self.use_cache else None
    
    def _generate_cache_key(self) -> str:
        """Generate unique cache key from URL and params"""
        key_str = f"{self.url}:{str(self.params)}"
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def run(self):
        """Execute API call in background with retry logic"""
        retry_count = 0
        last_error = None
        retry_after_seconds = None
        
        while retry_count <= self.max_retries:
            try:
                if self.method == 'GET':
                    response = requests.get(self.url, params=self.params, timeout=self.timeout)
                elif self.method == 'POST':
                    response = requests.post(self.url, json=self.json_data, timeout=self.timeout)
                elif self.method == 'PUT':
                    response = requests.put(self.url, json=self.json_data, timeout=self.timeout)
                elif self.method == 'PATCH':
                    response = requests.patch(self.url, json=self.json_data, timeout=self.timeout)
                elif self.method == 'DELETE':
                    response = requests.delete(self.url, timeout=self.timeout)
                else:
                    self.error.emit(f'Unsupported method: {self.method}')
                    self.finished.emit(False, None)
                    return
                
                response.raise_for_status()
                
                # Try to parse JSON, fall back to text
                try:
                    data = response.json()
                except:
                    data = {'text': response.text, 'status_code': response.status_code}
                
                self.finished.emit(True, data)
                return
                
            except requests.exceptions.Timeout as e:
                last_error = 'Request timeout'
                retry_count += 1
            except requests.exceptions.ConnectionError as e:
                last_error = 'Connection error - Cannot reach server'
                retry_count += 1
            except requests.exceptions.HTTPError as e:
                status = getattr(e.response, 'status_code', None)
                # Special-case 429 (rate limited): retry GETs with backoff / Retry-After
                if status == 429 and self.method == 'GET' and retry_count < self.max_retries:
                    last_error = 'HTTP error: 429'
                    try:
                        ra = e.response.headers.get('Retry-After')
                        retry_after_seconds = int(ra) if ra and ra.isdigit() else None
                    except Exception:
                        retry_after_seconds = None
                    retry_count += 1
                else:
                    # Don't retry on other 4xx errors (client errors)
                    if status is not None and 400 <= status < 500:
                        self.error.emit(f'HTTP error: {status}')
                        self.finished.emit(False, None)
                        return
                    last_error = f'HTTP error: {status}' if status is not None else 'HTTP error'
                    retry_count += 1
            except Exception as e:
                last_error = str(e)
                retry_count += 1
            
            # Exponential backoff before retry
            if retry_count <= self.max_retries:
                if retry_after_seconds is not None:
                    time.sleep(max(0, retry_after_seconds))
                    retry_after_seconds = None
                else:
                    # 0.5s, 1s, 2s, 4s...
                    time.sleep(0.5 * (2 ** (retry_count - 1)))
        
        # All retries exhausted
        self.error.emit(last_error)
        self.finished.emit(False, None)


class AsyncHelper:
    """
    Optimized helper class for async API calls with caching and retry logic
    
    Usage:
        helper = AsyncHelper(self)
        helper.get('/api/patients/', 
                   on_success=self.on_patients_loaded,
                   on_error=self.on_error,
                   use_cache=True)
    """
    
    # Class-level cache shared across all instances
    _global_cache = RequestCache()
    
    def __init__(self, parent, base_url: str = ""):
        self.parent = parent
        self.base_url = base_url
        self.active_workers = []  # Track active workers
        self.request_queue = {}  # Track pending requests to avoid duplicates

    def get_cached(self, url: str, params: Optional[Dict] = None, cache_ttl: int = 300) -> Optional[Any]:
        """Return cached GET response for a URL if present and not expired.

        Notes:
            - Cache is in-memory only (cleared on app restart).
            - Cache key matches the one used in `_make_request`.
        """
        full_url = self.base_url + url if not url.startswith('http') else url
        request_key = f"GET:{full_url}:{str(params)}"
        return self._global_cache.get(request_key, ttl=cache_ttl)
    
    def get(self, url: str, 
            on_success: Callable[[Any], None],
            on_error: Optional[Callable[[str], None]] = None,
            params: Optional[Dict] = None,
            timeout: int = 15,  # Reduced from 30
            show_loading: bool = False,
            loading_widget = None,
            loading_title: str = "Loading...",
            loading_subtitle: str = None,
            use_cache: bool = False,
            cache_ttl: int = 300):
        """
        Make async GET request with optional caching and loading indicator
        
        Args:
            url: API endpoint
            on_success: Callback when successful (receives data)
            on_error: Callback on error (receives error message)
            params: Query parameters
            timeout: Request timeout in seconds
            show_loading: Show loading overlay
            loading_widget: Widget to show loading on
            loading_title: Title for loading modal
            loading_subtitle: Subtitle for loading modal
            use_cache: Enable response caching
            cache_ttl: Cache time-to-live in seconds
        """
        return self._make_request('GET', url, on_success, on_error, 
                                 params=params, timeout=timeout,
                                 show_loading=show_loading, 
                                 loading_widget=loading_widget,
                                 loading_title=loading_title,
                                 loading_subtitle=loading_subtitle,
                                 use_cache=use_cache,
                                 cache_ttl=cache_ttl)
    
    def post(self, url: str,
             on_success: Callable[[Any], None],
             data: Optional[Dict] = None,
             on_error: Optional[Callable[[str], None]] = None,
             timeout: int = 15,
             show_loading: bool = False,
             loading_widget = None,
             loading_title: str = "Saving...",
             loading_subtitle: str = None):
        """Make async POST request with optional loading indicator"""
        return self._make_request('POST', url, on_success, on_error,
                                 json_data=data, timeout=timeout,
                                 show_loading=show_loading,
                                 loading_widget=loading_widget,
                                 loading_title=loading_title,
                                 loading_subtitle=loading_subtitle)
    
    def put(self, url: str,
            on_success: Callable[[Any], None],
            data: Optional[Dict] = None,
            on_error: Optional[Callable[[str], None]] = None,
            timeout: int = 15,
            show_loading: bool = False,
            loading_widget = None,
            loading_title: str = "Saving...",
            loading_subtitle: str = None):
        """Make async PUT request with optional loading indicator"""
        return self._make_request('PUT', url, on_success, on_error,
                                 json_data=data, timeout=timeout,
                                 show_loading=show_loading,
                                 loading_widget=loading_widget,
                                 loading_title=loading_title,
                                 loading_subtitle=loading_subtitle)
    
    def patch(self, url: str,
              on_success: Callable[[Any], None],
              data: Optional[Dict] = None,
              on_error: Optional[Callable[[str], None]] = None,
              timeout: int = 15,
              show_loading: bool = False,
              loading_widget = None,
              loading_title: str = "Saving...",
              loading_subtitle: str = None):
                """Make async PATCH request with optional loading indicator"""
                return self._make_request('PATCH', url, on_success, on_error,
                                                                 json_data=data, timeout=timeout,
                                                                 show_loading=show_loading,
                                                                 loading_widget=loading_widget,
                                                                 loading_title=loading_title,
                                                                 loading_subtitle=loading_subtitle)
    
    def delete(self, url: str,
               on_success: Callable[[Any], None],
               on_error: Optional[Callable[[str], None]] = None,
                             timeout: int = 15,
                             show_loading: bool = False,
                             loading_widget = None,
                             loading_title: str = "Deleting...",
                             loading_subtitle: str = None):
                """Make async DELETE request with optional loading indicator"""
                return self._make_request('DELETE', url, on_success, on_error,
                                                                    timeout=timeout,
                                                                    show_loading=show_loading,
                                                                    loading_widget=loading_widget,
                                                                    loading_title=loading_title,
                                                                    loading_subtitle=loading_subtitle)
    
    def _make_request(self, method: str, url: str,
                     on_success: Callable,
                     on_error: Optional[Callable] = None,
                     json_data: Optional[Dict] = None,
                     params: Optional[Dict] = None,
                     timeout: int = 15,
                     show_loading: bool = False,
                     loading_widget = None,
                     loading_title: str = "Loading...",
                     loading_subtitle: str = None,
                     use_cache: bool = False,
                     cache_ttl: int = 300):
        """Internal method to create and start worker with loading modal support"""
        
        # Build full URL
        full_url = self.base_url + url if not url.startswith('http') else url
        
        # Check for duplicate pending requests (avoid simultaneous identical requests)
        request_key = f"{method}:{full_url}:{str(params)}"
        if request_key in self.request_queue:
            # Add callback to existing request instead of creating new one
            self.request_queue[request_key].append((on_success, on_error))
            return None
        
        # Check cache for GET requests
        if use_cache and method == 'GET':
            cached_data = self._global_cache.get(request_key, ttl=cache_ttl)
            if cached_data is not None:
                on_success(cached_data)
                return None
        
        # Show loading if requested
        loading_modal = None
        if show_loading:
            try:
                from Desktop_Application.Frontend.loading_overlay import LoadingOverlay
                parent_widget = loading_widget if loading_widget is not None else (self.parent if hasattr(self, 'parent') else None)
                loading_modal = LoadingOverlay(
                    parent_widget,
                    message=loading_title,
                    submessage=loading_subtitle
                )
                loading_modal.show()
            except Exception as e:
                print(f"Warning: Could not show loading modal: {e}")
        
        # Create worker
        worker = AsyncAPICall(method, full_url, json_data, params, timeout,
                            max_retries=2, use_cache=use_cache, cache_ttl=cache_ttl)
        
        # Initialize callback queue for this request
        self.request_queue[request_key] = [(on_success, on_error)]
        
        # Connect callbacks
        def on_finished(success, data):
            # Hide loading
            if loading_modal:
                loading_modal.hide()
            
            # Call all pending callbacks for this request
            callbacks = self.request_queue.pop(request_key, [])
            for callback_success, callback_error in callbacks:
                if success:
                    # Cache the result for GET requests
                    if use_cache and method == 'GET':
                        self._global_cache.set(request_key, data)
                    callback_success(data)
                elif callback_error:
                    callback_error("Request failed")
            
            # Clean up worker
            if worker in self.active_workers:
                self.active_workers.remove(worker)
        
        def on_error_signal(error_msg):
            # Hide loading
            if loading_modal:
                loading_modal.hide()
            
            # Call all pending error callbacks
            callbacks = self.request_queue.pop(request_key, [])
            for callback_success, callback_error in callbacks:
                if callback_error:
                    callback_error(error_msg)
        
        worker.finished.connect(on_finished)
        worker.error.connect(on_error_signal)
        
        # Track and start worker
        self.active_workers.append(worker)
        worker.start()
        
        return worker
    
    def invalidate_cache(self, pattern: str = None):
        """Invalidate cache entries by pattern"""
        self._global_cache.invalidate(pattern)
    
    def clear_cache(self):
        """Clear all cached responses"""
        self._global_cache.clear()
    
    def cancel_all(self):
        """Cancel all active requests"""
        for worker in self.active_workers:
            if worker.isRunning():
                worker.terminate()
                worker.wait()
        self.active_workers.clear()
        self.request_queue.clear()

