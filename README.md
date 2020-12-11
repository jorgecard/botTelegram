# De qué se trata

Este proyecto ha sido creado para experimentar la creación de un **bot** para Telegram. El bot es un programa que contesta en un canal de Telegram propio a los comandos que introducte el usuario, o publica eventos y mensajes por si mismo automática,emte

# Tecnologías

Para el desarrollo se ha utilizado:

- Python 3.7
- Visual Studio Code y extensión de Python
- Librería Python-telegram-bot: https://github.com/python-telegram-bot/python-telegram-bot
- Telegram web o en app móvil para probar el funcionamiento

# Requisitos

1. Crear un bot a través del **Bot Father**. No asignará un token para la API de telegram que integraremos en nuestro proyecto.
2. Debemos instalar siempre en primer lugar la librería que vamos a utilizar. En mi caso, yo lo he hecho a través de la terminal de VS Code.

```
pip install python-telegram-bot
```

3. Desde telegram buscaremos el canal y nos conectaremos a él para realizar las pruebas

# Canal de pruebas

El canal se llama ```Danitic_bot``` y se puede encontrar en Telegram

- Aditya: https://web.telegram.org/#/im?p=@aditya931_bot
- Edson: https://web.telegram.org/#/im?p=@Apzzunbot
- Jose Luis (@hyukilbot): https://web.telegram.org/#/im?p=@hyukilbot
- Christian (@pascubot): https://web.telegram.org/#/im?p=@pascubot
- Miguel Angel:https://web.telegram.org/#/im?p=@sgvsegbot
- Leo: https://web.telegram.org/#/im?p=@LeombBot
- Mariano: https://web.telegram.org/#/im?p=@uver_bot

# Poner estilos

Actualizar las respuestas:

```python
update.message.reply_text('*_bold and italic_*', parse_mode='MarkdownV2')
```
Ejemplos:

```
*bold \*text*
_italic \*text_
__underline__
~strikethrough~
*bold _italic bold ~italic bold strikethrough~ __underline italic bold___ bold*
[inline URL](http://www.example.com/)
[inline mention of a user](tg://user?id=123456789)
`inline fixed-width code`
```


