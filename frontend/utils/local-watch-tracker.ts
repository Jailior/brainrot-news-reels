/**
 * Local watch tracking for demo mode.
 * Uses AsyncStorage to persist which reels have been watched locally.
 */

import AsyncStorage from '@react-native-async-storage/async-storage';

const WATCHED_REELS_KEY = 'brainrot_demo_watched_reels';

/**
 * Get the set of watched reel IDs from local storage.
 */
export async function getWatchedReelIds(): Promise<Set<string>> {
  try {
    const data = await AsyncStorage.getItem(WATCHED_REELS_KEY);
    if (data) {
      const ids: string[] = JSON.parse(data);
      return new Set(ids);
    }
  } catch (error) {
    console.error('[LocalWatchTracker] Failed to get watched reels:', error);
  }
  return new Set();
}

/**
 * Mark a reel as watched in local storage.
 */
export async function markReelAsWatched(reelId: string): Promise<void> {
  try {
    const watchedIds = await getWatchedReelIds();
    watchedIds.add(reelId);
    await AsyncStorage.setItem(WATCHED_REELS_KEY, JSON.stringify([...watchedIds]));
    console.log(`[LocalWatchTracker] Marked reel ${reelId} as watched`);
  } catch (error) {
    console.error('[LocalWatchTracker] Failed to mark reel as watched:', error);
  }
}

/**
 * Check if a specific reel has been watched.
 */
export async function isReelWatched(reelId: string): Promise<boolean> {
  const watchedIds = await getWatchedReelIds();
  return watchedIds.has(reelId);
}

/**
 * Clear all watch history (for demo reset).
 */
export async function clearWatchHistory(): Promise<void> {
  try {
    await AsyncStorage.removeItem(WATCHED_REELS_KEY);
    console.log('[LocalWatchTracker] Watch history cleared');
  } catch (error) {
    console.error('[LocalWatchTracker] Failed to clear watch history:', error);
  }
}

/**
 * Get the count of watched reels.
 */
export async function getWatchedCount(): Promise<number> {
  const watchedIds = await getWatchedReelIds();
  return watchedIds.size;
}
