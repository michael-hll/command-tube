# -*- coding: utf-8 -*-
#!/usr/bin/python

# ----------------------------------------------------------------
# Command Tube - A tool can run local and server commands together
#    GitHub: https://github.com/michael-hll/command-tube.git
#    Author: Michael Han
#     Email: michael_hll@outlook.com
# Copyright: @2021 @2022 
# ----------------------------------------------------------------

'''
<< About >>
Command Tube is a tool that can run a group of sequenced commands. 
You can get a full list of supportted tube commands from readme document.
'''
import os
import sys
from os import path
from pathlib import Path
import traceback
import subprocess
from datetime import datetime, timedelta, date
import time
import argparse
from argparse import ArgumentParser
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import xml.etree.ElementTree as ET
import math
from shutil import copyfile
import multiprocessing
from argparse import RawTextHelpFormatter
import uuid
import shlex
import shutil
from random import choice, randrange, paretovariate
import threading
import glob
import keyword

# -------- CLASSES --------------
class Storage():
    I = None
    def __init__(self) -> None:
        Storage.I = self     
        # -------- CONSTANTS START --------
        self.C_CURR_VERSION            = '2.0.2 Beta'  
        self.C_KEYWORDS                = set(keyword.kwlist)
        self.C_SUPPORT_FROM_VERSION    = 'SUPPORT_FROM_VERSION'     
        self.C_YAML_VERSION            = 'VERSION'        
        self.C_DATETIME_FORMAT         = '%Y-%m-%d %H:%M:%S'
        self.C_CURR_DIR                = os.getcwd()   
        self.C_TUBE_HOME               = 'TUBE_HOME' 
        self.C_OS_NAME                 = 'OS_NAME'
        self.C_SLEEP_SECONDS           = 1
        self.C_BUILD_SUCCESSFUL        = 'BUILD SUCCESSFUL'
        self.C_BUILD_FAILED            = 'BUILD FAILED'
        self.C_TUBE_SUCCESSFUL         = 'SUCCESSFUL'
        self.C_TUBE_PARTIAL_SUCCESSFUL = 'PARTIAL SUCCESSFUL'
        self.C_TUBE_FAILED             = 'FAILED'
        self.C_STATUS_LINE             = '------------------'    
        self.C_SUCCESSFUL              = 'SUCCESSFUL'
        self.C_FAILED                  = 'FAILED'
        self.C_SKIPPED                 = 'SKIPPED'
        self.C_RUNNING                 = 'RUNNING'
        # Tube Command names and parameters
        self.C_LINUX_COMMAND           = 'LINUX_COMMAND'
        self.C_PATH                    = 'PATH'
        self.C_COMMAND                 = 'COMMAND'
        self.C_GET_XML_TAG_TEXT        = 'GET_XML_TAG_TEXT'
        self.C_SET_XML_TAG_TEXT        = 'SET_XML_TAG_TEXT'
        self.C_SET_FILE_KEY_VALUE      = 'SET_FILE_KEY_VALUE'
        self.C_WRITE_LINE_IN_FILE      = 'WRITE_LINE_IN_FILE'
        self.C_NEW_LINE_BEFORE         = 'NEW_LINE_BEFORE'
        self.C_NEW_LINE_BEFORE_SHORT   = 'NLB'
        self.C_NEW_LINE_AFTER          = 'NEW_LINE_AFTER'
        self.C_NEW_LINE_AFTER_SHORT    = 'NLA'
        self.C_DELETE_LINE             = 'DELETE_LINE'
        self.C_DELETE_LINE_SHORT       = 'DL'
        self.C_DELETE_LINE_IN_FILE     = 'DELETE_LINE_IN_FILE'
        self.C_LINE_BEGINS             = 'LINE_BEGINS'   
        self.C_PAUSE                   = 'PAUSE'
        self.C_TAIL_FILE               = 'TAIL_FILE'
        self.C_REPORT_PROGRESS         = 'REPORT_PROGRESS'
        self.C_GET_FILE_KEY_VALUE      = 'GET_FILE_KEY_VALUE'
        self.C_EMAIL                   = 'EMAIL'
        self.C_EXEC                    = 'EXEC'
        self.C_COUNT                   = 'COUNT'
        self.C_SET_VARIABLE            = 'SET_VARIABLE'
        self.C_DELETE_VARIABLE         = 'DELETE_VARIABLE'
        self.C_SFTP_GET                = 'SFTP_GET'
        self.C_SFTP_PUT                = 'SFTP_PUT'
        self.C_CHECK_CHAR_EXISTS       = 'CHECK_CHAR_EXISTS'  
        self.C_REPLACE_CHAR            = 'REPLACE_CHAR'
        self.C_PRINT_VARIABLES         = 'PRINT_VARIABLES'
        self.C_PRINT                   = 'PRINT'
        self.C_RUN_TUBE                = 'RUN_TUBE'
        self.C_BREAK                   = 'BREAK'
        self.C_CONTINUE                = 'CONTINUE'
        self.C_READ_LINE_IN_FILE       = 'READ_LINE_IN_FILE'
        self.C_LIST_FILES              = 'LIST_FILES'
        self.C_LIST_DIRS               = 'LIST_DIRS'
        self.C_FILE_EXIST              = 'FILE_EXIST'
        self.C_FILE_POP                = 'FILE_POP'
        self.C_FILE_APPEND             = 'FILE_APPEND'
        self.C_FILE_PUSH               = 'FILE_PUSH'
        self.C_FILE_EMPTY              = 'FILE_EMPTY'
        self.C_FILE_READ               = 'FILE_READ'
        self.C_FILE_DELETE             = 'FILE_DELETE'
        self.C_FILE_COPY               = 'FILE_COPY'
        self.C_FILE_MOVE               = 'FILE_MOVE'
        self.C_FILE_CREATE             = 'FILE_CREATE'
        self.C_FILE_INSERT             = 'FILE_INSERT'
        self.C_FILE_SORT               = 'FILE_SORT'
        self.C_DIR_EXIST               = 'DIR_EXIST'
        self.C_DIR_DELETE              = 'DIR_DELETE'
        self.C_DIR_CREATE              = 'DIR_CREATE'
        self.C_TAIL_LINES_HEADER       = 'TAIL '
        self.C_LOG_HEADER              = '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\nCommand Tube Log starts at '
        self.C_JOB_HEADER              = '\n--------------------------------------\nJob starts at '
        self.C_FINISHED_HEADER         = '*** Command Tube Finished Status ***'
        self.C_CONTINUE_PARAMETER      = '--continue'
        self.C_REDO_PARAMETER          = '--redo'
        self.C_IF_PARAMETER            = '--if'
        self.C_KEY_PARAMETER           = '--key'
        self.C_NOTES_PARAMETER         = '--note'
        self.C_PLACE_HOLDER            = '--raw'
        self.C_INDENTATION             = '    '
        self.C_RETRIED_COMMAND_NOTE    = '* The star(*) after command type means the command is run again.'
        self.C_FAILED_COMMAND_LIST     = '----- Failed Command List -----'
        self.C_DESC_NEW_LINE_SPACE     = '             '
        self.C_ALIAS                   = 'ALIAS'
        self.C_HELP                    = '''Use optional 'args' argument you can set the tube file name or get tube help.
    Input 'tube-yaml-file' to override the --tube argument value.
    Input 'help commands [name]' to print all commands usages; With optional 'name' argument will only list command names.
    Input 'help command-name [name|desc|syntax|parameters|support]' to print all the tube commands which name matched.
    Input 'help general-arg-name' to print the general argument usage:
        'help continue' to view the --continue syntax;
        'help redo' to view the --redo syntax;
        'help if' to view the --if syntax;
        'help key' to view the --key syntax;
        'help raw' to view the --raw syntax;
        'help note' to view the --note syntax;
    Input 'help template' to view the tube tempalte;
    Input 'help variable' to view the tube variables usage;
    Input 'help vars' to print all the given tube variables;'''
        # Server used
        self.C_SERVERS                 = 'SERVERS'
        self.C_SERVER                  = 'SERVER'
        self.C_SERVER_NAME             = 'NAME'
        self.C_SERVER_HOST             = 'HOST'
        self.C_SERVER_PORT             = 'SSH_PORT'
        self.C_SERVER_USER             = 'USER'
        self.C_SERVER_PASSWORD         = 'PASSWORD'
        self.C_SERVER_ROOT             = 'ROOT'
        self.C_SERVER_PROFILE          = 'PROFILE'
        self.C_CONNECT                 = 'CONNECT'
        self.C_SSH_CONNECT_TIMEOUT     = 15 # seconds
        # Variables
        self.C_VARIABLES               = 'VARIABLES'
        # Tube Argument Used
        self.C_ARG_SYNTAX              = 'SYNTAX'
        self.C_ARG_ARGS                = 'ARGS'
        self.C_COMMAND_DESCRIPTION     = 'DESCRIPTION'
        # Run mode used
        self.C_RUN_MODE                = 'RUN_MODE'
        self.C_RUN_MODE_SRC            = 'SRC'
        self.C_RUN_MODE_BIN            = 'BIN' 
        self.C_RUN_MODE_DEBUG          = 'DEBUG'       
        # Current Version
        self.C_PROGRAM_NAME            = 'Command Tube'
        # Tube
        self.C_TUBE                    = 'TUBE'
        # Email
        self.C_EMAIL                   = 'EMAIL'
        self.C_EMAIL_SMTP_SERVER       = 'EMAIL_SMTP_SERVER'
        self.C_EMAIL_SERVER_PORT       = 'EMAIL_SERVER_PORT'
        self.C_EMAIL_SENDER_ADDRESS    = 'EMAIL_SENDER_ADDRESS'
        self.C_EMAIL_SENDER_PASSWORD   = 'EMAIL_SENDER_PASSWORD'
        self.C_EMAIL_RECEIVER_ADDRESS  = 'EMAIL_RECEIVER_ADDRESS'
        self.C_EMAIL_SUBJECT           = 'EMAIL_SUBJECT'
        # PRINT
        self.C_PRINT_PREFIX            = '[TUBE]'
        self.C_PRINT_PREFIX_EMPTY      = ''
        self.C_PRINT_TYPE_INFO         = 'INFO'
        self.C_PRINT_TYPE_WARNING      = 'WARNING'
        self.C_PRINT_TYPE_ERROR        = 'ERROR'
        self.C_PRINT_TYPE_DEBUG        = 'DEBUG'
        self.C_PRINT_TYPE_EMPTY        = ''
        self.C_PRINT_COLOR_RED         = (0,0,0)
        self.C_PRINT_COLOR_YELLOW      = (0,0,0)
        self.C_PRINT_COLOR_ORANGE      = (0,0,0)
        self.C_PRINT_COLOR_GREEN       = (0,0,0)
        self.C_PRINT_COLOR_BLUE        = (0,0,0)
        self.C_PRINT_COLOR_PURPLE      = (0,0,0)
        self.C_PRINT_COLOR_GREY        = (71,71,71)
        self.C_PRINT_COLOR_STYLE       = None
        # -------- CONSTANTS END --------
        # ************************************************************************
        # Run mode
        self.RUN_MODE                  = self.C_RUN_MODE_SRC        
        self.YAML_VERSION              = None
        # User inputs, these values should be all set well from config file
        self.EXEC_DATE_TIME            = '01/01/20 00:00:00'   
        self.GOTO_HOST_ROOT            = 'cd /' 
        # Some default input parameters
        self.IS_IMMEDIATE              = False
        self.IS_FORCE_RUN              = False
        self.IS_SENT_EMAIL             = False
        self.SERVERS                   = None 
        self.VARIABLES                 = None      
        self.TUBE_NAME                 = None # Main tube name        
        self.TUBE_YAML                 = None
        self.TUBE_YAML_FILE            = None
        self.TUBE_LOG_FILE             = 'tube.log'
        self.IS_CLEAR_LOG              = False
        self.IS_LOOP                   = False
        self.LOOP_TIMES                = 1024
        self.CURR_LOOP_ID              = 0
        self.NEXT_REFRESH              = 0
        self.PIP_NAME                  = 'pip'
        # Email configuration
        self.EMAIL_SMTP_SERVER         = 'smtp.live.com'
        self.EMAIL_SERVER_PORT         = 587
        self.EMAIL_SENDER_ADDRESS      = '<sender email address>'
        self.EMAIL_SENDER_PASSWORD     = '<sender email password>'
        self.EMAIL_RECEIVER_ADDRESS    = '<receiver email address comma list>'
        self.EMAIL_SUBJECT             = 'Command Tube Result'
        # global variables
        self.LOGS                      = []
        self.DISK_SPACE_STATUS         = {} 
        self.INSTALLED_PACKAGES        = []
        self.TUBE                      = None # Reference to the main tube instance
        self.TUBE_RUN                  = []  # Reference the main tube tube run list
        self.TUBE_LIST                 = []  # Hold all the instanced tube list        
        self.HOSTS                     = {}
        self.CURR_HOST                 = ''
        self.CURR_HOST_PROFILE         = ''
        self.CURR_HOST_ROOT            = ''
        self.START_DATE_TIME           = ''
        self.IS_STOP                   = False
        self.MAX_TUBE_COMMAND_LENGTH   = 10
        self.TUBE_FILE_LIST            = {}
        self.IS_MATRIX_MODE            = False
        self.IS_MATRIX_MODE_RUNNING    = False
        self.MATRIX_THREAD             = None
        self.IS_REPORT_PROGRESS        = False
        self.HAS_EMAIL_SETTINGS        = False
        self.EVAL_CODE_SET             = set()

        self.__gen_tube_args()
        
    def __gen_tube_args(self):
        # Tube Command argument configurations design details
        # 0: Is postion arguments
        # 1: -  Short argument name. eg: -f (if you want leave it empty, then only put '-' value)
        # 2: -- Long argument anme. eg: --force
        # 3: type
        # 4: nargs
        # 5: destination
        # 6: is required
        # 7: has action
        # 8: action
        # 9: default 
        # LAST: description
        self.TUBE_ARGS_CONFIG = {  
            self.C_RUN_TUBE: {                
                self.C_SUPPORT_FROM_VERSION: '2.0.2',
                self.C_ALIAS: {'RUN'},
                self.C_ARG_ARGS: [
                    [True, '-','--', 'str', '+', 'tube', True, False, '', '',
                        'The tube you want to run. It supports 3 formats: \
                         \n{0}        - \'file.yaml\': Run TUBE from file.yaml file. With this format the global variables in file.xml will also be imported. \
                         \n{0}        - \'file[X]\': Run tube X from file.yaml file. \
                         \n{0}        - \'X\': Run tube X from the current yaml file.'.format(Storage.I.C_DESC_NEW_LINE_SPACE)],    
                    [False, '-v','--variables', 'str', '+', 'variables', False, False, '', '',
                        'Pass local variable key values to sub tube. format: -v v1 = 1, v2 = \'Command Tube\''], 
                    [False, '-w','--while', 'str', '+', 'conditions', False, False, '', '',
                        'Set the while condtions to run the tube: --while <eval-expression-condition>'],  
                    [False, '-e','--each', 'str', '+', 'each', False, False, '', '',
                        'Set the foreach loop arguments with format: --each [index_name,] item_name in list_name'],
                    [False, '-f','--for', 'str', '+', 'each', False, False, '', '',
                        'The alias of --each argument.'],                      
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_KEY_PARAMETER: True,
                self.C_PLACE_HOLDER: True,
                self.C_NOTES_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Run a sub-tube. \n{0:13s}With the \'--while\' conditions provided, {1} will continuely run and stop when conditions return false. \
                                             \n{0:13s}With the \'--each\' parameters provided, {1} will iterate the list variable and run the sub-tube.' \
                                             .format(' ', self.C_RUN_TUBE)
            }, 
            self.C_BREAK: {                
                self.C_SUPPORT_FROM_VERSION: '2.0.2',
                self.C_ALIAS: {'BREAK'},
                self.C_ARG_ARGS: [
                    [True, '-','--', 'str', '*', 'reason', False, False, '', '',
                        'The reason you want to break. [Optional]'],
                ],
                self.C_CONTINUE_PARAMETER: False,
                self.C_REDO_PARAMETER: False,
                self.C_IF_PARAMETER: True,
                self.C_KEY_PARAMETER: True,
                self.C_PLACE_HOLDER: True,
                self.C_NOTES_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'The command can break a tube\'s running.'
            },   
            self.C_CONTINUE: {                
                self.C_SUPPORT_FROM_VERSION: '2.0.2',
                self.C_ALIAS: {'CONTINUE'},
                self.C_ARG_ARGS: [
                    [True, '-','--', 'str', '*', 'reason', False, False, '', '',
                        'The reason you want to continue. [Optional]'],
                ],
                self.C_CONTINUE_PARAMETER: False,
                self.C_REDO_PARAMETER: False,
                self.C_IF_PARAMETER: True,
                self.C_KEY_PARAMETER: True,
                self.C_PLACE_HOLDER: True,
                self.C_NOTES_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'The command can continue a tube\'s running while it\'s in a loop.'
            },                 
            self.C_TAIL_FILE: {
                self.C_SUPPORT_FROM_VERSION: '2.0.0',
                self.C_ALIAS: {'TAIL'},
                self.C_ARG_ARGS: [        
                    [False, '-f','--file', 'str', '+', 'file', True, False, '', '',
                        'The text file you want to tail.'],
                    [False, '-l','--lines', 'str', 1, 'lines', True, False, '', '',
                        'The lines count you want to output.'],
                    [False, '-k','--keywords', 'str', '*', 'keywords', False, False, '', '',
                        'Output start from the given keywords.'],       
                    [False, '-r','--result', 'str', 1, 'result', False, False, '', '',
                        'The text file to store the tail result.'],    
                    [False, '-v','--variable', 'str', 1, 'variable', False, False, '', '',
                        'The tube variable name to store the tail result as lines.'],
                    [False, '-u','--force', '', '', 'is_force', False, True, 'store_true', False, 
                        'Force update even the variable is readonly. Default no.'],  
                    [False, '-g','--global', '', '', 'is_global', False, True, 'store_true', False,
                        'If update the variable in global tube variables. Default no.'],           
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_KEY_PARAMETER: True,
                self.C_PLACE_HOLDER: True,
                self.C_NOTES_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Print/Log the last N lines of given file.'                
            },
            self.C_FILE_EXIST: {
                self.C_SUPPORT_FROM_VERSION: '2.0.2',
                self.C_ALIAS: {'F_EXIST'},
                self.C_ARG_ARGS: [        
                    [False, '-f','--file', 'str', 1, 'file', True, False, '', '',
                        'The file name you want to check.'],
                    [False, '-v','--variable', 'str', 1, 'variable', True, False, '', '',
                        'The tube variable name to store the exist result. (True/False)'],
                    [False, '-u','--force', '', '', 'is_force', False, True, 'store_true', False, 
                        'Force update even the variable is readonly. Default no.'],  
                    [False, '-g','--global', '', '', 'is_global', False, True, 'store_true', False,
                        'If update the variable in global tube variables. Default no.'],                    
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_KEY_PARAMETER: True,
                self.C_PLACE_HOLDER: True,
                self.C_NOTES_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Check if a file exists.'                
            },
            self.C_FILE_POP: {
                self.C_SUPPORT_FROM_VERSION: '2.0.2',
                self.C_ALIAS: {'F_POP'},
                self.C_ARG_ARGS: [        
                    [True, '-','--', 'str', '*', 'file', False, False, '', '',
                        'The text file name you want to pop.'],
                    [False, '-f','--file', 'str', 1, 'afile', False, False, '', '',
                        'The text file name you want to pop. It will override the file argument.'],
                    [False, '-v','--variable', 'str', 1, 'variable', False, False, '', '',
                        'The tube variable name to store the line content result.'],  
                    [False, '-n','--number', 'str', 1, 'number', False, False, '', '',
                        'The line number you want to pop. Default 1 to pop the first line. -1 to pop the last line.'],  
                    [False, '-u','--force', '', '', 'is_force', False, True, 'store_true', False, 
                        'Force update even the variable is readonly. Default no.'],  
                    [False, '-g','--global', '', '', 'is_global', False, True, 'store_true', False,
                        'If update the variable in global tube variables. Default no.'],               
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_KEY_PARAMETER: True,
                self.C_PLACE_HOLDER: True,
                self.C_NOTES_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Pop one line of the given text file. If there is no line there then store empty.'                
            },
            self.C_FILE_APPEND: {
                self.C_SUPPORT_FROM_VERSION: '2.0.2',
                self.C_ALIAS: {'F_APPEND'},
                self.C_ARG_ARGS: [        
                    [False, '-f','--file', 'str', '+', 'file', True, False, '', '',
                        'The text file name you want to append.'],
                    [False, '-v','--value', 'str', '+', 'value', True, False, '', '',
                        'The content you want to append to the text file.'],                
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_KEY_PARAMETER: True,
                self.C_PLACE_HOLDER: True,
                self.C_NOTES_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Append the content to the last line of the given text file.'                
            },
            self.C_FILE_PUSH: {
                self.C_SUPPORT_FROM_VERSION: '2.0.2',
                self.C_ALIAS: {'F_PUSH'},
                self.C_ARG_ARGS: [        
                    [False, '-f','--file', 'str', 1, 'file', True, False, '', '',
                        'The text file name you want to push.'],
                    [False, '-v','--value', 'str', '+', 'value', True, False, '', '',
                        'The content you want to push to the text file.'],                
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_KEY_PARAMETER: True,
                self.C_PLACE_HOLDER: True,
                self.C_NOTES_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Push the content to the first line of the given text file.'                
            },
            self.C_FILE_INSERT: {
                self.C_SUPPORT_FROM_VERSION: '2.0.2',
                self.C_ALIAS: {'F_INSERT'},
                self.C_ARG_ARGS: [        
                    [False, '-f','--file', 'str', '+', 'file', True, False, '', '',
                        'The file you want to insert.'],
                    [False, '-n','--number', 'str', 1, 'number', True, False, '', '',
                        'The line number you want to inert. 1 means the first line, -1 means the last line.'], 
                    [False, '-v','--value', 'str', '+', 'value', True, False, '', '',
                        'The line you want to insert into the file.'],                                       
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_KEY_PARAMETER: True,
                self.C_PLACE_HOLDER: True,
                self.C_NOTES_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Insert a line before given line number. If line number doesnot exist then insert to the end.'                    
            },
            self.C_FILE_SORT: {
                self.C_SUPPORT_FROM_VERSION: '2.0.2',
                self.C_ALIAS: {'F_SORT'},
                self.C_ARG_ARGS: [        
                    [True, '-','--', 'str', '*', 'file', False, False, '', '',
                        'The file you want to sort.'],
                    [False, '-f','--file', 'str', 1, 'afile', False, False, '', '',
                        'The file you want to sort. It will override file argument.'],
                    [False, '-n','--number', '', '', 'is_number', False, True, 'store_true', False,
                        'If sort file line content as numbers. Default No.'],
                    [False, '-s','--sort', 'str', 1, 'sort', False, False, '', '',
                        'Default value is asc. You can set value \'desc\' to reverse the sorting.'],                                       
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_KEY_PARAMETER: True,
                self.C_PLACE_HOLDER: True,
                self.C_NOTES_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Sort a text file lines content.'                    
            },
            self.C_FILE_EMPTY: {
                self.C_SUPPORT_FROM_VERSION: '2.0.2',
                self.C_ALIAS: {'F_EMPTY'},
                self.C_ARG_ARGS: [        
                    [True, '-','--', 'str', '*', 'file', False, False, '', '',
                        'The text file name you want to empty.'],     
                    [False, '-f','--file', 'str', 1, 'afile', False, False, '', '',
                        'The text file name you want to empty. It will override the file argument.'], 
                    [False, '-c','--create', '', '', 'is_create', False, True, 'store_true', False,
                        'If the give file doesnot exist if create a new empty file. Default No.'],         
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_KEY_PARAMETER: True,
                self.C_PLACE_HOLDER: True,
                self.C_NOTES_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Clear an existing text file or create a new empty file.'                
            },
            self.C_FILE_CREATE: {
                self.C_SUPPORT_FROM_VERSION: '2.0.2',
                self.C_ALIAS: {'F_CREATE'},
                self.C_ARG_ARGS: [        
                    [True, '-','--', 'str', '*', 'file', False, False, '', '',
                        'The text file name you want to create.'],      
                    [False, '-f','--file', 'str', 1, 'afile', False, False, '', '',
                        'The text file name you want to create. It will override the file argument.'],      
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_KEY_PARAMETER: True,
                self.C_PLACE_HOLDER: True,
                self.C_NOTES_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Create an empty file.'                
            },
            self.C_FILE_READ: {
                self.C_SUPPORT_FROM_VERSION: '2.0.2',
                self.C_ALIAS: {'F_READ'},
                self.C_ARG_ARGS: [        
                    [False, '-f','--file', 'str', '+', 'file', True, False, '', '',
                        'The file name you want to read its whole content.'],
                    [False, '-c','--content', 'str', 1, 'content', False, False, '', '',
                        'The tube variable name to store the file content.'],
                    [False, '-l','--lines', 'str', 1, 'lines', False, False, '', '',
                        'The tube variable name to store the file content as lines.'],   
                    [False, '-s','--skip-empty', '', '', 'skip_empty', False, True, 'store_true', False, 
                        'If skip empty lines. Default no.'],  
                    [False, '-u','--force', '', '', 'is_force', False, True, 'store_true', False, 
                        'Force update even the variable is readonly. Default no.'],  
                    [False, '-g','--global', '', '', 'is_global', False, True, 'store_true', False,
                        'If update the variable in global tube variables. Default no.'],                    
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_KEY_PARAMETER: True,
                self.C_PLACE_HOLDER: True,
                self.C_NOTES_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Read a file content to tube variable. Doesn\'t include the new-line (\\n) char.'                
            },
            self.C_FILE_DELETE: {
                self.C_SUPPORT_FROM_VERSION: '2.0.2',
                self.C_ALIAS: {'F_DELETE', 'F_DEL'},
                self.C_ARG_ARGS: [        
                    [True, '-','--', 'str', '*', 'file', False, False, '', '',
                        'The file name you want to delete.'], 
                    [False, '-f','--file', 'str', 1, 'afile', False, False, '', '',
                        'The text file name you want to delete. It will override the file argument.'],
                    [False, '-r','--result', 'str', 1, 'result', False, False, '', '',
                        'The text file to store deleted files result.'],                   
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_KEY_PARAMETER: True,
                self.C_PLACE_HOLDER: True,
                self.C_NOTES_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Delete any files math the file name.'                
            },
            self.C_FILE_COPY: {
                self.C_SUPPORT_FROM_VERSION: '2.0.2',
                self.C_ALIAS: {'F_COPY', 'F_CP'},
                self.C_ARG_ARGS: [        
                    [False, '-s|-f','--src|--from', 'str', '+', 'src', True, False, '', '',
                        'The source file name you want to copy.'],  
                    [False, '-d|-t','--dest|--to', 'str', '+', 'dest', True, False, '', '',
                        'The target file or folder'],                  
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_KEY_PARAMETER: True,
                self.C_PLACE_HOLDER: True,
                self.C_NOTES_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Copy any files to target.'                
            },
            self.C_FILE_MOVE: {
                self.C_SUPPORT_FROM_VERSION: '2.0.2',
                self.C_ALIAS: {'F_MOVE', 'F_MV'},
                self.C_ARG_ARGS: [        
                    [False, '-s|-f','--src|--from', 'str', '+', 'src', True, False, '', '',
                        'The source file name you want to move.'],  
                    [False, '-d|-t','--dest|--to', 'str', '+', 'dest', True, False, '', '',
                        'The target file or folder'],                  
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_KEY_PARAMETER: True,
                self.C_PLACE_HOLDER: True,
                self.C_NOTES_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Move any files to target.'                
            },
            self.C_DIR_EXIST: {
                self.C_SUPPORT_FROM_VERSION: '2.0.2',
                self.C_ALIAS: {'D_EXIST'},
                self.C_ARG_ARGS: [    
                    [False, '-d','--dir', 'str', 1, 'directory', True, False, '', '',    
                        'The directory you want to check.'],
                    [False, '-v','--variable', 'str', 1, 'variable', True, False, '', '',
                        'The tube variable name to store the exist result. (True/False)'],
                    [False, '-u','--force', '', '', 'is_force', False, True, 'store_true', False, 
                        'Force update even the variable is readonly. Default no.'],  
                    [False, '-g','--global', '', '', 'is_global', False, True, 'store_true', False,
                        'If update the variable in global tube variables. Default no.'],                    
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_KEY_PARAMETER: True,
                self.C_PLACE_HOLDER: True,
                self.C_NOTES_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Check if a directory exists.'                
            },
            self.C_DIR_CREATE: {
                self.C_SUPPORT_FROM_VERSION: '2.0.2',
                self.C_ALIAS: {'D_CREATE'},
                self.C_ARG_ARGS: [        
                    [True, '-','--', 'str', 1, 'directory', True, False, '', '',
                        'The directory you want to create.'],                  
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_KEY_PARAMETER: True,
                self.C_PLACE_HOLDER: True,
                self.C_NOTES_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Create a directory if it doesnot exist.'                
            },
            self.C_DIR_DELETE: {
                self.C_SUPPORT_FROM_VERSION: '2.0.2',
                self.C_ALIAS: {'D_DELETE', 'D_DEL'},
                self.C_ARG_ARGS: [        
                    [True, '-','--', 'str', 1, 'directory', True, False, '', '',
                        'The directory you want to delete.'],                   
                    [False, '-f','--force', '', '', 'is_force', False, True, 'store_true', False, 
                        'Force delete if the director is not empty. Default no.'],
                    [False, '-r','--result', 'str', 1, 'result', False, False, '', '',
                        'The text file to store deleted directory result.'], 
                ],                  
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_KEY_PARAMETER: True,
                self.C_PLACE_HOLDER: True,
                self.C_NOTES_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Delete a directory and its sub-directories.'                
            },
            self.C_DELETE_LINE_IN_FILE: {
                self.C_SUPPORT_FROM_VERSION: '2.0.0',
                self.C_ALIAS: {'DELETE_LINE', 'DEL_LINE', 'DEL_LN'},
                self.C_ARG_ARGS: [        
                    [False, '-f','--file', 'str', '+', 'file', True, False, '', '',
                        'The file you want to delete lines from.'],
                    [False, '-n','--number', 'str', 1, 'number', False, False, '', '',
                        'The line number you want to delete. 1 is the first line, -1 is the last line.'], 
                    [False, '-b','--begins', 'str', '+', 'begins', False, False, '', '',
                        'The line begins with character you want to delete.'],
                    [False, '-c','--contains', 'str', '+', 'contains', False, False, '', '',
                        'The line contains with character you want to delete.'],
                    [False, '-e','--empty', '', '', 'del_empty', False, True, 'store_true', False,
                        'A flag to tell if delete empty line. Default no.'],
                    [False, '-r','--result', 'str', 1, 'result', False, False, '', '',
                        'The text file to store deleted result.'], 
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_KEY_PARAMETER: True,
                self.C_PLACE_HOLDER: True,
                self.C_NOTES_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Conditionally delete lines from a file.'
            },  
            self.C_READ_LINE_IN_FILE: {
                self.C_SUPPORT_FROM_VERSION: '2.0.2',
                self.C_ALIAS: {'READ_LINE', 'READ_LN'},
                self.C_ARG_ARGS: [        
                    [False, '-f','--file', 'str', '+', 'file', True, False, '', '',
                        'The file you want to read a line from.'],
                    [False, '-n','--number', 'str', 1, 'number', True, False, '', '',
                        'The line number you want to read. 1 is the first line, -1 is the last line. If the number is greater than file lines then return the last line.'], 
                    [False, '-v','--variable', 'str', 1, 'variable', True, False, '', '',
                        'The tube variable name to save the line content.'],
                    [False, '-u','--force', '', '', 'is_force', False, True, 'store_true', False,
                        'Force update even the varialbe is readonly. Default no.'],
                    [False, '-g','--global', '', '', 'is_global', False, True, 'store_true', False,
                        'If update the variable in global tube variables. Default no.'],
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_KEY_PARAMETER: True,
                self.C_PLACE_HOLDER: True,
                self.C_NOTES_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Read one line by given line number, and save the line content to tube variable.'
            }, 
            self.C_WRITE_LINE_IN_FILE: {
                self.C_SUPPORT_FROM_VERSION: '2.0.0',
                self.C_ALIAS: {'WRITE_LINE', 'WRITE_LN'},
                self.C_ARG_ARGS: [        
                    [False, '-f','--file', 'str', '+', 'file', True, False, '', '',
                        'The file you want to update.'],
                    [False, '-v','--value', 'str', '+', 'value', True, False, '', '',
                        'The character value you want to update in the file.'],
                    [False, '-n','--number', 'str', 1, 'number', False, False, '', '',
                        'The line number you want to update. If not provided then append the value to the file.'],                    
                    [False, '-c','--contains', 'str', '+', 'contains', False, False, '', '',
                        'Only update the line if it contains the given characters content.'],
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_KEY_PARAMETER: True,
                self.C_PLACE_HOLDER: True,
                self.C_NOTES_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Write any characters into a file.'                    
            },    
            self.C_SET_FILE_KEY_VALUE: {
                self.C_SUPPORT_FROM_VERSION: '2.0.0',
                self.C_ALIAS: {'SET_KEY'},
                self.C_ARG_ARGS: [        
                    [False, '-f','--file', 'str', '+', 'file', True, False, '', '',
                        'The file you want to update.'],
                    [False, '-k','--keywords', 'str', '+', 'keywords', True, False, '', '',
                        'The key in the left side of \'=\'.'],
                    [False, '-v','--value', 'str', '*', 'value', True, False, '', '',
                        'The value in the right side of \'=\'.'],
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_KEY_PARAMETER: True,
                self.C_PLACE_HOLDER: True,
                self.C_NOTES_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Update key-value file.'
            },
            self.C_GET_XML_TAG_TEXT: {
                self.C_SUPPORT_FROM_VERSION: '2.0.0',
                self.C_ALIAS: {'GET_XML_TAG'},
                self.C_ARG_ARGS: [        
                    [False, '-f','--file', 'str', '+', 'file', True, False, '', '',
                        'The XML file you want to get tag text.'],
                    [False, '-x','--xpath', 'str', '+', 'xpath', True, False, '', '',
                        'The xpath of the XML tag.'],
                    [False, '-v','--variable', 'str', 1, 'variable', False, False, '', '',
                        'The tube variable name to store the value. [2.0.2]'],
                    [False, '-u','--force', '', '', 'is_force', False, True, 'store_true', False, 
                        'Force update even the variable is readonly. Default no. [2.0.2]'],
                    [False, '-g','--global', '', '', 'is_global', False, True, 'store_true', False,
                        'If update the variable in global tube variables. Default no. [2.0.2]'],                    
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_KEY_PARAMETER: True,
                self.C_PLACE_HOLDER: True,
                self.C_NOTES_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Get XML file tag text value. \
                                           \nThe result will be stored into a tube variable and xpath will be used as the variable name.'
            },
            self.C_SET_XML_TAG_TEXT: {
                self.C_SUPPORT_FROM_VERSION: '2.0.0',
                self.C_ALIAS: {'SET_XML_TAG'},
                self.C_ARG_ARGS: [        
                    [False, '-f','--file', 'str', '+', 'file', True, False, '', '',
                        'The XML file you want tup set tag text.'],
                    [False, '-x','--xpath', 'str', '+', 'xpath', True, False, '', '',
                        'The xpath of the XML tag'],
                    [False, '-v','--value', 'str', '+', 'value', True, False, '', '',
                        'The new value of the tag.'],
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_KEY_PARAMETER: True,
                self.C_PLACE_HOLDER: True,
                self.C_NOTES_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Update XML file tag text using xpath.'
            },
            self.C_SET_VARIABLE: {
                self.C_SUPPORT_FROM_VERSION: '2.0.0',
                self.C_ALIAS: {'SET_VAR', 'SET'},
                self.C_ARG_ARGS: [   
                    [True, '-','--', 'str', '*', 'expression', False, False, '', '',
                        'Assign variable value with format: var_name = expression, var_name["keyword"] = expression or var_name[index] = expression; \
                         \n{0:18s}You can also use operator +=, *=, /+ to make the assignment eaiser: i += 1, i += -1 etc;  \
                         \n{0:18s}Or you can use --name, --keyword, --index, --value arguments to set the variable value explicitly.'.format(' ')],     
                    [False, '-n','--name', 'str', 1, 'name', False, False, '', '',
                        'The tube variable name you want to set.'],
                    [False, '-k','--keyword', 'str', 1, 'keyword', False, False, '', '',
                        'If update a dictional type variable, this --keyword value is to set the dict key.'],
                    [False, '-i','--index', 'str', 1, 'index', False, False, '', '',
                        'If update a list type variable, this --index value is to set list index.'],
                    [False, '-v','--value', 'str', '*', 'value', False, False, '', '',
                        'The tube variable value you want to set. \n  \
                Note: The backend is using \'eval(expression)\' so you can do more things, eg: \n \
                    - set_var: -n dayOfWeek -v datetime.today().weekday() # Tube variable dayOfWeek will be set to weekday() value. \n \
                    - set_var: ls = [1,2,3] # Tube variable ls was updated to list value: [1,2,3]. \n \
                    - set_var: ls = ls.append(4) # Tube variable ls appended value 4 to its end: [1,2,3,4].'],
                    [False, '-r','--readonly', '', '', 'is_readonly', False, True, 'store_true', False,
                        'Mark the variable as readonly after updating. Default no. [2.0.2]'],
                    [False, '-u','--force', '', '', 'is_force', False, True, 'store_true', False,
                        'Force update even the varialbe is readonly. Default no. [2.0.2]'],
                    [False, '-g','--global', '', '', 'is_global', False, True, 'store_true', False,
                        'If set the variable to global (Main TUBE).\n \
                 With this flag, it will try to find the first variable from current and its parent tube chain that mathes the input variable name, and update its value. \n \
                 If found nothing then the variable will be updated in the main tube. \n \
                 Without this flag, it will update the variable in current tube. \n \
                 Default no. [2.0.2]'],
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_KEY_PARAMETER: True,
                self.C_PLACE_HOLDER: True,
                self.C_NOTES_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Set tube variable value.'
            },
            self.C_DELETE_VARIABLE: {
                self.C_SUPPORT_FROM_VERSION: '2.0.2',
                self.C_ALIAS: {'DELETE_VAR', 'DEL_VAR'},
                self.C_ARG_ARGS: [      
                    [True, '-','--', 'str', '+', 'name', True, False, '', '',  
                        'The tube variable name you want to delete from current tube.'],
                    [False, '-g','--global', '', '', 'is_global', False, True, 'store_true', False,
                        'With --global parameter you can delete it from current and its parent tubes.'],
                    [False, '-a','--all', '', '', 'is_del_all', False, True, 'store_true', False,
                        'With --all parameter you can delete it from all tubes.'],
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_KEY_PARAMETER: True,
                self.C_PLACE_HOLDER: True,
                self.C_NOTES_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Delete tube variables.'
            },
            self.C_CONNECT: {
                self.C_SUPPORT_FROM_VERSION: '2.0.0',
                self.C_ALIAS: {'CONN'},
                self.C_ARG_ARGS: [        
                    [True, '-','--', 'str', '+', 'host', True, False, '', '',
                        'The Linux server host or name you want to connect using SSH protocal.'],
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_KEY_PARAMETER: True,
                self.C_PLACE_HOLDER: True,
                self.C_NOTES_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'You can use this command to switch your server connection.'
            },
            self.C_REPORT_PROGRESS: {
                self.C_SUPPORT_FROM_VERSION: '2.0.0',
                self.C_ALIAS: {'REPORT_PRO'},
                self.C_ARG_ARGS: [        
                    [True, '-','--', 'str', '+', 'subject', True, False, '', '',
                        'The email subject/title you want to set.'],
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_KEY_PARAMETER: True,
                self.C_PLACE_HOLDER: True,
                self.C_NOTES_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'You can use this command to sent current progress via Email.'
            },
            self.C_PAUSE: {
                self.C_SUPPORT_FROM_VERSION: '2.0.0',
                self.C_ALIAS: {'PAUZE'},
                self.C_ARG_ARGS: [        
                    [True, '-','--', 'str', '+', 'minutes', True, False, '', '',
                        'The minutes you want to pause. You can end it with \'s\' char to pause for xxx seconds.'],
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_KEY_PARAMETER: True,
                self.C_PLACE_HOLDER: True,
                self.C_NOTES_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Command Tube will pause with given minutes/seconds.'
            },
            self.C_PATH: {
                self.C_SUPPORT_FROM_VERSION: '2.0.0',
                self.C_ALIAS: {'CD'},
                self.C_ARG_ARGS: [        
                    [True, '-','--', 'str', '+', 'directory', True, False, '', '',
                        'The directory you want to goto.'],
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_KEY_PARAMETER: True,
                self.C_PLACE_HOLDER: True,
                self.C_NOTES_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Go to specific directory.'
            },
            self.C_GET_FILE_KEY_VALUE: {
                self.C_SUPPORT_FROM_VERSION: '2.0.0',
                self.C_ALIAS: {'GET_KEYS'},
                self.C_ARG_ARGS: [    
                    [False, '-f','--file', 'str', '+', 'file', True, False, '', '',
                        'The file you want to get key-value from.'],    
                    [False, '-k','--keywords', 'str', '+', 'keywords', False, False, '', '',
                        'The key you want to get values from the file. It supports comma seperated format for multiple keys.'],  
                    [False, '-u','--force', '', '', 'is_force', False, True, 'store_true', False,
                        'Force update even the variable is readonly. Default no. [2.0.2]'],
                    [False, '-g','--global', '', '', 'is_global', False, True, 'store_true', False,
                        'If update the variable in global tube variables. Default no. [2.0.2]'],
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_KEY_PARAMETER: True,
                self.C_PLACE_HOLDER: True,
                self.C_NOTES_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Read key values from key-value file. \
                                           \nIt also supports to read key-value from Yaml file with simple type. \
                                           \nThe key-value results will be stored into tube variables.'
            },
            self.C_EMAIL: {
                self.C_SUPPORT_FROM_VERSION: '2.0.0',
                self.C_ALIAS: {'MAIL'},
                self.C_ARG_ARGS: [        
                    [False, '-t','--to', 'str', '+', 'to', True, False, '', '',
                        'The sending email addresses.'],
                    [False, '-s','--subject', 'str', '+', 'subject', True, False, '', '',
                        'The email title.'],
                    [False, '-b','--body', 'str', '+', 'body', True, False, '', '',
                        'The email content. If it\'s text file name, then the content of the file will be as the email content.'],
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_KEY_PARAMETER: True,
                self.C_PLACE_HOLDER: True,
                self.C_NOTES_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Sent Email to someone with given subject and content.'
            },
            self.C_EXEC: {
                self.C_SUPPORT_FROM_VERSION: '2.0.2',
                self.C_ALIAS: {'EXEC'},
                self.C_ARG_ARGS: [        
                    [True, '-','--', 'str', '+', 'commands', True, False, '', '',
                        'The python commands.'],
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_KEY_PARAMETER: True,
                self.C_PLACE_HOLDER: True,
                self.C_NOTES_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'The python commands you want to run. The original idea is to use it to import other python modules. \
                         \nThen you can use the newly imported module in set or condition expressions.'
            },
            self.C_COMMAND: {
                self.C_SUPPORT_FROM_VERSION: '2.0.0',
                self.C_ALIAS: {'CMD'},
                self.C_ARG_ARGS: [        
                    [True, '-','--', 'str', '+', 'command', True, False, '', '',
                        'Any command you want to run.'],     
                    [False, '-','--result', 'str', 1, 'result', False, False, '', '',
                        'The text file to store command outputs. [2.0.2]'],            
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_KEY_PARAMETER: True,
                self.C_PLACE_HOLDER: True,
                self.C_NOTES_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Run any Windows/MacOS terminal command.'
            },
            self.C_LINUX_COMMAND: {
                self.C_SUPPORT_FROM_VERSION: '2.0.0',
                self.C_ALIAS: {'LCMD','SSHCMD'},
                self.C_ARG_ARGS: [        
                    [True, '-','--', 'str', '+', 'command', True, False, '', '',
                        'Any Linux command you want to run.'], 
                    [False, '-','--log-detail', '', '', 'is_log_detail', False, True, 'store_true', False,
                        'Log command output to tube log file. Default no. [2.0.2]'],                 
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_KEY_PARAMETER: True,
                self.C_PLACE_HOLDER: True,
                self.C_NOTES_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Run a Linux command from the previous connected server.'                
            },
            self.C_COUNT: {
                self.C_SUPPORT_FROM_VERSION: '2.0.0',
                self.C_ALIAS: {'CNT'},
                self.C_ARG_ARGS: [        
                    [False, '-f','--file', 'str', '+', 'file', False, False, '', '',
                        'The file you want to count line numbers.'],
                    [False, '-t','--tube|--status', 'str', '+', 'tube', False, False, '', '',
                        'The tube command status you want to count.'],
                    [False, '-v','--variable', 'str', '+', 'variable', True, False, '', '',
                        'The tube variable name to store the count result.'],
                    [False, '-c','--current', '', '', 'current_tube', False, True, 'store_true', False,
                        'If only count current tube. Default no.'],
                    [False, '-s','--skip', '', '', 'skip_count', False, True, 'store_true', False,
                        'If skip COUNT command. Default no.'],
                    [False, '-u','--force', '', '', 'is_force', False, True, 'store_true', False, 
                        'Force update even the variable is readonly. Default no. [2.0.2]'], 
                    [False, '-g','--global', '', '', 'is_global', False, True, 'store_true', False,
                        'If update the variable in global tube variables. Default no. [2.0.2]'],
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_KEY_PARAMETER: True,
                self.C_PLACE_HOLDER: True,
                self.C_NOTES_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Count file lines number (-f) or Count tube command number by status (-t).' 
            },
            self.C_SFTP_GET: {
                self.C_SUPPORT_FROM_VERSION: '2.0.1',
                self.C_ALIAS: {'FTP_GET'},
                self.C_ARG_ARGS: [        
                    [False, '-r','--remotepath', 'str',  1,  'remotepath', True, False, '', '',
                        'The file full remotepath.'],
                    [False, '-l','--localpath',  'str',  1,  'localpath', True, False, '', '',
                        'The file localpath.'],
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_KEY_PARAMETER: True,
                self.C_PLACE_HOLDER: True,
                self.C_NOTES_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Using SSHClient to copy remote server file to local. \
                                           \nWhen copy multiple files using *.* then localpath must be a directory.'
            },
            self.C_SFTP_PUT: {
                self.C_SUPPORT_FROM_VERSION: '2.0.1',
                self.C_ALIAS: {'FTP_PUT'},
                self.C_ARG_ARGS: [        
                    [False, '-l','--localpath',  'str',  1,  'localpath', True, False, '', '',
                        'The file localpath.'],                    
                    [False, '-r','--remotepath', 'str',  1,  'remotepath', True, False, '', '',
                        'The file full remotepath.'],
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_KEY_PARAMETER: True,
                self.C_PLACE_HOLDER: True,
                self.C_NOTES_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Using SSHClient to put local file to remote server. \
                                           \nWhen copy multiple files using *.* then remotepath must be a directory.'
            },
            self.C_CHECK_CHAR_EXISTS: {
                self.C_SUPPORT_FROM_VERSION: '2.0.1',
                self.C_ALIAS: {'CHECK_CHAR'},
                self.C_ARG_ARGS: [        
                    [False, '-f','--file',  'str', '+',  'file', True, False, '', '',
                        'The file you want to check.'],                    
                    [False, '-c','--char',  'str', '+',  'characters', True, False, '', '',
                        'The characters you want to check.'],
                    [False, '-v','--variable', 'str', 1,   'variable', True, False, '', '',
                        'The tube variable name to store the checking result.'], 
                    [False, '-u','--force', '', '', 'is_force', False, True, 'store_true', False, 
                        'Force update even the variable is readonly. Default no. [2.0.2]'], 
                    [False, '-g','--global', '', '', 'is_global', False, True, 'store_true', False,
                        'If update the variable in global tube variables. Default no. [2.0.2]'],
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_KEY_PARAMETER: True,
                self.C_PLACE_HOLDER: True,
                self.C_NOTES_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Check if given characters exists from a file. Result was updated into a tube variable.'
            },
            self.C_REPLACE_CHAR: {
                self.C_SUPPORT_FROM_VERSION: '2.0.1',
                self.C_ALIAS: {'REPLACE'},
                self.C_ARG_ARGS: [        
                    [False, '-f','--file',  'str', '+',  'file', True, False, '', '',
                        'The file you want to replace given characters.'],                    
                    [False, '-o','--oldvalue',  'str', '+',  'oldvalue', True, False, '', '',
                        'The oldvalue you want to replace (Support regular expressions).'],
                    [False, '-n','--newvalue', 'str', '+',   'newvalue', True, False, '', '',
                        'The newvalue to replace.'],
                    [False, '-c','--count', 'str', 1,   'count', False, False, '', '',
                        'The replaced times you want to set. Default 1.'],
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_KEY_PARAMETER: True,
                self.C_PLACE_HOLDER: True,
                self.C_NOTES_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Replace file line content which contains/matches given value.'
            },
            self.C_PRINT_VARIABLES: {
                self.C_SUPPORT_FROM_VERSION: '2.0.2',
                self.C_ALIAS: {'PRINT_VARS'},
                self.C_ARG_ARGS: [        
                    [True, '-','--', 'str', '+', 'name', True, False, '', '',
                        'The tube variable name. With value \'*\' or \'.\' can print all variables.'],
                    [False, '-r','--result', 'str', 1, 'result', False, False, '', '',
                        'The text file to store the result.'],  
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_KEY_PARAMETER: True,
                self.C_PLACE_HOLDER: True,
                self.C_NOTES_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Print tube variable values for debugging purpose.'
            },
            self.C_PRINT: {
                self.C_SUPPORT_FROM_VERSION: '2.0.2',
                self.C_ALIAS: {'ECHO'},
                self.C_ARG_ARGS: [        
                    [True, '-','--', 'str', '+', 'message', True, False, '', '',
                        'The message you want to print in the terminal.'],
                    [False, '-c','--color', 'str', 1, 'color', False, False, '', '',
                        'The message color you want to use. You can use color name \'red\' or \'FF0000\' to set the color value.'],  
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_KEY_PARAMETER: True,
                self.C_PLACE_HOLDER: True,
                self.C_NOTES_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Print a message to the console for debugging purpose.'
            },
            self.C_LIST_FILES: {
                self.C_SUPPORT_FROM_VERSION: '2.0.2',
                self.C_ALIAS: {'LIST_F'},
                self.C_ARG_ARGS: [      
                    [False, '-d','--dir', 'str', 1, 'directory', False, False, '', '',  
                        'The directory with file name matchings. If not provided then use default *.* to list all files. eg: <directory>/*.* or *.jpg'],
                    [False, '-f','--file', 'str', 1, 'afile', False, False, '', '',  
                        'The files name you want to list. If not provided then use default *.* to list all files. eg: <directory>/*.* or *.jpg'],
                    [False, '-r','--result', 'str', 1, 'result', False, False, '', '',
                        'The text file to store the search result.'], 
                    [False, '-s','--sort', 'str', '+', 'sort', False, False, '', '',
                        'Using \'-s atime|mtime|ctime|name|size [asc|desc]\' to set the sort properties. Default uses the file modification mtime (mtime asc) to sort the result.'],
                    [False, '-c','--count', 'str', 1, 'count', False, False, '', '',
                        'The tube variable name to store the files count.'],
                    [False, '-v','--variable', 'str', 1, 'variable', False, False, '', '',
                        'The tube variable name to store the list result.'],
                    [False, '-u','--force', '', '', 'is_force', False, True, 'store_true', False, 
                        'Force update even the variable is readonly. Default no.'],  
                    [False, '-g','--global', '', '', 'is_global', False, True, 'store_true', False,
                        'If update the variable in global tube variables. Default no.'], 
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_KEY_PARAMETER: True,
                self.C_PLACE_HOLDER: True,
                self.C_NOTES_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Get matched files list and save it to a text file or variable.'
            },
            self.C_LIST_DIRS: {
                self.C_SUPPORT_FROM_VERSION: '2.0.2',
                self.C_ALIAS: {'LIST_D'},
                self.C_ARG_ARGS: [        
                    [False, '-d','--dir', 'str', 1, 'directory', True, False, '', '', 
                        'The directory you want to list its sub directories.'],
                    [False, '-r','--result', 'str', 1, 'result', False, False, '', '',
                        'The text file to store the list result.'], 
                    [False, '-s','--sort', 'str', '+', 'sort', False, False, '', '',
                        'It accepts \'asc\' or \'desc\' value for the sorting. Default is \'asc\'.'],
                    [False, '-c','--count', 'str', 1, 'count', False, False, '', '',
                        'The tube variable name to store the directories count.'],
                    [False, '-v','--variable', 'str', 1, 'variable', False, False, '', '',
                        'The tube variable name to store the list result.'],
                    [False, '-u','--force', '', '', 'is_force', False, True, 'store_true', False, 
                        'Force update even the variable is readonly. Default no.'],  
                    [False, '-g','--global', '', '', 'is_global', False, True, 'store_true', False,
                        'If update the variable in global tube variables. Default no.'], 
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_KEY_PARAMETER: True,
                self.C_PLACE_HOLDER: True,
                self.C_NOTES_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Got all sub directories for the given directory, and save the result list to a text file or variable.'
            },
        }

class TDict(dict):
    '''
    This class is used to replace the placehoders from the command
    in case the key doesn't exists in the tube variables list.
    Using this TDict it will not raise key missing error
    '''
    def __missing__(self, key):
        return '{' + key + '}'
    
class Utility():
    
    @classmethod
    def check_file_exists(self, file, *exts):
        '''
        *exts: if file doesn't exist than check if file+ext exits
        
        Return (exists, file_full_path)
        '''
        f = file
        # exists
        if path.exists(f) and not path.isdir(f):
            return (True, os.path.abspath(f))
        if path.exists(f) and path.isdir(f):
            # then try exts
            for ext in exts:
                if path.exists(f + ext) and not path.isdir(f + ext):
                    return(True, os.path.abspath(f + ext))
        # not exists
        if not path.exists(f):
            for ext in exts:
                if path.exists(f + ext) and not path.isdir(f + ext):
                    return(True, os.path.abspath(f + ext))
        return (False, f)

    @classmethod
    def read_password_from_file(self, file, key):
        '''
        file: A key=value file.
        
        Return (found, password)
        '''
        exists, _ = Utility.check_file_exists(file)
        if exists == True:
            with open(file, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    line = line.replace('\n', '')
                    if key in line and '=' in line:
                        i = line.index('=')
                        line_key = line[0:i].strip()
                        line_value = line[i+1:].strip()
                        if key == line_key:
                            return (True, line_value)
        return (False, None)

    @classmethod
    def get_file_size(self, file_full_name, unit):
        '''     
        Return file size in unit.

        Parameters:
            unit: Unit could be 'KB', 'MB', 'GB' or 'TB'. Other value will return size in bytes
        '''

        if path.exists(file_full_name):
            file_size = os.stat(file_full_name).st_size
            if unit == 'KB':
                return file_size / math.pow(1024, 1)
            elif unit == 'MB':
                return file_size / math.pow(1024, 2)
            elif unit == 'GB':
                return file_size / math.pow(1024, 3)
            elif unit == 'TB':
                return file_size / math.pow(1024, 4)
            else:
                return file_size
        else:
            return 0

    @classmethod
    def read_file_content(self, file):
        '''
        Retrun all file content
        
        Parameters:
            file: the file you want to read content from.
        '''
        
        exists, file = Utility.check_file_exists(file)
        if exists == True:
            with open(file, 'r') as f:
                lines = f.readlines()
                return ''.join(lines)
        else:
            raise Exception('File not found: ' + file)

    @classmethod
    def add_tag_namespace(self, el, temp_namespace):
        '''
        Check all xml element, add namesapce back from temp_namespace
        and delete the temp_namesapce attribute
        '''
        for sub_el in el:
            if temp_namespace in sub_el.attrib.keys():
                sub_el.tag = sub_el.attrib[temp_namespace] + sub_el.tag
                del sub_el.attrib[temp_namespace]
            Utility.add_tag_namespace(sub_el, temp_namespace)
        if temp_namespace in el.attrib.keys():
            el.tag = el.attrib[temp_namespace] + el.tag
            del el.attrib[temp_namespace]

    @classmethod
    def replace_str_ignorecase(self, from_str, to_str, source_str, is_strip=True):
        '''
        Replace from_str to to_str ignorecases
        
        Return replace result
        '''   
        
        insensitive_replace = re.compile(re.escape(from_str), re.IGNORECASE)
        return_str = insensitive_replace.sub(to_str, source_str)
        if is_strip == True:
            return_str = return_str.strip()
        return return_str

    @classmethod
    def get_original_key_value(self, line, *args):
        '''
        If the original key was commented by #, REM then the
        #, or REM will be removed from returned key
        
        *args: The characters in this list will be ignored.
        
        retrun: (key, value)
        '''    
        if not '=' in line:
            return ('', '')
        line_array = line.split('=', 1)
        original_key = line_array[0].strip()
        comment_keys = ['#', 'REM']
        if len(args) > 0:
            comment_keys = args
        for comment_key in comment_keys:
            original_key = Utility.replace_str_ignorecase(comment_key, '', original_key)
            
        return (original_key, line_array[1].strip())

    @classmethod
    def get_key_count(self, key, lines):   
        '''
        This method could help to check the how many times of the given key occured.
        
        if the key is commented out with #, REM, it will be counted too
        
        Parameters:
            key: the key you want to count
            lines: the key-value file content in list format (without \\n character)
        ''' 
        count = 0
        if key == None or lines == None:
            return count

        for line in lines:
            if '=' in line:
                original_key = Utility.get_original_key_value(line, '#', 'REM')[0]
                if key.upper() == original_key.upper():
                    count += 1
        return count

    @classmethod
    def get_datetime_difference(self, large_date, small_date):
        '''
        Return two datetime gaps in format: X DAYS, X HOURS, X MINUTES, X SECONDS
        '''
        duration      = large_date - small_date
        duration_in_s = duration.total_seconds() 
        days          = divmod(duration_in_s, 86400)       
        hours         = divmod(days[1], 3600)              
        minutes       = divmod(hours[1], 60)                
        seconds       = divmod(minutes[1], 1)   
        return str(int(days[0])) + ' DAYS, ' + str(int(hours[0])) + ' HOURS, ' + str(int(minutes[0])) + ' MINUTES, ' + str(int(seconds[0])) + ' SECONDS'

    @classmethod
    def format_duration_unit(self, duration: float, unit='HOURS'):
        
        '''
        Unit could be 'HOURS', 'MINUTES' or 'DAYS'
        
        return (duraion, unit)
        '''
        
        if duration < 1.0:
            duration = duration * 60.0
            unit = 'MINUTES'
        elif duration > 24.0:
            duration = duration / 24.0
            unit = 'DAYS'
        
        return (duration, unit)
    
    @classmethod
    def reset_yes_no_character(self, *args):
        '''
        If arg in uppercase equal 'YES' or 'NO', then set it to 'True' or 'False';
        
        If arg in uppercase equal 'TRUE' or 'FALSE', then set it to 'True' or 'False';
        
        Return (arg1,arg2,...argN)
        '''
        if not args:
            return args
        
        returns = []
        
        for arg in args:
            if type(arg) != str:
                returns.append(arg)
                continue
            if arg.upper() == 'YES':
                returns.append('True')
            elif arg.upper() == 'NO':
                returns.append('False')
            elif arg.upper() == 'TRUE':
                returns.append('True')
            elif arg.upper() == 'FALSE':
                returns.append('False')
            else:
                returns.append(arg)
        
        return (i for i in returns)           
    
    @classmethod
    def convert_arg_values_to_set(self, value_list):
        '''
        Convert  value list to a set collection
        '''
        return_set = set()
        for item in value_list:
            if ',' in item:
                item_array = item.split(',')
                for i in item_array:
                    if i:
                        return_set.add(i)
            else:
                return_set.add(item)
        return return_set
    
    @classmethod
    def safe_load_yaml_with_upper_key(self, f):
        data = yaml.safe_load(f)
        Utility.make_dict_key_upper(data)
        return data    
    
    @classmethod
    def make_dict_key_upper(self, yaml):
        '''
        Skip the key value is list type key (skip tube key)
        '''
        if not yaml or type(yaml) is not dict:
            return
        
        deleted_keys = []
        
        # make the key upper cases
        keys = [k for k in yaml.keys()]
        for key in keys:
            if key != key.upper() and type(yaml[key]) != list:
                yaml[key.upper()] = yaml[key]
                deleted_keys.append(key)
        
        # deleted not upper case key/value
        for key in deleted_keys:
            del yaml[key]   
    
    @classmethod
    def safe_load_yaml(self, f):
        with open(f, 'r') as f:
            data = yaml.safe_load(f)
            return data
    
    @classmethod
    def eval_while_conditions(self, while_condition: str, is_main = True, command = None):
        result = True
        if while_condition != None: 
            while_condition = command.self_format_placeholders(while_condition, is_quoted_str = True)
            result = Utility.eval_conditions(while_condition.split(' '), command) == True  
        elif while_condition == None and is_main == False:
            result = False
        return result
   
    @classmethod
    def eval_conditions(self, conditions = [], command = None):
        '''
        Use python eval method to evaluate the input conditions in list format
        
        Args:
            condtions: []
        '''       
        is_holder_exists = [ True if '{' in item else False for item in conditions]    
        is_holder_exists = True in is_holder_exists
        conditions_trim = [command.self_format_placeholders(item.strip(), is_quoted_str = True) for item in conditions]
        conditions_trim = ['True' if Utility.equal_true(item) else item for item in conditions_trim]
        conditions_trim = ['False' if Utility.equal_false(item) else item for item in conditions_trim]
        conditions_str = ' '.join(conditions_trim)
        if Utility.if_compare_char_exists(conditions_str): 
            # if cound contionds char we use the normal eval method to do check the condition
            code = compile(conditions_str, '<string>', 'eval')    
            local_dict = {}
            # Add the missing codes into local varialbes as str
            for name in code.co_names:
                kv = command.tube.get_first_key_value(name) if is_holder_exists == False else None
                if is_holder_exists == False and kv != None:
                    local_dict[name] = kv
                    continue
                if name in Storage.I.EVAL_CODE_SET:
                    continue
                if not name in globals().keys():
                    local_dict[name] = str(name)                        
            if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:
                msg = 'The eval parameter is: {0}, local dict: {1}, running command is {2}.'.format(conditions_str, local_dict, command.get_full_content())
                tprint(msg, type=Storage.I.C_PRINT_TYPE_DEBUG)
                write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
            return eval(conditions_str, globals(), local_dict)
        else:
            # no conditions char exist case
            if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:
                msg = 'The condition is: \'{0}\', running command is \'{1}\'.'.format(conditions_str, command.get_full_content())
                tprint(msg, type=Storage.I.C_PRINT_TYPE_DEBUG)
                write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
            # for the cases don't contain ==, >, <, != etc
            if ' ' in conditions_str:
                # for 'condtion1 condition2 case'
                for value in conditions_trim:
                    if is_holder_exists == False:
                        kv = command.tube.get_first_key_value(value) 
                        value = kv if kv != None else value
                    if Utility.equal_false(value):
                        return False
            else:
                # for 'condition' case
                if is_holder_exists == False:
                    kv = command.tube.get_first_key_value(conditions_str) 
                    conditions_str = kv if kv != None else conditions_str
                if Utility.equal_false(conditions_str):
                    return False 
        return True
    
    @classmethod
    def if_compare_char_exists(self, value):
        '''
        Check if '=', '!=', '>', '<' exists from a string value
        '''
        value = str(value)
        if '=' in value or '>' in value or \
           '!=' in value or '<' in value or \
            'not' in value.lower() or \
            'and' in value.lower():
               return True
        return False
    
    @classmethod
    def equal_false(self, value):
        '''
        If value equal 'NO' or 'FALSE' then return True
        Otherwise return False
        '''
        value = str(value).strip('"').strip('\'')
        if value.upper() == 'NO' or value.upper() == 'FALSE':
            return True
        return False
    
    @classmethod
    def equal_true(self, value):
        '''
        If value equal 'YES' or 'TRUE' then return True
        Otherwise return False
        '''
        value = str(value).strip('"').strip('\'')
        if value.upper() == 'YES' or value.upper() == 'TRUE':
            return True
        return False
    
    @classmethod
    def replace_empty_dict(self, input_dict):
        '''
        Replace '' string value to "''" and return a new copy the original dict
        '''
        tempDict = input_dict.copy()
        for key in tempDict.keys():
            if tempDict[key] == '':
                tempDict[key] = "''"
        return tempDict
    
    @classmethod
    def convert_value_auto(self, value):
        '''
        If value is int, float, bool then convert it automatically
        '''
        value_temp = value
        if reUtility.is_matched_int(value_temp):
            value = int(value_temp)
        elif reUtility.is_matched_float(value_temp):
            value = float(value_temp)
        elif Utility.equal_true(value_temp):
            value = True
        elif Utility.equal_false(value_temp):
            value = False
        
        return value

    @classmethod
    def split_assign_expression(self, item, command=None):
        '''
        Split equal expressions 'name = value or name["key"] = value'
        Return (name, value) or (name, key, value)
        '''
        item = item.strip()
        if reUtility.is_matched_assign_expresson(item):
            name = item[:item.index('=')].strip()
            value = item[item.index('=')+1:].strip()
            value = Utility.convert_value_auto(value)
        
            return (name, value) 
        
        elif reUtility.is_matched_assign_dict_expresson(item):
            name_key = item[:item.index('=')].strip()
            value = item[item.index('=')+1:].strip()
            left_bracket_index = name_key.index('[')
            right_bracket_index = name_key.index(']')
            name = name_key[:left_bracket_index].strip()
            key = name_key[left_bracket_index + 2 : right_bracket_index - 1]

            return (name, key, value)
        
        elif reUtility.is_matched_assign_list_expresson(item):
            name_index = item[:item.index('=')].strip()
            value = item[item.index('=')+1:].strip()
            indexes = []
            matches = re.findall('[\[][a-zA-Z0-9]+[\]]', name_index)
            for match in matches:
                index_tmp = match.strip('[').strip(']')
                index = Utility.eval_expression(index_tmp, command.tube)
                indexes.append(int(index))
            left_bracket_index = name_index.index('[')
            name = name_index[:left_bracket_index].strip()

            return (name, indexes, value)
        else:
            return (None, None)

    @classmethod
    def split_each_expression(self, each: str, tube):
        '''
        return (index_name, item_name, ls_instance)
        '''
        index_name = None
        item_name = None
        ls = None
        if reUtility.is_matched_each_item_expresson(each):
            each_list = re.split(' +', each)
            item_name = each_list[0]
            ls_name = each_list[2]
            ls = tube.get_first_key_value(ls_name)
            if ls == None or type(ls) != list:
                raise Exception('List doesnot exist: {0}'.format(ls_name))
            
        elif reUtility.is_matched_each_index_item_expresson(each):
            each_list_temp = each.split(',')
            index_name = each_list_temp[0].strip()
            each_list = re.split(' +', each_list_temp[1].strip())
            item_name = each_list[0]
            ls_name = each_list[2]
            ls = tube.get_first_key_value(ls_name)
            if ls == None or type(ls) != list:
                raise Exception('List doesnot exist: {0}'.format(ls_name))
        
        return(index_name, item_name, ls)
        
    @classmethod
    def quote_dict_str_value(self, d):
        d_new = {}
        for k in d.keys():
            if type(d[k]) == str and not (d[k].startswith('\'') or d[k].startswith('"')):
                d_new[k] = '"' + d[k] + '"'   
            else:
                d_new[k] = d[k]
        return d_new

    @classmethod
    def quoted_with_space_characters(self, value):
        if value == None or value == '':
            return '\'\''
        if len(value) > 0 and value.strip() == 0:
            return '\'' + value + '\''
        if len(value) > 0 and (value.startswith(' ') or value.endswith(' ')):
            return '\'' + value + '\''
        else:
            return value

    @classmethod
    def gen_eval_code_set(self):
        Storage.I.EVAL_CODE_SET = set.union(
            set(dir(__builtins__)),
            set(dir(str)),
            set(dir(int)),
            set(dir(float)),
            set(dir(bool)),
            set(dir(list)),
            set(dir(dict)),
            set(dir(set)),
            set(dir(datetime)))

    @classmethod
    def write_result_to_file(self, file, lines):
        with open(file, 'w') as f:
            if len(lines) == 0:
                f.write('')
            for i, line in enumerate(lines):
                if i == 0:
                    f.write(line)
                else:
                    f.write('\n' + line)

    @classmethod
    def eval_expression(self, expression: str, tube, var_name: str = None):
        '''
        Args:

        expression: the expression you want to eval
        tube: the tube to trigger this eval
        var_name: this parameter is used to for the collections method
        '''
        if expression != None and type(expression) != str:
            return expression

        # evalulate eval inputs
        try:
            # if cound contionds char we use the normal eval method to do check the condition
            code = compile(expression, '<string>', 'eval')    
            local_dict = {}
            # Add the missing codes into local varialbes as str
            for code in code.co_names:
                kv = tube.get_first_key_value(code)
                if kv != None:
                    local_dict[code] = kv
                    continue
                if code in Storage.I.EVAL_CODE_SET:
                    if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:
                        msg = 'Code \'{0}\' is in the EVAL_CODE_SET.'.format(
                            code
                        )
                        tprint(msg, type=Storage.I.C_PRINT_TYPE_DEBUG)
                        write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
                    continue
                if not code in globals().keys():
                    local_dict[code] = str(code)                       
            if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:
                msg = 'The current expression is: {0}, local_dict: {1}'.format(
                    expression, local_dict
                )
                tprint(msg, type=Storage.I.C_PRINT_TYPE_DEBUG)
                write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
            expression = eval(expression, globals(), local_dict)  
            # In order to achieve the list, dict, set methods operations
            # we can use the local_dict value as the expression returns
            # Since most of the collections method don't return the collection itself
            # then we can achieve this set method:
            # - set: ls = ls.append('xxx')
            if var_name and var_name in local_dict.keys():
                var_type = type(local_dict[var_name])
                expression_type = type(expression)
                if var_type != expression_type and (var_type == list or var_type == dict or var_type == set):
                    expression_before = expression
                    expression = local_dict[var_name]   
                    if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:
                        msg = 'The expression was updated from \'{0}\' to \'{1}\''.format(
                            expression_before, expression
                        )
                        tprint(msg, type=Storage.I.C_PRINT_TYPE_DEBUG)
                        write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)       
        except Exception as e:
            if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:
                tprint(str(e), type=Storage.I.C_PRINT_TYPE_ERROR)
                write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', str(e))
        finally:
            return expression

class reUtility():

    # regular expression to match: {name}|{name:format}|{name[0/i]}|{name[0/i]:format}|{name["key"]}|{name["key"]:format}
    RE_MATCH_PLACEHOLDER = '(\{([a-zA-Z_0-9]+)(\[[a-zA-Z_0-9]+\]|\[[\"|\'][a-zA-Z_0-9]+[\"|\']\]){,2}(:[^:\{\}]+)?\})'
    P_PlaceHolder: re.Pattern = re.compile(RE_MATCH_PLACEHOLDER)

    # 1 = key, 2 = list index: [0][0], 5 = dict key, 6 = operator: +, -, *, /  7 = value
    RE_MATCH_ASSIGN_PLUS = '(([a-zA-Z0-9_]+)((\[[a-zA-Z0-9_]+\]){,2})(\[[\'\"]([a-zA-Z0-9_]+)[\'\"]\])?[ ]?([\+\*\/]{1})\=[ ]?([^\=]+))'
    P_AssignPlus: re.Pattern = re.compile(RE_MATCH_ASSIGN_PLUS)
    
    @staticmethod
    def is_matched_assign_expresson(input_value):
        '''
        To see if match 'x = y' expression 
        '''
        p = '[a-zA-Z_0-9]+[ ]*[=]{1}[ ]*[\S ]+'
        prog = re.compile(p)
        return prog.fullmatch(input_value) != None
    
    @staticmethod
    def is_matched_assign_dict_expresson(input_value: str):
        '''
        To see if match 'x["key"] = y' expression 
        '''
        p = '[a-zA-Z_0-9]+[\[]{1}["|\']{1}[a-zA-Z_0-9]+["|\']{1}[\]]{1}[ ]*[=]{1}[ ]*[\S ]+'
        prog = re.compile(p)
        return prog.fullmatch(input_value) != None
    
    @staticmethod
    def is_matched_assign_list_expresson(input_value: str):
        '''
        To see if match 'x[index] = y' expression 
        '''
        p = '[a-zA-Z_0-9]+([\[][a-zA-Z_0-9]+[\]])+[ ]*[=]{1}[ ]*[\S ]+'
        prog = re.compile(p)
        return prog.fullmatch(input_value) != None

    @staticmethod
    def is_matched_assign_plus_expression(input_value: str):
        '''
        To see if match 'x += 1' expression
        '''
        return reUtility.P_AssignPlus.fullmatch(input_value) != None

    @staticmethod
    def is_matched_each_item_expresson(input_value: str):
        '''
        To see if match 'item in ls' expression 
        '''
        p = '[a-zA-Z_0-9]+[ ]+in{1}[ ]+[a-zA-Z_0-9]+'
        prog = re.compile(p)
        return prog.fullmatch(input_value) != None
    
    @staticmethod
    def is_matched_each_index_item_expresson(input_value: str):
        '''
        To see if match 'index, item in ls' expression 
        '''
        p = '[a-zA-Z_0-9]+[ ]*[,]{1}[ ]*[a-zA-Z_0-9]+[ ]+in{1}[ ]+[a-zA-Z_0-9]+'
        prog = re.compile(p)
        return prog.fullmatch(input_value) != None

    @staticmethod
    def is_matched_int(input_value: str):
        '''
        To see if match int value
        '''
        p = '[1-9]+[0-9]*'
        prog = re.compile(p)
        return prog.fullmatch(input_value) != None
    
    @staticmethod
    def is_matched_float(input_value: str):
        '''
        To see if match float value
        '''
        p = '[1-9]+[.]*[0-9]*|[.]+[0-9]+'
        prog = re.compile(p)
        return prog.fullmatch(input_value) != None
 
class TubeCommandArgument():
    
    def __init__(self, shot_flag=None, full_flag=None, type=None, 
                 nargs=None, dest=None, required=False, is_inputs=False) -> None:
        self.short_flag = shot_flag
        self.long_flag = full_flag
        self.type = type
        self.nargs = nargs
        self.dest = dest
        self.required = required
        self.is_inputs = is_inputs
        self.has_action = False
        self.action = None
        self.default = None
        self.flags = []
    
    def gen_flags(self):
        if self.short_flag and self.short_flag != '-':
            flags = self.short_flag.split('|')
            for flag in flags:
                self.flags.append(flag)
        if self.long_flag and self.long_flag != '--':
            flags = self.long_flag.split('|')
            for flag in flags:
                self.flags.append(flag)

class TubeCommandArgumentConfig():
        
    def __init__(self, type, config_dict) -> None:
        self.type = type
        self.tube_command_arguments = []
        self.is_support_continue = False
        self.is_support_redo = False
        self.is_support_if_run = False
        self.is_support_key = False  
        self.is_support_notes = False     
        self.is_support_placeholder = False
        self.syntax = None        
        
        if self.type in config_dict.keys():
            self.syntax = TubeCommand.get_command_syntax(self.type, Storage.I.TUBE_ARGS_CONFIG)
            self.is_support_continue = config_dict[self.type][Storage.I.C_CONTINUE_PARAMETER]
            self.is_support_redo = config_dict[self.type][Storage.I.C_REDO_PARAMETER]  
            self.is_support_if_run = config_dict[self.type][Storage.I.C_IF_PARAMETER] 
            self.is_support_key = config_dict[self.type][Storage.I.C_KEY_PARAMETER]         
            self.is_support_notes = config_dict[self.type][Storage.I.C_NOTES_PARAMETER]  
            self.is_support_placeholder = config_dict[self.type][Storage.I.C_PLACE_HOLDER]         
            self.__load_arguments(config_dict)
        
    def __load_arguments(self, config_dict):
        if self.type in config_dict.keys():
            args_array = config_dict[self.type][Storage.I.C_ARG_ARGS]
            for item in args_array:
                argument = TubeCommandArgument()
                argument.is_inputs  = item[0]
                argument.short_flag = item[1]
                argument.long_flag  = item[2]
                argument.type       = item[3]
                argument.nargs      = item[4]
                argument.dest       = item[5]
                argument.required   = item[6]
                argument.has_action = item[7]
                argument.action     = item[8]
                argument.default    = item[9]
                argument.gen_flags()
                self.tube_command_arguments.append(argument)

class TubeArgumentParser(ArgumentParser):  
    
    argument_error = []
    argument_config = None
    
    def error(self, message):
        self.argument_error.append('ERROR: %s' % (message))
        
    def get_formated_errors(self):
        errors = []
        for err in self.argument_error:
            errors.append(err)
        if len(self.argument_error) > 0: 
            errors.append(TubeCommand.get_command_syntax(self.argument_config.type, Storage.I.TUBE_ARGS_CONFIG))            
        return errors    

    @classmethod
    def create_argument_parser(self, argument_config: TubeCommandArgumentConfig):
        
        new_parser = TubeArgumentParser(allow_abbrev=False, prog=argument_config.type, add_help=False)
        new_parser.argument_config = argument_config
        
        # add arguments
        argument: TubeCommandArgument
        for argument in argument_config.tube_command_arguments:
            if argument.is_inputs:   
                # position arguments             
                new_parser.add_argument(argument.dest, type=type(argument.type), nargs=argument.nargs)
            else:
                # optional arguments
                if not argument.has_action:
                    # without action
                    new_parser.add_argument(*argument.flags, type=type(argument.type), nargs=argument.nargs, required=argument.required, dest=argument.dest)
                else:
                    # store value to action
                    new_parser.add_argument(*argument.flags, dest=argument.dest, action=argument.action, default=argument.default, required=argument.required)

        # check general arguments
        if argument_config.is_support_continue:
            new_parser.add_argument(Storage.I.C_CONTINUE_PARAMETER, dest='continue_steps', type=int, nargs='*', required=False)
        if argument_config.is_support_redo:
            new_parser.add_argument(Storage.I.C_REDO_PARAMETER, type=int, nargs='*', required=False)
        if argument_config.is_support_if_run:
            new_parser.add_argument(Storage.I.C_IF_PARAMETER, dest='if_run', type=str, nargs='+', required=False)
        if argument_config.is_support_key:
            new_parser.add_argument(Storage.I.C_KEY_PARAMETER, dest='key', action='store_true', default=False, required=False)
        if argument_config.is_support_placeholder:
            new_parser.add_argument(Storage.I.C_PLACE_HOLDER, dest='is_raw', action='store_true', default=False, required=False)
        if argument_config.is_support_notes:
            new_parser.add_argument(Storage.I.C_NOTES_PARAMETER, dest='notes', type=str, nargs='+', required=False)        
        return new_parser

class TubeCommand():
    
    def __init__(self, cmd_type, content) -> None:
        self.cmd_type                   = cmd_type
        self.command_type               = StorageUtility.get_command_type(cmd_type)
        self.uuid                       = str(uuid.uuid4())
        self.original_uuid              = self.uuid
        # contents
        self.content                    = content
        self.original_content           = content
        self.has_content                = True
        self.notes                      = ''
        self.redo_content               = None
        # continue & redo properties
        self.is_failed_redo             = False
        self.redo_steps                 = 0
        self.is_failed_continue         = False
        self.success_skip_steps         = 0 # Success skip steps -> n
        self.is_success_skip            = False
        self.fail_skip_steps            = 0 # failed skip steps -> m
        self.is_fail_skip               = False
        self.is_skip                    = False
        self.is_skip_by_if              = False
        self.is_skip_by_while           = False
        self.is_redo_added              = False
        self.if_run                     = True
        self.index                      = None       
        self.has_syntax_error           = False        
        self.log: TubeCommandLog        = TubeCommandLog(self)
        self.is_single_placeholder      = False
        self.has_placeholders           = False
        self.is_key_command             = False
        self.is_raw                     = False
        self.results: list              = []       
        self.tube: Tube                 = None # The current command's tube container
        self.sub_tube: Tube             = None # The RUN_TUBE command points to the sub tube
        self.loop_index                 = -1
        
        # Private properties
        self.__original_content2   = None # content without place holders  
        
        # check None/empty content
        if self.content == None:
            self.content = ''
        if not self.content and self.command_type != Storage.I.C_BREAK and \
                self.command_type != Storage.I.C_CONTINUE:
            self.has_content = False
            return
                
        # to convert type int/float to str        
        if type(content) is int or type(content) is float:
            self.content = str(self.content)
            self.redo_content = str(self.redo_content)
         
        # check if it's single placeholder
        # for single placeholder we could replace the place holder     
        if type(self.content) is dict:
            keys = [k for k in self.content.keys()]
            # if it's single placeholder
            if keys and len(keys) == 1 and self.content[keys[0]] == None:
                self.is_single_placeholder = True   
                self.has_placeholders = True
                self.content = '{' + keys[0] + '}'
                self.original_content = self.content            
                
        # check if command content has place holders
        if type(self.content) is str:
            if '{' in self.content and '}' in self.content:
                self.has_placeholders = True            
                
        # init command type    
        self.tube_argument_config = TubeCommandArgumentConfig(self.command_type, Storage.I.TUBE_ARGS_CONFIG)
        self.tube_argument_parser = TubeArgumentParser.create_argument_parser(self.tube_argument_config)
    
    def __create_sub_tube(self, data, tube_type, tube_name, file, conditions):
        if tube_type == 3: # to run a yaml file case
            if tube_name not in data.keys() and tube_name.lower() in data.keys():
                tube_name = tube_name.lower()
            elif tube_name not in data.keys() and tube_name.title() in data.keys():
                tube_name = tube_name.title()
        if tube_name in data.keys():
            sub_tube_yaml = data[tube_name]
            if not sub_tube_yaml or type(sub_tube_yaml) != list:
                raise Exception('Tube {0} doesnot exist from or no commands list: {1}.'.format(tube_name, file))
            tube_index = StorageUtility.get_tube_index(file, tube_name)
            self.sub_tube = Tube(file, tube_name, tube_index, sub_tube_yaml, self.tube)
            self.sub_tube.tube_conditions = conditions
            self.sub_tube.tube_run_times = 0 # initial the tube running times to 0
        else:
            # the 'TUBE' section doesn't exists from the sub-tube file
            raise Exception('\'{0}\' section doesnot exists from tube file: {1}'.format(tube_name, file))

    def update_key_value(self, key, value, is_override=True, is_force=False, is_readonly=False, is_global=False) -> bool:
        '''
        If is_global is true, then udpate the key,value in global 
        Otherwise update the key,value in current command's tube scope
        
        Args:
            key: The key you want to update
            value: The value of the key
            is_override: Is override existing key.
            is_force: Is update readonly key.
            is_readonly: Is set the key as readonly in its scope.
            is_global: If update the key,value in global scope.
        '''
        if is_global == True:
            exists, tube_first = self.tube.find_key_from_tubes(key)
            # if found exists parent tubes has this key, then update the first found tube
            if exists:
                return tube_first.update_key_value(key, value, is_force=is_force, is_readonly=is_readonly, is_override=is_override)
            else:
                # else we set the global key-value to the root tube
                return Storage.I.TUBE.update_key_value(key, value, is_force=is_force, is_readonly=is_readonly, is_override=is_override)

        # if not found from parent tubes, then update the key-value in current tube
        return self.tube.update_key_value(key, value, 
                is_force=is_force, is_readonly=is_readonly, is_override=is_override)
                  
    def get_formatted_status(self) -> str:
        '''
        Return something like: '[0] - status - type: content
        '''
        status = 'NOT STARTED'
        if self.log and self.log.status != None:
            status = self.log.status
        index = 0
        if self.index != None:
            index = self.index
        return '[%s] - [%s] - %s: %s' % (str(index), status, self.cmd_type, self.get_formatted_content())

    def get_formatted_type(self, include_tube=True, include_index=False):
        '''
        Return something like: [0:TUBE] >>> COMMAND
        '''   
        command_type = ''
        if include_tube:
            tube_format_name = '[' + str(self.tube.tube_index) + ':' + self.tube.tube_name + ']'
            tube_format_len = Tube.TUBE_NAME_MAX_LENGTH
            command_type = ('{0:>' + str(tube_format_len) + '}').format(tube_format_name)
            if include_index:
                command_type += '[' + str(self.index) + ']'
        
        command_type += ' >>> ' + self.cmd_type
        if self.is_redo_added == True:
            command_type += ' *'

        return command_type
    
    def get_formatted_content(self):
        '''
        Remove the placehoders form the content and return
        '''
        loop_status = ''
        if self.tube != None and self.loop_index > 0 and (self.tube.tube_conditions != None or self.tube.each_ready):
            loop_status = '[LOOP %s] ' % str(self.loop_index)
        try:
            if self.__original_content2 == None and self.original_content:
                # we need to show the readable print/log output
                # if the key value is an empty string                
                self.__original_content2 = self.self_format_placeholders(self.original_content, is_show_empty = True).rstrip('\n')
                if self.notes:
                    self.__original_content2 = self.__original_content2.replace(Storage.I.C_NOTES_PARAMETER, '').replace(self.notes, '').strip()
                    self.__original_content2 = ' '.join(self.__original_content2.split(' '))
                    self.__original_content2 += '  # => {0}'.format(self.notes)
                return loop_status + str(self.__original_content2)
            else:
                if not self.original_content:
                    return ''
                else:
                    return loop_status + str(self.__original_content2)
        except Exception as e:
            return loop_status + self.original_content
    
    def get_full_content(self):
        return self.get_formatted_type() + ': ' + self.get_formatted_content()
    
    def reset_general_arguments(self):
        
        # return command with singlie placeholder
        if self.is_single_placeholder or self.has_content == False:
            return
        
        args, unknow = general_command_parser.parse_known_args(shlex.split(self.content, posix=False))
        # unknow will store all content except arguments
        if unknow != None:
            self.content = ' '.join(unknow)
            self.redo_content = self.content
        else:
            self.content = ''
            self.redo_content = ''
        
        # reset to initial
        self.is_failed_continue = False
        self.is_failed_redo = False
        
        self.fail_skip_steps = 0
        self.success_skip_steps = 0
        self.redo_steps = 0
        
        self.if_run = True
        
        # check notes value
        if args.notes:
            self.notes = self.self_format_placeholders(' '.join(args.notes))
        
        # analyze redo parameter
        if args.redo != None:       
            self.is_failed_continue = True
            self.is_failed_redo = True
            
            # Get redo steps
            if len(args.redo) > 0:
                # replace placeholders
                redo_steps_str = self.self_format_placeholders(args.redo[0]) 
                self.redo_steps = int(redo_steps_str)
                
            # reset redo content    
            # the redo content should include the continue parameter values    
            if args.continue_steps != None:
                self.redo_content += ' ' + Storage.I.C_CONTINUE_PARAMETER
                if len(args.continue_steps) > 0:
                    self.redo_content += (' ' + ' '.join(str(n) for n in args.continue_steps))
        
        # analyze continue parameter
        if args.continue_steps != None:
            self.is_failed_continue = True
            
            # replace placeholders
            for i, n in enumerate(args.continue_steps):
                args.continue_steps[i] = int(self.self_format_placeholders(n))
                
            # The first case is for --continue m
            if len(args.continue_steps) == 1 and args.continue_steps[0] > 0:            
                self.fail_skip_steps = args.continue_steps[0]
                self.is_fail_skip = True
            # The second case is for --continue m n
            if len(args.continue_steps) == 2:
                if  args.continue_steps[0] >= 0:            
                    self.fail_skip_steps = args.continue_steps[0]
                    self.is_fail_skip = True
                if  args.continue_steps[1] > 0:            
                    self.success_skip_steps = args.continue_steps[1]
                    self.is_success_skip = True

        # check if --raw is set
        if args.is_raw:
            self.is_raw = True

        # analyze if parameter
        if args.if_run != None:
            self.if_run = Utility.eval_conditions(args.if_run, self) == True
              
        # check if it's key command to decide the tube result
        if args.key:
            self.is_key_command = True        
        
    def check_if_key_command(self):
        '''
        Only check if current command is a key command
        
        Return: True or False
        '''
        if type(self.original_content) is str and ' --key' in self.original_content:
            return True
        return False
                    
    def get_xml_tag_text(self):
        '''
        For command GET_XML_TAG_TEXT
        '''
        return_val = None
        file_name, xpath = '',''    
        parser = self.tube_argument_parser
        inputs = self.self_format_placeholders(self.content)
        args, _ = parser.parse_known_args(shlex.split(inputs))
        file_name = ' '.join(args.file)
        xpath = ' '.join(args.xpath)
        is_global = False
        is_force = False
        is_global = args.is_global
        is_force = args.is_force
        variable = None
        if args.variable:
            variable = ' '.join(args.variable)            
            
        if(path.exists(file_name)):
            it = ET.iterparse(file_name)
            # remove all namespace first
            for _, el in it:
                _, _, el.tag = el.tag.rpartition('}')
            root = it.root  
            found_tag = root.find(xpath)
            if found_tag != None:
                return_val = found_tag.text
            else:
                raise Exception('xml tag not found: ' + xpath)
        else:
            raise Exception('xml file not found: ' + xpath)
        
        # update key value
        # update tube variables dependantly
        if variable:
            key = variable
        else:
            key = xpath
        
        key_result = self.update_key_value(key, return_val, is_force=is_force, is_global=is_global)
        if key_result == False:
            raise Exception('Update key-value failed: {0}:{1}'.format(key, return_val))

        if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:
            msg = 'Get xml tag value: ' + str(return_val) 
            tprint(msg, type=Storage.I.C_PRINT_TYPE_DEBUG)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg) 
        else:
            msg = 'Get xml tag value successfully.'
            tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)  

        return True
    
    def set_xml_tag_text(self):
        '''
        For command: SET_XML_TAG_TEXT
        '''
        file_name, xpath, value = None, None, None
        parser = self.tube_argument_parser
        inputs = self.self_format_placeholders(self.content)
        args, _ = parser.parse_known_args(shlex.split(inputs))
        file_name = ' '.join(args.file)
        xpath = ' '.join(args.xpath)
        value = ' '.join(args.value)
        
        # local variables
        temp_namespace = 'temp_ns_attrib_name'
        
        # start to update
        if(path.exists(file_name)):
            # get all namespaces    
            all_namespaces = dict([node for _, node in ET.iterparse(file_name, events=['start-ns'])])
            
            # register namespace
            for key in all_namespaces.keys():
                if key == None:
                    ET.register_namespace('', all_namespaces[key])
                else:
                    ET.register_namespace(key, all_namespaces[key])
                    
            # remove all namespace from elements first
            # and temp save it to tag attribute
            it = ET.iterparse(file_name, parser=ET.XMLParser(target=ET.TreeBuilder(insert_comments=True)))
            for _, el in it:
                prefix, has_namespace, postfix = el.tag.partition('}')
                if has_namespace:
                    el.tag = postfix
                    el.set(temp_namespace, prefix + has_namespace)
                    
            # find and update
            root = it.root
            updated = False
            for el in root.findall(xpath):
                el.text = str(value)  
                updated = True
            if updated == False:
                raise Exception('Not found xpath: ' + xpath)
                    
            # get xml comments before root level
            doc_comments = []
            with open(file_name, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith('<?xml'):
                        continue
                    if line.startswith('<' + root.tag):
                        break
                    else:
                        doc_comments.append(line)
            
            # Add tag namespace back
            # and remove temp attrib    
            Utility.add_tag_namespace(root, temp_namespace)
            
            # write back to xml file        
            tree = ET.ElementTree(root) 
            tree.write(file_name, encoding='unicode', xml_declaration=True)
            
            if len(doc_comments) == 0:
                return True       
            
            # write xml comments before root back
            lines = []
            # first read all lines
            with open(file_name, 'r') as f:
                lines = f.readlines()
            # second, insert xml comments back into memory
            for i, line in enumerate(lines):
                if line.startswith('<?xml'):            
                    insert_at = i + 1
                    for comment in doc_comments:
                        lines.insert(insert_at, comment)
                        insert_at += 1
                    break
            # finally, write all contents to file
            with open(file_name, 'w') as f:
                for line in lines:
                    f.write(line)  

            if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:
                msg = 'Set xml tag value successfully: ' + str(value)
                tprint(msg, type=Storage.I.C_PRINT_TYPE_DEBUG)
                write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg) 
            else:
                msg = 'Set xml tag value successfully.'
                tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO)
                write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)  
                
            return True
        else:
            raise Exception('XML file doesnot exist: ' + file_name)
    
    def set_file_key_value(self):
        '''
        For command: SET_FILE_KEY_VALUE
        '''
        return_val = False
        file_name, keywords, value = '', '', ''
        parser = self.tube_argument_parser
        inputs = self.self_format_placeholders(self.content)
        args, _ = parser.parse_known_args(shlex.split(inputs))
        file_name = ' '.join(args.file)
        keywords = ' '.join(args.keywords)
        value = ' '.join(args.value)
            
        if(path.exists(file_name)):
            
            is_file_endswith_newline = False       
            new_lines = []  
            key_found = False    
            # reset value      
            with open(file_name, 'r') as f:
                lines = f.readlines()
                # check if last line is endswith '\n'
                if lines and len(lines) > 0:
                    is_file_endswith_newline = lines[len(lines)-1].endswith('\n')   
                
                # remove all \n characters
                lines = [line.replace('\n', '') for line in lines]                 
                
                key_count = Utility.get_key_count(keywords, lines)
                updated_same = False
                for line in lines:                    
                    line = line.strip()
                    # logic for configuration.properties
                    if key_count == 1 and '=' in line and key_found == False: 
                        original_key = Utility.get_original_key_value(line, '#', 'REM')[0]
                        if keywords.upper() == original_key.upper():
                            line = keywords + '=' + value
                            key_found = True      
                    # logic for multiple keys found, only turn on the matched on
                    # others will be commented out                  
                    elif key_count > 1 and '=' in line: 
                        key_found = True
                        original_key, original_value = Utility.get_original_key_value(line, '#', 'REM')
                        if keywords.upper() == original_key.upper():
                            if original_value == value and updated_same == False:
                                line = keywords + '=' + value
                                updated_same = True
                            else:
                                if not line.startswith('#'):
                                    line = '#' + line
                        
                    # append new line into array as final output            
                    new_lines.append(line)  

            # for new key value cases
            if not key_found or (key_count > 1 and updated_same == False):
                new_lines.append(keywords + '=' + value)  
            
            # write back to the file      
            with open(file_name, 'w') as f:
                line_count = len(new_lines)
                for i, line in enumerate(new_lines):
                    if i < line_count -1:
                        # not the last line
                        f.write(line + '\n')
                    else:
                        if is_file_endswith_newline == True:
                            # to append the last line don't need the \n
                            f.write('\n' + line)
                        else:
                            f.write(line)
                           
            if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:
                try:                    
                    file_content = Utility.read_file_content(file_name)
                    msg = 'File (%s) content: \n%s' % (file_name, file_content)
                    tprint(msg, type=Storage.I.C_PRINT_TYPE_DEBUG)
                    write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
                except Exception as ed:
                    tprint(str(ed), type=Storage.I.C_PRINT_TYPE_DEBUG)
                    write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', str(ed))
            else:
                msg = 'Set file key value successfully.'
                tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO)
                write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
            return_val = True    
        else:
            raise Exception('file not found: ' + file_name)   
        return return_val

    def write_line_in_file(self):
        '''
        For command: WRITE_LINE_IN_FILE
        
        If line_no doesn't exist, then line_content will be appended.
        '''
        file, line_no, line_content, line_contains = '', 0 ,'', None
        write_mode = 'w'
        is_append_mode = False

        parser = self.tube_argument_parser
        inputs = self.self_format_placeholders(self.content)
        args, _ = parser.parse_known_args(shlex.split(inputs))
        file = ' '.join(args.file)
        if args.number:
            line_no = int(args.number[0])
        line_content = ' '.join(args.value)
        if args.contains:
            line_contains = ' '.join(args.contains)    
            
        # check if in append mode
        if line_no == 0 and line_contains == None:
            is_append_mode = True
        
        # write line content to file
        if os.path.exists(file):
            lines = []
            endswith_newline = '\n'
            # If not in append mode, then read original lines into memory
            with open(file,'r') as f:
                lines = f.readlines()
                if lines and len(lines) > 0:
                    if not lines[len(lines)-1].endswith('\n'):
                        endswith_newline = ''
            
            # start to loop the original lines
            updated = False
            if is_append_mode == False and lines and len(lines) > 0:
                for no, line in enumerate(lines):     

                    # break for loop if there is no conditions
                    if line_no == 0 and line_contains == None:
                        break
                    
                    # check line contains parameter
                    # if user not provided contains then contains_valid is set to True
                    contains_valid = True if (line_contains and line_contains in line) or line_contains == None else False
                    if not contains_valid and line_no == 0:
                        continue
                        
                    # check line no and line contains
                    if ((no+1) == line_no and line_no > 0 and contains_valid) or (line_no == 0 and contains_valid):                    
                        ends = '\n' if line.endswith('\n') else ''
                        lines[no] = line_content + ends                  
                        updated = True
                        if line_no > 0:
                            break

            # For append cases                                 
            if is_append_mode:
                if endswith_newline == '':
                    line_content = '\n' + line_content
                else:
                    line_content = line_content + endswith_newline
                lines.append(line_content)
                updated = True
            
            # overwrite new lines into file
            with open(file, write_mode) as f:
                for line in lines:
                    f.write(line)  
               
            if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:
                try:                    
                    msg = 'Write line in file successfully with parameters: file: {0}, content: {1}, line no: {2}, contains: {3}'.format(
                        file, str(line_content), str(line_no), str(line_contains))
                    if updated == False:
                        msg = 'Write nothing with parameters: file {0}, content: {1}, line no: {2}, contains: {3}'.format(
                                file, str(line_content), str(line_no), str(line_contains)) 
                    tprint(msg, type=Storage.I.C_PRINT_TYPE_DEBUG)
                    write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
                except Exception as ed:
                    tprint(str(ed), type=Storage.I.C_PRINT_TYPE_DEBUG)    
            else:
                msg = 'Write line in file successfully:' + file
                if updated == False:
                    msg = 'Write nothing to file: ' + file
                tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO)
                write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)          
        else:
            raise Exception("file doesn't exist: " + file)

        return True

    def delete_line_in_file(self):
        '''
        For command: DELETE_LINE_IN_FILE
        '''
        file, line_begins, line_contains, delete_empty, line_number = '', '', '', False, None
        deleted_count = 0
        
        parser = self.tube_argument_parser
        inputs = self.self_format_placeholders(self.content)
        args, _ = parser.parse_known_args(shlex.split(inputs))
        file = ' '.join(args.file)
        if args.begins != None:
            line_begins = ' '.join(args.begins)
        if args.contains != None:
            line_contains = ' '.join(args.contains)
        if args.del_empty:
            delete_empty = True
        if args.number:
            line_number = args.number[0]
        result = None
        if args.result:
            result = ' '.join(args.result)
        
        # if didn't found any conditions then delete nothing
        if line_begins == '' and line_contains == '' and not delete_empty and line_number == None:
            raise Exception('No parameters found: -n, -c, -b or -e')  
            
        if os.path.exists(file):
            lines = []
            lines_new = []
            deleted_lines = []
            is_last_char_new_line = True
            # get file original lines
            with open(file,'r') as f:
                lines = f.readlines()
                # check if last line endswith '\n'
                if len(lines) > 0:
                    line = lines[len(lines) - 1]
                    is_last_char_new_line = line.endswith('\n')   
                    
            # check line numbers
            is_asc = True
            count = len(lines)
            if line_number != None:
                line_number = int(line_number)
                if line_number < 0:
                    is_asc = False
                line_number = abs(line_number)              
             
            # go through each line for contains, begins, empty    
            for i, line in enumerate(lines):
                is_delete = False         
                if len(line_begins) > 0 and len(line_contains) == 0 and line.startswith(line_begins): 
                    is_delete = True
                if len(line_contains) > 0 and len(line_begins) == 0 and line_contains in line:
                    is_delete = True
                if len(line_contains) > 0 and len(line_begins) > 0 and \
                    line.startswith(line_begins) and line_contains in line:
                    is_delete = True
                
                # to check delete empty condition
                if is_delete == False:
                    if (line.strip() == '\n' or line.strip() == '') and delete_empty: 
                        is_delete = True
                        
                # to check line numbers
                if line_number != None and is_delete == False:
                    if is_asc == True and i == (line_number - 1):
                        is_delete = True
                    elif is_asc == False:
                        reverse_i = count - i - 1
                        if reverse_i == line_number - 1:
                            is_delete = True
                        
                # delte line which meet the conditions
                if is_delete == False:
                    lines_new.append(line)  
                else:
                    deleted_count += 1     
                    deleted_lines.append(line)              
            
            # overwrite new lines into file
            with open(file, 'w') as f:
                newlines_count = len(lines_new)
                for i, line in enumerate(lines_new):
                    # make sure the last char is the same as deleted before
                    if i == newlines_count - 1:
                        if is_last_char_new_line and not line.endswith('\n'):
                            line += '\n'
                        elif is_last_char_new_line == False and line.endswith('\n'):
                            line = line[:-1]
                    f.write(line)     

            # write deleted lines to file
            if result:
                Utility.write_result_to_file(result, deleted_lines)           
        
            # log how many lines deleted
            if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:
                msg = 'Deleted %s lines.' % (str(deleted_count))
                tprint(msg, type=Storage.I.C_PRINT_TYPE_DEBUG)
                write_line_to_log(Storage.I.TUBE_LOG_FILE, line=msg)
            else:
                msg = 'Deleted %s lines.' % (str(deleted_count))
                tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO)
                write_line_to_log(Storage.I.TUBE_LOG_FILE, line=msg)
        else:
            raise Exception("file doesn't exist: " + file)

        return True
    
    def read_line_in_file(self):
        '''
        For command: READ_LINE_IN_FILE
        '''
        file, line_number, variable, is_force, is_global = '', '', '', False, False
        parser = self.tube_argument_parser
        inputs = self.self_format_placeholders(self.content)
        args, _ = parser.parse_known_args(shlex.split(inputs))
        file = ' '.join(args.file)
        line_number = args.number[0]
        variable = args.variable[0]
        is_force = args.is_force
        is_global = args.is_global
        
        if os.path.exists(file):
            line_number = int(line_number)
            lines = []
            # read file lines into memory
            with open(file,'r') as f:
                lines = f.readlines()
                
            # check line numbers
            is_asc = True
            count = len(lines)
            if line_number < 0:
                is_asc = False
            line_number = abs(line_number)
            if line_number > count:
                if is_asc == True:
                    line_number = count    
                else:
                    line_number = 1
            
            # go through file line by line
            founded_line = None            
            for i, line in enumerate(lines):
                # to check line numbers
                if is_asc == True and i == (line_number - 1):
                    founded_line = line
                    break
                elif is_asc == False:
                    reverse_i = count - i - 1
                    if reverse_i == line_number - 1:
                        founded_line = line
                        break
            
            # update tube varialbe with found line
            if founded_line:
                founded_line = founded_line.replace('\n', '')
            
            # update tube variables dependantly
            key_result = self.update_key_value(variable, founded_line, is_force=is_force, is_global=is_global)
            if key_result == False:
                raise Exception('Update key-value failed: {0}:{1}'.format(variable, founded_line))
            
            if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:
                msg = 'Read line in file successfully: ' + str(founded_line) 
                tprint(msg, type=Storage.I.C_PRINT_TYPE_DEBUG)
                write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
            else:
                msg = 'Read line in file successfully.'
                tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO)
                write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)

        else:
            # file not exists
            raise Exception("file doesn't exist: " + file)

        return True

    def list_files(self):
        directory, result, sort, asc, count, variable = None, None, 'mtime', 'asc', None, None
        parser = self.tube_argument_parser
        inputs = self.self_format_placeholders(self.content)
        args, _ = parser.parse_known_args(shlex.split(inputs, posix=True))
        if args.directory:
            directory = ' '.join(args.directory)
        if args.afile:
            directory = ' '.join(args.afile)
        if args.result:
            result = ' '.join(args.result)
        if args.variable:
            variable = args.variable[0]
        if args.count:
            count = args.count[0]
        is_global = args.is_global
        is_force = args.is_force

        if not directory:
            raise Exception('-f|--file or -d|--directory argument is missing.')
    
        if args.sort:
            if len(args.sort) == 1:
                s = args.sort[0]
                s = self.self_format_placeholders(s).lower()
                if s == 'mtime' or s == 'atime' or s == 'ctime' or s == 'name' or s == 'size':
                    sort = s
                else:
                    raise Exception('Sort type could only be [a|c|m]time, name or size.')
            elif len(args.sort) == 2:
                s = self.self_format_placeholders(args.sort[0]).lower()
                a = self.self_format_placeholders(args.sort[1]).lower()
                if s == 'mtime' or s == 'atime' or s == 'ctime' or s == 'name' or s == 'size':
                    sort = s
                else:
                    raise Exception('Sort type could only be time, name or size.')
                if a.lower() == 'asc' or a.lower() == 'desc':
                    asc = a
                else:
                    raise Exception('The sort can only be sort as asc or desc.')
            else:
                raise Exception('Sort argument could only be [a|c|m]time, name or size.')

        if not result and not variable:
            raise Exception('--result or --variable argument is missing.')

        # get file list
        basename = path.basename(directory)        
        if basename == '.':           
            directory = directory[:-1] + '*.*'
        
        # deal with default *.* logic
        basename = path.basename(directory)    
        if basename == '' or '.' not in basename:
            if directory.endswith('/') or directory.endswith('\\'):
                directory += '*.*'
            else:
                if os.name.startswith('nt'):
                    directory += '\\' + '*.*'
                else:
                    directory += '/' + '*.*' 
        # searching                   
        list_files = glob.glob(directory)
        # sortings
        if sort == 'mtime':
            list_files.sort(key=os.path.getmtime)
        if sort == 'atime':
            list_files.sort(key=os.path.getatime)
        if sort == 'ctime':
            list_files.sort(key=os.path.getctime)
        elif sort == 'name':
            list_files.sort(key=os.path.basename)
        elif sort == 'size':
            list_files.sort(key=os.path.getsize)
        else:            
            list_files.sort(key=os.path.getmtime)
        
        # asc, desc
        if asc == 'desc':
            list_files.reverse()
            
        # writing result
        if result:
            with open(result, 'w') as f:
                Utility.write_result_to_file(result, list_files)

        # store list files count result to tube count var
        if count:
            f_count = 0
            if list_files:
                f_count = len(list_files)
            key_result = self.update_key_value(count, f_count, is_force=is_force, is_global=is_global)
            if key_result == False:
                raise Exception('Update key-value failed: {0}:{1}'.format(count, f_count))  

        # store list files to tube var
        if variable:
            key_result = self.update_key_value(variable, list_files, is_force=is_force, is_global=is_global)
            if key_result == False:
                raise Exception('Update key-value failed: {0}:{1}'.format(variable, list_files))               

        if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:
            msg = 'List files successfully: ' + str(list_files) 
            tprint(msg, type=Storage.I.C_PRINT_TYPE_DEBUG)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg) 
        else:
            msg = 'List files successfully.'
            tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)       

        return True
    
    def list_dirs(self):
        
        directory, result, sort, count, variable = None, None, 'asc', None, None
        parser = self.tube_argument_parser
        inputs = self.self_format_placeholders(self.content)
        args, _ = parser.parse_known_args(shlex.split(inputs, posix=True))
        directory = ' '.join(args.directory)
        if args.result:
            result = ' '.join(args.result)
        
        if args.sort:
            if len(args.sort) == 1:
                s = args.sort[0]
                s = self.self_format_placeholders(s).lower()
                if s == 'asc' or s == 'desc':
                    sort = s
                else:
                    raise Exception('Sort type could only be \'asc\' or \'desc\'.')
            else:
                raise Exception('Sort argument only supports \'asc\' or \'desc\'.')

        if args.variable:
            variable = args.variable[0]
        if args.count:
            count = args.count[0]
        is_global = args.is_global
        is_force = args.is_force

        if not result and not variable:
            raise Exception('--result or --variable argument is missing.')

        # check directory exists
        if not (os.path.exists(directory) and \
            not os.path.isfile(directory)):
            raise Exception('The directory: \'{0}\' is not valid.'.format(directory))
        
        # get sub directories
        ls = next(os.walk(directory))[1]
         
        # asc, desc
        ls.sort()
        if sort == 'desc':
            ls.reverse()
            
        # writing result
        if result:
            with open(result, 'w') as f:
                Utility.write_result_to_file(result, ls)

        # store list directories count result to tube count var
        if count:
            d_count = 0
            if ls:
                d_count = len(ls)
            key_result = self.update_key_value(count, d_count, is_force=is_force, is_global=is_global)
            if key_result == False:
                raise Exception('Update key-value failed: {0}:{1}'.format(count, d_count)) 
        
        # store list result to tube var
        if variable:
            key_result = self.update_key_value(variable, ls, is_force=is_force, is_global=is_global)
            if key_result == False:
                raise Exception('Update key-value failed: {0}:{1}'.format(variable, ls)) 

        if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:
            msg = 'List directories successfully: ' + str(ls) 
            tprint(msg, type=Storage.I.C_PRINT_TYPE_DEBUG)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg) 
        else:
            msg = 'List directories successfully.'
            tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)    

        return True
    
    def file_exist(self):
        file, var = None, None
        parser = self.tube_argument_parser
        inputs = self.self_format_placeholders(self.content)
        args, _ = parser.parse_known_args(shlex.split(inputs))
        file = ' '.join(args.file)
        var = ' '.join(args.variable)

        is_global = args.is_global
        is_force = args.is_force
        
        value = False
        if '*' in path.basename(file) and len(glob.glob(file)) > 0:
                value = True
        else:
            if path.exists(file) and path.isfile(file):
                value = True
        
        if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:
            msg = 'File {0} exists.'.format(file)
            if not value:
                msg = 'File {0} doesnot exist.'.format(file)
            tprint(msg, type=Storage.I.C_PRINT_TYPE_DEBUG)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
        else:
            msg = 'File {0} exists.'.format(file)
            if not value:
                msg = 'File {0} doesnot exist.'.format(file)
            tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
            
        # update tube variables dependantly
        key_result = self.update_key_value(var, value, is_force=is_force, is_global=is_global)
        if key_result == False:
            raise Exception('Update key-value failed: {0}:{1}'.format(var, value))  

        return True
    
    def file_pop(self):
        file, var, number = None, None, 0
        parser = self.tube_argument_parser
        inputs = self.self_format_placeholders(self.content)
        args, _ = parser.parse_known_args(shlex.split(inputs))
        if args.file:
            file = ' '.join(args.file)
        if args.afile:
            file = ' '.join(args.afile)
        if args.variable:
            var = ' '.join(args.variable)
            # replace placeholders 
            var = self.self_format_placeholders(var)
        if args.number:
            number = int(args.number[0])
            if number > 0:
                number = number - 1

        is_global = args.is_global
        is_force = args.is_force

        if not file:
            raise Exception('\'file\' argument was not provided.')       
        
        pop_line = None
        if os.path.exists(file):
            lines = None
            pop_line = None
            # read file lines into memory
            with open(file,'r') as f:
                lines = f.readlines()
                if len(lines) > 0:
                    pop_line = lines.pop(number).replace('\n', '')
            
            # write lines back to text file
            with open(file, 'w') as f:
                for line in lines:
                    f.write(line)
                    
            # update tube variable
            if var:
                # update tube variables dependantly
                key_result = self.update_key_value(var, pop_line, is_force=is_force, is_global=is_global)
                if key_result == False:
                    raise Exception('Update key-value failed: {0}:{1}'.format(var, pop_line))
                    
        else:
            raise Exception('File doesnot exists: {0}'.format(file))
        
        if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:
            msg = 'File was popped successfully: ' + str(pop_line) 
            tprint(msg, type=Storage.I.C_PRINT_TYPE_DEBUG)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
        else:
            msg = 'File was popped successfully.'
            tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
            
        return True
    
    def file_append(self):
        file, value = None, None
        parser = self.tube_argument_parser
        inputs = self.self_format_placeholders(self.content)
        args, _ = parser.parse_known_args(shlex.split(inputs))
        file = ' '.join(args.file)
        value = ' '.join(args.value) 
        
        if os.path.exists(file):
            
            is_new_line = '\n'
            with open(file, 'r') as f:
                lines = f.readlines()
                if lines and len(lines) > 0:
                    if not lines[len(lines)-1].endswith('\n'):
                        is_new_line = ''
            
            # write lines back to text file
            with open(file, 'a+') as f:
                if is_new_line == '':
                    f.write('\n' + value)
                else:
                    f.write(value + is_new_line)
       
        else:
            raise Exception('File doesnot exists: {0}'.format(file))
        
        if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG: 
            msg = 'File was successfully append content: {0}'.format(value) 
            tprint(msg, type=Storage.I.C_PRINT_TYPE_DEBUG)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
        else:
            msg = 'File was successfully appended.'
            tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
            
        return True
    
    def file_push(self):
        file, value = None, None
        parser = self.tube_argument_parser
        inputs = self.self_format_placeholders(self.content)
        args, _ = parser.parse_known_args(shlex.split(inputs))
        file = ' '.join(args.file)
        value = ' '.join(args.value)      
        
        if os.path.exists(file):
            
            lines = []
            with open(file, 'r') as f:
                lines = f.readlines()
            
            # write lines back to text file
            with open(file, 'w') as f:                
                lines.insert(0, value + '\n')
                for line in lines:
                    f.write(line)   
                             
        else:
            raise Exception('File doesnot exists: {0}'.format(file))
        
        if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:
            msg = 'File was successfully pushed content: {0}'.format(value)
            tprint(msg, type=Storage.I.C_PRINT_TYPE_DEBUG)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg) 
        else:
            msg = 'File was successfully pushed.'
            tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
            
        return True

    def file_insert(self):
        file, value, number = None, None, None
        parser = self.tube_argument_parser
        inputs = self.self_format_placeholders(self.content)
        args, _ = parser.parse_known_args(shlex.split(inputs))
        file = ' '.join(args.file)
        value = ' '.join(args.value)      
        number = int(args.number[0])
        
        if os.path.exists(file):
            
            lines = []
            endswith_newline = '\n'
            with open(file, 'r') as f:
                lines = f.readlines()
                # we need to keep the last char if with newline character after the
                # inersert
                insert_at = number
                if number > 0:
                    insert_at = number - 1            
                    
                if lines and len(lines) > 0:
                    if not lines[len(lines)-1].endswith('\n'):
                        endswith_newline = ''
                if number > len(lines):
                    if endswith_newline:
                        lines.insert(insert_at, value + '\n')
                    else:
                        lines.insert(insert_at, '\n' + value)
                else:
                    lines.insert(insert_at, value + '\n')
                    
            # write lines back to text file
            with open(file, 'w') as f:                
                for line in lines:
                    f.write(line) 
                             
        else:
            raise Exception('File doesnot exists: {0}'.format(file))
        
        if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:
            msg = 'File was successfully inserted: {0}'.format(value)
            tprint(msg, type=Storage.I.C_PRINT_TYPE_DEBUG)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg) 
        else:
            msg = 'File was successfully inserted.'
            tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
            
        return True
    
    def file_sort(self):
        file, is_number, is_sort_desc = None, False, False
        parser = self.tube_argument_parser
        inputs = self.self_format_placeholders(self.content)
        args, _ = parser.parse_known_args(shlex.split(inputs))
        if args.file:
            file = ' '.join(args.file)
        if args.afile:
            file = ' '.join(args.afile)
        if args.sort:
            is_sort_desc = True if args.sort[0].upper() == 'DESC' else False 
        if args.is_number:
            is_number = True

        if not file:
            raise Exception('\'file\' argument was not provided.') 
        
        if os.path.exists(file):
            
            lines = []
            endswith_newline = '\n'
            with open(file, 'r') as f:
                lines = f.readlines()     
                # get last char of the file to see if it's '\n'    
                if lines and len(lines) > 0:
                    if not lines[len(lines)-1].endswith('\n'):
                        endswith_newline = ''
            
            newlines = []
            for i, line in enumerate(lines):
                line = line.replace('\n', '')
                if is_number:
                    if reUtility.is_matched_int(line):
                        line = int(line)
                    elif reUtility.is_matched_float(line):
                        line = float(line)
                    else:
                        raise Exception('Line {0} content is not a number: {1}'.format(str(i+1), line))
                newlines.append(line)
            
            # sort the new lines
            newlines.sort(reverse=is_sort_desc)
                    
            # write lines back to text file
            with open(file, 'w') as f:   
                count = len(newlines)             
                for i, newline in enumerate(newlines):
                    line = str(newline)
                    if i < count - 1:
                        line = line + '\n'
                    elif i == count - 1: # the last line content we need to add the correct ending char
                        line = line + endswith_newline
                    
                    f.write(line)                             
        else:
            raise Exception('File doesnot exists: {0}'.format(file))
        
        if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:
            msg = 'File was successfully sorted.'
            tprint(msg, type=Storage.I.C_PRINT_TYPE_DEBUG)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
            
        return True
    
    def file_empty(self):
        file = None
        parser = self.tube_argument_parser
        inputs = self.self_format_placeholders(self.content)
        args, _ = parser.parse_known_args(shlex.split(inputs))
        if args.file:
            file = ' '.join(args.file)
        if args.afile:
            file = ' '.join(args.afile)

        is_create = args.is_create

        if not file:
            raise Exception('\'file\' argument was not provided.') 
                 
        msg = ''
        if os.path.exists(file):            
            # write lines back to text file
            with open(file, 'w') as f:                
                f.write('')                    
            msg = 'File {0} was cleared.'.format(file)
        else:
            if is_create:
                # write lines back to text file
                with open(file, 'w+') as f:                
                    f.write('')
                msg = 'File {0} was created.'.format(file)                
            else:
                raise Exception('File doesnot exists: {0}'.format(file))

        # LOG message    
        tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO)
        write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
            
        return True
    
    def file_create(self):
        file = None
        parser = self.tube_argument_parser
        inputs = self.self_format_placeholders(self.content)
        args, _ = parser.parse_known_args(shlex.split(inputs))
        if args.file:
            file = ' '.join(args.file)
        if args.afile:
            file = ' '.join(args.afile)
        
        if not file:
            raise Exception('\'file\' argument was not provided.')
                 
        msg = ''
        if not os.path.exists(file):            
            with open(file, 'w+') as f:                
                f.write('')                   
            msg = 'File {0} was created.'.format(file)
        else:            
            raise Exception('File already exists: {0}'.format(file))

        # LOG message    
        tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO)
        write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
            
        return True

    def file_read(self):
        file, v_content, v_lines, is_skip_empty = None, None, None, False
        parser = self.tube_argument_parser
        inputs = self.self_format_placeholders(self.content)
        args, _ = parser.parse_known_args(shlex.split(inputs))
        file = ' '.join(args.file)
        if args.content:
            v_content = args.content[0]
        if args.lines:
            v_lines = args.lines[0]
        is_global = args.is_global
        is_force = args.is_force
        is_skip_empty = args.skip_empty

        if not v_content and not v_lines:
            raise Exception('Missing --content or --lines argument.')
        
        lines = [] 
        content = ''       
        if os.path.exists(file):            
            # write lines back to text file
            with open(file, 'r') as f:                
                for line in f.readlines():     
                    line = line.replace('\n', '')
                    if is_skip_empty and not line:
                        continue
                    if v_lines:             
                        lines.append(line)
                    if v_content:
                        content += line
        else:
            raise Exception('File doesnot exists: {0}'.format(file))

        # update tube variables dependantly
        if v_content:
            key_result = self.update_key_value(v_content, content, is_force=is_force, is_global=is_global)
            if key_result == False:
                raise Exception('Update key-value failed: {0}:{1}'.format(v_content, content))

        if v_lines:
            key_result = self.update_key_value(v_lines, lines, is_force=is_force, is_global=is_global)
            if key_result == False:
                raise Exception('Update key-value failed: {0}:{1}'.format(v_lines, lines))
        
        if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:
            msg = 'File content was read successfully: {0}'.format(file)
            tprint(msg, type=Storage.I.C_PRINT_TYPE_DEBUG)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)   
        else:
            msg = 'File content was read successfully.'
            tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg) 
        return True
    
    def file_delete(self):
        file = None
        parser = self.tube_argument_parser
        inputs = self.self_format_placeholders(self.content)
        args, _ = parser.parse_known_args(shlex.split(inputs))
        if args.file:
            file = ' '.join(args.file)
        if args.afile:
            file = ' '.join(args.afile)
        result = None
        if args.result:
            result = ' '.join(args.result)
        
        if not file:
            raise Exception('\'file\' argument was not provided.')
          
        count = 0   
        deleted_files = [] 
        if '*' in path.basename(file):
            files = glob.glob(file)
            for f in files:
                if path.isfile(f):
                    os.remove(f)
                    deleted_files.append(f)
                    count += 1
        elif os.path.exists(file) and path.isfile(file):            
            os.remove(file)
            deleted_files.append(file)
            count += 1
        else:
            raise Exception('File doesnot exists: {0}'.format(file))

        # write deleted files to file
        if result:
            Utility.write_result_to_file(result, deleted_files)
        
        if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:
            msg = 'Successfully deleted {0} files.'.format(count)
            tprint(msg, type=Storage.I.C_PRINT_TYPE_DEBUG)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)   
            if count > 0:
                for file in deleted_files:
                    msg = file
                    tprint(msg, type=Storage.I.C_PRINT_TYPE_DEBUG)
                    write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)  
        else:
            msg = 'Successfully deleted {0} files.'.format(count)
            tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg) 

        return True
    
    def file_copy(self):
        src, dest = None, None
        parser = self.tube_argument_parser
        inputs = self.self_format_placeholders(self.content)
        args, _ = parser.parse_known_args(shlex.split(inputs))
        src = ' '.join(args.src)
        dest = ' '.join(args.dest)
          
        count = 0   
        if os.path.exists(src) and path.isfile(src):
            full_file_name = os.path.abspath(src)
            shutil.copy(full_file_name, dest)
            count += 1
        elif os.path.exists(dest) and not path.isfile(dest):
            files = glob.glob(src)
            for file in files:
                full_file_name = os.path.abspath(file)
                shutil.copy(full_file_name, dest)
                count += 1
        else:
            raise Exception('The src or dest folder doesnot correct.')
        
        if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:
            msg = 'Successfully copied {0} files.'.format(count)
            tprint(msg, type=Storage.I.C_PRINT_TYPE_DEBUG)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)  
        else:
            msg = 'Successfully copied {0} files.'.format(count)
            tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)

        return True
    
    def file_move(self):
        src, dest = None, None
        parser = self.tube_argument_parser
        inputs = self.self_format_placeholders(self.content)
        args, _ = parser.parse_known_args(shlex.split(inputs))
        src = ' '.join(args.src)
        dest = ' '.join(args.dest)
          
        count = 0   
        if os.path.exists(src) and path.isfile(src):
            full_file_name = os.path.abspath(src)
            shutil.move(full_file_name, dest)
            count += 1
        elif os.path.exists(dest) and not path.isfile(dest):
            files = glob.glob(src)
            for file in files:
                full_file_name = os.path.abspath(file)
                shutil.move(full_file_name, dest)
                count += 1
        else:
            raise Exception('The src or dest folder doesnot correct.')
        
        if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:
            msg = 'Successfully moved {0} files.'.format(count)
            tprint(msg, type=Storage.I.C_PRINT_TYPE_DEBUG)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg) 
        else:
            msg = 'Successfully moved {0} files.'.format(count)
            tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)    

        return True
    
    def delete_variable(self):
        parser = self.tube_argument_parser
        inputs = self.self_format_placeholders(self.content)
        args, _ = parser.parse_known_args(shlex.split(inputs))
        name = ' '.join(args.name)
        is_global = args.is_global
        is_del_all = args.is_del_all

        deleted = []

        # delete current
        key = self.tube.KEY_VALUES_DICT.pop(name, None)
        self.tube.KEYS_READONLY_SET.discard(name)
        if key:
            deleted.append('{0} was deleted from tube: {1}'.format(name, self.tube.tube_name))
        # delete global
        t: Tube
        if is_global:
            parents = self.tube.get_parent_tube_list()
            for t in parents:
                key = t.KEY_VALUES_DICT.pop(name, None)
                t.KEYS_READONLY_SET.discard(name)
                if key:
                    deleted.append('{0} was deleted from tube: {1}'.format(name, self.tube.tube_name))
        # delete all
        if is_del_all:
            for t in Storage.I.TUBE_LIST:
                key = t.KEY_VALUES_DICT.pop(name, None)
                t.KEYS_READONLY_SET.discard(name)
                if key:
                    deleted.append('{0} was deleted from tube: {1}'.format(name, self.tube.tube_name))

        if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:
            for msg in deleted:
                tprint(msg, type=Storage.I.C_PRINT_TYPE_DEBUG)
                write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)  

        return True

    def dir_exist(self):
        directory, var = None, None
        parser = self.tube_argument_parser
        inputs = self.self_format_placeholders(self.content)
        args, _ = parser.parse_known_args(shlex.split(inputs))
        directory = ' '.join(args.directory)
        var = ' '.join(args.variable)
        is_global = args.is_global
        is_force = args.is_force
        
        value = False
        if path.exists(directory) and not path.isfile(directory):
            value = True
        
        if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:
            msg = 'Directory {0} exists.'.format(directory)
            if not value:
                msg = 'Directory {0} doesnot exist.'.format(directory)
            tprint(msg, type=Storage.I.C_PRINT_TYPE_DEBUG)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)  
        else:
            msg = 'Directory {0} exists.'.format(directory)
            if not value:
                msg = 'Directory {0} doesnot exist.'.format(directory)
            tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg) 

        # update tube variables dependantly
        key_result = self.update_key_value(var, value, is_force=is_force, is_global=is_global)
        if key_result == False:
            raise Exception('Update key-value failed: {0}:{1}'.format(var, value))  
        return True
    
    def dir_delete(self):
        directory = None
        parser = self.tube_argument_parser
        inputs = self.self_format_placeholders(self.content)
        args, _ = parser.parse_known_args(shlex.split(inputs))
        directory = ' '.join(args.directory)
        is_force = args.is_force
        result = None
        if args.result:
            result = ' '.join(args.result)
          
        count = 0   
        deleted_dirs = []
        if os.path.exists(directory) and not path.isfile(directory) and is_force:            
            shutil.rmtree(directory)
            deleted_dirs.append(directory)
            count += 1
        elif os.path.exists(directory) and not path.isfile(directory):
            os.rmdir(directory)
            deleted_dirs.append(directory)
            count += 1
        else:
            raise Exception('Directory doesnot exists: {0}'.format(directory))
        
        # write deleted files to file
        if result:
            Utility.write_result_to_file(result, deleted_dirs)
        
        if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:
            msg = 'Successfully deleted {0} directory: {1}.'.format(count, directory)
            tprint(msg, type=Storage.I.C_PRINT_TYPE_DEBUG)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)   
        else:
            msg = 'Successfully deleted {0} directory: {1}.'.format(count, directory)
            tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)  

        return True
    
    def dir_create(self):
        directory = None
        parser = self.tube_argument_parser
        inputs = self.self_format_placeholders(self.content)
        args, _ = parser.parse_known_args(shlex.split(inputs))
        directory = ' '.join(args.directory)
          
        os.makedirs(directory)
        
        if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:
            msg = 'Directory created successfully: {0}.'.format(directory)
            tprint(msg, type=Storage.I.C_PRINT_TYPE_DEBUG)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg) 
        else:  
            msg = 'Directory created successfully: {0}.'.format(directory)
            tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)  

        return True
       
    def tail_file(self):
        '''
        For command: TAIL_FILE
        '''
        file, lines_count, keywords, r_file, var_name = '', 0, '', '', ''

        parser = self.tube_argument_parser
        inputs = self.self_format_placeholders(self.content)
        args, _ = parser.parse_known_args(shlex.split(inputs))
        file = ' '.join(args.file)
        lines_count = args.lines[0]
        if args.keywords != None:
            keywords = [k.strip() for k in args.keywords]
            keywords = ' '.join(keywords) 
        if args.result:
            r_file = ' '.join(args.result)    
        if args.variable:
            var_name = args.variable[0]
        is_global = args.is_global
        is_force = args.is_force    

        if not r_file and not var_name:
            raise Exception('Missing result parameter --file or --variable.') 
    
        lines_count = int(lines_count)        
        return_lines = []
        temp_lines = []
        try:
            if not path.exists(file):
                raise Exception("File doesn't exist: " + file)
            # get temp lines which has the same size of lines_count (if the source is big enough)
            with open(file, 'r', encoding='utf8') as f:
                for line in f:
                    line = line.replace('\n', '')
                    if len(line) > 0:
                        temp_lines.append(line)
                    if len(temp_lines) > lines_count:
                        temp_lines.pop(0)

            # get the first line that has of of the keywords
            found_line = -1
            if keywords != None and len(keywords) > 0:
                keywords_array = keywords.split(',')
                for i, line in enumerate(temp_lines):
                    for keyword in keywords_array:
                        if keyword.upper() in line.upper():
                            found_line = i
                            break
                    if found_line >= 0:
                        break
            
            # decide returned lines
            if found_line >= 0:
                return_lines = temp_lines[found_line:]
            else:
                return_lines = temp_lines
            
            if len(return_lines) > 0:
                header = Storage.I.C_TAIL_LINES_HEADER + str(lines_count) + ' LINES FROM FILE [KEYWORDS:' + keywords + '] => '
                tprint(header, prefix='')
                write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', header)
                self.results.append(header)
            for line in return_lines:
                tprint(line, prefix='')
                write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', line)  
                self.results.append(header)

            # write result to result file
            if r_file:
                Utility.write_result_to_file(r_file, return_lines) 

            # write result to tube variable
            if var_name:
                key_result = self.update_key_value(var_name, return_lines, is_force=is_force, is_global=is_global)
                if key_result == False:
                    raise Exception('Update key-value failed: {0}:{1}'.format(var_name, return_lines))         

            return True

        except Exception as e:
            raise e

    def report_progress(self, commands):
        '''
        For command: REPORT_PROGRESS
        '''
        tprint('Command Tube is reporting progress via e-mail settings... ', type=Storage.I.C_PRINT_TYPE_INFO)
        self.content = self.self_format_placeholders(self.content)
        email_subject = self.content
        email_body = ''
        new_line = '<br>'
        progress = calculate_progress_status(commands)
        email_body += progress + new_line
        command: TubeCommand
        
        # prepare emial body
        for command in commands:
            email_body += command.get_formatted_status() + new_line 
            if command.log and command.log.errors and command.log.status == Storage.I.C_FAILED:
                for err in command.log.errors:
                    email_body += err + new_line  
        
        # report progress via email   
        subject = Storage.I.EMAIL_SUBJECT + ' - PROGRESS' 
        if email_subject != None:
            subject = email_subject  
        result = send_email(Storage.I.EMAIL_SENDER_ADDRESS,
                            Storage.I.EMAIL_SENDER_PASSWORD,
                            Storage.I.EMAIL_RECEIVER_ADDRESS,
                            subject,
                            email_body,
                            Storage.I.EMAIL_SMTP_SERVER) 

        if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:
            msg = 'Report progress result: ' + str(result)
            tprint(msg, type=Storage.I.C_PRINT_TYPE_DEBUG)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg) 
        else:
            msg = 'Report progress result: ' + str(result)
            tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)  
        return result  

    def get_file_key_value(self):
        '''
        For command: GET_FILE_KEY_VALUE
        '''
        parser = self.tube_argument_parser
        inputs = self.self_format_placeholders(self.content)
        args, _ = parser.parse_known_args(shlex.split(inputs))
        # replace , from the keys  
        keywords = set()
        if args.keywords:
            # replace ',' to ''
            for i, k in enumerate(args.keywords): 
                if ',' in k:
                    keys_temp = args.keywords[i].split(',')
                    for temp in keys_temp:
                        keywords.add(temp)           
                else:
                    keywords.add(k)
            
        file = ' '.join(args.file)
        key_values = [] 
        is_global = args.is_global
        is_force = args.is_force
        
        # check if file is yaml file    
        is_yaml_file = file.endswith('.yaml') or file.endswith('.yml')     
        
        if is_yaml_file:
            # yaml file
            data = Utility.safe_load_yaml(file)
            for key in data.keys():
                value = data[key]
                if value == None:
                    value = ''
                if type(value) != dict and type(value) != list:
                    if len(keywords) == 0:
                        # update tube variables dependantly
                        key_result = self.update_key_value(key, value, is_force=is_force, is_global=is_global)
                        if key_result == False:
                            raise Exception('Update key-value failed: {0}:{1}'.format(key, value))
                        key_values.append(key + '=' + value)                        
                    else:
                        if key in keywords:  
                            # update tube variables dependantly
                            key_result = self.update_key_value(key, value, is_force=is_force, is_global=is_global)
                            if key_result == False:
                                raise Exception('Update key-value failed: {0}:{1}'.format(key, value))
                            key_values.append(key + '=' + value)     
            
        else:
            # key value file
            with open(file, 'r') as f:
                for line in f:
                    line = line.replace('\n', '')
                    if len(line) < 0:
                        continue
                    if '=' in line:
                        i = line.index('=')
                        key = line[:i].strip()
                        value = line[i+1:].strip()
                        if value == None:
                            value = ''
                        elif reUtility.is_matched_int(value):
                            value = int(value)
                        elif reUtility.is_matched_float(value):
                            value = float(value)
                        elif Utility.equal_true(value):
                            value = True
                        elif Utility.equal_false(value):
                            value = False
                        if len(keywords) == 0:
                            # update tube variables dependantly
                            key_result = self.update_key_value(key, value, is_force=is_force, is_global=is_global)
                            if key_result == False:
                                raise Exception('Update key-value failed: {0}:{1}'.format(key, value))
                            key_values.append(key + '=' + str(value))
                        else:
                            if key in keywords:
                                # update tube variables dependantly
                                key_result = self.update_key_value(key, value, is_force=is_force, is_global=is_global)
                                if key_result == False:
                                    raise Exception('Update key-value failed: {0}:{1}'.format(key, value)) 
                                key_values.append(key + '=' + str(value))
                                                   
        if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:
            msg = 'Get file key values successfully:\n' + str(key_values)
            tprint(msg, type=Storage.I.C_PRINT_TYPE_DEBUG)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg) 
        else:
            msg = 'Get file key values successfully.'
            tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)

        return True, key_values    

    def send_email_via_command(self):
        '''
        For command: EMAIL
        '''
        parser = self.tube_argument_parser
        inputs = self.self_format_placeholders(self.content)
        args, _ = parser.parse_known_args(shlex.split(inputs)) 
        to_list = [item for item in args.to]
        to_list = ','.join(to_list)
        subject = ' '.join(args.subject)
        body = ' '.join(args.body)
        
        # to check if emial body is a file
        # if it's a file then read email body from it
        if body.startswith('$') or path.exists(body):
            file = body
            if file.startswith('$'):
                file = file[1:]
            body = ''
            # read email body from text file
            with open(file, 'r') as f:
                for line in f:
                    body += line + '<br>'              
        tprint('Tube is sending email to %s' % (to_list), type=Storage.I.C_PRINT_TYPE_INFO)   
        result = send_email(Storage.I.EMAIL_SENDER_ADDRESS, Storage.I.EMAIL_SENDER_PASSWORD, to_list, 
                            subject, body, Storage.I.EMAIL_SMTP_SERVER)

        if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:
            msg = 'Sent email result: ' + str(result)
            tprint(msg, type=Storage.I.C_PRINT_TYPE_DEBUG)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg) 
        else:
            msg = 'Sent email result: ' + str(result)
            tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
        return result == True

    def run_tube(self, continue_redo_parser: TubeArgumentParser):
        '''
        For command: RUN_TUBE
        '''
        parser = self.tube_argument_parser
        args, _ = parser.parse_known_args(shlex.split(self.content))
        tube, conditions, each, variables  = None, None, None, None
        if args.tube:
            tube = ' '.join(args.tube)
            tube = self.self_format_placeholders(tube)
        if args.conditions:
            conditions = ' '.join(args.conditions)
        if args.each:
            each = ' '.join(args.each)
        key_value_list = None
        if args.variables:
            variables = ' '.join(args.variables)
            variables = self.self_format_placeholders(variables)
            key_value_list = variables.split(',')
            # to check if the expression match the expression v1 = a1, v2 = a2
            for item in key_value_list:
                item = item.strip().strip('\'').strip('"')
                if not reUtility.is_matched_assign_expresson(item):
                    raise Exception('The tube input variables have wrong format: {0}'.format(item))

        # it's not allowed to have both --while and --each arguments
        if conditions and each:
            raise Exception('--while and --each cannot use together.')
        
        # each logic
        each_index_name = None
        each_item_name = None
        each_list = None
        each_ready = False
        if each:
            if reUtility.is_matched_each_item_expresson(each) or \
               reUtility.is_matched_each_index_item_expresson(each):
                each_index_name, each_item_name, each_list = Utility.split_each_expression(each, self.tube)                
            else:
                raise Exception('The each format is not correct: \'{0}\'.'.format(each))
            each_ready = True

        msg = ''
        # Define re pattern for switching tube type 
        p1 = re.compile('[a-zA-Z_0-9-]+\[[a-zA-Z_0-9]+\]') # file[tube]
        p2 = re.compile('[a-zA-Z_0-9]+') # tube
        p3 = re.compile('[a-zA-Z_0-9-/\\.]+[.]{1}(yaml|yml)') # file.yaml
        
        # analyze input tube type   
        # tube_type = 3 # 1: file[tube] 2: tube  3: file             
        if p1.fullmatch(tube) != None:
            tube_type = 1
        elif p2.fullmatch(tube) != None:
            tube_type = 2
        elif p3.fullmatch(tube) != None:
            tube_type = 3
        else:
            raise Exception('The tube :\'{0}\' doesnot exists.'.format(tube))            
        
        # Check while condition of RUN_TUBE command
        while_condition = True
        if not each_ready:
            while_condition = Utility.eval_while_conditions(conditions, command=self) 
        if  while_condition or each_ready:
            tube_name = ''
            file = tube
            if tube_type == 1: # file[tube]
                file = tube[:tube.index('[')]
                tube_name = tube[tube.index('[')+1:-1]               
            elif tube_type == 2: # tube
                file = self.tube.tube_file
                tube_name = tube   
            elif tube_type == 3: # file.yaml
                tube_name = Storage.I.C_TUBE

            # create sub tube instance
            exists, file = Utility.check_file_exists(file, '.yaml', '.yml')
            data = None
            if exists:
                with open(file, 'r') as f:
                    data = Utility.safe_load_yaml_with_upper_key(f)
                    self.__create_sub_tube(data, tube_type, tube_name, file, conditions)
                
                # each parameters init
                if each_ready:
                    self.sub_tube.each_ready = each_list != None and len(each_list) > 0
                    self.sub_tube.each_index_name = each_index_name
                    self.sub_tube.each_item_name = each_item_name
                    self.sub_tube.each_ls = each_list
            else:    
                raise Exception('The tube :\'{0}\' doesnot exists.'.format(file))                

            # for read whole yaml file case, we need to load
            # email, server, variables as well
            if tube_type == 3:                
                if Storage.I.C_SERVERS in data.keys():       
                    # Get servers to hosts
                    StorageUtility.read_hosts(data[Storage.I.C_SERVERS])
                    if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:
                        msg = 'Servers hosts are updated by tube: %s.' % tube
                        tprint(msg, type=Storage.I.C_PRINT_TYPE_WARNING)
                        write_line_to_log(Storage.I.TUBE_LOG_FILE, line=msg)
                
                if Storage.I.C_EMAIL in data.keys():
                    # read emails
                    StorageUtility.read_emails(data[Storage.I.C_EMAIL])
                    if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:
                        msg = 'Email configurations are updated by tube: %s.' % tube
                        tprint(msg, type=Storage.I.C_PRINT_TYPE_WARNING)
                        write_line_to_log(Storage.I.TUBE_LOG_FILE, line=msg)

                if Storage.I.C_VARIABLES in data.keys():
                    # Read variables 
                    StorageUtility.read_variables(data[Storage.I.C_VARIABLES], tube=self.sub_tube) 
                    if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:
                        msg = 'Tube local variables are updated by tube: %s.' % tube
                        tprint(msg, type=Storage.I.C_PRINT_TYPE_WARNING)
                        write_line_to_log(Storage.I.TUBE_LOG_FILE, line=msg) 

            # checking sub tube command syntax            
            has_errors, errors = StorageUtility.check_tube_command_arguments(self.sub_tube.tube_run, continue_redo_parser)
            if has_errors == False:
                # update tube local variables from RUN_TUBE arguments
                if key_value_list:
                    for item in key_value_list:
                        key, value = Utility.split_assign_expression(item)
                        value = Utility.eval_expression(value, tube=self.tube)
                        self.sub_tube.update_key_value(key, value, is_force=False, is_readonly=False)
                msg = 'Start sub tube successfully: ' + tube 
            else:
                for err in errors:
                    self.log.add_error(err)
                    self.log.status = Storage.I.C_FAILED  
                msg = 'Start tube failed: ' + tube 
        else:
            # while condition return False
            self.log.status = Storage.I.C_SKIPPED   
            self.is_skip_by_while = True  
            msg = 'Sub tube was skipped: ' + tube 
        
        # print log message
        tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO)
        write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
    
    def tube_break(self):
        self.tube.is_broke = True

        if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:
            msg = 'Tube is broke.'
            tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)

        return True

    def tube_continue(self):
        self.tube.is_continued = True

        if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:
            msg = 'Tube is continued.'
            tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
            
        return True
    
    def count(self):
        '''
        For command: COUNT
        '''
        file, status_set, variable, current_tube, skip_count = '', set(), '', False, False
        parser = self.tube_argument_parser
        inputs = self.self_format_placeholders(self.content)
        args, _ = parser.parse_known_args(shlex.split(inputs))
        if args.file:
            file = ' '.join(args.file)     
        if args.tube and len(args.tube) > 0:
            status_set_tmp = Utility.convert_arg_values_to_set(args.tube)
            for item in status_set_tmp:
                status_set.add(item)
                                
        variable = args.variable[0]
        
        # check flags arguments
        if args.current_tube:
            current_tube = True
        if args.skip_count:
            skip_count = True
        
        # get override and force argument
        is_global = False
        is_force = False
        if args.is_global:
            is_global = True 
        if args.is_force:
            is_force = True
        
        # check input parameter
        if not file and len(status_set) == 0:
            raise Exception('Parameter -f (file) or -t (tube status) is missing.')
        
        # case 1: count file lines count
        if file:
            line_count = 0
            with open(file, 'r') as f:
                line_count = sum(1 for line in f)
            # update tube variables dependantly
            key_result = self.update_key_value(variable, line_count, is_force=is_force, is_global=is_global)
            if key_result == False:
                raise Exception('Update key-value failed: {0}:{1}'.format(variable, line_count))
            msg = 'Count successfully: ' + str(line_count)
                  
        # case 2: count tube command count by status
        elif len(status_set) > 0:
            cmd_count = 0
            cmd: TubeCommand
            log: TubeCommandLog
            for log in Storage.I.LOGS:
                cmd = log.command
                # skip COUNT command itself
                if skip_count and cmd.cmd_type == Storage.I.C_COUNT:
                    continue
                # to check if count within current tube only
                if current_tube and cmd.tube.tube_index != self.tube.tube_index:
                    continue
                # count tube command
                if cmd.log.status in status_set:
                    cmd_count += 1
            # update tube variables dependantly
            key_result = self.update_key_value(variable, cmd_count, is_force=is_force, is_global=is_global)
            if key_result == False:
                raise Exception('Update key-value failed: {0}:{1}'.format(variable, cmd_count))
            msg = 'Count successfully: ' + str(cmd_count)

        if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:
            tprint(msg, type=Storage.I.C_PRINT_TYPE_DEBUG)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg) 
        else:
            msg = 'Count successfully.'
            tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
            
        return True

    def set_variable(self):
        '''
        For command: SET_VARIABLE
        '''
        name, key, index, value, is_readonly, is_force, is_global = '', '', None, '', False, False, False
        parser = self.tube_argument_parser
        inputs = self.self_format_placeholders(self.content)
        args, _ = parser.parse_known_args(shlex.split(inputs, posix=False))
        if args.name and len(args.name) > 0:
            name = args.name[0]
        if args.keyword and len(args.keyword) > 0:
            key = args.keyword[0]
        if args.index and len(args.index) > 0:
            index = int(args.index[0].strip())
        if args.value:
            value = ' '.join(args.value)
        # check if expressions given
        if args.expression:
            expression = ' '.join(args.expression)
            # rebuild assign plus case expression
            if reUtility.is_matched_assign_plus_expression(expression):
                f_result = reUtility.P_AssignPlus.findall(expression)[0]                        
                var_name = f_result[1]
                if f_result[2]:
                    var_name += f_result[2]
                if f_result[4]:
                    var_name += f_result[4]
                var_operator = f_result[6]
                var_value = f_result[7]
                expression = var_name + '=' + var_name + var_operator + var_value
            # to check if the expression match the expression v1 = a1
            if reUtility.is_matched_assign_expresson(expression):
                # override the key, value from expression to the --name, --value arguements
                name, value = Utility.split_assign_expression(expression)
                value = str(value)
            elif reUtility.is_matched_assign_dict_expresson(expression):
                name, key, value = Utility.split_assign_expression(expression)
                value = str(value)  
            elif reUtility.is_matched_assign_list_expresson(expression): 
                name, index, value = Utility.split_assign_expression(expression, command=self)
                value = str(value)    
            
            else:
                raise Exception('The set variable has wrong format: {0}'.format(expression))

        is_readonly = args.is_readonly
        is_force = args.is_force
        is_global = args.is_global   

        # if key value exists 
        # to update dict case
        if key:
            value = Utility.eval_expression(value, tube=self.tube)
            # check if name already exists
            exists, temp_tube = self.tube.find_key_from_tubes(name)
            if exists:
                temp_value = temp_tube.KEY_VALUES_DICT[name]
                if type(temp_value) == dict:
                    value_temp = temp_value.copy()
                    value_temp[key] = value
                    value = value_temp
                else:
                    raise Exception('Variable {0} value is not a dict, the update was failed.'.format(name))
            else:
                value = {key: value}
        
        # if index value exists
        # to update list item case
        if index != None:
            value = Utility.eval_expression(value, tube=self.tube)
            # check if name already exists
            exists, temp_tube = self.tube.find_key_from_tubes(name)
            if not exists:
                raise Exception('List doenot exist: {0}'.format(name))
            temp_value = temp_tube.KEY_VALUES_DICT[name]
            if type(temp_value) == list:
                if type(index) == int:
                    temp_value[index] = value
                    value = temp_value
                elif type(index) == list:
                    if len(index) == 1:
                        temp_value[index[0]] = value
                        value = temp_value
                    elif len(index) == 2:
                        temp_value[index[0]][index[1]] = value
                        value = temp_value    
                    elif len(index) == 3:
                        temp_value[index[0]][index[1]][index[2]] = value
                        value = temp_value 
            else:
                raise Exception('Variable {0} value is not a list, the update was failed.'.format(name))

        # evalulate eval inputs
        if not key and not index and type(value) == str:
            value = Utility.eval_expression(value, tube=self.tube, var_name=name)

        return self.update_key_value(name, value, is_force=is_force, is_readonly=is_readonly, is_global=is_global)

    def sftp_get_put(self, ssh):
        '''
        Get or Put files between local and linux server using ssh.
        '''
        localpath, remotepath = '',''
        
        parser = self.tube_argument_parser
        inputs = self.self_format_placeholders(self.content)
        args, _ = parser.parse_known_args(shlex.split(inputs))
        localpath = args.localpath[0]
        remotepath = args.remotepath[0]
        
        star_char = '*.'
        copy_count = 0
        
        sftp = ssh.open_sftp()
        try:      
            if self.cmd_type == Storage.I.C_SFTP_GET:   
                if not star_char in remotepath:                
                    sftp.get(remotepath, localpath)
                    copy_count += 1
                    msg = 'Remote file \'%s\' is transferred to local \'%s\' ' % (remotepath, localpath)
                    tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO)
                    write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg) 
                else:
                    # to deal with *.* or *.extension case
                    # localpath must be a directory in order to copy multiple files from remove server directory
                    if not os.path.isdir(localpath):
                        msg = 'Directory \'%s\' doesnot exists.' % localpath
                        raise Exception(msg) 
                    
                    # get remote directory
                    last_slash_index = -1
                    remote_dir = remotepath
                    file_pattern = remotepath
                    if '/' in remotepath:
                        last_slash_index = remotepath.rindex('/')
                        remote_dir = remotepath[:last_slash_index]
                        file_pattern = remotepath[last_slash_index + 1 :]
                    
                    # run a find linux command to get file list to copy
                    find_files_command = 'find {path} -name {pattern}'
                    find_files_command = find_files_command.format(path=remote_dir, pattern=file_pattern)
                    _, stdout, _ = ssh.exec_command(find_files_command)
                    filelist = stdout.read().splitlines()

                    for afile in filelist:
                        (_, filename) = os.path.split(afile)
                        if type(afile) is bytes:
                            afile = afile.decode()
                        if type(filename) is bytes:
                            filename = filename.decode()
                        localfile_path = os.path.join(localpath, filename)
                        # copy to local
                        sftp.get(afile, localfile_path)   
                        copy_count += 1
                        if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:
                            msg = 'Remote file \'%s\' is transferred to local \'%s\' ' % (afile, localfile_path)
                            tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO)
                            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)    
                
                # log total copied files
                msg = '%s files are copied to local.' % str(copy_count)
                tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO)
                write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
                    
            elif self.cmd_type == Storage.I.C_SFTP_PUT:
                if not star_char in localpath:
                    sftp.put(localpath, remotepath)
                    copy_count += 1
                    msg = 'Local file \'%s\' is transferred to remote \'%s\' ' % (localpath, remotepath)
                    tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO)
                    write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg) 
                else:
                    # to deal with *.* or *.extension case
                    # remotepath must be an existing directory
                    cd_command = 'cd %s' % remotepath
                    _, stdout, _ = ssh.exec_command(cd_command)                    
                    return_code = stdout.channel.recv_exit_status()
                    if return_code != 0:
                        msg = 'Directory \'%s\' doesnot exists.' % remotepath
                        raise Exception(msg)  
                    
                    # get local files      
                    localdir = localpath
                    start_index = localpath.index(star_char)
                    localdir = localdir[:start_index]
                    file_extension = localpath[start_index + 1:]
                    local_files = os.listdir(Path(localdir))
                    for lfile in local_files:
                        if file_extension != '.*' and not lfile.endswith(file_extension):
                            continue
                        local_file_fullpath = os.path.join(localdir, lfile)
                        if os.path.isfile(local_file_fullpath):
                            if remotepath.endswith('/'):
                                remote_file_fullpath = remotepath + lfile
                            else:
                                remote_file_fullpath = remotepath + '/' + lfile
                            sftp.put(local_file_fullpath, remote_file_fullpath)   
                            copy_count += 1     
                            if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:                       
                                msg = 'Local file \'%s\' is transferred to remote \'%s\' ' % (local_file_fullpath, remote_file_fullpath)
                                tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO)
                                write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg) 
                
                # log total copied files
                msg = '%s files are copied to server.' % str(copy_count)
                tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO)
                write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg) 
                    
        finally:
            sftp.close()
    
    def check_char_exists(self):
        '''
        Check if given characters exists from given file.
        Checking result was updated into given tube variable.
        '''
        parser = self.tube_argument_parser
        inputs = self.self_format_placeholders(self.content)
        args, _ = parser.parse_known_args(shlex.split(inputs))
        file, characters, variable = '', '', False
        
        # get user inputs
        file = ' '.join(args.file)
        characters = ' '.join(args.characters)
        variable = args.variable[0]
        
        is_global = args.is_global
        is_force = args.is_force
        
        found = False
        # read file line by line
        try:
            with open(file, 'r') as f:
                for line in f:
                    if characters in line:
                        found = True
                        break                       
        
        finally:
            # update tube variables dependantly
            key_result = self.update_key_value(variable, found, is_force=is_force, is_global=is_global)
            if key_result == False:
                raise Exception('Update key-value failed: {0}:{1}'.format(variable, found))

        msg = 'Checking characters result: ' + str(found)
        tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO)
        write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
    
    def replace_char(self) -> int:
        '''
        Replace strings for a given file line by line
        '''
        parser = self.tube_argument_parser
        inputs = self.self_format_placeholders(self.content)
        args, _ = parser.parse_known_args(shlex.split(inputs))
        file, oldvalue, newvalue, count = '', '', '', 1
        
        # get user inputs
        file = ' '.join(args.file)
        oldvalue = ' '.join(args.oldvalue)
        newvalue = ' '.join(args.newvalue)
        if args.count:
            count = int(args.count[0])
        
        # check input count parameter
        if count < 1:
            raise Exception('Count parameter is less than 1: %s' % str(count))
        
        # local variables
        replaced_count = 0
        
        if os.path.exists(file):
            lines = []
            lines_new = []
            
            with open(file, 'r') as f:
                lines = f.readlines()
            for line in lines:
                while re.search(oldvalue, line) is not None and replaced_count < count:
                    line = re.sub(oldvalue, newvalue, line, 1)
                    replaced_count += 1
                lines_new.append(line)
            
            # write replaced lines back to file
            with open(file, 'w') as f:
                for line in lines_new:
                    f.write(line)
        else:
            raise Exception("file doesn't exist: " + file)        

        msg = 'There are \'%s\' items replaced.' % replaced_count
        tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO)
        write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
        return True
    
    def print_variables(self):
        '''
        Print global variables and it's tube variables
        '''

        parser = self.tube_argument_parser
        inputs = self.self_format_placeholders(self.content)
        args, _ = parser.parse_known_args(shlex.split(inputs))
        variables = ''.join(args.name)
        variables = variables.split(',')
        variables = [var.strip() for var in variables]
        result = None
        if args.result:
            result = ' '.join(args.result)
        
        # print tube variabels
        msg = '=== Tube Variables ==='
        tprint(msg, prefix='')
        write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
        lines = self.__print_tube_variables(variables, self.tube)   
        output_tube_file_list(is_print=True, indexes=self.tube.get_parent_tube_indexes(), lines=lines)  

        # output to file
        if result:
            Utility.write_result_to_file(result, lines) 

    def print_message(self):
        '''
        Print message to the terminal
        '''
        parser = self.tube_argument_parser
        inputs = self.self_format_placeholders(self.content)
        args, _ = parser.parse_known_args(shlex.split(inputs, posix=True))
        msg = ''
        if args.message:
            msg = ' '.join(args.message)
        color = None
        if args.color:
            color = args.color[0]
        
        # print tube variabels
        tprint(msg, prefix='', tcolor=color)
        write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)        
    
    def __print_tube_variables(self, variables, tube, lines=None):
        '''
        It will print it's parent scope variables and parent's parent
        '''
        if lines == None:
            lines = []
        for key in tube.KEY_VALUES_DICT.keys():
            for var in variables:
                if var == '*' or var == '.' or var == key:
                    # get value
                    value = str(tube.KEY_VALUES_DICT[key])
                    value = Utility.quoted_with_space_characters(value)
                    # get readonly
                    readonly = ''
                    if key in tube.KEYS_READONLY_SET:
                        readonly = ' (readonly)'
                    msg = '[%s:%s] %s=%s %s' % (tube.tube_index, tube.tube_name, key, value, readonly)
                    tprint(msg, prefix='')
                    write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg) 
                    lines.append(msg)
            
        # to check if parent is None
        if tube.parent:
            return self.__print_tube_variables(variables, tube.parent, lines)       

        return lines   
    
    def self_report_progress(self):
        
        '''
        Report each tube command finished status via Email
        If --report-progress is not set or there is no Email settings
        then the report status will do nothing
        '''
        
        if(Storage.I.IS_REPORT_PROGRESS == False or 
           Storage.I.HAS_EMAIL_SETTINGS == False):
            
            # log message when there is no email settings
            if (Storage.I.IS_REPORT_PROGRESS == True and 
                Storage.I.HAS_EMAIL_SETTINGS == False):
                
                msg = 'Tube command self report progress is returned since there is no Email settings.'
                tprint(msg, type=Storage.I.C_PRINT_TYPE_WARNING)
                write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
            
            return
        
        # index
        index = '[%s]' % str(self.index)
        
        # status
        status = '-%s >> '
        if self.log.status == Storage.I.C_SUCCESSFUL:
            status = status % 'SUCCESS'
        elif self.log.status == Storage.I.C_SKIPPED:
            status = status % 'SKIP'
        else:
            status = status % 'FAIL'
        
        # email title
        title = index + status + self.cmd_type + ': ' + self.get_formatted_content()
        
        # prepare errors content
        email_body = ''
        if self.log.status == Storage.I.C_FAILED:
            for error in self.log.errors:
                error = error.replace('\n','')
                if len(error) == 0:
                    continue
                email_body += error + '<br>'
        else:
            for result in self.results:
                email_body += result + '<br>'
        try:
            send_email(Storage.I.EMAIL_SENDER_ADDRESS, Storage.I.EMAIL_SENDER_PASSWORD, Storage.I.EMAIL_RECEIVER_ADDRESS, 
                    title, email_body, Storage.I.EMAIL_SMTP_SERVER)  
        except Exception as e:
            msg = 'Report progress errors for command: %s' % (self.cmd_type + ': ' + self.content + ' errors: ' + str(e)) 
            tprint(msg, type=Storage.I.C_PRINT_TYPE_ERROR)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)   
    
    def self_format_placeholders(self, value, is_show_empty = False, is_quoted_str=False, tube=None):
        '''
        Recurrencly format placeholder from self and its parent
        
        Args:
            value: The characters you want to replace place hoders {x}
            is_show_empty: When true the empty string will be formated to ''
            is_quoted_str: This is used for if/while conditions, with quoted string then the eval method could work correctly
        '''
        # if in raw format then disable the placeholder
        if self.is_raw:
            return value

        # make sure the tube input are has value
        if tube == None:
            tube = self.tube

        # get all Key_Values
        KV = self.tube.get_parent_key_values()
        # prepare the temp_dict for placeholder using    
        temp_dict = None
        # for checking if/while condition cases we need to add quotes for string type value
        if is_quoted_str == True:
            temp_dict = Utility.quote_dict_str_value(KV)
        else:
            temp_dict = KV
        
        # for logging purpose, we need to quoted empty string with ''
        if is_show_empty:
            temp_dict = Utility.replace_empty_dict(temp_dict)

        # replace with current tube k-v dict
        value = TubeCommand.format_placeholders(value, temp_dict)  
        
        return value
    
    def pause(self):
        self.content = self.self_format_placeholders(self.content).strip().replace(' ', '').upper()
        is_paused_seconds = False
        msg = ''
        paused_mins = 0
        paused_seconds = 0
        self.content = self.content.replace('MIN', '').replace('UTE', '')
        if self.content.endswith('SEC') or \
            self.content.endswith('SECOND') or \
            self.content.endswith('S'):
            self.content = self.content.upper().replace('SEC', '').replace('OND', '').replace('S', '')
            is_paused_seconds = True
        if self.content.endswith('MIN') or \
            self.content.endswith('MINUTE') or \
            self.content.endswith('M'):
            self.content = self.content.upper().replace('MIN', '').replace('UTE', '').replace('M', '')
            is_paused_seconds = False
            
        # conver to float
        if is_paused_seconds:
            paused_seconds = float(self.content)
            paused_mins = paused_seconds / 60
            msg = str(paused_seconds) + ' seconds.'
        else:
            paused_mins = float(self.content)  
            paused_seconds = paused_mins * 60
            msg = str(paused_mins) + ' minutes.'
                        
        tprint('Command Tube is paused for ' + msg, type=Storage.I.C_PRINT_TYPE_INFO)
        time.sleep(paused_seconds)
        
        return True    
    
    def connect(self):
        # replace placeholders
        self.content = self.self_format_placeholders(self.content) 
        host_name = self.content
        host: Host = None
        ssh = None
        
        # check if connect host name exists from configruations
        host = StorageUtility.get_host(host=host_name, name=host_name)
        if host != None:  
            if host.is_connected:
                Host.SSHConnection = host.ssh
                ssh = host.ssh
            else:
                ssh = host.connect()  
            # update profile command
            if host.is_connected:
                Storage.I.CURR_HOST_PROFILE = host.profile
                Storage.I.CURR_HOST_ROOT = host.root
                Storage.I.CURR_HOST = host.host
                
                # log a message for switching server successfully
                msg = 'Connected to server: ' + host_name               
                tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO)
                write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
        else:
            # host name doesn't exist then set ssh to None
            ssh = None
            Host.SSHConnection = None
        
        # update command status and datetime
        if host.is_connected == True:
            return True
        else:
            self.log.add_error('Please check your servers configurations.')
            if host != None:
                for error in host.errors:
                    self.log.add_error(error) 
            return False                       
    
    def exec_command(self):
        inputs = self.self_format_placeholders(self.content)
        exec(inputs)
        return True

    def linux_command(self):
        log = self.log
        # Check if we have a valid ssh connection
        if Host.SSHConnection == None:
            msg = 'Please check your provide server information, ssh failed to connect to your server.'
            raise Exception(msg) 
        
        # Check Linux Server Disk Space, only checking on the first Linux Command
        check_disk_space(Host.SSHConnection)  

        # replace placeholders
        self.content = self.self_format_placeholders(self.content) 
        
        # Check command
        parser = self.tube_argument_parser
        args, _ = parser.parse_known_args(shlex.split(self.content))
        
        # check if log detial
        if args.is_log_detail:
            self.content = self.content.replace('--log-detail', '').strip()

        # Execute any linux command
        Storage.I.GOTO_HOST_ROOT = 'cd %s;' % Storage.I.CURR_HOST_ROOT # update root path    
        _ , stdout, stderr = Host.SSHConnection.exec_command(Storage.I.CURR_HOST_PROFILE + Storage.I.GOTO_HOST_ROOT + self.content)                    
        
        # print linux command outputs
        while True:
            line = stdout.readline()
            if not line:
                break
            line = line.replace('\n', '')                    
            tprint(line, prefix='')
            # log details to tube log file
            if args.is_log_detail:
                lines = line.split('\r')
                if len(line) > 0 and len(lines) > 0:
                    # if the line contains multiple lines
                    # then we only output the last line
                    line = lines[len(lines) - 1]
                write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', line)    

        # print errors if there are any
        return_code = stdout.channel.recv_exit_status()
        errors = stderr.readlines()
        if return_code != 0:            
            for error in errors:
                tprint(error.replace('\n',''), type=Storage.I.C_PRINT_TYPE_ERROR)    
                log.add_error(error.replace('\n',''))
            return False
        
        return True

    def command(self):
        log = self.log
        log_file = None
        parser = self.tube_argument_parser
        inputs = self.self_format_placeholders(self.content)
        args, _ = parser.parse_known_args(shlex.split(inputs))
        if args.result:
            log_file = args.result[0]
            inputs = re.sub('--result[ ]*' + log_file, '', inputs, 1).strip()

        process = None
        if log_file:
            # write outputs to log file
            with open(log_file, 'w') as f:
                process = subprocess.Popen(inputs, shell=True,
                         stdout=f, stderr=subprocess.PIPE)     
        else:
            # write outputs to terminal console
            process = subprocess.Popen(inputs, shell=True,
                     stdout=sys.stdout, stderr=subprocess.PIPE)  
        
        # Need to print error to the terminal and the log file
        while True:
            '''
            https://realpython.com/python-subprocess/#processes-and-subprocesses
            Note: If you put the Popen object into text mode and then called .read() on .stdout, the call to .read() 
            would be blocking until it reached a newline. In this case, a newline would coincide with the end of the 
            timer program. This behavior isn’t desired in this situation.
            To read as many bytes as are available at that time, disregarding newlines, you need to read with .read1(). 
            It’s important to note that .read1() is only available on byte streams, so you need to make sure to deal 
            with encodings manually and not use text mode.
            '''
            line = process.stderr.read1().decode('utf-8')
            if not line:
                break
            line = line.replace('\n', '')            
            tprint(line, prefix='')
            log.errors.append(line)                       

        # wait the process and get running result 
        process.communicate()
        if process.returncode != 0:  
            return False                           
        else:
            log.errors.clear() 
        
        if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:
            if log_file:
                msg = 'Command outputs are written to file: {0}'.format(os.path.abspath(log_file))
                tprint(msg, type=Storage.I.C_PRINT_TYPE_DEBUG)
                write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)

        return True
    
    def run(self):        
        
        log = self.log 
        try:
            # Log current running step
            running_command = ' [%s][%s]%s'
            msg = datetime.now().strftime(Storage.I.C_DATETIME_FORMAT) + running_command % \
                (str(self.tube.tube_index) + ':' + self.tube.tube_name, str(self.index), 
                 self.get_formatted_type(include_tube=False) + ': ' + str(self.get_formatted_content()))
            tprint(msg, tcolor=Storage.I.C_PRINT_COLOR_YELLOW, type=Storage.I.C_PRINT_TYPE_INFO)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)

            # checking log if has errors
            if log.has_errors():
                # since errors already exist from log.errors
                # then just throw empty exceptions
                raise Exception()

            # checking if command has content
            if self.has_content == False:
                raise Exception('Command is empty >>> {0}:'.format(self.cmd_type))
            
            # initial logs             
            log.start_datetime = datetime.now()
            log.status = Storage.I.C_SUCCESSFUL
            result = True
            # --------------------------------------------------------
            # Begin to run each tube command based on its command type
            # --------------------------------------------------------     
            command_type = self.command_type
            if command_type == Storage.I.C_LINUX_COMMAND:
                result = self.linux_command()              

            elif command_type == Storage.I.C_PATH:
                self.content = self.self_format_placeholders(self.content) 
                result = os.chdir(self.content)
            
            elif command_type == Storage.I.C_PAUSE:
                result = self.pause()

            elif command_type == Storage.I.C_COMMAND:
                result = self.command()                

            elif command_type == Storage.I.C_GET_XML_TAG_TEXT:                      
                result = self.get_xml_tag_text()     

            elif command_type == Storage.I.C_SET_XML_TAG_TEXT:                     
                result = self.set_xml_tag_text()  
            
            elif command_type == Storage.I.C_SET_FILE_KEY_VALUE:                      
                result = self.set_file_key_value()                                                                    

            elif command_type == Storage.I.C_WRITE_LINE_IN_FILE:                        
                result = self.write_line_in_file()  

            elif command_type == Storage.I.C_DELETE_LINE_IN_FILE:                       
                result = self.delete_line_in_file()  
                    
            elif command_type == Storage.I.C_READ_LINE_IN_FILE:                      
                result = self.read_line_in_file()  
            
            elif command_type == Storage.I.C_LIST_FILES:                       
                result = self.list_files()  

            elif command_type == Storage.I.C_LIST_DIRS:                      
                result = self.list_dirs()  
                    
            elif command_type == Storage.I.C_FILE_EXIST:                      
                result = self.file_exist()  

            elif command_type == Storage.I.C_FILE_POP:                       
                result = self.file_pop()  
            
            elif command_type == Storage.I.C_FILE_PUSH:                      
                result = self.file_push()  
                    
            elif command_type == Storage.I.C_FILE_EMPTY:                      
                result = self.file_empty()  
            
            elif command_type == Storage.I.C_FILE_CREATE:                      
                result = self.file_create()  
                    
            elif command_type == Storage.I.C_FILE_READ:                      
                result = self.file_read()  
                    
            elif command_type == Storage.I.C_FILE_APPEND:
                result = self.file_append()  

            elif command_type == Storage.I.C_FILE_INSERT:
                result = self.file_insert() 

            elif command_type == Storage.I.C_FILE_SORT:
                result = self.file_sort() 
                    
            elif command_type == Storage.I.C_FILE_DELETE:
                result = self.file_delete()  
                    
            elif command_type == Storage.I.C_FILE_COPY:
                result = self.file_copy()  
                    
            elif command_type == Storage.I.C_FILE_MOVE:
                result = self.file_move()  
            
            elif command_type == Storage.I.C_DIR_EXIST:
                result = self.dir_exist()  
                    
            elif command_type == Storage.I.C_DIR_DELETE:
                result = self.dir_delete()  
                    
            elif command_type == Storage.I.C_DIR_CREATE:
                result = self.dir_create()  

            elif command_type == Storage.I.C_TAIL_FILE:
                result = self.tail_file()   
            
            elif command_type == Storage.I.C_CONNECT:                                        
                try:
                    result = self.connect() 
                except Exception as e:
                    Host.SSHConnection = None
                    raise Exception(e)           
            
            elif command_type == Storage.I.C_REPORT_PROGRESS:              
                result = self.report_progress(Storage.I.TUBE_RUN)              
            
            elif command_type == Storage.I.C_GET_FILE_KEY_VALUE:
                result, values = self.get_file_key_value()
                # TODO: need to double check the results feature??
                for item in values:
                    self.results.append(item) 
            
            elif command_type == Storage.I.C_EMAIL:
                result = self.send_email_via_command()
            
            elif command_type == Storage.I.C_EXEC:
                result = self.exec_command()
            
            elif command_type == Storage.I.C_RUN_TUBE:
                log.status = Storage.I.C_RUNNING
                self.run_tube(general_command_parser)
            
            elif command_type == Storage.I.C_BREAK:
                self.tube_break()
            
            elif command_type == Storage.I.C_CONTINUE:
                self.tube_continue()
            
            elif command_type == Storage.I.C_COUNT:
                result = self.count()
            
            elif command_type == Storage.I.C_SET_VARIABLE:
                result = self.set_variable()

            elif command_type == Storage.I.C_DELETE_VARIABLE:
                result = self.delete_variable()
            
            elif command_type == Storage.I.C_SFTP_GET or \
                    command_type == Storage.I.C_SFTP_PUT:
                # Check if we have a valid ssh connection
                if Host.SSHConnection == None:
                    msg = 'Please check your provide server information, ssh failed to connect to your server.'
                    raise Exception(msg)
                
                self.sftp_get_put(Host.SSHConnection)
            
            elif command_type == Storage.I.C_CHECK_CHAR_EXISTS:
                self.check_char_exists()
            
            elif command_type == Storage.I.C_REPLACE_CHAR:
                result = self.replace_char()
            
            elif command_type == Storage.I.C_PRINT_VARIABLES:
                self.print_variables()
            
            elif command_type == Storage.I.C_PRINT:
                self.print_message()
                        
            # not supported command found then log errors and continue next          
            else:
                log.status = Storage.I.C_FAILED 
                self.is_failed_continue = True
                msg = 'Not supported tube command found: ' + log.command.cmd_type
                tprint(msg, type=Storage.I.C_PRINT_TYPE_ERROR)
                log.add_error(msg)
                Storage.I.LOGS.append(log)
                return False

            # ending the log status
            if result == False:
                log.status = Storage.I.C_FAILED
            log.end_datetime = datetime.now()
            
            # set the final result of running method
            return True
        except Exception as e:
            log.status = Storage.I.C_FAILED            
            if e and len(str(e)) > 0:                   
                log.add_error(str(e))
                tprint(str(e), type=Storage.I.C_PRINT_TYPE_ERROR) 
            else:
                for msg in log.errors:
                    tprint(msg, type=Storage.I.C_PRINT_TYPE_ERROR) 
            log.end_datetime = datetime.now()
            return True
        
    # ---- IMPORTANT RULE ------
    # The best time to format placesholder is when running this command
    # for display command content could use the format_placeholders_no_error method
    @classmethod
    def format_placeholders(self, value, key_values = None):
        '''
        Replace all placeholders {variable_name} from tube variables
        
        Parameters:
            value: The string you want to replace its all placeholders.
            key_values: If not provided return the input value.
        '''
        
        # return for None or empty
        if not value or not key_values:
            return value  
        
        # We need to check if the command content only contains one {variable} case
        # in this case the value is a dict
        # we need to convert the dict to a norml placeholder: {variable}
        if type(value) is dict:
            keys = [k for k in value.keys()]
            if keys and len(keys) == 1 and value[keys[0]] == None:
                value = '{' + keys[0] + '}'
            else:
                return value
        
        # if type is not string, conver to str
        if type(value) is not str:
            value = str(value)
        
        # replace placeholders from tube commands        
        ret_value = value
        matches = reUtility.P_PlaceHolder.findall(ret_value)
        processed = set()
        for t in matches:
            match_str = t[0]
            match_str_value = t[0]
            var_name = t[1]
            var_format = t[3]            

            # don't do duplict processed
            if match_str in processed:
                continue
            else:            
                processed.add(match_str)
    
            # if key is in dict then we are simple           
            if var_name in key_values.keys():
                ph_key = match_str.strip('{').strip('}')
                if ':' in ph_key:
                    ph_key = ph_key[0:ph_key.index(':')]
                if not '[' in ph_key:
                    match_str_value = key_values[ph_key]
                else:
                    match_str_value = eval(ph_key, globals(), key_values)
                if var_format:
                    match_str_value = ('{0' + var_format + '}').format(match_str_value)
                ret_value = ret_value.replace(match_str, str(match_str_value))                

        return ret_value

    @classmethod
    def format_placeholders_no_error(self, value, key_values = None): 
        '''
        Replace all placeholders {variable_name} from tube variables with no error.
        
        Parameters:
            value: The string you want to replace its all placeholders.
        '''   
        
        ret_value = value
        try:
            ret_value = TubeCommand.format_placeholders(value, key_values)
            return ret_value
        except Exception as e:
            return ret_value    

    @classmethod
    def get_command_syntax(self, command_type, arg_configs) -> str:   
        '''
        Dynamicly get command syntax.
        '''     
        syntax = 'Syntax: - ' + command_type + ': '
        arg_config = arg_configs[command_type]
        args = arg_config[Storage.I.C_ARG_ARGS]
        for arg in args:
            if arg[0] is True: # postion argument
                if arg[6] is True: # is required
                    syntax += arg[5]
                else:
                    syntax += '[' + arg[5] + ']'
            else:
                prefix, suffix = '[', ']'
                if arg[6] is True: # is required
                    prefix, suffix = '', ''
                stored_variable = ' ' + arg[5]
                if arg[7] == True: # has store action
                    stored_variable = ''
                # arg[1]: short argument name
                # arg[2]: long argument name
                if arg[1] == '-':
                    syntax += prefix + arg[2] + stored_variable + suffix
                else:
                    syntax += prefix + arg[1] + '|' + arg[2] + stored_variable + suffix
            
            syntax += ' '   
        general_args = ''  
        if arg_config[Storage.I.C_CONTINUE_PARAMETER]:
            general_args += '[--continue [m][n]] '
        if arg_config[Storage.I.C_REDO_PARAMETER]:
            general_args += '[--redo [m]] '  
        if arg_config[Storage.I.C_IF_PARAMETER]:
            general_args += '[--if run] ' 
        if arg_config[Storage.I.C_KEY_PARAMETER]:
            general_args += '[--key] ' 
        if arg_config[Storage.I.C_PLACE_HOLDER]:
            general_args += '[--raw] '
        if arg_config[Storage.I.C_NOTES_PARAMETER]:
            general_args += '[--note note]' 
        syntax += general_args          
        return syntax

    @classmethod
    def get_command_parameters(self, command_type, arg_configs) -> str:  
        '''
        Dynamicly get command parameter details.
        '''      
        parameters = 'Parameters:\n'
        arg_config = arg_configs[command_type]
        args = arg_config[Storage.I.C_ARG_ARGS]
        indentation = '   '
        # get max argument character lenght
        max_arg_length = 0
        for arg in args:
            if len(arg[1]) + len(arg[2]) > max_arg_length:
                max_arg_length = len(arg[1]) + len(arg[2])
            if len(arg[5]) > max_arg_length:
                max_arg_length = len(arg[5])
        max_arg_length += 5
        # format parameters
        format_str = '{:<' + str(max_arg_length) + '} {}'
        for arg in args:
            if arg[0] is False:
                if arg[1] == '-':
                    parameters += format_str.format(indentation + arg[2] + ':', arg[len(arg) - 1] + '\n')
                else:
                    parameters += format_str.format(indentation + arg[1] + '|' + arg[2] + ':', arg[len(arg) - 1] + '\n')
            else:
                parameters += format_str.format(indentation + arg[5] + ':', arg[len(arg) - 1] + '\n')                
            
        return parameters

    @classmethod
    def get_command_description(self, command_type, arg_configs) -> str:   
        '''
        Dynamicly get command description
        '''     
        description = 'Description: '
        arg_config = arg_configs[command_type]
        description += arg_config[Storage.I.C_COMMAND_DESCRIPTION]
            
        return description
    
    @classmethod
    def get_command_alias(self, command_type, arg_configs) -> str:
        arg_config = arg_configs[command_type]
        alias = 'Alias: '
        if len(arg_config[Storage.I.C_ALIAS]) > 0:
            
            for item in arg_config[Storage.I.C_ALIAS]:
                alias += item + ', '
            alias = alias.strip().rstrip(',')
            return alias
        return alias

    @classmethod
    def get_child_commands(self, command, child_commands):
        if command.tube != None and len(command.tube) > 0:
            for command in command.tube:
                child_commands.append(command)
                TubeCommand.get_child_commands(command, child_commands)                

