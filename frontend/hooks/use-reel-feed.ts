import { useCallback, useRef, useState } from 'react';
import { Dimensions, FlatList, ViewToken } from 'react-native';
import { ReelItemData } from '@/components/reel-item';
import { generateInfiniteFeedData } from '@/utils/feed';

const { height: SCREEN_HEIGHT } = Dimensions.get('window');

export function useReelFeed() {
  const [currentIndex, setCurrentIndex] = useState(0);
  const flatListRef = useRef<FlatList>(null);

  const [feedData, setFeedData] = useState<ReelItemData[]>(() => generateInfiniteFeedData(0, 10));

  const onViewableItemsChanged = useCallback(
    ({ viewableItems }: { viewableItems: ViewToken[] }) => {
      if (viewableItems.length > 0 && viewableItems[0].index !== null) {
        const newIndex = viewableItems[0].index;
        if (newIndex !== currentIndex) {
          setCurrentIndex(newIndex);
          console.log(`📱 Scrolled to item ${newIndex + 1}`);
        }
      }
    },
    [currentIndex]
  );

  const onMomentumScrollEnd = useCallback((event: any) => {
    const offsetY = event.nativeEvent.contentOffset.y;
    const currentItem = Math.round(offsetY / SCREEN_HEIGHT);
    flatListRef.current?.scrollToIndex({
      index: currentItem,
      animated: false,
    });
  }, []);

  const viewabilityConfig = useRef({
    itemVisiblePercentThreshold: 50,
  }).current;

  const handleEndReached = useCallback(() => {
    const lastIndex = feedData.length;
    const newItems = generateInfiniteFeedData(lastIndex, 5);
    setFeedData((prev) => [...prev, ...newItems]);
  }, [feedData.length]);

  const getItemLayout = useCallback(
    (_: any, index: number) => ({
      length: SCREEN_HEIGHT,
      offset: SCREEN_HEIGHT * index,
      index,
    }),
    []
  );

  return {
    currentIndex,
    flatListRef,
    feedData,
    onViewableItemsChanged,
    onMomentumScrollEnd,
    viewabilityConfig,
    handleEndReached,
    getItemLayout,
    SCREEN_HEIGHT,
  };
}
