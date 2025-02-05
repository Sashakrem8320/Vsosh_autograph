import cv2
from ultralytics import YOLO
import random
import time

def process_webcam_with_detection(model):

    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        raise Exception("Ошибка: Не удалось открыть веб-камеру.")

    previous_box = None
    stationary_threshold = 300  # Порог для определения неподвижности
    stationary_time = 1  # Время в секундах, в течение которого объект должен быть неподвижен
    last_movement_time = time.time()  # Время последнего движения
    min_area = 600  # Минимальная площадь объекта для обработки

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Выполнить обнаружение объектов
        results = model(frame, iou=0.87, conf=0.6, imgsz=1024, verbose=False)

        # Проверка наличия обнаруженных объектов
        if results[0].boxes is not None and len(results[0].boxes) > 0:
            print(f"Обнаружено {len(results[0].boxes)} объектов.")

            # Получение координат и идентификаторов объектов
            boxes = results[0].boxes.xyxy.numpy().astype(int)

            # Проверка наличия идентификаторов
            if results[0].boxes.id is not None:
                ids = results[0].boxes.id.numpy().astype(int)
            else:
                print("Идентификаторы объектов не найдены.")
                ids = [0] * len(boxes)  # Присвоить идентификаторы по умолчанию, если они отсутствуют

            if len(boxes) == 1:  # Проверяем, если обнаружен только один объект
                current_box = boxes[0]
                # Вычисляем площадь текущего объекта
                width = current_box[2] - current_box[0]
                height = current_box[3] - current_box[1]
                area = width * height

                if area > min_area:  # Проверяем, больше ли площадь минимальной
                    if previous_box is not None:
                        # Проверка на неподвижность
                        if (abs(current_box[0] - previous_box[0]) < stationary_threshold and
                            abs(current_box[1] - previous_box[1]) < stationary_threshold and
                            abs(current_box[2] - previous_box[2]) < stationary_threshold and
                            abs(current_box[3] - previous_box[3]) < stationary_threshold):
                            # Если объект неподвижен, проверяем время
                            if time.time() - last_movement_time >= stationary_time:
                                # Вычисляем координаты центра объекта
                                center_x = (current_box[0] + current_box[2]) // 2
                                center_y = (current_box[1] + current_box[3]) // 2
                                return center_x, center_y
                        else:
                            print("Объект движется.")
                            last_movement_time = time.time()  # Обновляем время последнего движения
                    previous_box = current_box  # Обновляем предыдущие координаты
                else:
                    print(f"Объект слишком мал (площадь: {area}), игнорируем.")

            else:
                print("Объекты не обнаружены или их больше одного.")

            for box, id in zip(boxes, ids):
                # Вычисляем площадь текущего объекта
                width = box[2] - box[0]
                height = box[3] - box[1]
                area = width * height

                if area > min_area:  # Проверяем, больше ли площадь минимальной
                    # Сгенерировать случайный цвет для каждого объекта на основе его ID
                    random.seed(int(id))
                    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

                    cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), color, 2)
                    cv2.putText(
                        frame,
                        f"Id {id}",
                        (box[0], box[1]),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 255, 255),
                        2,
                    )


        # Показать изображение с обнаруженными объектами
        cv2.imshow("Detected Objects", frame)

        # Выход из цикла при нажатии клавиши 'q'
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Освободить веб-камеру
    cap.release()
    cv2.destroyAllWindows()


def process_webcam_with_detection(model):

    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        raise Exception("Ошибка: Не удалось открыть веб-камеру.")

    previous_box = None
    stationary_threshold = 300  # Порог для определения неподвижности
    stationary_time = 1  # Время в секундах, в течение которого объект должен быть неподвижен
    last_movement_time = time.time()  # Время последнего движения
    min_area = 600  # Минимальная площадь объекта для обработки

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Выполнить обнаружение объектов
        results = model(frame, iou=0.87, conf=0.6, imgsz=1024, verbose=False)

        # Проверка наличия обнаруженных объектов
        if results[0].boxes is not None and len(results[0].boxes) > 0:
            print(f"Обнаружено {len(results[0].boxes)} объектов.")

            # Получение координат и идентификаторов объектов
            boxes = results[0].boxes.xyxy.numpy().astype(int)

            # Проверка наличия идентификаторов
            if results[0].boxes.id is not None:
                ids = results[0].boxes.id.numpy().astype(int)
            else:
                print("Идентификаторы объектов не найдены.")
                ids = [0] * len(boxes)  # Присвоить идентификаторы по умолчанию, если они отсутствуют

            if len(boxes) == 1:  # Проверяем, если обнаружен только один объект
                current_box = boxes[0]
                # Вычисляем площадь текущего объекта
                width = current_box[2] - current_box[0]
                height = current_box[3] - current_box[1]
                area = width * height

                if area > min_area:  # Проверяем, больше ли площадь минимальной
                    if previous_box is not None:
                        # Проверка на неподвижность
                        if (abs(current_box[0] - previous_box[0]) < stationary_threshold and
                            abs(current_box[1] - previous_box[1]) < stationary_threshold and
                            abs(current_box[2] - previous_box[2]) < stationary_threshold and
                            abs(current_box[3] - previous_box[3]) < stationary_threshold):
                            # Если объект неподвижен, проверяем время
                            if time.time() - last_movement_time >= stationary_time:
                                # Вычисляем координаты центра объекта
                                center_x = (current_box[0] + current_box[2]) // 2
                                center_y = (current_box[1] + current_box[3]) // 2
                                return center_x, center_y
                        else:
                            print("Объект движется.")
                            last_movement_time = time.time()  # Обновляем время последнего движения
                    previous_box = current_box  # Обновляем предыдущие координаты
                else:
                    print(f"Объект слишком мал (площадь: {area}), игнорируем.")

            else:
                print("Объекты не обнаружены или их больше одного.")

            for box, id in zip(boxes, ids):
                # Вычисляем площадь текущего объекта
                width = box[2] - box[0]
                height = box[3] - box[1]
                area = width * height

                if area > min_area:  # Проверяем, больше ли площадь минимальной
                    # Сгенерировать случайный цвет для каждого объекта на основе его ID
                    random.seed(int(id))
                    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

                    cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), color, 2)
                    cv2.putText(
                        frame,
                        f"Id {id}",
                        (box[0], box[1]),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 255, 255),
                        2,
                    )


        # Показать изображение с обнаруженными объектами
        cv2.imshow("Detected Objects", frame)

        # Выход из цикла при нажатии клавиши 'q'
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Освободить веб-камеру
    cap.release()
    cv2.destroyAllWindows()


