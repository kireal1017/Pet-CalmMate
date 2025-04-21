import math
import sys
import torch
import torch.nn as nn
import numpy as np
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter

from utils import Helper
from Second.t6_fc2 import AudioEmotionModel as Model
from torchsummary import summary  # 이 라이브러리는 PyTorch로 구성된 모델의 각 층 출력 크기를 확인할 수 있음
import datetime  # 날짜 및 시간 모듈

import os

from utils.Matrix import plot_confusion_matrix

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

helper = Helper.Helper()
model_name = Model.__name__
writer = SummaryWriter(os.path.join('runs', model_name))

torch.backends.cudnn.enabled = False
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(device)
num_epochs = 100
decay_epoch = 40
num_classes = 5
batch_size = 64
learning_rate = 0.001
weight_decay = 0.001
momentum = 0.9
print_counter = 5
data_dir = r'/home/AI2022/ycj/1_shuoshi/data/root'


save_dir = os.path.join('result', model_name)


if not os.path.exists(save_dir):
    os.makedirs(save_dir)


# 로그 파일
sys.stdout = Helper.Logger(os.path.join(save_dir, 'net.txt'.format()))

# 학습 및 테스트 데이터셋 불러오기
trainDataset = Helper.Dataset(os.path.realpath(os.path.join(data_dir, 'train_x.npy')),
                              os.path.realpath(os.path.join(data_dir, 'train_y.npy')))  # 학습 데이터셋 불러오기
train_loader = DataLoader(dataset=trainDataset, batch_size=batch_size, shuffle=True,
                          num_workers=0)  # num_workers는 멀티스레드 사용

testDataset = Helper.Dataset(os.path.realpath(os.path.join(data_dir, 'test_x.npy')),
                             os.path.realpath(os.path.join(data_dir, 'test_y.npy')))
test_loader = DataLoader(testDataset, batch_size, shuffle=True, num_workers=0)


# 랜덤 시드 고정 및 초기화
helper.setup_seed(20)
# 모델 초기화
model = Model(num_classes=num_classes)
model = model.to(device)


print('时间: ', datetime.datetime.now())
print(f'Batch_Size: {batch_size}, Learning_Rate: {learning_rate}, epochs: {num_epochs}')
summary(model, input_size=(16, 1, 64000))
criterion = nn.CrossEntropyLoss()  #교차 엔트로피 손실 함수
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate, weight_decay=weight_decay)  # 옵티마이저

# 모델 학습
total_samples = len(trainDataset)
n_iterations = math.ceil(total_samples / batch_size)  # 반복 횟수

tr_number = 0
tr_pre = 0
'''
    model.train(): BatchNormalization과 Dropout을 활성화
    model.eval(): BatchNormalization과 Dropout을 비활성화
'''
# model.train()  # Set model to train mode
early_stop_array = [None] * num_epochs  # 같은 길이의 빈 배열 생성
counter_time = 0
counter_freq = 0
pic_iterations, pic_loss = [], []
max_acc = []
val_List = []
train_list = []
valid_loss_curve = []
train_loss_curve = []