class TubeCommandLog:

    def __init__(self, command: TubeCommand):
        self.command        = command
        self.start_datetime = datetime.now()
        self.end_datetime   = datetime.now()
        self.status         = None
        self.errors         = []
        self.log            = None

    def get_total_minutes(self):
        '''
        return tube total running time in minutes
        '''
        duration      = self.end_datetime - self.start_datetime 
        duration_in_s = duration.total_seconds() 
        duration_in_m = divmod(duration_in_s, 60)[0]
        return int(duration_in_m)
    
    def get_total_seconds(self):
        '''
        return total tube running time in seconds
        '''
        duration      = self.end_datetime - self.start_datetime 
        duration_in_s = duration.total_seconds()
        return int(duration_in_s)

    def format_log(self, sequence, include_index=False):
        '''
        format tube log status overview
        '''
        duration_in_s = self.get_total_seconds()
        duration_str = '%s SEC' % duration_in_s
        command_type = self.command.get_formatted_type(include_index=include_index)
        if duration_in_s >= 60:
            duration_str = '%s MIN' % self.get_total_minutes()
        return_foramt = '%5s - %10s - %8s - %' + str(Tube.TUBE_NAME_MAX_LENGTH) + 's: %s'   
        return return_foramt % \
            ('[' + str(sequence) + ']', self.status, duration_str, command_type, \
             self.command.get_formatted_content())
    
    def get_hierarchy_seq(self, command: TubeCommand, full_seq = ''):
        if command.parent:
            full_seq = self.get_hierarchy_seq(command.parent, full_seq)

        if full_seq:
            full_seq += '-' + str(command.index)
        else:
            full_seq = str(command.index)
        return full_seq
    
    def print_log(self, sequence):
        '''
        print tube log status overview
        '''
        duration_in_s = self.get_total_seconds()
        duration_str = '%s SEC' % duration_in_s
        if duration_in_s >= 60:
            duration_str = '%s MIN' % str(int(divmod(duration_in_s, 60)[0]))
        command_type = self.command.get_formatted_type(include_index=True)
        log_format = '%5s - %10s - %8s - %' + str(Tube.TUBE_NAME_MAX_LENGTH) + 's: %s'
        log_value = ('[' + str(sequence) + ']', self.status, duration_str, 
                     command_type, self.command.get_formatted_content())
        msg = log_format % log_value
        if self.status == Storage.I.C_SUCCESSFUL:
            tprint(msg, tcolor=Storage.I.C_PRINT_COLOR_GREEN, prefix=Storage.I.C_PRINT_PREFIX_EMPTY)
        elif self.status == Storage.I.C_FAILED:
            tprint(msg, tcolor=Storage.I.C_PRINT_COLOR_RED, prefix=Storage.I.C_PRINT_PREFIX_EMPTY)            
        elif self.status == Storage.I.C_SKIPPED:
            tprint(msg, tcolor=Storage.I.C_PRINT_COLOR_ORANGE, prefix=Storage.I.C_PRINT_PREFIX_EMPTY)  
        elif self.status == Storage.I.C_RUNNING:
            tprint(msg, tcolor=Storage.I.C_PRINT_COLOR_ORANGE, prefix=Storage.I.C_PRINT_PREFIX_EMPTY)                          
    
    def add_error(self, error):
        '''
        Add error to current tube log errors
        '''
        if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:
            traces = traceback.format_exc()
            if not traces.startswith('NoneType'):
                self.errors.append(error + ' ' + traces)
            else:
                self.errors.append(error)
        else:
            self.errors.append(error)  
            
    def write_errors_to_log(self):
        '''
        Write any errors into tube log file
        '''
        for err in self.errors:
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', err)          

    def has_errors(self):
        return len(self.errors) > 0

    def clear(self):
        self.errors.clear()

