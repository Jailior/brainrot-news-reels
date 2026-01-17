import { StyleSheet, View, Text, ScrollView } from 'react-native';
import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { IconSymbol } from '@/components/ui/icon-symbol';
import { Fonts } from '@/constants/theme';

export default function ProfileScreen() {
  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <ThemedView style={styles.header}>
        <IconSymbol
          size={120}
          color="#808080"
          name="person.crop.circle.fill"
        />
        <ThemedText type="title" style={styles.title}>Profile</ThemedText>
      </ThemedView>

      <ThemedView style={styles.section}>
        <ThemedText type="subtitle">About Brainrot News</ThemedText>
        <ThemedText style={styles.text}>
          Welcome to your personalized feed of trending news and viral moments. 
          Scroll through to stay updated with the latest in the digital world.
        </ThemedText>
      </ThemedView>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
  },
  content: {
    padding: 24,
    paddingTop: 60,
  },
  header: {
    alignItems: 'center',
    marginBottom: 32,
    backgroundColor: 'transparent',
  },
  title: {
    marginTop: 16,
    fontFamily: Fonts.rounded,
    color: '#fff',
  },
  section: {
    backgroundColor: '#111',
    padding: 20,
    borderRadius: 16,
  },
  text: {
    marginTop: 8,
    color: 'rgba(255, 255, 255, 0.7)',
    lineHeight: 22,
  },
});
