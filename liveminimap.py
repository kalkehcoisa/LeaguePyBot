import cv2
import numpy as np
from mss import mss
from time import time
import multiprocessing

# Base
# bounding_box = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}

# League Client
bounding_box ={'left': 150, 'top': 100, 'width': 1770, 'height': 700}

ratio = 1

sct = mss()

def capture_window():
    sct_img = sct.grab(bounding_box)
    width = int(bounding_box['width']/ratio)
    height = int(bounding_box['height']/ratio)
    sct_img = cv2.resize(np.array(sct_img),(width,height))
    return sct_img


def template_match(img_bgr, template_img, name):
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    template = cv2.imread(template_img, 0)
    # w, h = template.shape[::-1]
    width = int(template.shape[1]/ratio)
    height = int(template.shape[0]/ratio)
    template = cv2.resize(template, (width,height))

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.95
    loc = np.where(res > threshold)

    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_bgr, pt, (pt[0]+width, pt[1]+height), (0,255,255), 1)
        cv2.putText(img_bgr, name, (pt[0], pt[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,255), 2)

    return img_bgr


loop_time = time()

while True:
    sct_img = capture_window()
    path = ['patterns/enemy/champion.png', 'patterns/enemy/minion.png', 'patterns/enemy/tower.png', 'patterns/ally/minion.png']
    name = ['champion', 'minion', 'tower', 'ally']
    processes = []
    for i in range(4):
        p = multiprocessing.Process(target=template_match, args=(sct_img,path[i],name[i]))
        processes.append(p)
        p.start()
    for process in processes:
        process.join()
    cv2.imshow('screen', sct_img)
 
    print('FPS {}'.format(round(1 / (time() - loop_time), 2)))
    loop_time = time()

    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break