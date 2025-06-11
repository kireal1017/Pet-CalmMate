import { Stack } from 'expo-router';
import React from 'react';
import { AuthProvider } from '../share/store/auth_store';

export default function RootLayout() {
  return (
    <AuthProvider>
      
      <Stack screenOptions={{ headerShown: false }}>
        <Stack.Screen name="index" />
        <Stack.Screen name="auth_main" />
        <Stack.Screen name="(tabs)/main_home" />
      </Stack>
    </AuthProvider>
  );
}
