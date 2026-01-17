import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';

export interface User {
  id: string;
  name: string;
  email: string;
  hasCompletedSetup: boolean;
  preferences?: {
    categories: string[];
    videoStyle: string;
  };
}

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  tempPreferences: User['preferences'] | null;
  signIn: (email: string, password: string) => Promise<void>;
  signUp: (name: string, email: string, password: string) => Promise<void>;
  signOut: () => void;
  setPreferences: (preferences: User['preferences']) => void;
  completeSetup: (preferences: User['preferences']) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [tempPreferences, setTempPreferences] = useState<User['preferences'] | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Mock persistence check
  useEffect(() => {
    // In a real app, we would check for a stored token
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 1000);
    return () => clearTimeout(timer);
  }, []);

  const signIn = useCallback(async (email: string, _password: string) => {
    setIsLoading(true);
    // Rudimentary mock sign in
    setTimeout(() => {
      setUser({
        id: '1',
        name: 'John Doe',
        email: email,
        hasCompletedSetup: true, // Existing users likely finished setup
      });
      setIsLoading(false);
    }, 1000);
  }, []);

  const signUp = useCallback(
    async (name: string, email: string, _password: string) => {
      setIsLoading(true);
      // Rudimentary mock sign up
      setTimeout(() => {
        setUser({
          id: '2',
          name: name,
          email: email,
          hasCompletedSetup: !!tempPreferences, // Setup is complete if they just came from setup screen
          preferences: tempPreferences || undefined,
        });
        setTempPreferences(null);
        setIsLoading(false);
      }, 1000);
    },
    [tempPreferences]
  );

  const signOut = useCallback(() => {
    setUser(null);
    setTempPreferences(null);
  }, []);

  const setPreferences = useCallback((preferences: User['preferences']) => {
    setTempPreferences(preferences);
  }, []);

  const completeSetup = useCallback(async (preferences: User['preferences']) => {
    setIsLoading(true);
    // Mock update setup status
    setTimeout(() => {
      setUser((prev) => (prev ? { ...prev, hasCompletedSetup: true, preferences } : null));
      setIsLoading(false);
    }, 1000);
  }, []);

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        tempPreferences,
        signIn,
        signUp,
        signOut,
        setPreferences,
        completeSetup,
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
