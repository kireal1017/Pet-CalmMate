// import React, { useRef, useState } from 'react';
// import { ActivityIndicator, StyleSheet, Text, View } from 'react-native';
// import { ResizeMode, Video } from 'react-native-video';

// export default function M3U8Player() {
//   const videoRef = useRef(null);
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState<string | null>(null);

//   const handleVideoLoadStart = () => {
//     console.log('Video Load Start');
//     setLoading(true);
//     setError(null); // 새로운 로딩 시작 시 에러 초기화
//   };

//   const handleVideoReadyForDisplay = () => {
//     console.log('Video Ready for Display');
//     setLoading(false);
//   };

//   const handleVideoError = (e: any) => { // 에러 타입 명시를 위해 'any' 사용
//     console.error('Video Playback Error:', e);
//     let errorMessage = '비디오 재생 오류가 발생했습니다.';
//     if (e.error && e.error.localizedDescription) {
//       errorMessage = `비디오 오류: ${e.error.localizedDescription}`;
//     } else if (e.error) {
//       errorMessage = `비디오 오류: ${JSON.stringify(e.error)}`;
//     } else if (e.nativeEvent && e.nativeEvent.error) {
//       errorMessage = `비디오 오류: ${e.nativeEvent.error}`;
//     }
//     setError(errorMessage);
//     setLoading(false);
//   };

//   return (
//     <View style={styles.container}>
//       <Video
//         ref={videoRef}
//         style={styles.video}
//         source={{ uri: 'http://54.180.212.150:8080/hls/kvs-stream.m3u8' }}
//         controls // useNativeControls 대신 controls 사용
//         useExoPlayer={true} // Android에서 HLS 지원
//         resizeMode={ResizeMode.CONTAIN}
//         paused={false} // shouldPlay 대신 paused={false} 또는 playInBackground={true} 등을 고려
//         repeat // isLooping 대신 repeat 사용
//         onLoadStart={handleVideoLoadStart}
//         onReadyForDisplay={handleVideoReadyForDisplay}
//         onError={handleVideoError}
//         // onBuffer={(buffer) => console.log('Buffering:', buffer.isBuffering)} // 버퍼링 상태 확인용
//         // onProgress={(progress) => console.log('Progress:', progress.currentTime)} // 재생 시간 확인용
//       />
//       {loading && (
//         <View style={styles.overlay}>
//           <ActivityIndicator size="large" color="#fff" />
//           <Text style={styles.loadingText}>비디오를 불러오는 중...</Text>
//         </View>
//       )}
//       {error && (
//         <View style={styles.overlay}>
//           <Text style={styles.errorText}>{error}</Text>
//         </View>
//       )}
//     </View>
//   );
// }

// const styles = StyleSheet.create({
//   container: { flex: 1, backgroundColor: '#000', justifyContent: 'center', alignItems: 'center' },
//   video: { width: '100%', aspectRatio: 16 / 9, backgroundColor: '#000' },
//   overlay: {
//     position: 'absolute',
//     top: 0,
//     left: 0,
//     right: 0,
//     bottom: 0,
//     justifyContent: 'center',
//     alignItems: 'center',
//     backgroundColor: 'rgba(0,0,0,0.5)', // 오버레이 배경색 추가
//   },
//   loadingText: {
//     color: '#fff',
//     marginTop: 10,
//     fontSize: 16,
//   },
//   errorText: {
//     color: 'red',
//     fontSize: 16,
//     textAlign: 'center',
//     marginHorizontal: 20,
//   },
// });