class Tube():    

    TUBE_NAME_MAX_LENGTH = 0

    def __init__(self, file, name, index, tube_yaml, parent=None):
        '''
        Args:
            file: Tube full file name
            name: Tube name within that file
            index: Tube index
            tube_yaml: Tube commands with YAML format
            parent: Parent tube instance
        '''
        self.KEY_VALUES_DICT   = {} 
        self.KEYS_READONLY_SET = set()
        self.KEYS_DEFAULT      = set()
        self.tube_file         = file
        self.tube_name         = name
        self.tube_index        = index
        self.parent: Tube      = parent
        self.tube_yaml         = tube_yaml        
        self.tube_run          = []
        self.tube_run_all      = []
        self.tube_conditions   = None
        self.tube_run_times    = None
        self.each_ready: bool  = False
        self.__each_index__    = None
        self.each_index_name   = None
        self.each_item_name    = None
        self.each_ls           = None
        self.is_broke          = False
        self.is_continued      = False
        self.gen_tube_run()
        # class properties
        format_tube_name_len = len(self.tube_name) + len(str(self.tube_index)) + 3
        if format_tube_name_len > Tube.TUBE_NAME_MAX_LENGTH:
            Tube.TUBE_NAME_MAX_LENGTH = format_tube_name_len      
        # global properties
        Storage.I.TUBE_LIST.append(self)  
        Storage.I.TUBE_FILE_LIST[self.tube_index] = self.tube_name + '=' + self.tube_file       
        
    def gen_tube_run(self):
        '''
        Convert tube from yaml format to TubeCommand list
        '''
        
        tube_run_new = []
        
        # check empty tube commands
        if not self.tube_yaml:
            self.tube_run = []
            return
        
        # go through each tube command and added
        for item in self.tube_yaml:            
            for key in item.keys():                  
                command = TubeCommand(key, item[key])
                command.tube = self                
                tube_run_new.append(command) 

        # update max command type length
        StorageUtility.reset_max_tube_command_type_length(tube_run_new)
        self.tube_run = tube_run_new

    def update_key_value(self, key, value, is_force=False, is_readonly=False, is_override=True) -> bool:
        '''
        Update key-value in current tube only
        '''
        return StorageUtility.update_key_value_dict(key, value, 
            tube=self, is_force=is_force, is_readonly=is_readonly, is_override=is_override)

    def find_key_from_tubes(self, key):
        '''
        Find if a key exists from tube and it's all parents

        Return (Exists: bool, Tube)
        '''
        if key in self.KEY_VALUES_DICT.keys():
            return (True, self)
        if self.parent:
            return self.parent.find_key_from_tubes(key)
        return (False, None)

    def get_parent_tube_indexes(self, indexes=None):
        '''
        Return all tube and its parents index set
        '''
        if indexes == None:
            indexes = set()
        indexes.add(self.tube_index)
        if tube.parent:
            self.get_parent_tube_indexes(indexes)
        return indexes

    def get_first_key_value(self, key):
        '''
        Return the first value found in the tube parents list
        '''
        if key in self.KEY_VALUES_DICT.keys():
            return self.KEY_VALUES_DICT[key]
        if self.parent:
            return self.parent.get_first_key_value(key)
        return None

    def get_parent_tube_list(self, parents=None):
        '''
        Get current and its all parent tube list
        '''
        if parents == None:
            parents = []
        parents.append(self)
        if self.parent:
            return self.parent.get_parent_tube_list(parents)
        return parents

    def get_parent_key_values(self, KV=None):
        '''
        Get current tube key-values and all its parents tube key-values
        '''
        if KV==None:
            KV = {}
        
        # copy tube and its parents tubes key values to KV and return
        for key in self.KEY_VALUES_DICT:
            if not key in KV.keys():
                KV[key] = self.KEY_VALUES_DICT[key]
        # checking parents
        if self.parent:
            return self.parent.get_parent_key_values(KV)
        return KV

    def clear_each(self):
        self.KEY_VALUES_DICT.pop(self.each_item_name, None)
        if self.each_index_name:
            self.KEY_VALUES_DICT.pop(self.each_index_name, None)
        self.__each_index__ = None
        self.each_index_name = None
        self.each_item_name = None
        self.each_ls = None 

