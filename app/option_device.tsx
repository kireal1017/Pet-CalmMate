import { useRouter } from 'expo-router';
import React, { useState } from 'react';
import { Alert, StyleSheet, Text, TextInput, TouchableOpacity, View } from 'react-native';
import { useAuth } from '../share/store/auth_store';

const DeviceConnectScreen: React.FC = () => {
  const router = useRouter();
  const { dogId } = useAuth(); 

  const [deviceId, setDeviceId] = useState('');
  const [loading, setLoading] = useState(false);

  const handleConnectDevice = async () => {
    if (!deviceId) {
      Alert.alert('기기 ID를 입력해주세요.');
      return;
    }
    if (!dogId) {
      Alert.alert('강아지 정보가 없습니다.');
      return;
    }
    setLoading(true);
    try {
      const response = await fetch('http://54.180.212.150/api/register-device', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ device_id: deviceId, dog_id: dogId }),
      });
      const data = await response.json();
      if (response.ok) {
        Alert.alert('기기 등록 성공', '', [
          { text: '확인', onPress: () => router.back() }
        ]);
      } else {
        Alert.alert('등록 실패', data.error || data.message || '기기 등록에 실패했습니다.');
      }
    } catch (error) {
      Alert.alert('등록 실패', '올바르지 않은 기기 ID입니다.');
    }
    setLoading(false);
  };

  return (
    <View style={styles.container}>
      <View style={styles.content}>
        <View style={styles.centerContainer}>
          <Text style={styles.label}>기기 ID를 입력하세요</Text>
          <TextInput
            style={styles.input}
            value={deviceId}
            onChangeText={setDeviceId}
            placeholder="기기 ID 입력"
            autoCapitalize="none"
            autoCorrect={false}
            editable={!loading}
          />
          <TouchableOpacity
            style={styles.connectButton}
            onPress={handleConnectDevice}
            disabled={loading}
          >
            <Text style={styles.connectButtonText}>
              {loading ? '연결 중...' : '장치 연결하기'}
            </Text>
          </TouchableOpacity>
        </View>
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
  content: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  centerContainer: {
    alignItems: 'center',
    width: '100%',
  },
  label: {
    fontSize: 15,
    color: '#333',
    marginBottom: 18,
  },
  input: {
    width: 233,
    height: 48,
    backgroundColor: '#FFE3E3',
    borderRadius: 8,
    paddingHorizontal: 12,
    fontSize: 16,
    color: '#222',
    marginBottom: 18,
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
