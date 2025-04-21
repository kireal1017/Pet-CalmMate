import librosa
import numpy as np
import os
from tqdm import *
from sklearn.model_selection import train_test_split
from ssqueezepy import cwt, stft, ssq_cwt, ssq_stft, Wavelet
import soundfile as sf
from scipy.signal import resample
from ssqueezepy import ssq_stft


# 읽기 파일 경로 가져오기
def get_wav_files(parent_dir, sub_dirs):
    wav_files = []
    for l, sub_dir in enumerate(sub_dirs):
        wav_path = os.path.join(parent_dir, sub_dir)
        for (dirpath, dirnames, filenames) in os.walk(wav_path):  # os.walk() 방법은 디렉토리 트리에서 디렉토리에 출력되는 파일 이름을 위 또는 아래로 이동하는 데 사용됩니다.
            for filename in filenames:
                if filename.endswith('.wav') or filename.endswith('.WAV'):
                    filename_path = os.sep.join([dirpath, filename])
                    filename_path = os.path.realpath(filename_path)
                    wav_files.append(filename_path)
    return wav_files


parent_dir = r'/home/AI2022/ycj/1_shuoshi/data/wav'
data_save_root = r'/home/AI2022/ycj/1_shuoshi/data/dog_root_envelope'  # 데이터 저장소 주소
sub_dir = ['00', '01', '02', '03', '04']  # 하위 디렉토리
# sub_dir = ['fold1', 'fold2', 'fold3', 'fold4', 'fold5', 'fold6', 'fold7', 'fold8', 'fold9', 'fold10']
file_names = get_wav_files(parent_dir, sub_dir)  # 데이터 폴더의 모든 파일 경로 가져오기

if not os.path.exists(data_save_root):  # 파일을 저장할 폴더의 존재 여부 판단하기
    os.makedirs(data_save_root)

features_all = []
labels_all = []
index = 0

def feature_out(y_16k, label):
    ssq_spec, _, _, _ = ssq_stft(x=y_16k, n_fft=512, hop_len=160, window='hann', fs=16000)
    features_all.append(ssq_spec)
    labels_all.append(label)
    return 0


for file in tqdm(file_names):
    label_str = file.split('/')[-2]
    label = int(label_str)
    y, sr = librosa.load(file, sr=16000)  #원본 샘플링 빈도로 데이터 파일 읽기

    if label_str == '00' or label_str == '01':
        #  long
        if len(y) >= 64000:
            y1 = y[:64000]
            feature_out(y1, label)

        else:
            number = 64000 - int(len(y))
            array = np.full(number, 0)
            y2 = np.concatenate((y, array), axis=0)
            feature_out(y2, label)

    elif label_str == '02' or label_str == '03' or label_str == '04':
        # short
        if len(y) >= 80000:
            y1 = y[:64000]
            y2 = y[len(y) - 64000:len(y)]
            feature_out(y1, label)
            feature_out(y2, label)


        elif len(y) < 80000 and len(y) >= 64000:
            y3 = y[:64000]
            feature = feature_out(y3, label)
        elif len(y) < 64000:
            number = 64000 - int(len(y))
            array = np.full(number, 0)
            y4 = np.concatenate((y, array), axis=0)
            feature_out(y4, label)

    else:
        print("데이터를 한 번 처리할지 두 번 처리할지 결정할 수 없는 상황이기 때문에,
이 라벨은 분류 로직에서 오류를 발생시킬 수 있다.")

print('features_all:{}'.format(np.shape(features_all)))
print('labels_all:{}'.format(np.shape(labels_all)))

images = np.array(features_all, dtype=float)
labels = np.array(labels_all, dtype=int)

test_x, train_x, test_y, train_y = train_test_split(images, labels, train_size=0.2, stratify=labels, shuffle=True)
np.save(data_save_root + "/train_x.npy", train_x)
np.save(data_save_root + "/train_y.npy", train_y)
np.save(data_save_root + "/test_x.npy", test_x)
np.save(data_save_root + "/test_y.npy", test_y)
