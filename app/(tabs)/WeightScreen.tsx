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

const WeightScreen = () => {
  const [weight, setWeight] = useState('');
  const router = useRouter();

  return (
    <View style={styles.container}>
      <Header2 />
      <View style={styles.body}>
        <Text style={styles.title}>{getTodayString()}</Text>
        <Text style={styles.subtitle}>체중 기록</Text>
        <View style={styles.inputRow}>
          <TextInput
            style={styles.input}
            value={weight}
            onChangeText={setWeight}
            placeholder="오늘의 체중은?"
            placeholderTextColor="#b48b8b"
            keyboardType="numeric"
            maxLength={5}
          />
          <Text style={styles.unit}>kg</Text>
        </View>
        <TouchableOpacity style={styles.button} onPress={() => router.navigate('/(tabs)/HomeScreen')}>
          <Text style={styles.buttonText}>작성 완료</Text>
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
    paddingTop: 28,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    marginTop: 6,
    textAlign: 'center',
    color: '#111',
  },
  subtitle: {
    fontSize: 16,
    fontWeight: 'bold',
    marginTop: 2,
    marginBottom: 24,
    textAlign: 'center',
    color: '#111',
  },
  inputRow: {
    flexDirection: 'row',
    alignItems: 'center',
    width: 230,
    marginBottom: 30,
  },
  input: {
    flex: 1,
    height: 36,
    backgroundColor: '#FFE3E3',
    borderRadius: 4,
    paddingHorizontal: 10,
    fontSize: 15,
    color: '#222',
  },
  unit: {
    marginLeft: 8,
    fontSize: 15,
    color: '#222',
    fontWeight: '500',
  },
  button: {
    marginTop: 18,
    width: 220,
    height: 44,
    backgroundColor: '#FFE3E3',
    borderRadius: 6,
    justifyContent: 'center',
    alignItems: 'center',
    elevation: 1,
  },
  buttonText: {
    fontSize: 18,
    color: '#222',
    fontWeight: '500',
    letterSpacing: 1,
  },
});

export default WeightScreen;
