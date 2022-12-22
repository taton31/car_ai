import cv2 as cv
import numpy as np

SCREEN_HEIGHT = 900

def nothing(x): #функция, передаваемая в трэкбар, ничего не делает
    pass

def draw(event,x,y,flags,param):#рисует круг по нажатию правой кнопки мыши и прямую между двумя точками по нажатию левой кнопки мыши
    if event == cv.EVENT_RBUTTONDOWN:
        cv.circle(img,(x,y),20,(0,255,0),-1)
        lines.clear()
    if event == cv.EVENT_LBUTTONDOWN and len(lines)!=0:
        cv.line(img,(lines[0],lines[1]),(x,y),(255,0,0),5)
        lines[0]=x
        lines[1]=y
        print (f'{x},{SCREEN_HEIGHT - y}')
    elif event == cv.EVENT_LBUTTONDOWN:
        print (f'{x},{SCREEN_HEIGHT - y}')
        lines.append(x)
        lines.append(y)

    
lines=[]#нужно для рисования прямой
img = cv.imread('paint/shablon2.png',1)#читаем рисунок
events = [i for i in dir(cv) if 'EVENT' in i]# добавляем события

cv.namedWindow('image')
cv.createTrackbar('bright','image',0,30,nothing)
cv.setMouseCallback('image',draw)
while 1: #бесконечно обновляем рисунок с учетом нарисованного и передвинутого ползунка
    br = cv.getTrackbarPos('bright','image')#получаем значение ползунка
    IImg=br + img # увеличиваем яркость
    cv.imshow('image',IImg) #рисуем
    
    if cv.waitKey(20) & 0xFF == 32: # выходим по пробелу
        lines.clear()
        print()
cv.destroyAllWindows()#закрываем все окна
