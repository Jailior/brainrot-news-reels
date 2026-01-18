import { useCallback, useEffect, useRef, useState } from 'react';
import { FlatList, ViewToken } from 'react-native';
import { ReelItemData } from '@/components/reel-item';
import { generateInfiniteFeedData, transformReelsToFeedItems } from '@/utils/feed';
import { fetchReels } from '@/utils/api';
import { isDemoMode } from '@/utils/config';
import {
  getDemoReels,
  transformDemoReelsToFeedItems,
  hasDemoVideos,
} from '@/constants/demo-reels';
import {
  markReelAsWatched,
  getWatchedReelIds,
} from '@/utils/local-watch-tracker';

const PAGE_SIZE = 10;

// NOTE: View tracking is disabled for API mode to allow infinite scrolling
// In demo mode, local watch tracking is always enabled
const ENABLE_VIEW_TRACKING = false;

export function useReelFeed(itemHeight?: number) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const flatListRef = useRef<FlatList>(null);
  const [feedData, setFeedData] = useState<ReelItemData[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [hasMore, setHasMore] = useState(true);
  const [isCaughtUp, setIsCaughtUp] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [offset, setOffset] = useState(0);
  const isLoadingMore = useRef(false);
  const allReels = useRef<ReelItemData[]>([]); // Store all reels for infinite loop
  const watchedIdsRef = useRef<Set<string>>(new Set()); // Track watched IDs in demo mode
  const loopCounter = useRef(0); // Counter to ensure unique IDs when looping

  // Check if we're in demo mode
  const isDemo = isDemoMode();

  // Load initial reels on mount
  useEffect(() => {
    loadInitialReels();
  }, []);

  // Load demo reels from local assets
  const loadDemoReels = async () => {
    setIsLoading(true);
    setError(null);

    try {
      // Load watched IDs from local storage
      watchedIdsRef.current = await getWatchedReelIds();

      if (!hasDemoVideos()) {
        console.warn('[Feed] Demo mode enabled but no demo videos configured');
        setError('No demo videos available. Add videos to assets/demo/');
        setIsCaughtUp(true);
        setHasMore(false);
        setFeedData([]);
        return;
      }

      const demoReels = getDemoReels();
      const items = transformDemoReelsToFeedItems(demoReels, 0);
      allReels.current = items;
      setFeedData(items);
      setHasMore(true); // Allow infinite looping
      setIsCaughtUp(false);

      console.log(`[Feed] Demo mode: Loaded ${items.length} demo reels`);
    } catch (err) {
      console.error('[Feed] Failed to load demo reels:', err);
      setError('Failed to load demo reels');
    } finally {
      setIsLoading(false);
    }
  };

  // Load reels from API
  const loadApiReels = async () => {
    setIsLoading(true);
    setError(null);

    try {
      // Don't pass user_id to get all reels (no watched filtering)
      const response = await fetchReels(PAGE_SIZE, 0, null);

      if (response.reels.length === 0) {
        // No reels available at all
        setIsCaughtUp(true);
        setHasMore(false);
        setFeedData([]);
      } else {
        const items = transformReelsToFeedItems(response.reels, 0);
        allReels.current = items;
        setFeedData(items);
        setOffset(response.reels.length);
        setHasMore(response.reels.length < response.total);
        setIsCaughtUp(false);
      }
    } catch (err) {
      console.error('[Feed] Failed to load reels:', err);
      setError('Failed to load reels');
      // Fallback to placeholder data
      setFeedData(generateInfiniteFeedData(0, PAGE_SIZE));
      setHasMore(true);
    } finally {
      setIsLoading(false);
    }
  };

  const loadInitialReels = async () => {
    if (isDemo) {
      console.log('[Feed] Running in DEMO mode');
      await loadDemoReels();
    } else {
      console.log('[Feed] Running in API mode');
      await loadApiReels();
    }
  };

  // Load more reels for infinite scrolling (demo mode)
  const loadMoreDemoReels = () => {
    if (isLoadingMore.current || allReels.current.length === 0) return;

    isLoadingMore.current = true;
    loopCounter.current += 1;
    const currentLoop = loopCounter.current;

    // Loop existing demo reels for infinite scroll with unique IDs
    setFeedData((prev) => {
      const loopedItems = allReels.current.map((item, idx) => ({
        ...item,
        id: `${item.id}-loop${currentLoop}-${idx}`,
        virtualIndex: prev.length + idx,
      }));
      return [...prev, ...loopedItems];
    });

    isLoadingMore.current = false;
  };

  // Load more reels from API
  const loadMoreApiReels = async () => {
    if (isLoadingMore.current) return;

    isLoadingMore.current = true;

    try {
      // Don't pass user_id to get all reels
      const response = await fetchReels(PAGE_SIZE, offset, null);

      if (response.reels.length === 0) {
        // No more new reels - loop back to start for infinite scrolling
        if (allReels.current.length > 0) {
          loopCounter.current += 1;
          const currentLoop = loopCounter.current;
          // Create duplicates with unique IDs for infinite scroll
          setFeedData((prev) => {
            const loopedItems = allReels.current.map((item, idx) => ({
              ...item,
              id: `${item.id}-loop${currentLoop}-${idx}`,
              virtualIndex: prev.length + idx,
            }));
            return [...prev, ...loopedItems];
          });
        }
        // Keep hasMore true for infinite scrolling
        setHasMore(true);
      } else {
        const newItems = transformReelsToFeedItems(response.reels, feedData.length);
        allReels.current = [...allReels.current, ...newItems];
        setFeedData((prev) => [...prev, ...newItems]);
        setOffset((prev) => prev + response.reels.length);
        setHasMore(true); // Always allow more for infinite scroll
      }
    } catch (err) {
      console.error('[Feed] Failed to load more reels:', err);
      // On error, loop existing reels for infinite scroll
      if (allReels.current.length > 0) {
        loopCounter.current += 1;
        const currentLoop = loopCounter.current;
        setFeedData((prev) => {
          const loopedItems = allReels.current.map((item, idx) => ({
            ...item,
            id: `${item.id}-loop${currentLoop}-${idx}`,
            virtualIndex: prev.length + idx,
          }));
          return [...prev, ...loopedItems];
        });
      }
    } finally {
      isLoadingMore.current = false;
    }
  };

  const loadMoreReels = () => {
    if (isDemo) {
      loadMoreDemoReels();
    } else {
      loadMoreApiReels();
    }
  };

  // Handle reel view - tracks locally in demo mode
  const handleReelView = useCallback(async (reelId: string) => {
    if (isDemo) {
      // In demo mode, always track views locally
      await markReelAsWatched(reelId);
      watchedIdsRef.current.add(reelId);
      console.log(`[Feed] Demo mode: Marked reel ${reelId} as watched`);
      return;
    }

    if (!ENABLE_VIEW_TRACKING) {
      console.log(`[Feed] View tracking disabled, skipping reel ${reelId}`);
      return;
    }
    // View tracking code would go here when re-enabled for API mode
  }, [isDemo]);

  const onViewableItemsChanged = useCallback(
    ({ viewableItems }: { viewableItems: ViewToken[] }) => {
      if (viewableItems.length > 0 && viewableItems[0].index !== null) {
        const newIndex = viewableItems[0].index;
        if (newIndex !== currentIndex) {
          setCurrentIndex(newIndex);
        }
      }
    },
    [currentIndex]
  );

  const viewabilityConfig = useRef({
    itemVisiblePercentThreshold: 50,
  }).current;

  const handleEndReached = useCallback(() => {
    // Always try to load more for infinite scrolling
    loadMoreReels();
  }, []);

  const refresh = useCallback(() => {
    setOffset(0);
    setIsCaughtUp(false);
    setHasMore(true);
    loadInitialReels();
  }, []);

  return {
    currentIndex,
    flatListRef,
    feedData,
    onViewableItemsChanged,
    viewabilityConfig,
    handleEndReached,
    handleReelView,
    // States
    isLoading,
    isCaughtUp,
    hasMore,
    error,
    refresh,
    // Demo mode state
    isDemoMode: isDemo,
  };
}
