
import numpy as np
import cv2
import os

#========================== KNN ==============================
def distance(v1, v2):               # Tính khoảng cách euclid
    return np.sqrt(((v1-v2)**2).sum())

def knn(train, test, k=5):
    dist = []
    for i in range(train.shape[0]):

        ix = train[i, :-1]                      # Lấy tất cả các vector từng ảnh của từng người trong data có sẵn
        iy = train[i, -1]                       # Tên của từng người
        d = distance(test, ix)                  # So sánh sự khác nhau giữa test và ảnh của từng người
        dist.append([d, iy])
    dk = sorted(dist, key=lambda x: x[0])[:k]   # Chọn ra k người giống test nhất
    labels = np.array(dk)[:, -1]                # Tên của k người được chọn
    output = np.unique(labels, return_counts=True)  # Lấy tần suất của từng tên trong k người đó
    index = np.argmax(output[1])
    if np.max(output[1]) == 1 or np.count_nonzero(labels == labels[0]) > 1: return labels[0]
    return output[0][index]                         # Trả về tên người giống nhất
#=============================================================

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier("Model/haarcascade_frontalface_alt.xml")
#haarcascade_frontalface_alt.xml: Bộ lọc quét toàn ảnh để tìm ra khu vực mặt
#Trả về hình ảnh khuôn mặt là face_cascade

dataset_path = "./face_dataset/"
face_data = []
num_train = []
labels = []
class_id = 0
names = {}
sum = 0
right = 0
right1 = []
wrong1 =[]
who = None
number_people = 0
pre_people = None
# Bước chuẩn bị các data đã có sẵn (tập huấn luyện)
for fx in os.listdir(dataset_path):
    if fx.endswith('.npy'):
        names[class_id] = fx[:-5]
        data_item = np.load(dataset_path + fx)
        face_data.append(data_item)
        target = class_id * np.ones((data_item.shape[0],))
        
        if pre_people == None or pre_people != fx[:-5]:
            pre_people = fx[:-5]
            number_people = class_id
        
        num_train.append([number_people])
            
        class_id += 1
        labels.append(target)

print(names)
face_dataset = np.concatenate(face_data, axis=0)
face_labels = np.concatenate(labels, axis=0).reshape((-1, 1))


trainset = np.concatenate((face_dataset, num_train), axis=1)
print(trainset.shape)

font = cv2.FONT_HERSHEY_SIMPLEX

while True:
	ret, frame = cap.read()
	if ret == False:
		continue
	# Convert frame to grayscale
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# Detect multi faces in the image
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
 
	for face in faces:
		x, y, w, h = face
		x -= 2
		y -= 2
		w = round((w - 2) * 1)
		h = round((h - 2) * 1.2)

		offset1 = 6
		offset2 = 5
		face_offset = frame[y-offset1:y+h+offset1,x-offset2:x+w+offset2]    # Resize khung hình camera còn mỗi mặt 
		face_section = cv2.resize(face_offset, (100, 120))

		out = knn(trainset, face_section.flatten())

		# Draw rectangle in the original image
		cv2.putText(frame, names[int(out)],(x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,0,0),2,cv2.LINE_AA)
		if who == None or (who != None and who != names[int(out)]):
			who = names[int(out)]
			print('===========Dự đoán===============')
			print(names[int(out)])
		cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

	cv2.imshow("Faces", frame)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		print('=================================')
		break

cap.release()
cv2.destroyAllWindows()
