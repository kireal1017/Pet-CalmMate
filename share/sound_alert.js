import { useEffect } from 'react';
import { EventSource } from 'react-native-sse';
import Toast from 'react-native-toast-message';

export default function SoundAlert() {
  useEffect(() => {
    const source = new EventSource('http://54.180.212.150/api/alert-stream');
    source.addEventListener('message', (event) => {
      const data = JSON.parse(event.data);
      console.log('알림 도착:', data);
      Toast.show({
        type: 'info',
        text1: '알림',
        text2: data.message || '강아지가 짖었습니다!',
        position: 'top',
        visibilityTime: 4000,
      });
    });
    source.addEventListener('error', (err) => {
      console.error('SSE 오류:', err);
    });
    return () => source.close();
  }, []);
  return null;
}
