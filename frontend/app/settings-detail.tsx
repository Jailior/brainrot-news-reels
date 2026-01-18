import React, { useState, useEffect } from 'react';
import {
  StyleSheet,
  TouchableOpacity,
  TextInput,
  View,
  ScrollView,
  Modal,
  Alert,
} from 'react-native';
import { useRouter, useLocalSearchParams, Stack } from 'expo-router';

import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { IconSymbol } from '@/components/ui/icon-symbol';
import { useThemeColor } from '@/hooks/use-theme-color';
import { useAuth } from '@/context/auth-context';

const LANGUAGES = ['English', 'French', 'Spanish'];

export default function SettingsDetailScreen() {
  const router = useRouter();
  const { title } = useLocalSearchParams<{ title: string }>();
  const iconColor = useThemeColor({}, 'icon');
  const { user, updateProfile, deleteAccount, completeSetup, isLoading, error, clearError } =
    useAuth();

  const [name, setName] = useState(user?.name || '');
  const [selectedLanguage, setSelectedLanguage] = useState<string>(
    user?.preferences?.language || 'English'
  );
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showCurrentPassword, setShowCurrentPassword] = useState(false);
  const [showNewPassword, setShowNewPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [deleteConfirmText, setDeleteConfirmText] = useState('');

  // Sync name and language fields with user object
  useEffect(() => {
    if (user?.name !== undefined) {
      setName(user.name || '');
    }
    if (user?.preferences?.language) {
      setSelectedLanguage(user.preferences.language);
    }
  }, [user?.name, user?.preferences?.language]);

  const textColor = useThemeColor({}, 'text');
  const borderColor = useThemeColor({}, 'icon');
  const buttonBackground = useThemeColor({}, 'tint');
  const secondaryBackgroundColor = useThemeColor(
    { light: '#f5f5f5', dark: '#1c1c1e' },
    'background'
  );

  const handleInputChange = (setter: (value: string) => void) => (value: string) => {
    if (error) {
      clearError();
    }
    setter(value);
  };

  const handleUpdateProfile = async () => {
    if (!user) return;

    try {
      // Validate password fields if password is being changed
      if (newPassword) {
        if (!currentPassword) {
          Alert.alert('Error', 'Please enter your current password');
          return;
        }
        if (newPassword !== confirmPassword) {
          Alert.alert('Error', 'New passwords do not match');
          return;
        }
        if (newPassword.length < 6) {
          Alert.alert('Error', 'Password must be at least 6 characters');
          return;
        }
      }

      // Update language if changed
      if (user.preferences?.language !== selectedLanguage) {
        await completeSetup({
          categories: user.preferences?.categories || [],
          language: selectedLanguage,
        });
      }

      await updateProfile(
        name !== user.name ? name : undefined,
        newPassword || undefined,
        newPassword ? currentPassword : undefined
      );

      // Clear password fields on success
      setCurrentPassword('');
      setNewPassword('');
      setConfirmPassword('');

      Alert.alert('Success', 'Profile updated successfully');
    } catch (err) {
      // Error is handled by auth context
    }
  };

  const handleDeleteAccount = async () => {
    if (deleteConfirmText.toLowerCase() !== 'delete') {
      Alert.alert('Error', 'Please type "DELETE" to confirm');
      return;
    }

    try {
      await deleteAccount();
      setShowDeleteModal(false);
      setDeleteConfirmText('');
      // Navigation will be handled by auth context (user will be logged out)
    } catch (err) {
      // Error is handled by auth context
    }
  };

  const renderAccountForm = () => {
    if (!user) return null;

    return (
      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
        <ThemedView style={styles.content}>
          <ThemedText type="subtitle" style={styles.sectionTitle}>
            Profile Information
          </ThemedText>

          {error && (
            <ThemedText style={styles.errorText}>
              {error}
            </ThemedText>
          )}

          <View style={styles.form}>
            <ThemedText style={styles.label}>Name</ThemedText>
            <TextInput
              style={[
                styles.input,
                {
                  color: textColor,
                  borderColor: borderColor + '40',
                  backgroundColor: secondaryBackgroundColor,
                },
              ]}
              placeholder="Enter your name"
              placeholderTextColor={borderColor + '80'}
              value={name}
              onChangeText={handleInputChange(setName)}
            />

            <ThemedText style={[styles.label, styles.sectionSpacing]}>Language</ThemedText>
            <View style={styles.languageContainer}>
              {LANGUAGES.map((language) => (
                <TouchableOpacity
                  key={language}
                  onPress={() => setSelectedLanguage(language)}
                  style={[
                    styles.languageCard,
                    {
                      backgroundColor: secondaryBackgroundColor,
                      borderColor: selectedLanguage === language ? buttonBackground : 'transparent',
                      borderWidth: 2,
                    },
                  ]}
                >
                  <ThemedText style={styles.languageText}>{language}</ThemedText>
                  {selectedLanguage === language && (
                    <IconSymbol name="checkmark.circle.fill" size={20} color={buttonBackground} />
                  )}
                </TouchableOpacity>
              ))}
            </View>

            <ThemedText style={[styles.label, styles.sectionSpacing]}>
              Change Password
            </ThemedText>
            <View style={styles.passwordContainer}>
              <TextInput
                style={[
                  styles.input,
                  styles.passwordInput,
                  {
                    color: textColor,
                    borderColor: borderColor + '40',
                    backgroundColor: secondaryBackgroundColor,
                  },
                ]}
                placeholder="Current password"
                placeholderTextColor={borderColor + '80'}
                value={currentPassword}
                onChangeText={handleInputChange(setCurrentPassword)}
                secureTextEntry={!showCurrentPassword}
              />
              <TouchableOpacity
                style={styles.eyeIcon}
                onPress={() => setShowCurrentPassword(!showCurrentPassword)}
              >
                <IconSymbol
                  name={showCurrentPassword ? 'eye.slash' : 'eye'}
                  size={20}
                  color={iconColor}
                />
              </TouchableOpacity>
            </View>
            <View style={styles.passwordContainer}>
              <TextInput
                style={[
                  styles.input,
                  styles.passwordInput,
                  {
                    color: textColor,
                    borderColor: borderColor + '40',
                    backgroundColor: secondaryBackgroundColor,
                  },
                ]}
                placeholder="New password"
                placeholderTextColor={borderColor + '80'}
                value={newPassword}
                onChangeText={handleInputChange(setNewPassword)}
                secureTextEntry={!showNewPassword}
              />
              <TouchableOpacity
                style={styles.eyeIcon}
                onPress={() => setShowNewPassword(!showNewPassword)}
              >
                <IconSymbol
                  name={showNewPassword ? 'eye.slash' : 'eye'}
                  size={20}
                  color={iconColor}
                />
              </TouchableOpacity>
            </View>
            <View style={styles.passwordContainer}>
              <TextInput
                style={[
                  styles.input,
                  styles.passwordInput,
                  {
                    color: textColor,
                    borderColor: borderColor + '40',
                    backgroundColor: secondaryBackgroundColor,
                  },
                ]}
                placeholder="Confirm new password"
                placeholderTextColor={borderColor + '80'}
                value={confirmPassword}
                onChangeText={handleInputChange(setConfirmPassword)}
                secureTextEntry={!showConfirmPassword}
              />
              <TouchableOpacity
                style={styles.eyeIcon}
                onPress={() => setShowConfirmPassword(!showConfirmPassword)}
              >
                <IconSymbol
                  name={showConfirmPassword ? 'eye.slash' : 'eye'}
                  size={20}
                  color={iconColor}
                />
              </TouchableOpacity>
            </View>

            <TouchableOpacity
              style={[
                styles.button,
                { backgroundColor: buttonBackground },
                isLoading && styles.buttonDisabled,
              ]}
              onPress={handleUpdateProfile}
              disabled={isLoading}
            >
              <ThemedText style={styles.buttonText}>
                {isLoading ? 'Updating...' : 'Update Profile'}
              </ThemedText>
            </TouchableOpacity>
          </View>

          <View style={styles.deleteSection}>
            <ThemedText type="subtitle" style={styles.dangerSectionTitle}>
              Danger Zone
            </ThemedText>
            <ThemedText style={styles.dangerDescription}>
              Once you delete your account, there is no going back. Please be certain.
            </ThemedText>
            <TouchableOpacity
              style={[styles.deleteButton, { backgroundColor: secondaryBackgroundColor }]}
              onPress={() => setShowDeleteModal(true)}
            >
              <ThemedText style={styles.deleteButtonText}>Delete Account</ThemedText>
            </TouchableOpacity>
          </View>
        </ThemedView>

        {/* Delete Confirmation Modal */}
        <Modal
          visible={showDeleteModal}
          transparent
          animationType="fade"
          onRequestClose={() => setShowDeleteModal(false)}
        >
          <View style={styles.modalOverlay}>
            <ThemedView style={[styles.modalContent, { backgroundColor: secondaryBackgroundColor }]}>
              <ThemedText type="subtitle" style={styles.modalTitle}>
                Delete Account
              </ThemedText>
              <ThemedText style={styles.modalText}>
                This action cannot be undone. This will permanently delete your account and all
                associated data.
              </ThemedText>
              <ThemedText style={styles.modalText}>
                Type <ThemedText style={styles.boldText}>DELETE</ThemedText> to confirm:
              </ThemedText>
              <TextInput
                style={[
                  styles.modalInput,
                  {
                    color: textColor,
                    borderColor: borderColor + '40',
                    backgroundColor: secondaryBackgroundColor,
                  },
                ]}
                placeholder="Type DELETE to confirm"
                placeholderTextColor={borderColor + '80'}
                value={deleteConfirmText}
                onChangeText={setDeleteConfirmText}
                autoCapitalize="characters"
              />
              {error && (
                <ThemedText style={styles.errorText}>{error}</ThemedText>
              )}
              <View style={styles.modalButtons}>
                <TouchableOpacity
                  style={[styles.modalButton, styles.modalButtonCancel]}
                  onPress={() => {
                    setShowDeleteModal(false);
                    setDeleteConfirmText('');
                    clearError();
                  }}
                >
                  <ThemedText style={styles.modalButtonTextCancel}>Cancel</ThemedText>
                </TouchableOpacity>
                <TouchableOpacity
                  style={[
                    styles.modalButton,
                    styles.modalButtonDelete,
                    (deleteConfirmText.toLowerCase() !== 'delete' || isLoading) &&
                      styles.modalButtonDisabled,
                  ]}
                  onPress={handleDeleteAccount}
                  disabled={deleteConfirmText.toLowerCase() !== 'delete' || isLoading}
                >
                  <ThemedText style={styles.modalButtonTextDelete}>
                    {isLoading ? 'Deleting...' : 'Delete Account'}
                  </ThemedText>
                </TouchableOpacity>
              </View>
            </ThemedView>
          </View>
        </Modal>
      </ScrollView>
    );
  };

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
      {title === 'Account' ? (
        renderAccountForm()
      ) : (
        <ThemedView style={styles.content}>
          <ThemedText type="subtitle">This is the {title} page</ThemedText>
          <ThemedText style={styles.placeholderText}>
            This is a placeholder for the {title} settings and functionality.
          </ThemedText>
        </ThemedView>
      )}
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    flexGrow: 1,
    paddingBottom: 40,
  },
  content: {
    padding: 20,
    paddingTop: 20,
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
  sectionTitle: {
    marginBottom: 20,
  },
  form: {
    gap: 12,
  },
  label: {
    fontSize: 14,
    fontWeight: '600',
    marginBottom: 8,
    opacity: 0.8,
  },
  sectionSpacing: {
    marginTop: 24,
  },
  input: {
    height: 56,
    borderWidth: 1,
    borderRadius: 12,
    paddingHorizontal: 16,
    fontSize: 16,
    marginBottom: 4,
  },
  passwordContainer: {
    position: 'relative',
    marginBottom: 4,
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
  languageContainer: {
    gap: 12,
    marginBottom: 4,
  },
  languageCard: {
    padding: 16,
    borderRadius: 12,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  languageText: {
    fontSize: 16,
    fontWeight: '500',
  },
  button: {
    height: 56,
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 8,
  },
  buttonDisabled: {
    opacity: 0.6,
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  errorText: {
    color: '#ff4444',
    fontSize: 14,
    marginBottom: 16,
  },
  deleteSection: {
    marginTop: 48,
    paddingTop: 24,
    borderTopWidth: 1,
    borderTopColor: 'rgba(128, 128, 128, 0.2)',
  },
  dangerSectionTitle: {
    color: '#ff4444',
    marginBottom: 8,
  },
  dangerDescription: {
    fontSize: 14,
    opacity: 0.7,
    marginBottom: 16,
  },
  deleteButton: {
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 1,
    borderColor: '#ff4444',
  },
  deleteButtonText: {
    color: '#ff4444',
    fontSize: 16,
    fontWeight: '600',
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  modalContent: {
    borderRadius: 16,
    padding: 24,
    width: '100%',
    maxWidth: 400,
  },
  modalTitle: {
    marginBottom: 16,
    color: '#ff4444',
  },
  modalText: {
    fontSize: 14,
    marginBottom: 12,
    opacity: 0.8,
  },
  boldText: {
    fontWeight: '700',
  },
  modalInput: {
    height: 48,
    borderWidth: 1,
    borderRadius: 8,
    paddingHorizontal: 12,
    fontSize: 16,
    marginTop: 8,
    marginBottom: 16,
  },
  modalButtons: {
    flexDirection: 'row',
    gap: 12,
    marginTop: 8,
  },
  modalButton: {
    flex: 1,
    height: 48,
    borderRadius: 8,
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalButtonCancel: {
    backgroundColor: 'rgba(128, 128, 128, 0.2)',
  },
  modalButtonDelete: {
    backgroundColor: '#ff4444',
  },
  modalButtonDisabled: {
    opacity: 0.5,
  },
  modalButtonTextCancel: {
    fontSize: 16,
    fontWeight: '600',
  },
  modalButtonTextDelete: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
});
