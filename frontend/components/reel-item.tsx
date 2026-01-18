import React, { useEffect, useState } from 'react';
import { Dimensions, Pressable, StyleSheet } from 'react-native';
import { VideoView, useVideoPlayer } from 'expo-video';

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
});
