import re
import os
from uuid import uuid4

from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InputMediaPhoto,
    InputMediaAudio,
    InputMediaVideo,
    InputMediaDocument,
)
from telegram.ext import CallbackContext

import locales
import states
import config

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

    ctxt.user_data.pop('artwork_type', None)
    ctxt.user_data.pop('artworks', None)
    ctxt.user_data.pop('username', None)
    ctxt.user_data.pop('social_media', None)
    ctxt.user_data.pop('artwork_comment', None)

    return states.USERNAME

def process_username(update: Update, ctxt: CallbackContext):
    ctxt.user_data['username'] = update.effective_message.text

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
        ctxt.user_data['social_media'] = update.effective_message.text

    update.effective_chat.send_message(
        text = locales.artwork_comment_text(lang=ctxt.user_data.get('language')),
    )

    return states.ARTWORK_COMMENT

def process_artwork_comment(update: Update, ctxt: CallbackContext):
    if update.effective_message.text not in (locales.omit_step_keyboard_text(lang=ctxt.user_data.get('language'))):
        ctxt.user_data['artwork_comment'] = update.effective_message.text

    update.effective_chat.send_message(
        text = locales.artwork_content_text(lang='language'),
        reply_markup = ReplyKeyboardMarkup(
            keyboard = [
                [
                    locales.cancel_step_keyboard_text(lang=ctxt.user_data.get('language')),
                    locales.confirm_artwork_button_text(lang=ctxt.user_data.get('language')),
                ],
            ],
            resize_keyboard= True,
        ),
        parse_mode = config.PARSE_MODE,
    )

    return states.ARTWORK_CONTENT

def process_artwork_content(update: Update, ctxt: CallbackContext):
    '''
    Process artworks sent by user
    '''
    if update.effective_message.photo:
        if ctxt.user_data.get('artwork_type',None) not in ('photo', None):
            update.effective_chat.send_message(
                text = locales.not_the_expected_artwork(lang=ctxt.user_data.get('language')),
            )
            return None
        else:
            if ctxt.user_data.get('artwork_type', None) is None:
                ctxt.user_data['artwork_type'] = 'photo'
            if ctxt.user_data.get('artworks', None) is None:
                ctxt.user_data['artworks'] = []

            ctxt.user_data['artworks'].append(update.effective_message.photo[0].file_id)

    if update.effective_message.audio:
        if ctxt.user_data.get('artwork_type', None) not in ('audio', None):
            update.effective_chat.send_message(
                text = locales.not_the_expected_artwork(lang=ctxt.user_data.get('language')),
            )
            return None
        else:
            if ctxt.user_data.get('artwork_type', None) is None:
                ctxt.user_data['artwork_type'] = 'audio'
            if ctxt.user_data.get('artworks', None) is None:
                ctxt.user_data['artworks'] = []

            ctxt.user_data['artworks'].append(update.effective_message.audio.file_id)

    if update.effective_message.video:
        if ctxt.user_data.get('artwork_type', None) not in ('video', None):
            update.effective_chat.send_message(
                text = locales.not_the_expected_artwork(lang=ctxt.user_data.get('language')),
            )
            return None
        else:
            if ctxt.user_data.get('artwork_type', None) is None:
                ctxt.user_data['artwork_type'] = 'video'
            if ctxt.user_data.get('artworks', None) is None:
                ctxt.user_data['artworks'] = []

            ctxt.user_data['artworks'].append(update.effective_message.video.file_id)

    if update.effective_message.document:
        if ctxt.user_data.get('artwork_type', None) not in ('document', None):
            update.effective_chat.send_message(
                text = locales.not_the_expected_artwork(lang=ctxt.user_data.get('language')),
            )
            return None
        else:
            if ctxt.user_data.get('artwork_type', None) is None:
                ctxt.user_data['artwork_type'] = 'document'
            if ctxt.user_data.get('artworks', None) is None:
                ctxt.user_data['artworks'] = []
        
            ctxt.user_data['artworks'].append(update.effective_message.document.file_id)

    update.effective_chat.send_message(
        text = locales.artwork_received_text(lang=ctxt.user_data.get('language')),
        parse_mode = config.PARSE_MODE,
    )
    return None

