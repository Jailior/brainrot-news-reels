import { Tabs, usePathname } from 'expo-router';
import React from 'react';

import { HapticTab } from '@/components/haptic-tab';
import { IconSymbol } from '@/components/ui/icon-symbol';
import { Colors } from '@/constants/theme';
import { useColorScheme } from '@/hooks/use-color-scheme';

export default function TabLayout() {
  const colorScheme = useColorScheme();
  const pathname = usePathname();

  const isProfileTab = pathname === '/profile';
  const isLightTheme = colorScheme === 'light';

  // White tab bar for light theme + profile tab, dark gray otherwise
  const tabBarBackgroundColor = isLightTheme && isProfileTab ? '#ffffff' : Colors.dark.background;

  const tabBarBorderColor = isLightTheme && isProfileTab ? '#e5e5e5' : '#2a2a2a';

  const tabBarActiveTintColor = isLightTheme && isProfileTab ? '#000000' : '#ffffff';

  const tabBarInactiveTintColor = isLightTheme && isProfileTab ? '#999999' : '#666666';

  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: tabBarActiveTintColor,
        tabBarInactiveTintColor: tabBarInactiveTintColor,
        headerShown: false,
        tabBarButton: HapticTab,
        tabBarStyle: {
          backgroundColor: tabBarBackgroundColor,
          borderTopColor: tabBarBorderColor,
        },
      }}
    >
      <Tabs.Screen
        name="index"
        options={{
          title: 'Home',
          tabBarIcon: ({ color }) => <IconSymbol size={28} name="house" color={color} />,
        }}
      />
      <Tabs.Screen
        name="profile"
        options={{
          title: 'Profile',
          tabBarIcon: ({ color }) => <IconSymbol size={28} name="person" color={color} />,
        }}
      />
    </Tabs>
  );
}
