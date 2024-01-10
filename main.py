from flask import (
    Flask,
    request
)
import pandas as pd
import os

app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def index():
    agent = request.user_agent
    ipadr = request.remote_addr
    agent = str(agent)

    save_to_csv(ipadr, agent)

    return f'ip: {ipadr}\nuser-agent: {agent}'


def save_to_csv(ip, user_agent, file_path='your_file.csv'):
    # Пытаемся загрузить существующий файл в DataFrame
    try:
        df = pd.read_csv(file_path)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        # Если файл не существует или пуст, создаем новый DataFrame
        df = pd.DataFrame(columns=['ip', 'user-agent'])

    # Создаем новую строку данных и добавляем в DataFrame
    new_row = pd.DataFrame({'ip': [ip], 'user-agent': [user_agent]})
    df = pd.concat([df, new_row], ignore_index=True)

    # Сохраняем DataFrame обратно в файл CSV
    df.to_csv(file_path, index=False)
    print("ok")
    return 0


if __name__ == '__main__':
    app.run(port=7070, debug=True, host="0.0.0.0")
