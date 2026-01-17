import { StyleSheet, View, ScrollView, TouchableOpacity, Pressable } from 'react-native';
import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { IconSymbol } from '@/components/ui/icon-symbol';
import { Fonts } from '@/constants/theme';
import { useThemeColor } from '@/hooks/use-theme-color';
import { useProfile } from '@/hooks/use-profile';
import { SETTINGS_CONFIG, SettingItem } from '@/constants/settings';

export default function ProfileScreen() {
  const { user, navigateToSetting, logout } = useProfile();

  const borderColor = useThemeColor({}, 'icon');
  const secondaryBackgroundColor = useThemeColor(
    { light: '#f5f5f5', dark: '#1c1c1e' },
    'background'
  );
  const iconColor = useThemeColor({}, 'icon');

  const renderSettingItem = (item: SettingItem) => (
    <Pressable
      key={item.id}
      style={({ pressed }) => [
        styles.settingItem,
        pressed && { backgroundColor: borderColor + '10' },
      ]}
      onPress={() => navigateToSetting(item.label)}
    >
      <View style={styles.settingItemLeft}>
        <IconSymbol name={item.icon as any} size={22} color={iconColor} />
        <ThemedText style={styles.settingLabel}>{item.label}</ThemedText>
      </View>
      <IconSymbol name="chevron.right" size={20} color={iconColor} />
    </Pressable>
  );

  return (
    <ThemedView style={styles.container}>
      <ScrollView showsVerticalScrollIndicator={false} contentContainerStyle={styles.content}>
        <ThemedText type="title" style={styles.pageTitle}>
          Settings
        </ThemedText>

        {/* Profile Section */}
        <ThemedView style={[styles.profileCard, { backgroundColor: secondaryBackgroundColor }]}>
          <View style={styles.profileInfo}>
            <IconSymbol size={60} color={iconColor} name="person.crop.circle.fill" />
            <View style={styles.profileTextContainer}>
              <ThemedText type="subtitle">{user.name}</ThemedText>
              <ThemedText style={styles.emailText}>{user.email}</ThemedText>
            </View>
          </View>
        </ThemedView>

        {/* Analytics Section */}
        <View style={styles.section}>
          <ThemedText type="defaultSemiBold" style={styles.sectionTitle}>
            Analytics
          </ThemedText>
          <ThemedView
            style={[styles.sectionContent, { backgroundColor: secondaryBackgroundColor }]}
          >
            {SETTINGS_CONFIG.analytics.map((item, index) => (
              <View key={item.id}>
                {renderSettingItem(item)}
                {index < SETTINGS_CONFIG.analytics.length - 1 && (
                  <View style={[styles.separator, { backgroundColor: borderColor + '20' }]} />
                )}
              </View>
            ))}
          </ThemedView>
        </View>

        {/* Settings Section */}
        <View style={styles.section}>
          <ThemedText type="defaultSemiBold" style={styles.sectionTitle}>
            General Settings
          </ThemedText>
          <ThemedView
            style={[styles.sectionContent, { backgroundColor: secondaryBackgroundColor }]}
          >
            {SETTINGS_CONFIG.general.map((item, index) => (
              <View key={item.id}>
                {renderSettingItem(item)}
                {index < SETTINGS_CONFIG.general.length - 1 && (
                  <View style={[styles.separator, { backgroundColor: borderColor + '20' }]} />
                )}
              </View>
            ))}
          </ThemedView>
        </View>

        {/* Bottom Log Out Section */}
        <View style={styles.bottomSection}>
          <TouchableOpacity
            style={[styles.logoutButton, { backgroundColor: secondaryBackgroundColor }]}
            onPress={logout}
          >
            <ThemedText style={styles.logoutButtonText}>Log Out</ThemedText>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  content: {
    padding: 20,
    paddingTop: 60,
    paddingBottom: 40,
  },
  pageTitle: {
    marginBottom: 24,
    fontFamily: Fonts.rounded,
  },
  profileCard: {
    borderRadius: 16,
    padding: 16,
    marginBottom: 24,
  },
  profileInfo: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  profileTextContainer: {
    marginLeft: 16,
    justifyContent: 'center',
  },
  emailText: {
    fontSize: 14,
    marginTop: 2,
    opacity: 0.5,
  },
  section: {
    marginBottom: 24,
  },
  sectionTitle: {
    marginBottom: 8,
    marginLeft: 4,
    opacity: 0.6,
    fontSize: 13,
    textTransform: 'uppercase',
  },
  sectionContent: {
    borderRadius: 16,
    overflow: 'hidden',
  },
  settingItem: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: 16,
  },
  settingItemLeft: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  settingLabel: {
    marginLeft: 12,
    fontSize: 16,
  },
  separator: {
    height: 1,
    marginLeft: 50,
  },
  bottomSection: {
    marginTop: 12,
  },
  logoutButton: {
    borderRadius: 16,
    padding: 16,
    alignItems: 'center',
    justifyContent: 'center',
  },
  logoutButtonText: {
    color: '#FF3B30',
    fontSize: 16,
    fontWeight: '600',
  },
});
