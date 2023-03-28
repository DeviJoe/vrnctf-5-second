#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position

import logging
import random
import re

import os

from telegram import __version__ as TG_VER, ReplyKeyboardMarkup

import defines

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    PicklePersistence,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

YEAR_TYPING = 0

IMAGES = {}


def parse_im_folder():
    for file in os.listdir('images'):
        year = re.search(r'\d+', file).group()
        IMAGES[f'images/{file}'] = year


def get_random_image_without_repeat(used_images):
    if used_images:
        result_list = [i for i in IMAGES.keys() if i not in used_images]
    else:
        result_list = list(IMAGES.keys())

    return random.choice(result_list)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_text = "Вы вошли в SCP-052, для возврата в настоящее время требуется калибровка маяка. Введите год."

    context.user_data["solved"] = 0
    if 'images' not in context.user_data:
        context.user_data["images"] = []

    if len(context.user_data["images"]) == len(IMAGES):
        context.user_data["images"] = []
    image = get_random_image_without_repeat(context.user_data["images"])
    context.user_data["current"] = IMAGES[image]
    context.user_data["images"].append(image)

    await update.message.reply_text(reply_text)
    await update.message.reply_photo(image)

    return YEAR_TYPING


async def year_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    year = update.message.text.lower()

    if year == context.user_data["current"]:
        context.user_data["solved"] += 1

        if context.user_data["solved"] == defines.NEED_TO_SOLVE:
            reply_text = defines.FLAG
            await update.message.reply_text(reply_text)

            return ConversationHandler.END
        else:
            reply_text = "Продолжение калибровки, переход на следующую остановку"
            await update.message.reply_text(reply_text)

            if len(context.user_data['images']) == len(IMAGES):
                context.user_data["images"] = []
            image = get_random_image_without_repeat(context.user_data["images"])
            context.user_data["current"] = IMAGES[image]
            context.user_data["images"].append(image)

            await update.message.reply_photo(image)

            return YEAR_TYPING
    else:
        reply_text = "Данные неверны. Агент потерян во времени."
        reply_keyboard = [["/start"]]
        await update.message.reply_text(reply_text,
                                        reply_markup=ReplyKeyboardMarkup(
                                            reply_keyboard, one_time_keyboard=True
                                        )
                                        )

        return ConversationHandler.END


async def incorrect_data_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_text = 'Неправильный формат данных'

    await update.message.reply_text(reply_text)

    return YEAR_TYPING


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        f"Вас сожрали"
    )
    return ConversationHandler.END


def main() -> None:
    persistence = PicklePersistence(filepath=os.environ['PERSISTENCE_FILEPATH'])
    application = Application.builder().token(os.environ['BOT_TOKEN']).persistence(persistence).build()

    parse_im_folder()

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            YEAR_TYPING: [
                MessageHandler(
                    filters.Regex("^\d+$"), year_handler
                ),
                MessageHandler(filters.TEXT, incorrect_data_handler),
            ]
            # TYPING_CHOICE: [
            #     MessageHandler(
            #         filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")), regular_choice
            #     )
            # ]
        },
        fallbacks=[MessageHandler(filters.Regex("^Done$"), done)],
        name="ctf_conv",
        persistent=True,
    )

    application.add_handler(conv_handler)

    application.run_polling()


if __name__ == "__main__":
    main()
