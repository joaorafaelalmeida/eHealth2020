import argparse
import sys
import configparser
import time
from FileManager import FileManager
from Orchestrator import Orchestrator

def help(show=False):
	parser = argparse.ArgumentParser(description="")
	configs = parser.add_argument_group('Global settings', 'This settings are related with the location of the files and directories.')
	configs.add_argument('-s', '--settings', dest='settings', \
                        type=str, default="settings.ini", \
                        help='The system settings file (default: settings.ini)')	
	configs.add_argument('-ds', '--dataset', dest='dataset', type=str, default='train',\
                        help='The dataset used to process (train/dev/test).')	

	if show:
		parser.print_help()
	return parser.parse_args()

def readSettings(settingsFile):
	configuration = configparser.ConfigParser()
	configuration.read(settingsFile)
	if not configuration:
		raise Exception("The settings file was not found!")
	return configuration._sections

def main():
	args = help()
	settings = readSettings(args.settings)

	if args.dataset in settings:
		voc = FileManager.loadVocabularies(settings["vocabulary"])
		ds = FileManager.readDataset(settings[args.dataset])
		results = Orchestrator.process(args.dataset, voc, ds, settings)
		FileManager.writeResults(settings["results"], results)
	else:
		print("Dataset does not exist in the settings.ini")
		help(show=True)
		exit()

main()