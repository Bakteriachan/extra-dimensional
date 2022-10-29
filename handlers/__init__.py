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

CancelHandler = MessageHandler(
    filters=filters.button(
        btn_text=[
            locales.cancel_step_keyboard_text(lang=language) for language in locales.langs
        ]
    ),
    callback=callbacks.send,
)

conv_handler = ConversationHandler(
    entry_points = [
        CommandHandler(command='start', callback=callbacks.start),
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
            MessageHandler(filters=filters.artwork, callback=callbacks.process_artwork_content),
            CallbackQueryHandler(callback=callbacks.send_to_revision, pattern=r'revision_(send|cancel)'),
        ],
    }, 
    fallbacks = [
        CommandHandler(command='send', callback=callbacks.send),
        CommandHandler(command='start', callback=callbacks.start), 
    ]
)

process_artwork_handler = CallbackQueryHandler(callback=callbacks.process_artwork)
