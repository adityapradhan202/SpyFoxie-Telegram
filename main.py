from telegram import Update
from telegram.ext import MessageHandler
from telegram.ext import CommandHandler
from telegram.ext import filters
from telegram.ext import ApplicationBuilder
from telegram.ext import ConversationHandler
from telegram.ext import ContextTypes
from telegram.ext import CallbackContext

import time
import ytcourse as ytc

import os
import dotenv
dotenv.load_dotenv()
bot_token = os.getenv("TOKEN")

import pswd_encrypt
import admin_credentials as acreds

from customer_ids import customer_id_pass, random_id, id_password
from paid_links import paid


# start-command
async def start(update:Update, context:ContextTypes.DEFAULT_TYPE):
    start_msg = """
Hey there! 🦊 SpyFoxie welcomes you! 

Use the /help command to proceed!

DISCALIMER - We are not sponsered by any organization. This is a very private bot, trying it's best to deliver you quality content, either completelty free or at a very low price 💸"""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=start_msg)

# help command
async def help(update:Update, context:ContextTypes.DEFAULT_TYPE):
    help_text = """
Here are the commands that you can use to get the best free coding courses on youtube - 
> /python
> /webdev
> /machine_learning
> /appdev

If you have given the payment, then use the command given below to get access to your courses - 
> /customer_login

If you are the admin then use this command to login and unlock the admin commands - 
> /admin_login
"""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)


# free yt courses
async def python(update:Update, context:ContextTypes.DEFAULT_TYPE):
    for i in ytc.links["python"]:
        await update.message.reply_text(i)
        time.sleep(0.5)
    await update.message.reply_text("Here are some of the best popular python courses available on youtube ☝️")

async def webdev(update:Update, cotnext:ContextTypes.DEFAULT_TYPE):
    for i in ytc.links["webdev"]:
        await update.message.reply_text(i)
        time.sleep(0.5)
    await update.message.reply_text("Here are some of the best popular webdev courses available on youtube ☝️")

async def machine_learning(update:Update, context:ContextTypes.DEFAULT_TYPE):
    for i in ytc.links["machine_learning"]:
        await update.message.reply_text(i)
        time.sleep(0.5)
    await update.message.reply_text("Here are some of the best popular webdev courses available on youtube ☝️")

async def appdev(update:Update, context:ContextTypes.DEFAULT_TYPE):
    x = """We apologize for the inconvenience! Currently we are working on searching and listing the best app development courses for you! So right now we dont have any courses for you!"""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=x)


