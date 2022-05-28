import cv2
import numpy as np 
import os.path
import os

print('============TRAINING==============')
print(' 1. Camera')
print(' 2. Image')
print(' 3. Folder')
print('Choose type of train:')
x = input()
if x == str(1):
    print('==========Camera==============')
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier("Model/haarcascade_frontalface_alt.xml")
    #haarcascade_frontalface_alt.xml: Bộ lọc quét toàn ảnh để tìm ra khu vực mặt
    #Trả về hình ảnh khuôn mặt là face_cascade

    skip = 0
    face_data = []
    dataset_path = "./face_dataset/"

    file_name = input("Enter the name of person : ") + " "

    while True:
        # Đọc hình ảnh từ camera
        ret,frame = cap.read()
 
        # Chuyển hình ảnh về màu xám
        gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        if ret == False:
            continue

        # Nhận diện các khung chứa khuôn mặt khác nhau trong camera
        faces = face_cascade.detectMultiScale(gray_frame,1.3,5)
        if len(faces) == 0:
            continue
        
        k = 1
 
        # Sắp xếp các khung chứa khuôn mặt theo thứ tự từ gần ra xa so với camera
        faces = sorted(faces, key = lambda x : x[2]*x[3] , reverse = True)
        skip += 1
        for face in faces[:1]:      # Với mỗi khung chứa khuôn mặt
            x,y,w,h = face          # Lấy tọa độ và kích thước khung chứa khuôn mặt đó
            x -= 2
            y -= 2
            w = round((w - 2) * 1)
            h = round((h - 2) * 1.2)
                
            offset1 = 6                        # Phần dư trong khung chứa khuôn mặt
            offset2 = 5                          # Phần dư trong khung chứa khuôn mặt
            face_offset = frame[y-offset1:y+h+offset1,x-offset2:x+w+offset2]    # Resize khung hình camera còn mỗi mặt 
            face_selection = cv2.resize(face_offset,(100,120))              # Frame khuôn mặt

            if skip % 10 == 0:                          # Sau mỗi 10 frame thì thêm khuôn mặt vào face_data
                face_data = [face_selection]

            cv2.imshow(str(k), face_selection)          # Show các frame khuôn mặt trong giao diện phụ
            k += 1
        
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2) # Trong camera thì khung cái mặt bằng khung màu xanh

        cv2.imshow("faces",frame)                       # Show các frame khuôn mặt trong một giao diện chính

        key_pressed = cv2.waitKey(1) & 0xFF             # Tạo nút bấm khi đang thực thi
        if key_pressed == ord('q'):                     # Khi bấm nút thì kết thúc 
            break

    face_data = np.array(face_data)
    face_data = face_data.reshape((face_data.shape[0], -1))

    print('================Data đã lưu=================')
    print(face_data)
    print('=================Kích thước=================')
    print (face_data.shape)

    np.save(dataset_path + file_name, face_data)
    print ("Đã lưu dữ liệu : {}".format(dataset_path + file_name + '.npy'))
    
    cap.release()
    cv2.destroyAllWindows()

