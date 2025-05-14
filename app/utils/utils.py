import re

from argparse import ArgumentParser
import pandas as pd
from loguru import logger
from telethon import TelegramClient

from utils.tg_utils import get_inf_from_bot


def parse_arg() -> tuple[str, str]:
    parser = ArgumentParser()
    parser.add_argument('-p', type=str, required=True, help='Путь к исходному файлу')
    parser.add_argument('-r', type=str, required=True, help='Путь для сохранения')

    args = parser.parse_args()

    file_path = args.p
    res_path = args.r

    return file_path, res_path


async def find(client: TelegramClient, file_path: str, res_path: str) -> None:
    try:
        df = pd.read_csv(file_path)
        logger.debug('Файл преобразован в df')
    except Exception as e:
        logger.error('Не удалось преобразовать файл. Проверьте расширение')
        
        raise e

    try: 
        numbers = df['Телефон'].tolist()
        logger.debug('Колонка с номером найдена')
    except Exception as e:
        logger.error('Колонка "Телефон" отсутствует')

        raise e

    names, mails, tg = await get_inf_from_bot(client, numbers)
    comment = []

    for name, mail, tg_link in zip(names, mails, tg):
        comm = f'Возможные имена: {name}\nВозможная почта: {mail}\nТг: {tg_link}'
        comment.append(comm)

    df['Комментарий'] = comment

    df.to_csv(res_path, index=False)
    logger.debug('Файл сохранен')

    return None



