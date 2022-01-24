#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging, time, requests

from telegram import Update, ForceReply, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CommandHandler, ConversationHandler


OPCIONES, SELECCION, PROBLEMA, COMPCODIGO, OTROS, FINAL, AYUDA = range(7)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(fr'Hola {user.mention_markdown_v2()}\ espero estés teniendo un buen día, yo soy Botcito 🤖 y trataré de ayudarte, Escriba /PQRS para proceder')
    
    


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Siga los pasos que el bot escriba o seleccione las opciones que el bot le brinde para la solución a su duda.')

def dni(update: Update, context: CallbackContext):
    try:
        update.message.reply_markdown_v2('Por favor, para que podamos brindarle ayuda, digite su dni👇')
        return OPCIONES

        

    except(ValueError):
        update.message.reply_text("Siga los pasos que el bot escriba o seleccione las opciones que el bot le brinde para la solución a su duda.")
        
     
     
def opciones(update: Update, context: CallbackContext):
    """Echo the user message."""
    try:
        text= update.message.text
        URL = "https://dniruc.apisperu.com/api/v1/dni/"+text+"?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InBpZXJvMDc5N0BnbWFpbC5jb20ifQ.9ihQAPvseXrz-Z0ScbvXJG3lNhQ5KCuBGQZWba6IzMU"
        data = requests.get(URL) 
        data = data.json()
        if len(text)==8 and text.isnumeric():
            time.sleep(2)
            update.message.reply_text("Estoy viendo si tus datos están en mi base de datos🤖 ")
            time.sleep(2)
            update.message.reply_text("Tus datos:\nDNI: "+data['dni']+"\nNOMBRES: "+data['nombres']+"\nAPELLIDO PATERNO: "+data['apellidoPaterno']+"\nAPELLIDO MATERNO: "+data['apellidoMaterno'])
            time.sleep(2)
            update.message.reply_text("Gracias por seguir los pasos, usted se encuentra en la sección de PQRS (Peticiones, Quejas, Reclamos y Sugerencias) \n Por favor escriba el numero(1,2 o 3) que desea elegir😊")
            time.sleep(2)
            update.message.reply_text("1. Tengo un problema con el envío \n2. Necesito ayuda sobre el envío \n3. Sugerir algo a futuro.")
            return SELECCION

        else:
            update.message.reply_text('Por favor digitar un DNI valido😕, vuelva a escribir /PQRS para proceder.')
            return ConversationHandler.END
    except:
        update.message.reply_text('Por favor digitar un DNI valido😕, vuelva a escribir /PQRS para proceder.')
        return ConversationHandler.END
    
        
def seleccion(update: Update, context: CallbackContext):
    """Echo the user message."""
    
    opcion= update.message.text
    if opcion=="1":
        time.sleep(2)
        update.message.reply_text("Usted ha seleccionado la opción de tener un problema con el envío. \nPor favor seleccione el problema que usted tiene sobre el envío😁")
        time.sleep(2)
        update.message.reply_text("1. La orden que pedí no es el producto que seleccioné \n2. El producto me ha llegado, pero roto o con problemas dentro \n3. El envío ha llegado incompleto \n4. Otros.")
        return PROBLEMA
    elif opcion=="2":
        time.sleep(2)
        update.message.reply_text("Usted ha seleccionado la opción de querer ayuda con el envío \nPor favor seleccione la opción que más se acerque a su urgencia😁")
        time.sleep(2)
        update.message.reply_text("1. El Producto que he pedido no ha llegado y ya ha pasado el tiempo estimado de llegada \n2. Quisiera hacer reembolso del envío  \n3. Quisiera anular el envío \n4. Otros.")
        return AYUDA
    elif opcion=="3":
        time.sleep(2)
        update.message.reply_text("Usted ha seleccionado la opción de poder sugerir algo hacia nosotros😊 \nMuchas gracias por seleccionar esta opción, nosotros siempre escuchamos a nuestros clientes y siempre queremos que tengan la mayor satisfacción posible😊")
        time.sleep(2)
        update.message.reply_text("Ya que es una sugerencia, por favor detalle todo lo que usted quiera aconsejarnos👇, uno de nuestros empleados lo leerá y luego nos comunicará su sugerencia hacia nuestros jefes, Gracias.")
        return FINAL
    else:
        time.sleep(2)
        update.message.reply_text('Parece que me has enviado una opción inválida😕, por favor vuelva a escribir /PQRS para proceder👇')
        return ConversationHandler.END

