import React, { useEffect, useRef, useState } from 'react';
import { Dimensions, Pressable, StyleSheet, useWindowDimensions } from 'react-native';
import { VideoView, useVideoPlayer } from 'expo-video';
import { videoManager } from '@/utils/video-manager';

const { width: SCREEN_WIDTH } = Dimensions.get('window');

export interface ReelItemData {
  id: string;
  text: string;
  subtitle: string;
  background: string;
  virtualIndex: number;
  /** Video source - can be a require() result (number) or a URL string */
  videoSource: string | number;
}

interface ReelItemProps {
  item: ReelItemData;
  isActive: boolean;
  /** Callback when this reel is viewed (becomes active) */
  onView?: (reelId: string) => void;
  /** Height of the item - should be passed from parent to account for tab bar */
  itemHeight: number;
}

export const ReelItem = React.memo(({ item, isActive, onView, itemHeight }: ReelItemProps) => {
  const [isPaused, setIsPaused] = useState(false);
  const hasTrackedView = useRef(false);
  const wasActive = useRef(false);

  const player = useVideoPlayer(item.videoSource, (player) => {
    player.loop = true;
    // Start muted - video manager will unmute when active
    player.muted = true;
    player.volume = 1.0;
  });

  const handlePress = () => {
    if (!player || !isActive) return;

    const newPausedState = !isPaused;
    setIsPaused(newPausedState);

    // Use video manager for consistent control
    if (newPausedState) {
      videoManager.pauseActive();
    } else {
      videoManager.playActive();
    }
  };

  // Track view when reel becomes active
  useEffect(() => {
    if (isActive && !hasTrackedView.current && onView) {
      hasTrackedView.current = true;
      onView(item.id);
    }
  }, [isActive, item.id, onView]);

  // Handle activation/deactivation through the singleton video manager
  useEffect(() => {
    if (!player) return;

    if (isActive && !wasActive.current) {
      // Becoming active - register with video manager (this stops the previous player)
      videoManager.setActivePlayer(player, item.id);
      
      if (!isPaused) {
        videoManager.playActive();
      }
      wasActive.current = true;
    } else if (!isActive && wasActive.current) {
      // Becoming inactive - explicitly deactivate through video manager
      videoManager.deactivatePlayer(player, item.id);
      wasActive.current = false;
      setIsPaused(false); // Reset pause state when scrolling away
    } else if (isActive && wasActive.current) {
      // Already active, just handle pause state changes
      if (isPaused) {
        videoManager.pauseActive();
      } else {
        videoManager.playActive();
      }
    }
  }, [isActive, isPaused, player, item.id]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (player && wasActive.current) {
        videoManager.deactivatePlayer(player, item.id);
      }
    };
  }, [player, item.id]);

  return (
    <Pressable
      style={[styles.itemContainer, { height: itemHeight }]}
      onPress={handlePress}
    >
      <VideoView
        player={player}
        contentFit="cover"
        style={StyleSheet.absoluteFillObject}
        nativeControls={false}
        allowsFullscreen={false}
      />
    </Pressable>
  );
});

ReelItem.displayName = 'ReelItem';

const styles = StyleSheet.create({
  itemContainer: {
    width: SCREEN_WIDTH,
    backgroundColor: '#000',
  },
});
