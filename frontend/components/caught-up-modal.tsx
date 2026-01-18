import React from 'react';
import {
  Modal,
  View,
  Text,
  Pressable,
  StyleSheet,
  Dimensions,
} from 'react-native';

const { width: SCREEN_WIDTH } = Dimensions.get('window');

interface CaughtUpModalProps {
  visible: boolean;
  onDismiss: () => void;
}

export function CaughtUpModal({ visible, onDismiss }: CaughtUpModalProps) {
  return (
    <Modal
      animationType="fade"
      transparent={true}
      visible={visible}
      onRequestClose={onDismiss}
    >
      <View style={styles.overlay}>
        <View style={styles.modalContainer}>
          <Text style={styles.emoji}>✨</Text>
          <Text style={styles.title}>You're all caught up!</Text>
          <Text style={styles.subtitle}>
            Check back later for fresh content.
          </Text>
          <Pressable style={styles.button} onPress={onDismiss}>
            <Text style={styles.buttonText}>Got it</Text>
          </Pressable>
        </View>
      </View>
    </Modal>
  );
}

const styles = StyleSheet.create({
  overlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.7)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalContainer: {
    width: SCREEN_WIDTH * 0.8,
    backgroundColor: '#1a1a1a',
    borderRadius: 20,
    padding: 32,
    alignItems: 'center',
  },
  emoji: {
    fontSize: 48,
    marginBottom: 16,
  },
  title: {
    fontSize: 22,
    fontWeight: '700',
    color: '#fff',
    marginBottom: 8,
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 15,
    color: '#888',
    textAlign: 'center',
    marginBottom: 24,
    lineHeight: 22,
  },
  button: {
    backgroundColor: '#fff',
    paddingVertical: 14,
    paddingHorizontal: 48,
    borderRadius: 30,
  },
  buttonText: {
    color: '#000',
    fontSize: 16,
    fontWeight: '600',
  },
});
