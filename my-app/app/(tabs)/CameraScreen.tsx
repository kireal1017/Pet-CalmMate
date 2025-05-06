import React, { useState, useEffect, useRef } from 'react';
import { View, StyleSheet, Text, TouchableOpacity, ActivityIndicator } from 'react-native';
import { MaterialIcons, MaterialCommunityIcons } from '@expo/vector-icons';
//import Video from 'react-native-video';
import { Video } from 'expo-av';
import { ResizeMode } from 'expo-av';
import Header from './Header2';
import Footer from './Footer';

// Flask API 기본 URL과 엔드포인트
const API_BASE_URL = 'http://54.180.212.150/api';
const ENDPOINTS = {
  STREAM_URL: '/camera/stream-url',
  CAMERA_ON: '/camera/on',
  CAMERA_OFF: '/camera/off',
  DISPENSE_SNACK: '/dispense-snack'
};

const CameraScreen = () => {
  const [cameraActive, setCameraActive] = useState(true);
  const [micActive, setMicActive] = useState(true);
  const [streamUrl, setStreamUrl] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isActionLoading, setIsActionLoading] = useState(false);
  const [error, setError] = useState(null);
  const videoRef = useRef(null);

  // Flask API에서 HLS 스트림 URL 가져오기
  useEffect(() => {
    fetchStreamUrl();
  }, []);

  const fetchStreamUrl = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`${API_BASE_URL}${ENDPOINTS.STREAM_URL}`);
      
      if (!response.ok) {
        throw new Error(`서버 오류: ${response.status}`);
      }
      
      const data = await response.json();
      setStreamUrl(data.stream_url);
    } catch (err) {
      console.error('스트림 URL 가져오기 오류:', err);
      setError('비디오 스트림을 불러올 수 없습니다');
    } finally {
      setIsLoading(false);
    }
  };

  // 카메라 상태 전환 (API 호출)
  const toggleCamera = async () => {
    setIsActionLoading(true);
    
    try {
      const endpoint = cameraActive ? ENDPOINTS.CAMERA_OFF : ENDPOINTS.CAMERA_ON;
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      if (!response.ok) {
        throw new Error(`서버 오류: ${response.status}`);
      }
      
      const data = await response.json();
      setCameraActive(!cameraActive);
      
      // 카메라를 켤 때 스트림 URL 새로고침
      // if (!cameraActive) {
      //   fetchStreamUrl();
      // }
    } catch (err) {
      console.error('카메라 제어 오류:', err);
      alert('카메라 제어에 실패했습니다');
    } finally {
      setIsActionLoading(false);
    }
  };

  // 간식주기 API 호출
  const dispenseSnack = async () => {
    setIsActionLoading(true);
    
    try {
      const response = await fetch(`${API_BASE_URL}${ENDPOINTS.DISPENSE_SNACK}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ dog_id: 1 }),
      });
      
      if (!response.ok) {
        throw new Error(`서버 오류: ${response.status}`);
      }
      
      const data = await response.json();
      alert('간식을 배출했습니다!');
    } catch (err) {
      console.error('간식 배출 오류:', err);
      alert('간식 배출에 실패했습니다');
    } finally {
      setIsActionLoading(false);
    }
  };

  // 비디오 콘텐츠 렌더링 함수
  const renderVideoContent = () => {
    if (isLoading) {
      return (
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="#6D4A42" />
          <Text style={styles.loadingText}>스트림 로딩 중...</Text>
        </View>
      );
    }
    
    if (error) {
      return (
        <View style={styles.errorContainer}>
          <MaterialCommunityIcons name="alert-circle-outline" size={50} color="#222" />
          <Text style={styles.errorText}>{error}</Text>
          <Text style={styles.errorText}>{streamUrl}</Text>
          <TouchableOpacity style={styles.retryButton} onPress={fetchStreamUrl}>
            <Text style={styles.retryText}>다시 시도</Text>
          </TouchableOpacity>
        </View>
      );
    }
    
    if (!cameraActive) {
      return (
        <View style={styles.cameraInactive}>
          <View style={styles.diagonalLine} />
          <Text style={styles.inactiveText}>카메라가 꺼져 있습니다</Text>
        </View>
      );
    }
    
    return (
      <Video
        ref={videoRef}
        style={styles.video}
        source={{ uri: streamUrl! }}
        useNativeControls
        resizeMode={ResizeMode.CONTAIN}
        isLooping
        shouldPlay={cameraActive}
        onError={(error) => {
          console.log('비디오 오류:', error);
          setError('스트리밍 재생 실패');
        }}
      />
    );
  };

  return (
    <View style={styles.container}>
      <Header />
      <View style={styles.body}>
        {/* 비디오 표시 박스 */}
        <View style={styles.videoBox}>
          {renderVideoContent()}
        </View>
        
        {/* 버튼 영역 */}
        <View style={styles.buttonRow}>
          {/* 카메라 버튼 */}
          <View style={styles.buttonCol}>
            <TouchableOpacity
              style={[
                styles.circleButton,
                cameraActive ? styles.activeButton : styles.inactiveButton,
              ]}
              onPress={toggleCamera}
              disabled={isActionLoading}
              activeOpacity={0.8}
            >
              {isActionLoading ? (
                <ActivityIndicator color="#222" />
              ) : cameraActive ? (
                <MaterialIcons name="photo-camera" size={44} color="#222" />
              ) : (
                <MaterialCommunityIcons name="camera-off" size={44} color="#222" />
              )}
            </TouchableOpacity>
            <Text style={styles.buttonLabel}>카메라</Text>
          </View>
          
          {/* 마이크 버튼 */}
          <View style={styles.buttonCol}>
            <TouchableOpacity
              style={[
                styles.circleButton,
                micActive ? styles.activeButton : styles.inactiveButton,
              ]}
              onPress={() => setMicActive((prev) => !prev)}
              activeOpacity={0.8}
            >
              {micActive ? (
                <MaterialCommunityIcons name="microphone" size={44} color="#222" />
              ) : (
                <MaterialCommunityIcons name="microphone-off" size={44} color="#222" />
              )}
            </TouchableOpacity>
            <Text style={styles.buttonLabel}>마이크</Text>
          </View>
          
          {/* 간식주기 버튼 */}
          <View style={styles.buttonCol}>
            <TouchableOpacity
              style={[styles.circleButton, styles.activeButton]}
              onPress={dispenseSnack}
              disabled={isActionLoading}
              activeOpacity={0.8}
            >
              {isActionLoading ? (
                <ActivityIndicator color="#222" />
              ) : (
                <MaterialCommunityIcons name="cookie" size={44} color="#222" />
              )}
            </TouchableOpacity>
            <Text style={styles.buttonLabel}>간식주기</Text>
          </View>
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
  body: {
    flex: 1,
    alignItems: 'center',
    paddingTop: 24,
    paddingBottom: 12,
    backgroundColor: '#fff',
  },
  videoBox: {
    width: 640,
    height: 480,
    borderRadius: 8,
    backgroundColor: '#fff',
    marginBottom: 36,
    borderWidth: 1,
    borderColor: '#222',
    overflow: 'hidden',
    alignItems: 'center',
    justifyContent: 'center',
  },
  video: {
    width: 640,
    height: 480,
    borderRadius: 8,
    backgroundColor: '#000',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    marginTop: 10,
    fontSize: 16,
    color: '#222',
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  errorText: {
    marginTop: 10,
    fontSize: 16,
    color: '#222',
    textAlign: 'center',
  },
  retryButton: {
    marginTop: 20,
    paddingVertical: 8,
    paddingHorizontal: 16,
    backgroundColor: '#6D4A42',
    borderRadius: 8,
  },
  retryText: {
    color: '#fff',
    fontSize: 14,
  },
  cameraInactive: {
    width: 332,
    height: 332,
    backgroundColor: '#666666',
    borderRadius: 8,
    alignItems: 'center',
    justifyContent: 'center',
  },
  inactiveText: {
    color: '#fff',
    fontSize: 16,
    marginTop: 40,
  },
  diagonalLine: {
    position: 'absolute',
    left: 0,
    top: 0,
    width: 332,
    height: 332,
    borderLeftWidth: 2,
    borderColor: '#222',
    transform: [{ rotate: '45deg' }],
  },
  buttonRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    width: 332,
    marginBottom: 8,
  },
  buttonCol: {
    alignItems: 'center',
    flex: 1,
  },
  circleButton: {
    width: 103,
    height: 103,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
    marginHorizontal: 6,
    marginBottom: 6,
    elevation: 2,
  },
  activeButton: {
    backgroundColor: '#FFDEDE',
  },
  inactiveButton: {
    backgroundColor: '#6D4A42',
  },
  buttonLabel: {
    fontSize: 15,
    fontWeight: '500',
    color: '#222',
    textAlign: 'center',
    marginTop: 2,
  },
});

export default CameraScreen;
