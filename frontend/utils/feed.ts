import { REEL_PLACEHOLDER_DATA } from '@/constants/reels';
import { ReelItemData } from '@/components/reel-item';

// Array of all available video sources
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
 * Generates a set of reel items for infinite scrolling with random video order.
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
