# Coin Classifier with opencv by classifying
# on the basis of radii and brightness values
# Also estimates total value of the coins

import numpy as np
from google.colab.patches import cv2_imshow
import cv2


def av_pix(img, circles, size):  # Estimates brightness values for coins
    av_value = []
    for coords in circles[0, :]:
        col = np.mean(img[coords[1]-size:coords[1]+size, coords[0]-size:coords[0]+size])
        # print(img[coords[1]-size:coords[1]+size,coords[0]-size:coords[0]+size])
        av_value.append(col)
    return av_value


def get_radius(circles):  # Estimates radius of different coins
    radius = []
    for coords in circles[0, :]:
        radius.append(coords[2])
    return radius


# Reads image to Grayscale
img = cv2.imread('/content/drive/My Drive/capstone_coins.png', cv2.IMREAD_GRAYSCALE)

# Reads image as it is
original_image = cv2.imread('/content/drive/My Drive/capstone_coins.png', 1)

# Blurs grayscale image
img = cv2.GaussianBlur(img, (5, 5), 0)

# Hough Cirlce Transform(opencv)
circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,0.9,120,param1=50,param2=27,minRadius=40,maxRadius=160)

# print(circles)

circles = np.uint16(np.around(circles))
count = 1
for i in circles[0, :]:

    # draw the outer circle
    cv2.circle(original_image, (i[0],i[1]), i[2], (0,255,0), 2)
    # draw the center of the circle
    cv2.circle(original_image, (i[0],i[1]), 2, (0,0,255), 3)
    # cv2.putText(original_image, str(count),(i[0],i[1]), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 2)
    count += 1

radii = get_radius(circles)
# print(radii)  #prints radii of coins

bright_values = av_pix(img, circles, 20)
# print(bright_values)  #prints brightness values


# Classifying coins by radii and brightness value
val = []
for a, b in zip(bright_values, radii):
    if a > 170 and b > 60:
        val.append(10)
    elif a > 170 and b <= 60:
        val.append(5)
    elif a < 170 and b > 70:
        val.append(50)
    elif a < 170 and b > 60:
        val.append(2)
    elif a < 170 and b < 60:
        val.append(1)
# print(val)

# Printing estimated value ef each coin on itself
count_2 = 0
for i in circles[0, :]:
    cv2.putText(original_image, str(val[count_2]) + 'p', (i[0],i[1]), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 2)
    count_2 += 1

# Printing total estimated value
cv2.putText(original_image, 'ESTIMATED TOTAL VALUE:' + str(sum(val)) + 'p', (10,100), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)

# Opens image
cv2_imshow(original_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
