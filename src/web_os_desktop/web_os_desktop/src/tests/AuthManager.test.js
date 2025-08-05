// AuthManager.test.js - Tests for Unified Authentication Manager
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { authManager } from '../services/UnifiedAuthManager';
import { demoAuthService } from '../services/DemoAuthService';
import LoginForm from '../components/auth/LoginForm';

// Mock the demo auth service
jest.mock('../services/DemoAuthService');

describe('UnifiedAuthManager', () => {
  beforeEach(() => {
    // Clear auth state before each test
    authManager.clearAuth();
    jest.clearAllMocks();
  });

  describe('Authentication Flow', () => {
    test('should authenticate user with valid credentials', async () => {
      const mockAuthData = {
        access_token: 'mock-token',
        user: { id: 'admin', username: 'admin', role: 'administrator' },
        permissions: ['system_access', 'agent_management'],
        expires_in: 28800
      };

      demoAuthService.authenticate.mockResolvedValue(mockAuthData);

      const result = await authManager.authenticate('admin', 'password');

      expect(result.success).toBe(true);
      expect(authManager.isAuthenticated).toBe(true);
      expect(authManager.user).toEqual(mockAuthData.user);
      expect(authManager.permissions).toEqual(mockAuthData.permissions);
    });

    test('should reject authentication with invalid credentials', async () => {
      demoAuthService.authenticate.mockRejectedValue(new Error('Invalid credentials'));

      const result = await authManager.authenticate('invalid', 'invalid');

      expect(result.success).toBe(false);
      expect(result.error).toBe('Invalid credentials');
      expect(authManager.isAuthenticated).toBe(false);
    });

    test('should clear authentication on logout', async () => {
      // First authenticate
      const mockAuthData = {
        access_token: 'mock-token',
        user: { id: 'admin', username: 'admin' },
        permissions: ['system_access'],
        expires_in: 28800
      };
      demoAuthService.authenticate.mockResolvedValue(mockAuthData);
      await authManager.authenticate('admin', 'password');

      // Then logout
      demoAuthService.logout.mockResolvedValue({ success: true });
      await authManager.logout();

      expect(authManager.isAuthenticated).toBe(false);
      expect(authManager.user).toBe(null);
      expect(authManager.token).toBe(null);
    });
  });

  describe('Permission Management', () => {
    beforeEach(async () => {
      const mockAuthData = {
        access_token: 'mock-token',
        user: { id: 'admin', username: 'admin' },
        permissions: ['system_access', 'agent_management', 'file_access'],
        expires_in: 28800
      };
      demoAuthService.authenticate.mockResolvedValue(mockAuthData);
      await authManager.authenticate('admin', 'password');
    });

    test('should check single permission correctly', () => {
      expect(authManager.hasPermission('system_access')).toBe(true);
      expect(authManager.hasPermission('invalid_permission')).toBe(false);
    });

    test('should check multiple permissions with hasAnyPermission', () => {
      expect(authManager.hasAnyPermission(['system_access', 'invalid_permission'])).toBe(true);
      expect(authManager.hasAnyPermission(['invalid1', 'invalid2'])).toBe(false);
    });

    test('should check multiple permissions with hasAllPermissions', () => {
      expect(authManager.hasAllPermissions(['system_access', 'agent_management'])).toBe(true);
      expect(authManager.hasAllPermissions(['system_access', 'invalid_permission'])).toBe(false);
    });
  });

  describe('Token Management', () => {
    test('should provide correct authorization header', async () => {
      const mockAuthData = {
        access_token: 'mock-token-123',
        user: { id: 'admin', username: 'admin' },
        permissions: ['system_access'],
        expires_in: 28800
      };
      demoAuthService.authenticate.mockResolvedValue(mockAuthData);
      await authManager.authenticate('admin', 'password');

      expect(authManager.getAuthHeader()).toBe('Bearer mock-token-123');
    });

    test('should return null auth header when not authenticated', () => {
      expect(authManager.getAuthHeader()).toBe(null);
    });

    test('should refresh token successfully', async () => {
      // Initial authentication
      const mockAuthData = {
        access_token: 'old-token',
        user: { id: 'admin', username: 'admin' },
        permissions: ['system_access'],
        expires_in: 28800
      };
      demoAuthService.authenticate.mockResolvedValue(mockAuthData);
      await authManager.authenticate('admin', 'password');

      // Token refresh
      const refreshedAuthData = {
        access_token: 'new-token',
        user: { id: 'admin', username: 'admin' },
        permissions: ['system_access'],
        expires_in: 28800
      };
      demoAuthService.refreshToken.mockResolvedValue(refreshedAuthData);
      await authManager.refreshToken();

      expect(authManager.token).toBe('new-token');
    });
  });

  describe('State Persistence', () => {
    test('should persist authentication state to sessionStorage', async () => {
      const mockAuthData = {
        access_token: 'persist-token',
        user: { id: 'admin', username: 'admin' },
        permissions: ['system_access'],
        expires_in: 28800
      };
      demoAuthService.authenticate.mockResolvedValue(mockAuthData);
      await authManager.authenticate('admin', 'password');

      expect(sessionStorage.getItem('jaegis_token')).toBe('persist-token');
      expect(JSON.parse(sessionStorage.getItem('jaegis_user'))).toEqual(mockAuthData.user);
      expect(JSON.parse(sessionStorage.getItem('jaegis_permissions'))).toEqual(mockAuthData.permissions);
    });

    test('should restore authentication state from sessionStorage', () => {
      // Simulate stored auth data
      sessionStorage.setItem('jaegis_token', 'stored-token');
      sessionStorage.setItem('jaegis_user', JSON.stringify({ id: 'admin', username: 'admin' }));
      sessionStorage.setItem('jaegis_permissions', JSON.stringify(['system_access']));

      // Create new auth manager instance to test restoration
      const newAuthManager = new (authManager.constructor)();

      expect(newAuthManager.isAuthenticated).toBe(true);
      expect(newAuthManager.token).toBe('stored-token');
      expect(newAuthManager.user.username).toBe('admin');
    });

    test('should clear sessionStorage on logout', async () => {
      const mockAuthData = {
        access_token: 'clear-token',
        user: { id: 'admin', username: 'admin' },
        permissions: ['system_access'],
        expires_in: 28800
      };
      demoAuthService.authenticate.mockResolvedValue(mockAuthData);
      await authManager.authenticate('admin', 'password');

      demoAuthService.logout.mockResolvedValue({ success: true });
      await authManager.logout();

      expect(sessionStorage.getItem('jaegis_token')).toBe(null);
      expect(sessionStorage.getItem('jaegis_user')).toBe(null);
      expect(sessionStorage.getItem('jaegis_permissions')).toBe(null);
    });
  });
});

