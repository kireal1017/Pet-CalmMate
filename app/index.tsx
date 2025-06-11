import { Redirect } from 'expo-router';
import { useAuth } from '../share/store/auth_store';

export default function Index() {
  const { token, userId, loading } = useAuth();

  if (loading) {
    return null;
  }

  if (!token || !userId) {
    return <Redirect href="/auth_main" />;
  }
  return <Redirect href="/(tabs)/main_home" />;
}
