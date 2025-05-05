import React, { useState, useEffect, useRef } from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import Header2 from './Header2';
import Footer from './Footer';
import { useRouter } from 'expo-router';


const getTodayString = () => {
  const today = new Date();
  const year = String(today.getFullYear()).slice(2); 
  const month = String(today.getMonth() + 1).padStart(2, '0');
  const date = String(today.getDate()).padStart(2, '0');
  return `${year}년 ${month}월 ${date}일`;
};


const formatTime = (seconds) => {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = seconds % 60;
  
  return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
};

const WalkScreen2 = () => {
  const router = useRouter();
  const [activeTab, setActiveTab] = useState('측정');
  const [activeButton, setActiveButton] = useState('산책 중');
  const [seconds, setSeconds] = useState(0);
  const [distance, setDistance] = useState(0);
  const [isPaused, setIsPaused] = useState(false);
  
  const timerRef = useRef(null);


  const startTimer = () => {
    if (timerRef.current !== null) return;
    
    timerRef.current = setInterval(() => {
      setSeconds(prev => prev + 1);
      
      setDistance(prev => prev + (6 / 3600));
    }, 1000);
  };

  const pauseTimer = () => {
    if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }
  };

  
  const finishWalk = () => {
    pauseTimer();
   
    /* 
    sendDataToServer({
      time: seconds,
      distance: distance.toFixed(1),
      date: new Date()
    });
    */
    alert(`산책 완료! 시간: ${formatTime(seconds)}, 거리: ${distance.toFixed(1)}km`);
   
    router.navigate('/WalkScreen1');
  };

  const handleButtonPress = (buttonName) => {
    setActiveButton(buttonName);
    
    if (buttonName === '산책 중') {
      setIsPaused(false);
      startTimer();
    } else if (buttonName === '일시정지') {
      setIsPaused(true);
      pauseTimer();
    } else if (buttonName === '마치기') {
      finishWalk();
    }
  };

 
  useEffect(() => {
    startTimer();
    
    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, []);

  return (
    <View style={styles.container}>
      <Header2 />
      <View style={styles.body}>
     
        <View style={styles.tabContainer}>
          <TouchableOpacity 
            style={[
              styles.tabButton, 
              activeTab === '측정' ? styles.activeTab : styles.inactiveTab
            ]}
            onPress={() => setActiveTab('측정')}
          >
            <Text style={styles.tabText}>측정</Text>
          </TouchableOpacity>
          <TouchableOpacity 
            style={[
              styles.tabButton, 
              activeTab === '기록' ? styles.activeTab : styles.inactiveTab
            ]}
            onPress={() => {
                setActiveTab('측정'); 
                router.navigate('/(tabs)/WalkScreen1'); 
              }}
          >
            <Text style={styles.tabText}>기록</Text>
          </TouchableOpacity>
        </View>

        
        <Text style={styles.dateText}>{getTodayString()}</Text>
        <Text style={styles.title}>산책 기록</Text>

       
        <View style={styles.infoBox}>
          <Text style={styles.infoText}>{formatTime(seconds)}</Text>
        </View>

        
        <View style={styles.infoBox}>
          <Text style={styles.infoText}>{distance.toFixed(1)}km</Text>
        </View>

       
        <View style={styles.buttonGroup}>
          <TouchableOpacity 
            style={[
              styles.actionButton,
              activeButton === '일시정지' ? styles.activeButton : styles.inactiveButton
            ]}
            onPress={() => handleButtonPress('일시정지')}
          >
            <Text style={styles.buttonIcon}>⏸️</Text>
            <Text style={styles.buttonText}>일시정지</Text>
          </TouchableOpacity>
          
          <TouchableOpacity 
            style={[
              styles.actionButton,
              activeButton === '산책 중' ? styles.activeButton : styles.inactiveButton
            ]}
            onPress={() => handleButtonPress('산책 중')}
          >
            <Text style={styles.buttonIcon}>▶️</Text>
            <Text style={styles.buttonText}>산책 중</Text>
          </TouchableOpacity>
          
          <TouchableOpacity 
            style={[
              styles.actionButton,
              activeButton === '마치기' ? styles.activeButton : styles.inactiveButton
            ]}
            onPress={() => {
                handleButtonPress('마치기');
                router.navigate('/(tabs)/HomeScreen'); 
            }

            }
          >
            <Text style={styles.buttonIcon}>⏹️</Text>
            <Text style={styles.buttonText}>마치기</Text>
          </TouchableOpacity>
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
    paddingTop: 10,
  },
  tabContainer: {
    flexDirection: 'row',
    marginBottom: 20,
    borderRadius: 25,
    borderWidth: 1,
    borderColor: '#FFD5D5',
    overflow: 'hidden',
    width: 200,
  },
  tabButton: {
    flex: 1,
    paddingVertical: 8,
    paddingHorizontal: 20,
    alignItems: 'center',
  },
  activeTab: {
    backgroundColor: '#FFD5D5',
  },
  inactiveTab: {
    backgroundColor: '#fff',
  },
  tabText: {
    fontSize: 16,
    color: '#222',
    fontWeight: '500',
  },
  dateText: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 4,
  },
  title: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  infoBox: {
    backgroundColor: '#FFE6E6',
    padding: 15,
    borderRadius: 8,
    width: '90%',
    marginBottom: 16,
    alignItems: 'center',
  },
  infoText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#222',
  },
  buttonGroup: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    width: '100%',
    marginTop: 40,
  },
  actionButton: {
    alignItems: 'center',
    justifyContent: 'center',
    width: 80,
    height: 80,
    borderRadius: 40,
    borderWidth: 1,
    borderColor: '#FFD5D5',
  },
  activeButton: {
    backgroundColor: '#FFDEDE',
  },
  inactiveButton: {
    backgroundColor: '#fff',
  },
  buttonIcon: {
    fontSize: 24,
    marginBottom: 5,
  },
  buttonText: {
    fontSize: 12,
    color: '#222',
  }
});

export default WalkScreen2;
