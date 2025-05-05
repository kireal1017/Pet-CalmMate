import React from 'react';
import { View, StyleSheet, Image, TouchableOpacity, Dimensions } from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';


const { width } = Dimensions.get('window');

const Header: React.FC = () => {
  const router = useRouter();
  return (
    <View style={styles.header}>
      <Image
        source={require('./assets/dog_logo.png')} 
        style={styles.logo}
        resizeMode="contain"
      />
      <View style={styles.rightIcons}>
        <TouchableOpacity style={styles.iconButton}>
          <MaterialIcons name="notifications-none" size={28} color="#222" />
        </TouchableOpacity>
        <TouchableOpacity style={styles.profileButton} onPress={() => router.navigate('/(tabs)/OptionScreen')}>
          <Image
            source={require('./assets/profile.png')} 
            style={styles.profileImage}
          />
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  header: {
    height: 57,
    width: '100%',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 12,
    backgroundColor: '#fff',
  },
  logo: {
    width: 47,
    height: 47,
  },
  rightIcons: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  iconButton: {
    marginRight: 10,
  },
  profileButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    overflow: 'hidden',
    borderWidth: 1,
    borderColor: '#D9D9D9',
  },
  profileImage: {
    width: 40,
    height: 40,
  },
});

export default Header;
