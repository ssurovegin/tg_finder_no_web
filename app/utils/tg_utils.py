import os
import re

from telethon import TelegramClient
from loguru import logger
from natasha import Segmenter, NewsEmbedding, NewsNERTagger, Doc

async def get_inf_from_bot(client: TelegramClient, numbers: list[str] | list[int]) -> tuple[list[str], list[str], list[str]]:
    names, mails, tg = [], [], []
    
    try:
        async with client.conversation(os.getenv('BOT_UNAME'), max_messages=200, timeout=5) as conv:
            logger.debug('Диалог с ботом открыт')

            for num in numbers:
                logger.debug('Отправка сообщения')

                await conv.send_message(str(num))
                logger.debug('Сообщение успешно отправлено')

                bot = await client.get_entity(str(os.getenv('BOT_UNAME')))
                logger.debug('Бот найден')

                msg_history = []

                async for msg in client.iter_messages(bot, limit=6):
                    msg_history.append(msg.text)
                logger.debug('История сообщение получена')

                found = False

                for msg in msg_history:
                    first_w = msg.split(' ')[0]

                    if first_w == '📱':
                        found = True

                        n, m = extract_names_mail(msg)
                        if len(n) > 0:
                            names.append(n)
                        else: 
                            names.append('Не найдено')
                        
                        if len(m) > 0:
                            mails.append(m)
                        else:
                            mails.append('Не найдено')
                        
                        logger.debug('Ответ для добавления получен')

                        break
                
                if not found:
                    names.append('Не найдено')
                    mails.append('Не найдено')

                tg.append(make_url(num))

    except Exception as e:
        logger.error('Не удалось открыть диалог с ботом')
        raise e
    
    return names, mails, tg


def extract_names_mail(text: str) -> tuple[list[str], list[str]]:
    segm = Segmenter()
    emb = NewsEmbedding()
    ner_tag = NewsNERTagger(emb)
    doc = Doc(text)

    doc.segment(segm)
    doc.tag_ner(ner_tag)

    names = list(dict.fromkeys(
        [span.text for span in doc.spans if span.type == 'PER']
    ))

    mails = list(dict.fromkeys(
        re.findall(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', text)
    ))

    return names, mails


def make_url(number: str) -> str:
    return f'https://t.me/+{number}'
