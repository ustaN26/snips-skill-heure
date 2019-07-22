from hermes_python.hermes import Hermes
from datetime import datetime
from datetime import date
from pytz import timezone

MQTT_ADDR = "localhost:1883"


def verbalise_hour(i):
	if i == 0:
		return "minuit"
	elif i == 1:
		return "une heure"
	elif i == 12:
		return "midi"
	elif i == 21:
		return "vingt et une heures"
	else:
		return "{0} heures".format(str(i))

def verbalise_minute(i):
	if i == 0:
		return ""
	elif i == 1:
		return "une"
	elif i == 21:
		return "vingt et une"
	elif i == 31:
		return "trente et une"
	elif i == 41:
		return "quarante et une"
	elif i == 51:
		return "cinquante et une"
	else:
		return "{0}".format(str(i))


def intent_received(hermes, intent_message):

	print()
	print(intent_message.intent.intent_name)
	print ()
	if intent_message.intent.intent_name == 'ustaN:heure':
		sentence = 'Il est '
		print(intent_message.intent.intent_name)

		now = datetime.now(timezone('Europe/Paris'))

		sentence += verbalise_hour(now.hour) + " " + verbalise_minute(now.minute)
		print(sentence)

		hermes.publish_end_session(intent_message.session_id, sentence)
	elif intent_message.intent.intent_name == 'ustaN:date':
		MonthList = ['Janvier','Fevrier','Mars','Avril','Mai','Juin','Juillet','Aout','Septembre','Octobre','Novembre','Decembre']
		DayList = ['Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi','Dimanche']
		dayNumber = date.today().day
		weekday = DayList[date.today().weekday()-1]
		sentence = "On est le " + weekday + " " + str(dayNumber) + " "+ MonthList[date.today().month-1]
		print(sentence)
		hermes.publish_end_session(intent_message.session_id, sentence)
	else :
		hermes.publish_end_session(intent_message.session_id, "erreur!")


with Hermes(MQTT_ADDR) as h:
	print("test")
	hermes.publish_end_session(intent_message.session_id, "this is a simple test")
	h.subscribe_intents(intent_received).start()
