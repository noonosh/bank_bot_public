from telegram import *
from telegram.ext import *
from configs import *
from texts import *
import logging
import sqlite3
from buttons import *
import datetime
from token import API_TOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

conn = sqlite3.connect(database_path, check_same_thread=False)
cursor = conn.cursor()


def start(update, context):
    chat_id = update.message.chat_id
    user_update = update.message.from_user
    username = f'@{user_update.username}'
    user = f'{user_update.first_name} {user_update.last_name}'
    now = datetime.datetime.utcnow().replace(microsecond=0) + datetime.timedelta(hours=5)
    context.user_data.clear()
    buttons = [
        [
            InlineKeyboardButton("🇺🇿 Ўзбек тили", callback_data='uz'),
            InlineKeyboardButton("🇷🇺 Русский", callback_data='ru')
        ]
    ]
    update.message.reply_text(start_text,
                              reply_markup=InlineKeyboardMarkup(buttons))
    cursor.execute("""INSERT INTO Users (id, date_and_time, telegram_id, name, username) VALUES (
    NOT NULL, '{}', '{}', '{}', '{}'
    )
    """.format(now, chat_id, user, username))
    conn.commit()
    db_id = cursor.execute("""SELECT id FROM Users WHERE telegram_id = '{}' and date_and_time = '{}'
    """.format(chat_id, now)).fetchone()[0]
    context.user_data.update({
        'id': db_id
    })
    logger.info('%s - %s started the bot', chat_id, username)
    selected.clear()
    service_items.clear()
    return LANGUAGE


def my_id(context):
    my = context.user_data['id']
    return my


def language(context):
    lan = context.user_data['user']['lang']
    return lan


def greeting(update, context):
    query = update.callback_query.message
    data = update.callback_query.data
    telegram_id = query.chat.id
    update.callback_query.edit_message_text(greeting_txt[data])
    payload = {
        'user': {
            'chat_id': telegram_id,
            'first_name': query.chat.first_name,
            'last_name': query.chat.last_name,
            'username': query.chat.username,
            'lang': data
        }
    }
    context.user_data.update(payload)
    cursor.execute("UPDATE Users SET language = '{}' WHERE id = '{}'".format(data, my_id(context)))
    conn.commit()
    button = [
        [START_SURVEY[str(language(context))]]
    ]
    context.bot.send_message(chat_id=telegram_id,
                             text=start_survey_txt[language(context)],
                             reply_markup=ReplyKeyboardMarkup(button, resize_keyboard=True),
                             parse_mode='HTML')
    return IDENTITY


def identity(update, context):
    telegram_id = update.message.chat_id
    buttons = [
        [NATURAL_PERSON[language(context)]],
        [ENTITY[language(context)]],
        [INDIVIDUAL_ENTPRNR[language(context)]]
    ]
    update.message.reply_html(identity_txt[language(context)],
                              reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True))
    return REGION


def region(update, context):
    chat_id = update.message.chat_id
    data = update.message.text
    context.user_data.update({
        'identity': data
    })
    buttons = [
        [ANDIJAN[language(context)], BUKHARA[language(context)]],
        [DJIZAK[language(context)], KASHKADARYA[language(context)]],
        [KARAKALPAKSTAN[language(context)], NAVOI[language(context)]],
        [NAMANGAN[language(context)], SAMARKAND[language(context)]],
        [SIRDARYA[language(context)], SURKHANDARYA[language(context)]],
        [TASHKENT_REGION[language(context)], TASHKENT[language(context)]],
        [FERGANA[language(context)], KHOREZM[language(context)]]
    ]
    cursor.execute("UPDATE Users SET identity = '{}' WHERE id = '{}'".format(data, my_id(context)))
    conn.commit()
    context.bot.send_message(chat_id=chat_id,
                             text=region_txt[language(context)],
                             reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                             parse_mode='HTML')
    return CHOOSE_REGION_STATE


def andijan_region(update, context):
    chat_id = update.message.chat_id
    data = update.message.text
    context.user_data.update({
        'region': data
    })
    cursor.execute("UPDATE Users SET region = '{}' WHERE id = '{}'".format(data, my_id(context)))
    conn.commit()
    buttons = [
        [AGROBANK[language(context)], ALOQABANK[language(context)]],
        [ASAKABANK[language(context)], INFINBANK[language(context)]],
        [IPAKYULIBANK[language(context)], IPOTEKABANK[language(context)]],
        [QQB[language(context)], MIKROKREDITBANK[language(context)]],
        [OFB[language(context)], SAVDOGARBANK[language(context)]],
        [TRASTBANK[language(context)], TURONBANK[language(context)]],
        [UZMILLIYBANK[language(context)], UZSANOATQURILISHBANK[language(context)]],
        [XALQBANKI[language(context)], HAMKORBANK[language(context)]]
    ]
    context.bot.send_message(chat_id=chat_id,
                             text=bank_txt[language(context)],
                             reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                             parse_mode='HTML')
    return REASON


def bukhara_region(update, context):
    chat_id = update.message.chat_id
    data = update.message.text
    context.user_data.update({
        'region': data
    })
    cursor.execute("UPDATE Users SET region = '{}' WHERE id = '{}'".format(data, my_id(context)))
    conn.commit()
    buttons = [
        [AGROBANK[language(context)], ASIA_ALLIANCE_BANK[language(context)]],
        [ALOQABANK[language(context)], ASAKABANK[language(context)]],
        [INFINBANK[language(context)], IPOTEKABANK[language(context)]],
        [KAPITALBANK[language(context)], QQB[language(context)]],
        [MIKROKREDITBANK[language(context)], OFB[language(context)]],
        [SAVDOGARBANK[language(context)], TRASTBANK[language(context)]],
        [TURONBANK[language(context)], UZMILLIYBANK[language(context)]],
        [UZSANOATQURILISHBANK[language(context)], XALQBANKI[language(context)]],
        [HAMKORBANK[language(context)]]
    ]
    context.bot.send_message(chat_id=chat_id,
                             text=bank_txt[language(context)],
                             reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                             parse_mode='HTML')
    return REASON


def djizak_region(update, context):
    chat_id = update.message.chat_id
    data = update.message.text
    context.user_data.update({
        'region': data
    })
    cursor.execute("UPDATE Users SET region = '{}' WHERE id = '{}'".format(data, my_id(context)))
    conn.commit()
    buttons = [
        [AGROBANK[language(context)], ALOQABANK[language(context)]],
        [ASAKABANK[language(context)], IPOTEKABANK[language(context)]],
        [QQB[language(context)], MIKROKREDITBANK[language(context)]],
        [SAVDOGARBANK[language(context)], TRASTBANK[language(context)]],
        [TURONBANK[language(context)], UZMILLIYBANK[language(context)]],
        [UZSANOATQURILISHBANK[language(context)], XALQBANKI[language(context)]],
        [HAMKORBANK[language(context)]]
    ]
    context.bot.send_message(chat_id=chat_id,
                             text=bank_txt[language(context)],
                             reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                             parse_mode='HTML')
    return REASON


def kashkadarya_region(update, context):
    chat_id = update.message.chat_id
    data = update.message.text
    context.user_data.update({
        'region': data
    })
    cursor.execute("UPDATE Users SET region = '{}' WHERE id = '{}'".format(data, my_id(context)))
    conn.commit()
    buttons = [
        [AGROBANK[language(context)], ASIA_ALLIANCE_BANK[language(context)]],
        [ALOQABANK[language(context)], ASAKABANK[language(context)]],
        [INFINBANK[language(context)], IPAKYULIBANK[language(context)]],
        [IPOTEKABANK[language(context)], QQB[language(context)]],
        [MIKROKREDITBANK[language(context)], SAVDOGARBANK[language(context)]],
        [TRASTBANK[language(context)], TURONBANK[language(context)]],
        [UZMILLIYBANK[language(context)], UZSANOATQURILISHBANK[language(context)]],
        [UNIVERSALBANK[language(context)], XALQBANKI[language(context)]],
        [HAMKORBANK[language(context)]]
    ]
    context.bot.send_message(chat_id=chat_id,
                             text=bank_txt[language(context)],
                             reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                             parse_mode='HTML')
    return REASON


def karakalpakstan_region(update, context):
    chat_id = update.message.chat_id
    data = update.message.text
    context.user_data.update({
        'region': data
    })
    cursor.execute("UPDATE Users SET region = '{}' WHERE id = '{}'".format(data, my_id(context)))
    conn.commit()
    buttons = [
        [AGROBANK[language(context)], ALOQABANK[language(context)]],
        [ASAKABANK[language(context)], INFINBANK[language(context)]],
        [IPOTEKABANK[language(context)], KAPITALBANK[language(context)]],
        [QQB[language(context)], MIKROKREDITBANK[language(context)]],
        [SAVDOGARBANK[language(context)], TURONBANK[language(context)]],
        [UZMILLIYBANK[language(context)], UZSANOATQURILISHBANK[language(context)]],
        [XALQBANKI[language(context)], HAMKORBANK[language(context)]]
    ]
    context.bot.send_message(chat_id=chat_id,
                             text=bank_txt[language(context)],
                             reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                             parse_mode='HTML')
    return REASON


def navoi_region(update, context):
    chat_id = update.message.chat_id
    data = update.message.text
    context.user_data.update({
        'region': data
    })
    cursor.execute("UPDATE Users SET region = '{}' WHERE id = '{}'".format(data, my_id(context)))
    conn.commit()
    buttons = [
        [AGROBANK[language(context)], ALOQABANK[language(context)]],
        [ASAKABANK[language(context)], INFINBANK[language(context)]],
        [IPAKYULIBANK[language(context)], IPOTEKABANK[language(context)]],
        [QQB[language(context)], MIKROKREDITBANK[language(context)]],
        [SAVDOGARBANK[language(context)], TURONBANK[language(context)]],
        [UZMILLIYBANK[language(context)], UZSANOATQURILISHBANK[language(context)]],
        [XALQBANKI[language(context)], HAMKORBANK[language(context)]]
    ]
    context.bot.send_message(chat_id=chat_id,
                             text=bank_txt[language(context)],
                             reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                             parse_mode='HTML')
    return REASON


def namangan_region(update, context):
    chat_id = update.message.chat_id
    data = update.message.text
    context.user_data.update({
        'region': data
    })
    cursor.execute("UPDATE Users SET region = '{}' WHERE id = '{}'".format(data, my_id(context)))
    conn.commit()
    buttons = [
        [AGROBANK[language(context)], ALOQABANK[language(context)]],
        [ASAKABANK[language(context)], INFINBANK[language(context)]],
        [IPAKYULIBANK[language(context)], IPOTEKABANK[language(context)]],
        [KAPITALBANK[language(context)], QQB[language(context)]],
        [MIKROKREDITBANK[language(context)], SAVDOGARBANK[language(context)]],
        [TRASTBANK[language(context)], TURONBANK[language(context)]],
        [UZMILLIYBANK[language(context)], UZSANOATQURILISHBANK[language(context)]],
        [UNIVERSALBANK[language(context)], XALQBANKI[language(context)]],
        [HAMKORBANK[language(context)]]
    ]
    context.bot.send_message(chat_id=chat_id,
                             text=bank_txt[language(context)],
                             reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                             parse_mode='HTML')
    return REASON


def samarkand_region(update, context):
    chat_id = update.message.chat_id
    data = update.message.text
    context.user_data.update({
        'region': data
    })
    cursor.execute("UPDATE Users SET region = '{}' WHERE id = '{}'".format(data, my_id(context)))
    conn.commit()
    buttons = [
        [AGROBANK[language(context)], ASIA_ALLIANCE_BANK[language(context)]],
        [ALOQABANK[language(context)], ASAKABANK[language(context)]],
        [ZIRAATBANK[language(context)], INFINBANK[language(context)]],
        [IPAKYULIBANK[language(context)], IPOTEKABANK[language(context)]],
        [KAPITALBANK[language(context)], QQB[language(context)]],
        [MIKROKREDITBANK[language(context)], OFB[language(context)]],
        [SAVDOGARBANK[language(context)], TENGEBANK[language(context)]],
        [TRASTBANK[language(context)], TURONBANK[language(context)]],
        [UZMILLIYBANK[language(context)], UZSANOATQURILISHBANK[language(context)]],
        [XALQBANKI[language(context)], HAMKORBANK[language(context)]],
    ]
    context.bot.send_message(chat_id=chat_id,
                             text=bank_txt[language(context)],
                             reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                             parse_mode='HTML')
    return REASON


def surkhandarya_region(update, context):
    chat_id = update.message.chat_id
    data = update.message.text
    context.user_data.update({
        'region': data
    })
    cursor.execute("UPDATE Users SET region = '{}' WHERE id = '{}'".format(data, my_id(context)))
    conn.commit()
    buttons = [
        [AGROBANK[language(context)], ALOQABANK[language(context)]],
        [ASAKABANK[language(context)], IPOTEKABANK[language(context)]],
        [KAPITALBANK[language(context)], QQB[language(context)]],
        [MIKROKREDITBANK[language(context)], SAVDOGARBANK[language(context)]],
        [TRASTBANK[language(context)], TURONBANK[language(context)]],
        [UZMILLIYBANK[language(context)], UZSANOATQURILISHBANK[language(context)]],
        [XALQBANKI[language(context)], HAMKORBANK[language(context)]]
    ]
    context.bot.send_message(chat_id=chat_id,
                             text=bank_txt[language(context)],
                             reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                             parse_mode='HTML')
    return REASON


def sirdarya_region(update, context):
    chat_id = update.message.chat_id
    data = update.message.text
    context.user_data.update({
        'region': data
    })
    cursor.execute("UPDATE Users SET region = '{}' WHERE id = '{}'".format(data, my_id(context)))
    conn.commit()
    buttons = [
        [AGROBANK[language(context)], ALOQABANK[language(context)]],
        [ASAKABANK[language(context)], IPOTEKABANK[language(context)]],
        [QQB[language(context)], MIKROKREDITBANK[language(context)]],
        [SAVDOGARBANK[language(context)], TRASTBANK[language(context)]],
        [TURONBANK[language(context)], UZMILLIYBANK[language(context)]],
        [UZSANOATQURILISHBANK[language(context)], XALQBANKI[language(context)]],
        [HAMKORBANK[language(context)]]
    ]
    context.bot.send_message(chat_id=chat_id,
                             text=bank_txt[language(context)],
                             reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                             parse_mode='HTML')
    return REASON


