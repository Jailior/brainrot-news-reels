/**
 * Singleton Video Manager
 * Ensures only one video plays audio at a time.
 * When a new video becomes active, the previous one is stopped.
 *
 * Note: expo-video handles its own audio session, so we don't need
 * to configure expo-av Audio separately.
 */

import { VideoPlayer } from 'expo-video';

class VideoManager {
  private static instance: VideoManager;
  private activePlayer: VideoPlayer | null = null;
  private activeItemId: string | null = null;

  private constructor() {
    // expo-video handles audio session automatically
  }

  static getInstance(): VideoManager {
    if (!VideoManager.instance) {
      VideoManager.instance = new VideoManager();
    }
    return VideoManager.instance;
  }

  /**
   * Set the active player. This will stop the previous player.
   * @param player The video player to make active
   * @param itemId Unique identifier for the item
   */
  setActivePlayer(player: VideoPlayer, itemId: string): void {
    // If same player is already active, do nothing
    if (this.activeItemId === itemId) {
      return;
    }

    // Stop the previous player
    if (this.activePlayer && this.activePlayer !== player) {
      try {
        this.activePlayer.pause();
        this.activePlayer.muted = true;
      } catch {
        // Silently handle - player may already be disposed
      }
    }

    // Set new active player
    this.activePlayer = player;
    this.activeItemId = itemId;
  }

  /**
   * Play the active player with audio
   */
  playActive(): void {
    if (this.activePlayer) {
      try {
        this.activePlayer.muted = false;
        this.activePlayer.play();
      } catch {
        // Silently handle - player may be in invalid state
      }
    }
  }

  /**
   * Pause the active player (keeps it as active, just paused)
   */
  pauseActive(): void {
    if (this.activePlayer) {
      try {
        this.activePlayer.pause();
      } catch {
        // Silently handle - player may be in invalid state
      }
    }
  }

  /**
   * Deactivate a specific player (when scrolling away)
   */
  deactivatePlayer(player: VideoPlayer, itemId: string): void {
    try {
      player.pause();
      player.muted = true;
    } catch {
      // Silently handle - player may already be disposed
    }

    // If this was the active player, clear it
    if (this.activeItemId === itemId) {
      this.activePlayer = null;
      this.activeItemId = null;
    }
  }

  /**
   * Check if a specific item is currently active
   */
  isActive(itemId: string): boolean {
    return this.activeItemId === itemId;
  }

  /**
   * Stop all playback (for cleanup or app backgrounding)
   */
  stopAll(): void {
    if (this.activePlayer) {
      try {
        this.activePlayer.pause();
        this.activePlayer.muted = true;
      } catch {
        // Silently handle
      }
    }
    this.activePlayer = null;
    this.activeItemId = null;
  }
}

// Export singleton instance
export const videoManager = VideoManager.getInstance();
