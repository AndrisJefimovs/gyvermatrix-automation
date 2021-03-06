from telethon import TelegramClient
from time import sleep
# ⚠ Тут используем файл myScreenshoter.py ⚠
from myScreenshoter import makeSnapshot
import json

# Тут ключь для Telegram API
# Больше тут: https://core.telegram.org/api/obtaining_api_id#obtaining-api-id
api_id = '0123456'
api_hash = '01234abcdef56789ghijk'

# Расстояние от левого верхнего угла, где будет рисунок
offsetX = 0
offsetY = 0

# Это рисунок который мы хотим нарисовать
# Чтобы посмотреть что тут, можно вбить в поиск "1," :)
# 0 - выключить
# 1 - вкоючить
# 2 - пропустить
img = [
    [2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2],
    [2, 2, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2],
    [2, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 2, 2, 2],
    [2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 2, 2],
    [2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [2, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [2, 2, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [2, 2, 2, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0],
    [2, 2, 2, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0],
    [2, 2, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0],
    [2, 2, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0],
    [2, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
    [2, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
    [2, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0],
    [2, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
    [2, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
    [2, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 2],
    [2, 2, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 2, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2],
    [2, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 2],
    [2, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [2, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0],
    [2, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0],
    [2, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0],
    [2, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0]
]


async def main():
  # Выполнаем без остановки
    while True:
        # ⚠ Функция из второго файла
        # Делаем массив с матрицы на стриме
        makeSnapshot()
        # Шлём любое сообщение в чат Telegram @MatrixTest3
        message = await client.send_message(
            'MatrixTest3',
            '/set 0 0'
        )
        # Ждём немного
        sleep(0.25)
        # Читаем JSON с матрицы в массив
        f = open('bitmap.json')
        ledBitmap = json.loads(f.read())
        # Массив для координат светодиодов которые не совпадают с моей картикой
        bitmapError = []
        # Сравнивем матрицу с картинкой
        for y in range(len(img)):
            for x in range(len(img[0])):
              # Сравнение картинки с местом на матрице гду будем рисовать
              # Если 2 тогда пропускаем
                if(img[y][x] != ledBitmap[y+offsetY][x+offsetX] and img[y][x] != 2):
                  # Если есть отличие тогда координаты в массив
                    bitmapError.append([y, x])
        # Оповещение в консоль сколько светодиодов надо менять
        print('{} errors detected'.format(len(bitmapError)))
        # Пробегаемся по различиям
        for error in bitmapError:
          # Редактируем сообщение которые отсылали в начале
          # Тут вставляются координаты светодиодов несовпадающих с картинкой
            await message.edit('/{} {} {}'.format("set" if img[error[0]][error[1]] == 1 else "clr", error[1] + offsetX, error[0] + offsetY))
            # Также пишем консоль чтобы было видно что делается
            print('{} x: {} | y: {}'.format(
                "on" if img[error[0]][error[1]] == 1 else "off", error[1] + offsetX, error[0] + offsetY))
            # Немного задержки между редактированием но можно и без ибо ждём пока сообщение будет редактировано
            sleep(0.05)
        # Пауза между Скриншотами, лучше всего размером в задержку + немного
        # Мы пишем в чат, и если сразу опять смотреть ошибки они будут но они просто ещё не успели поменятся
        sleep(10)

# Логинимся в Telegram
with TelegramClient('anon', api_id, api_hash) as client:
    client.loop.run_until_complete(main())
