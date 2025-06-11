import { useRouter } from 'expo-router';
import React from 'react';
import { Alert, StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { useAuth } from '../../share/store/auth_store';

const option_options: React.FC = () => {
  const router = useRouter();
  const { logout } = useAuth();

  // 로그아웃 팝업
  const handleLogout = () => {
    Alert.alert(
      '로그아웃',
      '정말 로그아웃 하시겠습니까?',
      [
        {
          text: '아니오',
          style: 'cancel',
        },
        {
          text: '예',
          onPress: async () => {
            await logout(); 
            router.replace('/auth_main'); 
          },
          style: 'destructive',
        },
      ],
      { cancelable: true }
    );
  };

  return (
    <View style={styles.container}>
      <View style={styles.content}>
        {/* 장치 관리 섹션 */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>장치 관리</Text>
          <TouchableOpacity
            style={styles.optionButton}
            onPress={() => router.push('../option_device')}
          >
            <Text style={styles.optionText}>장치 연결</Text>
          </TouchableOpacity>
        </View>

        {/* 계정 관리 섹션 */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>계정 관리</Text>
          <TouchableOpacity style={styles.optionButton} onPress={handleLogout}>
            <Text style={styles.optionText}>로그아웃</Text>
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
    paddingHorizontal: 15,
  },
  section: {
    marginVertical: 10,
  },
  sectionTitle: {
    fontSize: 11.12,
    fontWeight: 'bold',
    marginBottom: 5,
    color: '#333',
  },
  optionButton: {
    paddingVertical: 10,
    borderBottomWidth: 0.5,
    borderBottomColor: '#FF9999',
    borderTopWidth: 1,
    borderTopColor: '#FF9999',
    justifyContent: 'space-between',
    flexDirection: 'row',
  },
  optionText: {
    fontSize: 11,
    color: '#333',
  },
});

export default option_options;
