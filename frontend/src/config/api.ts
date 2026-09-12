/**
 * Global API Configuration for TERRA Frontend.
 * Supports both Local Development and Server Deployment (e.g. port 3001 / Nginx reverse proxy).
 */

const getBaseUrl = (): string => {
  // 1. Explicit environment variable override
  if (import.meta.env.VITE_API_BASE_URL !== undefined && import.meta.env.VITE_API_BASE_URL !== '') {
    return import.meta.env.VITE_API_BASE_URL;
  }

  // 2. Global runtime window override
  if (typeof window !== 'undefined' && (window as any).__VITE_API_BASE_URL__) {
    return (window as any).__VITE_API_BASE_URL__;
  }

  // 3. Local development mode (vite dev): fallback to direct backend URL if no proxy
  if (import.meta.env.DEV) {
    return 'http://localhost:8000';
  }

  // 4. Production build (Docker / Nginx):
  // Relative URL '' directs requests to http://<server_host>:<server_port>/api/...
  // which Nginx cleanly reverse-proxies to backend:8000 without CORS or port leaks.
  return '';
};

export const API_BASE_URL = getBaseUrl();

export const apiUrl = (endpoint: string): string => {
  const cleanEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
  return `${API_BASE_URL}${cleanEndpoint}`;
};