class TubeRunner():
    
    def __init__(self, is_main = True, run_tube_command: TubeCommand = None, tube: Tube = None):
        '''
        Args:
            is_main: If the runner starts from main job. Default Yes.
            run_tube_command: The RUN_TUBE command reference that starts this runner
            tube: The tube instance runner could run
        '''
        
        self.pre_command: TubeCommand      = None
        self.is_main                       = is_main
        self.run_tube_command: TubeCommand = run_tube_command
        self.tube: Tube                    = tube
    
    def __output_while_condition(self, while_condition, tube_conditions, loop_index = 0, command=None):
        # print current while conditions in debug mode        
        if tube_conditions != None and Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:
            conditions = command.self_format_placeholders(tube_conditions)
            msg = '[LOOP {0}]: The current while condition returns \'{1}\': {2}'.format(
                str(loop_index+1),
                str(while_condition),                
                str(conditions)                   
                )
            tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO)  
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
        
    def __finish_start_again(self):
        
        # skip the main job
        if self.is_main:
            return
        
        # copy done list to the 'tube' that contains the whole sub command list
        command_done_list = self.tube.tube_run.copy()
        self.tube.tube_run_all.extend(command_done_list)
        status = calc_success_failed_for_tube(command_done_list)

        # if current loop failed then stop the tube running
        if status == Storage.I.C_FAILED:
            self.tube.is_broke = True
            
        # clear tube run
        self.tube.tube_run.clear()
        
        # check if need run again
        while_condition = True
        if not self.tube.each_ready:
            while_condition = Utility.eval_while_conditions(self.tube.tube_conditions, False, command=self.run_tube_command)
            # print current while conditions in debug mode
            self.__output_while_condition(while_condition, self.tube.tube_conditions, self.tube.tube_run_times, self.run_tube_command)
            
        # run again?
        self.tube.is_continued = False
        if not self.tube.is_broke and ((while_condition and not self.tube.each_ready) or \
            (self.tube.each_ready and self.tube.__each_index__ < len(self.tube.each_ls) - 1)):             
            self.pre_command = None       
            self.tube.gen_tube_run()     
            self.start()
        else:
            # At the end of the RUN_TUBE interations, we need to reset the sub tube running result
            self.run_tube_command.log.status = status
            # clear each parameters
            if self.tube.each_ready:
                self.tube.clear_each()               
    
    def start(self):
        '''
        Run a tube.          
        '''
        
        # increase the total interation times
        if self.is_main == False:
            self.tube.tube_run_times += 1

            if self.tube.each_ready:
                # update each index, item for tube local variable
                self.tube.__each_index__ = self.tube.tube_run_times - 1
                if self.tube.each_index_name:
                    self.tube.update_key_value(self.tube.each_index_name, self.tube.__each_index__)
                self.tube.update_key_value(self.tube.each_item_name, self.tube.each_ls[self.tube.__each_index__])
        
        # Loop each command within the tube and run it    
        command: TubeCommand
        for index, command in enumerate(self.tube.tube_run): 
            command.index = index + 1  
            # add a link if the tube runner is started a sub tube
            # linke the each sub tube command with the RUN_TUBE command
            if self.is_main == False:
                command.loop_index = self.tube.tube_run_times  

            # get log instance reference
            log = command.log
            
            # skip command which is skipped by continue arguments
            if command.is_skip == True:
                log.status = Storage.I.C_SKIPPED             
                Storage.I.LOGS.append(log)
                # log command which is skipped
                msg = 'SKIP: Tube command \'' + command.cmd_type + ': ' + command.content + '\' was skipped by previous --continue arguments.'
                write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
                tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO, tcolor=Storage.I.C_PRINT_COLOR_GREY)
                # check if report tube command status
                command.self_report_progress()
                # continue with next loop item
                continue
                        
            # skip if any previous command failed 
            if self.pre_command != None and \
              (self.pre_command.log.status == Storage.I.C_FAILED and self.pre_command.is_failed_continue == False):               
                log.status = Storage.I.C_SKIPPED
                Storage.I.LOGS.append(log)
                # check if report tube command status
                command.self_report_progress()
                # continue with next loop item                
                continue
            
            # reset general arguments
            try:
                command.reset_general_arguments()
            except Exception as e:
                log.add_error(str(e))
            
            # skip if_run == False cases
            if command.if_run == False and not log.has_errors():
                command.is_skip = True
                # in order to get key command correct running status
                # we need this flag to tell it's skipped by if run
                # if command is skipped by if run, then it will not 
                # affect the key command status
                command.is_skip_by_if = True
                log.status = Storage.I.C_SKIPPED             
                Storage.I.LOGS.append(log)
                # log command which is skipped
                msg = 'SKIP: Tube command \'' + command.cmd_type + ': ' + command.content + '\' was skipped since --if condition is False.'
                write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
                tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO, tcolor=Storage.I.C_PRINT_COLOR_GREY)
                # check if report tube command status
                command.self_report_progress()
                # continue with next loop item
                continue
            
            # --------------------------------------------------------
            # Begin to run each tube command based on its command type
            # --------------------------------------------------------
            if not command.run():
                self.pre_command = command
                continue
            
            # deal with the RUN_TUBE was skipped case
            if command.command_type == Storage.I.C_RUN_TUBE and command.log.status == Storage.I.C_SKIPPED:
                command.is_skip = True
                command.is_skip_by_while = True
                Storage.I.LOGS.append(log)
                # log command which is skipped
                msg = 'SKIP: Tube command \'' + command.cmd_type + ': ' + command.self_format_placeholders(command.content) + '\' was skipped since --while condition is False.'
                write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
                tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO, tcolor=Storage.I.C_PRINT_COLOR_GREY)
                # check if report tube command status
                command.self_report_progress()
                # continue with next loop item
                continue
              
            # support --redo arguments logic
            if command.is_failed_redo == True and log.status == Storage.I.C_FAILED:
                TubeCommandUtility.insert_failed_redo_commands(self.tube.tube_run, index, command)
            elif command.is_failed_redo == True and log.status == Storage.I.C_SUCCESSFUL and \
                 command.redo_steps > 0:
                TubeCommandUtility.insert_success_redo_commands(self.tube.tube_run, index, command)                
                    
            # check continue conditional skip steps at the end of each command
            if command.is_failed_continue:
                TubeCommandUtility.reset_command_skip(self.tube.tube_run, command)        
            
            # if command failed and errors then output to log
            if log.status == Storage.I.C_FAILED:
                log.write_errors_to_log()
                
            # check if report tube command status
            command.self_report_progress()
                                
            # Finnally append the command log
            Storage.I.LOGS.append(log)
            self.pre_command = command
            
            # Check if it's RUN_TUBE command
            if command.command_type == Storage.I.C_RUN_TUBE and log.status == Storage.I.C_RUNNING:                
                # print current while conditions in debug mode
                self.__output_while_condition(True, command.sub_tube.tube_conditions, command.sub_tube.tube_run_times, command=command)  
                # start the sub tube runner
                runner = TubeRunner(False, command, command.sub_tube)                 
                runner.start()

            # Check 'break' or 'continue' command
            if command.tube.is_broke or command.tube.is_continued:
               break

        # during the end of sub tube running
        # we need to check while condition again
        # to see if need to run the sub tube again
        self.__finish_start_again()
        