def confirm_artworks(update: Update, ctxt: CallbackContext):
    '''
    User finished sending artworks
    '''
    media_group = []

    if ctxt.user_data.get('artwork_type') in ('photo',):
        MediaType = InputMediaPhoto
    elif ctxt.user_data.get('artwork_type') in ('audio',):
        MediaType = InputMediaPhoto
    elif ctxt.user_data.get('artwork_type') in ('video',):
        MediaType = InputMediaVideo
    elif ctxt.user_data.get('artwork_type') in ('document',):
        MediaType = InputMediaDocument


    for artwork in ctxt.user_data.get('artworks'):
        if len(media_group) == 0:
            media_group.append(MediaType(
                media = artwork,
                caption = locales.build_artwork_caption(
                    lang = ctxt.user_data.get('language'),
                    artwork_data = {
                        'username': ctxt.user_data.get('username'),
                        'name': update.effective_user.first_name,
                        'social_media': ctxt.user_data.get('social_media'),
                        'artwork_comment': ctxt.user_data.get('artwork_comment'),
                        'bot_username': ctxt.bot.username,
                    },
                )
            ))
        else:
            media_group.append(InputMediaPhoto(media=artwork))

    ctxt.user_data['media_group'] = media_group
    update.effective_chat.send_media_group(media=media_group)


    update.effective_chat.send_message(
        text = locales.confirm_artwork_text(lang=ctxt.user_data.get('language')),
        reply_markup = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text = locales.confirm_artwork_keyboard_text(lang=ctxt.user_data.get('language')).get('send'),
                    callback_data = 'rev_send',
                ),
                InlineKeyboardButton(
                    text = locales.confirm_artwork_keyboard_text(lang=ctxt.user_data.get('language')).get('cancel'),
                    callback_data = 'rev_cancel'
                ),
            ],
        ]),
    )

def send_to_revision(update: Update, ctxt: CallbackContext):
    '''
    Send post to revision channel to be Accepted/Declined
    '''
    match = re.match(r'rev_(send|cancel)', update.callback_query.data)

    if match.group(1) is None:
        update.effective_chat.send_message(
            text = locales.error_text(lang=ctxt.user_data.get('language')),
            reply_markup = ReplyKeyboardRemove(),
        )
        return states.START

    if match.group(1).startswith('send'):
        media_group = ctxt.user_data.get('media_group')

        token = str(uuid4())

        ctxt.bot_data[token] = media_group

        ctxt.bot.send_media_group(chat_id=os.getenv('revisionchat'),media=media_group)
        ctxt.bot.send_message(
            chat_id=os.getenv('revisionchat'),
            text = locales.send_to_mainchannel_text(lang=ctxt.user_data.get('language')),
            reply_markup = InlineKeyboardMarkup(inline_keyboard = [[
                InlineKeyboardButton(
                    callback_data=f'artwork_send_{token}',
                    text=locales.send_to_mainchannel_keyboard_text(ctxt.user_data.get('language')),
                ),
            ]]),
        )

        update.effective_chat.send_message(
            text = locales.artwork_sent_message(lang = ctxt.user_data.get('language')),
        )
    
    update.effective_chat.send_message(
        text = locales.start_text(lang=ctxt.user_data.get('language')),
    )
        
    update.effective_message.delete()
    ctxt.user_data.pop('artworks', None)
    ctxt.user_data.pop('artwork_type', None)
    
    return states.START

def process_artwork(update: Update, ctxt: CallbackContext):
    '''
    act according to the decision of channels' admins
    '''
    match = re.match(r'artwork_(send_([\w\W]+)|decline)', update.callback_query.data)
    if match.group(1) is None:
        update.effective_chat.send_message(
            text = locales.error_text(lang=ctxt.user_data.get('language')),
        )
        return None
    
    if match.group(1).startswith('send'):
        token = match.group(2)
        media_group = ctxt.bot_data.get(token)
        if media_group is None:
            update.effective_chat.send_message(
                text = locales.error_text(lang=ctxt.user_data.get('language')),
            )
            return None
        ctxt.bot.send_media_group(chat_id = os.getenv('mainchannel'),media=media_group)
        ctxt.bot_data.pop(token)

    update.effective_message.delete()
    
def change_language(update: Update, ctxt: CallbackContext):
    '''
    Change the user language
    '''
    if len (ctxt.args) >= 1:
        language: str = ctxt.args[0]
        if language not in config.LANGS:
            update.effective_chat.send_message(
                text = locales.language_not_supported_error_text(lang = ctxt.user_data.get('language')),
            )
        else:
            ctxt.user_data['language'] = language
            update.effective_chat.send_message(
                text = locales.language_changed_text(lang = ctxt.user_data.get('language')),
            )
    else:
        update.effective_chat.send_message(
            text = locales.wrong_language_command_format_text(lang=ctxt.user_data.get('language')),
        )
        return
