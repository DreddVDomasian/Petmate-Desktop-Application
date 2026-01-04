/**
 * API Configuration
 * Handles API base URL based on environment
 */

// Get API URL from environment variable
// In production (Vercel), this will be set via Vercel env vars
// In development, it will use local backend
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Get the full API endpoint URL
 * @param {string} path - API endpoint path (e.g., '/api/pets/')
 * @returns {string} Full URL
 */
export const getApiUrl = (path) => {
  // Ensure path starts with /
  const normalizedPath = path.startsWith('/') ? path : `/${path}`;
  return `${API_BASE_URL}${normalizedPath}`;
};

/**
 * Fetch wrapper that automatically uses the correct API base URL
 * @param {string} path - API endpoint path
 * @param {RequestInit} options - Fetch options
 * @returns {Promise<Response>}
 */
export const apiFetch = (path, options = {}) => {
  const url = getApiUrl(path);
  
  // Ensure credentials are included for cookie-based auth
  const fetchOptions = {
    ...options,
    credentials: options.credentials || 'include',
  };
  
  return fetch(url, fetchOptions);
};

export default {
  getApiUrl,
  apiFetch,
  baseUrl: API_BASE_URL,
};