class Host():
    
    SSHConnection = None   
    
    def __init__(self, name='', host='', port=22, user='', pwd='', root='/', profile='') -> None:
        self.name         = str(name)
        self.host         = str(host)
        self.port         = str(port)
        self.user         = str(user)
        self.password     = str(pwd)
        self.root         = str(root)
        self.profile      = str(profile)
        self.ssh          = None
        self.is_connected = False
        self.errors       = set()
    
    def connect(self):
        '''
        Connect to linux server, if errors add them into errors.
        '''
        self.ssh = None
        try:            
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(self.host, self.port, self.user, self.password, timeout=Storage.I.C_SSH_CONNECT_TIMEOUT)
            self.is_connected = True
            Host.SSHConnection = self.ssh
            self.errors.clear()
        except Exception as e:
            msg = 'When connect to server: %s, port: %s, user: %s, password: %s, exception: %s' % \
                    (self.host, str(self.port), self.user, self.password, str(e))
            tprint(msg, type=Storage.I.C_PRINT_TYPE_ERROR) 
            self.errors.add(msg)
            #write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
            self.is_connected = False
            self.ssh = None  
            Host.SSHConnection = None      
        return self.ssh
    
    def disconnect(self):
        '''
        Disconnect if it's connected.
        '''
        if self.ssh != None:
            self.ssh.close()  
            self.ssh = None
        self.errors.clear()
        self.is_connected = False         

