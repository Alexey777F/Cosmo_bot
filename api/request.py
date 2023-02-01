import requests
import json
from googletrans import Translator
from typing import Dict, Any, List
import logging
from json import JSONDecodeError


def information() -> str:
    """Функция которая возвращает информацию о марсианском ровере"""
    text = "Марсоход третьего поколения, разработанный для исследования кратера Гейла на Марсе в рамках миссии НАСА" \
           " 'Марсианская научная лаборатория' (Mars Science Laboratory, сокр. MSL).\n\nМарсоход представляет собой " \
           "автономную химическую лабораторию. В ходе прошлых миссий учёные уже установили, что вода присутствовала " \
           "на Марсе и, по сути, присутствует сейчас в виде льда. Но одной воды недостаточно для поддержания жизни. " \
           "\n\nДля обнаружения ключевых факторов, доказывающих пригодность Марса для жизни, в конструкции Curiosity " \
           "имеются инструменты для бурения поверхности планеты и спектрометры, такие как Sample Analysis at Mars (SAM) " \
           "и Chemistry and Mineralogy (CheMin), используемые для анализа полученных при бурении образцов.\n\nЗа десять лет " \
           "исследований Curiosity обнаружил гораздо больше, чем просто необходимые для существования жизни элементы. " \
           "В конструкции марсохода имеются детекторы радиации, датчики для изучения окружающей среды и атмосферы, " \
           "которые хорошо показали себя на Марсе.\n\nНапример, во время странствий, когда Curiosity приближался к " \
           "геологическим образованиям, таким как скалы и холмы, инструменты марсохода определяли, что скалы блокируют " \
           "радиационное излучение.\n\nВ дальнейшем учёные рассчитывают на то, что Curiosity поможет понять, что произошло " \
           "с климатом Марса, который когда-то был пригоден для жизни, а также как долго планета сохраняла эти свойства."
    return text


def get_response(url) -> Any:
    """Функция которая возвращает ответ от api.nasa.gov"""
    logger = logging.getLogger(__name__)
    try:
        response = requests.get(url, timeout=10)
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


def get_galaxy_data(get_json) -> Dict:
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
    except KeyError as exc:
        logger.error(exc, exc_info=exc)


def get_mars_data(get_json) -> List:
    """Функция которая возвращает фотографии с марсохода"""
    logger = logging.getLogger(__name__)
    try:
        return get_json["photos"][0]["img_src"]
    except KeyError as exc:
        logger.error(exc, exc_info=exc)
