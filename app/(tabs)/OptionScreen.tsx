import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import Header2 from './Header2';
import Footer from './Footer';
import { useRouter } from 'expo-router';

const OptionScreen = () => {
  const router = useRouter();
  return (
    <View style={styles.container}>
      <Header2/>
      <View style={styles.content}>
       
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>장치 관리</Text>
          <TouchableOpacity
            style={styles.optionButton}
            onPress={() => router.navigate('/(tabs)/DeviceConnectScreen')}
          >
            <Text style={styles.optionText}>장치 연결</Text>
          </TouchableOpacity>
        </View>

     
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>계정 관리</Text>
          <TouchableOpacity style={styles.optionButton}>
            <Text style={styles.optionText}>로그아웃</Text>
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
    paddingHorizontal: 15,
  },
  section: {
    marginVertical: 10,
  },
  sectionTitle: {
    fontSize: 11.12,
    fontWeight: 'bold',
    marginBottom: 5,
    color: '#333',
  },
  optionButton: {
    paddingVertical: 10,
    borderBottomWidth: 0.5,
    borderBottomColor: '#FF9999',
    borderTopWidth: 1,
    borderTopColor: '#FF9999',
    justifyContent: 'space-between',
    flexDirection: 'row',
  },
  optionText: {
    fontSize: 11,
    color: '#333',
  },
});

export default OptionScreen;