class StorageUtility():

    @classmethod
    def update_key_value_dict(self, key, value, command: TubeCommand=None, tube: Tube=None, is_force=False, 
                              is_override=True, override_reason='It\'s not allowed to override this key.',
                              is_readonly=False):
        '''
        Update storage's key-value pair
        
        if the key already exist, then a warning will be loged into the log file.
        
        Parameters:
            key: The key you want to update
            value: The key's value, if None then empty string will be used
            command: The command triger this update
            tube: Which tube to update the key value
            is_force: If true it will always update the value. Default False.
            is_override: If update value if key already exists. Default True.
            override_reason: The reason user can't update this key.
            is_readonly: Set the variable to readonly. Default False. 
            
        '''
        # return for None or empty key
        if not key or not tube:
            return False

        # skip keywords cases
        if key in Storage.I.C_KEYWORDS:
            raise Exception(f'Keyword \'{key}\' is not allowed to used in variable name. The full keywords list are: {Storage.I.C_KEYWORDS}.')
        
        # check value is None
        if value == None:
            value = ''

        # reference the right key-value dict
        key_values_dict = None
        keys_readonly_set = None
        key_values_dict = tube.KEY_VALUES_DICT
        keys_readonly_set = tube.KEYS_READONLY_SET
                        
        # check if force
        if is_force:
            is_override = True
        
        # check override
        if is_override == False and key in key_values_dict.keys():
            msg = override_reason
            tprint(msg, type=Storage.I.C_PRINT_TYPE_WARNING)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)        
            return False 
        
        # update the key value
        updated = False   
        # If not in the readonly set then udpate directly     
        if not key in keys_readonly_set:
            key_values_dict[key] = value
            updated = True
        else:
            if is_force == False:
                msg = 'Variable (%s:%s) is readonly, you cannot update except use the set_variable (--forece) argument.' % (key, str(key_values_dict[key]))
                tprint(msg, type=Storage.I.C_PRINT_TYPE_WARNING)
                write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)   
            else:
                key_values_dict[key] = value
                updated = True        
        
        # give an note if the key-value dict was udpated        
        if updated:
            # if updte the variable in readonly 
            if is_readonly and not key in keys_readonly_set:
                keys_readonly_set.add(key)
                
            # give a warning that the key-value was overrode from the memory
            forced = ' '
            if is_force:
                forced = ' forced '
            if type(value) == str:
                value = '\'' + value + '\''
            msg = 'Tube variable \'%s\' was%supdated to value: %s.' % (key, forced, value)
            if command:
                msg += ' By tube[%s] command: %s' % (str(command.tube.tube_index), command.cmd_type + ': ' + str(command.get_formatted_content()))
            if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:
                tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO)
                write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
                
        return updated
    
    @classmethod
    def check_tube_command_arguments(self, tube_check, continue_redo_parser: TubeArgumentParser, is_check_import=False):
        '''
        Check if tube command syntax correct.
        '''
        
        has_errors = False    
        errors_return = []
        command: TubeCommand
        for command in tube_check:
            
            # skip COMMAND & LINUX_COMMAND
            if command.command_type == Storage.I.C_COMMAND or \
            command.command_type == Storage.I.C_LINUX_COMMAND:
                continue
            
            # check invalid command type
            if command.command_type == '':
                has_errors = True            
                msg = 'Command: %s doesnot support now.' % command.cmd_type
                tprint(msg, type=Storage.I.C_PRINT_TYPE_ERROR)
                errors_return.append(msg)
                write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
                continue
                        
            if not command.has_content:
                msg = 'Command: %s is empty.' % command.cmd_type
                tprint(msg, type=Storage.I.C_PRINT_TYPE_ERROR)
                errors_return.append(msg)            
                write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
                has_errors = True
                continue
            
            # check if syntax errors
            if command.tube_argument_parser != None:
                command_content = command.content           
                command.tube_argument_parser.parse_args(command_content.split())
                syntax_errors = command.tube_argument_parser.get_formated_errors()
                if len(syntax_errors) > 0:
                    command.has_syntax_error = True
                    has_errors = True                
                    for i, err in enumerate(syntax_errors):
                        msg = ''
                        if i == 0:
                            msg = 'In tube [{0}] command >>> {1} found {2}'.format(
                                str(command.tube.tube_index) + ':' + command.tube.tube_name, command.cmd_type + ': ' + command.get_formatted_content(), str(err))
                        else:
                            msg = 'It has {0}'.format(str(err))
                        errors_return.append(msg) 
                        tprint(msg, type=Storage.I.C_PRINT_TYPE_ERROR)                                           
                        write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)                    
                command.tube_argument_parser.argument_error.clear() 
            
            # check Server exists
            if command.has_syntax_error == False and \
            command.command_type == Storage.I.C_CONNECT:
                command_content = command.self_format_placeholders(command.content)
                _, input_server = continue_redo_parser.parse_known_args(command_content.split())
                input_server = ' '.join(input_server)
                host = StorageUtility.get_host(host=input_server,name=input_server)
                if host == None:
                    has_errors = True
                    msg = '%s: \'%s\' doesnot exists.' % (command.cmd_type, input_server)
                    tprint(msg, type=Storage.I.C_PRINT_TYPE_ERROR)
                    errors_return.append(msg)                
                    write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)                    
                    continue
            
        return (has_errors, errors_return)

    @classmethod
    def read_hosts(self, servers):
        '''
        Read host settings from tube server section.
        '''
        
        if(servers == None):
            return
        
        # read servers configuration from file
        if type(servers) is str:
            with open(servers, 'r') as f:
                servers = Utility.safe_load_yaml_with_upper_key(f)
                servers = servers[Storage.I.C_SERVERS]
        
        for server in servers:
            host: Host
            Utility.make_dict_key_upper(server)
            Utility.make_dict_key_upper(server[Storage.I.C_SERVER])
            host = Host(name=server[Storage.I.C_SERVER][Storage.I.C_SERVER_NAME], 
                        host=server[Storage.I.C_SERVER][Storage.I.C_SERVER_HOST], 
                        port=server[Storage.I.C_SERVER][Storage.I.C_SERVER_PORT], 
                        user=server[Storage.I.C_SERVER][Storage.I.C_SERVER_USER], 
                        pwd=server[Storage.I.C_SERVER][Storage.I.C_SERVER_PASSWORD], 
                        root=server[Storage.I.C_SERVER][Storage.I.C_SERVER_ROOT], 
                        profile=server[Storage.I.C_SERVER][Storage.I.C_SERVER_PROFILE])
            # read user password from file
            if host.password.startswith('$'):
                file = host.password[1:]
                found, pwd = Utility.read_password_from_file(file, host.user)
                if found == True:
                    host.password = pwd
            # check profile 
            if not host.profile.endswith(';'):
                host.profile += ';'
            Storage.I.HOSTS[host.host] = host

    @classmethod
    def get_host(self, host='', name=''):
        if host in Storage.I.HOSTS.keys():
            return Storage.I.HOSTS[host]
        
        for key in Storage.I.HOSTS.keys():
            host = Storage.I.HOSTS[key]
            if str(host.name) == name:
                return host
        
        return None
    
    @classmethod
    def read_variables(self, variables, tube:Tube, is_force=False):
        '''
        Read tube variables from tube variable section.

        Args:
            varialbes: The variables from yaml config file            
            tube: The tube to store these variables
            is_force: If update tube variable force
        '''
        
        if(not variables or type(variables) is not dict or not tube):
            return
        
        for key in variables.keys():
            tube.update_key_value(key, variables[key], is_force=is_force)
    
    @classmethod
    def add_default_variables(self, tube: Tube):
        # Update TUBE_HOME
        if Storage.I.C_TUBE_HOME not in tube.KEY_VALUES_DICT.keys():            
            StorageUtility.update_key_value_dict(Storage.I.C_TUBE_HOME, Storage.I.C_CURR_DIR, tube=tube, is_readonly=True)
            tube.KEYS_DEFAULT.add(Storage.I.C_TUBE_HOME)
        # Update OS Name
        if Storage.I.C_OS_NAME not in tube.KEY_VALUES_DICT.keys(): 
            StorageUtility.update_key_value_dict(Storage.I.C_OS_NAME, os.name, tube=tube, is_readonly=True)
            tube.KEYS_DEFAULT.add(Storage.I.C_OS_NAME)
        
    @classmethod
    def read_emails(self, emails):     
        '''
        Read email configurations from 'EMAIL' section.
        '''   
        if type(emails) is str:
            with open(emails, 'r') as f:
                emails = Utility.safe_load_yaml_with_upper_key(f)
                emails = emails[Storage.I.C_EMAIL]
                
        if type(emails) is dict:
            Utility.make_dict_key_upper(emails)
            Storage.I.EMAIL_SMTP_SERVER = emails[Storage.I.C_EMAIL_SMTP_SERVER]
            if Storage.I.C_EMAIL_SERVER_PORT in emails.keys():
                Storage.I.EMAIL_SERVER_PORT = emails[Storage.I.C_EMAIL_SERVER_PORT]
            Storage.I.EMAIL_SENDER_ADDRESS = emails[Storage.I.C_EMAIL_SENDER_ADDRESS]
            Storage.I.EMAIL_SENDER_PASSWORD = emails[Storage.I.C_EMAIL_SENDER_PASSWORD]
            Storage.I.EMAIL_RECEIVER_ADDRESS = emails[Storage.I.C_EMAIL_RECEIVER_ADDRESS]
            Storage.I.EMAIL_SUBJECT = emails[Storage.I.C_EMAIL_SUBJECT] 
        
        # Read email passwords form file
        if Storage.I.EMAIL_SENDER_PASSWORD.startswith('$'):
            file = Storage.I.EMAIL_SENDER_PASSWORD[1:]
            found, pwd = Utility.read_password_from_file(file, Storage.I.EMAIL_SENDER_ADDRESS)
            if found == True:
                Storage.I.EMAIL_SENDER_PASSWORD = pwd
        
        # Update email settings flag                
        Storage.I.HAS_EMAIL_SETTINGS = True
    
    @classmethod
    def read_variables_from_console(self, variables, tube: Tube):
        '''
        Read tube variables from user inputs.
        If variable was updated from console, then it 
        cannot be udpated again by other tube commands.
        '''
        if not variables:
            return
        variables = ' '.join(args.variables)
        variables = TubeCommand.format_placeholders(variables)
        key_value_list = variables.split(',')
        for item in key_value_list:
            item = item.strip().strip('\'').strip('"')
            if not reUtility.is_matched_assign_expresson(item):
                raise Exception('The tube input variables have wrong format: {0}'.format(item))
            key, value = Utility.split_assign_expression(item) 
            value = Utility.eval_expression(value, tube=tube)               
            StorageUtility.update_key_value_dict(key, value, is_readonly=True, tube=tube) 
            if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:
                msg = 'Read console variable: \'%s\', value: \'%s\' from console and set it to readonly.'                
                tprint(msg % (key, value), type=Storage.I.C_PRINT_TYPE_INFO)
                write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg % (key, value))                              

    @classmethod
    def reset_colors(self):
        '''
        Reset terminal colors based on OS type.
        '''
        if not os.name.startswith('nt'):
            # Mac OS
            Storage.I.C_PRINT_COLOR_RED = 'red'
            Storage.I.C_PRINT_COLOR_BLUE = 'blue'
            Storage.I.C_PRINT_COLOR_PURPLE = 'purple'
            Storage.I.C_PRINT_COLOR_GREEN = 'green'
            Storage.I.C_PRINT_COLOR_ORANGE = 'orange'
            Storage.I.C_PRINT_COLOR_YELLOW = 'yellow'
        else:
            # Windows
            Storage.I.C_PRINT_COLOR_RED = 'red'
            Storage.I.C_PRINT_COLOR_BLUE = 'green' # blue color doesn't work well in some windows terminals
            Storage.I.C_PRINT_COLOR_PURPLE = 'purple'
            Storage.I.C_PRINT_COLOR_GREEN = 'green'
            Storage.I.C_PRINT_COLOR_ORANGE = 'orange'
            Storage.I.C_PRINT_COLOR_YELLOW = 'yellow'
            Storage.I.C_PRINT_COLOR_STYLE = 'bright'
    
    @classmethod
    def get_tube_index(self, file, tube_name):
        '''
        Check if tube file exists from tube file list
        
        Args:
            file: Tube file name
        '''
        index = 0
        file_full_path = os.path.abspath(file)
        for key in Storage.I.TUBE_FILE_LIST.keys():
            value = Storage.I.TUBE_FILE_LIST[key]
            if value == tube_name + '=' + file_full_path:
                return key
        index = max([i for i in Storage.I.TUBE_FILE_LIST.keys()]) + 1
        Storage.I.TUBE_FILE_LIST[index] = tube_name + '=' + file_full_path
        return index

    @classmethod
    def get_command_type(self, cmd_type):
        for key in Storage.I.TUBE_ARGS_CONFIG.keys():
            if cmd_type.upper() == key:
                return key
            for alias in Storage.I.TUBE_ARGS_CONFIG[key][Storage.I.C_ALIAS]:
                if cmd_type.upper() == alias:
                    return key
        return ''  

    @classmethod
    def reset_max_tube_command_type_length(self, tube_command_list):
        if tube_command_list == None or len(tube_command_list) == 0:
            return Storage.I.MAX_TUBE_COMMAND_LENGTH
        type_list = [c.cmd_type + c.tube.tube_name for c in tube_command_list]
        max_length = len(max(type_list, key=len)) + 5
        if max_length > Storage.I.MAX_TUBE_COMMAND_LENGTH:
            Storage.I.MAX_TUBE_COMMAND_LENGTH = max_length

    @classmethod
    def check_if_key_command_exists(self, commands = []):
        '''
        Check if key command exists
        
        Args:
            commands: If not provided then check all the log linked commands
        '''
        if not commands or len(commands) == 0:
            for log in Storage.I.LOGS:        
                if log.command.check_if_key_command():
                    return True
        else:        
            command: TubeCommand
            for command in commands:
                if command.check_if_key_command():
                    return True        
        return False

class TubeCommandUtility():
    
    @classmethod
    def reset_command_skip(self, tube_run, curr_command: TubeCommand):
        '''
        Reset tube commands skip property.
        '''
        command: TubeCommand
        curr_skip_steps = 0
        for index, command in enumerate(tube_run):
            # skip previous and newly added commands
            if index < curr_command.index or command.is_redo_added == True:
                continue
            # only [m] parameters is provided
            if curr_command.is_fail_skip == True and curr_command.is_success_skip == False:
                curr_skip_steps += 1
                if curr_command.log.status == Storage.I.C_FAILED:                
                    if curr_skip_steps <= curr_command.fail_skip_steps:
                        command.is_skip = True
                    else:
                        break
                else:
                    break
            # both [m] [n] parameter are provided
            if curr_command.is_fail_skip == True and curr_command.is_success_skip == True:
                curr_skip_steps += 1   
                if curr_command.log.status == Storage.I.C_FAILED:
                    if curr_skip_steps <= curr_command.fail_skip_steps:
                        command.is_skip = True
                    else:
                        break
                if curr_command.log.status == Storage.I.C_SUCCESSFUL:
                    if curr_skip_steps > curr_command.fail_skip_steps and \
                        curr_skip_steps <= curr_command.success_skip_steps + curr_command.fail_skip_steps:
                        command.is_skip = True
                        pass
                    elif curr_skip_steps > curr_command.success_skip_steps + curr_command.fail_skip_steps:
                        break
        
    @classmethod               
    def insert_failed_redo_commands(self, tube_run, redo_command_index, redo_command: TubeCommand):
        '''
        Insert redo failed commands to the tube.
        '''
        # insert redo command first
        command_new = TubeCommand(redo_command.cmd_type, redo_command.redo_content)
        command_new.is_redo_added = True
        command_new.original_uuid = redo_command.uuid
        command_new.tube = redo_command.tube
        command_new.sub_tube = redo_command.sub_tube 
        
        tube_run.insert(redo_command_index + 1, command_new ) 
        
        # check if go back steps
        if redo_command.redo_steps >= 0:
            return    
        
        # get back steps into a list first
        back_steps = abs(redo_command.redo_steps)
        back_commands = []
        count = 0
        command: TubeCommand
        for i in range(redo_command_index - 1, -1, -1):        
            command = tube_run[i]
            if command.is_redo_added:
                continue
            command_new = TubeCommand(command.cmd_type, command.original_content)
            command_new.is_redo_added = True
            command_new.original_uuid = command.uuid 
            command_new.tube = command.tube
            command_new.sub_tube = command.sub_tube   
            back_commands.insert(0, command_new)
            count += 1
            if count >= back_steps:
                break
            
        # insert back steps to the new list
        insert_at_index = redo_command_index + 1
        for command in back_commands:
            tube_run.insert(insert_at_index, command)
            insert_at_index += 1
        
    @classmethod       
    def insert_success_redo_commands(self, tube_run, redo_command_index, redo_command: TubeCommand):
        '''
        Insert redo success commands to the tube.
        '''
        
        # the count of newly inserted command equals 
        # insert_count = redo_steps - 1
        # then the total is equal redo_steps
        for i in range(1, redo_command.redo_steps):
            command_new = TubeCommand(redo_command.cmd_type, redo_command.redo_content)
            command_new.is_redo_added = True
            command_new.original_uuid = redo_command.uuid
            command_new.tube = redo_command.tube
            command_new.sub_tube = redo_command.sub_tube
        
            tube_run.insert(redo_command_index + i, command_new ) 

class TubeVersion():
    
    '''
    Command Tube version format: x.x.x
    #1: Major version (number)
    #2: Minor version (number)
    #3: Fix or build version (character)
    '''
    
    def __init__(self, yaml_version) -> None:
        self.major_version = 0
        self.minor_version = 0
        self.fix_version = '0'
        # split versions
        if yaml_version:            
            version_array = yaml_version.split('.')
            if len(version_array) >= 3:
                self.major_version = int(version_array[0])
                self.minor_version = int(version_array[1])
                self.fix_version = str(version_array[2])
                if len(version_array) == 4:
                    self.fix_version += '.' + str(version_array[3])

