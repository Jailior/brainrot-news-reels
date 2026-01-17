import { REEL_PLACEHOLDER_DATA } from '@/constants/reels';
import { ReelItemData } from '@/components/reel-item';

/**
 * Generates a set of reel items for infinite scrolling based on placeholder data.
 * @param startIndex The starting index for the new items.
 * @param count The number of items to generate.
 * @returns An array of ReelItemData.
 */
export function generateInfiniteFeedData(startIndex: number, count: number): ReelItemData[] {
  const data: ReelItemData[] = [];
  for (let i = 0; i < count; i++) {
    const virtualIndex = startIndex + i;
    const originalIndex = virtualIndex % REEL_PLACEHOLDER_DATA.length;
    // Handle potential negative modulo results
    const safeIndex =
      originalIndex >= 0 ? originalIndex : originalIndex + REEL_PLACEHOLDER_DATA.length;
    const originalItem = REEL_PLACEHOLDER_DATA[safeIndex];

    data.push({
      ...originalItem,
      id: `${virtualIndex}`,
      virtualIndex: Math.abs(virtualIndex % REEL_PLACEHOLDER_DATA.length),
    });
  }
  return data;
}
