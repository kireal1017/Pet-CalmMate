import FontAwesome from '@expo/vector-icons/FontAwesome';
import { Tabs } from 'expo-router';

export default function TabLayout() {
  return (
    
    <Tabs screenOptions={{ tabBarActiveTintColor: '#222',headerShown: false }}>
      <Tabs.Screen
        name="chart_chart"
        options={{
          title: '통계',
          tabBarLabel: '통계',
          tabBarIcon: ({ color }) => <FontAwesome size={28} name="bar-chart" color={color} />,
        }}
      />
      <Tabs.Screen
        name="main_home"
        options={{
          title: '홈',
          tabBarLabel: '홈',
          tabBarIcon: ({ color }) => <FontAwesome size={28} name="home" color={color} />,
        }}
      />
      <Tabs.Screen
        name="option_option"
        options={{
          title: '옵션',
          tabBarLabel: '옵션',
          tabBarIcon: ({ color }) => <FontAwesome size={28} name="cog" color={color} />,
        }}
      />
    </Tabs>
  );
}
