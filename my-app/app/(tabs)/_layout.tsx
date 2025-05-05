import { Tabs } from 'expo-router';
import { MaterialIcons, MaterialCommunityIcons } from '@expo/vector-icons';

export default function TabsLayout() {
  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: '#FF9999',
        tabBarInactiveTintColor: '#888',
        tabBarStyle: {
          height: 65,
          borderTopWidth: 1,
          borderTopColor: '#D9D9D9',
        },
      }}
    >
      {/* 홈 탭 */}
      <Tabs.Screen
        name="index"
        options={{
          title: '홈',
          tabBarIcon: ({ color }) => (
            <MaterialIcons name="home" size={24} color={color} />
          ),
        }}
      />

      {/* 카메라 탭 */}
      <Tabs.Screen
        name="camera"
        options={{
          title: '카메라',
          tabBarIcon: ({ color }) => (
            <MaterialIcons name="photo-camera" size={24} color={color} />
          ),
        }}
      />

      {/* 설정 탭 */}
      <Tabs.Screen
        name="options"
        options={{
          title: '설정',
          tabBarIcon: ({ color }) => (
            <MaterialIcons name="settings" size={24} color={color} />
          ),
        }}
      />
    </Tabs>
  );
}