class Matrix():  
    '''
    The main code of this Matrix class are from: https://github.com/jsbueno/terminal_matrix
    '''
    MAX_CASCADES = 600
    MAX_COLS = 20
    FRAME_DELAY = 0.03
    MAX_SPEED  = 5
    CSI = '\x1b[' # \x1b = ESC # https://en.wikipedia.org/wiki/ANSI_escape_code
    
    Is_Ended = False
    cols, lines = 10, 10

    mprint = lambda command: print(Matrix.CSI, command, sep='', end='')
    get_chars = lambda start, end: [chr(i) for i in range(start, end)]

    black, green, white = '30', '32', '37'

    latin_chars = get_chars(0x30, 0x80)
    greek_chars = get_chars(0x390, 0x3d0)
    hebrew_chars = get_chars(0x5d0, 0x5eb)
    cyrillic_chars = get_chars(0x400, 0x50)

    chars_all = latin_chars + greek_chars + hebrew_chars + cyrillic_chars

    @staticmethod
    def __pareto(limit):
        scale = lines // 2
        number = (paretovariate(1.16) - 1) * scale
        return max(0, limit - number)

    @staticmethod
    def __init():
        global cols, lines        
        cols, lines = shutil.get_terminal_size()
        Matrix.mprint('2J') # clear terminal screen characters        
        Matrix.mprint('?25l')  # Hides cursor
        Matrix.mprint('s')  # Saves cursor position
        Matrix.Is_Ended = False # reset endded flag

    @staticmethod
    def __print_at(char, x, y, color='', bright='0'):
        Matrix.mprint('%d;%df' % (y, x))
        Matrix.mprint(bright + ';' + color + 'm')
        print(char, end='', flush=True)

    @staticmethod
    def __update_line(speed, counter, line):
        counter += 1
        if counter >= speed:
            line += 1
            counter = 0
        return counter, line

    @staticmethod
    def __cascade(col):
        speed = randrange(1, Matrix.MAX_SPEED)
        espeed = randrange(1, Matrix.MAX_SPEED)
        line = counter = ecounter = 0
        oldline = eline = -1
        erasing = False
        bright = '1'
        limit = Matrix.__pareto(lines)
        while True:
            counter, line = Matrix.__update_line(speed , counter, line)
            if randrange(10 * speed) < 1:
                bright = '0'
            if line > 1 and line <= limit and oldline != line:
                Matrix.__print_at(choice(Matrix.chars_all),col, line-1, Matrix.green, bright)
            if line < limit:
                Matrix.__print_at(choice(Matrix.chars_all),col, line, Matrix.white, '1')
            if erasing:
                ecounter, eline = Matrix.__update_line(espeed, ecounter, eline)
                Matrix.__print_at(' ',col, eline, Matrix.black)
            else:
                erasing = randrange(line + 1) > (lines / 2)
                eline = 0
            yield None
            oldline = line
            if eline >= limit:
                Matrix.__print_at(' ', col, oldline, Matrix.black)
                break

    @staticmethod
    def __add_new(cascading):
        if randrange(Matrix.MAX_CASCADES + 1) > len(cascading):
            col = randrange(cols)
            for i in range(randrange(Matrix.MAX_COLS)):
                cascading.add(Matrix.__cascade((col + i) % cols))
            return True
        return False

    @staticmethod
    def __iterate(cascading):
        stopped = set()
        for c in cascading:
            try:
                next(c)
            except StopIteration:
                stopped.add(c)
        return stopped

    @staticmethod
    def __main():
        global cols, lines
        cascading = set()
        while not Matrix.Is_Ended:
            while Matrix.__add_new(cascading): pass
            stopped = Matrix.__iterate(cascading)
            sys.stdout.flush()
            cascading.difference_update(stopped)
            cols, lines = shutil.get_terminal_size()
            time.sleep(Matrix.FRAME_DELAY)
            
    @staticmethod
    def start():
        try:
            Matrix.__init()
            Matrix.__main()
        except KeyboardInterrupt:
            Matrix.end()
        finally:
            Matrix.end()

    @staticmethod
    def end():
        Matrix.Is_Ended = True # set ended flag
        Matrix.mprint('m')   # reset attributes
        Matrix.mprint('2J')  # clear screen
        Matrix.mprint('u')  # Restores cursor position
        Matrix.mprint('?25h')  # Show cursor              

class MatrixThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
      
    def run(self):
        Matrix.start()    
    
    def stop(self):
        Matrix.end()   
 
# -------- END OF CLASSES -------

# --------- FUNCTIONS --------------------
def tprint(line='', prefix=None, type=None, tcolor=None, tcolor_style=None, tcolor_back=None, splitchar=': '):
    
    '''
    Args:
        line: the string to output to the console
        prefix: Any character print at the begining
        type: it could be 'INFO', 'WARNING', 'ERROR' or ''
        tcolor: the color of the main printed string
        tcolor_stype: the color style: ex: 'bright'
        tcolor_back: color back end

        output: prefix + type + line
    '''
    
    # return if in matrix terminal mode
    if Storage.I.IS_MATRIX_MODE_RUNNING:
        return
    
    # switch color style
    if os.name.startswith('nt') and not tcolor_style:
        tcolor_style = 'bright'
    
    # set default color type
    if type == Storage.I.C_PRINT_TYPE_WARNING:
        type = color(type + splitchar, fore=Storage.I.C_PRINT_COLOR_ORANGE, style=tcolor_style, back=tcolor_back)
    elif type == Storage.I.C_PRINT_TYPE_ERROR:
        type = color(type + splitchar, fore=Storage.I.C_PRINT_COLOR_RED, style=tcolor_style, back=tcolor_back)
        if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:
            traces = traceback.format_exc()
            if not traces.startswith('NoneType'):
                line += '\n' + traces
    elif type == Storage.I.C_PRINT_TYPE_INFO:
        type = color(type + splitchar,fore=Storage.I.C_PRINT_COLOR_BLUE, style=tcolor_style, back=tcolor_back)
    elif type == Storage.I.C_PRINT_TYPE_DEBUG:
        type = color(type + splitchar,fore=Storage.I.C_PRINT_COLOR_PURPLE, style=tcolor_style, back=tcolor_back)
    else:
        type = Storage.I.C_PRINT_TYPE_EMPTY
    
    # deal with main color
    if tcolor:
        line = color(line, fore=tcolor, style=tcolor_style, back=tcolor_back)
    
    # combine type + str    
    line = type + line
    
    # deal with prefix
    if prefix == None:
        line = Storage.I.C_PRINT_PREFIX + splitchar + line
    elif prefix == '':
        line = line      
    else:
        line = prefix + splitchar + line  
    
    # finally print it 
    print(line)
             
def write_line_to_log(file, mode='a+', line=''):
    '''
    Write line content into a file.

    Parameters:
        file: File full name.
        mode: Default 'a+'. File access modes: \n
              ReadOnly(r), ReadAndWrite(r+), WriteOnly(w), \n 
              WriteAndRead(w+), AppendOnly(a), AppendAndRead(a+)
        line: Content to write.
    '''
    try:    
        with open(file, mode) as f:            
            f.write(line + '\n')
    except Exception as e:
        msg = 'Write line to logfile with exception: ' + str(e)
        tprint(msg, type=Storage.I.C_PRINT_TYPE_ERROR)

def get_installed_packages_version(package_name):
    if len(Storage.I.INSTALLED_PACKAGES) == 0:
        proc = subprocess.Popen([Storage.I.PIP_NAME, 'freeze'], stdout=subprocess.PIPE)
        while True:
            line = proc.stdout.readline()
            if not line:
                break
            else:
                Storage.I.INSTALLED_PACKAGES.append(line)
    for line in Storage.I.INSTALLED_PACKAGES:
        line = (str(line.rstrip())[1:]).replace('\'','')
        installed_pkg = line.split('==')
        if(installed_pkg[0] == package_name):
            return installed_pkg[1] 
    return None  

def install_package(package_name):
    installed = False
    version = get_installed_packages_version(package_name)
    if version != None:
        installed = True
    if not installed:
        msg = 'Prepare to install package %s' % package_name
        print(msg)
        write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
        result = None
        if(os.name.startswith('nt')):
            result = subprocess.run([Storage.I.PIP_NAME, 'install', package_name], text=True, shell=True)
        else:
            # to support Mac OS or Linux
            result = subprocess.run([Storage.I.PIP_NAME, 'install', package_name])
        if result.returncode == 0:
            msg = 'Installed ' + package_name + ' package successfully.'
            print(msg)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
            installed = True
        else:
            msg = 'Installed ' + package_name + ' package failed.'
            print(msg)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
            installed = False
    return installed

def check_disk_space(ssh):
    
    # each host only checked once
    if Storage.I.CURR_HOST in Storage.I.DISK_SPACE_STATUS.keys():
        return
    
    # initial disk check result to empty
    disk_check_result = []
    
    try:
        # run a current linux 'df -h' command
        stdin, stdout, stderr = ssh.exec_command(Storage.I.CURR_HOST_PROFILE + Storage.I.GOTO_HOST_ROOT + 'df -h') 
        seq = 0
        while True:
            line = stdout.readline()
            if not line:
                break        
            seq = seq + 1
            line_array = line.split(' ')
            if seq > 1:
                for s in line_array:
                    if len(s) > 0 and '%' in s:
                        s = int(s.replace('%', '').strip())
                        if s >= 80:
                            disk_check_result.append(line.replace('\n', ''))
            else:
                disk_check_result.append(line.replace('\n', ''))
        
        if len(disk_check_result) == 1:
            disk_check_result = []
    except Exception as e:
        msg = 'DISK SPACE CHECK EXCEPTION on server: ' + Storage.I.CURR_HOST
        msg += '\nerrors: ' + str(e) 
        tprint(msg, type=Storage.I.C_PRINT_TYPE_ERROR)
        write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
        disk_check_result = []            
        
    # finally add the result to the dict
    Storage.I.DISK_SPACE_STATUS[Storage.I.CURR_HOST] = disk_check_result

def output_disk_space_check():
    
    for key in Storage.I.DISK_SPACE_STATUS.keys():
    
        if len(Storage.I.DISK_SPACE_STATUS[key]) == 0:
            continue
        line = '\n----- Disk Space (' + key + ') ( >= 80% ) -----' 
        tprint(line)
        write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', line)
        for line in Storage.I.DISK_SPACE_STATUS[key]:
            tprint(line, tcolor=Storage.I.C_PRINT_COLOR_ORANGE)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', line)
        line = '----- End of Checking Linux Disk Space -----'
        tprint(line)
        write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', line)

def print_input_parameters():
    tprint('-------------------------------')
    tprint('# Your Input Parameters #', tcolor=Storage.I.C_PRINT_COLOR_GREEN)
    tprint('-------------------------------')
    if Storage.I.IS_IMMEDIATE:
        tprint('Start Time      : %s' % (str(Storage.I.EXEC_DATETIME.strftime(Storage.I.C_DATETIME_FORMAT))))
        tprint('Run Immediately : %s' % str(Storage.I.IS_IMMEDIATE), tcolor=Storage.I.C_PRINT_COLOR_YELLOW)
    else:
        tprint('Start Time      : %s' % str(Storage.I.EXEC_DATETIME.strftime(Storage.I.C_DATETIME_FORMAT)), tcolor=Storage.I.C_PRINT_COLOR_YELLOW)
        tprint('Run Immediately : %s' % str(Storage.I.IS_IMMEDIATE))  
    tprint('Loop Mode       : %s' % str(Storage.I.IS_LOOP))   
    if(Storage.I.TUBE_YAML_FILE):
        tprint('Tube File:      : %s' % Storage.I.TUBE_YAML_FILE)
    if(Storage.I.IS_LOOP):
        duration, unit = Utility.format_duration_unit(Storage.I.NEXT_REFRESH)
        tprint('Loop Interval   : %.1f %s' % (duration, unit))       
        tprint('Loop Times      : %s' % str(Storage.I.LOOP_TIMES)) 
    tprint('Sent Email      : %s' % str(Storage.I.IS_SENT_EMAIL))
    tprint('\n             Tube Commands')
    tprint('-------------------------------------------------------')
    header_format = '   Seq   | %' + str(Storage.I.MAX_TUBE_COMMAND_LENGTH) + 's |  Command Value'
    tprint(header_format % ('Command Type'))
    tprint('-------------------------------------------------------')
    count = 0
    print_format = '  [%03d] %' + str(Storage.I.MAX_TUBE_COMMAND_LENGTH) + 's        %s'
    for item in Storage.I.TUBE_YAML:            
        for key in item.keys():                   
            count += 1
            tprint(print_format %(count, key,  TubeCommand.format_placeholders_no_error(item[key])))
    tprint('-------------------------------------------------------------------------')

def confirm(question):

    if Storage.I.IS_FORCE_RUN:
        return True

    '''
    Ask user to enter Y or N (case-insensitive).
    :return: True if the answer is Y.
    :rtype: bool
    '''
    answer = ''
    while answer not in ['y', 'n']:
        answer = input(question).lower() 
    return answer == 'y'

def output_tube_file_list(is_print=False, is_write_log=False, indexes=None, lines=None):
    keys = [k for k in Storage.I.TUBE_FILE_LIST.keys()]
    keys.sort()  
    for k in keys:
        if indexes and not k in indexes:
            continue
        item = Storage.I.TUBE_FILE_LIST[k]
        file = item[item.index('=')+1:]
        tube_name = item[0:item.index('=')]
        msg = '* [%s]: %s[%s]' % (str(k), file, tube_name)
        if lines:
            lines.append(msg)
        if is_print:
            tprint(msg, prefix='')
        if is_write_log:
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)   

def print_logs(LOGS):
    tprint(prefix='')    
    
    # print status of each command
    tprint('----- Status of Each Command -----', prefix='')    
    seq = 0
    total_minutes = 0
    total_seconds = 0
    has_retried_command = False
    log: TubeCommandLog
    for log in LOGS:
        if log.command.is_redo_added == True:
            has_retried_command = True
        seq += 1
        total_minutes += log.get_total_minutes()
        total_seconds += log.get_total_seconds()
        log.print_log(seq)
    # output tube file list as a note
    output_tube_file_list(is_print=True)   
    # If output note for * after command type    
    if has_retried_command == True:
        tprint(Storage.I.C_RETRIED_COMMAND_NOTE, prefix='') 
    
    # print overall tube logs at the end
    # then it's easier for the user to see
    tprint(prefix='') 
    tprint(Storage.I.C_FINISHED_HEADER, tcolor=Storage.I.C_PRINT_COLOR_YELLOW, prefix='')
    tprint(calculate_success_failed_details(False), prefix='')
    tprint(prefix='')   
    
    # print total running during time
    totals = '%s minutes' % str(int(divmod(total_seconds, 60)[0]))
    if total_seconds < 60:
        totals = '%s seconds' % str(total_seconds)
    tprint('-------------------------------', prefix='')
    tprint('Total Time: %s' % totals, prefix='')
    tprint('-------------------------------', prefix='')

def get_command_result_by_uuid(uuid, commands = []):
    '''
    Get command result by UUID
    
    Args:
        uuid: The UUID of the command
        tube: The tube you want to check, if not provided then check all the linked log commands
    '''
    command: TubeCommand
    status = Storage.I.C_FAILED
    if len(commands) == 0:
        for log in Storage.I.LOGS:
            command = log.command
            if command.original_uuid == uuid:
                if command.log.status == Storage.I.C_SKIPPED and status == Storage.I.C_FAILED:
                    status = Storage.I.C_SKIPPED
                elif command.log.status == Storage.I.C_SUCCESSFUL and status != Storage.I.C_SUCCESSFUL:
                    status = Storage.I.C_SUCCESSFUL
                    return status
    else:        
        for command in commands:
            if command.original_uuid == uuid:
                if command.log.status == Storage.I.C_SKIPPED and status == Storage.I.C_FAILED:
                    status = Storage.I.C_SKIPPED
                elif command.log.status == Storage.I.C_SUCCESSFUL and status != Storage.I.C_SUCCESSFUL:
                    status = Storage.I.C_SUCCESSFUL
                    return status
    return status

def calculate_success_failed_details(is_for_email):
    
    '''
    Calculate overall (main tube) status by log details
    '''
    
    success_count = 0
    failed_count = 0    
    skipped_count = 0
    details = None
    result = None

    # calcualte success and failed count
    command: TubeCommand
    for command in Storage.I.TUBE_RUN:
        log = command.log
        if log.status == Storage.I.C_FAILED:
            failed_count += 1
        elif log.status == Storage.I.C_SUCCESSFUL:
            success_count += 1
        elif log.status == Storage.I.C_SKIPPED:
            skipped_count +=1

    # prepared success and failed details count
    details = '[SUCCESS:%s, FAIL:%s, SKIP:%s]' % (success_count, failed_count, skipped_count)
    newline = ']\n'
    if is_for_email:
        newline = ']<br>'
    
    loops = ''
    if Storage.I.IS_LOOP:
        loops = ' LOOP: (%s/%s)' % (str(Storage.I.CURR_LOOP_ID), str(Storage.I.LOOP_TIMES))

    # ouput overall status
    key_command_exists_all = StorageUtility.check_if_key_command_exists(Storage.I.TUBE_RUN)    
    result = '['
    if not key_command_exists_all:
        # there are no key commands at all
        if failed_count == 0:
            result += Storage.I.C_TUBE_SUCCESSFUL + loops + newline + details
        elif failed_count > 0 and success_count > 0:
            result += Storage.I.C_TUBE_PARTIAL_SUCCESSFUL + loops + newline + details   
        elif failed_count > 0 and success_count == 0:
            result += Storage.I.C_TUBE_FAILED + loops + newline + details
    else:
        result_tmp = Storage.I.C_SUCCESSFUL
        command: TubeCommand
        for command in Storage.I.TUBE_RUN:
            # we can skip the --if no cases          
            if command.check_if_key_command() and (command.is_skip_by_if == False or command.is_skip_by_while == False):
                key_command_result = get_command_result_by_uuid(command.original_uuid, Storage.I.TUBE_RUN.copy())
                if key_command_result != Storage.I.C_SUCCESSFUL:
                    result_tmp = Storage.I.C_FAILED
                    break
        
        # include the loops and details information
        result += result_tmp + loops + newline + details

    return result

def calc_success_failed_for_tube(commands):
    
    '''
    Get tube success or failed status
    It doesn't calculete its sub-tube status
    '''
    
    success_count = 0
    failed_count = 0    
    skipped_count = 0
    result = None

    # calcualte success and failed count
    for command in commands:
        log = command.log
        if log.status == Storage.I.C_FAILED:
            failed_count += 1
        elif log.status == Storage.I.C_SUCCESSFUL:
            success_count += 1
        elif log.status == Storage.I.C_SKIPPED:
            skipped_count +=1

    # ouput overall status
    key_command_exists_all = StorageUtility.check_if_key_command_exists(commands)    
    result = Storage.I.C_TUBE_SUCCESSFUL
    if not key_command_exists_all:
        # there are no key commands at all
        if failed_count > 0:
            result = Storage.I.C_TUBE_FAILED
    else:
        result_tmp = Storage.I.C_SUCCESSFUL
        command: TubeCommand
        tube_temp = commands.copy()
        for command in commands:
            # we can skip the --if no cases          
            if command.check_if_key_command() and (command.is_skip_by_if == False or command.is_skip_by_while == False):
                key_command_result = get_command_result_by_uuid(command.original_uuid, tube_temp)
                if key_command_result != Storage.I.C_SUCCESSFUL:
                    result_tmp = Storage.I.C_FAILED
                    break
        
        # include the loops and details information
        result = result_tmp

    return result

def write_logs_to_file(LOGS):
    
    mode = 'a+'
    # output overall status
    write_line_to_log(Storage.I.TUBE_LOG_FILE, mode, '')
    write_line_to_log(Storage.I.TUBE_LOG_FILE, mode, Storage.I.C_FINISHED_HEADER)

    result = calculate_success_failed_details(False)
    write_line_to_log(Storage.I.TUBE_LOG_FILE, mode, result) 

    # log failed detail errors 
    has_retried_command = False
    has_written_header = False
    log: TubeCommandLog     
    for index, log in enumerate(LOGS):        
        if log.status == Storage.I.C_FAILED:
            if not has_written_header:
                write_line_to_log(Storage.I.TUBE_LOG_FILE, mode,  Storage.I.C_FAILED_COMMAND_LIST)  
                has_written_header = True   
            command_details = '[%s] - %s: %s' % (str(index+1), log.command.get_formatted_type(), str(log.command.content))
            write_line_to_log(Storage.I.TUBE_LOG_FILE, mode,  command_details) 
            for error in log.errors:
                error = error.replace('\n','').replace('\t', Storage.I.C_INDENTATION)
                if len(error) == 0:
                    continue
                write_line_to_log(Storage.I.TUBE_LOG_FILE, mode, Storage.I.C_INDENTATION + error)    
    
    # output each step status
    write_line_to_log(Storage.I.TUBE_LOG_FILE, mode, '\n----- Status of Each Step -----')    
    seq = 0
    total_minutes = 0
    total_seconds = 0
    for log in LOGS:
        if log.command.is_redo_added == True:
            has_retried_command = True
        seq += 1
        total_minutes += log.get_total_minutes()
        total_seconds += log.get_total_seconds()
        write_line_to_log(Storage.I.TUBE_LOG_FILE, mode, log.format_log(seq, include_index=True))
    
    # output tube file list
    output_tube_file_list(is_write_log=True)
    # If output note for * after command type
    if has_retried_command == True:
        write_line_to_log(Storage.I.TUBE_LOG_FILE, mode, Storage.I.C_RETRIED_COMMAND_NOTE)
    # totals
    totals = '%s minutes' % str(int(divmod(total_seconds, 60)[0]))
    if total_seconds < 60:
        totals = '%s seconds' % str(total_seconds)
    write_line_to_log(Storage.I.TUBE_LOG_FILE, mode, '--------------------------------')  
    write_line_to_log(Storage.I.TUBE_LOG_FILE, mode, 'Start at   : ' + Storage.I.START_DATE_TIME.strftime(Storage.I.C_DATETIME_FORMAT))      
    write_line_to_log(Storage.I.TUBE_LOG_FILE, mode, 'Finish at  : ' + datetime.now().strftime(Storage.I.C_DATETIME_FORMAT))
    write_line_to_log(Storage.I.TUBE_LOG_FILE, mode, 'Total Time : %s' % totals)
    write_line_to_log(Storage.I.TUBE_LOG_FILE, mode, '--------------------------------')

def send_email(sender_address, sender_password, receiver_address_list, subject, body_html, smtp_server):
    sent = False
    try:
        sender_address   = sender_address.strip()
        sender_pass      = sender_password.strip()

        #Create SMTP session for sending the mail
        session = smtplib.SMTP(smtp_server, Storage.I.EMAIL_SERVER_PORT)
        session.starttls() #enable security
        session.login(sender_address, sender_pass) #login with mail_id and password       

        # Split the receiver_address_list
        receiver_address_array = receiver_address_list.split(',')
        for receiver_address in receiver_address_array:            
            #Setup the MIME
            message = MIMEMultipart()
            message['From']    = 'TUBE ' + f'<{sender_address}>'
            message['To']      = receiver_address.strip()
            message['Subject'] = subject
            #The body and the attachments for the mail
            message.attach(MIMEText(body_html, 'html')) # plain?
            
            text = message.as_string()
            session.sendmail(sender_address, receiver_address.strip(), text)

        # Quit the email session
        session.quit()
        sent = True
    except Exception as e:
        msg = 'SEND EMAIL EXCEPTION:' + str(e)
        tprint(msg, type=Storage.I.C_PRINT_TYPE_ERROR)
        write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
    
    return sent

def prepare_emails_content_and_sent(LOGS):
    msg = 'Email sending...'
    tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO)
    write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)

    email_body = ''
    has_failed = False
    split_line = '------------------------------- <br><br>'
    # include errors into email
    result = calculate_success_failed_details(True)
    email_body += result + '<br>'

    # log failed errors    
    log: TubeCommandLog
    for index, log in enumerate(LOGS):        
        if log.status == Storage.I.C_FAILED:
            if not has_failed:
                email_body += Storage.I.C_FAILED_COMMAND_LIST + '<br>'    
                has_failed = True            
            command_details = '[%s] - %s: %s' % \
                (str(index+1), log.command.get_formatted_type(), str(log.command.content))
            email_body += command_details + '<br>'
            for error in log.errors:
                error = error.replace('\n','')
                if len(error) == 0:
                    continue
                email_body += error + '<br>'

    # add a split line
    email_body += split_line

    email_body += '----- Status of Each Step -----<br>'
    seq = 0
    total_minutes = 0
    total_seconds = 0
    for log in LOGS:
        seq += 1
        total_minutes += log.get_total_minutes()
        total_seconds += log.get_total_seconds()
        line = log.format_log(seq)     
        email_body += line + '<br>'
    # total time
    totals = '%s minutes' % str(int(divmod(total_seconds, 60)[0]))
    if total_seconds < 60:
        totals = '%s seconds' % str(total_seconds)
    email_body += '-------------------------------<br>'
    email_body += '<br>Total Time   : ' + totals + ' <br></body>'
    email_body = '<font face="monospace">' + email_body + '</font>'

    # disk space checking
    for key in Storage.I.DISK_SPACE_STATUS.keys():
        if len(Storage.I.DISK_SPACE_STATUS[key]) > 0:
            email_body += '<br><br><b>----- Disk Space (' + key + ') ( >= 80% ) -----</b><br>'
        for line in Storage.I.DISK_SPACE_STATUS[key]:
            email_body += line + '<br>'
        if len(Storage.I.DISK_SPACE_STATUS) > 0:
            email_body += '----- End of Checking Linux Disk Space -----<br>'
    
    # prepare to sent email
    result = send_email(Storage.I.EMAIL_SENDER_ADDRESS, Storage.I.EMAIL_SENDER_PASSWORD, Storage.I.EMAIL_RECEIVER_ADDRESS, 
                        Storage.I.EMAIL_SUBJECT, email_body, Storage.I.EMAIL_SMTP_SERVER)
    if result == True:
        msg = 'Email sent successfully!'
        tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO)
        write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
    msg = '--------------------------------'
    tprint(msg, prefix='')
    write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)

def calculate_progress_status(commands) -> str:
    command: TubeCommand
    total_count = 0
    finished_count = 0
    for command in commands:
        # total command count
        total_count += 1
        # finished command count
        if command.log and command.log.status != None:
            finished_count += 1
    
    return 'PROGRESS: (%s/%s)' % (str(finished_count), str(total_count))

def output_log_header():
    # Log start for xxx.yaml.log    
    Storage.I.START_DATE_TIME = datetime.now()
    run_mode = ' (%s)' % Storage.I.RUN_MODE
    open_file_mode = 'w' if Storage.I.IS_CLEAR_LOG else 'a+'
    header = Storage.I.C_LOG_HEADER if open_file_mode == 'w' else '\n' + Storage.I.C_LOG_HEADER
    write_line_to_log(Storage.I.TUBE_LOG_FILE, open_file_mode, 
                      Storage.I.C_LOG_HEADER + 
                      Storage.I.START_DATE_TIME.strftime(Storage.I.C_DATETIME_FORMAT) +
                      run_mode)

def output_user_console_inputs():
    user_inputs = ''
    for s in sys.argv:
        user_inputs += s + ' '
    if user_inputs and len(user_inputs) > 0:
        write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', 
                      'User inputs form console >>> ' + user_inputs)        

def init_log_file():
    # check the log file size in the begining
    if(path.exists(Storage.I.TUBE_LOG_FILE)):
        try:
            if Utility.get_file_size(Storage.I.TUBE_LOG_FILE, 'MB') > 5: # file size greater than 5 MB
                # backup log file: copy to new filename, and delete current
                # copy to new file name
                copyfile(Storage.I.TUBE_LOG_FILE, Storage.I.TUBE_LOG_FILE + '.backup')
                # delete the big log file
                os.remove(Storage.I.TUBE_LOG_FILE)
        except Exception as e:
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', 'Backup log file failed:' + str(e))

    # Log start for xxx.yaml.log    
    run_mode = ' (%s)' % Storage.I.RUN_MODE
    write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', 
                      Storage.I.C_JOB_HEADER + datetime.now().strftime(Storage.I.C_DATETIME_FORMAT) +
                      run_mode)
    # Log tube name information
    tube_name = Storage.I.TUBE_YAML_FILE
    if tube_name:
        write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+',
                          '** Running Tube: ' + tube_name) 

def init_arguments():
    # parameters for user inputs       
    parser.add_argument('-y', '--yaml', dest='yaml_config',
                        help='Command Tube file with YAML format. \nUse \'help template\' could print the YAML file template.' + \
                             '\nFor quick you could leave out the file name extension .yaml or .yml') 
    parser.add_argument('-t', '--tube', dest='yaml_config',
                        help='Command Tube file with YAML format. \nUse \'help template\' could print the YAML file template.' + \
                             '\nFor quick you could leave out the file name extension .yaml or .yml') 
    parser.add_argument('-v', '--vars', type=str, dest='variables', nargs='+',
                        help='Pass tube variables into tube: var1=value1 var2=value2')                 
    parser.add_argument('-i', '--immediate', dest='immediate', action='store_const', const='yes',
                        help='A flag to tell if run the tube immediately, but needs a user confirm. \nDefault no.')  
    parser.add_argument('-f', '--force', dest='force', action='store_const', const='yes',
                        help='A flag to run tube at once without confirmation. \nDefault no.') 
    parser.add_argument('-d', '--debug', dest='debug', action='store_const', const='yes',
                        help='A flag to run tube in debug mode. \nDefault no.') 
    parser.add_argument('--datetime', dest='datetime',
                        help='At what datetime to start this job. \nFORMAT: [mm/dd/yy H:M:S] e.g.: \'03/18/20 6:00:00\'; ' +
                             '\nIt also supports addition format \'n/tXX o\'clock, means next or this XX o\'clock. \ne.g.: \'n7\', means next 7:00 o\'clock; ' + \
                             '\'t7.5\' means this 7:30 o\'clock.')    
    parser.add_argument('-l', '--loop', dest='period_of_next_run', type=str,
                        help='Tube will enable loop mode and run once for every given period. \ne.g: -l 24 means every 24 hours; ' + \
                             '\n     -l 30m means every 30 minutes; \n     -l 2d means every two days. \nIn IMEDIATE/FORCE mode, it will run next iteration at once.')
    parser.add_argument('--times', dest='run_times', type=int,
                        help='Iteration times of tube. Default 1024.')  
    parser.add_argument('-e', '--email', dest='email', action='store_const', const='yes',
                        help='A flag to tell if sent result to your Email. \nNeed complete Email configurations first. Default no.')
    parser.add_argument('-m', '--matrix-mode', dest='matrix_mode', action='store_const', const='yes',
                        help='A flag to run terminal in matrix mode. Defalut no.')
    parser.add_argument('--report-progress', dest='report_progress', action='store_const', const='yes',
                        help='A flag to report each tube command progress via Email. Defalut no.')
    parser.add_argument('--log', dest='log_file', nargs=1,
                        help='Set log file name. Default is tube file name plus \'.log\'.')
    parser.add_argument('-c', '--clear-log', dest='clear_log', action='store_const', const='yes',
                        help='A flag to tell if clear tube log content first. Default no.')
    parser.add_argument('--pip', dest='pip_command',
                        help='To tell which pip command is used. e.g.: pip or pip3. \nWindows system is default pip, and MacOS system is default pip3. ' + \
                              '\nUsually you don\'t need to provide this parameter value, \nexcept in Windows system, it\'s not pip and in MacOS, it\'s not pip3.')                                                    
    parser.add_argument('--version', action='version', version=Storage.I.C_CURR_VERSION,
                        help='Print current version.')  
    parser.add_argument('args', type=str, nargs='*', 
                         help=Storage.I.C_HELP)     

    # general_command_parser is used to analyze the COMMAND or LINUX_COMMAND arguments
    general_command_parser.add_argument(Storage.I.C_CONTINUE_PARAMETER, dest='continue_steps', type=str, help=argparse.SUPPRESS, nargs='*')   
    general_command_parser.add_argument(Storage.I.C_REDO_PARAMETER, type=str, help=argparse.SUPPRESS, nargs='*')
    general_command_parser.add_argument(Storage.I.C_IF_PARAMETER, dest='if_run', type=str, help=argparse.SUPPRESS, nargs='+')
    general_command_parser.add_argument(Storage.I.C_KEY_PARAMETER, dest='key', action='store_true', default=False, required=False)
    general_command_parser.add_argument(Storage.I.C_PLACE_HOLDER, dest='is_raw', action='store_true', default=False, required=False)
    general_command_parser.add_argument(Storage.I.C_NOTES_PARAMETER, dest='notes', type=str, help=argparse.SUPPRESS, nargs='+')
    
