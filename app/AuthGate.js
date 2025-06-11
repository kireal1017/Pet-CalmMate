import { useRouter } from 'expo-router';
import { useEffect } from 'react';

export default function AuthGate() {
  const router = useRouter();

useEffect(() => {
  if (!loading) {
    if (!token || !userId) {
      router.replace('/auth_main');
    } else {
      router.replace('/main_home');
    }
  }
}, [token, userId, loading]);

  return null; 
}