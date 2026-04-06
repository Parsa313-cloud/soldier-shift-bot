import telebot
from config import API_TOKEN
import logging
from telebot import apihelper


#this file return bot variable which is connected with api from telebot


logger = telebot.logger

def get_bot():
    apihelper.API_URL=config.API_URL
    #apihelper.ENABLE_MIDDLEWARE = True
    bot = telebot.TeleBot(API_TOKEN)
    return bot