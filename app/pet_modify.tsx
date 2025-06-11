import * as ImagePicker from 'expo-image-picker';
import { useRouter } from 'expo-router';
import React, { useEffect, useState } from 'react';
import { ActivityIndicator, Alert, Image, ScrollView, StyleSheet, Text, TextInput, TouchableOpacity, View } from 'react-native';
import { SelectList } from 'react-native-dropdown-select-list';
import { useAuth } from '../share/store/auth_store';

const API_URL = 'http://54.180.212.150/api';

const breedData = [
  { key: '1', value: '골든 리트리버' },
  { key: '2', value: '그레이하운드' },
  { key: '3', value: '기타' },
  { key: '4', value: '닥스훈트' },
  { key: '5', value: '달마시안' },
  { key: '6', value: '도베르만' },
  { key: '7', value: '라브라도 리트리버' },
  { key: '8', value: '래브라도 리트리버' },
  { key: '9', value: '말라뮤트' },
  { key: '10', value: '말티즈' },
  { key: '11', value: '믹스' },
  { key: '12', value: '미니어처 핀셔' },
  { key: '13', value: '바셋 하운드' },
  { key: '14', value: '베들링턴 테리어' },
  { key: '15', value: '베르네즈 마운틴 독' },
  { key: '16', value: '보더 콜리' },
  { key: '17', value: '보스턴 테리어' },
  { key: '18', value: '복서' },
  { key: '19', value: '불독' },
  { key: '20', value: '불마스티프' },
  { key: '21', value: '비글' },
  { key: '22', value: '비숑 프리제' },
  { key: '23', value: '사모예드' },
  { key: '24', value: '삽살개' },
  { key: '25', value: '샤페이' },
  { key: '26', value: '셰퍼드' },
  { key: '27', value: '슈나우저' },
  { key: '28', value: '스코티시 테리어' },
  { key: '29', value: '스피츠' },
  { key: '30', value: '시바 이누' },
  { key: '31', value: '시츄' },
  { key: '32', value: '아메리칸 코커 스패니얼' },
  { key: '33', value: '아키타' },
  { key: '34', value: '아이리시 세터' },
  { key: '35', value: '에어데일 테리어' },
  { key: '36', value: '웰시 코기' },
  { key: '37', value: '요크셔 테리어' },
  { key: '38', value: '울프독' },
  { key: '39', value: '잭 러셀 테리어' },
  { key: '40', value: '진돗개' },
  { key: '41', value: '차우차우' },
  { key: '42', value: '치와와' },
  { key: '43', value: '코카 스패니얼' },
  { key: '44', value: '코커 스패니얼' },
  { key: '45', value: '코커푸' },
  { key: '46', value: '콜리' },
  { key: '47', value: '파피용' },
  { key: '48', value: '퍼그' },
  { key: '49', value: '페키니즈' },
  { key: '50', value: '포메라니안' },
  { key: '51', value: '푸들' },
  { key: '52', value: '풍산개' },
  { key: '53', value: '프렌치 불독' },
  { key: '54', value: '핏불 테리어' },
  { key: '55', value: '허스키' },
  
];

const yearData = Array.from({ length: 26 }, (_, i) => {
  const year = 2025 - i;
  return { key: year.toString(), value: year.toString() };
});
const monthData = Array.from({ length: 12 }, (_, i) => {
  const month = i + 1;
  return { key: month.toString(), value: month.toString() };
});
const dayData = Array.from({ length: 31 }, (_, i) => {
  const day = i + 1;
  return { key: day.toString(), value: day.toString() };
});

