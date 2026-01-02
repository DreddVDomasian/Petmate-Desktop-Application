"""
Async Helper - Simplifies threading API calls throughout the app
Makes any API call non-blocking with just a few lines of code
"""
from PyQt6.QtCore import QThread, pyqtSignal
import requests
from typing import Callable, Optional, Dict, Any


class AsyncAPICall(QThread):
    """Generic worker for any API call"""
    finished = pyqtSignal(bool, object)  # (success, data)
    error = pyqtSignal(str)
    
    def __init__(self, method: str, url: str, json_data: Optional[Dict] = None, 
                 params: Optional[Dict] = None, timeout: int = 30):
        super().__init__()
        self.method = method.upper()
        self.url = url
        self.json_data = json_data
        self.params = params
        self.timeout = timeout
    
    def run(self):
        """Execute API call in background"""
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
            
        except requests.exceptions.Timeout:
            self.error.emit('Request timeout')
            self.finished.emit(False, None)
        except requests.exceptions.ConnectionError:
            self.error.emit('Connection error - Cannot reach server')
            self.finished.emit(False, None)
        except requests.exceptions.HTTPError as e:
            self.error.emit(f'HTTP error: {e.response.status_code}')
            self.finished.emit(False, None)
        except Exception as e:
            self.error.emit(str(e))
            self.finished.emit(False, None)


class AsyncHelper:
    """
    Helper class to make async API calls simple
    
    Usage:
        helper = AsyncHelper(self)
        helper.get('/api/patients/', 
                   on_success=self.on_patients_loaded,
                   on_error=self.on_error)
    """
    
    def __init__(self, parent, base_url: str = ""):
        self.parent = parent
        self.base_url = base_url
        self.active_workers = []  # Track active workers
    
    def get(self, url: str, 
            on_success: Callable[[Any], None],
            on_error: Optional[Callable[[str], None]] = None,
            params: Optional[Dict] = None,
            timeout: int = 30,
            show_loading: bool = False,
            loading_widget = None):
        """
        Make async GET request
        
        Args:
            url: API endpoint
            on_success: Callback when successful (receives data)
            on_error: Callback on error (receives error message)
            params: Query parameters
            timeout: Request timeout in seconds
            show_loading: Show loading overlay
            loading_widget: Widget to show loading on
        """
        return self._make_request('GET', url, on_success, on_error, 
                                 params=params, timeout=timeout,
                                 show_loading=show_loading, 
                                 loading_widget=loading_widget)
    
    def post(self, url: str,
             on_success: Callable[[Any], None],
             data: Optional[Dict] = None,
             on_error: Optional[Callable[[str], None]] = None,
             timeout: int = 30,
             show_loading: bool = False,
             loading_widget = None):
        """Make async POST request"""
        return self._make_request('POST', url, on_success, on_error,
                                 json_data=data, timeout=timeout,
                                 show_loading=show_loading,
                                 loading_widget=loading_widget)
    
    def put(self, url: str,
            on_success: Callable[[Any], None],
            data: Optional[Dict] = None,
            on_error: Optional[Callable[[str], None]] = None,
            timeout: int = 30):
        """Make async PUT request"""
        return self._make_request('PUT', url, on_success, on_error,
                                 json_data=data, timeout=timeout)
    
    def patch(self, url: str,
              on_success: Callable[[Any], None],
              data: Optional[Dict] = None,
              on_error: Optional[Callable[[str], None]] = None,
              timeout: int = 30):
        """Make async PATCH request"""
        return self._make_request('PATCH', url, on_success, on_error,
                                  json_data=data, timeout=timeout)
    
    def delete(self, url: str,
               on_success: Callable[[Any], None],
               on_error: Optional[Callable[[str], None]] = None,
               timeout: int = 30):
        """Make async DELETE request"""
        return self._make_request('DELETE', url, on_success, on_error,
                                  timeout=timeout)
    
    def _make_request(self, method: str, url: str,
                     on_success: Callable,
                     on_error: Optional[Callable] = None,
                     json_data: Optional[Dict] = None,
                     params: Optional[Dict] = None,
                     timeout: int = 30,
                     show_loading: bool = False,
                     loading_widget = None):
        """Internal method to create and start worker"""
        
        # Build full URL
        full_url = self.base_url + url if not url.startswith('http') else url
        
        # Show loading if requested
        if show_loading:
            if hasattr(self.parent, 'show_skeleton_loader'):
                self.parent.show_skeleton_loader(loading_widget)
            elif hasattr(self.parent, 'loading_overlay'):
                self.parent.loading_overlay.show()
        
        # Create worker
        worker = AsyncAPICall(method, full_url, json_data, params, timeout)
        
        # Connect callbacks
        def on_finished(success, data):
            # Hide loading
            if show_loading:
                if hasattr(self.parent, 'hide_skeleton_loader'):
                    self.parent.hide_skeleton_loader(loading_widget)
                elif hasattr(self.parent, 'loading_overlay'):
                    self.parent.loading_overlay.hide()
            
            # Call user callback
            if success:
                on_success(data)
            elif on_error:
                on_error("Request failed")
            
            # Clean up worker
            if worker in self.active_workers:
                self.active_workers.remove(worker)
        
        def on_error_signal(error_msg):
            if on_error:
                on_error(error_msg)
        
        worker.finished.connect(on_finished)
        worker.error.connect(on_error_signal)
        
        # Track and start worker
        self.active_workers.append(worker)
        worker.start()
        
        return worker
    
    def cancel_all(self):
        """Cancel all active requests"""
        for worker in self.active_workers:
            if worker.isRunning():
                worker.terminate()
                worker.wait()
        self.active_workers.clear()
