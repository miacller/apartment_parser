#parser/utils.py
from dotenv import load_dotenv
import os

load_dotenv()

rooms_counter = {'одно' : 1, 'двух': 2, 'трех' : 3, 'четырех': 4, 'пяти': 5, 'шести': 6,}

PAGE_DELAY = (3, 7)  
APARTMENT_DELAY = (1, 3)  
ERROR_DELAY = 10 

BASE_URL = os.getenv("BASE_URL")