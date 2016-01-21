import telebot
import main

TOKEN = '126422692:AAH6cZnU66YKPa8cFtqQmsw6kuIn_Nm9t74'
bot = telebot.TeleBot(TOKEN, True)

@bot.message_handler(commands = ['setMatrix'])
def set_matrix(message):
	matrix = message.text[message.text.find(' ') + 1:]
	f = open('input.txt', 'w')
	f.write(matrix)
	bot.send_message(message.chat.id, 'hey')

@bot.message_handler(commands = ['check'])
def check_string(message):
	string = message.text[message.text.find(' ') + 1:]
	bot.send_message(message.chat.id, main.check(string, main.read_matrix()))

@bot.message_handler(commands = ['rightGramma'])
def right_gramma(message):
	bot.send_message(message.chat.id, main.rightGramma(main.read_matrix()))

@bot.message_handler(commands = ['getMatrix'])
def show_matrix(message):
	f = open('input.txt', 'r')
	bot.send_message(message.chat.id, f.read())

bot.polling()