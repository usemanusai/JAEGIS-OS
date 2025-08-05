// DemoAuthService.js - Demo Authentication Service for Development
// This simulates the N.L.D.S. authentication system

class DemoAuthService {
  constructor() {
    this.users = new Map([
      ['admin', {
        id: 'admin',
        username: 'admin',
        password: 'password', // In real implementation, this would be hashed
        role: 'administrator',
        permissions: [
          'system_access',
          'agent_management',
          'nlds_access',
          'data_processing',
          'llm_access',
          'ai_processing',
          'ai_chat',
          'conversation_history',
          'search_access',
          'data_indexing',
          'deployment_access',
          'system_config',
          'forge_access',
          'tool_management',
          'file_access',
          'ai_assistance',
          'file_system_access',
          'file_operations',
          'command_execution',
          'system_monitoring',
          'performance_data'
        ],
        profile: {
          name: 'Administrator',
          email: 'admin@jaegis.local',
          avatar: '/avatars/admin.png',
          department: 'System Administration',
          lastLogin: null
        }
      }],
      ['user', {
        id: 'user',
        username: 'user',
        password: 'password',
        role: 'user',
        permissions: [
          'ai_chat',
          'conversation_history',
          'search_access',
          'file_access',
          'ai_assistance'
        ],
        profile: {
          name: 'Standard User',
          email: 'user@jaegis.local',
          avatar: '/avatars/user.png',
          department: 'General',
          lastLogin: null
        }
      }],
      ['researcher', {
        id: 'researcher',
        username: 'researcher',
        password: 'password',
        role: 'researcher',
        permissions: [
          'nlds_access',
          'data_processing',
          'ai_chat',
          'conversation_history',
          'search_access',
          'data_indexing',
          'file_access',
          'ai_assistance',
          'system_monitoring'
        ],
        profile: {
          name: 'Research Scientist',
          email: 'researcher@jaegis.local',
          avatar: '/avatars/researcher.png',
          department: 'Research & Development',
          lastLogin: null
        }
      }]
    ]);
    
    this.sessions = new Map();
  }
  
  // Simulate authentication
  async authenticate(username, password) {
    // Simulate network delay
    await this.delay(500);
    
    const user = this.users.get(username);
    
    if (!user || user.password !== password) {
      throw new Error('Invalid username or password');
    }
    
    // Update last login
    user.profile.lastLogin = new Date().toISOString();
    
    // Generate session token
    const token = this.generateToken(user);
    
    // Store session
    this.sessions.set(token, {
      user: user,
      createdAt: new Date().toISOString(),
      expiresAt: new Date(Date.now() + 8 * 60 * 60 * 1000).toISOString() // 8 hours
    });
    
    return {
      access_token: token,
      token_type: 'Bearer',
      expires_in: 8 * 60 * 60, // 8 hours in seconds
      user: {
        id: user.id,
        username: user.username,
        role: user.role,
        profile: user.profile
      },
      permissions: user.permissions
    };
  }
  
  // Verify token
  async verifyToken(token) {
    await this.delay(100);
    
    const session = this.sessions.get(token);
    
    if (!session) {
      throw new Error('Invalid token');
    }
    
    // Check if token is expired
    if (new Date() > new Date(session.expiresAt)) {
      this.sessions.delete(token);
      throw new Error('Token expired');
    }
    
    return {
      valid: true,
      user: session.user,
      permissions: session.user.permissions
    };
  }
  
  // Refresh token
  async refreshToken(token) {
    await this.delay(200);
    
    const session = this.sessions.get(token);
    
    if (!session) {
      throw new Error('Invalid token');
    }
    
    // Generate new token
    const newToken = this.generateToken(session.user);
    
    // Remove old session
    this.sessions.delete(token);
    
    // Create new session
    this.sessions.set(newToken, {
      user: session.user,
      createdAt: new Date().toISOString(),
      expiresAt: new Date(Date.now() + 8 * 60 * 60 * 1000).toISOString()
    });
    
    return {
      access_token: newToken,
      token_type: 'Bearer',
      expires_in: 8 * 60 * 60,
      user: {
        id: session.user.id,
        username: session.user.username,
        role: session.user.role,
        profile: session.user.profile
      },
      permissions: session.user.permissions
    };
  }
  
  // Logout
  async logout(token) {
    await this.delay(100);
    
    this.sessions.delete(token);
    
    return { success: true };
  }
  
  // Generate JWT-like token (simplified for demo)
  generateToken(user) {
    const header = btoa(JSON.stringify({ alg: 'HS256', typ: 'JWT' }));
    const payload = btoa(JSON.stringify({
      sub: user.id,
      username: user.username,
      role: user.role,
      iat: Math.floor(Date.now() / 1000),
      exp: Math.floor(Date.now() / 1000) + (8 * 60 * 60)
    }));
    const signature = btoa(`demo_signature_${Date.now()}_${Math.random()}`);
    
    return `${header}.${payload}.${signature}`;
  }
  
  // Simulate network delay
  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
  
  // Get all users (for admin purposes)
  getUsers() {
    return Array.from(this.users.values()).map(user => ({
      id: user.id,
      username: user.username,
      role: user.role,
      profile: user.profile,
      permissions: user.permissions
    }));
  }
  
  // Get active sessions (for admin purposes)
  getActiveSessions() {
    return Array.from(this.sessions.entries()).map(([token, session]) => ({
      token: token.substring(0, 20) + '...',
      user: session.user.username,
      createdAt: session.createdAt,
      expiresAt: session.expiresAt
    }));
  }
}

// Global demo auth service instance
export const demoAuthService = new DemoAuthService();
export default DemoAuthService;
