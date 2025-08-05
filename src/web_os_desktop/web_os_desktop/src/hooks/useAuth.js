// useAuth.js - React Hook for Authentication
import { useState, useEffect } from 'react';
import { authManager } from '../services/UnifiedAuthManager';

export function useAuth() {
  const [authState, setAuthState] = useState({
    isAuthenticated: authManager.isAuthenticated,
    user: authManager.user,
    permissions: authManager.permissions,
    loading: false,
    error: null
  });
  
  useEffect(() => {
    const unsubscribe = authManager.subscribe((newAuthState) => {
      setAuthState(prevState => ({
        ...prevState,
        ...newAuthState,
        loading: false,
        error: null
      }));
    });
    
    return unsubscribe;
  }, []);
  
  const login = async (username, password) => {
    setAuthState(prevState => ({ ...prevState, loading: true, error: null }));
    
    const result = await authManager.authenticate(username, password);
    
    if (!result.success) {
      setAuthState(prevState => ({
        ...prevState,
        loading: false,
        error: result.error
      }));
    }
    
    return result;
  };
  
  const logout = async () => {
    setAuthState(prevState => ({ ...prevState, loading: true }));
    await authManager.logout();
  };
  
  const hasPermission = (permission) => {
    return authManager.hasPermission(permission);
  };
  
  const hasAnyPermission = (permissions) => {
    return authManager.hasAnyPermission(permissions);
  };
  
  const hasAllPermissions = (permissions) => {
    return authManager.hasAllPermissions(permissions);
  };
  
  return {
    ...authState,
    login,
    logout,
    hasPermission,
    hasAnyPermission,
    hasAllPermissions,
    getAuthHeader: () => authManager.getAuthHeader()
  };
}

// Permission-based component wrapper
export function RequirePermission({ permission, permissions, children, fallback = null }) {
  const { hasPermission, hasAnyPermission, hasAllPermissions } = useAuth();
  
  let hasRequiredPermission = false;
  
  if (permission) {
    hasRequiredPermission = hasPermission(permission);
  } else if (permissions) {
    if (Array.isArray(permissions)) {
      hasRequiredPermission = hasAllPermissions(permissions);
    } else if (permissions.any) {
      hasRequiredPermission = hasAnyPermission(permissions.any);
    } else if (permissions.all) {
      hasRequiredPermission = hasAllPermissions(permissions.all);
    }
  }
  
  return hasRequiredPermission ? children : fallback;
}

// Authentication guard component
export function AuthGuard({ children, fallback = <div>Please log in</div> }) {
  const { isAuthenticated } = useAuth();
  
  return isAuthenticated ? children : fallback;
}
