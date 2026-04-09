from core.bot_instant import logger,get_bot
import flask
from flask import Flask
from core.module_loader import load_modules
import telebot
from core.bot_instant import logger
import logging
from init_db import populate_database
from database.local_db import load_data_on_startup
from database.db_operations import reset_db
logger.setLevel(logging.DEBUG)
#reset_db()
populate_database()
load_data_on_startup()
bot =get_bot()



load_modules(bot)







bot.infinity_polling()

# app = Flask(__name__)
# @app.route("/", methods=["GET"])
# def home():
#     return "BOT IS RUNNIG BIO BIOOOOOO", 200
#
# @app.route("/webhook", methods=["POST"])
# def webhook():
#     try:
#         json_data = request.get_json(force=True)
#         bot.process_new_updates([telebot.types.Update.de_json(json_data)])
#     except Exception as e:
#         print("Webhook error:", e)
#     return "OK", 200
# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 8080))
#     print(f"Running on PORT = {port}")
#     app.run(host="0.0.0.0", port=port,debug=True)
#     logger.setLevel(logging.DEBUG)


