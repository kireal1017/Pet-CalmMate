import { MaterialCommunityIcons, MaterialIcons } from '@expo/vector-icons';
import { Audio, ResizeMode, Video } from 'expo-av';
import { useRouter } from 'expo-router';
import React, { useEffect, useRef, useState } from 'react';
import { ActivityIndicator, Alert, StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { WebView } from 'react-native-webview';
import MusicPlayButton from '../share/music_play_button';
import { useAuth } from '../share/store/auth_store';

const API_BASE_URL = 'http://54.180.212.150/api';
const ENDPOINTS = {
  STREAM_URL: '/camera/stream-url',
  CAMERA_ON: '/camera/on',
  CAMERA_OFF: '/camera/off',
  DISPENSE_SNACK: '/dispense-snack',
  MIC_UPLOAD: '/speak-upload',
};

  const pet_camera: React.FC = () => {
  const router = useRouter();
  const { dogId, idloading } = useAuth();

  const [cameraActive, setCameraActive] = useState(true);

  const [streamUrl, setStreamUrl] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isActionLoading, setIsActionLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [videoUrl, setVideoUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const recordingRef = useRef(null);
  const [isUploading, setIsUploading] = useState(false);
  const [micActive, setMicActive] = useState(false);




  const videoRef = useRef<Video | null>(null);


  const htmlContent = `
    <html>
    <head>
      <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
      <style>
        body, html { margin:0; padding:0; height:100%; width:100%; background:#000; }
        video { width:100vw; height:100vh; }
      </style>
    </head>
    <body>
      <video id="video" controls autoplay></video>
      <script>
        var video = document.getElementById('video');
        var videoSrc = 'http://54.180.212.150:8080/hls/kvs-stream.m3u8';
        if (Hls.isSupported()) {
          var hls = new Hls();
          hls.loadSource(videoSrc);
          hls.attachMedia(video);
        } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
          video.src = videoSrc;
        }
      </script>
    </body>
    </html>
    `;

    // 로딩 중이면 로딩 UI만 표시
    if (idloading) {
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

  useEffect(() => {
    // 예시: 백엔드에서 영상 URL 받아오기
    fetchStreamUrl();
  }, []);

  const fetchStreamUrl = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_BASE_URL}${ENDPOINTS.STREAM_URL}`);
      if (!response.ok) throw new Error(`서버 오류: ${response.status}`);
      const data = await response.json();
      console.log('m3u8',data)
      if (data?.stream_url) {
        setStreamUrl(data.stream_url); 
      } else {
        throw new Error('스트림 URL이 없습니다.');
      }
    } catch (err) {
      setError('비디오 스트림을 불러올 수 없습니다');
      setStreamUrl(null);
    } finally {
      setIsLoading(false);
    }
};

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
  if (!streamUrl) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#6D4A42" />
        <Text style={styles.loadingText}>스트림 URL 없음</Text>
      </View>
    );
  }
  return (
    <Video
      key={streamUrl}
      ref={videoRef}
      style={styles.video}
      source={{ uri: streamUrl }}
      resizeMode={ResizeMode.CONTAIN}
      useNativeControls={false}
      isLooping={false}
      shouldPlay={cameraActive}
      onError={status => {
        console.log('expo-av Video error:', status);
        setError('비디오 스트림 재생 실패');
      }}
      onReadyForDisplay={() => setIsLoading(false)}
      onLoadStart={() => setIsLoading(true)}
    />
  );
};
// 녹음
const startRecording = async () => {
  try {
    setMicActive(true);
    await Audio.requestPermissionsAsync();
    await Audio.setAudioModeAsync({
      allowsRecordingIOS: true,
      playsInSilentModeIOS: true,
    });
    const { recording } = await Audio.Recording.createAsync(
      Audio.RecordingOptionsPresets.HIGH_QUALITY
    );
    recordingRef.current = recording;
  } catch (e) {
    setMicActive(false);
    Alert.alert('음성 전송 실패', "녹음 시간이 너무 짧습니다.");
  }
};

const stopAndUpload = async () => {
  setMicActive(false);
  if (!recordingRef.current) return;
  try {
    await recordingRef.current.stopAndUnloadAsync();
    const uri = recordingRef.current.getURI();
    if (!uri) throw new Error('녹음 파일 없음');

    setIsUploading(true);

    const formData = new FormData();
    formData.append('file', {
      uri,
      name: 'voice.m4a',
      type: 'audio/m4a',
    });

    const response = await fetch(API_BASE_URL + ENDPOINTS.MIC_UPLOAD, {
      method: 'POST',
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      body: formData,
    });

    if (response.ok) {
      const data = await response.json();
      //Alert.alert('녹음 전송 성공','');
    } else {
      const errorText = await response.text();
      console.error('서버 에러 응답:', errorText);
      Alert.alert('전송 실패');
    }
  } catch (e) {
    Alert.alert('녹음/전송 실패');
  } finally {
    setIsUploading(false);
    recordingRef.current = null;
  }
};

  // 카메라 상태 전환 (API 호출)
  const toggleCamera = async () => {
    setIsActionLoading(true);
    try {
      const endpoint = cameraActive ? ENDPOINTS.CAMERA_ON : ENDPOINTS.CAMERA_OFF;
      console.log(endpoint)
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      });
      if (!response.ok) throw new Error(`서버 오류: ${response.status}`);
      setCameraActive(!cameraActive);
      if (!cameraActive) {
        await fetchStreamUrl();
      } else {
        setStreamUrl(null);
      }
    } catch (err) {
      console.error('카메라 제어 오류:', err);
      Alert.alert('카메라 제어에 실패했습니다');
    } finally {
      setIsActionLoading(false);
    }
  };

  // 간식주기 API 호출
const dispenseSnack = async () => {
  setIsActionLoading(true);
  try {
    if (!dogId) {
      alert('강아지 정보가 없습니다.');
      setIsActionLoading(false);
      return;
    }
    const response = await fetch(`${API_BASE_URL}${ENDPOINTS.DISPENSE_SNACK}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ dog_id: dogId }), 
    });
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || `서버 오류: ${response.status}`);
    }
    const data = await response.json();
    //alert(data.message || '간식을 배출했습니다!');
  } catch (err) {
    //console.error('간식 배출 오류:', err);
    Alert.alert('간식을 배출하였습니다.')
  } finally {
    setIsActionLoading(false);
  }
};

  const [showBackground, setShowBackground] = useState(true);
  const [cameraEnabled, setCameraEnabled] = useState(false);

  const handleCameraButton = () => {
    setShowBackground(!showBackground);
    setCameraEnabled(!cameraEnabled);
  };



  return (
    <View style={styles.container}>
      <View style={styles.body}>
        <View style={styles.videoBox }>
          {cameraActive && (
            <View style={styles.overlayBackground}>
              <Text>카메라가 꺼져있습니다.</Text>
            </View>
          )}
          <WebView
            key="hls-webview"
            originWhitelist={['*']}
            source={{ html: htmlContent }}
            allowsInlineMediaPlayback
            mediaPlaybackRequiresUserAction={false}
            javaScriptEnabled
            domStorageEnabled
            style={{ width: '100%', aspectRatio: 4/3, backgroundColor: 'black' }}
          />
        </View>
        <View style={styles.buttonGrid}>
          <View style={styles.buttonRow}>
            <View style={styles.buttonCell}>
              <TouchableOpacity
                style={[
                  styles.circleButton,
                  cameraActive ? styles.inactiveButton : styles.activeButton,
                ]}
                onPress={toggleCamera}
                disabled={isActionLoading}
                activeOpacity={0.8}
              >
                {isActionLoading ? (
                  <ActivityIndicator color="#222" />
                ) : cameraActive ? (
                  <MaterialCommunityIcons name="camera-off" size={44} color="#222" />
                ) : (
                  <MaterialIcons name="photo-camera" size={44} color="#222" />
                )}
              </TouchableOpacity>
              <Text style={styles.buttonLabel}>카메라</Text>
            </View>
            <View style={styles.buttonCell}>
              <TouchableOpacity
                style={[
                  styles.circleButton,
                  styles.activeButton ,
                ]}
                onPressIn={startRecording}
                onPressOut={stopAndUpload}
                disabled={isUploading}
                activeOpacity={0.7}
              >
                <MaterialCommunityIcons name="microphone" size={44} color="#222" />
              </TouchableOpacity>
              <Text style={styles.buttonLabel}>마이크</Text>
            </View>
          </View>
            <View style={styles.buttonRow}>
              <View style={styles.buttonCell}>
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
              <View style={styles.buttonCell}>
                <MusicPlayButton isActionLoading={isActionLoading} />
              </View> 
          </View>
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff',paddingTop: 32, },
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
  buttonGrid: {
  width: 332,
  justifyContent: 'center',
  alignItems: 'center',
},
buttonRow: {
  flexDirection: 'row',
  justifyContent: 'space-between',
  width: '100%',
  marginBottom: 12,
},
buttonCell: {
  flex: 1,
  alignItems: 'center',
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
    coloredBackground: {
    backgroundColor: '#FFDEDE', 
  },
  overlayBackground: {
  ...StyleSheet.absoluteFillObject, 
  backgroundColor: '#E0E0E0',
  zIndex: 2, 
  justifyContent: 'center',
  alignItems: 'center',
},
});
export default pet_camera;