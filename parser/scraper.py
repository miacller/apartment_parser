#parser/scraper.py
from bs4 import BeautifulSoup
import requests
from .db import sql_connection
from .utils import rooms_counter, random_sleep, PAGE_DELAY, APARTMENT_DELAY, ERROR_DELAY

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_tree(href):
    response = requests.get(href, headers=headers)
    tree = BeautifulSoup(response.text, 'html.parser')
    return tree

def get_apartments(href):
    tree = get_tree(href)
    links = [a['href'] for a in tree.find_all('a', class_= "_93444fe79c--link--VtWj6", href=True)]
    return links

def apartment_parameters(href):
    tree = get_tree(href)
    meta_tag = tree.find('meta', {'name': 'description'})
    desc = meta_tag['content']
    price = desc.split('Цена продажи -')[1].split(' руб.')[0].strip() + 'Руб'
    area = desc.split('площадью')[1].split('м²')[0].strip() + 'м²'
    addres = desc.split('м²')[1].split(',')[0].strip() + " " + desc.split('м²')[1].split(',')[1].strip()
    rooms = rooms_counter[desc.split('комнатную')[0].split('Купите ')[1].strip()]
    house_type = tree.find('div', {'data-testid': 'OfferSummaryInfoItem'}).find_all('p')[1].get_text(strip=True)
    decoration = tree.find('span', string='Тип дома').find_next('span').get_text(strip=True) if tree.find('span', string='Тип дома') else 'Продавец не предоставил информацию об отделке'
    number_of_lifts = tree.find('p', string='Количество лифтов').find_next('p').get_text(strip=True) if tree.find('p', string='Количество лифтов') else 'В доме нет лифта'
    floor = tree.find('span', string='Этаж').find_next('span').get_text(strip=True).split()[0]
    number_of_floors = tree.find('span', string='Этаж').find_next('span').get_text(strip=True).split()[-1]
    deal_id = href.split('/')[-2]
    
    apartment_info = {
        'deal_id': deal_id,
        'price': price, 
        'area': area, 
        'addres': addres,  
        'rooms': rooms, 
        'house_type': house_type, 
        'decoration': decoration, 
        'number_of_lifts': number_of_lifts, 
        'floor': floor, 
        'number_of_floors': number_of_floors
    }
    
    connection = sql_connection()
    with connection.cursor() as cursor:
        check_query = "SELECT 1 FROM apartments WHERE deal_id = %(deal_id)s"
        cursor.execute(check_query, {'deal_id': deal_id})
        exists = cursor.fetchone()    
        
        if not exists:
            insert_query = """
            INSERT INTO apartments 
            (deal_id, price, area, addres, rooms, house_type, decoration, number_of_lifts, floor, number_of_floors)
            VALUES 
            (%(deal_id)s, %(price)s, %(area)s, %(addres)s, %(rooms)s, %(house_type)s, %(decoration)s, %(number_of_lifts)s, %(floor)s, %(number_of_floors)s)
            """
            cursor.execute(insert_query, apartment_info)
            connection.commit()
            print(f"Добавлена новая запись: {deal_id}")
        else:
            print(f"Запись с deal_id {deal_id} уже существует, пропускаем")
    
    return deal_id