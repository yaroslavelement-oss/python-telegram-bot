import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

from bot.config import Settings
from bot.handlers import error_handler, set_bot_commands

logger = logging.getLogger(__name__)


def keyboard_main():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📚 Получить шпоры", url="https://t.me/shrimpege")],
        [InlineKeyboardButton("Я подписался", callback_data="check")]
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Добрый день, это shrimpEGE 👋\n\n"
        "Чтобы получить шпоры на 80+ баллов, подпишитесь на канал 👇",
        reply_markup=keyboard_main()
    )


async def check_sub(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    settings = context.application.bot_data["settings"]
    channel = settings.channel
    your_tg = settings.your_tg

    user_id = query.from_user.id

    try:
        member = await context.bot.get_chat_member(channel, user_id)
        is_sub = member.status in ["member", "administrator", "creator"]
    except:
        is_sub = False

    if not is_sub:
        await query.edit_message_text(
            "ой похоже кто-то не подписался 😏",
            reply_markup=keyboard_main()
        )
    else:
        await query.edit_message_text(
            "Хорош 😎\nНапиши мне, и я дам тебе шпоры",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Написать мне", url=your_tg)]
            ])
        )


def build_application(settings: Settings) -> Application:
    app = Application.builder().token(settings.bot_token).build()

    app.bot_data["settings"] = settings

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_sub, pattern="check"))
    app.add_error_handler(error_handler)

    return app


def main():
    settings = Settings.from_env()

    logging.basicConfig(
        format="%(asctime)s %(name)s [%(levelname)s] %(message)s",
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
    )

    app = build_application(settings)

    logger.info("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
