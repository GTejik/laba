import telebot
from telebot import types
import main

TOKEN = '126422692:AAH6cZnU66YKPa8cFtqQmsw6kuIn_Nm9t74'
bot = telebot.TeleBot(TOKEN, True)

@bot.message_handler(commands = ['start'])
def send_start(message):
	bot.send_message(message.chat.id, 'бот для сдачи лабораторных работ\nсписок команд смотри, введя \'/\'')
	
@bot.message_handler(commands = ['set_matrix'])
def set_matrix(message):
	if message.text.find(' ') == -1:
		bot.send_message(message.chat.id, 'пустой аргумент')
		return
	matrix = message.text[message.text.find(' ') + 1:].strip()
	f = open('input.txt', 'w')
	if len(matrix):
		f.write(matrix)
	bot.send_message(message.chat.id, 'новая матрица установлена')

@bot.message_handler(commands = ['right_gramma'])
def right_gramma(message):
	mes = main.rightGramma(main.read_matrix())
	if len(mes):
		bot.send_message(message.chat.id, mes)
	else:
		bot.send_message(message.chat.id, 'невозможно построить грамматику')

@bot.message_handler(commands = ['get_matrix'])
def show_matrix(message):
	f = open('input.txt', 'r')
	bot.send_message(message.chat.id, f.read())

@bot.message_handler(commands = ['regexp'])
def set_regexp(message):
	if message.text.find(' ') == -1:
		bot.send_message(message.chat.id, 'пустой аргумент')
		return
	regexp = message.text[message.text.find(' ') + 1:]

	main.regexp_to_nka(regexp)

	bot.send_message(message.chat.id, regexp)

@bot.message_handler(commands = ['laba'])
def send_choice(message):
	markup = types.ReplyKeyboardMarkup()
	markup.row('Задание 1_2', 'Задание 1_3')
	markup.row('Недетерминированная', 'Регулярное выражение')
	bot.send_message(message.chat.id, 'Выберите задание:', reply_markup = markup)

@bot.message_handler(regexp = 'Задание 1_2')
def set_matrix_laba2_1(message): 
	markup = types.ReplyKeyboardHide(selective = False)
	f = open('input.txt', 'w')
	f.write('0 1\n-A A B 0\nB B B 1');
	bot.send_message(message.chat.id, 'проверить, что в последовательности имеется по крайней мере одна \'1\', матрица:\n0 1\n-A A B 0\nB B B 1', reply_markup=markup)

@bot.message_handler(regexp = 'Задание 1_3')
def set_matrix_laba2_2(message):
	markup = types.ReplyKeyboardHide(selective = False)
	f = open('input.txt', 'w')
	f.write('0 1 2 3 4 5 6 7 8 9 + - * / = ,\n-a d b b b b b b b b b e f e e e e 0\nb b b b b b b b b b b c c c c c a 0\nc g h h h h h h h h h e e e e e a 0\nd e e e e e e e e e e c c c c c a 0\nf e b b b b b b b b b c c c c c a 0\nh h h h h h h h h h h c c c c c a 1\ng e e e e e e e e e e c c c c c a 1\ne e e e e e e e e e e e e e e e a 0');
	bot.send_message(message.chat.id, 'цепочка состоит из арифметических выражений и не содержит скобок, матрица:\n0 1 2 3 4 5 6 7 8 9 + - * / = ,\n-a d b b b b b b b b b e f e e e e 0\nb b b b b b b b b b b c c c c c a 0\nc g h h h h h h h h h e e e e e a 0\nd e e e e e e e e e e c c c c c a 0\nf e b b b b b b b b b c c c c c a 0\nh h h h h h h h h h h c c c c c a 1\ng e e e e e e e e e e c c c c c a 1\ne e e e e e e e e e e e e e e e a 0\n\na - начальное состояние\nb - только цифры\nc - арифметический знак встретили\nd - ноль (не может быть в начале) \nf - минус (не может быть -0, но -3 ок)\nh - не только цифры, есть выражения\ng - не только ноль, есть выражения\ne - ошибка\n', reply_markup=markup)

@bot.message_handler(regexp = 'Недетерминированная')
def set_nd_matrix(message):
	markup = types.ReplyKeyboardHide(selective = False)
	f = open('input.txt', 'w')
	f.write('0 1\n-a a,b c 0\n-b e c 1\nc e a,c 1\ne e e 0');
	bot.send_message(message.chat.id, 'матрица:\n0 1\n-a a,b c 0\n-b e c 1\nc e a,c 1\ne e e 0', reply_markup=markup)

@bot.message_handler(regexp = 'Регулярное выражение')
def set_l_regexp(message):
	markup = types.ReplyKeyboardHide(selective = False)
	regexp = '1+|1*01(11|a)+'

	bot.send_message(message.chat.id, 'Установлено: '+ regexp, reply_markup=markup)

	main.regexp_to_nka(regexp)

@bot.message_handler(commands = ['help'])
def send_help(message):
	bot.send_message(message.chat.id, 'Галайко Никита Сергеевич\nБИВ135\nВариант 6\nИсходные коды доступны по ссылке: github.com/ngalayko/laba')

@bot.message_handler(func=lambda m: True)
def check_string(message):
	string = message.text[message.text.find(' ') + 1:]
	bot.send_message(message.chat.id, main.check(string, main.read_matrix()))

bot.polling()