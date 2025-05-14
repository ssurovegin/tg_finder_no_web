import asyncio

from loguru import logger

from utils.tg_cli import start_client, get_telephone_client
from utils.utils import parse_arg, find


async def main():
    logger.debug('Файл запущен')
    file_path, res_path = parse_arg()
    logger.debug('Аргументы считаны')

    logger.debug('Запуск тг клиента')
    try:
        await start_client()

    except Exception as e:
        logger.error('Нет соединения с клиентом тг')
        
        raise e
    logger.debug('соединение с тг прошло успешно')

    client = get_telephone_client()

    logger.debug('Начало обработки')
    await find(client, file_path, res_path)
    logger.debug('Выполнение завершено')

if __name__ == '__main__':
    asyncio.run(main())


