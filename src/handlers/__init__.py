from telegram.ext import (
    ConversationHandler,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
)

import callbacks
import states
import filters
import locales
import config

CancelHandler = MessageHandler(
    filters=filters.button(
        btn_text=[
            locales.cancel_step_keyboard_text(lang=language) for language in config.LANGS
        ],
    ),
    callback=callbacks.send,
)

conv_handler = ConversationHandler(
    entry_points = [
        CommandHandler(command = 'start', callback=callbacks.start),
        CommandHandler(command = 'send', callback=callbacks.send),
        CallbackQueryHandler(callback=callbacks.process_agreement, pattern=r'rules_(accept|decline)'),
    ], 
    states = {
        states.START: [
            CommandHandler(command='send', callback=callbacks.send),
        ],
        states.USERNAME: [
            CancelHandler,
            MessageHandler(filters=filters.text, callback=callbacks.process_username),
        ],
        states.SOCIAL_MEDIA: [
            CancelHandler,
            MessageHandler(filters=filters.text, callback=callbacks.process_social_media),
        ],
        states.ARTWORK_COMMENT: [
            CancelHandler,
            MessageHandler(filters=filters.text, callback=callbacks.process_artwork_comment),
        ],
        states.ARTWORK_CONTENT: [
            CancelHandler,
            MessageHandler(filters=filters.button(btn_text=[locales.confirm_artwork_button_text(lang) for lang in config.LANGS]), callback=callbacks.confirm_artworks),
            MessageHandler(filters=filters.artwork, callback=callbacks.process_artwork_content),
            CallbackQueryHandler(callback=callbacks.send_to_revision, pattern=r'rev_(send|cancel)'),
        ],
    }, 
    fallbacks = [
        CommandHandler(command='send', callback=callbacks.send),
        CommandHandler(command='start', callback=callbacks.start), 
    ]
)

process_artwork_handler = CallbackQueryHandler(callback=callbacks.process_artwork)
change_language = CommandHandler(command='language', callback=callbacks.change_language)

sugestions_conv_handler = ConversationHandler(
    entry_points = [
        CommandHandler(command='suggest', callback=callbacks.suggest_command)
    ],
    states = {
        states.RECEIVE_SUGGESTION_TEXT: [
            MessageHandler(filters=filters.button(btn_text=[locales.cancel_step_keyboard_text(lang=language) for language  in config.LANGS]), callback = callbacks.cancel_suggest_command),
            MessageHandler(filters=filters.text, callback=callbacks.process_suggestion_text)
        ],
    },
    fallbacks = [],
)

