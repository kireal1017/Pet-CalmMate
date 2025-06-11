import MaterialCommunityIcons from '@expo/vector-icons/MaterialCommunityIcons';
import { useState } from 'react';
import { ActivityIndicator, Alert, Modal, StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { useAuth } from '../share/store/auth_store';

const API_BASE_URL = 'http://54.180.212.150/api';

const MusicPlayButton = ({ isActionLoading }) => {
  const { dogId } = useAuth();
  const [modalVisible, setModalVisible] = useState(false);
  const [musicStatus, setMusicStatus] = useState({ is_playing: false, type: '0' });
  const [loadingStatus, setLoadingStatus] = useState(false);

  const openModal = async () => {
    if (!dogId) {
      Alert.alert('강아지 정보가 없습니다.');
      return;
    }
    setLoadingStatus(true);
    setModalVisible(true);
    try {
      const res = await fetch(`${API_BASE_URL}/music-status?dog_id=${dogId}`);
      const data = await res.json();
      setMusicStatus(data);
    } catch (e) {
      Alert.alert('음악 상태 조회 실패', e.message);
    } finally {
      setLoadingStatus(false);
    }
  };

  // 음악 재생 요청
  const playMusic = async (type) => {
    if (!dogId) return;
    setLoadingStatus(true);
    try {
      const res = await fetch(`${API_BASE_URL}/music-play`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ dog_id: dogId, type: String(type) }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || '재생 실패');
      setMusicStatus({ is_playing: true, type: String(type) });
      //Alert.alert('음악 재생', data.message || `음악 ${type}번 재생`);
    } catch (e) {
      //sAlert.alert('음악 재생 실패', e.message);
    } finally {
      setLoadingStatus(false);
    }
  };

  // 음악 정지 요청
  const stopMusic = async () => {
    if (!dogId) return;
    setLoadingStatus(true);
    try {
      const res = await fetch(`${API_BASE_URL}/music-finished`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ dog_id: dogId }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || '정지 실패');
      setMusicStatus({ is_playing: false, type: '0' });
      //Alert.alert('음악 정지', data.message || '음악이 정지되었습니다.');
    } catch (e) {
      //Alert.alert('음악 정지 실패', e.message);
    } finally {
      setLoadingStatus(false);
    }
  };

  return (
    <View style={styles.buttonCell}>
      <TouchableOpacity
        style={[styles.circleButton, styles.activeButton]}
        disabled={isActionLoading}
        activeOpacity={0.8}
        onPress={openModal}
      >
        {isActionLoading ? (
          <ActivityIndicator color="#222" />
        ) : (
          <MaterialCommunityIcons name="music" size={44} color="#222" />
        )}
      </TouchableOpacity>
      <Text style={styles.buttonLabel}>노래재생</Text>

      {/* 음악 선택 모달 */}
      <Modal
        visible={modalVisible}
        transparent
        animationType="slide"
        onRequestClose={() => setModalVisible(false)}
      >
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <Text style={styles.modalTitle}>음악 재생</Text>
            {loadingStatus ? (
              <ActivityIndicator size="large" color="#222" />
            ) : (
              <>
                <Text style={styles.modalStatus}>
                  현재 재생 중: {musicStatus.is_playing && musicStatus.type !== '0'
                    ? `${musicStatus.type}번`
                    : '없음'}
                </Text>
                <View style={styles.musicList}>
                  {[1, 2, 3, 4, 5].map((num) => (
                    <TouchableOpacity
                      key={num}
                      style={styles.musicButton}
                      onPress={() => playMusic(num)}
                    >
                      <Text style={styles.musicButtonText}>{num}번 음악 재생</Text>
                    </TouchableOpacity>
                  ))}
                  <TouchableOpacity
                    style={[styles.musicButton, { backgroundColor: '#eee' }]}
                    onPress={stopMusic}
                  >
                    <Text style={[styles.musicButtonText, { color: '#d00' }]}>음악 정지</Text>
                  </TouchableOpacity>
                </View>
                <TouchableOpacity
                  style={styles.closeButton}
                  onPress={() => setModalVisible(false)}
                >
                  <Text style={styles.closeButtonText}>닫기</Text>
                </TouchableOpacity>
              </>
            )}
          </View>
        </View>
      </Modal>
    </View>
  );
};

export default MusicPlayButton;

const styles = StyleSheet.create({
  buttonCell: { alignItems: 'center', flex: 1 },
  circleButton: { width: 90, height: 90, borderRadius: 20, justifyContent: 'center', alignItems: 'center', marginBottom: 6, elevation: 2 },
  activeButton: { backgroundColor: '#FFDEDE' },
  buttonLabel: { fontSize: 15, fontWeight: '500', color: '#222', textAlign: 'center', marginTop: 2 },
  modalOverlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.3)', justifyContent: 'center', alignItems: 'center' },
  modalContent: { backgroundColor: '#fff', borderRadius: 12, padding: 24, width: 300, alignItems: 'center' },
  modalTitle: { fontSize: 18, fontWeight: 'bold', marginBottom: 16 },
  modalStatus: { fontSize: 15, marginBottom: 16 },
  musicList: { width: '100%', marginBottom: 16 },
  musicButton: { backgroundColor: '#FFDEDE', borderRadius: 8, padding: 12, marginVertical: 4, alignItems: 'center' },
  musicButtonText: { fontSize: 16, color: '#222' },
  closeButton: { marginTop: 8, padding: 8, borderRadius: 8, backgroundColor: '#eee', width: '100%', alignItems: 'center' },
  closeButtonText: { fontSize: 15, color: '#222' },
});
