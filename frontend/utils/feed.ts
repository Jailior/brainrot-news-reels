import { REEL_PLACEHOLDER_DATA } from '@/constants/reels';
import { ReelItemData } from '@/components/reel-item';
import { Reel } from '@/utils/api';

// Array of all available video sources (fallback for placeholder mode)
const VIDEO_SOURCES = [
  require('@/assets/videos/YTParkour1.mp4'),
  require('@/assets/videos/YTParkour2.mp4'),
  require('@/assets/videos/YTParkour3.mp4'),
  require('@/assets/videos/YTParkour4.mp4'),
];

/**
 * Shuffles an array using Fisher-Yates algorithm
 */
function shuffleArray<T>(array: T[]): T[] {
  const shuffled = [...array];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled;
}

/**
 * Transform a Reel from the API to ReelItemData for the feed.
 * @param reel The reel from the API response
 * @param index The index in the current feed
 * @returns ReelItemData formatted for the feed component
 */
export function transformReelToFeedItem(reel: Reel, index: number): ReelItemData {
  // Extract a title/text from the script or use a default
  const text = reel.script
    ? reel.script.substring(0, 50) + (reel.script.length > 50 ? '...' : '')
    : 'News Reel';

  return {
    id: reel.id.toString(),
    text,
    subtitle: `${reel.views} views`,
    background: '#111111',
    virtualIndex: index,
    videoSource: reel.video_url || VIDEO_SOURCES[index % VIDEO_SOURCES.length],
  };
}

/**
 * Transform an array of Reels from the API to ReelItemData array.
 * @param reels Array of reels from API
 * @param startIndex Starting index for virtualIndex
 * @returns Array of ReelItemData
 */
export function transformReelsToFeedItems(reels: Reel[], startIndex: number = 0): ReelItemData[] {
  return reels.map((reel, index) => transformReelToFeedItem(reel, startIndex + index));
}

/**
 * Generates a set of reel items for infinite scrolling with random video order.
 * This is the fallback/placeholder data generator.
 * @param startIndex The starting index for the new items.
 * @param count The number of items to generate.
 * @returns An array of ReelItemData with randomized videos.
 */
export function generateInfiniteFeedData(startIndex: number, count: number): ReelItemData[] {
  const data: ReelItemData[] = [];

  // Create a shuffled list of video indices for this batch
  const shuffledIndices: number[] = [];
  while (shuffledIndices.length < count) {
    shuffledIndices.push(...shuffleArray([0, 1, 2, 3]));
  }

  for (let i = 0; i < count; i++) {
    const virtualIndex = startIndex + i;
    const originalIndex = virtualIndex % REEL_PLACEHOLDER_DATA.length;
    // Handle potential negative modulo results
    const safeIndex =
      originalIndex >= 0 ? originalIndex : originalIndex + REEL_PLACEHOLDER_DATA.length;
    const originalItem = REEL_PLACEHOLDER_DATA[safeIndex];

    // Pick a random video from the shuffled list
    const videoIndex = shuffledIndices[i];

    data.push({
      ...originalItem,
      id: `${virtualIndex}`,
      virtualIndex: Math.abs(virtualIndex % REEL_PLACEHOLDER_DATA.length),
      videoSource: VIDEO_SOURCES[videoIndex],
    });
  }
  return data;
}
