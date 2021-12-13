import pandas as pd
import cv2
import numpy as np

img = cv2.imread('color.jpeg')

index=['color','color_name','hex','R','G','B']
csv = pd.read_csv('colors.csv', names=index, header=None)

clicked=False
r=g=b=xpos=ypos=0

# mouse click function - helps in the process of double click
'''The function parameters have the event name, (x,y) coordinates of the mouse position, etc. 
Here, we check if the event is double-clicked then we calculate and set the r,g,b values 
along with x,y positions of the mouse.'''
def mouse_click(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global g,b,r,xpos,ypos,clicked
        clicked=True
        xpos=x
        ypos=y
        b,g,r=img[y,x]
        b=int(b)
        g=int(g)
        r=int(r)

# color recognition function
#The function below will be called when you will double-click on an area of the image.
# It will return the name of the colour and the RGB values for that colour.
'''We have the r,g and b values. Now, we need another function which will return us the color name from RGB values. 
To get the color name, we calculate a distance(d) which tells us how close we are to color and 
choose the one having minimum distance.'''
def recognize_color(R,G,B):
    minimum=10000
    for i in range(len(csv)):
        d = abs(R-int(csv.loc[i,'R'])) + abs(G-int(csv.loc[i,'G'])) + abs(B-int(csv.loc[i,'B']))
        if (d<=minimum):
            minimum=d
            cname=csv.loc[i,'color_name']
    return cname

'''First, we created a window in which the input image will display. 
Then, we set a callback function which will be called when a mouse event happens.
'''
cv2.namedWindow('Color Detection')
cv2.setMouseCallback('Color Detection', mouse_click)

while(1):
    cv2.imshow('Color Detection', img)
    if (clicked):
        # cv2.rectangle(image, startpoint, endpoint, color, thickness)-1 fills entire rectangle
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)
        #creating textstring to display (color name and RGB values)
        text = recognize_color(r,g,b) + 'R=' + str(r) + 'G=' + str(g) + 'B=' + str(b)
        # cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
        cv2.putText(img,text,(50,50),2,0.8,(255,255,255),2,cv2.LINE_AA)
        # for light colors
        if (r+g+b>=600):
            cv2.putText(img,text,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)
        clicked=False

    # breaking the loop one 'esc' is hit
    if cv2.waitKey(20) & 0xFF==27:
        break

cv2.destroyAllWindows()