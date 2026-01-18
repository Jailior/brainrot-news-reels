/**
 * Simple API client for communicating with the backend.
 * MVP implementation - stores user ID in AsyncStorage.
 */

import AsyncStorage from '@react-native-async-storage/async-storage';
import { Platform } from 'react-native';
import Constants from 'expo-constants';

/**
 * Get the API base URL based on the platform.
 *
 * - iOS Simulator: localhost works
 * - Android Emulator: 10.0.2.2 maps to host machine
 * - Physical devices: Use your computer's local IP (e.g., 192.168.x.x)
 * - Web: localhost works
 *
 * To use a custom IP for physical devices, set EXPO_PUBLIC_API_URL in your .env
 * or update the DEVICE_IP constant below.
 */
function getApiBaseUrl(): string {
  // Allow override via environment variable
  if (Constants.expoConfig?.extra?.apiUrl) {
    return Constants.expoConfig.extra.apiUrl;
  }

  // For physical devices, replace with your computer's local IP address
  // Find it with: ifconfig (macOS/Linux) or ipconfig (Windows)
  const DEVICE_IP = '192.168.1.100'; // TODO: Replace with your actual local IP

  if (Platform.OS === 'android') {
    // Android emulator uses special IP to access host machine
    return __DEV__ ? 'http://10.0.2.2:8000/api' : `http://${DEVICE_IP}:8000/api`;
  } else if (Platform.OS === 'ios') {
    // iOS simulator can use localhost
    return __DEV__ ? 'http://localhost:8000/api' : `http://${DEVICE_IP}:8000/api`;
  } else {
    // Web platform
    return 'http://localhost:8000/api';
  }
}

const API_BASE_URL = getApiBaseUrl();

// Log the API URL in development for debugging
if (__DEV__) {
  console.log(`[API] Using base URL: ${API_BASE_URL}`);
}

// Storage keys
const USER_ID_KEY = 'brainrot_user_id';

// Types
export interface User {
  id: number;
  name: string | null;
  email: string;
  has_completed_setup: boolean;
  preferences: {
    categories?: string[];
    language?: string;
  } | null;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface SignupRequest {
  name: string;
  email: string;
  password: string;
}

export interface SetupRequest {
  user_id: number;
  preferences: {
    categories: string[];
    language: string;
  };
}

// API Error class
export class ApiError extends Error {
  constructor(
    public statusCode: number,
    message: string
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

// Helper function to make API requests
async function request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;

  const config: RequestInit = {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  };

  try {
    if (__DEV__) {
      console.log(`[API] ${options.method || 'GET'} ${url}`);
    }

    const response = await fetch(url, config);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new ApiError(
        response.status,
        errorData.detail || `Request failed with status ${response.status}`
      );
    }

    return response.json();
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    // Enhanced error message for network issues
    const errorMessage =
      error instanceof TypeError && error.message.includes('fetch')
        ? `Network error - cannot reach ${API_BASE_URL}. Make sure the backend is running and the IP address is correct.`
        : 'Network error - please check your connection';
    if (__DEV__) {
      console.error(`[API] Request failed:`, error);
    }
    throw new ApiError(0, errorMessage);
  }
}

// Storage helpers
export async function saveUserId(userId: number): Promise<void> {
  await AsyncStorage.setItem(USER_ID_KEY, userId.toString());
}

export async function getUserId(): Promise<number | null> {
  const id = await AsyncStorage.getItem(USER_ID_KEY);
  return id ? parseInt(id, 10) : null;
}

export async function clearUserId(): Promise<void> {
  await AsyncStorage.removeItem(USER_ID_KEY);
}

// API functions
export async function login(email: string, password: string): Promise<User> {
  const user = await request<User>('/login', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  });
  await saveUserId(user.id);
  return user;
}

export async function signup(name: string, email: string, password: string): Promise<User> {
  const user = await request<User>('/signup', {
    method: 'POST',
    body: JSON.stringify({ name, email, password }),
  });
  await saveUserId(user.id);
  return user;
}

export async function updateSetup(
  userId: number,
  preferences: SetupRequest['preferences']
): Promise<User> {
  const user = await request<User>('/setup', {
    method: 'POST',
    body: JSON.stringify({ user_id: userId, preferences }),
  });
  return user;
}

export async function getCurrentUser(userId: number): Promise<User> {
  return request<User>(`/me?user_id=${userId}`);
}

export async function logout(): Promise<void> {
  await clearUserId();
}

export interface UpdateProfileRequest {
  user_id: number;
  name?: string;
  password?: string;
  current_password?: string;
}

export async function updateProfile(data: UpdateProfileRequest): Promise<User> {
  const user = await request<User>('/update-profile', {
    method: 'PUT',
    body: JSON.stringify(data),
  });
  return user;
}

export interface DeleteAccountRequest {
  user_id: number;
}

export async function deleteAccount(data: DeleteAccountRequest): Promise<void> {
  await request<{ message: string }>('/delete-account', {
    method: 'DELETE',
    body: JSON.stringify(data),
  });
  await clearUserId();
}

// Guest user credentials
export const GUEST_CREDENTIALS = {
  email: 'guest@brainrot.app',
  password: 'guest123',
};
