import { useCallback } from 'react';
import { FlatList, StyleSheet, View } from 'react-native';
import { ReelItem, ReelItemData } from '@/components/reel-item';
import { useReelFeed } from '@/hooks/use-reel-feed';

export default function FeedScreen() {
  const {
    flatListRef,
    feedData,
    onViewableItemsChanged,
    onMomentumScrollEnd,
    viewabilityConfig,
    handleEndReached,
    getItemLayout,
    SCREEN_HEIGHT,
  } = useReelFeed();

  const renderItem = useCallback(
    ({ item }: { item: ReelItemData }) => <ReelItem item={item} />,
    []
  );

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
        disableIntervalMomentum={true}
        onMomentumScrollEnd={onMomentumScrollEnd}
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
});
