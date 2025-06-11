import React, { useState } from 'react';
import { Modal, StyleSheet, Text, TouchableOpacity, View } from 'react-native';

const TermsModal = () => {
  const [visible, setVisible] = useState(false);

  const termsContent = `
  [이용약관]
  1. 본 앱은 사용자의 편의를 위해 제공됩니다.
  2. 사용자는 앱 이용 시 관련 법규를 준수해야 합니다.
  3. 기타 약관 내용이 여기에 들어갑니다.
  `;

  return (
    <View style={styles.container}>
      {/* 이용약관 버튼 */}
      <TouchableOpacity style={styles.button} onPress={() => setVisible(true)}>
        <Text style={styles.buttonText}>이용약관</Text>
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
  );
};

const styles = StyleSheet.create({
  container: { alignItems: 'center', justifyContent: 'center', flex: 1 },
  button: {
    backgroundColor: '#FFDEDE',
    paddingVertical: 12,
    paddingHorizontal: 28,
    borderRadius: 8,
    marginTop: 20,
  },
  buttonText: { color: '#A55B5B', fontWeight: 'bold', fontSize: 16 },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.3)',
    justifyContent: 'center',
    alignItems: 'center',
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
});

export default TermsModal;