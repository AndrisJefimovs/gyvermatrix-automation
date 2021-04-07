import cv2
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import json

# Открываем стрим в браузере и минимизируем
PATH = 'C:\Program Files (x86)\chromedriver.exe'
driver = webdriver.Chrome(PATH)
driver.minimize_window()
driver.get('https://www.youtube.com/embed/vu-GBby44dQ')
# Даём загрузится
sleep(5)
# Запускаем видео
playButton = driver.find_element_by_css_selector(
    'button[aria-label="Play"]')
playButton.click()
sleep(5)

# Функция для считывания светодиодов на трансляции
def makeSnapshot():
    driver.save_screenshot('screenshot.png')
    # Загружаем фото, 0 - без цвета
    img = cv2.imread('screenshot.png', 0)
    # Создаём точки по которым будет выравниватся картинка
    # Точки можно найти открыв только что сохранённый скриншот в Paint и в углу взять координаты
    pts1 = np.float32([[103, 14], [916, 10], [111, 549], [901, 542]])
    pts2 = np.float32([[0, 0], [1034, 0], [0, 576], [1034, 576]])
    # Выпрямляем перспективу
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(img, matrix, (1034, 576))
    # Массив для точек с фото
    bitmap = []
    # Пробегаемя по всей матрице размером в 96 на 64
    for y in range(64):
        # В большой массив будем класть по массиву для каждой строки
        bitmapRow = []
        for x in range(96):
            # Сохраняем СВЕТЛОСТЬ пикселя в переменную ибо фото загрузили чёрно-белым
            k = result[round(y*(576/64)+(576/64/2)),
                       round(x*(1034/96)+(1034/96/2))]
            # Считанное в массив текущей строки, если больше 130 тогда 1, иначе 0
            # 0- выкл, 1 - вкл
            bitmapRow.append(0 if (k < 130) else 1)
            # Ставим белую точку на место, где брался цвет
            result[round(y*(576/64)+(576/64/2)),
                   round(x*(1034/96)+(1034/96/2))] = 255
        # Кладём массив строки в общий
        bitmap.append(bitmapRow)
    # Сохраняем фото с белыми точками на пикселях
    cv2.imwrite('result.png', result)
    # Делаем JSON'чик с нолями и единицами
    jsonBitmap = json.dumps(bitmap)
    # Сохраняем его в файл
    f = open('bitmap.json', 'w')
    f.write(jsonBitmap)
    f.close()
