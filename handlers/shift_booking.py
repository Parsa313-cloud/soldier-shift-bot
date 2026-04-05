

def shift_booking(bot):
    @bot.message_handler(commands=['my_shifts' , 'booking shifts'])
    def shift_panel(message):
        #decoratore ===> @soldier
        if message.text == "my_shifts":
            pass
        if message.text == "booking shifts":
            pass
