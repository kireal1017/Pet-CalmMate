import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, TextInput } from 'react-native';
import { MaterialIcons, Feather } from '@expo/vector-icons';
import Header2 from './Header2';
import Footer from './Footer';

const GroupScreen = () => {
  const groupName = 'OO의 그룹';
  const participants = [
    { id: 1, name: '나' }
  ];

  const handleInvite = () => {};
  const handleMenu = () => {};
  const handleParticipantPress = (participant) => {};

  return (
    <View style={styles.container}>
      <Header2 />
      <View style={styles.body}>
  
        <View style={styles.header}>
          <Text style={styles.headerTitle}>{groupName}</Text>
          <TouchableOpacity style={styles.menuButton} onPress={handleMenu}>
            <Feather name="menu" size={28} color="#222" />
          </TouchableOpacity>
        </View>

 
        <View style={styles.inviteRow}>
          <TextInput
            style={styles.searchInput}
            placeholder="참여자 목록"
            placeholderTextColor="#B48B8B"
            editable={false}
          />
          <TouchableOpacity style={styles.inviteButton} onPress={handleInvite}>
            <Text style={styles.inviteButtonText}>초대하기</Text>
          </TouchableOpacity>
        </View>

  
        <View style={styles.listContainer}>
          {participants.map((p) => (
            <TouchableOpacity
              key={p.id}
              style={styles.participantRow}
              onPress={() => handleParticipantPress(p)}
              activeOpacity={0.7}
            >
              <View style={styles.avatarCircle}>
                <MaterialIcons name="person" size={24} color="#B48B8B" />
              </View>
              <Text style={styles.participantName}>{p.name}</Text>
            </TouchableOpacity>
          ))}
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
    padding: 0,
    borderWidth: 1,
    borderColor: '#FFDEDE',
  },
  body: {
    flex: 1,
   
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 14,
    paddingTop: 18,
    paddingBottom: 8,
    backgroundColor: '#fff',
    borderBottomWidth: 0.5,
    borderBottomColor: '#FFDEDE',
  },
  headerTitle: {
    fontSize: 19,
    fontWeight: 'bold',
    color: '#222',
  },
  menuButton: {
    padding: 4,
  },
  inviteRow: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 14,
    paddingTop: 12,
    paddingBottom: 6,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#FFDEDE',
  },
  searchInput: {
    flex: 1,
    height: 32,
    backgroundColor: '#fff',
    borderRadius: 6,
    paddingHorizontal: 10,
    fontSize: 13,
    color: '#222',
    borderWidth: 1,
    borderColor: '#FFDEDE',
  },
  inviteButton: {
    marginLeft: 8,
    backgroundColor: '#FFD5D5',
    borderRadius: 6,
    paddingHorizontal: 16,
    paddingVertical: 7,
    justifyContent: 'center',
    alignItems: 'center',
  },
  inviteButtonText: {
    color: '#D94C4C',
    fontSize: 13,
    fontWeight: 'bold',
  },
  listContainer: {
    marginTop: 4,
    marginHorizontal: 14,
    backgroundColor: '#fff',
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#FFDEDE',
    paddingVertical: 2,
    paddingHorizontal: 0,
    minHeight: 60,
  },
  participantRow: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 8,
    paddingHorizontal: 8,
    borderBottomWidth: 0.5,
    borderBottomColor: '#FFDEDE',
  },
  avatarCircle: {
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: '#FFD5D5',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 8,
  },
  participantName: {
    fontSize: 15,
    color: '#222',
    fontWeight: '500',
  },
});

export default GroupScreen;
