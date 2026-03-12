import { useState, useEffect, useCallback } from 'react';

interface User {
  id: string;
  name: string;
  email: string;
  hardware_background?: string;
  software_background?: string;
  learning_goal?: string;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isLoading: boolean;
}

const API_URL = 'http://localhost:8000';
const STORAGE_KEY = 'textbook_auth';

function getStoredAuth(): { user: User; token: string } | null {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) return JSON.parse(stored);
  } catch {}
  return null;
}

function storeAuth(user: User, token: string) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify({ user, token }));
}

function clearAuth() {
  localStorage.removeItem(STORAGE_KEY);
}

export function useAuth() {
  const [state, setState] = useState<AuthState>({
    user: null,
    token: null,
    isLoading: true,
  });

  useEffect(() => {
    const stored = getStoredAuth();
    if (stored) {
      setState({ user: stored.user, token: stored.token, isLoading: false });
    } else {
      setState(prev => ({ ...prev, isLoading: false }));
    }
  }, []);

  const signUp = useCallback(async (data: {
    name: string;
    email: string;
    password: string;
    hardware_background: string;
    software_background: string;
    learning_goal?: string;
  }) => {
    const response = await fetch(`${API_URL}/users/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: data.name,
        email: data.email,
        hardware_background: data.hardware_background,
        software_background: data.software_background,
      }),
    });

    if (!response.ok) {
      const err = await response.json().catch(() => ({ detail: 'Registration failed' }));
      throw new Error(err.detail || 'Registration failed');
    }

    const user = await response.json();
    // For MVP, use user ID as a simple token (better-auth integration later)
    const token = String(user.id);
    storeAuth(user, token);
    setState({ user, token, isLoading: false });
    return user;
  }, []);

  const signIn = useCallback(async (email: string, _password: string) => {
    // For MVP: look up user by email via a custom endpoint
    // In production, better-auth handles session tokens
    const response = await fetch(`${API_URL}/users/lookup?email=${encodeURIComponent(email)}`);
    if (!response.ok) {
      throw new Error('Invalid credentials');
    }
    const user = await response.json();
    const token = String(user.id);
    storeAuth(user, token);
    setState({ user, token, isLoading: false });
    return user;
  }, []);

  const signOut = useCallback(() => {
    clearAuth();
    setState({ user: null, token: null, isLoading: false });
  }, []);

  return {
    user: state.user,
    token: state.token,
    session: state.token ? { token: state.token } : null,
    isLoading: state.isLoading,
    isAuthenticated: !!state.user,
    signUp,
    signIn,
    signOut,
  };
}
