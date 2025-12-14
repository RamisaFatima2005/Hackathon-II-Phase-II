// frontend/src/lib/api_client.ts
/**
 * API client for making requests to the backend.
 * This client is a wrapper around axios and provides methods for making GET, POST, PUT, PATCH, and DELETE requests.
 * It also handles authentication by including the access token in the headers of each request.
 * The base URL for the API is configured using the NEXT_PUBLIC_BACKEND_URL environment variable.
 */
import axios from "axios";

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers["Authorization"] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default apiClient;