import asyncio

from loguru import logger

from utils.tg_cli import get_telephone_client
from utils.utils import parse_arg, find


async def main():
    logger.debug('Файл запущен')
    file_path, res_path = parse_arg()
    logger.debug('Аргументы считаны')

    logger.debug('Запуск тг клиента')    

    logger.debug('соединение с тг прошло успешно')

    client = get_telephone_client()
    await client.connect()
    if await client.is_user_authorized():
        logger.debug('Соединение с клиентом установлено')
    else:
        await client.start()
        logger.debug('Авторизация прошла успешно')
        logger.warning('Сессия на других устройствах может быть завершена')

    logger.debug('Начало обработки')
    await find(client, file_path, res_path)
    logger.debug('Выполнение завершено')

if __name__ == '__main__':
    asyncio.run(main())


