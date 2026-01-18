import React, { useEffect, useState } from 'react';
import { Dimensions, Pressable, StyleSheet, View } from 'react-native';
import { VideoView, useVideoPlayer } from 'expo-video';
import { Ionicons } from '@expo/vector-icons';

const { width: SCREEN_WIDTH, height: SCREEN_HEIGHT } = Dimensions.get('window');

export interface ReelItemData {
  id: string;
  text: string;
  subtitle: string;
  background: string;
  virtualIndex: number;
  videoSource: any;
}

interface ReelItemProps {
  item: ReelItemData;
  isActive: boolean;
}

export const ReelItem = React.memo(({ item, isActive }: ReelItemProps) => {
  const [isPaused, setIsPaused] = useState(false);

  const player = useVideoPlayer(item.videoSource, (player) => {
    player.loop = true;
    player.muted = true;
    player.play();
  });

  const handlePress = () => {
    setIsPaused((prev) => !prev);
  };

  useEffect(() => {
    if (player) {
      if (isActive && !isPaused) {
        player.play();
      } else {
        player.pause();
      }
    }
  }, [isActive, isPaused, player]);

  return (
    <Pressable style={styles.itemContainer} onPress={handlePress}>
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
    height: SCREEN_HEIGHT,
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
