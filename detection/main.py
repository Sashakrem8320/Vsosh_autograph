import serial
import os
from ultralytics import YOLO
import serial.tools.list_ports
import find
import time
import cv2
model = YOLO('best.pt')
model.fuse()
# Функция для открытия последовательного порта
def open_serial_port():
    ports = serial.tools.list_ports.comports()  # Получаем список доступных портов
    for port in ports:
        try:
            s = serial.Serial(port.device, 115200, timeout=10)
            print(f'Connected to: {s.name}')
            return s  # Возвращаем открытый порт
        except (serial.SerialException, OSError):
            print(f'Failed to connect to {port.device}. Trying next port...')
    return None  # Если не удалось подключиться ни к одному порту

# Открытие последовательного порта GRBL
s = open_serial_port()
if s is None:
    print("Не удалось подключиться ни к одному порту. Завершение работы.")
    exit(1)  # Завершаем работу, если не удалось подключиться

print('Serial port open: ' + str(s.is_open))

def reset():
    send_gcode('$X')
    send_gcode('M3S40')
    send_gcode('$H')
    send_gcode('F2000')
    send_gcode('G92X0Y0')
    send_gcode('M3S40')
    print("Готов к работе")

# Функция для отправки G-кода
def send_gcode(gcode):

    s.write(str.encode(gcode + "\n"))
    print(s.readline().strip().decode('utf-8'))
    print('Sending: ' + gcode)

# Пробуждение GRBL
reset()

# Функция для обработки команд из файла
def process_commands_from_file(filename):
    with open(filename, 'r') as file:
        for line in file:
            if find.Chek(model) == 1:
                send_gcode('M3 S40')
                while find.Chek(model) == 1:
                    pass
                send_gcode('M5 S40')
            line = line.strip()
            if line.startswith('G1'):  # Обрабатываем только команды, начинающиеся с G1
                parts = line.split()
                new_command = []
                for part in parts:
                    if part.startswith('X'):
                        x_value = float(part[1:]) + x_coefficient
                        new_command.append(f'X{x_value:.2f}')  # Форматируем до 2 знаков после запятой
                    elif part.startswith('Y'):
                        y_value = float(part[1:]) + y_coefficient
                        new_command.append(f'Y{y_value:.2f}')  # Форматируем до 2 знаков после запятой
                    else:
                        new_command.append(part)
                # Отправляем измененную команду
                send_gcode(' '.join(new_command))
            else:
                # Если команда не G1, просто отправляем её без изменений
                send_gcode(line)

directory = r''
filename = '../drawing_app/gcode_files/drawing.gcode'

# Обработка команд из файла


kfx = 3.1
kfy = 3.2



while True:
    y, x, height, width = find.process_webcam_with_detection_low(model)
    print((width - y), x)
    #input()

    x_coefficient = ((width - y) - 120) / kfx
    y_coefficient = (x - 20) / kfy
    print(x_coefficient)
    print("ОК")


    # Если объект был убран, обрабатываем команды из файла
    process_commands_from_file(os.path.join(directory, filename))
    # Отправка команды на возврат в начальную позицию
    send_gcode("M3 S40")
    send_gcode("G1 X0.00 Y0.00")
    time.sleep(1)


# Закрытие последовательного порта
s.close()