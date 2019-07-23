# -*- coding: utf-8 -*-
from hermes_python.hermes import Hermes
from datetime import datetime
from datetime import date
from pytz import timezone
import ConfigParser
import io

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

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

class SnipsConfigParser(ConfigParser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, ConfigParser.Error) as e:
        return dict()

def subscribe_intent_callback(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    action_wrapper(hermes, intentMessage, conf)


def action_wrapper(hermes, intentMessage, conf):
	print(intentMessage)
	if intentMessage.intent.intent_name == 'ustaN:heure':
		sentence = 'Il est '
		now = datetime.now(timezone('Europe/Paris'))
		sentence += verbalise_hour(now.hour) + " " + verbalise_minute(now.minute)
		print(sentence)
		hermes.publish_end_session(intentMessage.session_id, sentence)
	elif intentMessage.intent.intent_name == 'ustaN:date':
		MonthList = ['Janvier','Fevrier','Mars','Avril','Mai','Juin','Juillet','Aout','Septembre','Octobre','Novembre','Decembre']
		DayList = ['Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi','Dimanche']
		dayNumber = date.today().day
		weekday = DayList[date.today().weekday()-1]
		sentence = "On est le " + weekday + " " + str(dayNumber) + " "+ MonthList[date.today().month-1]
		print(sentence)
		hermes.publish_end_session(intentMessage.session_id, sentence)
	else :
		hermes.publish_end_session(intentMessage.session_id, "erreur!")

if __name__ == "__main__":
    with Hermes("localhost:1883") as h:
        h.subscribe_intent("ustaN:date", subscribe_intent_callback) \
.start()