describe('LoginForm Component', () => {
  test('should render login form correctly', () => {
    render(<LoginForm onSuccess={jest.fn()} />);

    expect(screen.getByText('JAEGIS Web OS')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Enter your username')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Enter your password')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /sign in/i })).toBeInTheDocument();
  });

  test('should handle form submission', async () => {
    const mockOnSuccess = jest.fn();
    const mockAuthData = {
      access_token: 'test-token',
      user: { id: 'admin', username: 'admin' },
      permissions: ['system_access'],
      expires_in: 28800
    };

    demoAuthService.authenticate.mockResolvedValue(mockAuthData);
    render(<LoginForm onSuccess={mockOnSuccess} />);

    const usernameInput = screen.getByPlaceholderText('Enter your username');
    const passwordInput = screen.getByPlaceholderText('Enter your password');
    const submitButton = screen.getByRole('button', { name: /sign in/i });

    fireEvent.change(usernameInput, { target: { value: 'admin' } });
    fireEvent.change(passwordInput, { target: { value: 'password' } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(mockOnSuccess).toHaveBeenCalledWith(mockAuthData.user);
    });
  });

  test('should display error message on failed login', async () => {
    demoAuthService.authenticate.mockRejectedValue(new Error('Invalid credentials'));
    render(<LoginForm onSuccess={jest.fn()} />);

    const usernameInput = screen.getByPlaceholderText('Enter your username');
    const passwordInput = screen.getByPlaceholderText('Enter your password');
    const submitButton = screen.getByRole('button', { name: /sign in/i });

    fireEvent.change(usernameInput, { target: { value: 'invalid' } });
    fireEvent.change(passwordInput, { target: { value: 'invalid' } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText('Invalid credentials')).toBeInTheDocument();
    });
  });

  test('should toggle password visibility', () => {
    render(<LoginForm onSuccess={jest.fn()} />);

    const passwordInput = screen.getByPlaceholderText('Enter your password');
    const toggleButton = screen.getByRole('button', { name: '' }); // Password toggle button

    expect(passwordInput.type).toBe('password');

    fireEvent.click(toggleButton);
    expect(passwordInput.type).toBe('text');

    fireEvent.click(toggleButton);
    expect(passwordInput.type).toBe('password');
  });
});
