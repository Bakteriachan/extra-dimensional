ES : str = 'es'
default_lang = ES #default language in case the language is not specified

langs = [ES] # available languages

def start_text(lang:str, agreement=False):
    if agreement:
        text = {
            ES: '🛡 NORMATIVA PARA EL ENVÍO 🛡\n\n[ POSIBLES MOTIVOS DE RECHAZO DE OBRAS A PUBLICAR ]\n\n❌ Plagio o robo de piezas artísticas.\n\n❌ Ediciones no autorizadas de obras ajenas.\n\n❌ Realizar spam de manera intrusiva en los comentarios.\n\n❌ Contenido explícito o delicado, obras de índole muy agresiva o soez, entre otras de la misma índole.\n\n📣 Para una publicidad más profesional o un envío directo de su tabla de precios, diríjase al contacto @Sadboy603.\n\nEste contacto es público, para cualquier duda, sugerencia, queja o pregunta, escriba. Será bienvenido/a',
        }
    else:
        text = {
            ES: 'Para enviar su obra use el comando /send',
        }

    return text.get(lang, text.get(default_lang))

def start_keyboard_text(lang:str):
    text = {
        ES: {
            'accept': 'Acepto',
            'decline': 'No acepto',
        },
    }

    return text.get(lang, text.get(default_lang))

def agreement_declined(lang: str):
    text = {
        ES: 'Para usar nuestros servicios debe aceptar nuestras normativas.',
    }

    return text.get(lang, text.get(default_lang))

def error_text(lang:str):
    text = {
        ES: 'Hubo un error, por favor hable con los administradores',
    }
    
    return text.get(lang, text.get(default_lang))

def username_text(lang:str):
    text = {
        ES: 'Envie su nombre de usuario (@username)',
    }

    return text.get(lang, text.get(default_lang))

def social_media_text(lang:str):
    text = {
       ES: 'Envie las redes sociales que desee',
    }

    return text.get(lang, text.get(default_lang))

def omit_step_keyboard_text(lang:str):
    text = {
        ES: '➡️ Omitir',
    }

    return text.get(lang, text.get(default_lang))

def cancel_step_keyboard_text(lang:str):
    text = {
        ES: '🚫 Cancelar'
    }

    return text.get(lang, text.get(default_lang))

def artwork_comment_text(lang:str):
    text = {
        ES: 'Envie un comentario sobre esta obra',
    }

    return text.get(lang, text.get(default_lang))

def artwork_content_text(lang: str):
    text = {
        ES: 'Envie el contenido que desea enviar al canal.',
    }

    return text.get(lang, text.get(default_lang))

def build_artwork_caption(lang: str, artwork_data: dict):
    username = artwork_data.get('username')
    name = artwork_data.get('name')
    social_media = artwork_data.get('social_media')
    artwork_comment = artwork_data.get('artwork_comment')
    bot_username = artwork_data.get('bot_username')

    text = f'🔰 #Artista 🔰\n\n🔖 Nombre: {username}\n📌 #{name}'
    
    if social_media is not None:
        text += f'\n\n📱Redes📱\n{social_media}'
    
    if artwork_comment is not None:
        text += f'\n\n🪧Comentario: {artwork_comment}'
    
    text += f'\n\n🤖 Compartir Arte: @{bot_username}'

    return text

def artwork_sent_message(lang: str):
    text = {
        ES: 'Contenido enviado a revision.',
    }

    return text.get(lang, text.get(default_lang))

def send_artwork_for_revision_keyboard_text(lang: str):
    text = {
        ES: {
            'send': 'Enviar',
            'cancel': 'Cancelar',
        },
    }

    return text.get(lang, text.get(default_lang))
