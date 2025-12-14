"use client";

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useRouter } from 'next/navigation';
import apiClient from '../lib/api_client';
import { User } from '../types/user';
import { AuthResponse } from '../types/user';

interface AuthContextType {
  user: User | null;
  userId: number | null;
  signin: (email: string, password: string) => Promise<void>;
  signup: (email: string, password: string) => Promise<void>;
  signout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      apiClient.get('/auth/current_user')
        .then(response => {
          setUser(response.data);
        })
        .catch(() => {
          localStorage.removeItem('token');
        });
    }
  }, []);

  const signin = async (email: string, password: string) => {
    const response = await apiClient.post<AuthResponse>('/auth/signin', {
      email,
      password,
    });
    const { access_token } = response.data;
    localStorage.setItem('token', access_token);
    apiClient.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
    const userResponse = await apiClient.get('/auth/current_user');
    setUser(userResponse.data);
    router.push('/dashboard');
  };

  const signup = async (email: string, password: string) => {
    await apiClient.post('/auth/signup', { email, password });
    await signin(email, password);
  };

  const signout = async () => {
    setUser(null);
    localStorage.removeItem('token');
    delete apiClient.defaults.headers.common['Authorization'];
    router.push('/signin');
  };

  return (
    <AuthContext.Provider value={{ user, userId: user?.id || null, signin, signup, signout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
