import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { useRouter } from 'expo-router';
import Header from './Header2';
import Footer from './Footer';

const DeviceConnectScreen: React.FC = () => {
  const router = useRouter();

  const handleConnectDevice = () => {
    console.log('장치 연결 시작');
  };

  return (
    <View style={styles.container}>
      <Header />
      
      <View style={styles.content}>
        <View style={styles.centerContainer}>
          <Text style={styles.noDeviceText}>연결된 장치가 없습니다.</Text>
          <TouchableOpacity 
            style={styles.connectButton}
            onPress={handleConnectDevice}
          >
            <Text style={styles.connectButtonText}>장치 연결하기</Text>
          </TouchableOpacity>
        </View>
      </View>
      
      <Footer />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  content: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  centerContainer: {
    alignItems: 'center',
  },
  noDeviceText: {
    fontSize: 14,
    color: '#333',
    marginBottom: 20,
  },
  connectButton: {
    width: 233,
    height: 59,
    backgroundColor: '#FFCACA',
    borderRadius: 8,
    justifyContent: 'center',
    alignItems: 'center',
  },
  connectButtonText: {
    fontSize: 16,
    color: '#333',
  },
});

export default DeviceConnectScreen;
