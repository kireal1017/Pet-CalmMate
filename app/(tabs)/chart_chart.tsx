import { MaterialIcons } from '@expo/vector-icons';
import React, { useEffect, useState } from 'react';
import { ActivityIndicator, Dimensions, ScrollView, StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { BarChart } from 'react-native-chart-kit';
import { useAuth } from '../../share/store/auth_store';

const screenWidth = Dimensions.get('window').width;

const ChartChart = () => {
  const now = new Date();
  const [currentMonth, setCurrentMonth] = useState(now.getMonth() + 1);
  const [currentYear, setCurrentYear] = useState(now.getFullYear() % 100);
  const [activeCategory, setActiveCategory] = useState('기분');
  const [weightChartData, setWeightChartData] = useState(null);
  const [walkChartData, setWalkChartData] = useState(null);
  const [mealChartData, setMealChartData] = useState(null);
  const [subType, setSubType] = useState('');
  const [serverText, setServerText] = useState('월 건강 리포트를 불러오는 중...');
  const { dogId, loading } = useAuth();
  const [moodChartData, setMoodChartData] = useState(null);
  const [loadingMood, setLoadingMood] = useState(false);
  const [fetchError, setFetchError] = useState(false);

  // 월 이동
  const prevMonth = () => {
    if (currentMonth === 1) {
      setCurrentMonth(12);
      setCurrentYear(currentYear - 1);
    } else {
      setCurrentMonth(currentMonth - 1);
    }
    resetAllChartData();
  };
  const nextMonth = () => {
    if (currentMonth === 12) {
      setCurrentMonth(1);
      setCurrentYear(currentYear + 1);
    } else {
      setCurrentMonth(currentMonth + 1);
    }
    resetAllChartData();
  };
  const resetAllChartData = () => {
    setWeightChartData(null);
    setWalkChartData(null);
    setMealChartData(null);
    setMoodChartData(null);
    setSubType('');
  };

  // 월간 보고서
  const fetchMonthlyReport = async () => {
    setServerText('월 건강 리포트를 불러오는 중...');
    setFetchError(false);
    try {
      const response = await fetch("http://54.180.212.150/api/monthly-report", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ dog_id: dogId }),
      });
      const data = await response.json();
      if (response.ok && (data.message || data.solution)) {
        setServerText(data.message || data.solution);
        setFetchError(false);
      } else {
        setServerText(data.error || "월 리포트 불러오기에 실패했습니다.");
        setFetchError(true);
      }
    } catch (err) {
      setServerText("서버 연결에 실패했습니다.");
      setFetchError(true);
    }
  };
  useEffect(() => {
    if (dogId) fetchMonthlyReport();
    else setServerText("강아지 정보가 없습니다.");
  }, [dogId]);

  // 날짜 헤더 포맷
  const getDateHeader = () => {
    if (activeCategory === '체중' && subType === '연간') {
      return `${currentYear}년`;
    }
    return `${currentYear}년 ${currentMonth}월`;
  };

  // ================== API 호출 함수들 ==================

  // 체중
  const fetchWeightChart = async (year, month) => {
    try {
      const response = await fetch(
        `http://54.180.212.150/api/chart/weight?dog_id=${dogId}&year=${year}&month=${month}`
      );
      const data = await response.json();
      if (response.ok && Array.isArray(data.weights)) {
        setWeightChartData(data.weights.map((v) => v === null ? 0 : v));
      } else {
        setWeightChartData([]);
      }
    } catch {
      setWeightChartData([]);
    }
  };
  const fetchYearlyWeightChart = async (year) => {
    try {
      const response = await fetch(
        `http://54.180.212.150/api/chart/weight/yearly?dog_id=${dogId}&year=${year}`
      );
      const data = await response.json();
      if (response.ok && Array.isArray(data.monthly_avg_weights)) {
        setWeightChartData(data.monthly_avg_weights.map((v) => v === null ? 0 : v));
      } else {
        setWeightChartData([]);
      }
    } catch {
      setWeightChartData([]);
    }
  };

  // 산책
  const fetchWalkDistanceChart = async (year, month) => {
    try {
      const response = await fetch(
        `http://54.180.212.150/api/chart/walk/distance?dog_id=${dogId}&year=${year}&month=${month}`
      );
      const data = await response.json();
      if (response.ok && Array.isArray(data.walk_distances)) {
        setWalkChartData(data.walk_distances.map((v) => v === null ? 0 : v));
      } else {
        setWalkChartData([]);
      }
    } catch {
      setWalkChartData([]);
    }
  };
  const fetchWalkDurationChart = async (year, month) => {
    try {
      const response = await fetch(
        `http://54.180.212.150/api/chart/walk/duration?dog_id=${dogId}&year=${year}&month=${month}`
      );
      const data = await response.json();
      if (response.ok && Array.isArray(data.walk_durations)) {
        setWalkChartData(data.walk_durations.map((v) => v === null ? 0 : v));
      } else {
        setWalkChartData([]);
      }
    } catch {
      setWalkChartData([]);
    }
  };

  // 식사량
  const fetchMealChart = async (year, month) => {
    try {
      const response = await fetch(
        `http://54.180.212.150/api/chart/meal?dog_id=${dogId}&year=${year}&month=${month}`
      );
      const data = await response.json();
      if (response.ok && Array.isArray(data.meals)) {
        setMealChartData(data.meals.map((v) => v === null ? 0 : v));
      } else {
        setMealChartData([]);
      }
    } catch {
      setMealChartData([]);
    }
  };
  const fetchMealDailyChart = async (dateStr) => {
    try {
      const response = await fetch(
        `http://54.180.212.150/api/chart/meal/daily?dog_id=${dogId}&date=${dateStr}`
      );
      const data = await response.json();
      if (response.ok && Array.isArray(data.meals)) {
        setMealChartData(data.meals.map((v) => v === null ? 0 : v));
      } else {
        setMealChartData([]);
      }
    } catch {
      setMealChartData([]);
    }
  };

  // ================== 불안도(기분) ==================
  const fetchMonthlyMoodChart = async (year, month) => {
    setLoadingMood(true);
    try {
      const response = await fetch(
        `http://54.180.212.150/api/chart/anxiety?dog_id=${dogId}&year=${year}&month=${month}`
      );
      const data = await response.json();
      if (response.ok && Array.isArray(data.daily_avg_anxieties)) {
        setMoodChartData(data.daily_avg_anxieties.map((v) => v === null ? 0 : v));
      } else {
        setMoodChartData([]);
      }
    } catch {
      setMoodChartData([]);
    } finally {
      setLoadingMood(false);
    }
  };
  const fetchDailyMoodChart = async (dateStr) => {
    setLoadingMood(true);
    try {
      const response = await fetch(
        `http://54.180.212.150/api/chart/anxiety/daily?dog_id=${dogId}&date=${dateStr}`
      );
      const data = await response.json();
      console.log("일 기분:",data)
      if (response.ok && Array.isArray(data.hourly_avg_anxieties)) {
        setMoodChartData(data.hourly_avg_anxieties.map((v) => v === null ? 0 : v));
      } else {
        setMoodChartData([]);
      }
    } catch {
      setMoodChartData([]);
    } finally {
      setLoadingMood(false);
    }
  };

  // ================== 카테고리/서브타입 전환 ==================
  const handleCategoryPress = async (category) => {
    setActiveCategory(category);
    resetAllChartData();
    if (category === '기분') {
      setSubType('월간');
      await fetchMonthlyMoodChart(2000 + currentYear, currentMonth);
    } else if (category === '산책') {
      setSubType('산책거리');
      await fetchWalkDistanceChart(2000 + currentYear, currentMonth);
    } else if (category === '체중') {
      setSubType('월간');
      await fetchWeightChart(2000 + currentYear, currentMonth);
    } else if (category === '식사량') {
      setSubType('월간');
      await fetchMealChart(2000 + currentYear, currentMonth);
    }
  };

  const handleSubTypePress = async (type) => {
    setSubType(type);
    if (activeCategory === '기분') {
      if (type === '월간') {
        await fetchMonthlyMoodChart(2000 + currentYear, currentMonth);
      } else if (type === '일간') {
        const today = new Date();
        const dateStr = today.toISOString().split('T')[0];
        await fetchDailyMoodChart(dateStr);
      }
    } else if (activeCategory === '산책') {
      if (type === '산책거리') {
        await fetchWalkDistanceChart(2000 + currentYear, currentMonth);
      } else if (type === '산책시간') {
        await fetchWalkDurationChart(2000 + currentYear, currentMonth);
      }
    } else if (activeCategory === '체중') {
      if (type === '월간') {
        await fetchWeightChart(2000 + currentYear, currentMonth);
      } else if (type === '연간') {
        await fetchYearlyWeightChart(2000 + currentYear);
      }
    } else if (activeCategory === '식사량') {
      if (type === '월간') {
        await fetchMealChart(2000 + currentYear, currentMonth);
      } else if (type === '일간') {
        const today = new Date();
        const dateStr = today.toISOString().split('T')[0];
        await fetchMealDailyChart(dateStr);
      }
    }
  };

  // ================== 차트 데이터 가공 ==================
  const getChartData = () => {
    // 기분(불안도)
    if (activeCategory === '기분' && moodChartData !== null) {
      const data = moodChartData.map((v) => v === null ? 0 : v);
      return {
        labels: data.map((_, i) => (subType === '일간' ? i.toString() : (i + 1).toString())),
        datasets: [{ data }],
      };
    }
    // 산책
    if (activeCategory === '산책' && walkChartData) {
      const data = walkChartData.map((w) => w === null ? 0 : w);
      return {
        labels: data.map((_, i) => (i + 1).toString()),
        datasets: [{ data }],
      };
    }
    // 체중
    if (activeCategory === '체중' && weightChartData) {
      const data = weightChartData.map((w) => w === null ? 0 : w);
      if (subType === '연간') {
        return {
          labels: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
          datasets: [{ data }],
        };
      }
      return {
        labels: data.map((_, i) => (i + 1).toString()),
        datasets: [{ data }],
      };
    }
    // 식사량
    if (activeCategory === '식사량' && mealChartData) {
      const data = mealChartData.map((w) => w === null ? 0 : w);
      if (subType === '일간') {
        return {
          labels: data.map((_, i) => i.toString()), // 0~23시
          datasets: [{ data }],
        };
      }
      return {
        labels: data.map((_, i) => (i + 1).toString()),
        datasets: [{ data }],
      };
    }
    // 기본
    return {
      labels: [],
      datasets: [{ data: [] }],
    };
  };

  // BarChart width 계산
  const chartData = getChartData();
  const barCount = chartData.labels.length;
  const barWidth = 40;
  const chartWidth = Math.max(barCount * barWidth, screenWidth);

  // 동적 서브버튼
  const renderSubButtons = () => {
    if (activeCategory === '기분') {
      return (
        <View style={styles.subButtonGroup}>
          <TouchableOpacity
            style={[styles.subButton, subType === '월간' && styles.subButtonActive]}
            onPress={() => handleSubTypePress('월간')}
          >
            <Text style={subType === '월간' ? styles.subButtonTextActive : styles.subButtonText}>월간</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.subButton, subType === '일간' && styles.subButtonActive]}
            onPress={() => handleSubTypePress('일간')}
          >
            <Text style={subType === '일간' ? styles.subButtonTextActive : styles.subButtonText}>일간</Text>
          </TouchableOpacity>
        </View>
      );
    }
    if (activeCategory === '산책') {
      return (
        <View style={styles.subButtonGroup}>
          <TouchableOpacity
            style={[styles.subButton, subType === '산책거리' && styles.subButtonActive]}
            onPress={() => handleSubTypePress('산책거리')}
          >
            <Text style={subType === '산책거리' ? styles.subButtonTextActive : styles.subButtonText}>산책거리</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.subButton, subType === '산책시간' && styles.subButtonActive]}
            onPress={() => handleSubTypePress('산책시간')}
          >
            <Text style={subType === '산책시간' ? styles.subButtonTextActive : styles.subButtonText}>산책시간</Text>
          </TouchableOpacity>
        </View>
      );
    }
    if (activeCategory === '체중') {
      return (
        <View style={styles.subButtonGroup}>
          <TouchableOpacity
            style={[styles.subButton, subType === '월간' && styles.subButtonActive]}
            onPress={() => handleSubTypePress('월간')}
          >
            <Text style={subType === '월간' ? styles.subButtonTextActive : styles.subButtonText}>월간</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.subButton, subType === '연간' && styles.subButtonActive]}
            onPress={() => handleSubTypePress('연간')}
          >
            <Text style={subType === '연간' ? styles.subButtonTextActive : styles.subButtonText}>연간</Text>
          </TouchableOpacity>
        </View>
      );
    }
    if (activeCategory === '식사량') {
      return (
        <View style={styles.subButtonGroup}>
          <TouchableOpacity
            style={[styles.subButton, subType === '월간' && styles.subButtonActive]}
            onPress={() => handleSubTypePress('월간')}
          >
            <Text style={subType === '월간' ? styles.subButtonTextActive : styles.subButtonText}>월간</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.subButton, subType === '일간' && styles.subButtonActive]}
            onPress={() => handleSubTypePress('일간')}
          >
            <Text style={subType === '일간' ? styles.subButtonTextActive : styles.subButtonText}>일간</Text>
          </TouchableOpacity>
        </View>
      );
    }
    return null;
  };

  // 로딩, 강아지 정보 없음 처리
  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#FF6B6B" />
        <Text>로딩 중...</Text>
      </View>
    );
  }
  if (!dogId) {
    return (
      <View style={styles.loadingContainer}>
        <Text>강아지 정보가 없습니다.</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.content}>
        {/* 월/년 선택 헤더 */}
        <View style={styles.monthSelector}>
          <TouchableOpacity onPress={prevMonth} style={styles.monthButton}>
            <MaterialIcons name="chevron-left" size={28} color="black" />
          </TouchableOpacity>
          <Text style={styles.monthText}>{getDateHeader()}</Text>
          <TouchableOpacity onPress={nextMonth} style={styles.monthButton}>
            <MaterialIcons name="chevron-right" size={28} color="black" />
          </TouchableOpacity>
        </View>

        {/* 동적 서브버튼 */}
        {renderSubButtons()}

        {/* 차트 영역 */}
        <View>
          {loadingMood ? (
            <View style={styles.loadingContainer}>
              <ActivityIndicator size="large" color="#FF6B6B" />
              <Text>차트 불러오는 중...</Text>
            </View>
          ) : (
            <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={{ flexGrow: 1 }}>
              <BarChart
                style={styles.chartContainer}
                data={getChartData()}
                width={chartWidth}
                height={220}
                chartConfig={{
                  backgroundGradientFrom: '#fff',
                  backgroundGradientTo: '#fff',
                  color: (opacity = 1) => `rgba(88, 88, 88, ${opacity})`,
                  barPercentage: 0.5,
                  decimalPlaces: 1,
                  labelColor: (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
                  propsForBackgroundLines: {
                    strokeDasharray: '',
                    stroke: '#E9E9E9',
                  },
                }}
                fromZero
                showBarTops={true}
                withInnerLines
                withHorizontalLabels
              />
            </ScrollView>
          )}
        </View>

        {/* 카테고리 버튼 */}
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
        {/* 텍스트 표시 영역 */}
        <View style={styles.textContainer}>
          <Text style={styles.serverText}>{serverText}</Text>
          {fetchError && (
            <TouchableOpacity style={styles.registerButton} onPress={fetchMonthlyReport}>
              <Text style={styles.registerButtonText}>다시 시도</Text>
            </TouchableOpacity>
          )}
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff', paddingTop: 32 },
  content: { flex: 1, paddingHorizontal: 20, paddingTop: 10, paddingBottom: 20 },
  monthSelector: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: 8,
    backgroundColor: '#FFE6E6',
    borderRadius: 25,
    marginVertical: 10,
  },
  monthButton: { padding: 5 },
  monthText: { fontSize: 18, fontWeight: 'bold', paddingHorizontal: 20 },
  subButtonGroup: {
    flexDirection: 'row',
    justifyContent: 'center',
    marginVertical: 4,
  },
  subButton: {
    marginHorizontal: 8,
    paddingHorizontal: 18,
    paddingVertical: 7,
    borderRadius: 16,
    backgroundColor: '#FFDEDE',
  },
  subButtonActive: {
    backgroundColor: '#D2ADAD',
  },
  subButtonText: {
    fontSize: 14,
    color: '#222',
    fontWeight: '500',
  },
  subButtonTextActive: {
    fontSize: 14,
    color: '#fff',
    fontWeight: '700',
  },
  chartContainer: {
    marginVertical: 6,
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 1,
    borderColor: '#E9E9E9',
    borderRadius: 8,
    padding: 5,
    backgroundColor: '#fff',
  },
  categoryContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginTop: 0,
    marginBottom: 4,
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
    marginHorizontal: 20,
  },
  serverText: {
    fontSize: 14,
    lineHeight: 22,
    textAlign: 'center',
    color: '#333',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
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
});

export default ChartChart;