#SELECCION PROBLEMA    
def problema(update: Update, context: CallbackContext):
    """Echo the user message."""
    
    opcion= update.message.text
    if opcion=="1" or opcion=="3" :
        time.sleep(2)
        update.message.reply_text("Lamentamos mucho los problemas causados, para estos casos usted tiene la posibilidad de devolver el producto y nuestro sistema se encargará de hacer un nuevo pedido.")
        time.sleep(3)
        update.message.reply_text("Usted primero deberá llevar el paquete al transportista(puede consultarlo en el mismo paquete) y ellos le brindarán la información necesario para el procedimiento de reemplazo, luego en nuestra web podrá revisar la nueva orden de envío.")
        time.sleep(3)
        update.message.reply_text("Usted tiene 5 días para realizar este procedimiento, pasado estos 5 días, el paquete ya dejará de estar abierto a reclamos y no podrá hacer nada en estos casos, le aconsejamos que vaya lo más antes posible.")
        time.sleep(3)
        update.message.reply_text("Muchas gracias, Yo soy Botcito 🤖 y espero haberte ayudado, si deseas hacer otra consulta, por favor vuelva a escribir /PQRS. Espero tengas un buen día👋🏻 ")
        return ConversationHandler.END
    elif opcion=="2":
        time.sleep(2)
        update.message.reply_text("En caso de daños dentro del paquete, la única solución que podemos brindarle es reclamar en la compañia en dónde se contrató el transporte(Puede revisarlo en el mismo paquete)")
        time.sleep(2)
        update.message.reply_text("Usted tiene 7 días naturales para hacer el reclamo, Por favor hágalo lo más antes posible para que se pueda solucionar su problema.")
        time.sleep(2)
        update.message.reply_text("Muchas gracias, Yo soy Botcito 🤖 y espero haberte ayudado, si deseas hacer otra consulta, por favor vuelva a escribir /PQRS. Espero tengas un buen día👋🏻 ")
        return ConversationHandler.END
    elif opcion=="4":
        time.sleep(2)
        update.message.reply_text("Por favor, detállame tu consulta para poder ayudarte 👇")
        return OTROS
    else:
        time.sleep(2)
        update.message.reply_text('Parece que me has enviado una opción inválida😕, por favor vuelva a escribir /PQRS para proceder👇')
        return ConversationHandler.END

def ayuda(update: Update, context: CallbackContext):
    """Echo the user message."""
    
    opcion= update.message.text
    if opcion=="1" :
        time.sleep(2)
        update.message.reply_text("Lamentamos mucho los problemas causados, para este caso, usted deberá entrar en nuestra web, revisar su pedido y por último ir a la opción de 'Mi pedido no ha llegado en el tiempo estimado'.")
        time.sleep(3)
        update.message.reply_text("Por favor, asegurese de que realmente hayan pasado los días que ha seleccionado en la compra, lo puede ver en sus pedidos en la web.")
        time.sleep(3)
        update.message.reply_text("Le enviaremos un formulario para que llene con datos del producto, luego de realizar el formulario y enviarlo, solo deberá esperar nuestra respuesta, normalmente respondemos de 1 a 3 días.")
        time.sleep(3)
        update.message.reply_text("Muchas gracias, Yo soy Botcito 🤖 y espero haberte ayudado, si deseas hacer otra consulta, por favor vuelva a escribir /PQRS. Espero tengas un buen día👋🏻 ")
        return ConversationHandler.END
    elif opcion=="2":
        time.sleep(2)
        update.message.reply_text("En caso de querer reembolsar su producto, usted primero deberá llevar el paquete al transportista(puede consultarlo en el mismo paquete), ellos luego nos entregarán el producto en nuestro centro de devoluciones.")
        time.sleep(2)
        update.message.reply_text("Usted tiene 7 días naturales como MÁXIMO para hacer el reembolso, Luego de que el paquete haya sido procesado en nuestro centro de devoluciones, empezaremos a procesar la devolución de su dinero.")
        time.sleep(2)
        update.message.reply_text("Normalmente procesamos las devoluciones en 5 días hábiles.")
        time.sleep(2)
        update.message.reply_text("Muchas gracias, Yo soy Botcito 🤖 y espero haberte ayudado, si deseas hacer otra consulta, por favor vuelva a escribir /PQRS. Espero tengas un buen día👋🏻 ")
        return ConversationHandler.END
    elif opcion=="3":
        time.sleep(2)
        update.message.reply_text("En caso de querer anular el envío, en primer lugar asegurese que el envío esté lejos del tiempo estipulado para la entrega de este mismo.")
        time.sleep(3)
        update.message.reply_text("Este proceso de cancelación, solo lo podrá hacer en nuestra web. Deberá ir a mis pedidos y luego debe seleccionar el pedido a cancelar, luego darle a 'Cancelar productos marcados'.")
        time.sleep(3)
        update.message.reply_text("En caso el pedido ya está a 48 horas de llegar, usted deberá esperar a que llegue para luego realizar el proceso de 'Reembolsar pedido'. Lo puede consultar aquí mismo, solamente debe volver a empezar la consulta PQRS.")
        time.sleep(3)
        update.message.reply_text("Muchas gracias, Yo soy Botcito 🤖 y espero haberte ayudado, si deseas hacer otra consulta, por favor vuelva a escribir /PQRS. Espero tengas un buen día👋🏻 ")
        return ConversationHandler.END
    else:
        time.sleep(2)
        update.message.reply_text('Parece que me has enviado una opción inválida😕, por favor vuelva a escribir /PQRS para proceder👇')
        return ConversationHandler.END


