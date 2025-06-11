import { useRouter } from 'expo-router';
import React, { useState } from 'react';
import { ActivityIndicator, Alert, StyleSheet, Text, TextInput, TouchableOpacity, View } from 'react-native';
import { useAuth } from '../share/store/auth_store';

const pet_weight = () => {
  const { dogId, loading } = useAuth();
  const [weight, setWeight] = useState('');
  const router = useRouter();

     if (!dogId) {
     return (
       <View style={styles.loadingContainer}>
         <Text>강아지 정보가 없습니다.</Text>
         <TouchableOpacity
            style={styles.registerButton}
            onPress={() => router.push('/pet_add')}
            activeOpacity={0.8}
          >
            <Text style={styles.registerButtonText}>강아지 등록하기</Text>
          </TouchableOpacity>
          
       </View>
     ); 
   }

  const getTodayString = () => {
    const today = new Date();
    const year = String(today.getFullYear()).slice(2);
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const date = String(today.getDate()).padStart(2, '0');
    return `${year}년 ${month}월 ${date}일`;
  };

  const getTodayISO = () => {
    const today = new Date();
    return today.toISOString().split('T')[0];
  };

  const handleSubmit = async () => {
    if (!weight) {
      Alert.alert('체중을 입력해주세요.');
      return;
    }

    const weightValue = parseFloat(weight);
    if (isNaN(weightValue) || weightValue <= 0) {
      Alert.alert('유효한 체중을 입력해주세요.');
      return;
    }

    try {
      const response = await fetch('http://54.180.212.150/api/weight', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          dog_id: dogId,
          weight: weightValue,
          date: getTodayISO(),
        }),
      });

      const data = await response.json();

      if (response.ok) {
        Alert.alert('체중이 성공적으로 기록되었습니다.');
        router.navigate('/(tabs)/main_home');
      } else {
        Alert.alert('오류', '오늘은 이미 체중기록을 하였습니다.');
      }
    } catch (error) {
      Alert.alert('네트워크 오류', '서버에 연결할 수 없습니다.');
    }
  };

  // 로딩 중일 때는 로딩 UI만 보여줌
  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#FF6B6B" />
        <Text>로딩 중...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
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
        <TouchableOpacity style={styles.button} onPress={handleSubmit}>
          <Text style={styles.buttonText}>작성 완료</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    paddingTop: 32,
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
    fontSize: 12,
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
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
    registerButton: {
    backgroundColor: '#FFE3E3',
    borderRadius: 12,
    paddingVertical: 16,
    paddingHorizontal: 24,
    width: '100%',
    alignItems: 'center',
    marginBottom: 16,
    borderWidth: 1,
    borderColor: '#FFD1D1',
  },
  registerButtonText: {
    color: '#A55B5B',
    fontSize: 16,
    fontWeight: 'bold',
  },
});

export default pet_weight;
