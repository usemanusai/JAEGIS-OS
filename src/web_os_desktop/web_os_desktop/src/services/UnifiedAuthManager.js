// UnifiedAuthManager.js - Unified Authentication System for JAEGIS Web OS
import CryptoJS from 'crypto-js';
import { demoAuthService } from './DemoAuthService';

class UnifiedAuthManager {
  constructor() {
    this.token = null;
    this.user = null;
    this.permissions = [];
    this.isAuthenticated = false;
    this.subscribers = new Set();
    this.refreshTimer = null;
    this.apiBaseURL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';
    
    // Initialize from storage
    this.initializeFromStorage();
  }
  
  // Authenticate user with N.L.D.S. system
  async authenticate(username, password) {
    try {
      // Use demo service for development
      const authData = await demoAuthService.authenticate(username, password);
      this.setAuthData(authData);

      return { success: true, user: this.user };
    } catch (error) {
      console.error('Authentication error:', error);
      return { success: false, error: error.message };
    }
  }
  
  // Set authentication data
  setAuthData(authData) {
    this.token = authData.access_token;
    this.user = authData.user;
    this.permissions = authData.permissions || [];
    this.isAuthenticated = true;
    
    // Store in sessionStorage (secure storage)
    sessionStorage.setItem('jaegis_token', this.token);
    sessionStorage.setItem('jaegis_user', JSON.stringify(this.user));
    sessionStorage.setItem('jaegis_permissions', JSON.stringify(this.permissions));
    
    // Set up token refresh
    this.setupTokenRefresh(authData.expires_in);
    
    // Notify subscribers
    this.notifySubscribers();
  }
  
  // Clear authentication data
  clearAuth() {
    this.token = null;
    this.user = null;
    this.permissions = [];
    this.isAuthenticated = false;
    
    // Clear storage
    sessionStorage.removeItem('jaegis_token');
    sessionStorage.removeItem('jaegis_user');
    sessionStorage.removeItem('jaegis_permissions');
    
    // Clear refresh timer
    if (this.refreshTimer) {
      clearTimeout(this.refreshTimer);
      this.refreshTimer = null;
    }
    
    // Notify subscribers
    this.notifySubscribers();
  }
  
  // Check if user has specific permission
  hasPermission(permission) {
    return this.permissions.includes(permission);
  }
  
  // Check if user has any of the specified permissions
  hasAnyPermission(permissions) {
    return permissions.some(permission => this.hasPermission(permission));
  }
  
  // Check if user has all specified permissions
  hasAllPermissions(permissions) {
    return permissions.every(permission => this.hasPermission(permission));
  }
  
  // Get authorization header for API requests
  getAuthHeader() {
    return this.token ? `Bearer ${this.token}` : null;
  }
  
  // Subscribe to authentication changes
  subscribe(callback) {
    this.subscribers.add(callback);
    // Immediately call with current state
    callback({
      isAuthenticated: this.isAuthenticated,
      user: this.user,
      permissions: this.permissions
    });
    
    // Return unsubscribe function
    return () => this.subscribers.delete(callback);
  }
  
  // Notify all subscribers of auth changes
  notifySubscribers() {
    const authState = {
      isAuthenticated: this.isAuthenticated,
      user: this.user,
      permissions: this.permissions
    };
    
    this.subscribers.forEach(callback => callback(authState));
  }
  
  // Initialize from sessionStorage
  initializeFromStorage() {
    const token = sessionStorage.getItem('jaegis_token');
    const userStr = sessionStorage.getItem('jaegis_user');
    const permissionsStr = sessionStorage.getItem('jaegis_permissions');
    
    if (token && userStr && permissionsStr) {
      try {
        this.token = token;
        this.user = JSON.parse(userStr);
        this.permissions = JSON.parse(permissionsStr);
        this.isAuthenticated = true;
        
        // Verify token is still valid
        this.verifyToken();
      } catch (error) {
        console.error('Failed to restore auth from storage:', error);
        this.clearAuth();
      }
    }
  }
  
  // Verify token validity
  async verifyToken() {
    if (!this.token) return false;

    try {
      await demoAuthService.verifyToken(this.token);
      return true;
    } catch (error) {
      console.error('Token verification failed:', error);
      this.clearAuth();
      return false;
    }
  }
  
  // Setup automatic token refresh
  setupTokenRefresh(expiresIn) {
    // Refresh token 5 minutes before expiration
    const refreshTime = (expiresIn - 300) * 1000;
    
    if (this.refreshTimer) {
      clearTimeout(this.refreshTimer);
    }
    
    this.refreshTimer = setTimeout(async () => {
      await this.refreshToken();
    }, refreshTime);
  }
  
  // Refresh authentication token
  async refreshToken() {
    try {
      const authData = await demoAuthService.refreshToken(this.token);
      this.setAuthData(authData);
    } catch (error) {
      console.error('Token refresh failed:', error);
      this.clearAuth();
    }
  }
  
  // Logout user
  async logout() {
    try {
      await demoAuthService.logout(this.token);
    } catch (error) {
      console.error('Logout API call failed:', error);
    } finally {
      // Clear auth data regardless of API call result
      this.clearAuth();
    }
  }
  
  // Get current user info
  getCurrentUser() {
    return this.user;
  }
  
  // Check if user is authenticated
  isUserAuthenticated() {
    return this.isAuthenticated;
  }
  
  // Get user role
  getUserRole() {
    return this.user?.role || 'guest';
  }
  
  // Security error class
  static SecurityError = class extends Error {
    constructor(message) {
      super(message);
      this.name = 'SecurityError';
    }
  };
}

// Global authentication manager instance
export const authManager = new UnifiedAuthManager();
export default UnifiedAuthManager;
