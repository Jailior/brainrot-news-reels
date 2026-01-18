import React, { useState } from 'react';
import { StyleSheet, TextInput, TouchableOpacity, View } from 'react-native';
import { Link, useRouter } from 'expo-router';
import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { useAuth } from '@/context/auth-context';
import { useThemeColor } from '@/hooks/use-theme-color';
import { IconSymbol } from '@/components/ui/icon-symbol';

export default function LoginScreen() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const { signIn, isLoading, error, clearError } = useAuth();

  const textColor = useThemeColor({}, 'text');
  const borderColor = useThemeColor({}, 'icon');
  const buttonBackground = useThemeColor({}, 'tint');
  const iconColor = useThemeColor({}, 'icon');

  const handleLogin = async () => {
    if (email && password) {
      try {
        await signIn(email, password);
      } catch {
        // Error is handled by auth context and displayed below
      }
    }
  };

  const handleInputChange = (setter: (value: string) => void) => (value: string) => {
    // Clear error when user starts typing
    if (error) {
      clearError();
    }
    setter(value);
  };

  return (
    <ThemedView style={styles.container}>
      <TouchableOpacity style={styles.backButton} onPress={() => router.push('/(auth)/signup')}>
        <IconSymbol name="chevron.left" size={28} color={iconColor} />
      </TouchableOpacity>
      <View style={styles.content}>
        <ThemedText type="title" style={styles.title}>
          Welcome Back
        </ThemedText>
        <ThemedText style={styles.subtitle}>Sign in to continue</ThemedText>

        {/* Error Text */}
        {error && <ThemedText style={styles.errorText}>Invalid email or password</ThemedText>}

        <View style={styles.form}>
          <TextInput
            style={[
              styles.input,
              {
                color: textColor,
                borderColor: error ? '#ff4444' : borderColor + '40',
                borderWidth: error ? 2 : 1,
                backgroundColor: error ? '#fff5f5' : 'transparent',
              },
            ]}
            placeholder="Email"
            placeholderTextColor={borderColor}
            value={email}
            onChangeText={handleInputChange(setEmail)}
            autoCapitalize="none"
            keyboardType="email-address"
          />
          <View style={styles.passwordContainer}>
            <TextInput
              style={[
                styles.input,
                styles.passwordInput,
                {
                  color: textColor,
                  borderColor: error ? '#ff4444' : borderColor + '40',
                  borderWidth: error ? 2 : 1,
                  backgroundColor: error ? '#fff5f5' : 'transparent',
                },
              ]}
              placeholder="Password"
              placeholderTextColor={borderColor}
              value={password}
              onChangeText={handleInputChange(setPassword)}
              secureTextEntry={!showPassword}
            />
            <TouchableOpacity style={styles.eyeIcon} onPress={() => setShowPassword(!showPassword)}>
              <IconSymbol name={showPassword ? 'eye.slash' : 'eye'} size={20} color={iconColor} />
            </TouchableOpacity>
          </View>

          <TouchableOpacity
            style={[styles.button, { backgroundColor: buttonBackground }]}
            onPress={handleLogin}
            disabled={isLoading}
          >
            <ThemedText style={styles.buttonText}>
              {isLoading ? 'Signing in...' : 'Sign In'}
            </ThemedText>
          </TouchableOpacity>
        </View>

        <View style={styles.footer}>
          <ThemedText>Don&apos;t have an account? </ThemedText>
          <Link href="/(auth)/signup" asChild>
            <TouchableOpacity>
              <ThemedText style={{ color: buttonBackground, fontWeight: '600' }}>
                Sign Up
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
    justifyContent: 'center',
  },
  backButton: {
    position: 'absolute',
    top: 40,
    left: 12,
    width: 44,
    height: 44,
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 1,
  },
  content: {
    width: '100%',
  },
  title: {
    marginBottom: 8,
  },
  subtitle: {
    marginBottom: 32,
    opacity: 0.6,
  },
  errorText: {
    color: '#ff4444',
    fontSize: 14,
    marginBottom: 16,
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
  passwordContainer: {
    position: 'relative',
  },
  passwordInput: {
    paddingRight: 50,
  },
  eyeIcon: {
    position: 'absolute',
    right: 16,
    top: 18,
    padding: 4,
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
