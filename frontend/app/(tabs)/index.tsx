import { useCallback } from 'react';
import {
  ActivityIndicator,
  FlatList,
  StyleSheet,
  Text,
  View,
  useWindowDimensions,
} from 'react-native';
import { useBottomTabBarHeight } from '@react-navigation/bottom-tabs';
import { ReelItem, ReelItemData } from '@/components/reel-item';
import { useReelFeed } from '@/hooks/use-reel-feed';

// NOTE: Caught up modal is disabled for now - infinite scrolling enabled
// import { CaughtUpModal } from '@/components/caught-up-modal';

export default function FeedScreen() {
  const { height: windowHeight } = useWindowDimensions();
  const tabBarHeight = useBottomTabBarHeight();

  // Calculate the available height for each reel item (window height minus tab bar)
  const itemHeight = windowHeight - tabBarHeight;

  const {
    currentIndex,
    flatListRef,
    feedData,
    onViewableItemsChanged,
    viewabilityConfig,
    handleEndReached,
    handleReelView,
    isLoading,
    error,
  } = useReelFeed(itemHeight);

  const renderItem = useCallback(
    ({ item, index }: { item: ReelItemData; index: number }) => (
      <ReelItem
        item={item}
        isActive={index === currentIndex}
        onView={handleReelView}
        itemHeight={itemHeight}
      />
    ),
    [currentIndex, handleReelView, itemHeight]
  );

  // Memoized getItemLayout for FlatList optimization
  const getItemLayout = useCallback(
    (_: any, index: number) => ({
      length: itemHeight,
      offset: itemHeight * index,
      index,
    }),
    [itemHeight]
  );

  // Loading state
  if (isLoading && feedData.length === 0) {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" color="#fff" />
        <Text style={styles.loadingText}>Loading reels...</Text>
      </View>
    );
  }

  // Empty state - no reels at all
  if (!isLoading && feedData.length === 0) {
    return (
      <View style={styles.centerContainer}>
        <Text style={styles.emptyEmoji}>📺</Text>
        <Text style={styles.emptyTitle}>No reels yet</Text>
        <Text style={styles.emptySubtitle}>Check back later for fresh content.</Text>
      </View>
    );
  }

  // Error state with no data
  if (error && feedData.length === 0) {
    return (
      <View style={styles.centerContainer}>
        <Text style={styles.errorText}>{error}</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <FlatList
        ref={flatListRef}
        data={feedData}
        renderItem={renderItem}
        keyExtractor={(item) => item.id}
        pagingEnabled
        showsVerticalScrollIndicator={false}
        snapToInterval={itemHeight}
        snapToAlignment="start"
        decelerationRate="fast"
        disableIntervalMomentum={true}
        scrollEnabled={true}
        onViewableItemsChanged={onViewableItemsChanged}
        viewabilityConfig={viewabilityConfig}
        onEndReached={handleEndReached}
        onEndReachedThreshold={0.5}
        getItemLayout={getItemLayout}
        removeClippedSubviews={true}
        maxToRenderPerBatch={2}
        windowSize={3}
        initialNumToRender={1}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
  },
  centerContainer: {
    flex: 1,
    backgroundColor: '#000',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 32,
  },
  loadingText: {
    color: '#888',
    fontSize: 16,
    marginTop: 16,
  },
  emptyEmoji: {
    fontSize: 64,
    marginBottom: 16,
  },
  emptyTitle: {
    fontSize: 24,
    fontWeight: '700',
    color: '#fff',
    marginBottom: 8,
    textAlign: 'center',
  },
  emptySubtitle: {
    fontSize: 16,
    color: '#888',
    textAlign: 'center',
  },
  errorText: {
    color: '#ff6b6b',
    fontSize: 16,
    textAlign: 'center',
  },
});