# customer-login command
# ----------------------------------------------------------------
async def customer_panel(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Use the commands in this panel to get the links for all the paid courses!")
    customer_panel_text = """
Use these commands to get access to the premium courses - 
> Paid python courses -> /dev8ion67829
> Paid machine learning or datascience courses -> /dev8ion97821
"""
    await update.message.reply_text(customer_panel_text)



CUSTOMER_ID, CUSTOMER_PASSWORD = range(2)
async def customer_login(update:Update, context:CallbackContext):
    await update.message.reply_text("You would have received the login credentials if you have done the payment.")
    await update.message.reply_text("Use those login credentials to login.")
    await update.message.reply_text("Use the /cancel_process command to cancel the procedure at any moment!")
    await update.message.reply_text("First enter your ID here in the chat!")

    return CUSTOMER_ID

async def get_customer_password(update:Update, context:CallbackContext):
    context.user_data["customer_id"] = update.message.text
    print("-> Customer id stored")

    await update.message.reply_text("Nice! Enter the password now!")

    return CUSTOMER_PASSWORD

async def verify_customer(update:Update, context:CallbackContext):

    context.user_data["customer_password"] = update.message.text
    print("-> Customer password stored")

    await update.message.reply_text("Wait for a few seconds!")
    time.sleep(2)
    cust_id, cust_pass = context.user_data["customer_id"], context.user_data["customer_password"]

    if customer_id_pass[cust_id] == cust_pass:
        print("-> Customer has logged in!")
        await update.message.reply_text("Login successful!")

        f = open("user_logins.txt", "r")
        logins = f.read()
        f.close()

        logins = int(logins)
        logins += 1

        f2 = open("user_logins.txt", "w")
        f2.write(str(logins))
        f2.close()

        
        await customer_panel(update, context)
        return ConversationHandler.END
    else:
        await update.message.reply_text("Invalid login credentials!")
        return ConversationHandler.End

async def cancel_process(update:Update, context:CallbackContext):
    await update.message.reply_text("Customer authentication process cancelled!")
    return ConversationHandler.END


# -----------------------------
# All the premium commands here...
async def dev8ion67829(update:Update, context:ContextTypes.DEFAULT_TYPE):
    """python"""
    for i in paid["python"]:
        await update.message.reply_text(f"{i} - {paid['python'][i]}", disable_web_page_preview=True)
    
    await update.message.reply_text("These are all the paid python course we have for you!")
    
async def dev8ion97821(update:Update, context:ContextTypes.DEFAULT_TYPE):
    "machine-learning-datascience"
    for i in paid["machine_learning_datasciennce"]:
        await update.message.reply_text(f"{i} - {paid['machine_learning_datasciennce'][i]}", disable_web_page_preview=True)
    
    await update.message.reply_text("These are all the paid machine-learning-datasciene course we have for you!")



# ----------------------------------
# ADMIN-LOGIN-PART
# conversation-states
ADMIN_USERNAME, ADMIN_PASS = range(2) 

# entry-point
async def admin_login(update:Update, context:CallbackContext):
    await update.message.reply_text("If you are the admin then you will need the login credentials to get access!")
    await update.message.reply_text("Use /cancel to cancel the process at any moment!")
    await update.message.reply_text("Please enter your username here!")

    return ADMIN_USERNAME

async def admin_password(update:Update, context:CallbackContext):
    print("Entering admin_passw function...")
    context.user_data["admin_username"] = update.message.text  
    print("-> Username has been stored")  
    
    await update.message.reply_text(f"Ohh...\n{update.message.text} is such a cute username UwU")
    await update.message.reply_text("Nice! Now enter the password 😉")
    
    return ADMIN_PASS

async def verify_admin(update:Update, context:CallbackContext):
    context.user_data["admin_password"] = update.message.text
    print("-> Password has been stored")
    await update.message.reply_text("Wait for a few seconds, let the system verify if it is really the admin or someone else...")
    time.sleep(3)

    ad_username = context.user_data["admin_username"]
    ad_password = context.user_data["admin_password"]

    try:

        if pswd_encrypt.verify_password(ad_password, acreds.admin_data[ad_username]):
            print("-> Admin has logged in!")
            await update.message.reply_text("Login successful!")
            await update.message.reply_text("Generating the admin panel...")
            time.sleep(2)
            await admin_help(update, context)
            await update.message.reply_text("You can use the admin commands given in this pannel ☝️")
            return ConversationHandler.END # ending for now
        
        else:
            await update.message.reply_text("Invalid credentials!")
            return ConversationHandler.END
        
    except Exception as e:

        print(f"Error occured while admin-verification - {e}")
        await update.message.reply_text("Either the username or the password is wrong.")
        await update.message.reply_text("Make sure to enter the correct username and password.")

        return ConversationHandler.END


        
async def cancel(update: Update, context: CallbackContext):
    await update.message.reply_text("Authentication cancelled!")

    return ConversationHandler.END


# ------------------------------------------------
# Admin commands - secret commands
async def dev8ion67119(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Here is the username and password for the customer.")
    customer_id = random_id()
    customer_pass = id_password(customer_id)
    await update.message.reply_text(f"Username: {customer_id}\nPassword: {customer_pass}")
    await update.message.reply_text("Share this information with the customer!")

async def admin_help(update:Update, context:ContextTypes.DEFAULT_TYPE):
    admin_help_text = """
> Generate id-pass for new customer - /dev8ion67119
"""
    await update.message.reply_text(admin_help_text)

# COMMANDS FOR ADMIN-1 ONLY
async def cust_logins123(update:Update, context:ContextTypes.DEFAULT_TYPE):

    file = open("user_logins.txt", "r")
    logins = file.read()

    await update.message.reply_text(f"Number of logins: {logins}")
    await update.message.reply_text(f"This is a very secret information! Don't share this with anyone 🤫")

UPDATED_CUSTOMER_LOGINS = range(1)
async def cust_logins_update123(update:Update, context:CallbackContext):
    await update.message.reply_text("Enter the updated data (for number of customer logins)")
    return UPDATED_CUSTOMER_LOGINS

async def get_customer_logins(update:Update, context:CallbackContext):
    try:
        updated_logins = int(update.message.text)
        with open("user_logins.txt", "w") as f:
            f.write(str(updated_logins))

        print("-> Customer logins has been upated!")
        await update.message.reply_text("Data provided by you has been updated!")

        return ConversationHandler.END

    except Exception as e:
        print(f"-> Exception occured while updating user-logins - {e}")
        await update.message.reply_text("Please enter integer value!")
        await cust_logins_update123(update, context)


async def cancel_updation_process(update:Update, context:CallbackContext):
    await update.message.reply_text("Updation process cancelled!")

    return ConversationHandler.END


# ----------------------------------------------------------


    
if __name__ == "__main__":
    
    # building the app
    app = ApplicationBuilder().token(bot_token).build()


    start_cmd = CommandHandler("start", start)
    help_cmd = CommandHandler("help", help)

    # conversation-handler-admin-login
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("admin_login", admin_login)],
        states={
            ADMIN_USERNAME: [MessageHandler((filters.TEXT & ~filters.COMMAND), admin_password)],
            ADMIN_PASS: [MessageHandler((filters.TEXT& ~filters.COMMAND), verify_admin)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )


    # conversation-handler-customer-login
    conv_handler_cust_login = ConversationHandler(
        entry_points=[CommandHandler("customer_login", customer_login)],
        states={
            CUSTOMER_ID: [MessageHandler((filters.TEXT & ~filters.COMMAND), get_customer_password)],
            CUSTOMER_PASSWORD: [MessageHandler((filters.TEXT& ~filters.COMMAND), verify_customer)]
        },
        fallbacks=[CommandHandler("cancel_process", cancel_process)]
    )


    # msg_handler = MessageHandler((filters.TEXT & ~filters.COMMAND), msg_checker)

    app.add_handler(start_cmd)
    app.add_handler(help_cmd)
    # app.add_handler(msg_handler)

    app.add_handlers(handlers={
        0:[CommandHandler("webdev", webdev)],
        1:[CommandHandler("machine_learning", machine_learning)],
        2:[CommandHandler("appdev", appdev)],
        3:[CommandHandler("python", python)]
    })


    # adding the conv-handler
    app.add_handler(conv_handler)
    # adding the conv-handler-customer-login-part
    app.add_handler(conv_handler_cust_login)

    # handlers of the admin command
    new_customer_handler = CommandHandler("dev8ion67119", dev8ion67119)
    app.add_handler(new_customer_handler)


    # premium-commands-command-handler 
    app.add_handlers(
        handlers={
            0:[CommandHandler("dev8ion67829", dev8ion67829)],
            1:[CommandHandler("dev8ion97821", dev8ion97821)]
        }
    )

    # Handler for ADMIN-1 only commands

    app.add_handler(CommandHandler("cust_logins123", cust_logins123))

    cust_login_update_handler = ConversationHandler(
        entry_points=[CommandHandler("cust_logins_update123", cust_logins_update123)],
        states={
            UPDATED_CUSTOMER_LOGINS: [MessageHandler((filters.TEXT & ~filters.COMMAND), get_customer_logins)],
        },
        fallbacks=[CommandHandler("cancel_updation_process", cancel_updation_process)]
    )

    app.add_handler(cust_login_update_handler)

    print("-----------------")
    print("The bot is up! Open the telegram app to test the bot!")
    app.run_polling()


 
# Bot link - t.me/spyfoxie_bot