import requests
import json
import csv
import time

def get_content(url: str, flag: str = ''):
    """Возвращает содержимое ответа сервера

    Args:
        url (str): url-адрес
        flag (str): флаг, определяющий возвращаемое значение. Ожидается либо '', либо 'json'
    Returns:
        str or dict: ответ сервера
    """

    response = requests.get(url) # get запрос на сервер

    # если передали флаг json, то ожидаем, что хотим получить информацию о текущем имени файла базы данных
    if flag == 'json':
        return response.json()

    # иначе возвращаем текст ответа
    return response.text

def get_market_items_db(current_db_file_name: str):
    """Возвращает базу данных всех вещей на продаже в фиксированный момент времени

    Args:
        current_db_file_name (str): имя файла базы данных, формат csv

    Returns:
        market_items_db (str): CSV-файл с данными в формате строки
    """
    db_file_url = f'https://market.csgo.com/itemdb/{current_db_file_name}' # url-адрес файла базы данных
    market_items_db = get_content(db_file_url) # получаем базу данных вещей
    return market_items_db 

def get_current_db_file_name():
    """Возвращает текущее имя файла базы данных

    Returns:
        current_db_file_name (str): имя файла базы данных, формат csv
    """
    url = 'https://market.csgo.com/itemdb/current_730.json' # адрес имени файла базы данных
    current_db_file_name = get_content(url, flag='json')['db'] # получение имени БД
    return current_db_file_name

def write_market_items_to_file(market_items_db: str):
    """Сохраняет базу данных вещей на продаже в фиксированный момент времени в csv-файл

    Args:
        market_items_db (str): CSV-файл с данными в формате строки
    """

    with open('market_items_db.csv', 'w', encoding='utf-8') as file:
        file.write(market_items_db)

def update_market_items():
    """Обновляет базу данных всех вещей на продаже в фиксированный момент времени

    Информация о предметах на главной странице сайте строится из предложений продавцов, 
    находящихся в данный момент онлайн на сайте. Она хранится в специальной базе данных и обновляется раз в минуту.
    Таким образом, сканировать главную или выполнять поиск по предметам чаще, чем раз в минуту, 
    не имеет смысла и создаёт избыточную нагрузку на наш сервер. (c) CSGO Market
    """
    current_db_file_name = get_current_db_file_name() # имя файла базы данных
    market_items_db = get_market_items_db(current_db_file_name) # сама база данных вещей
    write_market_items_to_file(market_items_db) # сохранение
    # write_market_items_to_file(get_market_items_db(get_current_db_file_name()))

def main():
    update_market_items()

if __name__ == '__main__':
    main()