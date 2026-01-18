import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import * as api from '@/utils/api';

export interface User {
  id: string;
  name: string;
  email: string;
  hasCompletedSetup: boolean;
  preferences?: {
    categories: string[];
    language: string;
  };
}

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  error: string | null;
  tempPreferences: User['preferences'] | null;
  signIn: (email: string, password: string) => Promise<void>;
  signUp: (name: string, email: string, password: string) => Promise<void>;
  signOut: () => void;
  setPreferences: (preferences: User['preferences']) => void;
  completeSetup: (preferences: User['preferences']) => Promise<void>;
  loginAsGuest: () => Promise<void>;
  clearError: () => void;
  updateProfile: (name?: string, password?: string, currentPassword?: string) => Promise<void>;
  deleteAccount: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Convert API user to frontend User type
function mapApiUser(apiUser: api.User): User {
  return {
    id: apiUser.id.toString(),
    name: apiUser.name || '',
    email: apiUser.email,
    hasCompletedSetup: apiUser.has_completed_setup,
    preferences: apiUser.preferences
      ? {
          categories: apiUser.preferences.categories || [],
          language: apiUser.preferences.language || 'English',
        }
      : undefined,
  };
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [tempPreferences, setTempPreferences] = useState<User['preferences'] | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Check for existing user on app start
  useEffect(() => {
    async function loadUser() {
      try {
        const userId = await api.getUserId();
        if (userId) {
          const apiUser = await api.getCurrentUser(userId);
          setUser(mapApiUser(apiUser));
        }
      } catch {
        // User not found or other error - clear stored ID
        await api.clearUserId();
        console.log('No stored user found, starting fresh');
      } finally {
        setIsLoading(false);
      }
    }
    loadUser();
  }, []);

  const signIn = useCallback(async (email: string, password: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const apiUser = await api.login(email, password);
      setUser(mapApiUser(apiUser));
    } catch (err) {
      const message = err instanceof api.ApiError ? err.message : 'Login failed';
      setError(message);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const signUp = useCallback(
    async (name: string, email: string, password: string) => {
      setIsLoading(true);
      setError(null);
      try {
        const apiUser = await api.signup(name, email, password);

        // If we have temp preferences from setup screen, apply them
        if (tempPreferences) {
          const updatedUser = await api.updateSetup(apiUser.id, tempPreferences);
          setUser(mapApiUser(updatedUser));
          setTempPreferences(null);
        } else {
          setUser(mapApiUser(apiUser));
        }
      } catch (err) {
        const message = err instanceof api.ApiError ? err.message : 'Signup failed';
        setError(message);
        throw err;
      } finally {
        setIsLoading(false);
      }
    },
    [tempPreferences]
  );

  const signOut = useCallback(async () => {
    await api.logout();
    setUser(null);
    setTempPreferences(null);
    setError(null);
  }, []);

  const setPreferences = useCallback((preferences: User['preferences']) => {
    setTempPreferences(preferences);
  }, []);

  const completeSetup = useCallback(
    async (preferences: User['preferences']) => {
      if (!user || !preferences) return;

      setIsLoading(true);
      setError(null);
      try {
        const apiUser = await api.updateSetup(parseInt(user.id, 10), preferences);
        setUser(mapApiUser(apiUser));
      } catch (err) {
        const message = err instanceof api.ApiError ? err.message : 'Setup failed';
        setError(message);
        throw err;
      } finally {
        setIsLoading(false);
      }
    },
    [user]
  );

  const loginAsGuest = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const apiUser = await api.login(api.GUEST_CREDENTIALS.email, api.GUEST_CREDENTIALS.password);
      setUser(mapApiUser(apiUser));
    } catch (err) {
      const message = err instanceof api.ApiError ? err.message : 'Guest login failed';
      setError(message);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  const updateProfile = useCallback(
    async (name?: string, password?: string, currentPassword?: string) => {
      if (!user) return;

      setIsLoading(true);
      setError(null);
      try {
        const updateData: api.UpdateProfileRequest = {
          user_id: parseInt(user.id, 10),
        };
        if (name !== undefined) updateData.name = name;
        if (password) {
          updateData.password = password;
          if (currentPassword) {
            updateData.current_password = currentPassword;
          }
        }

        const apiUser = await api.updateProfile(updateData);
        setUser(mapApiUser(apiUser));
      } catch (err) {
        const message = err instanceof api.ApiError ? err.message : 'Profile update failed';
        setError(message);
        throw err;
      } finally {
        setIsLoading(false);
      }
    },
    [user]
  );

  const deleteAccount = useCallback(async () => {
    if (!user) return;

    setIsLoading(true);
    setError(null);
    try {
      await api.deleteAccount({ user_id: parseInt(user.id, 10) });
      setUser(null);
      setTempPreferences(null);
      setError(null);
    } catch (err) {
      const message = err instanceof api.ApiError ? err.message : 'Account deletion failed';
      setError(message);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [user]);

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        error,
        tempPreferences,
        signIn,
        signUp,
        signOut,
        setPreferences,
        completeSetup,
        loginAsGuest,
        clearError,
        updateProfile,
        deleteAccount,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
