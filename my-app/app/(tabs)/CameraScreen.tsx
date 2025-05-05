import React, { useState } from 'react';
import { View, StyleSheet, Text, TouchableOpacity, Dimensions } from 'react-native';
import { MaterialIcons, MaterialCommunityIcons } from '@expo/vector-icons';
import Header from './Header2';
import Footer from './Footer';
import Video from 'react-native-video';

const BOX_SIZE = 332;
const VIDEO_HEIGHT = 332; 
const VIDEO_URL = 'https://www.w3schools.com/html/mov_bbb.mp4'; 

const CameraScreen = () => {
  const [cameraActive, setCameraActive] = useState(true);
  const [micActive, setMicActive] = useState(true);

  return (
    <View style={styles.container}>
      <Header />
      <View style={styles.body}>
      
        <View style={styles.videoBox}>
          {cameraActive ? (
            <Video
              source={{ uri: VIDEO_URL }}
              style={styles.video}
              resizeMode="cover"
              repeat
              paused={false}
              muted={!micActive}
              controls={false}
            />
          ) : (
            <View style={styles.cameraInactive}>
              <View style={styles.diagonalLine} />
            </View>
          )}
        </View>
     
        <View style={styles.buttonRow}>
          <View style={styles.buttonCol}>
            <TouchableOpacity
              style={[
                styles.circleButton,
                cameraActive ? styles.activeButton : styles.inactiveButton,
              ]}
              onPress={() => setCameraActive((prev) => !prev)}
              activeOpacity={0.8}
            >
              {cameraActive ? (
                <MaterialIcons name="photo-camera" size={44} color="#222" />
              ) : (
                <MaterialCommunityIcons name="camera-off" size={44} color="#222" />
              )}
            </TouchableOpacity>
            <Text style={styles.buttonLabel}>카메라</Text>
          </View>
  
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
       
          <View style={styles.buttonCol}>
            <TouchableOpacity
              style={[styles.circleButton, styles.activeButton]}
              activeOpacity={0.8}
              onPress={() => {}}
            >
              <MaterialCommunityIcons name="cookie" size={44} color="#222" />
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
    width: BOX_SIZE,
    height: 414,
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
    width: BOX_SIZE,
    height: VIDEO_HEIGHT,
    borderRadius: 8,
    backgroundColor: '#000',
  },
  cameraInactive: {
    width: BOX_SIZE,
    height: VIDEO_HEIGHT,
    backgroundColor: '#666666',
    borderRadius: 8,
    alignItems: 'center',
    justifyContent: 'center',
  },
  diagonalLine: {
    position: 'absolute',
    left: 0,
    top: 0,
    width: BOX_SIZE,
    height: VIDEO_HEIGHT,
    borderLeftWidth: 2,
    borderColor: '#222',
    transform: [{ rotate: '45deg' }],
  },
  buttonRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    width: BOX_SIZE,
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
