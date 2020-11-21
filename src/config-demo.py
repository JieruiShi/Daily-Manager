#This file is to contain information based on the client's computer, filepath, customization, etc
#Rename the file config.py before use
import os
srcPath = os.path.dirname(os.path.realpath(__file__)) # Get the file path to src
prePath = srcPath[:-3] + 'presentables'

#todos module
#
# 1. filepath to store list of active todos
# 2. filepath to store list of archieved todos

TODO_FILEPATH = srcPath + r'\myPlans\todo.json' #Default the cache for to do in the folder my Plans
ARCHIEVE_FILEPATH = srcPath + r'\myPlans\archieve.json' #Default archieve.json in same folder as TODOs.py

#diary module
#
#1. filepath to diary document (Word, .docx format)

DIARY_FILEPATH = prePath + r'\diary.docx' #Default diary.docx in the same folder as myscripts, put full filepath to your diary!
DIARYCACHE_FILEPATH = srcPath + r'\Diary\diaryCache.json'

#overhead module
#
#1. filepath to overhead document (Excel, xlsx format)

OVERHEAD_FILEPATH = prePath + r'\overhead.xlsx'