import React, { useState } from 'react';
import { StyleSheet, TextInput, TouchableOpacity, View } from 'react-native';
import { Link, useRouter } from 'expo-router';
import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { useAuth } from '@/context/auth-context';
import { useThemeColor } from '@/hooks/use-theme-color';
import { IconSymbol } from '@/components/ui/icon-symbol';

export default function SignUpScreen() {
  const router = useRouter();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { signUp, isLoading } = useAuth();

  const textColor = useThemeColor({}, 'text');
  const borderColor = useThemeColor({}, 'icon');
  const buttonBackground = useThemeColor({}, 'tint');
  const iconColor = useThemeColor({}, 'icon');

  const handleSignUp = async () => {
    if (name && email && password) {
      await signUp(name, email, password);
    }
  };

  return (
    <ThemedView style={styles.container}>
      <TouchableOpacity style={styles.backButton} onPress={() => router.back()}>
        <IconSymbol name="chevron.left" size={28} color={iconColor} />
      </TouchableOpacity>

      <View style={styles.content}>
        <ThemedText type="title" style={styles.title}>
          Create Account
        </ThemedText>
        <ThemedText style={styles.subtitle}>Join Brainrot News Reels today</ThemedText>

        <View style={styles.form}>
          <TextInput
            style={[styles.input, { color: textColor, borderColor: borderColor + '40' }]}
            placeholder="Full Name"
            placeholderTextColor={borderColor}
            value={name}
            onChangeText={setName}
          />
          <TextInput
            style={[styles.input, { color: textColor, borderColor: borderColor + '40' }]}
            placeholder="Email"
            placeholderTextColor={borderColor}
            value={email}
            onChangeText={setEmail}
            autoCapitalize="none"
            keyboardType="email-address"
          />
          <TextInput
            style={[styles.input, { color: textColor, borderColor: borderColor + '40' }]}
            placeholder="Password"
            placeholderTextColor={borderColor}
            value={password}
            onChangeText={setPassword}
            secureTextEntry
          />

          <TouchableOpacity
            style={[styles.button, { backgroundColor: buttonBackground }]}
            onPress={handleSignUp}
            disabled={isLoading}
          >
            <ThemedText style={styles.buttonText}>
              {isLoading ? 'Creating account...' : 'Sign Up'}
            </ThemedText>
          </TouchableOpacity>
        </View>

        <View style={styles.footer}>
          <ThemedText>Already have an account? </ThemedText>
          <Link href="/(auth)/login" asChild>
            <TouchableOpacity>
              <ThemedText style={{ color: buttonBackground, fontWeight: '600' }}>
                Sign In
              </ThemedText>
            </TouchableOpacity>
          </Link>
        </View>
      </View>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
  },
  backButton: {
    marginTop: 40,
    marginBottom: 20,
    marginLeft: -8,
    width: 44,
    height: 44,
    justifyContent: 'center',
    alignItems: 'center',
  },
  content: {
    flex: 1,
    width: '100%',
    justifyContent: 'center',
    paddingBottom: 40,
  },
  title: {
    marginBottom: 8,
  },
  subtitle: {
    marginBottom: 32,
    opacity: 0.6,
  },
  form: {
    gap: 16,
  },
  input: {
    height: 56,
    borderWidth: 1,
    borderRadius: 12,
    paddingHorizontal: 16,
    fontSize: 16,
  },
  button: {
    height: 56,
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 8,
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  footer: {
    flexDirection: 'row',
    justifyContent: 'center',
    marginTop: 24,
  },
});
