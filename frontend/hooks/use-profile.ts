import { useRouter } from 'expo-router';
import { useCallback } from 'react';

export interface UserProfile {
  name: string;
  email: string;
  avatarUrl?: string;
}

export function useProfile() {
  const router = useRouter();

  // Mock user data - in a real app, this would come from an auth context or API
  const user: UserProfile = {
    name: 'User Name',
    email: 'user@example.com',
  };

  const navigateToSetting = useCallback(
    (label: string) => {
      router.push({
        pathname: '/settings-detail',
        params: { title: label },
      });
    },
    [router]
  );

  const logout = useCallback(() => {
    console.log('Logging out...');
    // Implement actual logout logic here
  }, []);

  return {
    user,
    navigateToSetting,
    logout,
  };
}
