import React, { useEffect, useRef, useState } from 'react';
import { Dimensions, Pressable, StyleSheet, View } from 'react-native';
import { VideoView, useVideoPlayer } from 'expo-video';
import { Ionicons } from '@expo/vector-icons';
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

// Safe player control helper - catches errors from disposed players
const safePlayerControl = (player: any, action: () => void) => {
  try {
    action();
  } catch {
    // Player may be disposed - ignore errors
  }
};

export const ReelItem = React.memo(({ item, isActive, onView, itemHeight }: ReelItemProps) => {
  const [isPaused, setIsPaused] = useState(false);
  const hasTrackedView = useRef(false);
  const isMounted = useRef(true);
  const hasStartedPlaying = useRef(false);

  const player = useVideoPlayer(item.videoSource, (player) => {
    player.loop = true;
    player.muted = true;
    player.volume = 1.0;
    // Don't call pause here - let the effect handle it
  });

  // Track mounted state
  useEffect(() => {
    isMounted.current = true;
    return () => {
      isMounted.current = false;
    };
  }, []);

  const handlePress = () => {
    if (!player || !isActive || !isMounted.current) return;

    const newPausedState = !isPaused;
    setIsPaused(newPausedState);

    // Directly control this player
    safePlayerControl(player, () => {
      if (newPausedState) {
        player.pause();
      } else {
        player.muted = false;
        player.play();
      }
    });
  };

  // Track view when reel becomes active
  useEffect(() => {
    if (isActive && !hasTrackedView.current && onView) {
      hasTrackedView.current = true;
      onView(item.id);
    }
  }, [isActive, item.id, onView]);

  // Handle activation/deactivation - this is the key logic for preventing audio layering
  useEffect(() => {
    if (!player || !isMounted.current) return;

    if (isActive) {
      // This item is active - register with video manager which will stop any other player
      videoManager.setActivePlayer(player, item.id);

      // Only play if not paused by user and we haven't already started
      if (!isPaused) {
        safePlayerControl(player, () => {
          player.muted = false;
          player.play();
        });
        hasStartedPlaying.current = true;
      }
    } else {
      // This item is NOT active - ensure it's stopped and muted
      safePlayerControl(player, () => {
        player.muted = true;
        player.pause();
      });
      setIsPaused(false); // Reset pause state when not active
      hasStartedPlaying.current = false;
    }
  }, [isActive, isPaused, player, item.id]);

  return (
    <Pressable style={[styles.itemContainer, { height: itemHeight }]} onPress={handlePress}>
      <VideoView
        player={player}
        contentFit="cover"
        style={StyleSheet.absoluteFillObject}
        nativeControls={false}
        allowsFullscreen={false}
      />
      {/* Right side action icons */}
      <View style={styles.iconContainer}>
        <Pressable style={styles.iconButton}>
          <Ionicons name="heart-outline" size={32} color="#fff" />
        </Pressable>
        <Pressable style={styles.iconButton}>
          <Ionicons name="chatbubble-outline" size={30} color="#fff" />
        </Pressable>
        <Pressable style={styles.iconButton}>
          <Ionicons name="share-outline" size={30} color="#fff" />
        </Pressable>
      </View>
    </Pressable>
  );
});

ReelItem.displayName = 'ReelItem';

const styles = StyleSheet.create({
  itemContainer: {
    width: SCREEN_WIDTH,
    backgroundColor: '#000',
  },
  iconContainer: {
    position: 'absolute',
    right: 16,
    top: '50%',
    transform: [{ translateY: -80 }],
    alignItems: 'center',
    gap: 20,
  },
  iconButton: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: 'rgba(0, 0, 0, 0.3)',
    justifyContent: 'center',
    alignItems: 'center',
  },
});