for epoch in range(num_epochs):
    tr_pre, tr_number = 0, 0
    train_loss_mean = 0
    valid_loss_mean = 0
    helper.adjust_learning_rate(optimizer, epoch, learning_rate, decay_epoch=decay_epoch)  # 반복 횟수 및 손실 저장
    save_va_acc = 0
    for i, (images, labels) in enumerate(train_loader):
        model.train()

        # 최대값 정규화
        images = images.reshape(-1, 1, 64000).to(device)
        labels = labels.reshape(-1).to(device)

        # 데이터 2차 셔플
        images, labels = helper.shuffle_Data(images, labels)

        outputs = model(images)
        loss = criterion(outputs, labels.long())

        train_loss_mean += loss.item()

        if i != 0:
            i = i + n_iterations * epoch
            pic_iterations.append(int(i)), pic_loss.append(
                float(loss.item()))  # # 배치 번호와 손실 값을 pic_iterations, pic_loss에 저장

        optimizer.zero_grad()	# 이전의 기울기 초기화
        loss.backward()	# 역전파 수행
        optimizer.step()	# 가중치 갱신

        _, argmax = torch.max(outputs, 1)  # argmax는 예측된 클래스(분류 결과)를 반환
        tr_number += argmax.size(0)  # tr_number는 전체 학습 데이터 수 누적
        tr_pre += (labels == argmax).sum().item()  # # tr_pre는 정답과 일치하는 개수(정확히 분류한 수)를 누적

        iter_number = math.ceil(total_samples / batch_size)
        if num_epochs >= 50:
            print_counter = 1
        valid_step = iter_number // print_counter
        if i % valid_step == (valid_step - 1):  # print every 100 mini-batches

            # #검증 데이터셋
            model.eval()	# 모델을 평가 모드로 설정 (Dropout, BatchNorm 비활성화)
            with torch.no_grad():	# 그래디언트 계산 비활성화 (메모리 및 속도 절약)
                correct = 0
                total = 0
                for images, labels in test_loader:
                    images = images.reshape(-1, 1, 64000).to(device)
                    labels = labels.reshape(-1).to(device)

                    out = model(images)
                    loss1 = criterion(out, labels.long())
                    valid_loss_mean += loss1.item()	# 검증 손실 누적

                    _, predicted = torch.max(out, 1)

                    total += predicted.size(0)	# 전체 샘플 수 누적
                    correct += (labels == predicted).sum().item()	# 정확히 맞춘 수 누적

                va_acc = correct / total	# 검증 정확도
                val = correct / total
                train = tr_pre / tr_number	# 학습 정확도
                val_List.append(float(val))		# 검증 정확도 리스트 저장
                train_list.append(float(train))	# 학습 정확도 리스트 저장
                max_acc.append(float(va_acc))	# 최고 정확도 추적용
                a = loss.item()			 # 현재 학습 손실
                b = loss1.item()			# 현재 검증 손실
                print(
                    f'epoch: {epoch + 1}/{num_epochs}, step: {i + 1}/{n_iterations}, tr_acc: {tr_pre / tr_number:.4f},va_acc: {va_acc:.4f} ,tr_loss: {a:.4f},vaa_loss:{b:.4f}')

                writer.add_scalar('train_acc', tr_pre / tr_number, epoch)	# TensorBoard 로그
                writer.add_scalar('val_acc', va_acc, epoch)
                writer.add_scalar('tr_loss', a, epoch)
                writer.add_scalar('vaa_loss', b, epoch)

                if va_acc > save_va_acc:
                    save_va_acc = va_acc		# 현재 에폭에서 가장 높은 검증 정확도 저장
                tr_pre, tr_number = 0, 0		# 정확도 계산용 카운터 초기화
    train_loss_mean /= len(train_loader)	# 에폭당 평균 학습 손실
    train_loss_curve.append(train_loss_mean)	# 학습 손실 그래프용 리스트 저장
    valid_loss_mean /= len(test_loader)		# 에폭당 평균 검증 손실
    valid_loss_curve.append(valid_loss_mean)	# 검증 손실 그래프용 리스트 저장


    def list_max(list):
        index = 0
        max = list[0]
        for i in range(0, len(list)):
            if (list[i] > max):
                max = list[i]
                index = i
        return (index, max)


    list = max_acc
    res = list_max(list)
    print(res)
    torch.save(model.state_dict(), 'result/' + model_name +'/model_' + str(batch_size) + '.pkl')

Emotion_kinds = num_classes
conf_matrix = torch.zeros(Emotion_kinds, Emotion_kinds)


def confusion_matrix(preds, labels, conf_matrix):
    preds = torch.argmax(preds, 1)
    for p, t in zip(preds, labels):
        conf_matrix[p, t] += 1
    return conf_matrix


# torch.no_grad()를 사용하면 테스트 시 GPU 메모리 사용량을 크게 줄일 수 있음
with torch.no_grad():
    for step, (imgs, targets) in enumerate(test_loader):
        imgs = imgs.reshape(-1, 1, 64000).to(device)
        targets = targets.reshape(-1).to(device)

        out = model(imgs)
        # # 혼동 행렬(confusion matrix) 계산
        conf_matrix = confusion_matrix(out, targets, conf_matrix)
        conf_matrix = conf_matrix.cpu()

