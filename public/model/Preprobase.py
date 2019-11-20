import cv2 as cv
import numpy as np
import os
basePath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Preprobase:
    hogPro = basePath + '/model/HOG/deploy.prototxt.txt'
    hogModel = basePath + '/model/HOG/res10_300x300_ssd_iter_140000.caffemodel'

    def detectFace(self,img):
        model = cv.dnn.readNetFromCaffe(self.hogPro, self.hogModel)
        (h, w) = img.shape[:2]
        s=300
        original_image = cv.cvtColor(img,cv.COLOR_BGR2RGB)
        blob = cv.dnn.blobFromImage(cv.resize(original_image, (s,s)), 1.0, (s, s), (103.93, 116.77, 123.68))
        model.setInput(blob)
        detections = model.forward()
        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.7:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
        
        startX -= 5
        startY -= 5
        endX += 5
        endY += 5
        width = endX - startX
        height = endY - startY 
        centerX = int((endX + startX)/2)
        centerY = int((endY + startY)/2)

        return (startX, startY, width, height, centerX, centerY)
    
    def resizedFlipSave(self, cropImage,size,path):
        extension = '.jpg'
        resized = cv.resize(cropImage, (size, size))
        cv.imwrite(path+'.jpg', resized)

    def detectCropResize(self,path,original_image,size,face):
        (x, y, w, h) = face
        self.resizedFlipSave(original_image[y:y+w, x:x+h],size,path+'-N')
        for i in range(1,26,1):
            self.resizedFlipSave(original_image[y:y+w, x+i:x+i+h],size,path+'-xL-'+str(i))
            self.resizedFlipSave(original_image[y:y+w, x-i:x-i+h],size,path+'-xR-'+str(i))
            self.resizedFlipSave(original_image[y-i:y-i+w, x:x+h],size,path+'-yU-'+str(i))
            self.resizedFlipSave(original_image[y+i:y+i+w, x:x+h],size,path+'-yD-'+str(i))
            self.resizedFlipSave(original_image[y+i:y+w+i, x+i:x+h+i],size,path+'-d1L-'+str(i))
            self.resizedFlipSave(original_image[y-i:y+w-i, x-i:x+h-i],size,path+'-d1R-'+str(i))
            self.resizedFlipSave(original_image[y-i:y+w-i, x+i:x+h+i],size,path+'-d2L-'+str(i))
            self.resizedFlipSave(original_image[y+i:y+w+i, x-i:x+h-i],size,path+'-d2R-'+str(i))
        return True
    
    def cropresize(self,original_image):
        (x, y, w, h, c) = self.detectFace(original_image)
        if (w > h):
            h = w
        else:
            w = h
        newC = int((x+x+w)/2)
        diffC = newC - c
        x = x - diffC
        image = original_image[int(y):int(y)+int(w), int(x):int(x)+int(h)]
        resized = cv.resize(image, (224, 224))
        cv.imwrite(basePath+'/model/result.jpg', resized)
        reshapeImg = resized.reshape(1,224,224,3)
        return reshapeImg
    
    def drawRealpictContour(self,original_image,imagePath):
        (column, row, width, height, cx, cy) = self.detectFace(original_image)
        # if(width > height):
        #     height = width
        # else:
        #     width = height
        # newCX = int((column +column+width)/2)
        # diffCX = newCX - cx
        # column = column - diffCX
        height = width
        newCY = int((row +row+height)/2)
        diffCY = newCY - cy
        row = row - diffCY

        cv.rectangle(
            original_image,
            (column, row),
            (column + width, row + height),
            (0, 255, 0),
            4
        )
        cv.imwrite(imagePath, original_image)
        return (column, row, width, height)