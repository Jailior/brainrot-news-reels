/**
 * Demo reel data for offline/demo mode.
 * Videos should be placed in assets/demo/ folder.
 *
 * To add demo videos:
 * 1. Place .mp4 files in frontend/assets/demo/
 * 2. Add entries to DEMO_REELS array below
 * 3. Use require() to reference the video file
 */

import { ReelItemData } from '@/components/reel-item';

// Demo video sources - videos from assets/demo/ folder
const DEMO_VIDEO_SOURCES: (number | string)[] = [
  require('@/assets/demo/video1.mp4'),
  require('@/assets/demo/video2.mp4'),
  require('@/assets/demo/video3.mp4'),
];

/**
 * Demo reel metadata.
 * Each entry represents a demo reel with its video and display info.
 */
export interface DemoReel {
  id: string;
  title: string;
  subtitle: string;
  videoSource: number | string;
}

/**
 * Generate demo reels from available video sources.
 * This creates reel data from the DEMO_VIDEO_SOURCES array.
 */
export function getDemoReels(): DemoReel[] {
  return DEMO_VIDEO_SOURCES.map((source, index) => ({
    id: `demo-${index + 1}`,
    title: `Demo Reel ${index + 1}`,
    subtitle: 'Demo content',
    videoSource: source,
  }));
}

/**
 * Transform demo reels to feed item format.
 */
export function transformDemoReelsToFeedItems(
  demoReels: DemoReel[],
  startIndex: number = 0
): ReelItemData[] {
  return demoReels.map((reel, index) => ({
    id: reel.id,
    text: reel.title,
    subtitle: reel.subtitle,
    background: '#111111',
    virtualIndex: startIndex + index,
    videoSource: reel.videoSource,
  }));
}

/**
 * Check if demo mode has videos configured.
 */
export function hasDemoVideos(): boolean {
  return DEMO_VIDEO_SOURCES.length > 0;
}