conf_matrix = np.array(conf_matrix.cpu())  # 혼동 행렬을 GPU에서 CPU로 옮긴 후 NumPy 배열로 변환
corrects = conf_matrix.diagonal(offset=0)  # 대각선 값: 각 클래스에서 맞게 분류된 개수
per_kinds = conf_matrix.sum(axis=1)  # 각 클래스의 전체 테스트 샘플 수

print(conf_matrix)

# 각 감정(Emotion) 클래스의 정확도 출력
print("각 클래스의 총 샘플 수：", per_kinds)
print("각 클래스에서 정확히 분류된 개수：", corrects)
print("각 클래스의 분류 정확도：{0}".format([rate * 100 for rate in corrects / per_kinds]))

import numpy as np


# 실험 결과에서 정확도와 손실을 읽어옴
def calculate_prediction(metrix):
    """
    정확도 계산
    """
    label_pre = []
    current_sum = 0
    for i in range(metrix.shape[0]):
        current_sum += metrix[i][i]
        label_total_sum = metrix.sum(axis=0)[i]
        pre = round(100 * metrix[i][i] / label_total_sum, 4)
        label_pre.append(pre)
    print("각 클래스별 정밀도：", label_pre)
    all_pre = round(100 * current_sum / metrix.sum(), 4)
    print("전체 정밀도：", all_pre)
    return label_pre, all_pre


def calculate_recall(metrix):
    """
    먼저 각 클래스의 재현율(Recall)을 계산한 후,
    전체 평균 재현율을 계산함
    """
    label_recall = []
    for i in range(metrix.shape[0]):
        label_total_sum = metrix.sum(axis=1)[i]		# 실제 클래스 i의 총 개수
        label_correct_sum = metrix[i][i]			# 정확히 예측한 개수
        recall = 0
        if label_total_sum != 0:
            recall = round(100 * float(label_correct_sum) / float(label_total_sum), 4)

        label_recall.append(recall)
    print("각 클래스별 재현율：", label_recall)
    all_recall = round(np.array(label_recall).sum() / metrix.shape[0], 4)
    print("전체 재현율：", all_recall)
    return label_recall, all_recall


def calculate_f1(prediction, all_pre, recall, all_recall):
    """
    F1 점수 계산
    """
    all_f1 = []
    for i in range(len(prediction)):
        pre, reca = prediction[i], recall[i]
        f1 = 0
        if (pre + reca) != 0:
            f1 = round(2 * pre * reca / (pre + reca), 4)

        all_f1.append(f1)
    print("각 클래스별 F1 점수：", all_f1)
    print("전체 F1 점수：", round(2 * all_pre * all_recall / (all_pre + all_recall), 4))
    return all_f1


from matplotlib import pyplot as plt

#
loss_x = range(1, len(train_loss_curve) + 1)
train_loss_y = train_loss_curve
valid_loss_y = valid_loss_curve
plt.figure(1)
plt.plot(loss_x, train_loss_y, "r", label="Train_loss")
plt.plot(loss_x, valid_loss_y, "b", label="Valid_loss")
plt.ylabel('loss value')
plt.xlabel('epoch')
plt.legend()
plt.savefig("result/{}/loss_curve.png".format(model_name))

x_label = range(1, len(val_List) + 1)
plt.figure(2)
plt.plot(x_label, train_list, 'r', label='train acc')
plt.plot(x_label, val_List, 'b', label='validation acc')
plt.title('train and validation accuracy')
plt.xlabel('epochs')
plt.ylabel('acc value')
plt.legend()
plt.savefig("result/{}/acc_curve.png".format(model_name))
plt.show()
plt.close()

if __name__ == '__main__':
    metrix = conf_matrix
    print(metrix.sum(axis=0)[0], metrix.sum(axis=1)[0])
    label_pre, all_pre = calculate_prediction(metrix)
    label_recall, all_recall = calculate_recall(metrix)
    # ************************************
    calculate_f1(label_pre, all_pre, label_recall, all_recall)
    trans_mat = np.array(metrix)
    if True:
        labels = ['1', '2']
        label = labels
        plot_confusion_matrix(trans_mat, label, model_name=model_name)


print('현재 시간 : ', datetime.datetime.now())

