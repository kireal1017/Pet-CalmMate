import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Dimensions } from 'react-native';
import { BarChart } from 'react-native-chart-kit';
import Header2 from './Header2';
import Footer from './Footer';
import { MaterialIcons } from '@expo/vector-icons';

const screenWidth = Dimensions.get('window').width;

const ChartScreen = () => {
  const now = new Date();
  const [currentMonth, setCurrentMonth] = useState(now.getMonth() + 1); 
  const [currentYear, setCurrentYear] = useState(now.getFullYear() % 100); 
  const [activeCategory, setActiveCategory] = useState('기분'); 
  
  const chartData = {
    labels: Array.from({ length: 30 }, (_, i) => (i + 1).toString()).slice(0, 15),
    datasets: [
      {
        data: [
          20, 45, 35, 25, 15, 25, 35, 45, 25, 35, 45, 15, 25, 10, 45
        ],
      }
    ]
  };
  
  
  const chartConfig = {
    backgroundGradientFrom: '#fff',
    backgroundGradientTo: '#fff',
    color: (opacity = 1) => `rgba(65, 105, 225, ${opacity})`,
    barPercentage: 0.5,
    decimalPlaces: 0,
    labelColor: (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
    propsForBackgroundLines: {
      strokeDasharray: '',
      stroke: '#E9E9E9',
    },
  };

 
  const prevMonth = () => {
    if (currentMonth === 1) {
      setCurrentMonth(12);
      setCurrentYear(currentYear - 1);
    } else {
      setCurrentMonth(currentMonth - 1);
    }
  };

  
  const nextMonth = () => {
    if (currentMonth === 12) {
      setCurrentMonth(1);
      setCurrentYear(currentYear + 1);
    } else {
      setCurrentMonth(currentMonth + 1);
    }
  };

  
  const handleCategoryPress = (category) => {
    setActiveCategory(category);
  };

  
  const serverText = `1월의 OO은 산책을 주 ${currentMonth}회 정도 했습니다.
일당 산책 시간은 주 3.5km입니다.`;

  return (
    <View style={styles.container}>
      <Header2 />
      <View style={styles.content}>
  
        <View style={styles.monthSelector}>
          <TouchableOpacity onPress={prevMonth} style={styles.monthButton}>
            <MaterialIcons name="chevron-left" size={28} color="black" />
          </TouchableOpacity>
          <Text style={styles.monthText}>{`${currentYear}년 ${currentMonth}월`}</Text>
          <TouchableOpacity onPress={nextMonth} style={styles.monthButton}>
            <MaterialIcons name="chevron-right" size={28} color="black" />
          </TouchableOpacity>
        </View>

        <View style={styles.chartContainer}>
          <BarChart
            data={chartData}
            width={screenWidth - 40}
            height={220}
            chartConfig={chartConfig}
            fromZero
            showBarTops={false}
            withInnerLines
            withHorizontalLabels
          />
        </View>

  
        <View style={styles.categoryContainer}>
          {['기분', '산책', '체중', '식사량'].map((category) => (
            <TouchableOpacity
              key={category}
              style={[
                styles.categoryButton,
                activeCategory === category ? styles.categoryButtonActive : styles.categoryButtonInactive
              ]}
              onPress={() => handleCategoryPress(category)}
            >
              <Text
                style={[
                  styles.categoryText,
                  activeCategory === category ? styles.categoryTextActive : styles.categoryTextInactive
                ]}
              >
                {category}
              </Text>
            </TouchableOpacity>
          ))}
        </View>

  
        <View style={styles.textContainer}>
          <Text style={styles.serverText}>{serverText}</Text>
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
  content: {
    flex: 1,
    paddingHorizontal: 20,
    paddingTop: 10,
    paddingBottom: 20,
  },
  monthSelector: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: 8,
    backgroundColor: '#FFE6E6',
    borderRadius: 25,
    marginVertical: 10,
  },
  monthButton: {
    padding: 5,
  },
  monthText: {
    fontSize: 18,
    fontWeight: 'bold',
    paddingHorizontal: 20,
  },
  chartContainer: {
    marginVertical: 15,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#E9E9E9',
    borderRadius: 8,
    padding: 5,
    backgroundColor: '#fff',
  },
  categoryContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginTop: 5,
    marginBottom: 15,
  },
  categoryButton: {
    paddingHorizontal: 15,
    paddingVertical: 8,
    borderRadius: 15,
    minWidth: 60,
    alignItems: 'center',
  },
  categoryButtonActive: {
    backgroundColor: '#D2ADAD',
  },
  categoryButtonInactive: {
    backgroundColor: '#FFDEDE',
  },
  categoryText: {
    fontSize: 14,
    fontWeight: '500',
  },
  categoryTextActive: {
    color: 'white',
  },
  categoryTextInactive: {
    color: 'black',
  },
  textContainer: {
    backgroundColor: '#fff',
    borderRadius: 20,
    padding: 15,
    marginTop: 5,
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
});

export default ChartScreen;
