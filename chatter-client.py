from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

bot = ChatBot('Bot')
bot.set_trainer(ListTrainer)

while True:
		message = input('You:')
		if message.strip() != 'Bye':
			reply = bot.get_response(message)
			print('Chatbot : ', reply)
		if message.strip() == 'Bye':
			print('ChatBot : Bye')
			break