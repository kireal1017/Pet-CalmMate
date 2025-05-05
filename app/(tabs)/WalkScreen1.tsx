import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, TextInput } from 'react-native';
import Header2 from './Header2';
import Footer from './Footer';
import { useRouter } from 'expo-router';


const getTodayString = () => {
  const today = new Date();
  const year = String(today.getFullYear()).slice(2); 
  const month = String(today.getMonth() + 1).padStart(2, '0');
  const date = String(today.getDate()).padStart(2, '0');
  return `${year}년 ${month}월 ${date}일`;
};

const WalkScreen1 = () => {
  const router = useRouter();
  const [activeTab, setActiveTab] = useState('측정');

  return (
    <View style={styles.container}>
      <Header2 />
      <View style={styles.body}>
       
        <View style={styles.tabContainer}>
          <TouchableOpacity 
            style={[
              styles.tabButton, 
              activeTab === '측정' ? styles.activeTab : styles.inactiveTab
            ]}
            onPress={() => {
                setActiveTab('측정'); 
                router.navigate('/(tabs)/WalkScreen2'); 
              }}
          >
            <Text style={styles.tabText}>측정</Text>
          </TouchableOpacity>
          <TouchableOpacity 
            style={[
              styles.tabButton, 
              activeTab === '기록' ? styles.activeTab : styles.inactiveTab
            ]}
            onPress={() => setActiveTab('기록')}
          >
            <Text style={styles.tabText}>기록</Text>
          </TouchableOpacity>
        </View>

        <Text style={styles.dateText}>{getTodayString()}</Text>
        <Text style={styles.title}>산책 기록</Text>

        <View style={styles.inputContainer}>
          <TextInput
            style={styles.input}
            placeholder="오늘 산책 km"
            placeholderTextColor="#b48b8b"
          />
        </View>

        <View style={styles.inputContainer}>
          <TextInput
            style={styles.input}
            placeholder="오늘 산책 시간:분:초"
            placeholderTextColor="#b48b8b"
          />
        </View>

        <TouchableOpacity 
          style={styles.submitButton}
          onPress={() => {
            router.navigate('/HomeScreen');
          }}
        >
          <Text style={styles.submitText}>작성 완료</Text>
        </TouchableOpacity>
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
  body: {
    flex: 1,
    alignItems: 'center',
    paddingTop: 10,
  },
  tabContainer: {
    flexDirection: 'row',
    marginBottom: 20,
    borderRadius: 25,
    borderWidth: 1,
    borderColor: '#FFD5D5',
    overflow: 'hidden',
    width: 200,
  },
  tabButton: {
    flex: 1,
    paddingVertical: 8,
    paddingHorizontal: 20,
    alignItems: 'center',
  },
  activeTab: {
    backgroundColor: '#FFD5D5',
  },
  inactiveTab: {
    backgroundColor: '#fff',
  },
  tabText: {
    fontSize: 16,
    color: '#222',
    fontWeight: '500',
  },
  dateText: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 4,
  },
  title: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  inputContainer: {
    width: '90%',
    marginBottom: 16,
  },
  input: {
    backgroundColor: '#FFE6E6',
    padding: 15,
    borderRadius: 8,
    width: '100%',
    fontSize: 16,
  },
  submitButton: {
    backgroundColor: '#FFE6E6',
    paddingVertical: 15,
    paddingHorizontal: 40,
    borderRadius: 8,
    marginTop: 20,
    width: '90%',
    alignItems: 'center',
  },
  submitText: {
    fontSize: 18,
    color: '#222',
    fontWeight: '500',
  },
});

export default WalkScreen1;
