"""
API Worker Thread - Makes API calls without blocking the UI
"""
from PyQt6.QtCore import QThread, pyqtSignal
import requests


class APIWorker(QThread):
    """Worker thread for making API calls asynchronously"""
    
    # Signals to communicate back to main thread
    finished = pyqtSignal(bool, dict)  # (success, response)
    error = pyqtSignal(str)
    
    def __init__(self, method, url, json_data=None, timeout=10):
        super().__init__()
        self.method = method
        self.url = url
        self.json_data = json_data
        self.timeout = timeout
    
    def run(self):
        """Execute API call in background thread"""
        try:
            if self.method == 'POST':
                response = requests.post(
                    self.url,
                    json=self.json_data,
                    timeout=self.timeout
                )
            elif self.method == 'GET':
                response = requests.get(
                    self.url,
                    timeout=self.timeout
                )
            elif self.method == 'PUT':
                response = requests.put(
                    self.url,
                    json=self.json_data,
                    timeout=self.timeout
                )
            elif self.method == 'DELETE':
                response = requests.delete(
                    self.url,
                    timeout=self.timeout
                )
            
            if response.status_code in [200, 201]:
                self.finished.emit(True, response.json())
            else:
                try:
                    error_data = response.json()
                except:
                    error_data = {'error': response.text}
                self.finished.emit(False, error_data)
                
        except requests.exceptions.Timeout:
            self.error.emit('Request timeout - Server not responding')
            self.finished.emit(False, {'error': 'Request timeout'})
        except requests.exceptions.ConnectionError:
            self.error.emit('Connection error - Cannot reach server')
            self.finished.emit(False, {'error': 'Connection error'})
        except Exception as e:
            self.error.emit(f'Error: {str(e)}')
            self.finished.emit(False, {'error': str(e)})


class DataLoaderWorker(QThread):
    """Worker specifically for loading list data (patients, services, etc.)"""
    
    finished = pyqtSignal(bool, object)  # (success, data)
    error = pyqtSignal(str)
    
    def __init__(self, url, timeout=10):
        super().__init__()
        self.url = url
        self.timeout = timeout
    
    def run(self):
        """Execute GET request in background"""
        try:
            response = requests.get(self.url, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            self.finished.emit(True, data)
        except requests.exceptions.Timeout:
            self.error.emit('Request timeout')
            self.finished.emit(False, None)
        except requests.exceptions.ConnectionError:
            self.error.emit('Connection error')
            self.finished.emit(False, None)
        except Exception as e:
            self.error.emit(str(e))
            self.finished.emit(False, None)