const pet_modify = () => {
  const { dogId, loading } = useAuth(); // 비동기식 dog_id
  const router = useRouter();

  // 폼 상태
  const [dogName, setDogName] = useState('');
  const [selectedBreed, setSelectedBreed] = useState('');
  const [selectedYear, setSelectedYear] = useState('');
  const [selectedMonth, setSelectedMonth] = useState('');
  const [selectedDay, setSelectedDay] = useState('');
  const [gender, setGender] = useState<'male' | 'female' | null>(null);
  const [imageUri, setImageUri] = useState<string | null>(null);
  const [originPhotoUrl, setOriginPhotoUrl] = useState<string | null>(null);
  const [fetching, setFetching] = useState(true);

  // 기존 정보 불러오기
  useEffect(() => {
    const fetchDogInfo = async () => {
      if (!dogId) return;
      setFetching(true);
      try {
        const res = await fetch(`${API_URL}/dogs?user_id=`);
        const data = await res.json();
        // dogId에 해당하는 강아지 찾기
        const dog = Array.isArray(data) ? data.find((d: any) => String(d.dog_id) === String(dogId)) : null;
        if (dog) {
          setDogName(dog.name || '');
          setSelectedBreed(dog.breed || '');
          if (dog.birth_date) {
            const [y, m, d] = dog.birth_date.split('-');
            setSelectedYear(y);
            setSelectedMonth(m);
            setSelectedDay(d);
          }
          if (dog.gender === '남' || dog.gender === 'male') setGender('male');
          else if (dog.gender === '여' || dog.gender === 'female') setGender('female');
          else setGender(null);
          setOriginPhotoUrl(dog.photo_url || null);
        }
      } catch (e) {
        Alert.alert('오류', '강아지 정보를 불러오지 못했습니다.');
      } finally {
        setFetching(false);
      }
    };
    if (dogId && !loading) fetchDogInfo();
  }, [dogId, loading]);

  // 사진 선택 핸들러
  const pickImage = async () => {
    const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (status !== 'granted') {
      alert('사진첩 접근 권한이 필요합니다.');
      return;
    }
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      quality: 1,
    });
    if (!result.canceled && result.assets && result.assets.length > 0) {
      setImageUri(result.assets[0].uri);
    }
  };

  // 강아지 정보 수정 완료 핸들러
  const handleModifyComplete = async () => {
    if (!dogName || !selectedBreed || !selectedYear || !selectedMonth || !selectedDay || !gender) {
      Alert.alert('오류', '모든 필드를 입력해주세요');  
      return;
    }
    try {
      const formData = new FormData();
      formData.append('name', dogName);
      formData.append('breed', selectedBreed);
      formData.append('birth_date', `${selectedYear}-${selectedMonth.padStart(2, '0')}-${selectedDay.padStart(2, '0')}`);
      formData.append('gender', gender === 'male' ? 'M' : 'F');
      // 새 이미지가 있으면 첨부
      if (imageUri) {
        const filename = imageUri.split('/').pop() || 'photo.jpg';
        const match = /\.(\w+)$/.exec(filename);
        const type = match ? `image/${match[1]}` : 'image/jpeg';
        formData.append('photo', {
          uri: imageUri,
          type: type,
          name: filename,
        } as any);
      }
      console.log(formData);
      // PUT 요청
      const response = await fetch(`${API_URL}/dogs/${dogId}`, {
        method: 'PUT',
        body: formData,
        // headers: { 'Content-Type': 'multipart/form-data' }, // X
      });
      const contentType = response.headers.get('content-type');
      let result;
      if (contentType && contentType.includes('application/json')) {
        result = await response.json();
      } else {
        const text = await response.text();
        throw new Error('서버 오류: ' + text);
      }
      if (response.ok) {
        Alert.alert('성공', '강아지 정보가 수정되었습니다');
        router.replace('/(tabs)/main_home');
      } else {
        throw new Error(result.error || '수정 실패');
      }
    } catch (error) {
      Alert.alert('오류', error instanceof Error ? error.message : '서버 연결 실패');
    }
  };

  if (loading || fetching) {
    return (
      <View style={styles.container}>
        <ActivityIndicator size="large" color="#222" />
        <Text>강아지 정보를 불러오는 중...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <ScrollView style={styles.content} contentContainerStyle={styles.scrollContent}>
        <Text style={styles.title}>강아지 정보 수정</Text>
        {/* 강아지 이름 입력 */}
        <Text style={styles.label}>강아지 이름</Text>
        <TextInput
          style={styles.input}
          value={dogName}
          onChangeText={setDogName}
          placeholder=""
        />
        {/* 품종 선택 */}
        <Text style={styles.label}>종</Text>
        <SelectList
          setSelected={setSelectedBreed}
          data={breedData}
          save="value"
          placeholder="강아지 품종 선택"
          boxStyles={styles.dropdownBox}
          dropdownStyles={styles.dropdown}
          search={false}
        />
        {/* 생일 선택 */}
        <Text style={styles.label}>생일</Text>
        <View style={styles.dateContainer}>
          <View style={styles.dateItem}>
            <SelectList
              setSelected={setSelectedYear}
              data={yearData}
              save="value"
              placeholder="년"
              boxStyles={styles.dateBox}
              dropdownStyles={styles.dateDropdown}
              search={false}
              defaultOption={yearData.find(item => item.value === selectedYear)}
            />
          </View>
          <View style={styles.dateItem}>
            <SelectList
              setSelected={setSelectedMonth}
              data={monthData}
              save="value"
              placeholder="월"
              boxStyles={styles.dateBox}
              dropdownStyles={styles.dateDropdown}
              search={false}
              defaultOption={monthData.find(item => item.value === selectedMonth)}
            />
          </View>
          <View style={styles.dateItem}>
            <SelectList
              setSelected={setSelectedDay}
              data={dayData}
              save="value"
              placeholder="일"
              boxStyles={styles.dateBox}
              dropdownStyles={styles.dateDropdown}
              search={false}
              defaultOption={dayData.find(item => item.value === selectedDay)}
            />
          </View>
        </View>
        {/* 성별 선택 */}
        <Text style={styles.label}>성별</Text>
        <View style={styles.genderContainer}>
          <TouchableOpacity
            style={[
              styles.genderButton,
              gender === 'male' && styles.genderButtonSelected
            ]}
            onPress={() => setGender('male')}
          >
            <Text style={styles.genderText}>남</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[
              styles.genderButton,
              gender === 'female' && styles.genderButtonSelected
            ]}
            onPress={() => setGender('female')}
          >
            <Text style={styles.genderText}>여</Text>
          </TouchableOpacity>
        </View>
        {/* 사진 변경 */}
        <Text style={styles.label}>사진 변경</Text>
        <TouchableOpacity style={styles.photoButton} onPress={pickImage}>
          <Text style={styles.photoButtonText}>갤러리에서 사진 선택</Text>
        </TouchableOpacity>
        {(imageUri || originPhotoUrl) && (
          <View style={styles.photoPreviewContainer}>
            <Image 
              source={{ uri: imageUri || originPhotoUrl || '' }} 
              style={styles.photoPreview} 
              resizeMode="cover"
            />
          </View>
        )}
        {/* 수정 완료 버튼 */}
        <TouchableOpacity style={styles.registerButton} onPress={handleModifyComplete}>
          <Text style={styles.registerButtonText}>수정 완료</Text>
        </TouchableOpacity>
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F7F7F7',
    paddingTop: 32,
  },
  content: {
    flex: 1,
    paddingHorizontal: 20,
  },
  scrollContent: {
    paddingVertical: 20,
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 20,
    textAlign: 'center',
  },
  label: {
    fontSize: 16,
    marginBottom: 8,
    marginTop: 16,
  },
  input: {
    backgroundColor: 'white',
    borderWidth: 1,
    borderColor: '#E0E0E0',
    borderRadius: 4,
    padding: 10,
    height: 45,
  },
  dropdownBox: {
    backgroundColor: 'white',
    borderColor: '#E0E0E0',
    height: 45,
  },
  dropdown: {
    backgroundColor: 'white',
    borderColor: '#E0E0E0',
  },
  dateContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  dateItem: {
    flex: 1,
    marginRight: 8,
  },
  dateBox: {
    backgroundColor: 'white',
    borderColor: '#E0E0E0',
    height: 45,
  },
  dateDropdown: {
    backgroundColor: 'white',
    borderColor: '#E0E0E0',
    zIndex: 3000,
  },
  genderContainer: {
    flexDirection: 'row',
    marginBottom: 25,
  },
  genderButton: {
    flex: 1,
    height: 45,
    backgroundColor: 'white',
    borderWidth: 1,
    borderColor: '#E0E0E0',
    justifyContent: 'center',
    alignItems: 'center',
  },
  genderButtonSelected: {
    backgroundColor: '#EEEEEE',
  },
  genderText: {
    fontSize: 16,
  },
  photoButton: {
    backgroundColor: 'white',
    borderWidth: 1,
    borderColor: '#E0E0E0',
    height: 45,
    borderRadius: 4,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 15,
  },
  photoButtonText: {
    fontSize: 16,
  },
  photoPreviewContainer: {
    alignItems: 'center',
    marginBottom: 20,
  },
  photoPreview: {
    width: 200,
    height: 200,
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#E0E0E0',
  },
  registerButton: {
    backgroundColor: 'white',
    borderWidth: 1,
    borderColor: '#222',
    height: 50,
    borderRadius: 4,
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 20,
  },
  registerButtonText: {
    fontSize: 16,
    fontWeight: 'bold',
  },
});

export default pet_modify;