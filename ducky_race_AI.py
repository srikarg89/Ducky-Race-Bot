#C:\Users\Srikar\Documents\MyProjects\NeuralNetworks\duckyracetest
import pyautogui
import time
import cv2
import numpy

def dictToContours(pics_names):
    cnts_arr = {}
    minus_cnt = None
    for index in pics_names:
        name = pics_names[index]
        temp = str(i)
        image = cv2.imread("contours/"+name+".png")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
        _, contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        contours = list(reversed(sorted(contours, key=lambda c: cv2.contourArea(c))))
        num = 0
        while num < len(contours):
            [x, y, w, h] = cv2.boundingRect(contours[num])
            for a in range(num):
                [x1, y1, w1, h1] = cv2.boundingRect(contours[a])
                if x > x1 and y > y1 and x + w < x1 + w1 and y + h < y1 + h1:
                    contours.remove(contours[num])
                    num -= 1
                    break
            num += 1
        if len(contours) != 1:
            print("ERROR")
        cnts_arr[index] = contours[0]
    return cnts_arr

def contour_to_text(arr,contours):
    num = 0
    while num < len(contours):
        [x, y, w, h] = cv2.boundingRect(contours[num])
        for a in range(num):
            [x1, y1, w1, h1] = cv2.boundingRect(contours[a])
            if x > x1 and y > y1 and x + w < x1 + w1 and y + h < y1 + h1:
                contours.remove(contours[num])
                num -= 1
                break
        num += 1
    contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[0])
    text = ""
    for cnt in contours:
        minnum = ""
        minval = float("inf")
        for key in arr:
            num_cnt = arr[key]
            val = cv2.matchShapes(num_cnt, cnt, cv2.CONTOURS_MATCH_I1, 1)
            if val < minval:
                minval = val
                minnum = key
        print(minnum)
        text += minnum
    return text

answers_names = {}
questions_names = {}
for i in range(10):
    answers_names[str(i)] = "Contour"+str(i)
    questions_names[str(i)] = "QContour"+str(i)
questions_names["-"] = "QContourMinus"
answers_cnts = dictToContours(answers_names)
questions_cnts = dictToContours(questions_names)

location = []
location.append(pyautogui.locateOnScreen('pics/answer1.PNG',confidence=0.99))
location.append(pyautogui.locateOnScreen('pics/answer2.png',confidence=0.99))
location.append(pyautogui.locateOnScreen('pics/answer3.png',confidence=0.99))
location.append(pyautogui.locateOnScreen('pics/answer4.png',confidence=0.99))
question_loc = pyautogui.locateOnScreen('pics/question.png',confidence=0.9)
print(location)
for i in range(150): #Arbitrary value, can be changed to a higher number or even infinity

    #Find question contours
    im = pyautogui.screenshot(region=(question_loc.left+100,question_loc.top+10, 250, 50))
    image = numpy.array(im)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    ret, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    _, contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    #    text = pytesseract.image_to_string(Image.fromarray(image), lang='eng', config='--psm 7')
    #Find question text and the correct answer
    text = contour_to_text(questions_cnts, contours)
    if "-" not in text:
        print("Error: Minus not found")
    print(text)
    text = text.split('-')
    num1 = int(text[0])
    num2 = int(text[1])
    num3 = num1 - num2
    #    print(num3)

    answers = []
    count = 0
    tim = time.time()
    #Loop through answers and look for the correct one
    for loc in location:
        #Don't check last answer choice, assume it's right since we already looped through the rest.
        if count == 3:
            cent = pyautogui.center(location[count])
            pyautogui.click(cent.x, cent.y)
            break

        #Get answer choice contours and convert that to text
        im = pyautogui.screenshot(region=(loc.left + 20, loc.top + 5, 80, 50))
        image = numpy.array(im)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        ret, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        _, contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        contours = list(reversed(sorted(contours, key=lambda c: cv2.contourArea(c))))
        text = contour_to_text(answers_cnts,contours)
        value = int(text)

        #Check if answer choice is the correct answer, if so click
        if value == num3:
            cent = pyautogui.center(location[count])
            pyautogui.click(cent.x, cent.y)
            break
        answers.append(value)
        count += 1

    #Wait for the game to load the next question
    time.sleep(0.1)
