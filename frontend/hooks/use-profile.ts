import { useRouter } from 'expo-router';
import { useCallback } from 'react';
import { useAuth } from '@/context/auth-context';

export function useProfile() {
  const router = useRouter();
  const { user, signOut } = useAuth();

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
    signOut();
  }, [signOut]);

  return {
    user,
    navigateToSetting,
    logout,
  };
}
