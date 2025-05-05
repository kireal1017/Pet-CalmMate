import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Image, Dimensions } from 'react-native';
import { useRouter } from 'expo-router';

export default function LoginScreen() {
  const router = useRouter();


  return (
    <View style={styles.container}>
      <Text style={styles.title}>멍냥케어</Text>
      <Text style={styles.subtitle}>안심되는 우리 강아지 관리</Text>
      <Image
        source={require('../../assets/dog_logo.png')} 
        style={styles.dogImage}
        resizeMode="contain"
      />
      <TouchableOpacity
        style={styles.loginButton}
        onPress={() => router.navigate('/(tabs)/HomeScreen')}
      >
        <Text style={styles.loginButtonText}>멍냥케어 로그인</Text>
      </TouchableOpacity>
      <TouchableOpacity
        style={[styles.loginButton, styles.kakaoButton]}
        activeOpacity={0.8}
      >
        <Text style={styles.kakaoButtonText}>카카오톡으로 로그인</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F8DADA', 
    alignItems: 'center',
    justifyContent: 'center',
  },
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

export default LoginScreen;
