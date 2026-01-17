import { StyleSheet, TouchableOpacity } from 'react-native';
import { useRouter, useLocalSearchParams, Stack } from 'expo-router';

import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { IconSymbol } from '@/components/ui/icon-symbol';
import { useThemeColor } from '@/hooks/use-theme-color';

export default function SettingsDetailScreen() {
  const router = useRouter();
  const { title } = useLocalSearchParams<{ title: string }>();
  const iconColor = useThemeColor({}, 'icon');

  return (
    <ThemedView style={styles.container}>
      <Stack.Screen
        options={{
          title: title || 'Settings',
          headerShown: true,
          headerLeft: () => (
            <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
              <IconSymbol name="chevron.left" size={24} color={iconColor} />
            </TouchableOpacity>
          ),
        }}
      />
      <ThemedView style={styles.content}>
        <ThemedText type="subtitle">This is the {title} page</ThemedText>
        <ThemedText style={styles.placeholderText}>
          This is a placeholder for the {title} settings and functionality.
        </ThemedText>
      </ThemedView>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  content: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  backButton: {
    padding: 8,
    marginLeft: -8,
  },
  placeholderText: {
    marginTop: 12,
    textAlign: 'center',
    opacity: 0.6,
  },
});
