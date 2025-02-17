import cv2
import random
import time
cap = cv2.VideoCapture(1)

def process_webcam_with_detection_low(model):
    mus = -1
    out = 0

    if not cap.isOpened():
        raise Exception("Ошибка: Не удалось открыть веб-камеру.")

    previous_box = None
    stationary_threshold = 300  # Порог для определения неподвижности
    stationary_time = 4  # Время в секундах, в течение которого объект должен быть неподвижен
    no_object_time = 0  # Время, в течение которого не обнаружены объекты
    last_movement_time = time.time()  # Время последнего движения
    min_area = 900
    max_area = 1800# Минимальная площадь объекта для обработки

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Выполнить обнаружение объектов
        results = model(frame, iou=0.8, conf=0.6, imgsz=640, verbose=False)

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

            # Фильтруем объекты по площади
            filtered_boxes = []
            filtered_ids = []

            for box, id in zip(boxes, ids):
                width = box[2] - box[0]
                height = box[3] - box[1]
                area = width * height

                if min_area < area < max_area:
                    filtered_boxes.append(box)
                    filtered_ids.append(id)

            # Проверяем количество оставшихся объектов после фильтрации
            if len(filtered_boxes) > 0:
                current_box = filtered_boxes[0]
                width = current_box[2] - current_box[0]
                height = current_box[3] - current_box[1]
                area = width * height
                print(area)

                # Логика для обработки одного объекта
                if len(filtered_boxes) == 1:
                    if previous_box is not None:
                        no_object_time = 0
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
                                height, width, channels = frame.shape
                                out = center_x, center_y, height, width
                                if mus == -1:
                                    mus = 1

                        else:
                            print("Объект движется.")
                            mus = -1
                            out = 0
                            last_movement_time = time.time()  # Обновляем время последнего движения
                else:
                    out = 0
                    last_movement_time = time.time()
                    time.sleep(1)
                    mus = -1
                    print("Объекты не обнаружены или их больше одного.")

                previous_box = current_box  # Обновляем предыдущие координаты
            else:
                print("Все объекты слишком малы или слишком велики, игнорируем.")

            # Отображение оставшихся объектов
            for box, id in zip(filtered_boxes, filtered_ids):
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

        if out != 0:
            no_object_time += 1  # Увеличиваем время, когда объекты не обнаружены
            print("qweqwwqwe")
            if mus == 1:
                import winsound
                frequency = 2500  # Set Frequency To 2500 Hertz
                duration = 500  # Set Duration To 1000 ms == 1 second
                winsound.Beep(frequency, duration)
                mus = 0
            if no_object_time >= 1.5 * 10:
                mus = -1 # Проверяем, прошло ли 5 секунд (30 FPS)
                print("Объекты не обнаружены более 5 секунд.")
                return out
        # Показать изображение с обнаруженными объектами
        cv2.imshow("Detected Objects", frame)

        # Выход из цикла при нажатии клавиши 'q'
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

def Chek(model):
    out = 0
    if not cap.isOpened():
        raise Exception("Ошибка: Не удалось открыть веб-камеру.")

    previous_box = None
    stationary_threshold = 300  # Порог для определения неподвижности
    stationary_time =  1 # Время в секундах, в течение которого объект должен быть неподвижен
    no_object_time = 0  # Время, в течение которого не обнаружены объекты
    last_movement_time = time.time()  # Время последнего движения
    min_area = 900
    max_area = 1800 # Минимальная площадь объекта для обработки

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Выполнить обнаружение объектов
        results = model(frame, iou=0.8, conf=0.3, imgsz=200, verbose=False)
        # Проверка наличия обнаруженных объектов
        if results[0].boxes is not None and len(results[0].boxes) > 0:
            print(f"Обнаружено {len(results[0].boxes)} объектов.")
              # Сброс времени, когда объекты обнаружены

            # Получение координат и идентификаторов объектов
            boxes = results[0].boxes.xyxy.numpy().astype(int)

            # Проверка наличия идентификаторов
            if results[0].boxes.id is not None:
                ids = results[0].boxes.id.numpy().astype(int)
            else:
                print("Идентификаторы объектов не найдены.")
                ids = [0] * len(boxes)  # Присвоить идентификаторы по умолчанию, если они отсутствуют


            current_box = boxes[0]
            # Вычисляем площадь текущего объекта
            width = current_box[2] - current_box[0]
            height = current_box[3] - current_box[1]
            area = width * height

            if area > min_area and area < max_area:  # Проверяем, больше ли площадь минимальной
                 return 1

            else:
                print(f"Объект слишком мал (площадь: {area}), игнорируем.")



            for box, id in zip(boxes, ids):
                # Вычисляем площадь текущего объекта
                width = box[2] - box[0]
                height = box[3] - box[1]
                area = width * height

                if area > min_area and area < max_area:  # Проверяем, больше ли площадь минимальной
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
            if out != 0:
                no_object_time += 1  # Увеличиваем время, когда объекты не обнаружены
                print("qweqwwqwe")
                if no_object_time >=  1 * 10:  # Проверяем, прошло ли 5 секунд (30 FPS)
                    print("Объекты не обнаружены более 5 секунд.")
                    # Возвращаем None, если объекты не обнаружены более 5 секунд

        # Показать изображение с обнаруженными объектами
        cv2.imshow("Detected Objects", frame)

        # Выход из цикла при нажатии клавиши 'q'
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        return 0