import { Audio } from 'expo-av';
import * as ImagePicker from 'expo-image-picker';
import { LinearGradient } from 'expo-linear-gradient';
import { useRouter } from 'expo-router';
import { Pedometer } from 'expo-sensors';
import React, { useEffect } from 'react';
import { Image, StyleSheet, Text, TouchableOpacity, } from 'react-native';



const auth_main: React.FC = () => {
    const router = useRouter();
    useEffect(() => {
    const requestPermissions = async () => {
      await Audio.requestPermissionsAsync();
      await ImagePicker.requestCameraPermissionsAsync();
      await ImagePicker.requestMediaLibraryPermissionsAsync();
      await Pedometer.requestPermissionsAsync(); 
    };
    requestPermissions();
  }, []);

    return (
        <LinearGradient
          colors={['#FFDEDE', '#FFFFFF']}
          style={styles.container}
        >
          <Text style={styles.title}>냥멍케어</Text>
          <Text style={styles.subtitle}>안심되는 우리 강아지 관리</Text>
          <Image
            source={require('../assets/images/dog_logo.png')} 
            style={styles.dogImage}
            resizeMode="contain"
          />
          <TouchableOpacity
            style={styles.loginButton}
            onPress={() => router.push('/auth_login')}
          >
            <Text style={styles.loginButtonText}>냥멍케어 로그인</Text>
          </TouchableOpacity>
          {/* <TouchableOpacity
            style={[styles.loginButton, styles.kakaoButton]}
            onPress={() => router.push('/auth_kakao')}
          >
            <Text style={styles.kakaoButtonText}>카카오톡으로 로그인</Text>
          </TouchableOpacity> */}
          <TouchableOpacity onPress={() => router.push('/auth_register')}>
            <Text>
              냥멍케어 회원가입
            </Text>
          </TouchableOpacity>
        </LinearGradient>
    );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  // 나머지 스타일은 기존과 동일하게 사용
  title: {
    width: 262,
    height: 82,
    fontSize: 48,
    fontWeight: 'bold',
    textAlign: 'center',
    color: '#fff',
    marginTop: 40,
  },
  subtitle: {
    width: 139,
    height: 28,
    fontSize: 12,
    fontWeight: 'bold',
    textAlign: 'center',
    color: '#fff',
    marginBottom: 30,
  },
  dogImage: {
    width: 200,
    height: 200,
    marginVertical: 30,
  },
  loginButton: {
    width: 254,
    height: 56,
    borderRadius: 5,
    backgroundColor: '#fff',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 16,
    borderRightWidth: 1,
    borderBottomWidth: 1,
    borderColor: '#000',
    shadowColor: '#000',
    shadowOffset: { width: 2, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 2,
  },
  loginButtonText: {
    fontSize: 16,
    color: '#000',
    fontWeight: 'bold',
  },
  kakaoButton: {
    backgroundColor: '#FEE500',
  },
  kakaoButtonText: {
    fontSize: 16,
    color: '#3C1E1E',
    fontWeight: 'bold',
  },
});

export default auth_main;
