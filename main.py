from core.bot_instant import bot,logger
import flask
from flask import Flask
from core.module_loader import load_module


load_module(bot)









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


