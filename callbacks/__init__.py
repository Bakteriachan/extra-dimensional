import re
import os

from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from telegram.ext import CallbackContext

import locales
import states

def start(update: Update, ctxt: CallbackContext):
    if ctxt.user_data.get('agreement', None) in (None, 'decline'):
        keyboard_text = locales.start_keyboard_text(lang=ctxt.user_data.get('language'))
        inline_keyboard = [
            [
                InlineKeyboardButton(
                    text = keyboard_text.get('accept'),
                    callback_data = 'rules_accept',
                ),
                InlineKeyboardButton(
                    text = keyboard_text.get('decline'),
                    callback_data = 'rules_decline',
                )
            ],
        ]
        update.effective_chat.send_message(
            text= locales.start_text(lang=ctxt.user_data.get('language'),agreement=True),
            reply_markup= InlineKeyboardMarkup(inline_keyboard=inline_keyboard),
        )
        return -1
    else:
        update.effective_chat.send_message(
            text = locales.start_text(lang=ctxt.user_data.get('laguage')),
        )

def process_agreement(update: Update, ctxt: CallbackContext):
    match = re.match(r'rules_(accept|decline)', update.callback_query.data)

    if match is None:
        update.effective_chat.send_message(
            text = locales.error_text(ctxt.user_data.get('language')),
        )
        return -1

    update.effective_message.delete()

    ctxt.user_data['agreement'] = match.group(1)

    if ctxt.user_data.get('agreement') in ('accept',):
        update.effective_chat.send_message(
            text = locales.start_text(lang=ctxt.user_data.get('language')),
        )
        return states.START
    else:
        update.effective_chat.send_message(
            text = locales.agreement_declined(lang=ctxt.user_data.get('language')),
        )
        return -1

def send(update: Update, ctxt: CallbackContext):
    update.effective_chat.send_message(
        text = locales.username_text(lang=ctxt.user_data.get('language')),
    )

    
    return states.USERNAME

def process_username(update: Update, ctxt: CallbackContext):
    ctxt.user_data.setdefault('username', update.effective_message.text)

    update.effective_chat.send_message(
        text= locales.social_media_text(lang=ctxt.user_data.get('language')),
        reply_markup = ReplyKeyboardMarkup(
            keyboard = [
                [
                    locales.omit_step_keyboard_text(lang=ctxt.user_data.get('language')),
                    locales.cancel_step_keyboard_text(lang=ctxt.user_data.get('language')),
                ]
            ],
            resize_keyboard = True,
        )
    )

    return states.SOCIAL_MEDIA

def process_social_media(update: Update, ctxt: CallbackContext):
    if update.effective_message.text not in (locales.omit_step_keyboard_text(lang=ctxt.user_data.get('language')),):
        ctxt.user_data.setdefault('social_media', update.effective_message.text)

    update.effective_chat.send_message(
        text = locales.artwork_comment_text(lang=ctxt.user_data.get('language')),
    )

    return states.ARTWORK_COMMENT

def process_artwork_comment(update: Update, ctxt: CallbackContext):
    if update.effective_message.text not in (locales.omit_step_keyboard_text(lang=ctxt.user_data.get('language'))):
        ctxt.user_data.setdefault('artwork_comment', update.effective_message.text)

    update.effective_chat.send_message(
        text = locales.artwork_content_text(lang='language'),
        reply_markup = ReplyKeyboardMarkup(
            keyboard = [
                [locales.cancel_step_keyboard_text(lang=ctxt.user_data.get('language'))]
            ],
            resize_keyboard= True,
        )
    )

    return states.ARTWORK_CONTENT

def process_artwork_content(update: Update, ctxt: CallbackContext):
    try:
        keyboard_text = locales.send_artwork_for_revision_keyboard_text(lang = ctxt.user_data.get('language'))
        update.effective_message.copy(
            chat_id = update.effective_chat.id,
            caption = locales.build_artwork_caption(
                artwork_data = {
                    'username': ctxt.user_data.get('username'),
                    'social_media': ctxt.user_data.get('social_media'),
                    'artwork_comment': ctxt.user_data.get('artwork_comment'),
                    'name': update.effective_user.first_name,
                    'bot_username': ctxt.bot.username,
                },
                lang = ctxt.user_data.get('language'),
            ),
            reply_markup = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text = keyboard_text.get('send'),
                            callback_data = 'revision_send',
                        )
                    ], [
                        InlineKeyboardButton(
                            text = keyboard_text.get('cancel'),
                            callback_data = 'revision_cancel',
                        ),
                    ],
                ]
            )
        )
    except Exception as e:
        print(e)
        update.effective_chat.send_message(
            text = locales.error_text(lang=ctxt.user_data.get('language')),
            reply_markup = ReplyKeyboardRemove(),
        )
    else:
        ctxt.user_data.pop('username', None)
        ctxt.user_data.pop('social_media', None)
        ctxt.user_data.pop('artwork_comment', None)

def send_to_revision(update: Update, ctxt: CallbackContext):

    match = re.match(r'revision_(send|cancel)', update.callback_query.data)

    if match.group(1) is None:
        update.effective_chat.send_message(
            text = locales.error_text(lang=ctxt.user_data.get('language')),
            reply_markup = ReplyKeyboardRemove(),
        )
        return states.START

    if match.group(1) == 'send':
        update.effective_message.copy(
            chat_id = os.getenv('revisionchat'),
            reply_markup = InlineKeyboardMarkup(
                inline_keyboard = [
                    [
                        InlineKeyboardButton(
                            text = 'Send',
                            callback_data = 'artwork_send',
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text = 'Decline',
                            callback_data = 'artwork_decline',
                        )
                    ],
                ]
            ),
        )

        update.effective_chat.send_message(
            text = locales.artwork_sent_message(lang = ctxt.user_data.get('language')),
        )
    
    update.effective_chat.send_message(
        text = locales.start_text(lang=ctxt.user_data.get('language')),
    )
        
    update.effective_message.delete()
    
    return states.START

def process_artwork(update: Update, ctxt: CallbackContext):
    '''
    act according to the decision of channels' admins
    '''
    match = re.match(r'artwork_(send|decline)', update.callback_query.data)

    if match.group(1) is None:
        update.effective_chat.send_message(
            text = locales.error_text(lang=ctxt.user_data.get('language')),
        )
        return None
    
    if match.group(1) == 'send':
        update.effective_message.copy(
            chat_id = os.getenv('mainchannel'),
            reply_markup = None,
        )

    update.effective_message.delete()
    
    