elif x == str(2):
    print('==========Read image==============')
    face_cascade = cv2.CascadeClassifier("Model/haarcascade_frontalface_alt.xml")
    face_data = []
    dataset_path = "./face_dataset/"
    file_name = input("Enter the name of person : ")
    picture = input("Link image: ")
    frame = cv2.imread(picture)
    # Chuyển hình ảnh về màu xám
    gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    # Nhận diện các khung chứa khuôn mặt khác nhau trong camera
    faces = face_cascade.detectMultiScale(gray_frame,1.3,5)
    # Sắp xếp các khung chứa khuôn mặt theo thứ tự từ gần ra xa so với camera
    faces = sorted(faces, key = lambda x : x[2]*x[3] , reverse = True)
    # Chỉnh lại thông số khuôn mặt hợp lý
    for face in faces[:1]:      # Với mỗi khung chứa khuôn mặt
        x,y,w,h = face          # Lấy tọa độ và kích thước khung chứa khuôn mặt đó
        x -= 2
        y -= 2
        w = round((w - 2) * 1)
        h = round((h - 2) * 1.2)        
        offset1 = 6                        # Phần dư trong khung chứa khuôn mặt
        offset2 = 5                          # Phần dư trong khung chứa khuôn mặt
        face_offset = frame[y-offset1:y+h+offset1,x-offset2:x+w+offset2]    # Resize khung hình camera còn mỗi mặt 
        face_selection = cv2.resize(face_offset,(100,120))              # Frame khuôn mặt                                   
        face_data.append(face_selection)        
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2) # Trong camera thì khung cái mặt bằng khung màu xanh
    cv2.imshow("faces",frame)                       # Show các frame khuôn mặt trong một giao diện chính
    face_data = np.array(face_data)
    face_data = face_data.reshape((face_data.shape[0], -1))
    np.save(dataset_path + file_name, face_data)
    
    
    print('================Data đã lưu=================')
    print(face_data)
    print('=================Kích thước=================')
    print (face_data.shape)

    
    print ("Dataset saved at : {}".format(dataset_path + file_name + '.npy'))
    if cv2.waitKey(0) == 27:
        exit(0)
        
elif x == str(3):
    print('==========Read folder==============')
    face_cascade = cv2.CascadeClassifier("Model/haarcascade_frontalface_alt.xml")
    #haarcascade_frontalface_alt.xml: Bộ lọc quét toàn ảnh để tìm ra khu vực mặt
    #Trả về hình ảnh khuôn mặt là face_cascade

    dataset_path = "./face_dataset/"

    file_name = ""
    folder = input("Link folder: ")
    
    for fx in os.listdir(folder):
        face_data = []
        if fx.endswith('.jpeg'):
            file_name = fx[:-11]
        print(fx)
        print(file_name)
        link = "./" + folder + "/" + fx
        frame = cv2.imread(link)

        # Chuyển hình ảnh về màu xám
        gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        # Nhận diện các khung chứa khuôn mặt khác nhau trong camera
        faces = face_cascade.detectMultiScale(gray_frame,1.3,5)

        # Sắp xếp các khung chứa khuôn mặt theo thứ tự từ gần ra xa so với camera
        faces = sorted(faces, key = lambda x : x[2]*x[3] , reverse = True)
        for face in faces[:1]:      # Với mỗi khung chứa khuôn mặt
            x,y,w,h = face          # Lấy tọa độ và kích thước khung chứa khuôn mặt đó
            x -= 2
            y -= 2
            w = round((w - 2) * 1)
            h = round((h - 2) * 1.2)
                
            offset1 = 6                        # Phần dư trong khung chứa khuôn mặt
            offset2 = 5                          # Phần dư trong khung chứa khuôn mặt
            face_offset = frame[y-offset1:y+h+offset1,x-offset2:x+w+offset2]    # Resize khung hình camera còn mỗi mặt 
            face_selection = cv2.resize(face_offset,(100,120))              # Frame khuôn mặt
                        
            face_data.append(face_selection)
            
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2) # Trong camera thì khung cái mặt bằng khung màu xanh

        if len(face_data) > 0:
            cv2.imshow("faces",frame)                       # Show các frame khuôn mặt trong một giao diện chính

            face_data = np.array(face_data)
            face_data = face_data.reshape((face_data.shape[0], -1))

            print('================Data đã lưu=================')
            print(face_data)
            print('=================Kích thước=================')
            print (face_data.shape)

            full_name = file_name
            file_name = file_name + "0"
            Samefile = 0
            Savefile = dataset_path + file_name + ".npy"
            while os.path.exists(Savefile):
                Samefile += 1
                file_name = full_name + str(Samefile)
                Savefile = dataset_path + file_name + ".npy"
            
            np.save(dataset_path + file_name, face_data)
            print ("Dataset saved at : {}".format(dataset_path + file_name + '.npy'))
            cv2.waitKey(1000)
            print('================Hoàn tất=================\n\n')
        else:
            print('\nKhông tìm thầy không mặt\n')