def process_webcam_with_detection_low(model):
    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        raise Exception("Ошибка: Не удалось открыть веб-камеру.")

    previous_box = None
    stationary_threshold = 300  # Порог для определения неподвижности
    stationary_time = 1  # Время в секундах, в течение которого объект должен быть неподвижен
    no_object_time = 0  # Время, в течение которого не обнаружены объекты
    last_movement_time = time.time()  # Время последнего движения
    min_area = 600  # Минимальная площадь объекта для обработки

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Выполнить обнаружение объектов
        results = model(frame, iou=0.87, conf=0.6, imgsz=1024, verbose=False)

        # Проверка наличия обнаруженных объектов
        if results[0].boxes is not None and len(results[0].boxes) > 0:
            print(f"Обнаружено {len(results[0].boxes)} объектов.")
            no_object_time = 0  # Сброс времени, когда объекты обнаружены

            # Получение координат и идентификаторов объектов
            boxes = results[0].boxes.xyxy.numpy().astype(int)

            # Проверка наличия идентификаторов
            if results[0].boxes.id is not None:
                ids = results[0].boxes.id.numpy().astype(int)
            else:
                print("Идентификаторы объектов не найдены.")
                ids = [0] * len(boxes)  # Присвоить идентификаторы по умолчанию, если они отсутствуют

            if len(boxes) == 1:  # Проверяем, если обнаружен только один объект
                current_box = boxes[0]
                # Вычисляем площадь текущего объекта
                width = current_box[2] - current_box[0]
                height = current_box[3] - current_box[1]
                area = width * height

                if area > min_area:  # Проверяем, больше ли площадь минимальной
                    if previous_box is not None:
                        # Проверка на неподвижность
                        if (abs(current_box[0] - previous_box[0]) < stationary_threshold and
                            abs(current_box[1] - previous_box[1]) < stationary_threshold and
                            abs(current_box[2] - previous_box[2]) < stationary_threshold and
                            abs(current_box[3] - previous_box[3]) < stationary_threshold):
                            # Если объект неподвижен, проверяем время
                            if time.time() - last_movement_time >= stationary_time:
                                # Вычисляем координаты центра объекта
                                center_x = (current_box[0] + current_box[2]) // 2
                                center_y = (current_box[1] + current_box[3]) // 2
                                return center_x, center_y
                        else:
                            print("Объект движется.")
                            last_movement_time = time.time()  # Обновляем время последнего движения
                    previous_box = current_box  # Обновляем предыдущие координаты
                else:
                    print(f"Объект слишком мал (площадь: {area}), игнорируем.")

            else:
                print("Объекты не обнаружены или их больше одного.")

            for box, id in zip(boxes, ids):
                # Вычисляем площадь текущего объекта
                width = box[2] - box[0]
                height = box[3] - box[1]
                area = width * height

                if area > min_area:  # Проверяем, больше ли площадь минимальной
                    # Сгенерировать случайный цвет для каждого объекта на основе его ID
                    random.seed(int(id))
                    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

                    cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), color, 2)
                    cv2.putText(
                        frame,
                        f"Id {id}",
                        (box[0], box[1]),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 255, 255),
                        2,
                    )

        else:
            no_object_time += 1  # Увеличиваем время, когда объекты не обнаружены
            if no_object_time >= 5 * 30:  # Проверяем, прошло ли 5 секунд (30 FPS)
                print("Объекты не обнаружены более 5 секунд.")
                return None  # Возвращаем None, если объекты не обнаружены более 5 секунд

        # Показать изображение с обнаруженными объектами
        cv2.imshow("Detected Objects", frame)

        # Выход из цикла при нажатии клавиши 'q'
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Освободить веб-камеру
    cap.release()
    cv2.destroyAllWindows()