def otros(update: Update, context: CallbackContext):
    """Echo the user message."""
    time.sleep(2)
    update.message.reply_text("Debido la alta demanda te comunicaremos con un asesor para que podamos resolver tus dudas, Recuerda que soy Botcito🤖 y esperemos podamos resolver tus dudas 👋🏻. No te olvides de escribir /PQRS por si necesitas otra consulta ")
    return ConversationHandler.END

def final(update: Update, context: CallbackContext):
    """Echo the user message."""
    time.sleep(2)
    update.message.reply_text("Muchas gracias por su sugerencia, Yo soy Botcito 🤖 y espero haberte ayudado, si deseas hacer otra consulta, por favor vuelva a escribir /PQRS. Espero tengas un buen día👋🏻 ")
    return ConversationHandler.END

def compcodigo(update: Update, context: CallbackContext):
    """Echo the user message."""
    
    opcion= update.message.text
    update.message.reply_text("Por favor, escriba el código de producto que le brindamos cuando compró el producto.")
    if opcion=="1":
        update.message.reply_text("Por favor, escriba el código de producto que le brindamos cuando compró el producto.")
    elif opcion=="2":
        update.message.reply_text("En caso de daños dentro del paquete, la única solución que podemos brindarle es reclamar en la compañia en dónde se contrató el caso de transporte.")
        update.message.reply_text("Usted tiene 7 días naturales para hacer el reclamo, Por favor hágalo lo más antes posible para que se pueda solucionar su problema")
        update.message.reply_text("Muchas gracias, Yo soy Botcito y espero haberte ayudado, si deseas hacer otra consulta, por favor vuelva a escribir /PQRS. Espero tengas un buen día")
        return ConversationHandler.END
    else:
        update.message.reply_text('Por favor digitar una opción valida, vuelva a escribir /PQRS para proceder')
        return ConversationHandler.END
    
    
def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END
        
        
def pizza(update: Update, context: CallbackContext):
    """Echo the user message."""
    if(update.message.text.upper().find("MANZANAS VERDES") > 0):
        update.message.reply_text("Prefiero comer pizza")
        
        
def sumar(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    try:
        numero1= int(context.args[0])
        numero2= int(context.args[1])
        
        suma= numero1 + numero2
        
        update.message.reply_text("la suma es "+str(suma))
    except(ValueError):
        update.message.reply_text("Por favor utilice dos numeros")
    

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("2120107910:AAHj_FFrTF5wYoSL2rd-nfpDlEpopkvaRLs")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    
    dispatcher.add_handler(CommandHandler("start", start))

    conv_handler = (ConversationHandler(
        entry_points=[CommandHandler("PQRS", dni)], 
        states={
            OPCIONES:[MessageHandler(Filters.text, opciones)], 
            SELECCION:[MessageHandler(Filters.text, seleccion)],
            PROBLEMA:[MessageHandler(Filters.text, problema)],
            COMPCODIGO:[MessageHandler(Filters.text, compcodigo)],
            OTROS:[MessageHandler(Filters.text, otros)],
            FINAL:[MessageHandler(Filters.text, final)],
            AYUDA:[MessageHandler(Filters.text, ayuda)],
            }, 
        fallbacks=[CommandHandler("cancel", cancel)])
        )
    '''dispatcher.add_handler(ConversationHandler(
        entry_points=[CommandHandler("PQRS", dni)], 
        states={
            OPCIONES:[MessageHandler(Filters.text, opciones)], SELECCION:[MessageHandler(Filters.text, seleccion)],
            }, 
        fallbacks=[CommandHandler("cancel", cancel)])
        )'''
    '''
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("sumar", sumar))
    dispatcher.add_handler(CommandHandler("restar", restar))'''
    
    # on non command i.e message - echo the message on Telegram
    
    dispatcher.add_handler(conv_handler)
    
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()