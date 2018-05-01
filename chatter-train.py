from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.comparisons import levenshtein_distance
import os
import logging

default_response_txt = 'I am sorry, but I do not understand. Do you want me to search it in JIRA?'
new_text_to_save = False

def get_default_response(input_statement, response_list):
	print('get_default_response input : ', input_statement)
	print('get_default_response res : ', response_list)
	return response_list[0]
	
def get_most_frequent_response(input_statement, response_list):
	print('get_most_frequent_response input : ', input_statement)
	print('get_most_frequent_response res : ', response_list)
	return response_list[0]

bot = ChatBot(   
    'Bot',
	storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
			'statement_comparison_function': 'chatterbot.comparisons.levenshtein_distance',
            'response_selection_method': get_most_frequent_response
        },
        {
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': 0.70,
            'default_response': default_response_txt,
			'response_selection_method' : get_default_response
        }
    ],
	filters=["chatterbot.filters.RepetitiveResponseFilter"],
    trainer='chatterbot.trainers.ListTrainer'
)



def deleteSqlFile():
	filename = 'C://python//db.sqlite3'
	if os.path.exists(filename):
		os.remove(filename)


for files in os.listdir('C://python//chatterbot-corpus-master//chatterbot-corpus-master//chatterbot_corpus//data//english//'):
	data = open('C://python//chatterbot-corpus-master//chatterbot-corpus-master//chatterbot_corpus//data/english//' + files, 'r').readlines()
	bot.train(data)

while True:
	try:
		message = input('You:')
		print(new_text_to_save)
		if new_text_to_save :
			""" logic to save the keywords to new file, which in turn will be picked by JIRA runner to get proper data"""
			text_file = open("C://python//SearchJira.txt", "a")
			text_file.write("- - %s" % message +"\n")
			text_file.close()
			print('Chatbot : ', 'Thank you for the inputs. We will initiate the serach. Please search again after few minutes.')
			new_text_to_save = False;
		else :
			if message.strip().lower() != 'bye':
				reply = bot.get_response(message)
				if str(reply).find("Please mention keywords") == -1:
					new_text_to_save = False
				else :
					new_text_to_save = True
				print('Chatbot : ', reply)
			if message.strip().lower() == 'bye':
				print('ChatBot : Bye')
				deleteSqlFile()
				break
	except (KeyboardInterrupt, EOFError, SystemExit):
		print('ChatBot : Bye')
		deleteSqlFile()
		break