def tashkent_region(update, context):
    chat_id = update.message.chat_id
    data = update.message.text
    context.user_data.update({
        'region': data
    })
    cursor.execute("UPDATE Users SET region = '{}' WHERE id = '{}'".format(data, my_id(context)))
    conn.commit()
    buttons = [
        [AGROBANK[language(context)], ALOQABANK[language(context)]],
        [DAVRBANK[language(context)], INFINBANK[language(context)]],
        [IPAKYULIBANK[language(context)], IPOTEKABANK[language(context)]],
        [QQB[language(context)], MIKROKREDITBANK[language(context)]],
        [OFB[language(context)], SAVDOGARBANK[language(context)]],
        [TRASTBANK[language(context)], TURKISTONBANK[language(context)]],
        [TURONBANK[language(context)], UZMILLIYBANK[language(context)]],
        [UZSANOATQURILISHBANK[language(context)], UNIVERSALBANK[language(context)]],
        [XALQBANKI[language(context)], HAMKORBANK[language(context)]],
    ]
    context.bot.send_message(chat_id=chat_id,
                             text=bank_txt[language(context)],
                             reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                             parse_mode='HTML')
    return REASON


def tashkent_city(update, context):
    chat_id = update.message.chat_id
    data = update.message.text
    context.user_data.update({
        'region': data
    })
    cursor.execute("UPDATE Users SET region = '{}' WHERE id = '{}'".format(data, my_id(context)))
    conn.commit()
    buttons = [
        [AGROBANK[language(context)], ASIA_ALLIANCE_BANK[language(context)]],
        [ALOQABANK[language(context)], ANORBANK[language(context)]],
        [ASAKABANK[language(context)], DAVRBANK[language(context)]],
        [ZIRAATBANK[language(context)], INFINBANK[language(context)]],
        [IPAKYULIBANK[language(context)], IPOTEKABANK[language(context)]],
        [KAPITALBANK[language(context)], QQB[language(context)]],
        [MIKROKREDITBANK[language(context)], OFB[language(context)]],
        [POYTAXTBANK[language(context)], RAVNAQBANK[language(context)]],
        [SAVDOGARBANK[language(context)], TENGEBANK[language(context)]],
        [TBCBANK[language(context)], TRASTBANK[language(context)]],
        [TURKISTONBANK[language(context)], TURONBANK[language(context)]],
        [UZAGROBANK[language(context)], UZKDB[language(context)]],
        [UZMILLIYBANK[language(context)], UZSANOATQURILISHBANK[language(context)]],
        [UNIVERSALBANK[language(context)], HITECHBANK[language(context)]],
        [XALQBANKI[language(context)], HAMKORBANK[language(context)]],
        [ERONSODEROTBANK[language(context)]]
    ]
    context.bot.send_message(chat_id=chat_id,
                             text=bank_txt[language(context)],
                             reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                             parse_mode='HTML')
    return REASON


def fergana_region(update, context):
    chat_id = update.message.chat_id
    data = update.message.text
    context.user_data.update({
        'region': data
    })
    cursor.execute("UPDATE Users SET region = '{}' WHERE id = '{}'".format(data, my_id(context)))
    conn.commit()
    buttons = [
        [AGROBANK[language(context)], ASIA_ALLIANCE_BANK[language(context)]],
        [ALOQABANK[language(context)], ASAKABANK[language(context)]],
        [INFINBANK[language(context)], IPAKYULIBANK[language(context)]],
        [IPOTEKABANK[language(context)], KAPITALBANK[language(context)]],
        [QQB[language(context)], MADADINVESTBANK[language(context)]],
        [MIKROKREDITBANK[language(context)], SAVDOGARBANK[language(context)]],
        [TENGEBANK[language(context)], TRASTBANK[language(context)]],
        [TURONBANK[language(context)], UZMILLIYBANK[language(context)]],
        [UZSANOATQURILISHBANK[language(context)], UNIVERSALBANK[language(context)]],
        [XALQBANKI[language(context)], HAMKORBANK[language(context)]]
    ]
    context.bot.send_message(chat_id=chat_id,
                             text=bank_txt[language(context)],
                             reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                             parse_mode='HTML')
    return REASON


def khorezm_region(update, context):
    chat_id = update.message.chat_id
    data = update.message.text
    context.user_data.update({
        'region': data
    })
    cursor.execute("UPDATE Users SET region = '{}' WHERE id = '{}'".format(data, my_id(context)))
    conn.commit()
    buttons = [
        [AGROBANK[language(context)], ALOQABANK[language(context)]],
        [ASAKABANK[language(context)], INFINBANK[language(context)]],
        [IPOTEKABANK[language(context)], KAPITALBANK[language(context)]],
        [QQB[language(context)], MIKROKREDITBANK[language(context)]],
        [SAVDOGARBANK[language(context)], TRASTBANK[language(context)]],
        [TURONBANK[language(context)], UZMILLIYBANK[language(context)]],
        [UZSANOATQURILISHBANK[language(context)], XALQBANKI[language(context)]],
        [HAMKORBANK[language(context)]]
    ]
    context.bot.send_message(chat_id=chat_id,
                             text=bank_txt[language(context)],
                             reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                             parse_mode='HTML')
    return REASON


def reasons(update, context):
    chat_id = update.message.chat_id
    data = update.message.text
    context.user_data.update({
        'bank': data
    })
    cursor.execute("UPDATE Users SET bank = '{}' WHERE id = '{}'".format(data, my_id(context)))
    conn.commit()
    buttons = [
        [REASON_RECOMMENDATION[language(context)], REASON_SERVICE_CONDITIONS[language(context)]],
        [REASON_QUALITY_SERVICE[language(context)], REASON_CREDIT_AVAILABILITY[language(context)]],
        [REASON_BANK_POPULARITY[language(context)], REASON_UNDERSTANDABLE_CONDITIONS[language(context)]],
        [REASON_RELIABLE_BANK[language(context)], REASON_BANK_OPERATIVES[language(context)]],
        [REASON_WIDE_RANGE[language(context)]], [REASON_LOCATION[language(context)]],
        [REASON_REMOTE[language(context)]], [REASON_OTHER[language(context)]],
        [CONTINUE[language(context)]]
    ]
    context.bot.send_message(chat_id=chat_id,
                             text=reason_txt[language(context)],
                             reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                             parse_mode='HTML')
    return REASON_EDIT_STATE


selected = []


def reason_edit(update, context):
    chat_id = update.message.chat_id
    text = update.message.text
    buttons = [
        [REASON_RECOMMENDATION[language(context)], REASON_SERVICE_CONDITIONS[language(context)]],
        [REASON_QUALITY_SERVICE[language(context)], REASON_CREDIT_AVAILABILITY[language(context)]],
        [REASON_BANK_POPULARITY[language(context)], REASON_UNDERSTANDABLE_CONDITIONS[language(context)]],
        [REASON_RELIABLE_BANK[language(context)], REASON_BANK_OPERATIVES[language(context)]],
        [REASON_WIDE_RANGE[language(context)]], [REASON_LOCATION[language(context)]],
        [REASON_REMOTE[language(context)]], [REASON_OTHER[language(context)]],
        [CONTINUE[language(context)]]
    ]
    if text not in selected and text != PREVIOUS[language(context)]:
        selected.append(text)
        context.bot.send_message(chat_id=chat_id,
                                 text=multiple_choices_add[language(context)].format(text, ', '.join(selected[0:])),
                                 reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                                 parse_mode='HTML')
    elif text in selected and text != PREVIOUS[language(context)]:
        selected.remove(text)
        context.bot.send_message(chat_id=chat_id,
                                 text=multiple_choices_remove[language(context)].format(text, ', '.join(selected[0:])),
                                 reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                                 parse_mode='HTML')
    elif text == PREVIOUS[language(context)]:
        context.bot.send_message(chat_id=chat_id,
                                 text=multiple_choices_back[language(context)].format(', '.join(selected[0:])),
                                 reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                                 parse_mode='HTML')
        return REASON_EDIT_STATE


def reason_edit_other(update, context):
    chat_id = update.message.chat_id
    button = [
        [PREVIOUS[language(context)]]
    ]
    context.bot.send_message(chat_id=chat_id,
                             text=reason_other_txt[language(context)],
                             reply_markup=ReplyKeyboardMarkup(button, resize_keyboard=True))
    return REO_STATE


# Just catch the message from the function above
def get_reo(update, context):
    text = update.message.text
    cursor.execute("UPDATE Users SET reason_other = '{}' WHERE id = '{}'".format(text, my_id(context)))
    conn.commit()
    reason_edit(update, context)
    return REASON_EDIT_STATE