def install_3rd_party_packages(args):
    
    try:        
        # return if running in binary mode
        if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_BIN:
            msg = 'Command Tube is running in binary mode.'
            print(msg)
            return
        
        # check os to set default pip command
        if(os.name.startswith('nt')):
            Storage.I.PIP_NAME = 'pip'
        else:
            Storage.I.PIP_NAME = 'pip3'
        
        # override pip command from user inputs
        if(args.pip_command != None):
            Storage.I.PIP_NAME = args.pip_command

        # check pip if installed
        try:
            process = None
            if(os.name.startswith('nt')):
                process = subprocess.run([Storage.I.PIP_NAME, '--version'], text=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                process = subprocess.run([Storage.I.PIP_NAME, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)            
            if process.returncode != 0:
                return
        except Exception:
            if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:
                print(Storage.I.C_PRINT_TYPE_INFO + ' :pip/pip3 is not installed in this system.')
            return
        
        # Install color package
        if not install_package('Colr'):
            sys.exit()

        # Install package 'paramiko'
        if not install_package('paramiko'):
            sys.exit()
        
        # install package 'beautifulsoup4'
        if not install_package('beautifulsoup4'):
            sys.exit()

        # install package 'lxml'
        if not install_package('lxml'):
            sys.exit()

        # install package 'requests'
        if not install_package('requests'):
            sys.exit()

        # install package 'pyyaml'
        if not install_package('PyYAML'):
            sys.exit()
            
    except OSError as e1:
        msg = 'ERROR: Install/Check 3-rd party packages failed with exception: ' + str(e1)
        msg += '\nIf you run in binary mode, please check if your tube run mode is BIN. ' 
        print(msg)
        sys.exit()
    except Exception as e2:
        msg = 'ERROR: Install/Check 3-rd party packages failed with exception: ' + str(e2)
        print(msg)
        sys.exit()

def disconect_all_hosts(hosts):
    try:
        for host_name in hosts.keys():
            host: Host = hosts[host_name]
            if host.is_connected:
                host.disconnect()        
    except Exception as e:
        tprint('DISCONECT ALL HOSTS EXCEPTION: ' + str(e), type=Storage.I.C_PRINT_TYPE_ERROR)

def print_tube_command_help(args):
    try:   
        if not args:
            return  
        found_match = False
        if(args.args):
            if(len(args.args) >= 1 and len(args.args) <= 3 and args.args[0].upper() == 'HELP'):
                add_notes = Storage.I.C_PROGRAM_NAME + '=' + Storage.I.C_CURR_VERSION
                help_redo = '''
        Redo: 
            Syntax: --redo [m]
            Description: 
                Without m parameter, if current command failed it  
                will be re-executed once.

                With m (m < 0) parameter, and current command failed, it will  
                redo commands from previous m steps.

                With m (m > 0) parameter, and current command success, it will
                redo this command for m times.
                '''
                help_continue = '''
        Continue:
            Syntax: --continue [m] [n]
            Description:
                If current command failed the later tube commands will be 
                conditional skiped.

                Normally if current command failed, the later tube commands 
                will be skipped. But use --continue parameter could change
                this.

                Without m and n parameters: tube will run next command.
                        
                With m (m >= 1) parameter only: If current command failed,
                the later m steps will be skipped. Otherwise the later m steps
                will be executed as normal.

                With m & n ( m,n >=0 ) both parameters: If current command faild,
                the later m steps after current will be skiped, the later n steps
                after m will be executed.
                If current command successful, the previous senario will be swapped.
                The later m steps after current will be executed and the later n steps
                after m will be skipped.
                '''
                help_if = '''
        If:            
            Syntax: --if {tube_variable} | value=={tube_variable} | value!={tube_variable}
            Description:
                If {tube_variable} uppercase equals 'FALSE' or 'NO' then the current tube command
                will be skipped.
                For value=={tube_variable} condition, if value not equal {tube_variable} then current
                command will be skipped.
                For value!={tube_variable} condition, if value equal {tube_variable} then this
                command will be skipped.
                It also support >, >=, <, <= cases, make sure the values are numbers before comparison.
                Note: Extra spaces are NOT allowed in the compare expression.
                '''
                help_key='''
        Key:
            Syntax: --key
            Description:
                This flag can tell the tube which commands are the key commands. If there are
                key commands exist, only all of them run successfully, the tube result will be 
                marked as successfull. 
                '''
                help_raw='''
        Raw:
            Syntax: --raw
            Description:
                The flag can disable the command placeholder logic.
                '''
                help_note='''
        Note:
            Syntax: --note notes
            Description:
                Add a note to the command.
                '''
                help_var = '''
    - Tube Variables  

        Define Tube Variables:  
            1. From tube YAML file, under 'VARIABLES' property, you can add tube
               variable staticly.
            2. Use tube command SET_VARIABLE to dynamic create a tube variable.
            3. Read tube variable from terminal console.
            4. Pass tube variable to sub tubes.
            5. Some tube commands like GET_FILE_KEY_VALUE can read tube variables
               from a file.     

        Default Tube Variables:      
            # Below two hidden variables are assigned values for main tube:
            TUBE_HOME: <tube-running-startup-location-path> 
            OS_NAME: <current-os-system-name>     

        Scope:
            There is one main tube and the main tube could have multiple sub tubes.
            Tube variable default is available in its own tube and its own tube's sub-tubes. 
            Using --global argument can changed this behaviour.

            << Example 1 >>
            Tube:
                - SET_VAR: x = 100
                - RUN: SubTube
                - PRINT_VARS: x  # output 100
            
            SubTube:
                - PRINT_VARS: x  # ouput 100
                - SET_VAR: x = 200
                - PRINT_VARS: x  # output 200
            
            << Example 2 >>
            Tube:
                - SET_VAR: x = 100
                - RUN: SubTube
                - PRINT_VARS: x  # output 200
            
            SubTube:
                - PRINT_VARS: x  # ouput 100
                - SET_VAR: x = 200 --global
                - PRINT_VARS: x  # output 200

        Tube Variable Usage:
            You can reference any variable value via {var-name} in your tube 
            command arguments. eg:
                - PATH: {TUBE_HOME}
                - COMMAND: ls {cmd_parameters}    
            In SET_VARIABLE command or in --if and --while conditions, you can omit the curly brackets:
                - SET: x = 1
                - SET: y = x + 1         
             
        ** Note: If variable was updated from terminal console inputs, then it will become readonly. 
                '''
                help_title = '''-------------------------------           
# Welcome to Command Tube
## version: %s
-------------------------------
                '''
                help_title = help_title % Storage.I.C_CURR_VERSION
                help_all = '''
%s                      
## Introduction

    Command Tube is a tool that can run a group of sequenced commands. 
    You can get a full list of supportted tube commands from readme document.
    Using these commands you can easily build your own tube to do tasks like:
    Refresh Development Environment, Daily Run Test Cases etc.
    It's more user friendly and eaiser to use than PowerShell.

## How to run Command Tube    

    Command Tube is a Python 3 script. The most important two arguments 
    for Command Tube are '--tube' and '--datetime'.    
    All the tube configurations are maintained by a YAML file, 
    using '--tube file' you can specify the tube configurations. 
    From the 'tube.template.yaml' (tube help tempalte could output it) you could view it.
    Use '--datetime' argument you could set the execution time, 
    you could also run it at once by parameter '-f' or '-i'.
    For more information about input arguments please use following command 
    from your terminal (Needs Python >= 3.6):
        >>> python command-tube.py -h
    
    - Examples of running Command Tube via source code:
        1: Run at once and sent result via email: 
        >>> python command-tube.py -t tube.yaml -fe
        2: Run at 20:00 o'clock:
        >>> python command-tube.py -t tube.yaml -t20
        3: Run at every 6 o'clock for 100 days: 
        >>> python command-tube.py -t tube.yaml -t n6 -l 24 -times 100
        4: Run 10 times for every 5 minutes start from 10:00:
        >>> python command-tube.py -t tube.yaml -t t10 -l 5m -times 10
        5: Run tube at 9:00 AM Feb 1, 2022:
        >>> python command-tube.py -t tube.yaml -t '02/01/22 09:00:00'
        6: Find command syntax which name contains 'file' keyword:
        >>> python command-tube.py help file
    
        ** Find tube running result from tube.yaml.log file by default 

    - Binary Mode        
        Following below steps you can use it in binary (package) mode:
        1. Download 'tube' for MacOS or 'tube.exe' for Windows from github homepage
        3. Using it from your terminal (Need exec right from MacOS):
        >>> tube -t tube.yaml -f
        
        Following below steps to build an executable package:
        1. Get source code from github: https://github.com/michael-hll/command-tube.git
        2. From terminal goto source code root directory
        3. Run below command to build the package:
           >>> python3 command-tube.py -t package-mac.yaml -f
           Once the upper command run successfully, a file 'tube' will be output
           under the dist folder.
        4. Run tube version command to verify it's built successfully:
           >>> ./tube --version 
    
## General Arguments & Tube Variables
    - General Arguments
        Description: Most of tube commands support additional --continue, --redo,
                 --key, --if, --raw and --note general arguments. It could make your tube realize
                 more complex flow.         
%s
%s
%s
%s
%s
%s
%s
                '''
                help_all = help_all % (help_title, help_continue, help_redo.replace('\n', '', 1), 
                            help_if.replace('\n', '', 1), help_key.replace('\n', '', 1), 
                            help_raw.replace('\n', '', 1), help_note.replace('\n', '', 1), help_var)
                
                template = '''
Version: 2.0.x            
# Run_Mode is either SRC or BIN
Run_Mode: BIN
Servers:
    - Server:
        Name: server1
        Host: server1.xxx.com
        SSH_Port: 22
        User: root
        Password: $passwords.ini
        Root: /home/root
        Profile: source /etc/profile
    - Server:
        Name: server2
        Host: server2.xxx.com
        SSH_Port: 22
        User: root
        Password: $passwords.ini
        Root: /home/root
        Profile: source /etc/profile
Email:
    Email_SMTP_Server: smtp.office365.com
    Email_Server_Port: 587
    Email_Sender_Address: <sender email address>
    Email_Sender_Password: $passwords.ini
    Email_Receiver_Address: <receiver email address comma list>
    Email_Subject: Tube Email Subject
Variables:
    bl_root_folder: c:\workspaces\dev\project
    drive: X
    run: yes
    xxx-app: 1.0.0.0
Tube:
    # ----------------------------------------------------
    # You can use below command to view all command syntax
    # >>> python command-tube.py help
    # Or you can read README.md to get details
    # ----------------------------------------------------
    # Run a windows or Mac OS command
    - COMMAND: dir
    # Example of switching servers, connect to SERVER:HOST
    - CONNECT: server1.xxx.com
    # Example of delete a line which begin with 'hello'
    - DELETE_LINE_IN_FILE: -f tmp.txt -b hello
    # Sent an Email
    - EMAIL: -t michael_hll@hotmail.com -s Email Subject -b this is the content of your email
    # Example of read a XML file tag value using xpath
    - GET_XML_TAG_TEXT: -f xxx.xml -x xpath
    # Read key-value from a file and store them into tube variables
    - GET_FILE_KEY_VALUE: -f config.ini
    # Example of import commands from a sub tube 
    - RUN_TUBE: sub-tube.yaml
    # Run a linux command, make sure the server is connected by CONNECT command
    - LINUX_COMMAND: ls
    # Example of go to a directory
    - PATH: X:\dev\\trunk
    # To pause 30.5 minutes, in order to wait linux vm is up
    - PAUSE: 30.5
    # Example of report current tube progress
    - REPORT_PROGRESS: Refresh Code Failed
    # Example of set file key value
    - SET_FILE_KEY_VALUE: -f configuration.properties -k packages.xxx-app -v {xxx-app}
    # Example of update a xml file tag text
    - SET_XML_TAG_TEXT: -f file.xml -x xpath -v value
    # Example of tail a file content
    - TAIL_FILE: -f X:\dev\\build.log -l 100
    # Write a line in a file
    - WRITE_LINE_IN_FILE: -f xxx.txt -n line-nubmer -v content 
    # Count txt file line number or tube command numbers by status
    - COUNT: -t FAILED -v failed_count    
    # Set a tube variable value
    - SET_VARIABLE: -n var1 -v Hello Tube     
    # Get a Linux file to local
    - SFTP_GET: -r remotefile -l localfile
    # Put a local file to Linux
    - SFTP_PUT: -l localfile -r remotefile   
    # Check if given characters exists from a given file
    - CHECK_CHAR_EXISTS: -f file -c hello -r hello_exists
    # Replace file lines which contains given characters.
    - REPLACE_CHAR: -f file -o oldvalue -n newvalue -c 1
                '''
                examples = '''
## Tube File Samples 
### For samples tube file, please check templates folder.
<pre>
    Sample-refresh-dev.yaml
    Sample-conditional-build.yaml
</pre>
                '''
                command_name = ''
                command_arg = ''
                # get the second argument value
                if len(args.args) >= 2:
                    command_name = args.args[1]
                if len(args.args) >= 3:
                    command_arg = args.args[2]
                
                # check if help readme
                is_for_readme = False
                if command_name and command_name.upper() == 'README':
                    is_for_readme = True
                    
                # Prepare examples of each command
                command_examples = []
                command_examples.append('## Usage of Each Command:')
                keys = [k for k in Storage.I.TUBE_ARGS_CONFIG.keys()]
                keys.sort()                
                for index, key in enumerate(keys):
                    if is_for_readme:
                        command_examples.append('### %s: %s' % (str(index+1), key))
                        command_examples.append('#### %s' % TubeCommand.get_command_alias(key, Storage.I.TUBE_ARGS_CONFIG))
                        command_examples.append('<pre>%s\n' % TubeCommand.get_command_description(key, Storage.I.TUBE_ARGS_CONFIG)) 
                    else:
                        command_examples.append('[%s]: %s' % (str(index+1), key))                        
                        command_examples.append(TubeCommand.get_command_alias(key, Storage.I.TUBE_ARGS_CONFIG))                      
                        command_examples.append('%s\n' % TubeCommand.get_command_description(key, Storage.I.TUBE_ARGS_CONFIG)) 
                    
                    command_examples.append('%s' % TubeCommand.get_command_syntax(key, Storage.I.TUBE_ARGS_CONFIG)) 
                    command_examples.append('%s' % TubeCommand.get_command_parameters(key, Storage.I.TUBE_ARGS_CONFIG))
                    
                    if command_name == '' or command_name.upper() != 'README':
                        command_examples.append('[Support from version: %s]' % Storage.I.TUBE_ARGS_CONFIG[key][Storage.I.C_SUPPORT_FROM_VERSION])
                        command_examples.append(Storage.I.C_STATUS_LINE + Storage.I.C_STATUS_LINE)
                    else:
                        command_examples.append('Support from version: %s</pre>' % Storage.I.TUBE_ARGS_CONFIG[key][Storage.I.C_SUPPORT_FROM_VERSION])                    
                        
                # End of prepare examples of each command 
                if command_name == '' or command_name.upper() == 'ALL':
                    # print all help
                    tprint(help_all ,prefix='')
                    for eg in command_examples:
                        tprint(eg ,prefix='')  
                    tprint(add_notes ,prefix='')                         
                    sys.exit()
                elif command_name.upper() == 'COMMANDS':
                    for eg in command_examples:
                        if command_arg and command_arg == 'name':
                            if (not eg.startswith('[')) or eg.startswith('[Supp'):
                                continue
                        tprint(eg, prefix='')
                    sys.exit()
                elif command_name.upper() == 'TEMPLATE':
                    # print template and write it to a file
                    found_match = True
                    try:    
                        file = 'tube.template.yaml'
                        with open(file, 'w') as f:
                            f.write(template)
                        tprint(template,prefix='')
                        tprint('# ' + file + ' is generated.',prefix='')
                    except Exception as e:
                        tprint('Generated template exception: ' + str(e), type=Storage.I.C_PRINT_TYPE_ERROR) 
                elif command_name.upper() == 'HELP':
                    # write help to help.txt file
                    found_match = True
                    try:
                        file = 'help.txt'
                        with open(file, 'w') as f:
                            f.write(help_all + '\n')
                            for eg in command_examples:
                                f.write(eg + '\n')
                            f.write(add_notes)
                        tprint(file + ' is generated.' ,prefix='')
                    except Exception as e:
                        tprint('Generated readme exception: ' + str(e), type=Storage.I.C_PRINT_TYPE_ERROR) 
                elif command_name.upper() == 'VARS':
                    # print all tube variables
                    found_match = True
                    if not args.yaml_config:
                        tprint('-t/--tube aragument is not passed.', type=Storage.I.C_PRINT_TYPE_WARNING)
                        sys.exit()
                    yaml_file = args.yaml_config
                    exists, yaml_file = Utility.check_file_exists(yaml_file, '.yaml', '.yml')
                    if exists == False:
                        tprint('YAML file doesnot exists: ' + yaml_file, type=Storage.I.C_PRINT_TYPE_WARNING)
                        sys.exit()
                    # begin to read yaml file variables
                    try:
                        with open(yaml_file, 'r') as f:
                            lines = f.readlines()
                            var_start = False                            
                            for line in lines:
                                if line.upper().startswith(Storage.I.C_VARIABLES):    
                                    var_start = True
                                    continue
                                if var_start == True and line.startswith(' '):
                                    # skip comment out lines
                                    if line.strip().startswith('#'):
                                        continue
                                    # inorder to print var name/value in different color
                                    if ':' in line:
                                        line = line.strip().replace('\n', '')
                                        i = line.index(':')
                                        var_name = line[:i+1]
                                        var_value = line[i+1:]
                                        tprint(color(var_name, fore=Storage.I.C_PRINT_COLOR_BLUE, style=Storage.I.C_PRINT_COLOR_STYLE) + var_value, prefix='')
                                    continue
                                elif var_start == True and not line.startswith(' '):
                                    break
                                                     
                        sys.exit()
                    except Exception as e:
                        tprint('Read variables from yaml file errors:' + str(e), type=Storage.I.C_PRINT_TYPE_ERROR)
                        sys.exit()
                elif command_name.upper() == 'CONTINUE':
                    print(help_continue.replace('\n', '', 1))
                    sys.exit()
                elif command_name.upper() == 'REDO':
                    print(help_redo.replace('\n','',1))
                    sys.exit()
                elif command_name.upper() == 'IF':
                    print(help_if.replace('\n', '', 1))
                    sys.exit()
                elif command_name.upper() == 'KEY':
                    print(help_key.replace('\n', '', 1))
                    sys.exit()
                elif command_name.upper() == 'RAW':
                    print(help_raw.replace('\n', '', 1))
                    sys.exit()
                elif command_name.upper() == 'NOTE':
                    print(help_note.replace('\n', '', 1))
                    sys.exit()
                elif command_name.upper() == 'VARIABLE':
                    print(help_var.replace('\n', '', 1))
                    sys.exit()
                elif command_name.upper() == 'README':
                    with open('README.md', 'w') as f:
                        f.write(help_all + '\n')
                        for eg in command_examples:
                            f.write(eg + '\n')
                        # sampels tube file
                        f.write(examples)
                    sys.exit()
                else:     
                    # checking if could find matched commands             
                    index = 0
                    for _, key in enumerate(keys):
                        alias = [a for a in Storage.I.TUBE_ARGS_CONFIG[key][Storage.I.C_ALIAS] if command_name.upper() in a]
                        if command_name.upper() in key or len(alias) > 0:
                            found_match = True        
                            index += 1       
                            tprint('[%s]: %s' % (str(index),key), tcolor=Storage.I.C_PRINT_COLOR_YELLOW ,prefix='')
                            tprint(TubeCommand.get_command_alias(key, Storage.I.TUBE_ARGS_CONFIG) + '' ,prefix='')
                            if not command_arg or command_arg.lower() == 'desc':
                                tprint(TubeCommand.get_command_description(key, Storage.I.TUBE_ARGS_CONFIG) + '\n' ,prefix='')
                            if not command_arg or command_arg.lower() == 'syntax':
                                tprint(TubeCommand.get_command_syntax(key, Storage.I.TUBE_ARGS_CONFIG) ,prefix='')
                            if not command_arg or command_arg.lower() == 'parameters':                   
                                tprint(TubeCommand.get_command_parameters(key, Storage.I.TUBE_ARGS_CONFIG) ,prefix='')
                            if not command_arg or command_arg.lower() == 'support':
                                tprint('[Support from version: %s]' % Storage.I.TUBE_ARGS_CONFIG[key][Storage.I.C_SUPPORT_FROM_VERSION] ,prefix='')                            
                            if not command_arg:
                                tprint(Storage.I.C_STATUS_LINE ,prefix='')
                    if found_match == True and not command_arg:
                        tprint(add_notes ,prefix='')
                # found nothing match from help system
                # then raise error
                if found_match == False:                    
                    tprint('The argument: \'%s\' doesnot found matched.' % (command_name), type=Storage.I.C_PRINT_TYPE_WARNING)
                    tprint(Storage.I.C_HELP ,prefix='')
                    
                sys.exit()

            elif(len(args.args) == 1):
                exists, yaml_file = Utility.check_file_exists(args.args[0], '.yaml', '.yml')
                if exists:
                    found_match = True
                    args.yaml_config = args.args[0]
            
            # check positional argument result
            if not found_match:
                # return if positional argument not matched
                tprint(Storage.I.C_HELP ,prefix='')
                tprint('You entered value for position arguments: ' + str(args.args), tcolor=Storage.I.C_PRINT_COLOR_YELLOW)
                sys.exit()

    except argparse.ArgumentError as e:    
        tprint(str(e), type=Storage.I.C_PRINT_TYPE_ERROR)
        sys.exit()        
    except Exception as e:
        tprint(str(e), type=Storage.I.C_PRINT_TYPE_ERROR)
        sys.exit()        
    except SystemExit:
        sys.exit()

def read_run_mode():
    try:
        if Storage.I.TUBE_YAML_FILE and path.exists(Storage.I.TUBE_YAML_FILE):
            with open(Storage.I.TUBE_YAML_FILE, 'r') as f:
                for line in f:
                    line = line.replace('\n', '').strip()
                    if line.startswith(Storage.I.C_RUN_MODE):
                        start = line.index(':')
                        value = line[start+1:].strip()
                        if value == Storage.I.C_RUN_MODE_BIN:
                            Storage.I.RUN_MODE = value
                        elif value == Storage.I.C_RUN_MODE_DEBUG:
                            Storage.I.RUN_MODE = value
                        break
                                                                    
    except Exception as e:
        msg = 'READ RUN_MODE EXCEPTION: %s' % (str(e))
        tprint(msg, type=Storage.I.C_PRINT_TYPE_ERROR)
        write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)  

def start_matrix_terminal():  
    '''
    This method only run when --matrix-mode flag is set to true
    '''
    
    Storage.I.IS_MATRIX_MODE_RUNNING = True
    Storage.I.MATRIX_THREAD = MatrixThread()
    Storage.I.MATRIX_THREAD.start()    

def stop_matrix_terminal():
    '''
    This method only run when --matrix-mode flag is set to true
    '''
    Storage.I.IS_MATRIX_MODE_RUNNING = False
    Storage.I.MATRIX_THREAD.stop()
    Storage.I.MATRIX_THREAD.join()
    Storage.I.MATRIX_THREAD = None

def get_console_inputs():    

    # if debug
    if args.debug != None:
        Storage.I.RUN_MODE = Storage.I.C_RUN_MODE_DEBUG
    # if clear log
    if args.clear_log:
        Storage.I.IS_CLEAR_LOG = True

    # datetime
    if(args.datetime != None):
        pattern1 = '[nN]((\d+(\.\d*)?)|(\.\d+))$'  # match 'n7' as one example, means next 7 o'clock
        pattern2 = '[tT]((\d+(\.\d*)?)|(\.\d+))$'  # match 't7' as one example, means this 7 o'clock
        if re.match(pattern1, args.datetime):
            hours = float(args.datetime.replace('n','').replace('N',''))
            today = date.today() 
            future_datetime = datetime.strptime(str(today.month) + '/' + str(today.day) + '/' + str(today.year) + ' 00:00:00', '%m/%d/%Y %H:%M:%S')
            Storage.I.EXEC_DATETIME = future_datetime + timedelta(days=1, hours=hours)
        elif re.match(pattern2, args.datetime):
            hours = float(args.datetime.replace('t','').replace('T',''))
            today = date.today() 
            future_datetime = datetime.strptime(str(today.month) + '/' + str(today.day) + '/' + str(today.year) + ' 00:00:00', '%m/%d/%Y %H:%M:%S')
            Storage.I.EXEC_DATETIME = future_datetime + timedelta(days=0, hours=hours)
        else:        
            Storage.I.EXEC_DATETIME = datetime.strptime(args.datetime, '%m/%d/%y %H:%M:%S')
    else:
        Storage.I.EXEC_DATETIME = datetime.strptime(Storage.I.EXEC_DATE_TIME, '%m/%d/%y %H:%M:%S') 

    # if run in immediate mode
    if(args.immediate != None and (args.immediate.lower() == 'true' or args.immediate.lower() == 'yes' or 
    args.immediate.lower() == 'y' or args.immediate.lower() == 't')):
        Storage.I.IS_IMMEDIATE = True 

    # if sent email
    if(args.email != None and (args.email.lower() == 'true' or args.email.lower() == 'yes' or args.email.lower() == 'y' or args.email.lower() == 't')):
        Storage.I.IS_SENT_EMAIL = True  

    # if loop
    if(args.period_of_next_run != None):
        Storage.I.IS_LOOP      = True
        period = args.period_of_next_run.strip()        
        period_in_hours = 0
        if period.upper().endswith('M'):
            period_in_hour = float(period[:-1]) / 60.0
        elif period.upper().endswith('H'):
            period_in_hour = float(period[:-1])
        elif period.upper().endswith('D'):
            period_in_hour = float(period[:-1]) * 24.0
        else:
            period_in_hour = float(period)            
        Storage.I.NEXT_REFRESH = period_in_hour
    
    # iteration times
    if(args.run_times != None):
        Storage.I.LOOP_TIMES = args.run_times

    # if run force
    if(args.force != None and (args.force.lower() == 'true' or args.force.lower() == 'yes' or args.force.lower() == 'y' or args.force.lower() == 't')):
        Storage.I.IS_FORCE_RUN = True
        Storage.I.IS_IMMEDIATE = True
    
    # matrix mode
    if(args.matrix_mode != None and args.matrix_mode == 'yes'):
        Storage.I.IS_MATRIX_MODE = True
    
    # report progress
    if(args.report_progress != None and args.report_progress == 'yes'):
        Storage.I.IS_REPORT_PROGRESS = True

def job_start():
    
    '''
    Start the Command-Tube job
    '''

    try:
        # print job start initials into the log
        init_log_file()

        # Instance a new TubeRunner and ask it to run the tube
        runner = TubeRunner(is_main=True, run_tube_command=None, tube=Storage.I.TUBE)
        runner.start()
                   
    except Exception as e:
        msg = 'Exceptions found within job_start: ' + str(e)
        tprint(msg, type=Storage.I.C_PRINT_TYPE_ERROR)  
        write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)        
    finally:
        try:
            os.chdir(Storage.I.C_CURR_DIR) # changing dir back if 'PATH' command changed current dir
        except Exception as e:
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', str(e)) 

        # close all connections         
        disconect_all_hosts(Storage.I.HOSTS)     
        Host.SSHConnection = None  
# --------- END OF FUNCTIONS -----------------

# to check main flow
if __name__ != '__main__':
    sys.exit()

# Pyinstaller fix
multiprocessing.freeze_support()

# global instance to store any user inputs, outputs or variables
_ = Storage()  
# reset default print colors
# this is the only place to update constants
StorageUtility.reset_colors()
parser = ArgumentParser(allow_abbrev=False, formatter_class=RawTextHelpFormatter, description=__doc__)    
general_command_parser = ArgumentParser(allow_abbrev=False)   

# init Command-Tube arguments and help document
init_arguments()   

# parse user inputs arguments from console
args = None
try:
    args = parser.parse_args()
    get_console_inputs()
    
except Exception as e:
    # Log start
    write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', Storage.I.C_LOG_HEADER + datetime.now().strftime(Storage.I.C_DATETIME_FORMAT))
    write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', 'Command Tube parameters error:' + str(e))
    sys.exit()

# -------------------------------
# Install & Import 3rd-party Packages
# -------------------------------
install_3rd_party_packages(args)  
# Import 3rd-party packages
import paramiko 
from colr import color
from bs4 import BeautifulSoup
import requests
import yaml 

# check help document system
print_tube_command_help(args)

# ------------------------------------------------------------
# check input yaml/yml tube file
# if yaml file exists then reset log file name to xxx.yaml.log
# ------------------------------------------------------------ 
if(args.yaml_config != None):
    # if the config file name without extensions
    # then add '.yaml' or '.yml' ad default and
    # check if they exists
    yaml_file = args.yaml_config
    exists, yaml_file = Utility.check_file_exists(yaml_file, '.yaml', '.yml')       
    Storage.I.TUBE_YAML_FILE = yaml_file
    if(exists == True):
        if args.log_file == None:
            Storage.I.TUBE_LOG_FILE = os.path.join(Storage.I.C_CURR_DIR, Storage.I.TUBE_YAML_FILE + '.log')
        else:
            exists_log, log_file = Utility.check_file_exists(args.log_file[0])
            if exists_log:
                Storage.I.TUBE_LOG_FILE = os.path.abspath(args.log_file[0])
            else:
                Storage.I.TUBE_LOG_FILE = os.path.join(Storage.I.C_CURR_DIR, args.log_file[0])
        # read run mode file yaml file
        if Storage.I.RUN_MODE != Storage.I.C_RUN_MODE_DEBUG:
            read_run_mode()
    else:
        msg = "YAML file doesn't exist: " + Storage.I.TUBE_YAML_FILE
        tprint(msg, type=Storage.I.C_PRINT_TYPE_ERROR)
        # Log start
        write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', Storage.I.C_LOG_HEADER + datetime.now().strftime(Storage.I.C_DATETIME_FORMAT))
        write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
        sys.exit()         
else:
    msg = '-t or --tube parameter is missing. \
          \nUse \'-h\' argument to view the usage of all the parameters.'
    tprint(msg, type=Storage.I.C_PRINT_TYPE_ERROR)
    # Log start
    write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', Storage.I.C_LOG_HEADER + datetime.now().strftime(Storage.I.C_DATETIME_FORMAT))
    write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
    sys.exit()  
# --------End of Check Log Files -----------------------------

# -------------------------------------------------------
# Read tube file settings: TUBE, Email, Server, Variables
# Yaml version, and check tube commands syntax
# -------------------------------------------------------
try:
    data = None
    if(Storage.I.TUBE_YAML_FILE and path.exists(Storage.I.TUBE_YAML_FILE)):
        with open(Storage.I.TUBE_YAML_FILE, 'r') as f:
            data = Utility.safe_load_yaml_with_upper_key(f) 
    
    # check if given configuration file is empty        
    if not data:
        msg = 'The content of given config file is empty: %s'
        msg = msg % Storage.I.TUBE_YAML_FILE
        tprint(msg, type=Storage.I.C_PRINT_TYPE_ERROR)
        write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
        sys.exit()

    # tprint(json.dumps(data, indent=4))   
    if Storage.I.C_TUBE in data.keys(): 
        Storage.I.TUBE_YAML = data[Storage.I.C_TUBE]
        Storage.I.TUBE_NAME = Storage.I.C_TUBE
    elif Storage.I.C_TUBE.lower() in data.keys():
        Storage.I.TUBE_YAML = data[Storage.I.C_TUBE.lower()]
        Storage.I.TUBE_NAME = Storage.I.C_TUBE.lower()
    elif Storage.I.C_TUBE.title() in data.keys():
        Storage.I.TUBE_YAML = data[Storage.I.C_TUBE.title()]
        Storage.I.TUBE_NAME = Storage.I.C_TUBE.title()
    else:
        raise Exception('\'TUBE\', \'Tube\' or \'tube\' key does not exist from your main YAML file: {0}'.format(Storage.I.TUBE_YAML_FILE))
    # Emails
    if Storage.I.C_EMAIL in data.keys():        
        StorageUtility.read_emails(data[Storage.I.C_EMAIL])   
    # Servers
    if(Storage.I.C_SERVERS in data.keys()):
        Storage.I.SERVERS = data[Storage.I.C_SERVERS]
    # Variables
    if(Storage.I.C_VARIABLES in data.keys()):
        Storage.I.VARIABLES = data[Storage.I.C_VARIABLES]
    # YAML Version
    if Storage.I.C_YAML_VERSION in data.keys():
        Storage.I.YAML_VERSION = data[Storage.I.C_YAML_VERSION]        
    del data
    
    # log job header
    output_log_header()
    
    # log user inputs from console
    output_user_console_inputs()
        
    # Get servers to hosts
    StorageUtility.read_hosts(Storage.I.SERVERS)

    # Instance a new tube
    tube = Tube(Storage.I.TUBE_YAML_FILE, Storage.I.TUBE_NAME, 0, Storage.I.TUBE_YAML, None)

    # Read variables from console
    StorageUtility.read_variables_from_console(args.variables, tube)
    # add default variables
    StorageUtility.add_default_variables(tube)

    # generate the eval code set
    Utility.gen_eval_code_set()
    
    # Read variables 
    StorageUtility.read_variables(Storage.I.VARIABLES, tube)
        
    # checking tube command syntax
    Storage.I.TUBE = tube
    Storage.I.TUBE_RUN = tube.tube_run
    has_error, _ = StorageUtility.check_tube_command_arguments(tube.tube_run, general_command_parser)
    if has_error == True:
        msg = 'Tube has syntax errors, please double check.'
        tprint(msg, type=Storage.I.C_PRINT_TYPE_WARNING)
        write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
        sys.exit()
        
    # checking YAML versions
    # if command tube major/minor version is different
    # with YAML file version then raised a warning to the end user.
    yaml_ver = TubeVersion(Storage.I.YAML_VERSION)
    program_ver = TubeVersion(Storage.I.C_CURR_VERSION)
    if yaml_ver.major_version > 0 and \
       (yaml_ver.major_version != program_ver.major_version or \
       yaml_ver.minor_version != program_ver.minor_version):
        msg = 'Command Tube major/minor versions are different with YAML file version.'
        tprint(msg, type=Storage.I.C_PRINT_TYPE_WARNING)
        write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
    
except Exception as e:
    msg = str(e)
    tprint(msg, type=Storage.I.C_PRINT_TYPE_ERROR)
    write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
    sys.exit()
# ----- END Of Reading Configuration --------- 

# ----- Prepare to start the real job ------
# Print input parameters and ask user to confirm
if not Storage.I.IS_FORCE_RUN:
    print_input_parameters()

if not confirm('Are those parameters correct [Y/N]? '):
    msg = 'user quit.'
    write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
    sys.exit() 

# ----- Validations on running time  ------
# do a check on the user input datetime
# the job start datetime must be bigger than current
if(Storage.I.IS_IMMEDIATE == False and datetime.now() > Storage.I.EXEC_DATETIME):
    tprint('Please provide a future datetime to do the job, you provided: ' + str(Storage.I.EXEC_DATETIME), type=Storage.I.C_PRINT_TYPE_WARNING)
    sys.exit()
# ----------------------------------------        

#-----------------------------------------------
# Main job starting logic starts from here
#-----------------------------------------------
while Storage.I.IS_STOP == False:
    # get current datetime
    now = datetime.now()
    # If run time is less than current time and not in immediate/force mode
    # update how much time left to start
    if(now < Storage.I.EXEC_DATETIME and Storage.I.IS_IMMEDIATE == False):
        datetime_togo = Utility.get_datetime_difference(Storage.I.EXEC_DATETIME, now)
        space_to_override = ''
        if Storage.I.IS_LOOP:
            duration = Storage.I.NEXT_REFRESH
            unit = 'HOURS'
            duration, unit = Utility.format_duration_unit(duration, unit)
            space_to_override = ' [LOOP(%s/%s): EVERY %.1f %s]' % (str(Storage.I.CURR_LOOP_ID), str(Storage.I.LOOP_TIMES), duration, unit)
        space_to_override += '          ' # 10 spaces            
        print(color('\rWARNING: Tube will start after '.upper() +  datetime_togo + space_to_override, fore='yellow', style=Storage.I.C_PRINT_COLOR_STYLE), end = '\r')
        time.sleep(Storage.I.C_SLEEP_SECONDS)
    # if run time is greater than current time 
    # or in immediate/force mode
    else:
        # Start doing the job for one iteration
        if Storage.I.IS_LOOP == False:
            Storage.I.IS_STOP = True
        else:
            # In loop mode    
            # clear memories                           
            Storage.I.LOGS.clear() 
            Storage.I.DISK_SPACE_STATUS = {}
            Storage.I.TUBE_FILE_LIST = {}
            # calculate loop times
            # check if current loop times equal than max
            Storage.I.CURR_LOOP_ID += 1
            if Storage.I.CURR_LOOP_ID == Storage.I.LOOP_TIMES:
                Storage.I.IS_STOP = True
        
        # check matrix mode and start it
        if Storage.I.IS_MATRIX_MODE:
            start_matrix_terminal()
        
        # start the job
        job_start() 
        
        # stop matrix mode if it's started
        if Storage.I.IS_MATRIX_MODE:
            stop_matrix_terminal()
            
        print_logs(Storage.I.LOGS)
        write_logs_to_file(Storage.I.LOGS)        
        if Storage.I.IS_SENT_EMAIL:
            prepare_emails_content_and_sent(Storage.I.LOGS)
        output_disk_space_check()
        
        # In loop mode, we need to update the next run time
        # do this time updates just on each iteration is fully done
        if Storage.I.IS_LOOP == True:
            Storage.I.EXEC_DATETIME += timedelta(hours=Storage.I.NEXT_REFRESH)       
#--------End of the LOOP ----------------------- 