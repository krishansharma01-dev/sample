export const API_BASE = process.env.VUE_APP_API_BASE_URL !== undefined
  ? process.env.VUE_APP_API_BASE_URL
  : (process.env.NODE_ENV === 'development' ? 'http://localhost:5000' : '');
