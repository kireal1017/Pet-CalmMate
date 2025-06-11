import { useRouter } from 'expo-router';
import { Pedometer } from 'expo-sensors';
import React, { useEffect, useRef, useState } from 'react';
import { ActivityIndicator, Alert, StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { useAuth } from '../share/store/auth_store';

const getTodayString = () => {
  const today = new Date();
  const year = String(today.getFullYear()).slice(2);
  const month = String(today.getMonth() + 1).padStart(2, '0');
  const date = String(today.getDate()).padStart(2, '0');
  return `${year}년 ${month}월 ${date}일`;
};

const formatTime = (seconds) => {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = seconds % 60;
  return `${hours.toString().padStart(2, '0')}:${minutes
    .toString()
    .padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
};

function calculateDistance(steps) {
  if (steps <= 28) {
    return Number(((steps / 14) * 0.01).toFixed(2));
  } else {
    const extra_steps = steps - 28;
    const extra_distance = 0.02 * (extra_steps / 14);
    return Number((0.02 + extra_distance).toFixed(2));
  }
}

const pet_walk = () => {
  const { dogId, loading } = useAuth();
  const router = useRouter();
  const [activeButton, setActiveButton] = useState(null);
  const [seconds, setSeconds] = useState(0);
  const [distance, setDistance] = useState(0);
  const [isPaused, setIsPaused] = useState(true);
  const [stepCount, setStepCount] = useState(0);
  const [initialStepCount, setInitialStepCount] = useState(null);

  const timerRef = useRef(null);
  const pedometerSubscription = useRef(null);
  const initialStepCountRef = useRef(null);

  // 타이머 시작
  const startTimer = () => {
    if (timerRef.current !== null) return;
    timerRef.current = setInterval(() => {
      setSeconds((prev) => prev + 1);
    }, 1000);
  };

  // 타이머 일시정지
  const pauseTimer = () => {
    if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }
  };

  // 만보기 시작
 const startPedometer = async () => {
  if (pedometerSubscription.current) return;

  const { granted } = await Pedometer.requestPermissionsAsync();
  if (!granted) {
    Alert.alert('만보기 권한이 필요합니다.');
    return;
  }

  const isAvailable = await Pedometer.isAvailableAsync();
  if (!isAvailable) {
    Alert.alert('이 기기는 만보계 센서를 지원하지 않습니다.');
    return;
  }

  if (initialStepCountRef.current === null) {
    initialStepCountRef.current = 0;
    setInitialStepCount(0);
    setStepCount(0);
  }

  pedometerSubscription.current = Pedometer.watchStepCount((result) => {
    if (initialStepCountRef.current === null) return;
    const stepsWalked = result.steps - initialStepCountRef.current;
    setStepCount(stepsWalked > 0 ? stepsWalked : 0);
  });
};

  // 만보기 일시정지
  const pausePedometer = () => {
    if (pedometerSubscription.current) {
      pedometerSubscription.current.remove();
      pedometerSubscription.current = null;
    }
  };

  // stepCount 변할 때마다 거리 즉시 갱신
  useEffect(() => {
    setDistance(calculateDistance(stepCount));
  }, [stepCount]);

  // 산책 종료 및 서버 전송
  const finishWalk = async () => {
    pauseTimer();
    pausePedometer();

    if (!dogId) {
      Alert.alert('강아지 정보가 없습니다.');
      return;
    }

    const walk_distance = distance;
    const walk_duration = seconds;
    const date_time = new Date().toISOString().slice(0, 19);

    try {
      const response = await fetch('http://54.180.212.150/api/walk', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          dog_id: dogId,
          walk_distance,
          walk_duration,
          date_time,
        }),
      });
      const data = await response.json();
      if (response.ok) {
        Alert.alert('산책 기록 완료!', `시간: ${formatTime(seconds)}, 거리: ${distance.toFixed(2)}km`);
        router.navigate('/(tabs)/main_home');
      } else {
        Alert.alert('서버 오류', data.error || '산책 기록에 실패했습니다.');
      }
    } catch (e) {
      Alert.alert('네트워크 오류', '서버에 연결할 수 없습니다.');
    }
  };

  // 버튼 핸들링
  const handleButtonPress = async (buttonName) => {
    setActiveButton(buttonName);

    if (buttonName === '산책 중') {
      setIsPaused(false);
      startTimer();
      await startPedometer();
    } else if (buttonName === '일시정지') {
      setIsPaused(true);
      pauseTimer();
      pausePedometer();
    } else if (buttonName === '마치기') {
      finishWalk();
    }
  };

  // 언마운트 시 타이머/만보계 정리
  useEffect(() => {
    return () => {
      pauseTimer();
      pausePedometer();
    };
  }, []);

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#FF6B6B" />
        <Text>로딩 중...</Text>
      </View>
    );
  }

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

  return (
    <View style={styles.container}>
      <View style={styles.body}>
        <Text style={styles.dateText}>{getTodayString()}</Text>
        <Text style={styles.title}>산책 기록</Text>
        <View style={styles.infoBox}>
          <Text style={styles.infoText}>{formatTime(seconds)}</Text>
        </View>
        <View style={styles.infoBox}>
          <Text style={styles.infoText}>{distance.toFixed(2)}km</Text>
        </View>
        <View style={styles.infoBox}>
          <Text style={styles.infoText}>{stepCount} 걸음</Text>
        </View>
        <View style={styles.buttonGroup}>
          <TouchableOpacity
            style={[
              styles.actionButton,
              activeButton === '일시정지' ? styles.activeButton : styles.inactiveButton,
            ]}
            onPress={() => handleButtonPress('일시정지')}
          >
            <Text style={styles.buttonIcon}>⏸️</Text>
            <Text style={styles.buttonText}>일시정지</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[
              styles.actionButton,
              activeButton === '산책 중' ? styles.activeButton : styles.inactiveButton,
            ]}
            onPress={() => handleButtonPress('산책 중')}
          >
            <Text style={styles.buttonIcon}>▶️</Text>
            <Text style={styles.buttonText}>산책 중</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[
              styles.actionButton,
              activeButton === '마치기' ? styles.activeButton : styles.inactiveButton,
            ]}
            onPress={() => handleButtonPress('마치기')}
          >
            <Text style={styles.buttonIcon}>⏹️</Text>
            <Text style={styles.buttonText}>마치기</Text>
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
  body: {
    flex: 1,
    alignItems: 'center',
    paddingTop: 10,
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
  infoBox: {
    backgroundColor: '#FFE6E6',
    padding: 15,
    borderRadius: 8,
    width: '90%',
    marginBottom: 16,
    alignItems: 'center',
  },
  infoText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#222',
  },
  buttonGroup: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    width: '100%',
    marginTop: 40,
  },
  actionButton: {
    alignItems: 'center',
    justifyContent: 'center',
    width: 80,
    height: 80,
    borderRadius: 40,
    borderWidth: 1,
    borderColor: '#FFD5D5',
  },
  activeButton: {
    backgroundColor: '#FFDEDE',
  },
  inactiveButton: {
    backgroundColor: '#fff',
  },
  buttonIcon: {
    fontSize: 24,
    marginBottom: 5,
    color: 'black',
  },
  buttonText: {
    fontSize: 12,
    color: '#222',
    fontWeight: 'bold',
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

export default pet_walk;
