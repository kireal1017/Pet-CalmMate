// import React from 'react';
// import { StyleSheet, View } from 'react-native';
// import Video from 'react-native-video';

// export default function HLSPlayer() {
//   return (
//     <View style={styles.container}>
//       <Video
//         source={{ uri: 'http://54.180.212.150:8080/hls/kvs-stream.m3u8' }}
//         controls
//         resizeMode="contain"
//         paused={false}
//         repeat={true}
//         onError={e => console.log('Video error', e)}
//         onLoad={d => console.log('Video loaded', d)}
//         onBuffer={d => console.log('Buffering', d)}
//         style={{ width: '100%', height: 240, backgroundColor: 'black' }}
//         />
//     </View>
//   );
// }
// const styles = StyleSheet.create({
//   container: { flex: 1, justifyContent: 'center', alignItems: 'center' }
// });