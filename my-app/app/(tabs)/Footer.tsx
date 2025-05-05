import React from 'react';
import { View, StyleSheet, TouchableOpacity, Text } from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';

const Footer: React.FC = () => {
  const router = useRouter();

  return (
    <View style={styles.footer}>
      <TouchableOpacity style={styles.tab} onPress={() => router.navigate('/(tabs)/ChartScreen')}>
        <MaterialIcons name="insert-chart" size={28} color="#222" />
        <Text style={styles.tabText}>통계</Text>
      </TouchableOpacity>
      <TouchableOpacity style={styles.tab} onPress={() => router.navigate('/(tabs)/HomeScreen')}>
        <MaterialIcons name="home" size={28} color="#222" />
        <Text style={styles.tabText}>홈</Text>
      </TouchableOpacity>
      <TouchableOpacity style={styles.tab} onPress={() => router.navigate('/(tabs)/GroupScreen')}>
        <MaterialIcons name="group" size={28} color="#222" />
        <Text style={styles.tabText}>그룹</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  footer: {
    height: 65,
    width: '100%',
    flexDirection: 'row',
    borderTopWidth: 1,
    borderTopColor: '#D9D9D9',
    backgroundColor: '#fff',
    justifyContent: 'space-around',
    alignItems: 'center',
  },
  tab: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  tabText: {
    fontSize: 12,
    marginTop: 4,
    color: '#222',
  },
});

export default Footer;
