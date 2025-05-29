import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { User, AuthResponse, UserCreate, UserLogin } from '../types/user';

interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (userData: UserLogin) => Promise<void>;
  register: (userData: UserCreate) => Promise<void>;
  logout: () => void;
  isLoading: boolean;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

const API_BASE_URL = 'http://localhost:8000/api';

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // アプリ起動時にローカルストレージからトークンを復元
    const savedToken = localStorage.getItem('auth_token');
    const savedUser = localStorage.getItem('auth_user');
    
    if (savedToken && savedUser) {
      setToken(savedToken);
      setUser(JSON.parse(savedUser));
      // トークンが有効かサーバーに確認
      validateToken(savedToken);
    } else {
      setIsLoading(false);
    }
  }, []);

  const validateToken = async (authToken: string) => {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/me`, {
        headers: {
          'Authorization': `Bearer ${authToken}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
      } else {
        // トークンが無効な場合はクリア
        logout();
      }
    } catch (error) {
      console.error('Token validation failed:', error);
      logout();
    } finally {
      setIsLoading(false);
    }
  };

  const login = async (userData: UserLogin) => {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'ログインに失敗しました');
      }

      const authData: AuthResponse = await response.json();
      setUser(authData.user);
      setToken(authData.access_token);
      
      // ローカルストレージに保存
      localStorage.setItem('auth_token', authData.access_token);
      localStorage.setItem('auth_user', JSON.stringify(authData.user));
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    }
  };

  const register = async (userData: UserCreate) => {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'ユーザー登録に失敗しました');
      }

      const authData: AuthResponse = await response.json();
      setUser(authData.user);
      setToken(authData.access_token);
      
      // ローカルストレージに保存
      localStorage.setItem('auth_token', authData.access_token);
      localStorage.setItem('auth_user', JSON.stringify(authData.user));
    } catch (error) {
      console.error('Registration failed:', error);
      throw error;
    }
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('auth_token');
    localStorage.removeItem('auth_user');
  };

  const value: AuthContextType = {
    user,
    token,
    login,
    register,
    logout,
    isLoading,
    isAuthenticated: !!user && !!token,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};