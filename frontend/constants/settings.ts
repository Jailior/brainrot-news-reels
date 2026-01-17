export const SETTINGS_CONFIG = {
  analytics: [
    { id: 'feed-stats', label: 'Feed Statistics', icon: 'paperplane.fill' },
    { id: 'engagement', label: 'User Engagement', icon: 'house.fill' },
  ],
  general: [
    { id: 'account', label: 'Account', icon: 'house.fill' },
    { id: 'notifications', label: 'Notifications', icon: 'paperplane.fill' },
    { id: 'privacy', label: 'Privacy', icon: 'chevron.left.forwardslash.chevron.right' },
  ],
} as const;

export type SettingItem = {
  id: string;
  label: string;
  icon: string;
};
