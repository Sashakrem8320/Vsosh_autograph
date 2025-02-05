from flask import Flask, request, send_from_directory
import os

app = Flask(__name__)

SAVE_PATH = 'gcode_files'
if not os.path.exists(SAVE_PATH):
    os.makedirs(SAVE_PATH)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/save-gcode', methods=['POST'])
def save_gcode():
    gcode = request.data.decode('utf-8')  # Получаем G-code из запроса
    file_path = os.path.join(SAVE_PATH, 'drawing.gcode')

    with open(file_path, 'w') as file:
        file.write(gcode)  # Сохраняем G-code в файл

    return 'G-code успешно сохранен', 200
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)