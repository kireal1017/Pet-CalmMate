import { useRouter } from 'expo-router';
import React, { useState } from 'react';
import { ActivityIndicator, Alert, Modal, Pressable, StyleSheet, Text, TextInput, TouchableOpacity, View } from 'react-native';

const API_URL = 'http://54.180.212.150/api';

const auth_register: React.FC = () => {
  const router = useRouter();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [agree, setAgree] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const validateInputs = () => {

    if (!name.trim()) {
      setErrorMessage('이름을 입력해주세요.');
      return false;
    }

    if (!email.trim()) {
      setErrorMessage('이메일을 입력해주세요.');
      return false;
    }

    // 이메일 형식 검증
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      setErrorMessage('유효한 이메일 주소를 입력해주세요.');    
      return false;
    }

    if (password.length < 6) {
      setErrorMessage('비밀번호는 6자 이상이어야 합니다.');
      return false;
    }
    setErrorMessage('');
    return true;
  };

const handleRegister = async () => {
  if (!agree) {
    Alert.alert('알림', '이용약관에 동의해주세요.');
    return;
  }
  if (!validateInputs()) return;
  setIsLoading(true);

  try {
    const response = await fetch(`${API_URL}/users`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, name }),
    });

    if (!response.ok) {
      let errorMessage = '회원가입 중 오류가 발생했습니다.';
      try {
        const errorData = await response.json();
        errorMessage = errorData.error || errorMessage;
      } catch {
        const errorText = await response.text();
        if (errorText.trim().startsWith('<')) {
          errorMessage = '서버 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.';
        } else {
          errorMessage = errorText || errorMessage;
        }
      }
      throw new Error(errorMessage);
    }

    const data = await response.json();
    Alert.alert('회원가입 완료', '냥멍케어 회원가입이 완료되었습니다!', [
      { text: '로그인하기', onPress: () => router.push('/auth_login') },
    ]);
  } catch (error: any) {
    const errorMsg =
      error instanceof Error ? error.message : '네트워크 오류가 발생했습니다.';
    setErrorMessage(errorMsg);
    Alert.alert('회원가입 실패', errorMsg);
  } finally {
    setIsLoading(false);
  }
};

  const handleAgreementPress = () => {
    router.push('/auth_agreement');
  };

  const [visible, setVisible] = useState(false);
    const termsContent = `
    1. "앱은 강아지의 건강 관리, 먹이주기, 사진 및 영상 기록, 활동 추적 등 다양한 기능을 제공합니다."

    2. "회원 가입 시 이메일, 강아지 정보 등 일부 개인정보를 수집하며, 서비스 제공 목적 외에는 사용하지 않습니다."

    3. "카메라, 마이크, 사진 접근 권한은 강아지의 사진·영상 촬영, 음성 메모 기능에만 사용됩니다."

    4. "건강 정보, AI 솔루션 등은 참고용으로, 실제 건강 이상 시 전문가 상담을 권장합니다."

    5. "서비스 내용은 사전 고지 없이 변경, 중단될 수 있습니다."

    6. "이용약관은 변경될 수 있으며, 변경 시 앱 내 공지를 통해 안내합니다."
    `;

  

  return (
    <View style={styles.container}>
      <Text style={styles.title}>냥멍케어 회원가입</Text>
      {errorMessage ? (
        <Text style={styles.errorText}>{errorMessage}</Text>
      ) : null}
      <View style={styles.inputGroup}>
        <Text style={styles.label}>이름</Text>
        <TextInput
          style={styles.input}
          value={name}
          onChangeText={setName}
          placeholder="이름을 입력하세요"
          placeholderTextColor="#bbb"
        />

        <Text style={styles.label}>이메일</Text>
        <TextInput
          style={styles.input}
          value={email}
          onChangeText={setEmail}
          autoCapitalize="none"
          keyboardType="email-address"
          placeholder="이메일을 입력하세요"
          placeholderTextColor="#bbb"
        />

        <Text style={styles.label}>비밀번호</Text>
        <TextInput
          style={styles.input}
          value={password}
          onChangeText={setPassword}
          secureTextEntry
          autoCapitalize='none'
          placeholder="비밀번호를 입력하세요 (6자 이상)"
          placeholderTextColor="#bbb"

        />
      </View>

      {/* 이용약관 동의 */}
      <View style={styles.agreeRow}>
        <Pressable
          style={styles.checkbox}
          onPress={() => setAgree((prevAgree) => !prevAgree)}
          hitSlop={8}
        >
          {agree && <Text style={styles.checkmark}>✓</Text>}
        </Pressable>
        <TouchableOpacity  onPress={() => setVisible(true)}>
                <Text >이용약관내용 확인하기</Text>
              </TouchableOpacity>
        
              {/* 모달 뷰 */}
              <Modal
                visible={visible}
                animationType="slide"
                transparent
                onRequestClose={() => setVisible(false)}
              >
                <View style={styles.modalOverlay}>
                  <View style={styles.modalView}>
                    {/* X 버튼 */}
                    <TouchableOpacity
                      style={styles.closeButton}
                      onPress={() => setVisible(false)}
                      hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
                    >
                      <Text style={styles.closeText}>✕</Text>
                    </TouchableOpacity>
                    {/* 약관 내용 */}
                    <Text style={styles.termsTitle}>이용약관</Text>
                    <Text style={styles.termsContent}>{termsContent}</Text>
                  </View>
                </View>
              </Modal>
      </View>

      {/* 회원가입 버튼 */}
      <TouchableOpacity
        style={[
          styles.registerButton, 
          (!agree || isLoading) && styles.buttonDisabled
        ]}

        onPress={handleRegister}
        activeOpacity={agree && !isLoading ? 0.8 : 1}
        disabled={!agree || isLoading}
      >

        {isLoading ? (
          <ActivityIndicator size="small" color="#222" />
        ) : (
          <Text style={styles.registerButtonText}>냥멍케어 회원가입</Text>
        )}

      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F7F7F7',
    alignItems: 'center',
    paddingHorizontal: 24,
    paddingTop: 24,
  },

  backButton: {
    position: 'absolute',
    top: 16,
    left: 16,
    padding: 8,
    zIndex: 10,
  },

  arrow: {
    fontSize: 32,
    color: '#222',
  },

  title: {
    fontSize: 20,
    fontWeight: 'bold',
    marginTop: 48,
    marginBottom: 32,
    textAlign: 'center',
    color: '#222',
  },

  errorText: {
    color: 'red',
    marginBottom: 16,
    textAlign: 'center',
    width: '100%',
  },

  inputGroup: {
    width: '100%',
    marginBottom: 24,
  },

  label: {
    fontSize: 13,
    color: '#222',
    marginBottom: 6,
    marginTop: 12,
  },

  input: {
    backgroundColor: '#fff',
    borderRadius: 4,
    borderColor: '#E0E0E0',
    borderWidth: 1,
    height: 40,
    paddingHorizontal: 12,
    marginBottom: 4,
    fontSize: 15,
    color: '#222',
  },

  agreeRow: {
    flexDirection: 'row',
    alignItems: 'center',
    width: '100%',
    marginBottom: 28,
    marginTop: 8,
  },

  checkbox: {
    width: 20,
    height: 20,
    borderWidth: 1,
    borderColor: '#888',
    borderRadius: 3,
    backgroundColor: '#fff',
    marginRight: 8,
    justifyContent: 'center',
    alignItems: 'center',
  },

  checkmark: {
    fontSize: 16,
    color: '#333',
    fontWeight: 'bold',
  },

  agreeText: {
    fontSize: 13,
    color: '#222',
  },

  registerButton: {
    width: '100%',
    height: 48,
    borderRadius: 4,
    backgroundColor: '#fff',
    borderWidth: 1,
    borderColor: '#222',
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 8,
    shadowColor: '#000',
    shadowOffset: { width: 1, height: 1 },
    shadowOpacity: 0.06,
    shadowRadius: 2,
  },

  registerButtonText: {
    fontSize: 16,
    color: '#222',
    fontWeight: 'bold',
  },

  buttonDisabled: {
    opacity: 0.4,
  },
  modalView: {
    width: '80%',
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 20,
    elevation: 5,
    shadowColor: '#000',
    shadowOpacity: 0.2,
    shadowOffset: { width: 0, height: 2 },
    shadowRadius: 8,
    position: 'relative',
  },
  closeButton: {
    position: 'absolute',
    top: 10,
    right: 10,
    zIndex: 1,
    padding: 5,
  },
  closeText: { fontSize: 20, color: '#A55B5B' },
  termsTitle: { fontSize: 18, fontWeight: 'bold', marginBottom: 12, textAlign: 'center' },
  termsContent: { fontSize: 14, color: '#333', lineHeight: 22, marginTop: 8 },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.3)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  button: {
    backgroundColor: '#FFDEDE',
    paddingVertical: 12,
    paddingHorizontal: 28,
    borderRadius: 8,
    marginTop: 20,
  },
  buttonText: { color: '#A55B5B', fontWeight: 'bold', fontSize: 16 },
});

export default auth_register;