import requests
import json
from googletrans import Translator
from typing import Dict, Any
import logging
from json import JSONDecodeError


def get_response(key, date) -> Any:
    """Функция которая возвращает ответ от api.nasa.gov"""
    logger = logging.getLogger(__name__)
    try:
        response = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={key}&start_date={date}&end_date={date}",
                                timeout=10)
        if response.status_code == requests.codes.ok:
            return response
        else:
            return None
    except requests.exceptions.RequestException as exc:
        logger.error(exc, exc_info=exc)


def get_json(get_response) -> Dict:
    """Функция которая возвращает словарь с данными парсинга"""
    logger = logging.getLogger(__name__)
    try:
        data = json.loads(get_response.text)
        return data
    except(LookupError, JSONDecodeError, TypeError) as exc:
        logger.error(exc, exc_info=exc)


def get_data(get_json) -> Dict:
    """Функция которая возвращает название, описание и фото"""
    logger = logging.getLogger(__name__)
    data_dict = dict()
    trl = Translator()
    title = trl.translate(get_json[0]['title'], src='en', dest='ru')
    explanation = trl.translate(get_json[0]['explanation'], src='en', dest='ru')
    data_dict['Галактика'] = title.text
    data_dict['Описание'] = explanation.text
    if get_json[0]['url'].startswith("//"):
        get_json[0]['url'] = get_json[0]['url'][2:]
    data_dict['Ссылка'] = get_json[0]['url']
    try:
        return data_dict
    except(BaseException) as exc:
        logger.error(exc, exc_info=exc)