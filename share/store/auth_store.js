import * as SecureStore from 'expo-secure-store';
import React, { createContext, useContext, useEffect, useState } from 'react';


const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [token, setToken] = useState(null);
  const [userId, setUserId] = useState(null);
  const [dogId, setDogId] = useState(null); 
  const [loading, setLoading] = useState(true);

  

  useEffect(() => {
    (async () => {
      const storedToken = await SecureStore.getItemAsync('access_token');
      const storedUserId = await SecureStore.getItemAsync('user_id');
      const storedDogId = await SecureStore.getItemAsync('dog_id');  
      setToken(storedToken);
      setUserId(storedUserId);
      setDogId(storedDogId);
      setLoading(false);
    })();
  }, []);

  const login = async (accessToken) => {
    await SecureStore.setItemAsync('access_token', accessToken);
    setToken(accessToken);

    // 토큰으로 user_id 조회
    const res = await fetch('http://54.180.212.150/api/profile', {
      method: 'GET',
      headers: { Authorization: `Bearer ${accessToken}` },
    });
    const data = await res.json();  
    console.log('profile 응답:', data);
    if (res.ok && data.user) {
      await SecureStore.setItemAsync('user_id', data.user.user_id.toString());
      setUserId(data.user.user_id.toString());
    } else {
      setUserId(null);
    }
  };

  const logout = async () => {
    await SecureStore.deleteItemAsync('access_token');
    await SecureStore.deleteItemAsync('user_id');
    await SecureStore.deleteItemAsync('dog_id');
    setToken(null);
    setUserId(null);
    setDogId(null);
  };

  // dog_id 저장 함수
  const saveDogId = async (newDogId) => {
    await SecureStore.setItemAsync('dog_id', newDogId.toString());
    setDogId(newDogId.toString());
  };

  // dog_id 삭제 함수
  const removeDogId = async () => {
    await SecureStore.deleteItemAsync('dog_id');
    setDogId(null);
  };

  // 임시 로그인 로직
  const fakeLogin = async () => {
    const fakeToken = 'dummy_token_123456';
    const fakeUserId = 'dummy_user_1';
    const fakeDogId = 'dummy_dog_1'; 
    await SecureStore.setItemAsync('access_token', fakeToken);
    await SecureStore.setItemAsync('user_id', fakeUserId);
    await SecureStore.setItemAsync('dog_id', fakeDogId); 
    
    setToken(fakeToken);
    setUserId(fakeUserId);
    setDogId(fakeDogId); 
  };

  return (
    <AuthContext.Provider value={{ token, userId,dogId,saveDogId,removeDogId ,fakeLogin, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
    
  );
}

export const useAuth = () => useContext(AuthContext);