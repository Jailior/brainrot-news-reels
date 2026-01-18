/**
 * App configuration utilities.
 * Reads environment variables and provides typed config values.
 */

/**
 * Check if the app is running in demo mode.
 * In demo mode:
 * - Videos are loaded from local assets/demo/ folder
 * - Watch history is stored locally in AsyncStorage
 * - No API calls are made for reels
 */
export function isDemoMode(): boolean {
  const demoMode = process.env.EXPO_PUBLIC_DEMO_MODE;

  // Log for debugging - remove in production
  if (__DEV__) {
    console.log(`[Config] EXPO_PUBLIC_DEMO_MODE = "${demoMode}"`);
    console.log(`[Config] isDemoMode = ${demoMode === 'true' || demoMode === '1'}`);
  }

  return demoMode === 'true' || demoMode === '1';
}

/**
 * App configuration object
 */
export const config = {
  isDemoMode: isDemoMode(),
} as const;
