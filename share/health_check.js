import React, { useCallback, useEffect, useState } from "react";
import { ActivityIndicator, StyleSheet, Text, TouchableOpacity, View } from "react-native";
import { useAuth } from "../share/store/auth_store";

const HealthCheck = () => {
  const { dogId, loading } = useAuth();
  const [serverText, setServerText] = useState("건강 상태를 불러오는 중...");
  const [fetchError, setFetchError] = useState(false);
  const [fetching, setFetching] = useState(false);

  // API 호출 함수
  const fetchHealthCheck = useCallback(async () => {
    if (!dogId) {
      setServerText("강아지 정보가 없습니다.");
      setFetchError(true);
      return;
    }
    setFetching(true);
    setFetchError(false);
    try {
      const response = await fetch("http://54.180.212.150/api/health-check", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ dog_id: dogId }),
      });
      const data = await response.json();
      if (response.ok && (data.message || data.solution)) {
        setServerText(data.message || data.solution);
        setFetchError(false);
        } else if (data.error) {
        setServerText(data.error);
        setFetchError(true);
        } else {
        setServerText("건강 상태 정보를 불러올 수 없습니다.");
        setFetchError(true);
        }
    } catch (err) {
      setServerText("서버 연결에 실패했습니다.");
      setFetchError(true);
    } finally {
      setFetching(false);
    }
  }, [dogId]);

  useEffect(() => {
    if (!loading && dogId) {
      fetchHealthCheck();
    } else if (!loading && !dogId) {
      setServerText("강아지 정보가 없습니다.");
      setFetchError(true);
    }
  }, [dogId, loading, fetchHealthCheck]);

  if (loading || fetching) {
    return (
      <View style={styles.textContainer}>
        <ActivityIndicator size="small" color="#FF6B6B" />
        <Text style={styles.serverText}>로딩 중...</Text>
      </View>
    );
  }

  return (
    <View style={styles.textContainer}>
      <Text style={styles.serverText}>{serverText}</Text>
      {fetchError && (
        <TouchableOpacity style={styles.retryButton} onPress={fetchHealthCheck}>
          <Text style={styles.retryButtonText}>다시 시도</Text>
        </TouchableOpacity>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  textContainer: {
    padding: 15,
    backgroundColor: "#fff",
    borderRadius: 10,
    alignItems: "center",
    justifyContent: "center",
    margin: 10,
  },
  serverText: {
    fontSize: 15,
    color: "#222",
    textAlign: "center",
    marginBottom: 6,
  },
  retryButton: {
    marginTop: 8,
    paddingHorizontal: 18,
    paddingVertical: 8,
    backgroundColor: "#FF6B6B",
    borderRadius: 6,
  },
  retryButtonText: {
    color: "#fff",
    fontWeight: "bold",
    fontSize: 14,
  },
});

export default HealthCheck;
