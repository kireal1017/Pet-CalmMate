import { useFocusEffect } from '@react-navigation/native';
import { useRouter } from 'expo-router';
import React, { useCallback, useEffect, useState } from 'react';
import { ActivityIndicator, Dimensions, Image, ScrollView, StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import HealthCheck from '../../share/health_check';
import { useAuth } from '../../share/store/auth_store';



const { width } = Dimensions.get('window');

const main_home: React.FC = () => {
  const router = useRouter();
  const {userId, dogId, saveDogId } = useAuth(); 
  const [dogData, setDogData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState('');

  const defaultDog = {
  name: '',
  breed: '',
  birth_date: '',
  gender: ' ',
  photo_url: null,
};

  useEffect(() => {
    const fetchDogData = async () => {
      setLoading(true);
      setErrorMessage('');
      try {
        const response = await fetch(`http://54.180.212.150/api/dogs?user_id=${userId}`);
        if (!response.ok) throw new Error('서버 응답 오류');
        const data = await response.json();
        if (!Array.isArray(data) || data.length === 0 || !data[0].dog_id) {
          await saveDogId(null); 
          setDogData(null);
        } else {
          await saveDogId(data[0].dog_id); 
          setDogData(data[0]);
        }
      } catch (e) {
        await saveDogId(null); 
        setDogData(null);
        setErrorMessage('강아지 정보를 불러오지 못했습니다.');
      } finally {
        setLoading(false);
      }
    };
    fetchDogData();
  }, [saveDogId]);

  const dog = { ...defaultDog, ...(dogData ?? {}) };

//짖는 간식 횟수
  const [snackCount, setSnackCount] = useState(null);
  const [barkCount, setBarkCount] = useState(null);

useFocusEffect(
    useCallback(() => {
      setLoading(true);
      setErrorMessage('');

      const fetchSnackCount = async () => {
        try {
          const res = await fetch(`http://54.180.212.150/api/snack-today?dog_id=${dogId}`);
          const data = await res.json();
          if (res.ok && data.snack_count != null) {
            setSnackCount(data.snack_count);
          } else {
            setSnackCount(0);
          }
        } catch (e) {
          setSnackCount(0);
          await saveDogId(null);
          setDogData(null);
          setErrorMessage('강아지 정보를 불러오지 못했습니다.');
        }
      };

      const fetchBarkCount = async () => {
        try {
          const res = await fetch(`http://54.180.212.150/api/sound-count-today?dog_id=${dogId}`);
          const data = await res.json();
          if (res.ok && data.bark_count != null) {
            setBarkCount(data.bark_count);
          } else {
            setBarkCount(0);
          }
        } catch (e) {
          setBarkCount(0);
        }
      };

      // 두 API를 병렬로 호출
      Promise.all([fetchSnackCount(), fetchBarkCount()]).finally(() => {
        setLoading(false);
      });

      // cleanup 필요 없음
    }, [dogId])
  );

  // 서버에서 받은 photo_url이 있으면 이미지로 사용, 없으면 기본 이미지
  const dogImageSource = dogData?.photo_url
    ? { uri: dogData.photo_url }
    : require('../../assets/images/dog_logo.png');

  // 성별을 한글로 변환 (예: 'male' => '남', 'female' => '여')
  const getGenderText = (gender) => {
    if (!gender) return '';
    if (gender.toLowerCase() === 'M' || gender === 'M') return '남아';
    if (gender.toLowerCase() === 'F' || gender === 'F') return '여아';
    return gender;
  };
  
  const getYearAge = (birth_date) => {
  if (!birth_date) return null;
  const birthYear = parseInt(birth_date.slice(0, 4), 10);
  const currentYear = new Date().getFullYear();
  return currentYear - birthYear;
};






  return (
    <View style={styles.container}>
      <ScrollView contentContainerStyle={styles.scroll}>
        {loading ? (
          <ActivityIndicator size="large" color="#222" />
        ) : !dogId ? (
          <View style={styles.notRegisteredCard}>
            <TouchableOpacity
              style={styles.registerButton}
              onPress={() => router.push('/pet_add')}
              activeOpacity={0.8}
            >
              <Text style={styles.registerButtonText}>강아지 등록하기</Text>
            </TouchableOpacity>
            <View style={styles.notRegisteredInfoBox}>
              <Text style={styles.notRegisteredText}>
                등록된 강아지 정보가 없습니다.
              </Text>
              {errorMessage ? (
                <Text style={{ color: 'red', marginTop: 8 }}>{errorMessage}</Text>
              ) : null}
            </View>
          </View>
        ) : (
          <>
            <View style={styles.dogInfoCard}>
              <View style={styles.dogInfoRow}>
                <View style={styles.dogImageWrapper}>
                  <Image
                    source={dogImageSource}
                    style={styles.dogImage}
                    resizeMode="cover"
                  />
                </View>
                <View style={styles.dogInfoTexts}>
                  <Text style={styles.dogInfoText}>
                    이름: {dog.name}</Text>
                  <Text style={styles.dogInfoText}>
                    품종: {dog.breed}</Text>
                  <Text style={styles.dogInfoText}>
                    나이: {getYearAge(dog.birth_date)}살</Text>
                  <Text style={styles.dogInfoText}>
                    성별: {getGenderText(dog.gender)}
                  </Text>
                </View>
                <View>
                  <TouchableOpacity
                  style={styles.dogModifyButton}
                  onPress={() => router.push('/pet_modify')}>
                    <Text style={styles.dogModifyText}>수정</Text>
                  </TouchableOpacity>
                </View>
              </View>
            </View>
          </>
        )}


        {/* 짖은 횟수 간식 횟수*/}
        <View style={styles.snackBarkCard}>
          <View style={styles.snackCard}>
            <Text style={{ fontSize: 16, fontWeight: 'bold' }}>
              오늘 간식 횟수
            </Text>
            <Text>{snackCount}회</Text>
          </View>
          <View style={styles.spacer} />
          <View style={styles.snackCard}>
            <Text style={{ fontSize: 16, fontWeight: 'bold' }}>
              오늘 짖은 횟수
            </Text>
            <Text>{barkCount}회</Text>
          </View>
        </View>


        {/* 공통 버튼 그룹 */}
        <View style={styles.buttonGroup}>
          {/* <TouchableOpacity
            style={styles.roundButton}
            onPress={() => router.push('/test_m3u8')}
          >
            <Text style={styles.roundButtonText}>m3u8카메라 테스트</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={styles.roundButton}
            onPress={() => router.push('/test_mic')}
          >
            <Text style={styles.roundButtonText}>m3u8카메라</Text>
          </TouchableOpacity> */}
          {/* <TouchableOpacity
            style={styles.roundButton}
            onPress={() => router.push('/test_video')}
          >
            <Text style={styles.roundButtonText}>카메라 테스트</Text>
          </TouchableOpacity> */}
          {/* <TouchableOpacity
            style={styles.roundButton}
            onPress={() => router.push('/test_expovideo')}
          >
            <Text style={styles.roundButtonText}>expo/video</Text>
          </TouchableOpacity> */}
          <TouchableOpacity
            style={styles.roundButton}
            onPress={() => router.push('/pet_weight')}
          >
            <Text style={styles.roundButtonText}>체중 기록하기</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={styles.roundButton}
            onPress={() => router.push('/pet_camera')}
          >
            <Text style={styles.roundButtonText}>강아지 보기</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={styles.roundButton}
            onPress={() => router.push('/pet_walk')}
          >
            <Text style={styles.roundButtonText}>산책 시키기</Text>
          </TouchableOpacity>
        </View>
        <View style={styles.textContainer}>
          <HealthCheck />
        </View>
       
      </ScrollView>
    </View>
  );
};


const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    marginTop: 32,  
  },
  scroll: {
    alignItems: 'center',
    paddingBottom: 16,
  },
  notRegisteredCard: {
    width: '90%',
    marginTop: 32,
    alignItems: 'center',
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
  notRegisteredInfoBox: {
    backgroundColor: '#fff',
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#FFE3E3',
    width: '100%',
    minHeight: 120,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 16,
  },
  notRegisteredText: {
    color: '#888',
    fontSize: 15,
    textAlign: 'center',
  },
  dogInfoCard: {
    backgroundColor: '#FFDEDE',
    borderRadius: 12,
    width: '90%',
    marginTop: 16,
    paddingVertical: 16,
    paddingHorizontal: 12,
    alignItems: 'center',
    
  },
snackBarkCard: {
  margin: 5,
  flexDirection: 'row',
  justifyContent: 'center',
  borderColor: '#000000',
  borderWidth: 0,
  width: '90%',
  alignItems: 'center',
},
snackCard: {
  flex: 1, 
  marginTop: 10,
  backgroundColor: '#FFDEDE',
  borderRadius: 12,
  paddingVertical: 16,
  paddingHorizontal: 12,
  alignItems: 'center',
},
spacer: {
  width: 10, 
},
  dogInfoRow: {
    flexDirection: 'row',
    alignItems: 'center',
    width: '100%',
  },
  dogImageWrapper: {
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  dogImage: {
    width: width * 0.14,
    height: width * 0.14,
    borderRadius: width * 0.07,
    borderWidth: 2,
    borderColor: '#fff',
    backgroundColor: '#fff',
  },
  dogInfoTexts: {
    flex: 1,
    justifyContent: 'center',
  },
  dogInfoText: {
    fontSize: 15,
    marginVertical: 1,
    color: '#333',
    fontWeight: 'bold',
  },
  dogStatusWrapper: {
    alignItems: 'flex-end',
    justifyContent: 'center',
    minWidth: 80,
  },
  dogStatusLabel: {
    fontSize: 10,
    color: '#888',
    textAlign: 'center',
  },
  dogStatusValue: {
    fontSize: 12,
    fontWeight: 'bold',
    color: '#E57373',
    textAlign: 'center',
    marginTop: 2,
  },
  todayCard: {
    backgroundColor: '#FF9999',
    borderRadius: 12,
    width: '90%',
    marginTop: 18,
    paddingVertical: 16,
    alignItems: 'center',
  },
  todayTitle: {
    fontSize: 15,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 12,
  },
  todayStatsRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    width: '92%',
    marginBottom: 8,
  },
  statPill: {
    backgroundColor: '#fff',
    borderRadius: 20,
    paddingHorizontal: 14,
    paddingVertical: 6,
    marginHorizontal: 3,
    marginBottom: 4,
    minWidth: 90,
    alignItems: 'center',
  },
  statText: {
    fontSize: 12,
    color: '#333',
  },
  buttonGroup: {
    marginTop: 22,
    width: '90%',
    alignItems: 'center',
  },
  roundButton: {
    width: '100%',
    maxWidth: 400,
    height: 56,
    borderRadius: 100,
    borderWidth: 1,
    borderColor: '#FF9999',
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#fff',
    marginBottom: 16,
  },
  roundButtonText: {
    fontSize: 16,
    color: '#FF9999',
    fontWeight: 'bold',
  },
    textContainer: {
    backgroundColor: '#fff',
    borderRadius: 20,
    padding: 15,
    marginTop: 5,
    marginHorizontal:20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 3,
    elevation: 2,
  },
  serverText: {
    fontSize: 14,
    lineHeight: 22,
    textAlign: 'left',
    color: '#333',
  },
  dogModifyButton: {
    borderRadius: 100,
    padding: 6,
    margin:5,
    backgroundColor:'#fff'
  },
  dogModifyText: {
    fontWeight: 'bold',
  },
});

export default main_home;