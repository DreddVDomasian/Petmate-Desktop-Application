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

/**
 * Safely parse JSON from a Response (handles empty/non-JSON bodies).
 * @param {Response} res
 */
export const readJsonSafe = async (res) => {
  const text = await res.text();
  if (!text) return null;
  try {
    return JSON.parse(text);
  } catch {
    return null;
  }
};

/**
 * Normalize common DRF responses (array vs {results: []}).
 * @param {any} data
 * @returns {Array}
 */
export const normalizeList = (data) => {
  if (Array.isArray(data)) return data;
  if (data && Array.isArray(data.results)) return data.results;
  return [];
};

export default {
  getApiUrl,
  apiFetch,
  readJsonSafe,
  normalizeList,
  baseUrl: API_BASE_URL,
};
