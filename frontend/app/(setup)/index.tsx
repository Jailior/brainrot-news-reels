import { useRouter } from 'expo-router';
import React, { useState } from 'react';
import { StyleSheet, TouchableOpacity, View, ScrollView } from 'react-native';
import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { useAuth } from '@/context/auth-context';
import { useThemeColor } from '@/hooks/use-theme-color';
import { IconSymbol } from '@/components/ui/icon-symbol';

const CATEGORIES = ['Business', 'Entertainment', 'Health', 'Science', 'Sports', 'Technology'];
const LANGUAGES = ['English', 'French', 'Spanish'];

export default function SetupScreen() {
  const router = useRouter();
  const { user, completeSetup, setPreferences, isLoading } = useAuth();
  const [selectedCategories, setSelectedCategories] = useState<string[]>([]);
  const [selectedLanguage, setSelectedLanguage] = useState<string>('English');

  const buttonBackground = useThemeColor({}, 'tint');
  const cardBackground = useThemeColor({ light: '#f5f5f5', dark: '#1c1c1e' }, 'background');
  const textColor = useThemeColor({}, 'text');

  const toggleCategory = (category: string) => {
    setSelectedCategories((prev) =>
      prev.includes(category) ? prev.filter((c) => c !== category) : [...prev, category]
    );
  };

  const handleComplete = async () => {
    if (selectedCategories.length > 0 && selectedLanguage) {
      const preferences = {
        categories: selectedCategories,
        language: selectedLanguage,
      };

      if (user) {
        await completeSetup(preferences);
      } else {
        // Store preferences temporarily and go to signup
        setPreferences(preferences);
        router.push('/(auth)/signup');
      }
    }
  };

  return (
    <ThemedView style={styles.container}>
      <ScrollView contentContainerStyle={styles.content}>
        <ThemedText type="title" style={styles.title}>
          Welcome!
        </ThemedText>
        <ThemedText style={styles.subtitle}>Let&apos;s customize your news experience.</ThemedText>

        <View style={styles.section}>
          <ThemedText type="subtitle" style={styles.sectionTitle}>
            What news interests you?
          </ThemedText>
          <View style={styles.chipContainer}>
            {CATEGORIES.map((category) => (
              <TouchableOpacity
                key={category}
                onPress={() => toggleCategory(category)}
                style={[
                  styles.chip,
                  {
                    backgroundColor: selectedCategories.includes(category)
                      ? buttonBackground
                      : cardBackground,
                  },
                ]}
              >
                <ThemedText
                  style={[
                    styles.chipText,
                    { color: selectedCategories.includes(category) ? '#fff' : textColor },
                  ]}
                >
                  {category}
                </ThemedText>
              </TouchableOpacity>
            ))}
          </View>
        </View>

        <View style={styles.section}>
          <ThemedText type="subtitle" style={styles.sectionTitle}>
            Choose your language
          </ThemedText>
          <View style={styles.styleContainer}>
            {LANGUAGES.map((language) => (
              <TouchableOpacity
                key={language}
                onPress={() => setSelectedLanguage(language)}
                style={[
                  styles.styleCard,
                  {
                    backgroundColor: cardBackground,
                    borderColor: selectedLanguage === language ? buttonBackground : 'transparent',
                    borderWidth: 2,
                  },
                ]}
              >
                <ThemedText style={styles.styleText}>{language}</ThemedText>
                {selectedLanguage === language && (
                  <IconSymbol name="checkmark.circle.fill" size={20} color={buttonBackground} />
                )}
              </TouchableOpacity>
            ))}
          </View>
        </View>

        <TouchableOpacity
          style={[
            styles.finishButton,
            {
              backgroundColor: buttonBackground,
              opacity: selectedCategories.length > 0 && selectedLanguage ? 1 : 0.5,
            },
          ]}
          onPress={handleComplete}
          disabled={isLoading || !(selectedCategories.length > 0 && selectedLanguage)}
        >
          <ThemedText style={styles.finishButtonText}>
            {isLoading ? 'Saving...' : 'Start Watching'}
          </ThemedText>
        </TouchableOpacity>

        {!user && (
          <View style={styles.loginFooter}>
            <ThemedText>Already have an account? </ThemedText>
            <TouchableOpacity onPress={() => router.push('/(auth)/login')}>
              <ThemedText style={{ color: buttonBackground, fontWeight: '600' }}>Log In</ThemedText>
            </TouchableOpacity>
          </View>
        )}
      </ScrollView>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  content: {
    padding: 24,
    paddingTop: 80,
    paddingBottom: 40,
  },
  title: {
    marginBottom: 8,
  },
  subtitle: {
    marginBottom: 40,
    opacity: 0.6,
    fontSize: 16,
  },
  section: {
    marginBottom: 32,
  },
  sectionTitle: {
    marginBottom: 16,
    fontSize: 18,
  },
  chipContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 10,
  },
  chip: {
    paddingHorizontal: 16,
    paddingVertical: 10,
    borderRadius: 20,
  },
  chipText: {
    fontSize: 14,
    fontWeight: '500',
  },
  styleContainer: {
    gap: 12,
  },
  styleCard: {
    padding: 16,
    borderRadius: 12,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  styleText: {
    fontSize: 16,
    fontWeight: '500',
  },
  finishButton: {
    height: 56,
    borderRadius: 16,
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 20,
  },
  finishButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
  },
  loginFooter: {
    flexDirection: 'row',
    justifyContent: 'center',
    marginTop: 24,
  },
});
