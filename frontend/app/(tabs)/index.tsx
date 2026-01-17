import { useCallback, useRef, useState } from 'react';
import {
  Dimensions,
  FlatList,
  StyleSheet,
  Text,
  View,
  ViewToken,
} from 'react-native';
import * as Haptics from 'expo-haptics';

const { width: SCREEN_WIDTH, height: SCREEN_HEIGHT } = Dimensions.get('window');

// 5 placeholder items with minimal aesthetics
const PLACEHOLDER_DATA = [
  {
    id: '1',
    text: 'BREAKING NEWS',
    subtitle: 'Swipe up to explore',
    background: '#111111',
  },
  {
    id: '2',
    text: 'TRENDING NOW',
    subtitle: 'The latest stories',
    background: '#222222',
  },
  {
    id: '3',
    text: 'VIRAL MOMENT',
    subtitle: 'Everyone is talking about this',
    background: '#333333',
  },
  {
    id: '4',
    text: 'EXCLUSIVE',
    subtitle: 'You saw it here first',
    background: '#444444',
  },
  {
    id: '5',
    text: 'JUST IN',
    subtitle: 'Fresh off the press',
    background: '#555555',
  },
];

interface ItemData {
  id: string;
  text: string;
  subtitle: string;
  background: string;
  virtualIndex: number;
}

interface ReelItemProps {
  item: ItemData;
}

function ReelItem({ item }: ReelItemProps) {
  return (
    <View style={[styles.itemContainer, { backgroundColor: item.background }]}>
      <View style={styles.contentContainer}>
        <Text style={styles.mainText}>{item.text}</Text>
        <Text style={styles.subtitleText}>{item.subtitle}</Text>
      </View>
    </View>
  );
}

export default function FeedScreen() {
  const [currentIndex, setCurrentIndex] = useState(0);
  const flatListRef = useRef<FlatList>(null);
  
  // Create infinite data by cycling through placeholders
  const generateInfiniteData = useCallback((startIndex: number, count: number): ItemData[] => {
    const data: ItemData[] = [];
    for (let i = 0; i < count; i++) {
      const virtualIndex = startIndex + i;
      const originalIndex = virtualIndex % PLACEHOLDER_DATA.length;
      const originalItem = PLACEHOLDER_DATA[originalIndex >= 0 ? originalIndex : originalIndex + PLACEHOLDER_DATA.length];
      data.push({
        ...originalItem,
        id: `${virtualIndex}`,
        virtualIndex: Math.abs(virtualIndex % PLACEHOLDER_DATA.length),
      });
    }
    return data;
  }, []);

  const [feedData, setFeedData] = useState<ItemData[]>(() => generateInfiniteData(0, 10));
  
  // Handle scroll detection and haptic feedback
  const onViewableItemsChanged = useCallback(({ viewableItems }: { viewableItems: ViewToken[] }) => {
    if (viewableItems.length > 0 && viewableItems[0].index !== null) {
      const newIndex = viewableItems[0].index;
      if (newIndex !== currentIndex) {
        setCurrentIndex(newIndex);
        Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
        console.log(`📱 Scrolled to item ${newIndex + 1}`);
      }
    }
  }, [currentIndex]);

  const viewabilityConfig = useRef({
    itemVisiblePercentThreshold: 50,
  }).current;

  // Handle infinite scroll
  const handleEndReached = useCallback(() => {
    const lastIndex = feedData.length;
    const newItems = generateInfiniteData(lastIndex, 5);
    setFeedData(prev => [...prev, ...newItems]);
  }, [feedData.length, generateInfiniteData]);

  const renderItem = useCallback(({ item }: { item: ItemData }) => (
    <ReelItem item={item} />
  ), []);

  const getItemLayout = useCallback((_: any, index: number) => ({
    length: SCREEN_HEIGHT,
    offset: SCREEN_HEIGHT * index,
    index,
  }), []);

  return (
    <View style={styles.container}>
      <FlatList
        ref={flatListRef}
        data={feedData}
        renderItem={renderItem}
        keyExtractor={(item) => item.id}
        pagingEnabled
        showsVerticalScrollIndicator={false}
        snapToInterval={SCREEN_HEIGHT}
        snapToAlignment="start"
        decelerationRate="fast"
        onViewableItemsChanged={onViewableItemsChanged}
        viewabilityConfig={viewabilityConfig}
        onEndReached={handleEndReached}
        onEndReachedThreshold={0.5}
        getItemLayout={getItemLayout}
        removeClippedSubviews
        maxToRenderPerBatch={3}
        windowSize={5}
        initialNumToRender={2}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
  },
  itemContainer: {
    width: SCREEN_WIDTH,
    height: SCREEN_HEIGHT,
    justifyContent: 'center',
    alignItems: 'center',
  },
  contentContainer: {
    alignItems: 'center',
    paddingHorizontal: 32,
  },
  mainText: {
    fontSize: 28,
    fontWeight: '600',
    color: '#fff',
    textAlign: 'center',
    letterSpacing: 2,
  },
  subtitleText: {
    fontSize: 14,
    color: 'rgba(255, 255, 255, 0.5)',
    textAlign: 'center',
    marginTop: 12,
    fontWeight: '400',
  },
});