def save_info(update, context):
    if REASON_RECOMMENDATION[language(context)] in selected:
        cursor.execute("UPDATE Users SET reason_recommendation = 1 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    else:
        cursor.execute("UPDATE Users SET reason_recommendation = 0 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    if REASON_SERVICE_CONDITIONS[language(context)] in selected:
        cursor.execute("UPDATE Users SET reason_service_conditions = 1 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    else:
        cursor.execute("UPDATE Users SET reason_service_conditions = 0 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    if REASON_QUALITY_SERVICE[language(context)] in selected:
        cursor.execute("UPDATE Users SET reason_quality_service = 1 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    else:
        cursor.execute("UPDATE Users SET reason_quality_service = 0 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    if REASON_CREDIT_AVAILABILITY[language(context)] in selected:
        cursor.execute("UPDATE Users SET reason_credit_availability = 1 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    else:
        cursor.execute("UPDATE Users SET reason_credit_availability = 0 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    if REASON_BANK_POPULARITY[language(context)] in selected:
        cursor.execute("UPDATE Users SET reason_bank_popularity = 1 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    else:
        cursor.execute("UPDATE Users SET reason_bank_popularity = 0 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    if REASON_UNDERSTANDABLE_CONDITIONS[language(context)] in selected:
        cursor.execute("UPDATE Users SET reason_understandable_conditions = 1 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    else:
        cursor.execute("UPDATE Users SET reason_understandable_conditions = 0 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    if REASON_RELIABLE_BANK[language(context)] in selected:
        cursor.execute("UPDATE Users SET reason_reliable_bank = 1 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    else:
        cursor.execute("UPDATE Users SET reason_reliable_bank = 0 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    if REASON_BANK_OPERATIVES[language(context)] in selected:
        cursor.execute("UPDATE Users SET reason_bank_operatives = 1 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    else:
        cursor.execute("UPDATE Users SET reason_bank_operatives = 0 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    if REASON_WIDE_RANGE[language(context)] in selected:
        cursor.execute("UPDATE Users SET reason_wide_range = 1 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    else:
        cursor.execute("UPDATE Users SET reason_wide_range = 0 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    if REASON_LOCATION[language(context)] in selected:
        cursor.execute("UPDATE Users SET reason_location = 1 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    else:
        cursor.execute("UPDATE Users SET reason_location = 0 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    if REASON_REMOTE[language(context)] in selected:
        cursor.execute("UPDATE Users SET reason_remote = 1 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    else:
        cursor.execute("UPDATE Users SET reason_remote = 0 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    frequency(update, context)
    return FREQUENCY


def frequency(update, context):
    buttons = [
        [EVERYDAY[language(context)]],
        [ONCE_A_WEEK[language(context)], ONCE_A_MONTH[language(context)]],
        [DONT_GO[language(context)]],
        [FREQ_OTHER[language(context)]]
    ]
    update.message.reply_text(frequency_txt[language(context)],
                              reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                              parse_mode='HTML')
    return FREQUENCY


def freq_other(update, context):
    chat_id = update.message.chat_id
    button = [
        [PREVIOUS[language(context)]]
    ]
    context.bot.send_message(chat_id=chat_id,
                             text=other_frequency_txt[language(context)],
                             reply_markup=ReplyKeyboardMarkup(button, resize_keyboard=True))
    return FREQ_OTHER_STATE


def get_freq_other(update, context):
    text = update.message.text
    cursor.execute("UPDATE Users SET frequency = '{}' WHERE id = '{}'".format(text, my_id(context)))
    service(update, context)
    return SERVICE_STATE


def service(update, context):
    data = update.message.text
    user = context.user_data['identity']
    chat_id = update.message.chat_id
    cursor.execute("UPDATE Users SET frequency = '{}' WHERE id = '{}'".format(data, my_id(context)))
    conn.commit()
    buttons_1 = [
        [CREDIT[language(context)], DEPOSIT[language(context)]],
        [CARD[language(context)], PAYMENT[language(context)]],
        [EXCHANGE[language(context)], TRANSFER[language(context)]],
        [WITHDRAWAL[language(context)], SERVICE_OTHER[language(context)]],
        [CONTINUE[language(context)]]
    ]
    buttons_2 = [
        [CREDIT[language(context)], DEPOSIT[language(context)]],
        [CARD[language(context)], CHECKING_ACC[language(context)]],
        [CONSULTING[language(context)], CURRENCY_OP[language(context)]],
        [INTERNET_BANK[language(context)], SERVICE_OTHER[language(context)]],
        [CONTINUE[language(context)]]
    ]
    if user == NATURAL_PERSON[language(context)]:
        context.bot.send_message(chat_id=chat_id,
                                 text=services_txt[language(context)],
                                 reply_markup=ReplyKeyboardMarkup(buttons_1, resize_keyboard=True),
                                 parse_mode='HTML')
    else:
        context.bot.send_message(chat_id=chat_id,
                                 text=services_txt[language(context)],
                                 reply_markup=ReplyKeyboardMarkup(buttons_2, resize_keyboard=True),
                                 parse_mode='HTML')
    return SERVICE_STATE


service_items = []


def service_edit(update, context):
    chat_id = update.message.chat_id
    text = update.message.text
    user = context.user_data['identity']
    buttons_1 = [
        [CREDIT[language(context)], DEPOSIT[language(context)]],
        [CARD[language(context)], PAYMENT[language(context)]],
        [EXCHANGE[language(context)], TRANSFER[language(context)]],
        [WITHDRAWAL[language(context)], SERVICE_OTHER[language(context)]],
        [CONTINUE[language(context)]]
    ]
    buttons_2 = [
        [CREDIT[language(context)], DEPOSIT[language(context)]],
        [CARD[language(context)], CHECKING_ACC[language(context)]],
        [CONSULTING[language(context)], CURRENCY_OP[language(context)]],
        [INTERNET_BANK[language(context)], SERVICE_OTHER[language(context)]],
        [CONTINUE[language(context)]]
    ]
    if user == NATURAL_PERSON[language(context)]:
        if text not in service_items and text != PREVIOUS[language(context)]:
            service_items.append(text)
            context.bot.send_message(chat_id=chat_id,
                                     text=multiple_choices_add[language(context)].format(text,
                                                                                         ', '.join(service_items[0:])),
                                     reply_markup=ReplyKeyboardMarkup(buttons_1, resize_keyboard=True),
                                     parse_mode='HTML')
        elif text in service_items and text != PREVIOUS[language(context)]:
            service_items.remove(text)
            context.bot.send_message(chat_id=chat_id,
                                     text=multiple_choices_remove[language(context)].format(text, ', '.join(
                                         service_items[0:])),
                                     reply_markup=ReplyKeyboardMarkup(buttons_1, resize_keyboard=True),
                                     parse_mode='HTML')
        elif text == PREVIOUS[language(context)]:
            context.bot.send_message(chat_id=chat_id,
                                     text=multiple_choices_back[language(context)].format(', '.join(service_items[0:])),
                                     reply_markup=ReplyKeyboardMarkup(buttons_1, resize_keyboard=True),
                                     parse_mode='HTML')
            return SERVICE_STATE
    else:
        if text not in service_items and text != PREVIOUS[language(context)]:
            service_items.append(text)
            context.bot.send_message(chat_id=chat_id,
                                     text=multiple_choices_add[language(context)].format(text,
                                                                                         ', '.join(service_items[0:])),
                                     reply_markup=ReplyKeyboardMarkup(buttons_2, resize_keyboard=True),
                                     parse_mode='HTML')
        elif text in service_items and text != PREVIOUS[language(context)]:
            service_items.remove(text)
            context.bot.send_message(chat_id=chat_id,
                                     text=multiple_choices_remove[language(context)].format(text, ', '.join(
                                         service_items[0:])),
                                     reply_markup=ReplyKeyboardMarkup(buttons_2, resize_keyboard=True),
                                     parse_mode='HTML')
        elif text == PREVIOUS[language(context)]:
            context.bot.send_message(chat_id=chat_id,
                                     text=multiple_choices_back[language(context)].format(', '.join(service_items[0:])),
                                     reply_markup=ReplyKeyboardMarkup(buttons_2, resize_keyboard=True),
                                     parse_mode='HTML')
            return SERVICE_STATE


def service_edit_other(update, context):
    chat_id = update.message.chat_id
    button = [
        [PREVIOUS[language(context)]]
    ]
    context.bot.send_message(chat_id=chat_id,
                             text=service_other_txt[language(context)],
                             reply_markup=ReplyKeyboardMarkup(button, resize_keyboard=True))
    return SERVICE_EDIT_STATE


def get_service_other(update, context):
    text = update.message.text
    cursor.execute("UPDATE Users SET service_other = '{}' WHERE id = '{}'".format(text, my_id(context)))
    conn.commit()
    service_edit(update, context)
    return SERVICE_STATE


def save_services_info(update, context):
    if CREDIT[language(context)] in service_items:
        cursor.execute("UPDATE Users SET service_credit = 1 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    else:
        cursor.execute("UPDATE Users SET service_credit = 0 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    if DEPOSIT[language(context)] in service_items:
        cursor.execute("UPDATE Users SET service_deposit = 1 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    else:
        cursor.execute("UPDATE Users SET service_deposit = 0 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    if CARD[language(context)] in service_items:
        cursor.execute("UPDATE Users SET service_card = 1 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    else:
        cursor.execute("UPDATE Users SET service_card = 0 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    if PAYMENT[language(context)] in service_items:
        cursor.execute("UPDATE Users SET service_payment = 1 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    else:
        cursor.execute("UPDATE Users SET service_payment = 0 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    if EXCHANGE[language(context)] in service_items:
        cursor.execute("UPDATE Users SET service_exchange = 1 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    else:
        cursor.execute("UPDATE Users SET service_exchange = 0 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    if TRANSFER[language(context)] in service_items:
        cursor.execute("UPDATE Users SET service_transfer = 1 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    else:
        cursor.execute("UPDATE Users SET service_transfer = 0 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    if WITHDRAWAL[language(context)] in service_items:
        cursor.execute("UPDATE Users SET service_withdrawal = 1 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    else:
        cursor.execute("UPDATE Users SET service_withdrawal = 0 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    if CHECKING_ACC[language(context)] in service_items:
        cursor.execute("UPDATE Users SET service_checking_acc = 1 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    else:
        cursor.execute("UPDATE Users SET service_checking_acc = 0 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    if CONSULTING[language(context)] in service_items:
        cursor.execute("UPDATE Users SET service_consulting = 1 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    else:
        cursor.execute("UPDATE Users SET service_consulting = 0 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    if CURRENCY_OP[language(context)] in service_items:
        cursor.execute("UPDATE Users SET service_currency_op = 1 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    else:
        cursor.execute("UPDATE Users SET service_currency_op = 0 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    if INTERNET_BANK[language(context)] in service_items:
        cursor.execute("UPDATE Users SET service_internet_bank = 1 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    else:
        cursor.execute("UPDATE Users SET service_internet_bank = 0 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    rating_services_credit(update, context)
    return RATING_SERVICES_CREDIT


def rating_services_credit(update, context):
    chat_id = update.message.chat_id
    user = context.user_data['identity']
    buttons = [
        [GOOD[language(context)]],
        [SATISFACTORY[language(context)]],
        [DISSATISFACTORY[language(context)]],
        [BAD[language(context)]],
        [DONT_KNOW[language(context)]]
    ]
    context.bot.send_message(chat_id=chat_id,
                             text=rating_txt[language(context)].format(CREDIT[language(context)]),
                             reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                             parse_mode='HTML')


def get_credit_rating(update, context):
    text = update.message.text
    if text == GOOD[language(context)]:
        cursor.execute("UPDATE Users SET rating_credit = 5 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == SATISFACTORY[language(context)]:
        cursor.execute("UPDATE Users SET rating_credit = 4 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == DISSATISFACTORY[language(context)]:
        cursor.execute("UPDATE Users SET rating_credit = 3 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == BAD[language(context)]:
        cursor.execute("UPDATE Users SET rating_credit = 2 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == DONT_KNOW[language(context)]:
        cursor.execute("UPDATE Users SET rating_credit = 0 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    rating_services_deposit(update, context)
    return RATING_SERVICES_DEPOSIT


def rating_services_deposit(update, context):
    chat_id = update.message.chat_id
    buttons = [
        [GOOD[language(context)]],
        [SATISFACTORY[language(context)]],
        [DISSATISFACTORY[language(context)]],
        [BAD[language(context)]],
        [DONT_KNOW[language(context)]]
    ]
    context.bot.send_message(chat_id=chat_id,
                             text=rating_txt[language(context)].format(DEPOSIT[language(context)]),
                             reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                             parse_mode='HTML')


def get_deposit_rating(update, context):
    text = update.message.text
    if text == GOOD[language(context)]:
        cursor.execute("UPDATE Users SET rating_deposit = 5 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == SATISFACTORY[language(context)]:
        cursor.execute("UPDATE Users SET rating_deposit = 4 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == DISSATISFACTORY[language(context)]:
        cursor.execute("UPDATE Users SET rating_deposit = 3 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == BAD[language(context)]:
        cursor.execute("UPDATE Users SET rating_deposit = 2 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == DONT_KNOW[language(context)]:
        cursor.execute("UPDATE Users SET rating_deposit = 0 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    rating_services_card(update, context)
    return RATING_SERVICES_CARD


def rating_services_card(update, context):
    chat_id = update.message.chat_id
    buttons = [
        [GOOD[language(context)]],
        [SATISFACTORY[language(context)]],
        [DISSATISFACTORY[language(context)]],
        [BAD[language(context)]],
        [DONT_KNOW[language(context)]]
    ]
    context.bot.send_message(chat_id=chat_id,
                             text=rating_txt[language(context)].format(CARD[language(context)]),
                             reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                             parse_mode='HTML')


def get_card_rating(update, context):
    text = update.message.text
    if text == GOOD[language(context)]:
        cursor.execute("UPDATE Users SET rating_card = 5 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == SATISFACTORY[language(context)]:
        cursor.execute("UPDATE Users SET rating_card = 4 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == DISSATISFACTORY[language(context)]:
        cursor.execute("UPDATE Users SET rating_card = 3 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == BAD[language(context)]:
        cursor.execute("UPDATE Users SET rating_card = 2 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == DONT_KNOW[language(context)]:
        cursor.execute("UPDATE Users SET rating_card = 0 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    rating_services_payment(update, context)
    return RATING_SERVICES_PAYMENT


def rating_services_payment(update, context):
    chat_id = update.message.chat_id
    user = context.user_data['identity']
    buttons = [
        [GOOD[language(context)]],
        [SATISFACTORY[language(context)]],
        [DISSATISFACTORY[language(context)]],
        [BAD[language(context)]],
        [DONT_KNOW[language(context)]]
    ]
    if user == NATURAL_PERSON[language(context)]:
        context.bot.send_message(chat_id=chat_id,
                                 text=rating_txt[language(context)].format(PAYMENT[language(context)]),
                                 reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                                 parse_mode='HTML')
    else:
        context.bot.send_message(chat_id=chat_id,
                                 text=rating_txt[language(context)].format(CHECKING_ACC[language(context)]),
                                 reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                                 parse_mode='HTML')


def get_payment_rating(update, context):
    text = update.message.text
    user = context.user_data['identity']
    if user == NATURAL_PERSON[language(context)]:
        if text == GOOD[language(context)]:
            cursor.execute("UPDATE Users SET rating_payment = 5 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == SATISFACTORY[language(context)]:
            cursor.execute("UPDATE Users SET rating_payment = 4 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == DISSATISFACTORY[language(context)]:
            cursor.execute("UPDATE Users SET rating_payment = 3 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == BAD[language(context)]:
            cursor.execute("UPDATE Users SET rating_payment = 2 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == DONT_KNOW[language(context)]:
            cursor.execute("UPDATE Users SET rating_payment = 0 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        rating_services_exchange(update, context)
        return RATING_SERVICES_EXCHANGE
    else:
        if text == GOOD[language(context)]:
            cursor.execute("UPDATE Users SET rating_checking_acc = 5 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == SATISFACTORY[language(context)]:
            cursor.execute("UPDATE Users SET rating_checking_acc = 4 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == DISSATISFACTORY[language(context)]:
            cursor.execute("UPDATE Users SET rating_checking_acc = 3 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == BAD[language(context)]:
            cursor.execute("UPDATE Users SET rating_checking_acc = 2 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == DONT_KNOW[language(context)]:
            cursor.execute("UPDATE Users SET rating_checking_acc = 0 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        rating_services_exchange(update, context)
        return RATING_SERVICES_EXCHANGE


def rating_services_exchange(update, context):
    chat_id = update.message.chat_id
    user = context.user_data['identity']
    buttons = [
        [GOOD[language(context)]],
        [SATISFACTORY[language(context)]],
        [DISSATISFACTORY[language(context)]],
        [BAD[language(context)]],
        [DONT_KNOW[language(context)]]
    ]
    if user == NATURAL_PERSON[language(context)]:
        context.bot.send_message(chat_id=chat_id,
                                 text=rating_txt[language(context)].format(EXCHANGE[language(context)]),
                                 reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                                 parse_mode='HTML')
    else:
        context.bot.send_message(chat_id=chat_id,
                                 text=rating_txt[language(context)].format(CONSULTING[language(context)]),
                                 reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                                 parse_mode='HTML')


def get_exchange_rating(update, context):
    text = update.message.text
    user = context.user_data['identity']
    if user == NATURAL_PERSON[language(context)]:
        if text == GOOD[language(context)]:
            cursor.execute("UPDATE Users SET rating_exchange = 5 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == SATISFACTORY[language(context)]:
            cursor.execute("UPDATE Users SET rating_exchange = 4 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == DISSATISFACTORY[language(context)]:
            cursor.execute("UPDATE Users SET rating_exchange = 3 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == BAD[language(context)]:
            cursor.execute("UPDATE Users SET rating_exchange = 2 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == DONT_KNOW[language(context)]:
            cursor.execute("UPDATE Users SET rating_exchange = 0 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        rating_services_transfer(update, context)
        return RATING_SERVICES_TRANSFER
    else:
        if text == GOOD[language(context)]:
            cursor.execute("UPDATE Users SET rating_consulting = 5 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == SATISFACTORY[language(context)]:
            cursor.execute("UPDATE Users SET rating_consulting = 4 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == DISSATISFACTORY[language(context)]:
            cursor.execute("UPDATE Users SET rating_consulting = 3 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == BAD[language(context)]:
            cursor.execute("UPDATE Users SET rating_consulting = 2 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == DONT_KNOW[language(context)]:
            cursor.execute("UPDATE Users SET rating_consulting = 0 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        rating_services_transfer(update, context)
        return RATING_SERVICES_TRANSFER


def rating_services_transfer(update, context):
    chat_id = update.message.chat_id
    user = context.user_data['identity']
    buttons = [
        [GOOD[language(context)]],
        [SATISFACTORY[language(context)]],
        [DISSATISFACTORY[language(context)]],
        [BAD[language(context)]],
        [DONT_KNOW[language(context)]]
    ]
    if user == NATURAL_PERSON[language(context)]:
        context.bot.send_message(chat_id=chat_id,
                                 text=rating_txt[language(context)].format(TRANSFER[language(context)]),
                                 reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                                 parse_mode='HTML')
    else:
        context.bot.send_message(chat_id=chat_id,
                                 text=rating_txt[language(context)].format(CURRENCY_OP[language(context)]),
                                 reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                                 parse_mode='HTML')


def get_transfer_rating(update, context):
    text = update.message.text
    user = context.user_data['identity']
    if user == NATURAL_PERSON[language(context)]:
        if text == GOOD[language(context)]:
            cursor.execute("UPDATE Users SET rating_transfer = 5 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == SATISFACTORY[language(context)]:
            cursor.execute("UPDATE Users SET rating_transfer = 4 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == DISSATISFACTORY[language(context)]:
            cursor.execute("UPDATE Users SET rating_transfer = 3 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == BAD[language(context)]:
            cursor.execute("UPDATE Users SET rating_transfer = 2 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == DONT_KNOW[language(context)]:
            cursor.execute("UPDATE Users SET rating_transfer = 0 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        rating_services_withdrawal(update, context)
        return RATING_SERVICES_WITHDRAWAL
    else:
        if text == GOOD[language(context)]:
            cursor.execute("UPDATE Users SET rating_currency_op = 5 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == SATISFACTORY[language(context)]:
            cursor.execute("UPDATE Users SET rating_currency_op = 4 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == DISSATISFACTORY[language(context)]:
            cursor.execute("UPDATE Users SET rating_currency_op = 3 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == BAD[language(context)]:
            cursor.execute("UPDATE Users SET rating_currency_op = 2 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == DONT_KNOW[language(context)]:
            cursor.execute("UPDATE Users SET rating_currency_op = 0 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        rating_services_withdrawal(update, context)
        return RATING_SERVICES_WITHDRAWAL


def rating_services_withdrawal(update, context):
    chat_id = update.message.chat_id
    user = context.user_data['identity']
    buttons = [
        [GOOD[language(context)]],
        [SATISFACTORY[language(context)]],
        [DISSATISFACTORY[language(context)]],
        [BAD[language(context)]],
        [DONT_KNOW[language(context)]]
    ]
    if user == NATURAL_PERSON[language(context)]:
        context.bot.send_message(chat_id=chat_id,
                                 text=rating_txt[language(context)].format(WITHDRAWAL[language(context)]),
                                 reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                                 parse_mode='HTML')
    else:
        context.bot.send_message(chat_id=chat_id,
                                 text=rating_txt[language(context)].format(INTERNET_BANK[language(context)]),
                                 reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                                 parse_mode='HTML')


def get_withdrawal_rating(update, context):
    text = update.message.text
    user = context.user_data['identity']
    if user == NATURAL_PERSON[language(context)]:
        if text == GOOD[language(context)]:
            cursor.execute("UPDATE Users SET rating_withdrawal = 5 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == SATISFACTORY[language(context)]:
            cursor.execute("UPDATE Users SET rating_withdrawal = 4 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == DISSATISFACTORY[language(context)]:
            cursor.execute("UPDATE Users SET rating_withdrawal = 3 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == BAD[language(context)]:
            cursor.execute("UPDATE Users SET rating_withdrawal = 2 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == DONT_KNOW[language(context)]:
            cursor.execute("UPDATE Users SET rating_withdrawal = 0 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        p_deadline(update, context)
        return RATING_PARAMETERS_DEADLINE
    else:
        if text == GOOD[language(context)]:
            cursor.execute("UPDATE Users SET rating_internet_bank = 5 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == SATISFACTORY[language(context)]:
            cursor.execute("UPDATE Users SET rating_internet_bank = 4 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == DISSATISFACTORY[language(context)]:
            cursor.execute("UPDATE Users SET rating_internet_bank = 3 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == BAD[language(context)]:
            cursor.execute("UPDATE Users SET rating_internet_bank = 2 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == DONT_KNOW[language(context)]:
            cursor.execute("UPDATE Users SET rating_internet_bank = 0 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        p_deadline(update, context)
        return RATING_PARAMETERS_DEADLINE


def p_deadline(update, context):
    chat_id = update.message.chat_id
    buttons = [
        [FULLY_DISSATISFIED[language(context)]],
        [DISSATISFIED[language(context)]],
        [SATISFIED[language(context)]],
        [FULLY_SATISFIED[language(context)]],
        [HARD_TO_ANSWER[language(context)]]
    ]
    context.bot.send_message(chat_id=chat_id,
                             text=parameters_txt[language(context)].format(PARAM_D_T[language(context)]),
                             reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                             parse_mode='HTML')


def p_get_deadline(update, context):
    text = update.message.text
    if text == FULLY_DISSATISFIED[language(context)]:
        cursor.execute("UPDATE Users SET parameter_deadline = 2 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == DISSATISFIED[language(context)]:
        cursor.execute("UPDATE Users SET parameter_deadline = 3 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == SATISFIED[language(context)]:
        cursor.execute("UPDATE Users SET parameter_deadline = 4 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == FULLY_SATISFIED[language(context)]:
        cursor.execute("UPDATE Users SET parameter_deadline = 5 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == HARD_TO_ANSWER[language(context)]:
        cursor.execute("UPDATE Users SET parameter_deadline = 0 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    p_feedback(update, context)
    return RATING_PARAMETERS_FEEDBACK


def p_feedback(update, context):
    chat_id = update.message.chat_id
    buttons = [
        [FULLY_DISSATISFIED[language(context)]],
        [DISSATISFIED[language(context)]],
        [SATISFIED[language(context)]],
        [FULLY_SATISFIED[language(context)]],
        [HARD_TO_ANSWER[language(context)]]
    ]
    context.bot.send_message(chat_id=chat_id,
                             text=parameters_txt[language(context)].format(PARAM_F_T[language(context)]),
                             reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                             parse_mode='HTML')


def p_get_feedback(update, context):
    text = update.message.text
    if text == FULLY_DISSATISFIED[language(context)]:
        cursor.execute("UPDATE Users SET parameter_feedback = 2 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == DISSATISFIED[language(context)]:
        cursor.execute("UPDATE Users SET parameter_feedback = 3 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == SATISFIED[language(context)]:
        cursor.execute("UPDATE Users SET parameter_feedback = 4 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == FULLY_SATISFIED[language(context)]:
        cursor.execute("UPDATE Users SET parameter_feedback = 5 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == HARD_TO_ANSWER[language(context)]:
        cursor.execute("UPDATE Users SET parameter_feedback = 0 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    p_info_available(update, context)
    return RATING_PARAMETERS_INFO_AVAILABLE


def p_info_available(update, context):
    chat_id = update.message.chat_id
    buttons = [
        [FULLY_DISSATISFIED[language(context)]],
        [DISSATISFIED[language(context)]],
        [SATISFIED[language(context)]],
        [FULLY_SATISFIED[language(context)]],
        [HARD_TO_ANSWER[language(context)]]
    ]
    context.bot.send_message(chat_id=chat_id,
                             text=parameters_txt[language(context)].format(PARAM_IA_T[language(context)]),
                             reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                             parse_mode='HTML')


def p_get_info_available(update, context):
    text = update.message.text
    if text == FULLY_DISSATISFIED[language(context)]:
        cursor.execute("UPDATE Users SET parameter_info_availability = 2 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == DISSATISFIED[language(context)]:
        cursor.execute("UPDATE Users SET parameter_info_availability = 3 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == SATISFIED[language(context)]:
        cursor.execute("UPDATE Users SET parameter_info_availability = 4 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == FULLY_SATISFIED[language(context)]:
        cursor.execute("UPDATE Users SET parameter_info_availability = 5 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == HARD_TO_ANSWER[language(context)]:
        cursor.execute("UPDATE Users SET parameter_info_availability = 0 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    p_personal(update, context)
    return RATING_PARAMETERS_PERSONAL


def p_personal(update, context):
    chat_id = update.message.chat_id
    buttons = [
        [FULLY_DISSATISFIED[language(context)]],
        [DISSATISFIED[language(context)]],
        [SATISFIED[language(context)]],
        [FULLY_SATISFIED[language(context)]],
        [HARD_TO_ANSWER[language(context)]]
    ]
    context.bot.send_message(chat_id=chat_id,
                             text=parameters_txt[language(context)].format(PARAM_P_T[language(context)]),
                             reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                             parse_mode='HTML')


def p_get_personal(update, context):
    text = update.message.text
    if text == FULLY_DISSATISFIED[language(context)]:
        cursor.execute("UPDATE Users SET parameter_personal = 2 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == DISSATISFIED[language(context)]:
        cursor.execute("UPDATE Users SET parameter_personal = 3 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == SATISFIED[language(context)]:
        cursor.execute("UPDATE Users SET parameter_personal = 4 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == FULLY_SATISFIED[language(context)]:
        cursor.execute("UPDATE Users SET parameter_personal = 5 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == HARD_TO_ANSWER[language(context)]:
        cursor.execute("UPDATE Users SET parameter_personal = 0 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    r_workers_informed(update, context)
    return RATE_WORKERS_INFORMED


def r_workers_informed(update, context):
    chat_id = update.message.chat_id
    buttons = [
        [GOOD[language(context)]],
        [SATISFACTORY[language(context)]],
        [DISSATISFACTORY[language(context)]],
        [BAD[language(context)]],
        [HARD_TO_ANSWER[language(context)]]
    ]
    context.bot.send_message(chat_id=chat_id,
                             text=workers_txt[language(context)].format(WORKER_INF_T[language(context)]),
                             reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                             parse_mode='HTML')


def get_workers_informed(update, context):
    text = update.message.text
    if text == GOOD[language(context)]:
        cursor.execute("UPDATE Users SET worker_informed = 5 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == SATISFACTORY[language(context)]:
        cursor.execute("UPDATE Users SET worker_informed = 4 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == DISSATISFACTORY[language(context)]:
        cursor.execute("UPDATE Users SET worker_informed = 3 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == BAD[language(context)]:
        cursor.execute("UPDATE Users SET worker_informed = 2 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == HARD_TO_ANSWER[language(context)]:
        cursor.execute("UPDATE Users SET worker_informed = 0 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    r_workers_operative(update, context)
    return RATE_WORKERS_OPERATIVE


def r_workers_operative(update, context):
    chat_id = update.message.chat_id
    buttons = [
        [GOOD[language(context)]],
        [SATISFACTORY[language(context)]],
        [DISSATISFACTORY[language(context)]],
        [BAD[language(context)]],
        [HARD_TO_ANSWER[language(context)]]
    ]
    context.bot.send_message(chat_id=chat_id,
                             text=workers_txt[language(context)].format(WORKER_OP_T[language(context)]),
                             reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                             parse_mode='HTML')


def get_workers_operative(update, context):
    text = update.message.text
    if text == GOOD[language(context)]:
        cursor.execute("UPDATE Users SET worker_operative = 5 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == SATISFACTORY[language(context)]:
        cursor.execute("UPDATE Users SET worker_operative = 4 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == DISSATISFACTORY[language(context)]:
        cursor.execute("UPDATE Users SET worker_operative = 3 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == BAD[language(context)]:
        cursor.execute("UPDATE Users SET worker_operative = 2 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == HARD_TO_ANSWER[language(context)]:
        cursor.execute("UPDATE Users SET worker_operative = 0 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    r_workers_professional(update, context)
    return RATE_WORKERS_PROFESSIONAL


def r_workers_professional(update, context):
    chat_id = update.message.chat_id
    buttons = [
        [GOOD[language(context)]],
        [SATISFACTORY[language(context)]],
        [DISSATISFACTORY[language(context)]],
        [BAD[language(context)]],
        [HARD_TO_ANSWER[language(context)]]
    ]
    context.bot.send_message(chat_id=chat_id,
                             text=workers_txt[language(context)].format(WORKER_PROF_T[language(context)]),
                             reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                             parse_mode='HTML')


def get_workers_professional(update, context):
    text = update.message.text
    if text == GOOD[language(context)]:
        cursor.execute("UPDATE Users SET worker_professional = 5 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == SATISFACTORY[language(context)]:
        cursor.execute("UPDATE Users SET worker_professional = 4 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == DISSATISFACTORY[language(context)]:
        cursor.execute("UPDATE Users SET worker_professional = 3 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == BAD[language(context)]:
        cursor.execute("UPDATE Users SET worker_professional = 2 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == HARD_TO_ANSWER[language(context)]:
        cursor.execute("UPDATE Users SET worker_professional = 0 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    r_workers_polite(update, context)
    return RATE_WORKERS_POLITE


def r_workers_polite(update, context):
    chat_id = update.message.chat_id
    buttons = [
        [GOOD[language(context)]],
        [SATISFACTORY[language(context)]],
        [DISSATISFACTORY[language(context)]],
        [BAD[language(context)]],
        [HARD_TO_ANSWER[language(context)]]
    ]
    context.bot.send_message(chat_id=chat_id,
                             text=workers_txt[language(context)].format(WORKER_POL_T[language(context)]),
                             reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                             parse_mode='HTML')


def get_workers_polite(update, context):
    text = update.message.text
    if text == GOOD[language(context)]:
        cursor.execute("UPDATE Users SET worker_polite = 5 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == SATISFACTORY[language(context)]:
        cursor.execute("UPDATE Users SET worker_polite = 4 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == DISSATISFACTORY[language(context)]:
        cursor.execute("UPDATE Users SET worker_polite = 3 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == BAD[language(context)]:
        cursor.execute("UPDATE Users SET worker_polite = 2 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == HARD_TO_ANSWER[language(context)]:
        cursor.execute("UPDATE Users SET worker_polite = 0 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    r_workers_ready_help(update, context)
    return RATE_WORKERS_READY_HELP


def r_workers_ready_help(update, context):
    chat_id = update.message.chat_id
    buttons = [
        [GOOD[language(context)]],
        [SATISFACTORY[language(context)]],
        [DISSATISFACTORY[language(context)]],
        [BAD[language(context)]],
        [HARD_TO_ANSWER[language(context)]]
    ]
    context.bot.send_message(chat_id=chat_id,
                             text=workers_txt[language(context)].format(WORKER_RH_T[language(context)]),
                             reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                             parse_mode='HTML')


def get_workers_ready_help(update, context):
    text = update.message.text
    if text == GOOD[language(context)]:
        cursor.execute("UPDATE Users SET worker_ready_help = 5 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == SATISFACTORY[language(context)]:
        cursor.execute("UPDATE Users SET worker_ready_help = 4 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == DISSATISFACTORY[language(context)]:
        cursor.execute("UPDATE Users SET worker_ready_help = 3 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == BAD[language(context)]:
        cursor.execute("UPDATE Users SET worker_ready_help = 2 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == HARD_TO_ANSWER[language(context)]:
        cursor.execute("UPDATE Users SET worker_ready_help = 0 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    r_statement_navigation(update, context)
    return CHOOSE_STATEMENT_NAVIGATION


def r_statement_navigation(update, context):
    chat_id = update.message.chat_id
    buttons = [
        [FULLY_AGREE[language(context)]],
        [MOSTLY_AGREE[language(context)]],
        [MOSTLY_DISAGREE[language(context)]],
        [FULLY_DISAGREE[language(context)]],
        [HARD_TO_ANSWER[language(context)]]
    ]
    context.bot.send_message(chat_id=chat_id,
                             text=statements_txt[language(context)].format(ST_NAVIGATION[language(context)]),
                             reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                             parse_mode='HTML')


def get_statement_navigation(update, context):
    text = update.message.text
    if text == FULLY_AGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_navigation = 5 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == MOSTLY_AGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_navigation = 4 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == MOSTLY_DISAGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_navigation = 3 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == FULLY_DISAGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_navigation = 2 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == HARD_TO_ANSWER[language(context)]:
        cursor.execute("UPDATE Users SET statement_navigation = 0 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    r_statement_responsibility(update, context)
    return CHOOSE_STATEMENT_RESPONSIBILITY


def r_statement_responsibility(update, context):
    chat_id = update.message.chat_id
    buttons = [
        [FULLY_AGREE[language(context)]],
        [MOSTLY_AGREE[language(context)]],
        [MOSTLY_DISAGREE[language(context)]],
        [FULLY_DISAGREE[language(context)]],
        [HARD_TO_ANSWER[language(context)]]
    ]
    context.bot.send_message(chat_id=chat_id,
                             text=statements_txt[language(context)].format(ST_RESPONSIBILITY[language(context)]),
                             reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                             parse_mode='HTML')


def get_statement_responsibility(update, context):
    text = update.message.text
    user = context.user_data['identity']
    if user == NATURAL_PERSON[language(context)]:
        if text == FULLY_AGREE[language(context)]:
            cursor.execute("UPDATE Users SET statement_responsibility = 5 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == MOSTLY_AGREE[language(context)]:
            cursor.execute("UPDATE Users SET statement_responsibility = 4 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == MOSTLY_DISAGREE[language(context)]:
            cursor.execute("UPDATE Users SET statement_responsibility = 3 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == FULLY_DISAGREE[language(context)]:
            cursor.execute("UPDATE Users SET statement_responsibility = 2 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == HARD_TO_ANSWER[language(context)]:
            cursor.execute("UPDATE Users SET statement_responsibility = 0 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        r_statement_bank_response(update, context)
        return CHOOSE_STATEMENT_BANK_RESPONSE
    else:
        if text == FULLY_AGREE[language(context)]:
            cursor.execute("UPDATE Users SET statement_responsibility = 5 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == MOSTLY_AGREE[language(context)]:
            cursor.execute("UPDATE Users SET statement_responsibility = 4 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == MOSTLY_DISAGREE[language(context)]:
            cursor.execute("UPDATE Users SET statement_responsibility = 3 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == FULLY_DISAGREE[language(context)]:
            cursor.execute("UPDATE Users SET statement_responsibility = 2 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == HARD_TO_ANSWER[language(context)]:
            cursor.execute("UPDATE Users SET statement_responsibility = 0 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        r_statement_bank_advantage(update, context)
        return CHOOSE_STATEMENT_BANK_ADVANTAGE


def r_statement_bank_response(update, context):
    chat_id = update.message.chat_id
    buttons = [
        [FULLY_AGREE[language(context)]],
        [MOSTLY_AGREE[language(context)]],
        [MOSTLY_DISAGREE[language(context)]],
        [FULLY_DISAGREE[language(context)]],
        [HARD_TO_ANSWER[language(context)]]
    ]
    context.bot.send_message(chat_id=chat_id,
                             text=statements_txt[language(context)].format(ST_BANK_RESPONSE[language(context)]),
                             reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                             parse_mode='HTML')


def get_statement_bank_response(update, context):
    text = update.message.text
    if text == FULLY_AGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_bank_response = 5 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == MOSTLY_AGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_bank_response = 4 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == MOSTLY_DISAGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_bank_response = 3 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == FULLY_DISAGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_bank_response = 2 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == HARD_TO_ANSWER[language(context)]:
        cursor.execute("UPDATE Users SET statement_bank_response = 0 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    r_statement_worker_info(update, context)
    return CHOOSE_STATEMENT_WORKER_INFO


def r_statement_worker_info(update, context):
    chat_id = update.message.chat_id
    buttons = [
        [FULLY_AGREE[language(context)]],
        [MOSTLY_AGREE[language(context)]],
        [MOSTLY_DISAGREE[language(context)]],
        [FULLY_DISAGREE[language(context)]],
        [HARD_TO_ANSWER[language(context)]]
    ]
    context.bot.send_message(chat_id=chat_id,
                             text=statements_txt[language(context)].format(ST_WORKER_INFO[language(context)]),
                             reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                             parse_mode='HTML')


def get_statement_worker_info(update, context):
    text = update.message.text
    if text == FULLY_AGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_worker_info = 5 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == MOSTLY_AGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_worker_info = 4 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == MOSTLY_DISAGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_worker_info = 3 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == FULLY_DISAGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_worker_info = 2 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == HARD_TO_ANSWER[language(context)]:
        cursor.execute("UPDATE Users SET statement_worker_info = 0 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    r_statement_bank_fails(update, context)
    return CHOOSE_STATEMENT_BANK_FAILS


def r_statement_bank_fails(update, context):
    chat_id = update.message.chat_id
    buttons = [
        [FULLY_AGREE[language(context)]],
        [MOSTLY_AGREE[language(context)]],
        [MOSTLY_DISAGREE[language(context)]],
        [FULLY_DISAGREE[language(context)]],
        [HARD_TO_ANSWER[language(context)]]
    ]
    context.bot.send_message(chat_id=chat_id,
                             text=statements_txt[language(context)].format(ST_BANK_FAILS[language(context)]),
                             reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                             parse_mode='HTML')


def get_statement_bank_fails(update, context):
    text = update.message.text
    if text == FULLY_AGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_bank_fails = 5 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == MOSTLY_AGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_bank_fails = 4 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == MOSTLY_DISAGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_bank_fails = 3 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == FULLY_DISAGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_bank_fails = 2 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == HARD_TO_ANSWER[language(context)]:
        cursor.execute("UPDATE Users SET statement_bank_fails = 0 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    r_statement_worker_operative(update, context)
    return CHOOSE_STATEMENT_WORKER_OPERATIVE


def r_statement_worker_operative(update, context):
    chat_id = update.message.chat_id
    buttons = [
        [FULLY_AGREE[language(context)]],
        [MOSTLY_AGREE[language(context)]],
        [MOSTLY_DISAGREE[language(context)]],
        [FULLY_DISAGREE[language(context)]],
        [HARD_TO_ANSWER[language(context)]]
    ]
    context.bot.send_message(chat_id=chat_id,
                             text=statements_txt[language(context)].format(ST_WORKER_OPERATIVE[language(context)]),
                             reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                             parse_mode='HTML')


def get_statement_worker_operative(update, context):
    text = update.message.text
    if text == FULLY_AGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_worker_operative = 5 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == MOSTLY_AGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_worker_operative = 4 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == MOSTLY_DISAGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_worker_operative = 3 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == FULLY_DISAGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_worker_operative = 2 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == HARD_TO_ANSWER[language(context)]:
        cursor.execute("UPDATE Users SET statement_worker_operative = 0 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    r_statement_bank_advantage(update, context)
    return CHOOSE_STATEMENT_BANK_ADVANTAGE


def r_statement_bank_advantage(update, context):
    chat_id = update.message.chat_id
    buttons = [
        [FULLY_AGREE[language(context)]],
        [MOSTLY_AGREE[language(context)]],
        [MOSTLY_DISAGREE[language(context)]],
        [FULLY_DISAGREE[language(context)]],
        [HARD_TO_ANSWER[language(context)]]
    ]
    context.bot.send_message(chat_id=chat_id,
                             text=statements_txt[language(context)].format(ST_BANK_ADV[language(context)]),
                             reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                             parse_mode='HTML')


def get_statement_bank_advantage(update, context):
    text = update.message.text
    if text == FULLY_AGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_bank_advantage = 5 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == MOSTLY_AGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_bank_advantage = 4 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == MOSTLY_DISAGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_bank_advantage = 3 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == FULLY_DISAGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_bank_advantage = 2 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == HARD_TO_ANSWER[language(context)]:
        cursor.execute("UPDATE Users SET statement_bank_advantage = 0 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    r_statement_commission(update, context)
    return CHOOSE_STATEMENT_COMISSION


def r_statement_commission(update, context):
    chat_id = update.message.chat_id
    buttons = [
        [FULLY_AGREE[language(context)]],
        [MOSTLY_AGREE[language(context)]],
        [MOSTLY_DISAGREE[language(context)]],
        [FULLY_DISAGREE[language(context)]],
        [HARD_TO_ANSWER[language(context)]]
    ]
    context.bot.send_message(chat_id=chat_id,
                             text=statements_txt[language(context)].format(ST_COMMISSION[language(context)]),
                             reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                             parse_mode='HTML')


def get_statement_commission(update, context):
    text = update.message.text
    if text == FULLY_AGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_commission = 5 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == MOSTLY_AGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_commission = 4 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == MOSTLY_DISAGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_commission = 3 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == FULLY_DISAGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_commission = 2 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == HARD_TO_ANSWER[language(context)]:
        cursor.execute("UPDATE Users SET statement_commission = 0 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    r_statement_wide_range(update, context)
    return CHOOSE_STATEMENT_WIDE_RANGE


def r_statement_wide_range(update, context):
    chat_id = update.message.chat_id
    buttons = [
        [FULLY_AGREE[language(context)]],
        [MOSTLY_AGREE[language(context)]],
        [MOSTLY_DISAGREE[language(context)]],
        [FULLY_DISAGREE[language(context)]],
        [HARD_TO_ANSWER[language(context)]]
    ]
    context.bot.send_message(chat_id=chat_id,
                             text=statements_txt[language(context)].format(ST_WIDE_RANGE[language(context)]),
                             reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                             parse_mode='HTML')


def get_statement_wide_range(update, context):
    text = update.message.text
    if text == FULLY_AGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_wide_range = 5 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == MOSTLY_AGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_wide_range = 4 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == MOSTLY_DISAGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_wide_range = 3 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == FULLY_DISAGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_wide_range = 2 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == HARD_TO_ANSWER[language(context)]:
        cursor.execute("UPDATE Users SET statement_wide_range = 0 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    r_statement_credit_get(update, context)
    return CHOOSE_STATEMENT_CREDIT_GET


def r_statement_credit_get(update, context):
    chat_id = update.message.chat_id
    buttons = [
        [FULLY_AGREE[language(context)]],
        [MOSTLY_AGREE[language(context)]],
        [MOSTLY_DISAGREE[language(context)]],
        [FULLY_DISAGREE[language(context)]],
        [HARD_TO_ANSWER[language(context)]]
    ]
    context.bot.send_message(chat_id=chat_id,
                             text=statements_txt[language(context)].format(ST_CREDIT_GET[language(context)]),
                             reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                             parse_mode='HTML')


def get_statement_credit_get(update, context):
    text = update.message.text
    if text == FULLY_AGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_credit_get = 5 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == MOSTLY_AGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_credit_get = 4 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == MOSTLY_DISAGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_credit_get = 3 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == FULLY_DISAGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_credit_get = 2 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == HARD_TO_ANSWER[language(context)]:
        cursor.execute("UPDATE Users SET statement_credit_get = 0 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    r_statement_appearance(update, context)
    return CHOOSE_STATEMENT_APPEREANCE


def r_statement_appearance(update, context):
    chat_id = update.message.chat_id
    buttons = [
        [FULLY_AGREE[language(context)]],
        [MOSTLY_AGREE[language(context)]],
        [MOSTLY_DISAGREE[language(context)]],
        [FULLY_DISAGREE[language(context)]],
        [HARD_TO_ANSWER[language(context)]]
    ]
    context.bot.send_message(chat_id=chat_id,
                             text=statements_txt[language(context)].format(ST_APPCE[language(context)]),
                             reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                             parse_mode='HTML')


def get_statement_appearance(update, context):
    text = update.message.text
    if text == FULLY_AGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_appearance = 5 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == MOSTLY_AGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_appearance = 4 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == MOSTLY_DISAGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_appearance = 3 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == FULLY_DISAGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_appearance = 2 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == HARD_TO_ANSWER[language(context)]:
        cursor.execute("UPDATE Users SET statement_appearance = 0 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    r_statement_good_pr(update, context)
    return CHOOSE_STATEMENT_GOOD_PR


def r_statement_good_pr(update, context):
    chat_id = update.message.chat_id
    buttons = [
        [FULLY_AGREE[language(context)]],
        [MOSTLY_AGREE[language(context)]],
        [MOSTLY_DISAGREE[language(context)]],
        [FULLY_DISAGREE[language(context)]],
        [HARD_TO_ANSWER[language(context)]]
    ]
    context.bot.send_message(chat_id=chat_id,
                             text=statements_txt[language(context)].format(ST_GOOD_PR[language(context)]),
                             reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                             parse_mode='HTML')


def get_statement_good_pr(update, context):
    text = update.message.text
    user = context.user_data['identity']
    if user == NATURAL_PERSON[language(context)]:
        if text == FULLY_AGREE[language(context)]:
            cursor.execute("UPDATE Users SET statement_good_pr = 5 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == MOSTLY_AGREE[language(context)]:
            cursor.execute("UPDATE Users SET statement_good_pr = 4 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == MOSTLY_DISAGREE[language(context)]:
            cursor.execute("UPDATE Users SET statement_good_pr = 3 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == FULLY_DISAGREE[language(context)]:
            cursor.execute("UPDATE Users SET statement_good_pr = 2 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == HARD_TO_ANSWER[language(context)]:
            cursor.execute("UPDATE Users SET statement_good_pr = 0 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        r_statement_mobile_app(update, context)
        return CHOOSE_STATEMENT_MOBILE_APP
    else:
        if text == FULLY_AGREE[language(context)]:
            cursor.execute("UPDATE Users SET statement_good_pr = 5 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == MOSTLY_AGREE[language(context)]:
            cursor.execute("UPDATE Users SET statement_good_pr = 4 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == MOSTLY_DISAGREE[language(context)]:
            cursor.execute("UPDATE Users SET statement_good_pr = 3 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == FULLY_DISAGREE[language(context)]:
            cursor.execute("UPDATE Users SET statement_good_pr = 2 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        elif text == HARD_TO_ANSWER[language(context)]:
            cursor.execute("UPDATE Users SET statement_good_pr = 0 WHERE id = '{}'".format(my_id(context)))
            conn.commit()
        r_like_or_not(update, context)
        return LIKE_OR_NOT


def r_statement_mobile_app(update, context):
    chat_id = update.message.chat_id
    buttons = [
        [FULLY_AGREE[language(context)]],
        [MOSTLY_AGREE[language(context)]],
        [MOSTLY_DISAGREE[language(context)]],
        [FULLY_DISAGREE[language(context)]],
        [HARD_TO_ANSWER[language(context)]]
    ]
    context.bot.send_message(chat_id=chat_id,
                             text=statements_txt[language(context)].format(ST_MOBILE[language(context)]),
                             reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                             parse_mode='HTML')


def get_statement_mobile_app(update, context):
    text = update.message.text
    if text == FULLY_AGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_mobile_app = 5 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == MOSTLY_AGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_mobile_app = 4 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == MOSTLY_DISAGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_mobile_app = 3 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == FULLY_DISAGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_mobile_app = 2 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == HARD_TO_ANSWER[language(context)]:
        cursor.execute("UPDATE Users SET statement_mobile_app = 0 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    r_statement_atm(update, context)
    return CHOOSE_STATEMENT_ATM


def r_statement_atm(update, context):
    chat_id = update.message.chat_id
    buttons = [
        [FULLY_AGREE[language(context)]],
        [MOSTLY_AGREE[language(context)]],
        [MOSTLY_DISAGREE[language(context)]],
        [FULLY_DISAGREE[language(context)]],
        [HARD_TO_ANSWER[language(context)]]
    ]
    context.bot.send_message(chat_id=chat_id,
                             text=statements_txt[language(context)].format(ST_ATM[language(context)]),
                             reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                             parse_mode='HTML')


def get_statement_atm(update, context):
    text = update.message.text
    if text == FULLY_AGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_atm = 5 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == MOSTLY_AGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_atm = 4 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == MOSTLY_DISAGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_atm = 3 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == FULLY_DISAGREE[language(context)]:
        cursor.execute("UPDATE Users SET statement_atm = 2 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    elif text == HARD_TO_ANSWER[language(context)]:
        cursor.execute("UPDATE Users SET statement_atm = 0 WHERE id = '{}'".format(my_id(context)))
        conn.commit()
    r_like_or_not(update, context)
    return LIKE_OR_NOT


def r_like_or_not(update, context):
    chat_id = update.message.chat_id
    buttons = [
        [LIKE[language(context)]],
        [HARD_TO_ANSWER[language(context)]],
        [DONT_LIKE[language(context)]]
    ]
    context.bot.send_message(chat_id=chat_id,
                             text=like_or_not_txt[language(context)],
                             reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                             parse_mode='HTML')


def get_like_or_not(update, context):
    text = update.message.text
    chat_id = update.message.chat_id
    if text == LIKE[language(context)] or text == HARD_TO_ANSWER[language(context)]:
        if text == LIKE[language(context)]:
            cursor.execute("""UPDATE Users SET opinion_like = 1, opinion_hard_to_answer = 0
                           WHERE id = '{}'""".format(context.user_data['id']))
            conn.commit()
            comments(update, context)
            return COMMENTS
        else:
            cursor.execute("""UPDATE Users SET opinion_like = 0, opinion_hard_to_answer = 1
                           WHERE id = '{}'""".format(context.user_data['id']))
            conn.commit()
            comments(update, context)
            return COMMENTS
    elif text == DONT_LIKE[language(context)]:
        buttons = [
            [PREVIOUS[language(context)]]
        ]
        context.bot.send_message(chat_id=chat_id,
                                 text=dont_like_txt[language(context)],
                                 reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
                                 parse_mode='HTML')
        return LON_STATE
    elif text == PREVIOUS[language(context)]:
        r_like_or_not(update, context)
        return LIKE_OR_NOT


def get_dont_like_msg(update, context):
    text = update.message.text
    user = context.user_data['id']
    cursor.execute("UPDATE Users SET opinion_dont_like = '{}' WHERE id = '{}'".format(text, user))
    conn.commit()
    comments(update, context)
    return COMMENTS


def comments(update, context):
    chat_id = update.message.chat_id
    button = [
        [NO_COMMENTS_BUTTON[language(context)]]
    ]
    context.bot.send_message(chat_id=chat_id,
                             text=comment_txt[language(context)],
                             reply_markup=ReplyKeyboardMarkup(button, resize_keyboard=True),
                             parse_mode='HTML')


def get_comment(update, context):
    text = update.message.text
    cursor.execute("UPDATE Users SET comments = '{}' WHERE id = '{}'".format(text, context.user_data['id']))
    conn.commit()
    finish(update, context)
    return ConversationHandler.END


def finish(update, context):
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id,
                             text=thankyou_txt[language(context)],
                             reply_markup=ReplyKeyboardRemove(),
                             parse_mode='HTML')
    return ConversationHandler.END


def main():
    updater = Updater(token=API_TOKEN, workers=100)
    dispatcher = updater.dispatcher

    conversation = ConversationHandler(
        entry_points=[
            CommandHandler('start', start, run_async=True)
        ],
        states={
            LANGUAGE: [
                CallbackQueryHandler(greeting, pattern='ru'),
                CallbackQueryHandler(greeting, pattern='uz')
            ],
            IDENTITY: [
                MessageHandler(Filters.regex(START_SURVEY['uz']) |
                               Filters.regex(START_SURVEY['ru']), identity)
            ],
            REGION: [
                MessageHandler(Filters.regex(NATURAL_PERSON['uz']) |
                               Filters.regex(NATURAL_PERSON['ru']), region),
                MessageHandler(Filters.regex(ENTITY['uz']) |
                               Filters.regex(ENTITY['ru']), region),
                MessageHandler(Filters.regex(INDIVIDUAL_ENTPRNR['uz']) |
                               Filters.regex(INDIVIDUAL_ENTPRNR['ru']), region)
            ],
            CHOOSE_REGION_STATE: [
                MessageHandler(Filters.regex(ANDIJAN['uz']) |
                               Filters.regex(ANDIJAN['ru']), andijan_region),
                MessageHandler(Filters.regex(BUKHARA['uz']) |
                               Filters.regex(BUKHARA['ru']), bukhara_region),
                MessageHandler(Filters.regex(DJIZAK['uz']) |
                               Filters.regex(DJIZAK['ru']), djizak_region),
                MessageHandler(Filters.regex(KASHKADARYA['uz']) |
                               Filters.regex(KASHKADARYA['ru']), kashkadarya_region),
                MessageHandler(Filters.regex(KARAKALPAKSTAN['uz']) |
                               Filters.regex(KARAKALPAKSTAN['ru']), karakalpakstan_region),
                MessageHandler(Filters.regex(NAVOI['uz']) |
                               Filters.regex(NAVOI['ru']), navoi_region),
                MessageHandler(Filters.regex(NAMANGAN['uz']) |
                               Filters.regex(NAMANGAN['ru']), namangan_region),
                MessageHandler(Filters.regex(SAMARKAND['uz']) |
                               Filters.regex(SAMARKAND['ru']), samarkand_region),
                MessageHandler(Filters.regex(SURKHANDARYA['uz']) |
                               Filters.regex(SURKHANDARYA['ru']), surkhandarya_region),
                MessageHandler(Filters.regex(SIRDARYA['uz']) |
                               Filters.regex(SIRDARYA['ru']), sirdarya_region),
                MessageHandler(Filters.regex(TASHKENT_REGION['uz']) |
                               Filters.regex(TASHKENT_REGION['ru']), tashkent_region),
                MessageHandler(Filters.regex(TASHKENT['uz']) |
                               Filters.regex(TASHKENT['ru']), tashkent_city),
                MessageHandler(Filters.regex(FERGANA['uz']) |
                               Filters.regex(FERGANA['ru']), fergana_region),
                MessageHandler(Filters.regex(KHOREZM['uz']) |
                               Filters.regex(KHOREZM['ru']), khorezm_region),
            ],
            REASON: [
                MessageHandler(Filters.regex(AGROBANK['uz']) |
                               Filters.regex(AGROBANK['ru']), reasons),
                MessageHandler(Filters.regex(ASIA_ALLIANCE_BANK['uz']) |
                               Filters.regex(ASIA_ALLIANCE_BANK['ru']), reasons),
                MessageHandler(Filters.regex(ALOQABANK['uz']) |
                               Filters.regex(ALOQABANK['ru']), reasons),
                MessageHandler(Filters.regex(ANORBANK['uz']) |
                               Filters.regex(ANORBANK['ru']), reasons),
                MessageHandler(Filters.regex(ASAKABANK['uz']) |
                               Filters.regex(ASAKABANK['ru']), reasons),
                MessageHandler(Filters.regex(DAVRBANK['uz']) |
                               Filters.regex(DAVRBANK['ru']), reasons),
                MessageHandler(Filters.regex(ZIRAATBANK['uz']) |
                               Filters.regex(ZIRAATBANK['ru']), reasons),
                MessageHandler(Filters.regex(INFINBANK['uz']) |
                               Filters.regex(INFINBANK['ru']), reasons),
                MessageHandler(Filters.regex(IPAKYULIBANK['uz']) |
                               Filters.regex(IPAKYULIBANK['ru']), reasons),
                MessageHandler(Filters.regex(IPOTEKABANK['uz']) |
                               Filters.regex(IPOTEKABANK['ru']), reasons),
                MessageHandler(Filters.regex(KAPITALBANK['uz']) |
                               Filters.regex(KAPITALBANK['ru']), reasons),
                MessageHandler(Filters.regex(QQB['uz']) |
                               Filters.regex(QQB['ru']), reasons),
                MessageHandler(Filters.regex(MADADINVESTBANK['uz']) |
                               Filters.regex(MADADINVESTBANK['ru']), reasons),
                MessageHandler(Filters.regex(MIKROKREDITBANK['uz']) |
                               Filters.regex(MIKROKREDITBANK['ru']), reasons),
                MessageHandler(Filters.regex(OFB['uz']) |
                               Filters.regex(OFB['ru']), reasons),
                MessageHandler(Filters.regex(POYTAXTBANK['uz']) |
                               Filters.regex(POYTAXTBANK['ru']), reasons),
                MessageHandler(Filters.regex(RAVNAQBANK['uz']) |
                               Filters.regex(RAVNAQBANK['ru']), reasons),
                MessageHandler(Filters.regex(SAVDOGARBANK['uz']) |
                               Filters.regex(SAVDOGARBANK['ru']), reasons),
                MessageHandler(Filters.regex(TENGEBANK['uz']) |
                               Filters.regex(TENGEBANK['ru']), reasons),
                MessageHandler(Filters.regex(TBCBANK['uz']) |
                               Filters.regex(TBCBANK['ru']), reasons),
                MessageHandler(Filters.regex(TRASTBANK['uz']) |
                               Filters.regex(TRASTBANK['ru']), reasons),
                MessageHandler(Filters.regex(TURKISTONBANK['uz']) |
                               Filters.regex(TURKISTONBANK['ru']), reasons),
                MessageHandler(Filters.regex(TURONBANK['uz']) |
                               Filters.regex(TURONBANK['ru']), reasons),
                MessageHandler(Filters.regex(UNIVERSALBANK['uz']) |
                               Filters.regex(UNIVERSALBANK['ru']), reasons),
                MessageHandler(Filters.regex(UZAGROBANK['uz']) |
                               Filters.regex(UZAGROBANK['ru']), reasons),
                MessageHandler(Filters.regex(UZKDB['uz']) |
                               Filters.regex(UZKDB['ru']), reasons),
                MessageHandler(Filters.regex(UZMILLIYBANK['uz']) |
                               Filters.regex(UZMILLIYBANK['ru']), reasons),
                MessageHandler(Filters.regex(UZSANOATQURILISHBANK['uz']) |
                               Filters.regex(UZSANOATQURILISHBANK['ru']), reasons),
                MessageHandler(Filters.regex(HITECHBANK['uz']) |
                               Filters.regex(HITECHBANK['ru']), reasons),
                MessageHandler(Filters.regex(XALQBANKI['uz']) |
                               Filters.regex(XALQBANKI['ru']), reasons),
                MessageHandler(Filters.regex(HAMKORBANK['uz']) |
                               Filters.regex(HAMKORBANK['ru']), reasons),
                MessageHandler(Filters.regex(ERONSODEROTBANK['uz']) |
                               Filters.regex(ERONSODEROTBANK['ru']), reasons)
            ],
            REASON_EDIT_STATE: [
                MessageHandler(Filters.regex(REASON_RECOMMENDATION['uz']) |
                               Filters.regex(REASON_RECOMMENDATION['ru']), reason_edit),
                MessageHandler(Filters.regex(REASON_SERVICE_CONDITIONS['uz']) |
                               Filters.regex(REASON_SERVICE_CONDITIONS['ru']), reason_edit),
                MessageHandler(Filters.regex(REASON_QUALITY_SERVICE['uz']) |
                               Filters.regex(REASON_QUALITY_SERVICE['ru']), reason_edit),
                MessageHandler(Filters.regex(REASON_CREDIT_AVAILABILITY['uz']) |
                               Filters.regex(REASON_CREDIT_AVAILABILITY['ru']), reason_edit),
                MessageHandler(Filters.regex(REASON_BANK_POPULARITY['uz']) |
                               Filters.regex(REASON_BANK_POPULARITY['ru']), reason_edit),
                MessageHandler(Filters.regex(REASON_UNDERSTANDABLE_CONDITIONS['uz']) |
                               Filters.regex(REASON_UNDERSTANDABLE_CONDITIONS['ru']), reason_edit),
                MessageHandler(Filters.regex(REASON_RELIABLE_BANK['uz']) |
                               Filters.regex(REASON_RELIABLE_BANK['ru']), reason_edit),
                MessageHandler(Filters.regex(REASON_BANK_OPERATIVES['uz']) |
                               Filters.regex(REASON_BANK_OPERATIVES['ru']), reason_edit),
                MessageHandler(Filters.regex(REASON_WIDE_RANGE['uz']) |
                               Filters.regex(REASON_WIDE_RANGE['ru']), reason_edit),
                MessageHandler(Filters.regex(REASON_LOCATION['uz']) |
                               Filters.regex(REASON_LOCATION['ru']), reason_edit),
                MessageHandler(Filters.regex(REASON_REMOTE['uz']) |
                               Filters.regex(REASON_REMOTE['ru']), reason_edit),
                MessageHandler(Filters.regex(REASON_OTHER['uz']) |
                               Filters.regex(REASON_OTHER['ru']), reason_edit_other),
                MessageHandler(Filters.regex(CONTINUE['uz']) |
                               Filters.regex(CONTINUE['ru']), save_info)
            ],
            REO_STATE: [
                MessageHandler(Filters.regex(PREVIOUS['uz']) |
                               Filters.regex(PREVIOUS['ru']), reason_edit),
                MessageHandler(Filters.text, get_reo)
            ],
            FREQUENCY: [
                MessageHandler(Filters.regex(EVERYDAY['uz']) |
                               Filters.regex(EVERYDAY['ru']), service),
                MessageHandler(Filters.regex(ONCE_A_WEEK['uz']) |
                               Filters.regex(ONCE_A_WEEK['ru']), service),
                MessageHandler(Filters.regex(ONCE_A_MONTH['uz']) |
                               Filters.regex(ONCE_A_MONTH['ru']), service),
                MessageHandler(Filters.regex(DONT_GO['uz']) |
                               Filters.regex(DONT_GO['ru']), service),
                MessageHandler(Filters.regex(FREQ_OTHER['uz']) |
                               Filters.regex(FREQ_OTHER['ru']), freq_other)
            ],
            FREQ_OTHER_STATE: [
                MessageHandler(Filters.regex(PREVIOUS['uz']) |
                               Filters.regex(PREVIOUS['ru']), frequency),
                MessageHandler(Filters.text, get_freq_other)
            ],
            SERVICE_STATE: [
                MessageHandler(Filters.regex(CREDIT['uz']) |
                               Filters.regex(CREDIT['ru']), service_edit),
                MessageHandler(Filters.regex(DEPOSIT['uz']) |
                               Filters.regex(DEPOSIT['ru']), service_edit),
                MessageHandler(Filters.regex(CARD['uz']) |
                               Filters.regex(CARD['ru']), service_edit),
                MessageHandler(Filters.regex(PAYMENT['uz']) |
                               Filters.regex(PAYMENT['ru']), service_edit),
                MessageHandler(Filters.regex(EXCHANGE['uz']) |
                               Filters.regex(EXCHANGE['ru']), service_edit),
                MessageHandler(Filters.regex(TRANSFER['uz']) |
                               Filters.regex(TRANSFER['ru']), service_edit),
                MessageHandler(Filters.regex(WITHDRAWAL['uz']) |
                               Filters.regex(WITHDRAWAL['ru']), service_edit),
                MessageHandler(Filters.regex(CHECKING_ACC['uz']) |
                               Filters.regex(CHECKING_ACC['ru']), service_edit),
                MessageHandler(Filters.regex(CONSULTING['uz']) |
                               Filters.regex(CONSULTING['ru']), service_edit),
                MessageHandler(Filters.regex(CURRENCY_OP['uz']) |
                               Filters.regex(CURRENCY_OP['ru']), service_edit),
                MessageHandler(Filters.regex(INTERNET_BANK['uz']) |
                               Filters.regex(INTERNET_BANK['ru']), service_edit),
                MessageHandler(Filters.regex(SERVICE_OTHER['uz']) |
                               Filters.regex(SERVICE_OTHER['ru']), service_edit_other),
                MessageHandler(Filters.regex(CONTINUE['uz']) |
                               Filters.regex(CONTINUE['ru']), save_services_info)

            ],
            SERVICE_EDIT_STATE: [
                MessageHandler(Filters.regex(PREVIOUS['uz']) |
                               Filters.regex(PREVIOUS['ru']), service_edit),
                MessageHandler(Filters.text, get_service_other)
            ],
            RATING_SERVICES_CREDIT: [
                MessageHandler(Filters.regex(GOOD['uz']) |
                               Filters.regex(GOOD['ru']), get_credit_rating),
                MessageHandler(Filters.regex(SATISFACTORY['uz']) |
                               Filters.regex(SATISFACTORY['ru']), get_credit_rating),
                MessageHandler(Filters.regex(DISSATISFACTORY['uz']) |
                               Filters.regex(DISSATISFACTORY['ru']), get_credit_rating),
                MessageHandler(Filters.regex(BAD['uz']) |
                               Filters.regex(BAD['ru']), get_credit_rating),
                MessageHandler(Filters.regex(DONT_KNOW['uz']) |
                               Filters.regex(DONT_KNOW['ru']), get_credit_rating)
            ],
            RATING_SERVICES_DEPOSIT: [
                MessageHandler(Filters.regex(GOOD['uz']) |
                               Filters.regex(GOOD['ru']), get_deposit_rating),
                MessageHandler(Filters.regex(SATISFACTORY['uz']) |
                               Filters.regex(SATISFACTORY['ru']), get_deposit_rating),
                MessageHandler(Filters.regex(DISSATISFACTORY['uz']) |
                               Filters.regex(DISSATISFACTORY['ru']), get_deposit_rating),
                MessageHandler(Filters.regex(BAD['uz']) |
                               Filters.regex(BAD['ru']), get_deposit_rating),
                MessageHandler(Filters.regex(DONT_KNOW['uz']) |
                               Filters.regex(DONT_KNOW['ru']), get_deposit_rating)
            ],
            RATING_SERVICES_CARD: [
                MessageHandler(Filters.regex(GOOD['uz']) |
                               Filters.regex(GOOD['ru']), get_card_rating),
                MessageHandler(Filters.regex(SATISFACTORY['uz']) |
                               Filters.regex(SATISFACTORY['ru']), get_card_rating),
                MessageHandler(Filters.regex(DISSATISFACTORY['uz']) |
                               Filters.regex(DISSATISFACTORY['ru']), get_card_rating),
                MessageHandler(Filters.regex(BAD['uz']) |
                               Filters.regex(BAD['ru']), get_card_rating),
                MessageHandler(Filters.regex(DONT_KNOW['uz']) |
                               Filters.regex(DONT_KNOW['ru']), get_card_rating)
            ],
            RATING_SERVICES_PAYMENT: [
                MessageHandler(Filters.regex(GOOD['uz']) |
                               Filters.regex(GOOD['ru']), get_payment_rating),
                MessageHandler(Filters.regex(SATISFACTORY['uz']) |
                               Filters.regex(SATISFACTORY['ru']), get_payment_rating),
                MessageHandler(Filters.regex(DISSATISFACTORY['uz']) |
                               Filters.regex(DISSATISFACTORY['ru']), get_payment_rating),
                MessageHandler(Filters.regex(BAD['uz']) |
                               Filters.regex(BAD['ru']), get_payment_rating),
                MessageHandler(Filters.regex(DONT_KNOW['uz']) |
                               Filters.regex(DONT_KNOW['ru']), get_payment_rating)
            ],
            RATING_SERVICES_EXCHANGE: [
                MessageHandler(Filters.regex(GOOD['uz']) |
                               Filters.regex(GOOD['ru']), get_exchange_rating),
                MessageHandler(Filters.regex(SATISFACTORY['uz']) |
                               Filters.regex(SATISFACTORY['ru']), get_exchange_rating),
                MessageHandler(Filters.regex(DISSATISFACTORY['uz']) |
                               Filters.regex(DISSATISFACTORY['ru']), get_exchange_rating),
                MessageHandler(Filters.regex(BAD['uz']) |
                               Filters.regex(BAD['ru']), get_exchange_rating),
                MessageHandler(Filters.regex(DONT_KNOW['uz']) |
                               Filters.regex(DONT_KNOW['ru']), get_exchange_rating)
            ],
            RATING_SERVICES_TRANSFER: [
                MessageHandler(Filters.regex(GOOD['uz']) |
                               Filters.regex(GOOD['ru']), get_transfer_rating),
                MessageHandler(Filters.regex(SATISFACTORY['uz']) |
                               Filters.regex(SATISFACTORY['ru']), get_transfer_rating),
                MessageHandler(Filters.regex(DISSATISFACTORY['uz']) |
                               Filters.regex(DISSATISFACTORY['ru']), get_transfer_rating),
                MessageHandler(Filters.regex(BAD['uz']) |
                               Filters.regex(BAD['ru']), get_transfer_rating),
                MessageHandler(Filters.regex(DONT_KNOW['uz']) |
                               Filters.regex(DONT_KNOW['ru']), get_transfer_rating)
            ],
            RATING_SERVICES_WITHDRAWAL: [
                MessageHandler(Filters.regex(GOOD['uz']) |
                               Filters.regex(GOOD['ru']), get_withdrawal_rating),
                MessageHandler(Filters.regex(SATISFACTORY['uz']) |
                               Filters.regex(SATISFACTORY['ru']), get_withdrawal_rating),
                MessageHandler(Filters.regex(DISSATISFACTORY['uz']) |
                               Filters.regex(DISSATISFACTORY['ru']), get_withdrawal_rating),
                MessageHandler(Filters.regex(BAD['uz']) |
                               Filters.regex(BAD['ru']), get_withdrawal_rating),
                MessageHandler(Filters.regex(DONT_KNOW['uz']) |
                               Filters.regex(DONT_KNOW['ru']), get_withdrawal_rating)
            ],
            RATING_PARAMETERS_DEADLINE: [
                MessageHandler(Filters.regex(FULLY_DISSATISFIED['uz']) |
                               Filters.regex(FULLY_DISSATISFIED['ru']), p_get_deadline),
                MessageHandler(Filters.regex(DISSATISFIED['uz']) |
                               Filters.regex(DISSATISFIED['ru']), p_get_deadline),
                MessageHandler(Filters.regex(SATISFIED['uz']) |
                               Filters.regex(SATISFIED['ru']), p_get_deadline),
                MessageHandler(Filters.regex(FULLY_SATISFIED['uz']) |
                               Filters.regex(FULLY_SATISFIED['ru']), p_get_deadline),
                MessageHandler(Filters.regex(HARD_TO_ANSWER['uz']) |
                               Filters.regex(HARD_TO_ANSWER['ru']), p_get_deadline)
            ],
            RATING_PARAMETERS_FEEDBACK: [
                MessageHandler(Filters.regex(FULLY_DISSATISFIED['uz']) |
                               Filters.regex(FULLY_DISSATISFIED['ru']), p_get_feedback),
                MessageHandler(Filters.regex(DISSATISFIED['uz']) |
                               Filters.regex(DISSATISFIED['ru']), p_get_feedback),
                MessageHandler(Filters.regex(SATISFIED['uz']) |
                               Filters.regex(SATISFIED['ru']), p_get_feedback),
                MessageHandler(Filters.regex(FULLY_SATISFIED['uz']) |
                               Filters.regex(FULLY_SATISFIED['ru']), p_get_feedback),
                MessageHandler(Filters.regex(HARD_TO_ANSWER['uz']) |
                               Filters.regex(HARD_TO_ANSWER['ru']), p_get_feedback)
            ],
            RATING_PARAMETERS_INFO_AVAILABLE: [
                MessageHandler(Filters.regex(FULLY_DISSATISFIED['uz']) |
                               Filters.regex(FULLY_DISSATISFIED['ru']), p_get_info_available),
                MessageHandler(Filters.regex(DISSATISFIED['uz']) |
                               Filters.regex(DISSATISFIED['ru']), p_get_info_available),
                MessageHandler(Filters.regex(SATISFIED['uz']) |
                               Filters.regex(SATISFIED['ru']), p_get_info_available),
                MessageHandler(Filters.regex(FULLY_SATISFIED['uz']) |
                               Filters.regex(FULLY_SATISFIED['ru']), p_get_info_available),
                MessageHandler(Filters.regex(HARD_TO_ANSWER['uz']) |
                               Filters.regex(HARD_TO_ANSWER['ru']), p_get_info_available)
            ],
            RATING_PARAMETERS_PERSONAL: [
                MessageHandler(Filters.regex(FULLY_DISSATISFIED['uz']) |
                               Filters.regex(FULLY_DISSATISFIED['ru']), p_get_personal),
                MessageHandler(Filters.regex(DISSATISFIED['uz']) |
                               Filters.regex(DISSATISFIED['ru']), p_get_personal),
                MessageHandler(Filters.regex(SATISFIED['uz']) |
                               Filters.regex(SATISFIED['ru']), p_get_personal),
                MessageHandler(Filters.regex(FULLY_SATISFIED['uz']) |
                               Filters.regex(FULLY_SATISFIED['ru']), p_get_personal),
                MessageHandler(Filters.regex(HARD_TO_ANSWER['uz']) |
                               Filters.regex(HARD_TO_ANSWER['ru']), p_get_personal)
            ],
            RATE_WORKERS_INFORMED: [
                MessageHandler(Filters.regex(GOOD['uz']) |
                               Filters.regex(GOOD['ru']), get_workers_informed),
                MessageHandler(Filters.regex(SATISFACTORY['uz']) |
                               Filters.regex(SATISFACTORY['ru']), get_workers_informed),
                MessageHandler(Filters.regex(DISSATISFACTORY['uz']) |
                               Filters.regex(DISSATISFACTORY['ru']), get_workers_informed),
                MessageHandler(Filters.regex(BAD['uz']) |
                               Filters.regex(BAD['ru']), get_workers_informed),
                MessageHandler(Filters.regex(HARD_TO_ANSWER['uz']) |
                               Filters.regex(HARD_TO_ANSWER['ru']), get_workers_informed)
            ],
            RATE_WORKERS_OPERATIVE: [
                MessageHandler(Filters.regex(GOOD['uz']) |
                               Filters.regex(GOOD['ru']), get_workers_operative),
                MessageHandler(Filters.regex(SATISFACTORY['uz']) |
                               Filters.regex(SATISFACTORY['ru']), get_workers_operative),
                MessageHandler(Filters.regex(DISSATISFACTORY['uz']) |
                               Filters.regex(DISSATISFACTORY['ru']), get_workers_operative),
                MessageHandler(Filters.regex(BAD['uz']) |
                               Filters.regex(BAD['ru']), get_workers_operative),
                MessageHandler(Filters.regex(HARD_TO_ANSWER['uz']) |
                               Filters.regex(HARD_TO_ANSWER['ru']), get_workers_operative)
            ],
            RATE_WORKERS_PROFESSIONAL: [
                MessageHandler(Filters.regex(GOOD['uz']) |
                               Filters.regex(GOOD['ru']), get_workers_professional),
                MessageHandler(Filters.regex(SATISFACTORY['uz']) |
                               Filters.regex(SATISFACTORY['ru']), get_workers_professional),
                MessageHandler(Filters.regex(DISSATISFACTORY['uz']) |
                               Filters.regex(DISSATISFACTORY['ru']), get_workers_professional),
                MessageHandler(Filters.regex(BAD['uz']) |
                               Filters.regex(BAD['ru']), get_workers_professional),
                MessageHandler(Filters.regex(HARD_TO_ANSWER['uz']) |
                               Filters.regex(HARD_TO_ANSWER['ru']), get_workers_professional)
            ],
            RATE_WORKERS_POLITE: [
                MessageHandler(Filters.regex(GOOD['uz']) |
                               Filters.regex(GOOD['ru']), get_workers_polite),
                MessageHandler(Filters.regex(SATISFACTORY['uz']) |
                               Filters.regex(SATISFACTORY['ru']), get_workers_polite),
                MessageHandler(Filters.regex(DISSATISFACTORY['uz']) |
                               Filters.regex(DISSATISFACTORY['ru']), get_workers_polite),
                MessageHandler(Filters.regex(BAD['uz']) |
                               Filters.regex(BAD['ru']), get_workers_polite),
                MessageHandler(Filters.regex(HARD_TO_ANSWER['uz']) |
                               Filters.regex(HARD_TO_ANSWER['ru']), get_workers_polite)
            ],
            RATE_WORKERS_READY_HELP: [
                MessageHandler(Filters.regex(GOOD['uz']) |
                               Filters.regex(GOOD['ru']), get_workers_ready_help),
                MessageHandler(Filters.regex(SATISFACTORY['uz']) |
                               Filters.regex(SATISFACTORY['ru']), get_workers_ready_help),
                MessageHandler(Filters.regex(DISSATISFACTORY['uz']) |
                               Filters.regex(DISSATISFACTORY['ru']), get_workers_ready_help),
                MessageHandler(Filters.regex(BAD['uz']) |
                               Filters.regex(BAD['ru']), get_workers_ready_help),
                MessageHandler(Filters.regex(HARD_TO_ANSWER['uz']) |
                               Filters.regex(HARD_TO_ANSWER['ru']), get_workers_ready_help)
            ],
            CHOOSE_STATEMENT_NAVIGATION: [
                MessageHandler(Filters.regex(FULLY_AGREE['uz']) |
                               Filters.regex(FULLY_AGREE['ru']), get_statement_navigation),
                MessageHandler(Filters.regex(MOSTLY_AGREE['uz']) |
                               Filters.regex(MOSTLY_AGREE['ru']), get_statement_navigation),
                MessageHandler(Filters.regex(MOSTLY_DISAGREE['uz']) |
                               Filters.regex(MOSTLY_DISAGREE['ru']), get_statement_navigation),
                MessageHandler(Filters.regex(FULLY_DISAGREE['uz']) |
                               Filters.regex(FULLY_DISAGREE['ru']), get_statement_navigation),
                MessageHandler(Filters.regex(HARD_TO_ANSWER['uz']) |
                               Filters.regex(HARD_TO_ANSWER['ru']), get_statement_navigation)
            ],
            CHOOSE_STATEMENT_RESPONSIBILITY: [
                MessageHandler(Filters.regex(FULLY_AGREE['uz']) |
                               Filters.regex(FULLY_AGREE['ru']), get_statement_responsibility),
                MessageHandler(Filters.regex(MOSTLY_AGREE['uz']) |
                               Filters.regex(MOSTLY_AGREE['ru']), get_statement_responsibility),
                MessageHandler(Filters.regex(MOSTLY_DISAGREE['uz']) |
                               Filters.regex(MOSTLY_DISAGREE['ru']), get_statement_responsibility),
                MessageHandler(Filters.regex(FULLY_DISAGREE['uz']) |
                               Filters.regex(FULLY_DISAGREE['ru']), get_statement_responsibility),
                MessageHandler(Filters.regex(HARD_TO_ANSWER['uz']) |
                               Filters.regex(HARD_TO_ANSWER['ru']), get_statement_responsibility)
            ],
            CHOOSE_STATEMENT_BANK_RESPONSE: [
                MessageHandler(Filters.regex(FULLY_AGREE['uz']) |
                               Filters.regex(FULLY_AGREE['ru']), get_statement_bank_response),
                MessageHandler(Filters.regex(MOSTLY_AGREE['uz']) |
                               Filters.regex(MOSTLY_AGREE['ru']), get_statement_bank_response),
                MessageHandler(Filters.regex(MOSTLY_DISAGREE['uz']) |
                               Filters.regex(MOSTLY_DISAGREE['ru']), get_statement_bank_response),
                MessageHandler(Filters.regex(FULLY_DISAGREE['uz']) |
                               Filters.regex(FULLY_DISAGREE['ru']), get_statement_bank_response),
                MessageHandler(Filters.regex(HARD_TO_ANSWER['uz']) |
                               Filters.regex(HARD_TO_ANSWER['ru']), get_statement_bank_response)
            ],
            CHOOSE_STATEMENT_WORKER_INFO: [
                MessageHandler(Filters.regex(FULLY_AGREE['uz']) |
                               Filters.regex(FULLY_AGREE['ru']), get_statement_worker_info),
                MessageHandler(Filters.regex(MOSTLY_AGREE['uz']) |
                               Filters.regex(MOSTLY_AGREE['ru']), get_statement_worker_info),
                MessageHandler(Filters.regex(MOSTLY_DISAGREE['uz']) |
                               Filters.regex(MOSTLY_DISAGREE['ru']), get_statement_worker_info),
                MessageHandler(Filters.regex(FULLY_DISAGREE['uz']) |
                               Filters.regex(FULLY_DISAGREE['ru']), get_statement_worker_info),
                MessageHandler(Filters.regex(HARD_TO_ANSWER['uz']) |
                               Filters.regex(HARD_TO_ANSWER['ru']), get_statement_worker_info)
            ],
            CHOOSE_STATEMENT_BANK_FAILS: [
                MessageHandler(Filters.regex(FULLY_AGREE['uz']) |
                               Filters.regex(FULLY_AGREE['ru']), get_statement_bank_fails),
                MessageHandler(Filters.regex(MOSTLY_AGREE['uz']) |
                               Filters.regex(MOSTLY_AGREE['ru']), get_statement_bank_fails),
                MessageHandler(Filters.regex(MOSTLY_DISAGREE['uz']) |
                               Filters.regex(MOSTLY_DISAGREE['ru']), get_statement_bank_fails),
                MessageHandler(Filters.regex(FULLY_DISAGREE['uz']) |
                               Filters.regex(FULLY_DISAGREE['ru']), get_statement_bank_fails),
                MessageHandler(Filters.regex(HARD_TO_ANSWER['uz']) |
                               Filters.regex(HARD_TO_ANSWER['ru']), get_statement_bank_fails)
            ],
            CHOOSE_STATEMENT_WORKER_OPERATIVE: [
                MessageHandler(Filters.regex(FULLY_AGREE['uz']) |
                               Filters.regex(FULLY_AGREE['ru']), get_statement_worker_operative),
                MessageHandler(Filters.regex(MOSTLY_AGREE['uz']) |
                               Filters.regex(MOSTLY_AGREE['ru']), get_statement_worker_operative),
                MessageHandler(Filters.regex(MOSTLY_DISAGREE['uz']) |
                               Filters.regex(MOSTLY_DISAGREE['ru']), get_statement_worker_operative),
                MessageHandler(Filters.regex(FULLY_DISAGREE['uz']) |
                               Filters.regex(FULLY_DISAGREE['ru']), get_statement_worker_operative),
                MessageHandler(Filters.regex(HARD_TO_ANSWER['uz']) |
                               Filters.regex(HARD_TO_ANSWER['ru']), get_statement_worker_operative)
            ],
            CHOOSE_STATEMENT_BANK_ADVANTAGE: [
                MessageHandler(Filters.regex(FULLY_AGREE['uz']) |
                               Filters.regex(FULLY_AGREE['ru']), get_statement_bank_advantage),
                MessageHandler(Filters.regex(MOSTLY_AGREE['uz']) |
                               Filters.regex(MOSTLY_AGREE['ru']), get_statement_bank_advantage),
                MessageHandler(Filters.regex(MOSTLY_DISAGREE['uz']) |
                               Filters.regex(MOSTLY_DISAGREE['ru']), get_statement_bank_advantage),
                MessageHandler(Filters.regex(FULLY_DISAGREE['uz']) |
                               Filters.regex(FULLY_DISAGREE['ru']), get_statement_bank_advantage),
                MessageHandler(Filters.regex(HARD_TO_ANSWER['uz']) |
                               Filters.regex(HARD_TO_ANSWER['ru']), get_statement_bank_advantage)
            ],
            CHOOSE_STATEMENT_COMISSION: [
                MessageHandler(Filters.regex(FULLY_AGREE['uz']) |
                               Filters.regex(FULLY_AGREE['ru']), get_statement_commission),
                MessageHandler(Filters.regex(MOSTLY_AGREE['uz']) |
                               Filters.regex(MOSTLY_AGREE['ru']), get_statement_commission),
                MessageHandler(Filters.regex(MOSTLY_DISAGREE['uz']) |
                               Filters.regex(MOSTLY_DISAGREE['ru']), get_statement_commission),
                MessageHandler(Filters.regex(FULLY_DISAGREE['uz']) |
                               Filters.regex(FULLY_DISAGREE['ru']), get_statement_commission),
                MessageHandler(Filters.regex(HARD_TO_ANSWER['uz']) |
                               Filters.regex(HARD_TO_ANSWER['ru']), get_statement_commission)
            ],
            CHOOSE_STATEMENT_WIDE_RANGE: [
                MessageHandler(Filters.regex(FULLY_AGREE['uz']) |
                               Filters.regex(FULLY_AGREE['ru']), get_statement_wide_range),
                MessageHandler(Filters.regex(MOSTLY_AGREE['uz']) |
                               Filters.regex(MOSTLY_AGREE['ru']), get_statement_wide_range),
                MessageHandler(Filters.regex(MOSTLY_DISAGREE['uz']) |
                               Filters.regex(MOSTLY_DISAGREE['ru']), get_statement_wide_range),
                MessageHandler(Filters.regex(FULLY_DISAGREE['uz']) |
                               Filters.regex(FULLY_DISAGREE['ru']), get_statement_wide_range),
                MessageHandler(Filters.regex(HARD_TO_ANSWER['uz']) |
                               Filters.regex(HARD_TO_ANSWER['ru']), get_statement_wide_range)
            ],
            CHOOSE_STATEMENT_CREDIT_GET: [
                MessageHandler(Filters.regex(FULLY_AGREE['uz']) |
                               Filters.regex(FULLY_AGREE['ru']), get_statement_credit_get),
                MessageHandler(Filters.regex(MOSTLY_AGREE['uz']) |
                               Filters.regex(MOSTLY_AGREE['ru']), get_statement_credit_get),
                MessageHandler(Filters.regex(MOSTLY_DISAGREE['uz']) |
                               Filters.regex(MOSTLY_DISAGREE['ru']), get_statement_credit_get),
                MessageHandler(Filters.regex(FULLY_DISAGREE['uz']) |
                               Filters.regex(FULLY_DISAGREE['ru']), get_statement_credit_get),
                MessageHandler(Filters.regex(HARD_TO_ANSWER['uz']) |
                               Filters.regex(HARD_TO_ANSWER['ru']), get_statement_credit_get)
            ],
            CHOOSE_STATEMENT_APPEREANCE: [
                MessageHandler(Filters.regex(FULLY_AGREE['uz']) |
                               Filters.regex(FULLY_AGREE['ru']), get_statement_appearance),
                MessageHandler(Filters.regex(MOSTLY_AGREE['uz']) |
                               Filters.regex(MOSTLY_AGREE['ru']), get_statement_appearance),
                MessageHandler(Filters.regex(MOSTLY_DISAGREE['uz']) |
                               Filters.regex(MOSTLY_DISAGREE['ru']), get_statement_appearance),
                MessageHandler(Filters.regex(FULLY_DISAGREE['uz']) |
                               Filters.regex(FULLY_DISAGREE['ru']), get_statement_appearance),
                MessageHandler(Filters.regex(HARD_TO_ANSWER['uz']) |
                               Filters.regex(HARD_TO_ANSWER['ru']), get_statement_appearance)
            ],
            CHOOSE_STATEMENT_GOOD_PR: [
                MessageHandler(Filters.regex(FULLY_AGREE['uz']) |
                               Filters.regex(FULLY_AGREE['ru']), get_statement_good_pr),
                MessageHandler(Filters.regex(MOSTLY_AGREE['uz']) |
                               Filters.regex(MOSTLY_AGREE['ru']), get_statement_good_pr),
                MessageHandler(Filters.regex(MOSTLY_DISAGREE['uz']) |
                               Filters.regex(MOSTLY_DISAGREE['ru']), get_statement_good_pr),
                MessageHandler(Filters.regex(FULLY_DISAGREE['uz']) |
                               Filters.regex(FULLY_DISAGREE['ru']), get_statement_good_pr),
                MessageHandler(Filters.regex(HARD_TO_ANSWER['uz']) |
                               Filters.regex(HARD_TO_ANSWER['ru']), get_statement_good_pr)
            ],
            CHOOSE_STATEMENT_MOBILE_APP: [
                MessageHandler(Filters.regex(FULLY_AGREE['uz']) |
                               Filters.regex(FULLY_AGREE['ru']), get_statement_mobile_app),
                MessageHandler(Filters.regex(MOSTLY_AGREE['uz']) |
                               Filters.regex(MOSTLY_AGREE['ru']), get_statement_mobile_app),
                MessageHandler(Filters.regex(MOSTLY_DISAGREE['uz']) |
                               Filters.regex(MOSTLY_DISAGREE['ru']), get_statement_mobile_app),
                MessageHandler(Filters.regex(FULLY_DISAGREE['uz']) |
                               Filters.regex(FULLY_DISAGREE['ru']), get_statement_mobile_app),
                MessageHandler(Filters.regex(HARD_TO_ANSWER['uz']) |
                               Filters.regex(HARD_TO_ANSWER['ru']), get_statement_mobile_app)
            ],
            CHOOSE_STATEMENT_ATM: [
                MessageHandler(Filters.regex(FULLY_AGREE['uz']) |
                               Filters.regex(FULLY_AGREE['ru']), get_statement_atm),
                MessageHandler(Filters.regex(MOSTLY_AGREE['uz']) |
                               Filters.regex(MOSTLY_AGREE['ru']), get_statement_atm),
                MessageHandler(Filters.regex(MOSTLY_DISAGREE['uz']) |
                               Filters.regex(MOSTLY_DISAGREE['ru']), get_statement_atm),
                MessageHandler(Filters.regex(FULLY_DISAGREE['uz']) |
                               Filters.regex(FULLY_DISAGREE['ru']), get_statement_atm),
                MessageHandler(Filters.regex(HARD_TO_ANSWER['uz']) |
                               Filters.regex(HARD_TO_ANSWER['ru']), get_statement_atm)
            ],
            LIKE_OR_NOT: [
                MessageHandler(Filters.regex(LIKE['uz']) |
                               Filters.regex(LIKE['ru']), get_like_or_not),
                MessageHandler(Filters.regex(HARD_TO_ANSWER['uz']) |
                               Filters.regex(HARD_TO_ANSWER['ru']), get_like_or_not),
                MessageHandler(Filters.regex(DONT_LIKE['uz']) |
                               Filters.regex(DONT_LIKE['ru']), get_like_or_not)
            ],
            LON_STATE: [
                MessageHandler(Filters.regex(PREVIOUS['uz']) |
                               Filters.regex(PREVIOUS['ru']), get_like_or_not),
                MessageHandler(Filters.text, get_dont_like_msg)
            ],
            COMMENTS: [
                MessageHandler(Filters.regex(NO_COMMENTS_BUTTON['uz']) |
                               Filters.regex(NO_COMMENTS_BUTTON['ru']), finish),
                MessageHandler(Filters.text, get_comment)
            ]
        },
        fallbacks=[
            CommandHandler('start', start)
        ]
    )

    dispatcher.add_handler(conversation)

    try:
        updater.start_polling()
    except Exception as e:
        print(e)
    updater.idle()
