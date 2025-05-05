import React from 'react';
import { View, Text, StyleSheet, Image, TouchableOpacity, ScrollView } from 'react-native';
import Header from './Header';
import Footer from './Footer';
import { useRouter } from 'expo-router';



const awsDogData = null; 



// 기본값 설정
const defaultDog = {
  name: '강아지',
  breed: '종',
  age: '나이',
  gender: '남/여',
  weight: '체중',
  status: '', 
  barkCount: 0,
  snackCount: 0,
  snackAmount: 0,
  walk: 0,
  weightStatus: '보통',
  foodAmount: 0,
  imageUrl: null,
};

const dog = { ...defaultDog, ...(awsDogData ?? {}) };


const HomeScreen: React.FC = () => {
  const router = useRouter();

  const dogName = dog.name || '강아지';
  const dogStatus = dog.status || ' ';
  const todayTitle = `오늘의 ${dogName || '강아지'}`;

 
  const dogImageSource = dog.imageUrl
    ? { uri: dog.imageUrl }
    : require('../../assets/dog_logo.png'); 


  const barkCount = dog.barkCount ?? 0;
  const snackCount = dog.snackCount ?? 0;
  const snackAmount = dog.snackAmount ?? 0;
  const walk = dog.walk ?? 0;
  const weightStatus = dog.weightStatus || '보통';
  const foodAmount = dog.foodAmount ?? 0;

  
  const handleNavigate = (screen: string) => {
    console.log(`${screen}으로 이동`);
  };

  return (
    <View style={styles.container}>
      <Header />
      <ScrollView contentContainerStyle={styles.scroll}>
   
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
              <Text style={styles.dogInfoText}>{dog.name}</Text>
              <Text style={styles.dogInfoText}>{dog.breed}</Text>
              <Text style={styles.dogInfoText}>{dog.age}</Text>
              <Text style={styles.dogInfoText}>{dog.gender}</Text>
              <Text style={styles.dogInfoText}>{dog.weight}</Text>
            </View>
            <View style={styles.dogStatusWrapper}>
              <Text style={styles.dogStatusLabel}>
                현재 {dogName}의 상태는?
              </Text>
              <Text style={styles.dogStatusValue}>{dogStatus}</Text>
            </View>
          </View>
        </View>

 
        <View style={styles.todayCard}>
          <Text style={styles.todayTitle}>{todayTitle}</Text>
          <View style={styles.todayStatsRow}>
            <View style={styles.statPill}>
              <Text style={styles.statText}>짖음 횟수 {barkCount}회</Text>
            </View>
            <View style={styles.statPill}>
              <Text style={styles.statText}>간식 제공 횟수 {snackCount}회</Text>
            </View>
          </View>
          <View style={styles.todayStatsRow}>
            <View style={styles.statPill}>
              <Text style={styles.statText}>간식 제공량 {snackAmount}개</Text>
            </View>
            <View style={styles.statPill}>
              <Text style={styles.statText}>산책 {walk}km</Text>
            </View>
          </View>
          <View style={styles.todayStatsRow}>
            <View style={styles.statPill}>
              <Text style={styles.statText}>체중 {weightStatus}</Text>
            </View>
            <View style={styles.statPill}>
              <Text style={styles.statText}>권장 사료량 {foodAmount}g</Text>
            </View>
          </View>
        </View>

   
        <View style={styles.buttonGroup}>
          <TouchableOpacity
            style={styles.roundButton}
            onPress={() => router.navigate('/(tabs)/WalkScreen2')}
          >
            <Text style={styles.roundButtonText}>산책 시키기</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={styles.roundButton}
            onPress={() => router.navigate('/(tabs)/WeightScreen')}
          >
            <Text style={styles.roundButtonText}>체중 기록하기</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={styles.roundButton}
            onPress={() => router.navigate('/(tabs)/CameraScreen')}
          >
            <Text style={styles.roundButtonText}>강아지 보기</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
      <Footer />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff'
  },
  scroll: {
    alignItems: 'center',
    paddingBottom: 16,
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
    width: 60,
    height: 60,
    borderRadius: 30,
    borderWidth: 2,
    borderColor: '#fff',
    backgroundColor: '#fff',
  },
  dogInfoTexts: {
    flex: 1,
    justifyContent: 'center',
  },
  dogInfoText: {
    fontSize: 12,
    marginVertical: 1,
    color: '#333',
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
    width: 349,
    height: 70,
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
});

export default HomeScreen;
