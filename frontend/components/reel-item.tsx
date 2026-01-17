import React from 'react';
import { Dimensions, StyleSheet, Text, View } from 'react-native';

const { width: SCREEN_WIDTH, height: SCREEN_HEIGHT } = Dimensions.get('window');

export interface ReelItemData {
  id: string;
  text: string;
  subtitle: string;
  background: string;
  virtualIndex: number;
}

interface ReelItemProps {
  item: ReelItemData;
}

export const ReelItem = React.memo(({ item }: ReelItemProps) => {
  return (
    <View style={[styles.itemContainer, { backgroundColor: item.background }]}>
      <View style={styles.contentContainer}>
        <Text style={styles.mainText}>{item.text}</Text>
        <Text style={styles.subtitleText}>{item.subtitle}</Text>
      </View>
    </View>
  );
});

ReelItem.displayName = 'ReelItem';

const styles = StyleSheet.create({
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
