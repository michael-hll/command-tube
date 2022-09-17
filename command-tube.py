# -*- coding: utf-8 -*-
#!/usr/bin/python

# -------------------------
# Command Tube
# GitHub: https://github.com/michael-hll/command-tube
# Email: michael_hll@hotmail.com
# Author: Michael Han
# Date: May 1, 2022
# Copyright 2022 
# -------------------------

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

# -------- CLASSES --------------
class Utility():
    
    @classmethod
    def check_file_exists(self, file, *exts):
        '''
        *exts: if file doesn't exist than check if file+ext exits
        
        Return (exists, file)
        '''
        f = file
        # exists
        if path.exists(f) and not path.isdir(f):
            return (True, f)
        if path.exists(f) and path.isdir(f):
            # then try exts
            for ext in exts:
                if path.exists(f + ext) and not path.isdir(f + ext):
                    return(True, f + ext)
        # not exists
        if not path.exists(f):
            for ext in exts:
                if path.exists(f + ext) and not path.isdir(f + ext):
                    return(True, f + ext)        
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
    def safe_load_with_upper_key(self, f):
        data = yaml.safe_load(f)
        Utility.make_dict_key_upper(data)
        return data    
    
    @classmethod
    def make_dict_key_upper(self, yaml):
        if not yaml or type(yaml) is not dict:
            return
        
        deleted_keys = []
        
        # make the key upper cases
        keys = [k for k in yaml.keys()]
        for key in keys:
            if key != key.upper():
                yaml[key.upper()] = yaml[key]
                deleted_keys.append(key)
        
        # deleted not upper case key/value
        for key in deleted_keys:
            del yaml[key]   
            
class Storage():
    I = None
    def __init__(self) -> None:
        Storage.I = self     
        # -------- CONSTANTS START --------
        self.C_CURR_VERSION            = '2.0.2 Beta'  
        self.C_SUPPORT_FROM_VERSION    = 'SUPPORT_FROM_VERSION'     
        self.C_YAML_VERSION            = 'VERSION'        
        self.C_DATETIME_FORMAT         = '%Y-%m-%d %H:%M:%S'
        self.C_CURR_DIR                = os.getcwd()   
        self.C_TUBE_HOME               = 'TUBE_HOME' 
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
        self.C_GET_FILE_KEY_VALUE       = 'GET_FILE_KEY_VALUE'
        self.C_IMPORT_TUBE             = 'IMPORT_TUBE'
        self.C_EMAIL                   = 'EMAIL'
        self.C_COUNT                   = 'COUNT'
        self.C_SET_VARIABLE            = 'SET_VARIABLE'
        self.C_SFTP_GET                = 'SFTP_GET'
        self.C_SFTP_PUT                = 'SFTP_PUT'
        self.C_CHECK_CHAR_EXISTS       = 'CHECK_CHAR_EXISTS'  
        self.C_REPLACE_CHAR            = 'REPLACE_CHAR'
        self.C_PRINT_VARIABLES         = 'PRINT_VARS'
        self.C_TAIL_LINES_HEADER       = '\nTAIL '
        self.C_LOG_HEADER              = '\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\nCommand Tube Log starts at '
        self.C_JOB_HEADER              = '\n--------------------------------------\nJob starts at '
        self.C_FINISHED_HEADER         = '*** Command Tube Finished Status ***'
        self.C_CONTINUE_PARAMETER      = '--continue'
        self.C_REDO_PARAMETER          = '--redo'
        self.C_IF_PARAMETER            = '--if'
        self.C_KEY_PARAMETER           = '--key'
        self.C_INDENTATION             = '    '
        self.C_ANT_DEPLOY_LOG_FILE     = 'build.log'
        self.C_ANT_DEPLOY_ERROR        = 'BUILD FAILED'
        self.C_RETRIED_COMMAND_NOTE    = '* The star(*) before command type means the command is run again.'
        self.C_FAILED_COMMAND_LIST     = '----- Failed Command List -----'
        self.C_HELP                    = '''Use 'help' command to view the whole help document;
Use 'help commands' to print all commands usages;
Use 'help command-name' to print all the tube commands usage which name matched.
Use 'help continue' to view the --continue syntax;
Use 'help if' to view the --if syntax;
use 'help key' to view the --key syntax;
Use 'help redo' to view the --redo syntax;
Use 'help template' to view the tube tempalte;
Use 'help variable' to view the tube variables usage;
Use 'help vars' to print all the given tube variables;
        '''
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
        self.TUBE                      = None
        self.TUBE_YAML_FILE            = None
        self.TUBE_LOG_FILE             = 'tube.log'
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
        self.FILE_TAIL_LINES           = []
        self.KEY_VALUES_DICT           = {}
        self.KEYS_READONLY_SET          = set() # to store tube variables which are readonly
        self.DISK_SPACE_STATUS         = {} 
        self.INSTALLED_PACKAGES        = []
        self.TUBE_RUN                  = [] 
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
            self.C_IMPORT_TUBE: {
                self.C_SUPPORT_FROM_VERSION: '2.0.0',
                self.C_ARG_SYNTAX: 'Syntax: IMPORT_TUBE: file [--continue [m][n]] [--redo [m]] [--if run] [--key]',
                self.C_ARG_ARGS: [        
                    [True, '-','--', 'str', '+', 'file', True, False, '', '',
                        'Sub tube file with YAML format.'],
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Import tube commands from a sub-tube file, servers, variables or emails can also be imported.'
            },                     
            self.C_TAIL_FILE: {
                self.C_SUPPORT_FROM_VERSION: '2.0.0',
                self.C_ARG_SYNTAX: 'Syntax: TAIL_FILE: -f file -l lines [-k keywords] [--continue [m][n]] [--redo [m]] [--if run] [--key]',
                self.C_ARG_ARGS: [        
                    [False, '-f','--file', 'str', '+', 'file', True, False, '', '',
                        'The text file you want to tail.'],
                    [False, '-l','--lines', 'str', 1, 'lines', True, False, '', '',
                        'The lines count you want to output.'],
                    [False, '-k','--keywords', 'str', '*', 'keywords', False, False, '', '',
                        'Output file content only if it contains the given keywords.'],                    
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Print/Log the last N lines of given file.'                
            },
            self.C_DELETE_LINE_IN_FILE: {
                self.C_SUPPORT_FROM_VERSION: '2.0.0',
                self.C_ARG_SYNTAX: 'Syntax: DELETE_LINE_IN_FILE: -f file [-b begins] [-c contains] [-e] [--continue [m][n]] [--redo [m]] [--if run] [--key]',
                self.C_ARG_ARGS: [        
                    [False, '-f','--file', 'str', '+', 'file', True, False, '', '',
                        'The file you want to delete lines from.'],
                    [False, '-b','--begins', 'str', '+', 'begins', False, False, '', '',
                        'The line begins with character you want to delete.'],
                    [False, '-c','--contains', 'str', '+', 'contains', False, False, '', '',
                        'The line contains with character you want to delete.'],
                    [False, '-e','--empty', '', '', 'del_empty', False, True, 'store_true', False,
                        'A flag to tell if delete empty line. Default no.'],
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Conditionally delete lines from a file.'
            },  
            self.C_WRITE_LINE_IN_FILE: {
                self.C_SUPPORT_FROM_VERSION: '2.0.0',
                self.C_ARG_SYNTAX: 'Syntax: WRITE_LINE_IN_FILE: -f file [-n line-number] [-c contains] -v value | $file [--continue [m][n]] [--redo [m]] [--if run] [--key]',
                self.C_ARG_ARGS: [        
                    [False, '-f','--file', 'str', '+', 'file', True, False, '', '',
                        'The file you want to update.'],
                    [False, '-v','--value', 'str', '+', 'value', True, False, '', '',
                        'The character value you want to update in the file.'],
                    [False, '-n','--number', 'str', 1, 'number', False, False, '', '',
                        'The line number you want to update.'],                    
                    [False, '-c','--contains', 'str', '+', 'contains', False, False, '', '',
                        'Only update the line if it contains the given characters content.'],
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Write any characters into a file.  \
                    \nThe written characters also could be one of them: \'$NLB\' (NEW_LINE_BEFORE), \'$NLA\' (NEW_LINE_AFTER),\'$DL\' (DELETE_LINE). \
                    \nIf you need more than two space characters in the value content, you can use {s:m} (m > 0) formular. \
                    \nThe \'m\' means how many spaces you want to write. \
                    \neg: -v {s:5}hello => will be translated to 5 space chars plus hello: \'     hello\''                    
            },    
            self.C_SET_FILE_KEY_VALUE: {
                self.C_SUPPORT_FROM_VERSION: '2.0.0',
                self.C_ARG_SYNTAX: 'Syntax: SET_FILE_KEY_VALUE: -f file -k key -v value [--continue [m][n]] [--redo [m]] [--if run] [--key]',
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
                self.C_COMMAND_DESCRIPTION: 'Update key-value file.'
            },
            self.C_GET_XML_TAG_TEXT: {
                self.C_SUPPORT_FROM_VERSION: '2.0.0',
                self.C_ARG_SYNTAX: 'Syntax: GET_XML_TAG_TEXT: -f file -x xpath [--continue [m][n]] [--redo [m]] [--if run] [--key]',
                self.C_ARG_ARGS: [        
                    [False, '-f','--file', 'str', '+', 'file', True, False, '', '',
                        'The XML file you want to get tag text.'],
                    [False, '-x','--xpath', 'str', '+', 'xpath', True, False, '', '',
                        'The xpath of the XML tag.'],
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Get XML file tag text value. \
                                           \nThe result will be stored into a tube variable and xpath will be used as the variable name.'
            },
            self.C_SET_XML_TAG_TEXT: {
                self.C_SUPPORT_FROM_VERSION: '2.0.0',
                self.C_ARG_SYNTAX: 'Syntax: SET_XML_TAG_TEXT: -f file -x xpath -v value [--continue [m][n]] [--redo [m]] [--if run] [--key]',
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
                self.C_COMMAND_DESCRIPTION: 'Update XML file tag text using xpath.'
            },
            self.C_SET_VARIABLE: {
                self.C_SUPPORT_FROM_VERSION: '2.0.0',
                self.C_ARG_SYNTAX: 'Syntax: SET_VARIABLE: -n name -v value [--continue [m][n]] [--redo [m]] [--if run] [--key]',
                self.C_ARG_ARGS: [        
                    [False, '-n','--name', 'str', '+', 'name', True, False, '', '',
                        'The tube variable name you want to set.'],
                    [False, '-v','--value', 'str', '*', 'value', True, False, '', '',
                        'The tube variable value you want to set. \n  \
                Note: The \'eval(expression)\' is also supported, eg: \n \
                    - SET_VARIABLE: -n dayOfWeek -v eval(datetime.today().weekday()) # Tube variable dayOfWeek will be set to weekday() value. \n \
                    - SET_VARIABLE: -n sum -v eval({var1}+{var2}) # Tube variable sum will be set to the result of var1 + var2.'],
                    [False, '-r','--readonly', '', '', 'is_readonly', False, True, 'store_true', False,
                        'Mark the variable as readonly after updating. Default no. [2.0.2]'],
                    [False, '-f','--force', '', '', 'is_force', False, True, 'store_true', False,
                        'Force update even the varialbe is readonly. Default no. [2.0.2]'],
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Set tube variable value.'
            },
            self.C_CONNECT: {
                self.C_SUPPORT_FROM_VERSION: '2.0.0',
                self.C_ARG_SYNTAX: 'Syntax: CONNECT: xxx.xxx.com [--continue [m][n]] [--redo[m]] [--if run] [--key]',
                self.C_ARG_ARGS: [        
                    [True, '-','--', 'str', '+', 'host', True, False, '', '',
                        'The Linux server host or name you want to connect using SSH protocal.'],
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'You can use this command to switch your server connection.'
            },
            self.C_REPORT_PROGRESS: {
                self.C_SUPPORT_FROM_VERSION: '2.0.0',
                self.C_ARG_SYNTAX: 'Syntax: REPORT_PROGRESS: subject [--continue [m][n]] [--redo [m]] [--if run] [--key]',
                self.C_ARG_ARGS: [        
                    [True, '-','--', 'str', '+', 'subject', True, False, '', '',
                        'The email subject/title you want to set.'],
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'You can use this command to sent current progress via Email.'
            },
            self.C_PAUSE: {
                self.C_SUPPORT_FROM_VERSION: '2.0.0',
                self.C_ARG_SYNTAX: 'Syntax: PAUSE: minutes [--continue [m][n]] [--redo [m]] [--if run] [--key]',
                self.C_ARG_ARGS: [        
                    [True, '-','--', 'str', '+', 'minutes', True, False, '', '',
                        'The minutes you want to pause.'],
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Command Tube will pause with given minutes.'
            },
            self.C_PATH: {
                self.C_SUPPORT_FROM_VERSION: '2.0.0',
                self.C_ARG_SYNTAX: 'Syntax: PATH: directory [--continue [m][n]] [--redo [m]] [--if run] [--key]',
                self.C_ARG_ARGS: [        
                    [True, '-','--', 'str', '+', 'directory', True, False, '', '',
                        'The directory you want to goto.'],
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Go to specific directory.'
            },
            self.C_GET_FILE_KEY_VALUE: {
                self.C_SUPPORT_FROM_VERSION: '2.0.0',
                self.C_ARG_SYNTAX: 'Syntax: GET_FILE_KEY_VALUE: -f file [-k key[,key][...]] [--continue [m][n]] [--redo [m]] [--if run] [--key]',
                self.C_ARG_ARGS: [    
                    [False, '-f','--file', 'str', '+', 'file', True, False, '', '',
                        'The file you want to get key-value from.'],    
                    [False, '-k','--keywords', 'str', '+', 'keywords', False, False, '', '',
                        'Set the key you can get specific value of a given key.'],                    
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Read key values from key-value file. \
                                           \nThe key-value results will be stored into tube variables.'
            },
            self.C_EMAIL: {
                self.C_SUPPORT_FROM_VERSION: '2.0.0',
                self.C_ARG_SYNTAX: 'Syntax: EMAIL: -t addressA[,addressB][...] -s subject -b body | $file [--continue [m][n]] [--redo [m]] [--if run] [--key]',
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
                self.C_COMMAND_DESCRIPTION: 'Sent Email to someone with given subject and content.'
            },
            self.C_COMMAND: {
                self.C_SUPPORT_FROM_VERSION: '2.0.0',
                self.C_ARG_SYNTAX: 'Syntax: COMMAND: command [--continue [m][n]] [--redo [m]] [--if run] [--key]',
                self.C_ARG_ARGS: [        
                    [True, '-','--', 'str', '+', 'command', True, False, '', '',
                        'Any command you want to run.'],                 
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Run any Windows/MacOS terminal command.'
            },
            self.C_LINUX_COMMAND: {
                self.C_SUPPORT_FROM_VERSION: '2.0.0',
                self.C_ARG_SYNTAX: 'Syntax: LINUX_COMMAND: command [--continue [m][n]] [--redo [m]] [--if run] [--key]',
                self.C_ARG_ARGS: [        
                    [True, '-','--', 'str', '+', 'command', True, False, '', '',
                        'Any Linux command you want to run.'], 
                    [False, '-','--log-detail', '', '', 'is_log_detail', False, True, 'store_true', False,
                        'Log command output to tube log file. Default no. [2.0.2]'],                 
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Run a Linux command from the previous connected server.'                
            },
            self.C_COUNT: {
                self.C_SUPPORT_FROM_VERSION: '2.0.0',
                self.C_ARG_SYNTAX: 'Syntax: COUNT: -f file | -t statusA,B,.. -v variable [-c] [-s] [--continue [m][n]] [--redo [m]] [--if run] [--key]',
                self.C_ARG_ARGS: [        
                    [False, '-f','--file', 'str', '+', 'file', False, False, '', '',
                        'The file you want to count line numbers.'],
                    [False, '-t','--tube', 'str', '+', 'tube', False, False, '', '',
                        'The tube status you want to count.'],
                    [False, '-v','--variable', 'str', '+', 'variable', True, False, '', '',
                        'The tube variable name to store the count result.'],
                    [False, '-c','--current', '', '', 'current_tube', False, True, 'store_true', False,
                        'If only count current tube. Default no.'],
                    [False, '-s','--skip', '', '', 'skip_count', False, True, 'store_true', False,
                        'If skip COUNT command. Default no.'],
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Count file lines number (-f) or Count tube command number by status (-t).' 
            },
            self.C_SFTP_GET: {
                self.C_SUPPORT_FROM_VERSION: '2.0.1',
                self.C_ARG_SYNTAX: 'Syntax: SFTP_GET: -r remotefile -l localfile [--continue [m][n]] [--redo [m]] [--if run] [--key]',
                self.C_ARG_ARGS: [        
                    [False, '-r','--remotepath', 'str',  1,  'remotepath', True, False, '', '',
                        'The file full remotepath.'],
                    [False, '-l','--localpath',  'str',  1,  'localpath', True, False, '', '',
                        'The file localpath.'],
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Using SSHClient to copy remote server file to local. \
                                           \nWhen copy multiple files using *.* then localpath must be a directory.'
            },
            self.C_SFTP_PUT: {
                self.C_SUPPORT_FROM_VERSION: '2.0.1',
                self.C_ARG_SYNTAX: 'Syntax: SFTP_PUT: -l localfile -r remotefile [--continue [m][n]] [--redo [m]] [--if run] [--key]',
                self.C_ARG_ARGS: [        
                    [False, '-l','--localpath',  'str',  1,  'localpath', True, False, '', '',
                        'The file localpath.'],                    
                    [False, '-r','--remotepath', 'str',  1,  'remotepath', True, False, '', '',
                        'The file full remotepath.'],
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Using SSHClient to put local file to remote server. \
                                           \nWhen copy multiple files using *.* then remotepath must be a directory.'
            },
            self.C_CHECK_CHAR_EXISTS: {
                self.C_SUPPORT_FROM_VERSION: '2.0.1',
                self.C_ARG_SYNTAX: 'Syntax: CHECK_CHAR_EXISTS: -f file -c characters -r result [--continue [m][n]] [--redo [m]] [--if run] [--key]',
                self.C_ARG_ARGS: [        
                    [False, '-f','--file',  'str', '+',  'file', True, False, '', '',
                        'The file you want to check.'],                    
                    [False, '-c','--char',  'str', '+',  'characters', True, False, '', '',
                        'The characters you want to check.'],
                    [False, '-r','--result', 'str', 1,   'result', True, False, '', '',
                        'The tube variable name to store the checking result.'],
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Check if given characters exists from a file. Result was updated into a tube variable.'
            },
            self.C_REPLACE_CHAR: {
                self.C_SUPPORT_FROM_VERSION: '2.0.1',
                self.C_ARG_SYNTAX: 'Syntax: REPLACE_CHAR: -f file -o oldvalue -n newvalue [-c count] [--continue [m][n]] [--redo [m]] [--if run] [--key]',
                self.C_ARG_ARGS: [        
                    [False, '-f','--file',  'str', '+',  'file', True, False, '', '',
                        'The file you want to replace given characters.'],                    
                    [False, '-o','--oldvalue',  'str', '+',  'oldvalue', True, False, '', '',
                        'The oldvalue you want to replace (Support regular expressions).'],
                    [False, '-n','--newvalue', 'str', '+',   'newvalue', True, False, '', '',
                        'The newvalue to replace.'],
                    [False, '-c','--count', 'str', 1,   'count', False, False, '', '',
                        'The replaced times you want to set. Default no limitation.'],
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Replace file line content which contains/matches given value.'
            },
            self.C_PRINT_VARIABLES: {
                self.C_SUPPORT_FROM_VERSION: '2.0.2',
                self.C_ARG_SYNTAX: 'Syntax: PRINT_VARIABLES: name [--continue [m][n]] [--redo[m]] [--if run] [--key]',
                self.C_ARG_ARGS: [        
                    [True, '-','--', 'str', '+', 'name', True, False, '', '',
                        'The tube variable name. Provide value \'*\' can print all variable.'],
                ],
                self.C_CONTINUE_PARAMETER: True,
                self.C_REDO_PARAMETER: True,
                self.C_IF_PARAMETER: True,
                self.C_COMMAND_DESCRIPTION: 'Print tube variable values for debugging purpose.'
            },
        }

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

class TubeCommandArgumentConfig():
        
    def __init__(self, type, config_dict) -> None:
        self.type = type
        self.tube_command_arguments = []
        self.is_support_continue = True
        self.is_support_redo = True
        self.is_support_if_run = True
        self.is_support_key = True        
        self.syntax = None        
        
        if self.type in config_dict.keys():
            self.syntax = TubeCommand.get_command_syntax(self.type, Storage.I.TUBE_ARGS_CONFIG)
            self.is_support_continue = config_dict[self.type][Storage.I.C_CONTINUE_PARAMETER]
            self.is_support_redo = config_dict[self.type][Storage.I.C_REDO_PARAMETER]  
            self.is_support_if_run = config_dict[self.type][Storage.I.C_IF_PARAMETER]          
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
                new_parser.add_argument('inputs',
                                         type=type(argument.type),
                                         nargs=argument.nargs)
            else:
                if not argument.has_action:
                    # without action
                    new_parser.add_argument(argument.short_flag, 
                                        argument.long_flag,
                                        type=type(argument.type),
                                        nargs=argument.nargs,
                                        required=argument.required,
                                        dest=argument.dest)
                else:
                    # store value to action
                    new_parser.add_argument(argument.short_flag,
                                            argument.long_flag,
                                            dest=argument.dest,
                                            action=argument.action,
                                            default=argument.default,
                                            required=argument.required)
        # check general arguments
        if argument_config.is_support_continue:
            new_parser.add_argument(Storage.I.C_CONTINUE_PARAMETER, dest='continue_steps', type=int, nargs='*', required=False)
        if argument_config.is_support_redo:
            new_parser.add_argument(Storage.I.C_REDO_PARAMETER, type=int, nargs='*', required=False)
        if argument_config.is_support_if_run:
            new_parser.add_argument(Storage.I.C_IF_PARAMETER, dest='if_run', type=str, nargs='*', required=False)
        if argument_config.is_support_key:
            new_parser.add_argument(Storage.I.C_KEY_PARAMETER, dest='key', action='store_true', default=False, required=False)
        
        return new_parser

class TubeCommand():
    
    def __init__(self, cmd_type, content) -> None:
        self.cmd_type              = cmd_type
        self.uuid                  = str(uuid.uuid4())
        self.original_uuid         = self.uuid
        # contents
        self.content               = content
        self.original_content      = content
        self.redo_content          = None
        # continue & redo properties
        self.is_failed_redo        = False
        self.redo_steps            = 0
        self.is_failed_continue    = False
        self.success_skip_steps    = 0 # Success skip steps -> n
        self.is_success_skip       = False
        self.fail_skip_steps       = 0 # failed skip steps -> m
        self.is_fail_skip          = False
        self.is_skip               = False
        self.is_skip_by_if         = False
        self.is_redo_added         = False
        self.if_run                = True
        self.index                 = None
        self.log                   = None
        self.is_imported           = False
        self.has_syntax_error      = False
        self.tube_index            = 0
        self.tube_file             = ''
        self.log                   = TubeCommandLog(self)
        self.is_single_placeholder = False
        self.has_placeholders      = False
        self.is_key_command        = False
        self.results               = []
        
        # Private properties
        self.__original_content2   = None # content without place holders        
        
        # return if content is empty
        if self.content == None:
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
        self.tube_argument_config = TubeCommandArgumentConfig(self.cmd_type, Storage.I.TUBE_ARGS_CONFIG)
        self.tube_argument_parser = TubeArgumentParser.create_argument_parser(self.tube_argument_config)
    
    def get_formatted_status(self) -> str:
        '''
        Return something like: '[0] - status - type - content
        '''
        status = 'NOT STARTED'
        if self.log and self.log.status != None:
            status = self.log.status
        index = 0
        if self.index != None:
            index = self.index
        return '[%s] - [%s] - %s: %s' % (str(index), status, self.cmd_type, self.get_formatted_content())

    def get_formatted_type(self):
        '''
        Return something like: * COMMAND_TYPE[0]
        '''
        command_type = self.cmd_type
        command_type += '[%s]' % str(self.tube_index)
        if self.is_redo_added == True:
            command_type = '* ' + command_type
        return command_type
    
    def get_formatted_content(self):
        '''
        Remove the placehoders form the content and return
        '''
        try:
            if self.__original_content2 == None:
                self.__original_content2 = TubeCommand.format_placeholders(self.original_content)
            return self.__original_content2
        except Exception as e:
            return self.original_content
    
    def reset_general_arguments(self):
        
        # return command with singlie placeholder
        if self.is_single_placeholder:
            return
        
        args, unknow = general_command_parser.parse_known_args(self.content.split())
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
        
        # analyze redo parameter
        if args.redo != None:       
            self.is_failed_continue = True
            self.is_failed_redo = True
            
            # Get redo steps
            if len(args.redo) > 0:
                # replace placeholders
                redo_steps_str = TubeCommand.format_placeholders(args.redo[0]) 
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
                args.continue_steps[i] = int(TubeCommand.format_placeholders(n))
                
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

        # analyze if parameter
        if args.if_run != None:
            for value in args.if_run:
                value = TubeCommand.format_placeholders_no_error(value)
                
                # case for normal
                if '==' not in value and '!=' not in value and \
                    '<' not in value and '>' not in value:
                    if value.upper() == 'FALSE' or value.upper() == 'NO':
                        self.if_run = False
                        break
                    
                # case for equal
                elif '==' in value:
                    index = value.index('==')
                    left = value[:index]
                    right = value[index+2:]
                    # check boolean logic    
                    left, right = Utility.reset_yes_no_character(left,right)                                 
                    # check for other normal cases
                    if left != right:
                        self.if_run = False
                        break
                    
                # case for not equal
                elif '!=' in value:
                    index = value.index('!=')
                    left = value[:index]
                    right = value[index+2:]
                    # check boolean logic    
                    left, right = Utility.reset_yes_no_character(left,right)                                 
                    # check for other normal cases
                    if left == right:
                        self.if_run = False
                        break
                
                # case for greater than 
                elif '>' in value:
                    # to check if there is >= case
                    is_greater_or_equal = True if '>=' in value else False                    
                    index = value.index('>=') if is_greater_or_equal else value.index('>')
                    left = value[:index]
                    right = value[index+2:] if is_greater_or_equal else value[index+1:]
                    left = float(left)
                    right = float(right)
                    if is_greater_or_equal:
                        # >=
                        if left < right:
                            self.if_run = False
                            break
                    else:
                        # >
                        if left <= right:
                            self.if_run = False
                            break
                
                # case for less than 
                elif '<' in value:
                    # to check if <= case
                    is_less_or_equal = True if '<=' in value else False                    
                    index = value.index('<=') if is_less_or_equal else value.index('<')
                    left = value[:index]
                    right = value[index+2:] if is_less_or_equal else value[index+1:]
                    left = float(left)
                    right = float(right)
                    if is_less_or_equal:
                        # <=
                        if left > right:
                            self.if_run = False
                            break
                    else:
                        # <
                        if left >= right:
                            self.if_run = False
                            break
        
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
        args, _ = parser.parse_known_args(self.content.split())
        file_name = ' '.join(args.file)
        xpath = ' '.join(args.xpath)
            
        # replace placeholders
        file_name = TubeCommand.format_placeholders(file_name)
        xpath = TubeCommand.format_placeholders(xpath)    
            
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
        return (return_val, file_name, xpath)
    
    def set_xml_tag_text(self):
        '''
        For command: SET_XML_TAG_TEXT
        '''
        file_name, xpath, value = None, None, None
        parser = self.tube_argument_parser
        args, _ = parser.parse_known_args(self.content.split())
        file_name = ' '.join(args.file)
        xpath = ' '.join(args.xpath)
        value = ' '.join(args.value)
        
        # get value from dict
        if value.startswith('$'):
            if value[1:] in Storage.I.KEY_VALUES_DICT.keys():
                value = value[1:]            
                value = Storage.I.KEY_VALUES_DICT[value]   
            else:
                raise Exception('Value not found for key: ' + value)
            
        # replace placeholders
        file_name = TubeCommand.format_placeholders(file_name)
        xpath = TubeCommand.format_placeholders(xpath)
        value = TubeCommand.format_placeholders(value)
        
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
            return True
        else:
            raise Exception('XML file doesnot exist: ' + file_name)
        return False
    
    def get_package_version(self, url):
        try:
            package, start, end = '', '', ''
            parser = self.tube_argument_parser
            args, _ = parser.parse_known_args(self.content.split())
            package = args.package[0]
            start = args.start[0]
            end = args.end[0]
                
            # replace placeholders
            package = TubeCommand.format_placeholders(package)
            start = TubeCommand.format_placeholders(start)
            end = TubeCommand.format_placeholders(end)

            url += package + '/versions/%5B' + start + ',' + end + ')'
            source = requests.get(url)
            soup = BeautifulSoup(source.text, 'lxml')
            resources = soup.find('resources')
            resource_array = resources.find_all('resource')
            if len(resource_array) > 0:
                name = resource_array[0]['name']
                return (package, name[len(package)+1:])
            else:
                return None
        except Exception as e:
            msg = 'Get package version failed:' + 'package=' + package
            tprint(msg, type=Storage.I.C_PRINT_TYPE_ERROR)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
            return None

    def set_file_key_value(self):
        '''
        For command: SET_FILE_KEY_VALUE
        '''
        return_val = False
        file_name, keywords, value = '', '', ''
        parser = self.tube_argument_parser
        args, _ = parser.parse_known_args(self.content.split())
        file_name = ' '.join(args.file)
        keywords = ' '.join(args.keywords)
        value = ' '.join(args.value)
            
        # replace placeholders
        file_name = TubeCommand.format_placeholders(file_name)
        keywords = TubeCommand.format_placeholders(keywords)    
        value = TubeCommand.format_placeholders(value)    
            
        if(path.exists(file_name)):
            
            is_file_endswith_newline = False

            # get value from dict
            if value.startswith('@') or value.startswith('$'):
                if value[1:] in Storage.I.KEY_VALUES_DICT.keys():
                    value = value[1:]            
                    value = Storage.I.KEY_VALUES_DICT[value]   
                else:
                    raise Exception('Value not found for key: ' + value)         
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
                    tprint('File (%s) content: \n' % file_name + file_content, type=Storage.I.C_PRINT_TYPE_DEBUG)
                except Exception as ed:
                    tprint(str(ed), type=Storage.I.C_PRINT_TYPE_DEBUG)
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
        args, _ = parser.parse_known_args(self.content.split())
        file = ' '.join(args.file)
        if args.number:
            line_no = args.number[0]
        line_content = ' '.join(args.value)
        if args.contains:
            line_contains = ' '.join(args.contains)    
    
        # replace placeholders
        file = TubeCommand.format_placeholders(file)
        line_content = TubeCommand.format_placeholders(line_content)
        line_contains = TubeCommand.format_placeholders(line_contains)
        line_no = TubeCommand.format_placeholders(str(line_no))
        line_no = int(line_no)
        
        # read write content from file or $NLB, $NLA, $DL
        if line_content.startswith('$'):
            input_content = line_content[1:]
            # first check if it's write new line or delete line
            if input_content == Storage.I.C_NEW_LINE_BEFORE_SHORT:
                line_content = Storage.I.C_NEW_LINE_BEFORE
            elif input_content == Storage.I.C_NEW_LINE_AFTER_SHORT:
                line_content = Storage.I.C_NEW_LINE_AFTER
            elif input_content == Storage.I.C_DELETE_LINE_SHORT:
                line_content = Storage.I.C_DELETE_LINE
            else:
                # read content from file
                line_content = Utility.read_file_content(input_content)
                if not line_content:
                    return True
            
        # check if in append mode
        if line_no == 0 and line_contains == None:
            write_mode = 'a+'
            is_append_mode = True
        
        # write line content to file
        if os.path.exists(file):
            lines = []
            # If not in append mode, then read original lines into memory
            if is_append_mode == False:
                with open(file,'r') as f:
                    lines = f.readlines()
            if is_append_mode == False and lines and len(lines) > 0:                      
                no = 0
                updated = False
                for line in lines:                                
                    # break for loop if there is no conditions
                    if line_no == 0 and line_contains == None:
                        break
                    
                    # increase the line number
                    # to see if it equals user input
                    no += 1
                    
                    # check line contains parameter
                    contains_valid = False
                    if line_contains:
                        if line_contains not in line:
                            continue 
                        else:
                            contains_valid = True
                        
                    # check line no and line contains
                    if (no == line_no and line_no > 0) or (line_no == 0 and contains_valid == True):                    
                        ends = '\n' if line.endswith('\n') else ''
                        if line_content == Storage.I.C_NEW_LINE_BEFORE:
                            lines[no-1] = '\n' + line
                        elif line_content == Storage.I.C_NEW_LINE_AFTER:
                            lines[no-1] = line + '\n'
                        elif line_content == Storage.I.C_DELETE_LINE:
                            lines[no-1] = ''
                        else:
                            lines[no-1] = line_content + ends                  
                        updated = True
                        if line_no > 0:
                            break
                        
                # for give line nuber case, but didn't found matched line number
                # append a new line at the end        
                if not updated and not line_contains:   
                    if line_content == Storage.I.C_NEW_LINE_BEFORE or \
                    line_content == Storage.I.C_NEW_LINE_AFTER: 
                        lines.append('\n')
                    elif line_content == Storage.I.C_DELETE_LINE:
                        return True 
                    else:                    
                        lines.append('\n' + line_content)                
            else:
                # appand to an empty file
                lines = []
                if line_content == Storage.I.C_NEW_LINE_AFTER or \
                line_content == Storage.I.C_NEW_LINE_BEFORE:
                    lines.append('\n')
                elif line_content == Storage.I.C_DELETE_LINE:
                    return True
                else:
                    lines.append('\n' + line_content)
            
            # overwrite new lines into file
            with open(file, write_mode) as f:
                for line in lines:
                    f.write(line)  
            
            if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:
                try:                    
                    file_content = Utility.read_file_content(file)
                    tprint('File (%s) content: \n' % file + file_content, type=Storage.I.C_PRINT_TYPE_DEBUG)
                except Exception as ed:
                    tprint(str(ed), type=Storage.I.C_PRINT_TYPE_DEBUG)              
        else:
            raise Exception("file doesn't exist: " + file)

        return True

    def delete_line_in_file(self):
        '''
        For command: DELETE_LINE_IN_FILE
        '''
        file, line_begins, line_contains, delete_empty = '', '', '', False
        deleted_count = 0
        
        parser = self.tube_argument_parser
        args, _ = parser.parse_known_args(self.content.split())
        file = ' '.join(args.file)
        if args.begins != None:
            line_begins = ' '.join(args.begins)
        if args.contains != None:
            line_contains = ' '.join(args.contains)
        if args.del_empty:
            delete_empty = True
        # if didn't found any conditions then delete nothing
        if line_begins == '' and line_contains == '' and not delete_empty:
            raise Exception('No parameters found: -c, -b or -e')        
    
        # replace placeholders
        file = TubeCommand.format_placeholders(file)
        line_begins = TubeCommand.format_placeholders(line_begins)
        line_contains = TubeCommand.format_placeholders(line_contains)    
            
        if os.path.exists(file):
            lines = []
            lines_new = []
            is_last_char_new_line = True
            with open(file,'r') as f:
                lines = f.readlines()
                if len(lines) > 0:
                    line = lines[len(lines) - 1]
                    is_last_char_new_line = line.endswith('\n')        
            for line in lines:
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
                        
                # delte line which meet the conditions
                if is_delete == False:
                    lines_new.append(line)  
                else:
                    deleted_count += 1                    
            
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
        
            # log how many lines deleted
            msg = 'Deleted %s lines.' % (str(deleted_count))
            tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, line=msg)
        else:
            raise Exception("file doesn't exist: " + file)

        return True

    def tail_file(self):
        '''
        For command: TAIL_FILE
        '''
        file, lines_count, keywords = '', 0, ''

        parser = self.tube_argument_parser
        args, _ = parser.parse_known_args(self.content.split())
        file = ' '.join(args.file)
        lines_count = args.lines[0]
        if args.keywords != None:
            keywords = ' '.join(args.keywords)
            
        # replace placeholders
        file = TubeCommand.format_placeholders(file)
        keywords = TubeCommand.format_placeholders(keywords)  
        lines_count = TubeCommand.format_placeholders(str(lines_count))  
        lines_count = int(lines_count)
        
        return_lines = []
        try:
            if not path.exists(file):
                raise Exception("File doesn't exist: " + file)
            with open(file, 'r', encoding='utf8') as f:
                for line in f:
                    line = line.replace('\n', '')
                    if len(line) > 0:
                        return_lines.append(line)
                    if len(return_lines) > lines_count:
                        return_lines.pop(0)

            found_keyword = False
            if keywords != None and len(keywords) > 0:
                keywords_array = keywords.split(',')
                for line in return_lines:
                    for keyword in keywords_array:
                        if keyword.upper() in line.upper():
                            found_keyword = True
                            break
                    if found_keyword == True:
                        break
            else:
                found_keyword = True
            
            if found_keyword == False:
                return_lines = []
            
            return (return_lines, file, lines_count, keywords)

        except Exception as e:
            raise e

    def report_progress(self, commands):
        '''
        For command: REPORT_PROGRESS
        '''
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
        return result  

    def get_file_key_value(self):
        '''
        For command: GET_FILE_KEY_VALUE
        '''
        parser = self.tube_argument_parser
        args, _ = parser.parse_known_args(self.content.split())
        # replace , from the keys  
        keywords = []
        if args.keywords:
            # replace ',' to ''
            for i, k in enumerate(args.keywords): 
                if ',' in k:
                    keys_temp = args.keywords[i].split(',')
                    for temp in keys_temp:
                        keywords.append(temp)           
                else:
                    keywords.append(k)
            
        file = ' '.join(args.file)
        key_values = [] 
        
        # replace placeholders
        file = TubeCommand.format_placeholders(file)
        if args.keywords:
            keywords = [ TubeCommand.format_placeholders(item) for item in keywords]
        
        with open(file, 'r') as f:
            for line in f:
                line = line.replace('\n', '')
                if len(line) < 0:
                    continue
                if '=' in line:
                    i = line.index('=')
                    line_key = line[:i].strip()
                    line_value = line[i+1:].strip()
                    if len(keywords) == 0:
                        StorageUtility.update_key_value_dict(line_key, line_value, self)
                        key_values.append(line_key + '=' + line_value)
                    else:
                        for key in keywords:
                            if key == line_key:
                                StorageUtility.update_key_value_dict(key, line_value, self)   
                                key_values.append(key + '=' + line_value)
                                                   

        return True, key_values    

    def send_email_via_command(self):
        '''
        For command: EMAIL
        '''
        parser = self.tube_argument_parser
        args, _ = parser.parse_known_args(self.content.split())
        to_list = [item for item in args.to]
        to_list = ','.join(to_list)
        subject = ' '.join(args.subject)
        body = ' '.join(args.body)
        
        # replace placeholders
        to_list = TubeCommand.format_placeholders(to_list)
        subject = TubeCommand.format_placeholders(subject)
        body = TubeCommand.format_placeholders(body)
        
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
        return result

    def import_tube(self, continue_redo_parser: TubeArgumentParser):
        '''
        For command: IMPORT_TUBE
        '''
        retrun_value = False
        file = self.content
        # replace placeholders
        file = TubeCommand.format_placeholders(file) 
        insert_at_index = self.index
        tube_check = []
        with open(file, 'r') as f:
            data = Utility.safe_load_with_upper_key(f)
            if Storage.I.C_TUBE in data.keys():            
                sub_tube = data[Storage.I.C_TUBE] 
                
                if not sub_tube or type(sub_tube) != list:
                    msg = 'Tube file doesnot have any tube commands: ' + file
                    tprint(msg, type=Storage.I.C_PRINT_TYPE_WARNING)
                    write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg) 
                else:              
                    next_index = max([i for i in Storage.I.TUBE_FILE_LIST.keys()]) + 1
                    for item in sub_tube:
                        for key in item.keys():
                            sub_command = TubeCommand(key.upper(), item[key])
                            sub_command.is_imported = True
                            sub_command.tube_index = next_index
                            sub_command.tube_file = os.path.abspath(file)
                            Storage.I.TUBE_FILE_LIST[sub_command.tube_index] = sub_command.tube_file                
                            tube_check.append(sub_command)
            else:
                # the 'TUBE' section doesn't exists from the sub-tube file
                raise Exception('\'TUBE\' section doesnot exists from tube file: %s' % file)
            
            if Storage.I.C_SERVERS in data.keys():       
                # Get servers to hosts
                StorageUtility.read_hosts(data[Storage.I.C_SERVERS])
                msg = 'Servers hosts are updated by tube: %s.' % file
                tprint(msg, type=Storage.I.C_PRINT_TYPE_WARNING)
                write_line_to_log(Storage.I.TUBE_LOG_FILE, line=msg)

            if Storage.I.C_VARIABLES in data.keys():
                # Read variables 
                msg = 'Tube variables are updated by tube: %s.' % file
                tprint(msg, type=Storage.I.C_PRINT_TYPE_WARNING)
                write_line_to_log(Storage.I.TUBE_LOG_FILE, line=msg)
                StorageUtility.read_variables(data[Storage.I.C_VARIABLES])                
            
            if Storage.I.C_EMAIL in data.keys():
                # read emails
                StorageUtility.read_emails(data[Storage.I.C_EMAIL])
                msg = 'Email configurations are updated by tube: %s.' % file
                tprint(msg, type=Storage.I.C_PRINT_TYPE_WARNING)
                write_line_to_log(Storage.I.TUBE_LOG_FILE, line=msg)
                
        has_errors, errors = StorageUtility.check_tube_command_arguments(tube_check, continue_redo_parser)
        if has_errors == False:
            for sub_command in tube_check:
                Storage.I.TUBE_RUN.insert(insert_at_index, sub_command)
                insert_at_index += 1
            Storage.I.MAX_TUBE_COMMAND_LENGTH = get_max_tube_command_type_length(Storage.I.TUBE_RUN)        
            retrun_value = True
        else:
            for err in errors:
                self.log.add_error(err)
                self.log.status = Storage.I.C_FAILED       
        
        return retrun_value

    def count(self):
        '''
        For command: COUNT
        '''
        file, status_set, variable, current_tube, skip_count = '', set(), '', False, False
        parser = self.tube_argument_parser
        args, _ = parser.parse_known_args(self.content.split())
        if args.file:
            file = ' '.join(args.file)
            file = TubeCommand.format_placeholders(file)            
        if args.tube and len(args.tube) > 0:
            status_set_tmp = Utility.convert_arg_values_to_set(args.tube)
            for item in status_set_tmp:
                status_set.add(TubeCommand.format_placeholders(item))
                                
        variable = args.variable[0]
        variable = TubeCommand.format_placeholders(variable)
        
        # check flags arguments
        if args.current_tube:
            current_tube = True
        if args.skip_count:
            skip_count = True
        
        # check input parameter
        if not file and len(status_set) == 0:
            raise Exception('Parameter -f (file) or -t (tube status) is missing.')
        
        # case 1: count file lines count
        if file:
            line_count = 0
            with open(file, 'r') as f:
                line_count = sum(1 for line in f)
            StorageUtility.update_key_value_dict(variable, line_count)  
                  
        # case 2: count tube command count by status
        elif len(status_set) > 0:
            cmd_count = 0
            cmd: TubeCommand
            for cmd in Storage.I.TUBE_RUN:
                # skip COUNT command itself
                if skip_count and cmd.cmd_type == Storage.I.C_COUNT:
                    continue
                # to check if count within current tube only
                if current_tube and cmd.tube_index != self.tube_index:
                    continue
                # count tube command
                if cmd.log.status in status_set:
                    cmd_count += 1
            StorageUtility.update_key_value_dict(variable, cmd_count)
            
        return True

    def set_variable(self):
        '''
        For command: SET_VARIABLE
        '''
        name, value, is_readonly, is_force = '', '', False, False
        parser = self.tube_argument_parser
        args, _ = parser.parse_known_args(self.content.split())
        if len(args.name) > 0:
            name = args.name[0]
        if args.value:
            value = ' '.join(args.value)
        if args.is_readonly:
            is_readonly = True
        if args.is_force:
            is_force = True
        
        # replace placeholders
        name = TubeCommand.format_placeholders(name).strip()
        value = TubeCommand.format_placeholders(value).strip()

        # evalulate eval inputs
        if 'eval(' in value:
            value = value.replace('eval(', '')[:-1].replace('\'', '').replace('\"', '')
            value = eval(value)

        # check input parameter
        if not name:
            raise Exception('Parameter -n (name) is missing.')
        
        # check if variable has been updated from console inputs
        if is_force == False and name in Storage.I.KEYS_READONLY_SET:
            msg = 'Variable (%s:%s) is readonly, you cannot update except use the set_variable command.' % (name, str(Storage.I.KEY_VALUES_DICT[name]))
            tprint(msg, type=Storage.I.C_PRINT_TYPE_WARNING)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg) 
            return False
        
        # update key value dict
        if is_force:
            StorageUtility.update_key_value_dict(name, value, is_force=True)
        else:
            StorageUtility.update_key_value_dict(name, value)
        
        # check if marek variable as readonly
        if is_readonly == True and not name in Storage.I.KEYS_READONLY_SET:
            # Flag it has been updated to readonly
            Storage.I.KEYS_READONLY_SET.add(name)
            msg = 'Variable (%s:%s) is set to readonly.' % (name, str(Storage.I.KEY_VALUES_DICT[name]))
            tprint(msg, type=Storage.I.C_PRINT_TYPE_WARNING)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg) 
        
        return True

    def sftp_get_put(self, ssh):
        '''
        Get or Put files between local and linux server using ssh.
        '''
        localpath, remotepath = '',''
        
        parser = self.tube_argument_parser
        args, _ = parser.parse_known_args(self.content.split())
        localpath = args.localpath[0]
        remotepath = args.remotepath[0]
        
        # replace placeholders
        localpath = TubeCommand.format_placeholders(localpath)
        remotepath = TubeCommand.format_placeholders(remotepath)
        
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
        args, _ = parser.parse_known_args(self.content.split())
        file, characters, result = '', '', False
        
        # get user inputs
        file = ' '.join(args.file)
        characters = ' '.join(args.characters)
        result = args.result[0]
        
        # replace placeholders
        file = TubeCommand.format_placeholders(file)
        characters = TubeCommand.format_placeholders(characters)
        result = TubeCommand.format_placeholders(result)
        
        found = False
        # read file line by line
        try:
            with open(file, 'r') as f:
                for line in f:
                    if characters in line:
                        found = True
                        break                       
        
        finally:
            # update result to tube variables
            StorageUtility.update_key_value_dict(result, found)
    
    def replace_char(self) -> int:
        '''
        Replace strings for a given file line by line
        '''
        parser = self.tube_argument_parser
        args, _ = parser.parse_known_args(self.content.split())
        file, oldvalue, newvalue, count = '', '', '', sys.maxsize
        
        # get user inputs
        file = ' '.join(args.file)
        oldvalue = ' '.join(args.oldvalue)
        newvalue = ' '.join(args.newvalue)
        if args.count:
            count = int(args.count[0])
        
        # check input count parameter
        if count < 1:
            raise Exception('Count parameter is less than 1: %s' % str(count))
        
        # replace placeholders
        file = TubeCommand.format_placeholders(file)
        oldvalue = TubeCommand.format_placeholders(oldvalue)
        newvalue = TubeCommand.format_placeholders(newvalue)
        
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
        
        return replaced_count
    
    def print_variables(self):
        new_vars = []
        default_vars = []
        for key in Storage.I.KEY_VALUES_DICT.keys():
            if self.content == '*' or self.content == None or key.upper() in self.content.upper():
                # get value
                value = str(Storage.I.KEY_VALUES_DICT[key])
                if value == ' ':
                    value = '\' \''
                # get readonly
                readonly = ''
                if key in Storage.I.KEYS_READONLY_SET:
                    readonly = ' (readonly)'
                msg = '%s=%s %s' % (key, value, readonly)
                if key == 's' or key == 'S' or key == Storage.I.C_TUBE_HOME:
                    default_vars.append(msg)
                else:
                    new_vars.append(msg)
        
        for var in new_vars:
            tprint(var, type=Storage.I.C_PRINT_TYPE_INFO)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', var)
        
        if len(default_vars) > 0:
            msg = ' * Below list are hidden variables *'
            tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
            
        for var in default_vars:
            tprint(var, type=Storage.I.C_PRINT_TYPE_INFO)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', var) 
    
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
       
    # ---- IMPORTANT RULE ------
    # The best time to format placesholder is when running this command
    # for display command content could use the format_placeholders_no_error method
    @classmethod
    def format_placeholders(self, value):
        '''
        Replace all placeholders {variable_name} from tube variables
        
        Parameters:
            value: The string you want to replace its all placeholders.
        '''
        
        # return for None or empty
        if not value:
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
        
        # add format support
        value = value.replace('{0:', '{s:') # to compatible with {0:m} syntax
        # replace placeholders from tube commands
        ret_value = value.format(**Storage.I.KEY_VALUES_DICT)
        return ret_value

    @classmethod
    def format_placeholders_no_error(self, value): 
        '''
        Replace all placeholders {variable_name} from tube variables with no error.
        
        Parameters:
            value: The string you want to replace its all placeholders.
        '''   
        
        ret_value = value
        try:
            ret_value = TubeCommand.format_placeholders(value)
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
        general_args = '[--continue [m][n]] [--redo [m]] [--if run] [--key]'
        args = arg_config[Storage.I.C_ARG_ARGS]
        for arg in args:
            if arg[0] is True: # postion argument
                syntax += arg[5]
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
                    parameters += format_str.format(indentation + arg[1] + '/' + arg[2] + ':', arg[len(arg) - 1] + '\n')
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

    def format_log(self, sequence):
        '''
        format tube log status overview
        '''
        duration_in_s = self.get_total_seconds()
        duration_str = '%s SEC' % duration_in_s
        command_type = self.command.get_formatted_type()
        if duration_in_s >= 60:
            duration_str = '%s MIN' % self.get_total_minutes()
        return_foramt = '%5s - %10s - %8s - %' + str(Storage.I.MAX_TUBE_COMMAND_LENGTH) + 's: %s'        
        return return_foramt % \
            ('[' + str(sequence) + ']', self.status, duration_str, command_type, \
             self.command.get_formatted_content())
    
    def print_log(self, sequence):
        '''
        print tube log status overview
        '''
        duration_in_s = self.get_total_seconds()
        duration_str = '%s SEC' % duration_in_s
        if duration_in_s >= 60:
            duration_str = '%s MIN' % str(int(divmod(duration_in_s, 60)[0]))
        command_type = self.command.get_formatted_type()
        log_format = '%5s - %10s - %8s - %' + str(Storage.I.MAX_TUBE_COMMAND_LENGTH) + 's: %s'
        log_value = ('[' + str(sequence) + ']', self.status, duration_str, 
                     command_type, self.command.get_formatted_content())
        msg = log_format % log_value
        if self.status == Storage.I.C_SUCCESSFUL:
            tprint(msg, tcolor=Storage.I.C_PRINT_COLOR_GREEN, prefix=Storage.I.C_PRINT_PREFIX_EMPTY)
        elif self.status == Storage.I.C_FAILED:
            tprint(msg, tcolor=Storage.I.C_PRINT_COLOR_RED, prefix=Storage.I.C_PRINT_PREFIX_EMPTY)            
        elif self.status == Storage.I.C_SKIPPED:
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
    
class Host():
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
            self.errors.clear()
        except Exception as e:
            msg = 'When connect to server: %s, port: %s, user: %s, password: %s, exception: %s' % \
                    (self.host, str(self.port), self.user, self.password, str(e))
            tprint(msg, type=Storage.I.C_PRINT_TYPE_ERROR) 
            self.errors.add(msg)
            #write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
            self.is_connected = False
            self.ssh = None        
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
    def update_key_value_dict(self, key, value, command: TubeCommand=None, is_force=False):
        '''
        Update storage's key-value pair
        
        if the key already exist, then a warning will be loged into the log file.
        
        Parameters:
            key: the key you want to update
            value: the key's value, if None then empty string will be used
        '''
        # return for None or empty key
        if not key:
            return False
        
        # skip update 's' or 'S' reserved key
        if key.upper() == 'S':
            msg = 'It\'s not allowed to update tube reserved variable \'s\' with value: ' + str(value)
            tprint(msg, type=Storage.I.C_PRINT_TYPE_WARNING)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)        
            return False  
        
        # If value is None, then udpate it with empty string
        if value == None:
            value = ''
        
        # update the key value
        updated = False        
        if not key in Storage.I.KEYS_READONLY_SET:
            Storage.I.KEY_VALUES_DICT[key] = value
            updated = True
        else:
            if is_force == False:
                msg = 'Variable (%s:%s) is readonly, you cannot update except use the set_variable command.' % (key, str(Storage.I.KEY_VALUES_DICT[key]))
                tprint(msg, type=Storage.I.C_PRINT_TYPE_WARNING)
                write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)   
            else:
                Storage.I.KEY_VALUES_DICT[key] = value
                updated = True        
        
        # give an note if the key-value dict was udpated        
        if updated:
            # give a warning that the key-value was overrode from the memory
            forced = ' '
            if is_force:
                forced = ' forced '
            msg = 'Tube variable \'%s\' was%supdated to value: \'%s\'.' % (key, forced, value)
            if command:
                msg += ' By tube[%s] command: %s' % (str(command.tube_index), command.cmd_type + ': ' + str(command.get_formatted_content()))
            tprint(msg, type=Storage.I.C_PRINT_TYPE_WARNING)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
                
        return True
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
            if command.cmd_type == Storage.I.C_COMMAND or \
            command.cmd_type == Storage.I.C_LINUX_COMMAND:
                continue
            
            # check invalid command type
            if command.cmd_type not in Storage.I.TUBE_ARGS_CONFIG.keys():
                has_errors = True            
                msg = 'Command: %s doesnot support now.' % command.cmd_type
                if command.cmd_type.upper() in Storage.I.TUBE_ARGS_CONFIG.keys():
                    msg = 'Command: %s is only support in upper case.' % command.cmd_type
                tprint(msg, type=Storage.I.C_PRINT_TYPE_ERROR)
                errors_return.append(msg)
                write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
                continue
                        
            if command.content == None:
                msg = 'Command: %s is empty.' % command.cmd_type
                tprint(msg, type=Storage.I.C_PRINT_TYPE_ERROR)
                errors_return.append(msg)            
                write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
                has_errors = True
                continue
            
            # check if syntax errors
            if command.tube_argument_parser != None:
                command_content = TubeCommand.format_placeholders_no_error(command.content)            
                command.tube_argument_parser.parse_args(command_content.split())
                syntax_errors = command.tube_argument_parser.get_formated_errors()
                if len(syntax_errors) > 0:
                    command.has_syntax_error = True
                    has_errors = True                
                    for err in syntax_errors:
                        msg = '%s: %s' % (command.cmd_type, err)
                        tprint(msg, type=Storage.I.C_PRINT_TYPE_ERROR)
                        errors_return.append(msg)                    
                        write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)                    
                command.tube_argument_parser.argument_error.clear() 
            
            # check Server exists
            if command.has_syntax_error == False and \
            command.cmd_type == Storage.I.C_CONNECT:
                command_content = TubeCommand.format_placeholders_no_error(command.content)
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
                servers = Utility.safe_load_with_upper_key(f)
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
    def read_variables(self, variables):
        '''
        Read tube variables from tube variable section.
        '''
        
        if(not variables or type(variables) is not dict):
            return
        for key in variables.keys():
            StorageUtility.update_key_value_dict(key, variables[key])
        
        # always set key 's' to ' '
        Storage.I.KEY_VALUES_DICT['s'] = ' '
        Storage.I.KEY_VALUES_DICT['S'] = ' '      

    @classmethod
    def read_emails(self, emails):     
        '''
        Read email configurations from 'EMAIL' section.
        '''   
        if type(emails) is str:
            with open(emails, 'r') as f:
                emails = Utility.safe_load_with_upper_key(f)
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
    def read_variables_from_console(self, variables):
        '''
        Read tube variables from user inputs.
        If variable was updated from console, then it 
        cannot be udpated again by other tube commands.
        '''
        if not variables:
            return
        try:
            for var in variables:
                if '=' in var:
                    i = var.index('=')
                    var_key = var[0:i]
                    var_value = var[i+1:]
                    msg = 'Read console variable: \'%s\', value: \'%s\' from console.'                
                    tprint(msg % (var_key, var_value), type=Storage.I.C_PRINT_TYPE_INFO)
                    write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg % (var_key, var_value))
                    StorageUtility.update_key_value_dict(var_key, var_value)
                    # Flag it has been udpated by the user console inputs
                    Storage.I.KEYS_READONLY_SET.add(var_key)
                    msg = 'Variable (%s:%s) is set to readonly.' % (var_key, str(Storage.I.KEY_VALUES_DICT[var_key]))
                    tprint(msg, type=Storage.I.C_PRINT_TYPE_WARNING)
                    write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
        except Exception as e:
            msg = 'Read variables from console exception: ' + str(e)
            tprint(msg, type=Storage.I.C_PRINT_TYPE_ERROR)
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)

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
            Storage.I.C_PRINT_COLOR_BLUE = 'blue'
            Storage.I.C_PRINT_COLOR_PURPLE = 'purple'
            Storage.I.C_PRINT_COLOR_GREEN = 'green'
            Storage.I.C_PRINT_COLOR_ORANGE = 'orange'
            Storage.I.C_PRINT_COLOR_YELLOW = 'yellow'
            Storage.I.C_PRINT_COLOR_STYLE = 'bright'
  
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
        command_new.is_imported = redo_command.is_imported
        command_new.tube_index = redo_command.tube_index
        command_new.tube_file = redo_command.tube_file
        command_new.original_uuid = redo_command.uuid
        
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
            command_new.is_imported = redo_command.is_imported
            command_new.tube_index = redo_command.tube_index       
            command_new.tube_file = redo_command.tube_file  
            command_new.original_uuid = command.uuid      
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
            command_new.is_imported = redo_command.is_imported
            command_new.tube_index = redo_command.tube_index
            command_new.tube_file = redo_command.tube_file
            command_new.original_uuid = redo_command.uuid
        
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
def tprint(line='', prefix=None, type=None, tcolor=None, tcolor_style=None, splitchar=': '):
    
    '''
    line: the string to output to the console
    prefix: Any character print at the begining
    type: it could be 'INFO', 'WARNING', 'ERROR' or ''
    tcolor: the color of the main printed string
    
    return: prefix + type + line
    '''
    
    # return if in matrix terminal mode
    if Storage.I.IS_MATRIX_MODE_RUNNING:
        return
    
    # switch color style
    if os.name.startswith('nt') and not tcolor_style:
        tcolor_style = 'bright'
    
    # deal with type color
    if type == Storage.I.C_PRINT_TYPE_WARNING:
        type = color(type + splitchar, fore=Storage.I.C_PRINT_COLOR_ORANGE, style=tcolor_style)
        if not prefix:
            prefix = Storage.I.C_PRINT_PREFIX
    elif type == Storage.I.C_PRINT_TYPE_ERROR:
        type = color(type + splitchar, fore=Storage.I.C_PRINT_COLOR_RED, style=tcolor_style)
        if not prefix:
            prefix = Storage.I.C_PRINT_PREFIX
        if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:
            traces = traceback.format_exc()
            if not traces.startswith('NoneType'):
                line += '\n' + traces
    elif type == Storage.I.C_PRINT_TYPE_INFO:
        type = color(type + splitchar,fore=Storage.I.C_PRINT_COLOR_BLUE, style=tcolor_style)
        if not prefix:
            prefix = Storage.I.C_PRINT_PREFIX
    elif type == Storage.I.C_PRINT_TYPE_DEBUG:
        type = color(type + splitchar,fore=Storage.I.C_PRINT_COLOR_PURPLE, style=tcolor_style)
        if not prefix:
            prefix = Storage.I.C_PRINT_PREFIX
    else:
        type = Storage.I.C_PRINT_TYPE_EMPTY
    
    # deal with main color
    if tcolor:
        line = color(line, fore=tcolor, style=tcolor_style)
    
    # combine type + str    
    line = type + line
    
    # deal with prefix
    if prefix:
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

def get_ant_build_errors(log: TubeCommandLog):
    
    '''
    Currently this method is not used, it would be helpfule to read additional log errors from other files
    Keep it here in case some day later to use it.
    '''
    
    found_error = False
    return_lines = []
    try:
        logFile = os.path.join(os.getcwd(), Storage.I.C_ANT_DEPLOY_LOG_FILE)
        if not path.exists(logFile):
            return False
        
        # return last 50 lines
        with open(logFile, 'r', encoding='utf8') as f:
            for line in f:
                line = line.replace('\n', '')
                if Storage.I.C_ANT_DEPLOY_ERROR in line:
                    found_error = True
                if found_error and len(line) > 0:
                    return_lines.append(line)
        # output errors
        if found_error:
            log.add_error('THE FOLLOWING ERRORS ARE READ FROM FILE => ' + logFile)
            for line in return_lines:            
                log.add_error(line)               
  
        return found_error                               
                    
    except Exception as e:
        return False

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
    for item in Storage.I.TUBE:            
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

def output_tube_file_list(is_print=False, is_write_log=False):
    keys = [k for k in Storage.I.TUBE_FILE_LIST.keys()]
    keys.sort()  
    for k in keys:
        msg = '* [%s]: %s' % (str(k), Storage.I.TUBE_FILE_LIST[k])
        if is_print:
            tprint(msg)
        if is_write_log:
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)            

def print_logs(LOGS):
    tprint()    
    
    # print status of each command
    tprint('----- Status of Each Command -----')    
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
    # If output note for * before command type    
    if has_retried_command == True:
        tprint(Storage.I.C_RETRIED_COMMAND_NOTE) 
    
    # print overall tube logs at the end
    # then it's easier for the user to see
    tprint() 
    tprint(Storage.I.C_FINISHED_HEADER, tcolor=Storage.I.C_PRINT_COLOR_YELLOW)
    tprint(calculate_success_failed_details(LOGS, False))
    tprint()   
    
    # print total running during time
    totals = '%s minutes' % str(int(divmod(total_seconds, 60)[0]))
    if total_seconds < 60:
        totals = '%s seconds' % str(total_seconds)
    tprint('-------------------------------')
    tprint('Total Time: %s' % totals)
    tprint('-------------------------------')

def check_if_key_command_exists():
    command: TubeCommand
    for command in Storage.I.TUBE_RUN:
        if command.check_if_key_command():
            return True
    return False

def get_command_result_by_uuid(uuid):
    command: TubeCommand
    status = Storage.I.C_FAILED
    for command in Storage.I.TUBE_RUN:
        if command.original_uuid == uuid:
            if command.log.status == Storage.I.C_SKIPPED and status == Storage.I.C_FAILED:
                status = Storage.I.C_SKIPPED
            elif command.log.status == Storage.I.C_SUCCESSFUL and status != Storage.I.C_SUCCESSFUL:
                status = Storage.I.C_SUCCESSFUL
                return status
    return status

def calculate_success_failed_details(LOGS, is_for_email):
    success_count = 0
    failed_count = 0    
    skipped_count = 0
    details = None
    result = None

    # calcualte success and failed count
    for log in LOGS:
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
    key_command_exists_all = check_if_key_command_exists()    
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
            if command.check_if_key_command() and command.is_skip_by_if == False:
                key_command_result = get_command_result_by_uuid(command.original_uuid)
                if key_command_result != Storage.I.C_SUCCESSFUL:
                    result_tmp = Storage.I.C_FAILED
                    break
        
        # include the loops and details information
        result += result_tmp + loops + newline + details

    return result

def write_logs_to_file(LOGS):
    
    mode = 'a+'
    # output overall status
    write_line_to_log(Storage.I.TUBE_LOG_FILE, mode, '')
    write_line_to_log(Storage.I.TUBE_LOG_FILE, mode, Storage.I.C_FINISHED_HEADER)

    result = calculate_success_failed_details(LOGS, False)
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
        write_line_to_log(Storage.I.TUBE_LOG_FILE, mode, log.format_log(seq))
    
    # output tube file list
    output_tube_file_list(is_write_log=True)
    # If output note for * before command type
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
    result = calculate_success_failed_details(LOGS, True)
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

    # tail file lines
    for line in Storage.I.FILE_TAIL_LINES:
        if Storage.I.C_TAIL_LINES_HEADER in line:
            line = line
            email_body += '<br><b>' + line + '</b><br>'
        else:
            email_body += line.replace('\t', '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;').replace('<','&lt;').replace('>','&gt;') + '<br>'
    
    # prepare to sent email
    result = send_email(Storage.I.EMAIL_SENDER_ADDRESS, Storage.I.EMAIL_SENDER_PASSWORD, Storage.I.EMAIL_RECEIVER_ADDRESS, 
                        Storage.I.EMAIL_SUBJECT, email_body, Storage.I.EMAIL_SMTP_SERVER)
    if result == True:
        msg = 'Email sent successfully!'
        tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO)
        write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
    msg = '--------------------------------'
    tprint(msg)
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
         
def output_tail_lines(lines):
    for line in lines:
        if line.startswith(Storage.I.C_TAIL_LINES_HEADER):
            tprint(line, type=Storage.I.C_PRINT_COLOR_ORANGE)
        else:
            tprint(line)
        write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', line)
    if len(lines) > 0:
        write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', '-------------- END OF TAIL LINES --------------')

def output_log_header():
    # Log start for xxx.yaml.log    
    Storage.I.START_DATE_TIME = datetime.now()
    run_mode = ' (%s)' % Storage.I.RUN_MODE
    write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', 
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
    parser.add_argument('-v', '--vars', type=str, dest='variables', nargs='+',
                        help='Pass tube variables into tube: var1=value1 var2=value2')                 
    parser.add_argument('-i', '--immediate', dest='immediate', action='store_const', const='yes',
                        help='A flag to tell if run the tube immediately, but needs a user confirm. \nDefault no.')  
    parser.add_argument('-f', '--force', dest='force', action='store_const', const='yes',
                        help='A flag to run tube at once without confirmation. \nDefault no.') 
    parser.add_argument('-t', '--datetime', dest='datetime',
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
    parser.add_argument('--pip', dest='pip_command',
                        help='To tell which pip command is used. e.g.: pip or pip3. \nWindows system is default pip, and MacOS system is default pip3. ' + \
                              '\nUsually you don\'t need to provide this parameter value, \nexcept in Windows system, it\'s not pip and in MacOS, it\'s not pip3.')                                                    
    parser.add_argument('--version', action='version', version=Storage.I.C_CURR_VERSION,
                        help='Print current version.')  
    parser.add_argument('help', type=str, nargs='*', 
                         help=Storage.I.C_HELP)     

    # general_command_parser is used to analyze the COMMAND or LINUX_COMMAND arguments
    general_command_parser.add_argument(Storage.I.C_CONTINUE_PARAMETER, dest='continue_steps', type=str, help=argparse.SUPPRESS, nargs='*')   
    general_command_parser.add_argument(Storage.I.C_REDO_PARAMETER, type=str, help=argparse.SUPPRESS, nargs='*')
    general_command_parser.add_argument(Storage.I.C_IF_PARAMETER, dest='if_run', type=str, help=argparse.SUPPRESS, nargs='*')
    general_command_parser.add_argument(Storage.I.C_KEY_PARAMETER, dest='key', action='store_true', default=False, required=False)
    
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

def get_max_tube_command_type_length(tube):
    if tube == None or len(tube) == 0:
        return Storage.I.MAX_TUBE_COMMAND_LENGTH
    c: TubeCommand
    type_list = [c.cmd_type for c in tube]
    max_length = len(max(type_list, key=len))
    return max_length + 5

def convert_tube_to_new(tube, is_from_job_start=False):
    '''
    Convert tube from yaml format to TubeCommand list
    '''
    
    tube_new = []
    
    # check empty tube commands
    if not tube:
        return tube_new
    
    # go through each tube command and imported
    for item in tube:            
        for key in item.keys():                  
            command = TubeCommand(key.upper(), item[key])
            if is_from_job_start == True:
                command.tube_file = os.path.abspath(Storage.I.TUBE_YAML_FILE)
                Storage.I.TUBE_FILE_LIST[command.tube_index] = command.tube_file
            tube_new.append(command) 
            
    # update max command type length
    Storage.I.MAX_TUBE_COMMAND_LENGTH = get_max_tube_command_type_length(tube_new)
    return tube_new  

def disconect_all_hosts(hosts):
    try:
        for host_name in hosts.keys():
            host: Host = hosts[host_name]
            if host.is_connected:
                host.disconnect()        
    except Exception as e:
        tprint('DISCONECT ALL HOSTS EXCEPTION: ' + str(e), type=Storage.I.C_PRINT_TYPE_ERROR)

def print_tube_command_help(parser: ArgumentParser):
    try:   
        args = parser.parse_args()    
        if(args.help):
            if(len(args.help) >= 1 and len(args.help) <= 2 and args.help[0].upper() == 'HELP'):
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
                marked as successfull. (If the command's --if condition is False, then --key
                will be skipped.)
                '''
                help_var = '''
    - Tube Variables            
        From tube YAML file, you can add tube variables under 'VARIABLES' property. 
        e.g.:       
        VARIABLES:  
            root_folder: C:\workspaces\trunk
            package_name: xxx-app
            cmd_parameters: -l
            # Below two hidden variables are assigned values when tube starts:
            S: ' ' # Its value is a space char and can't be overridden
            TUBE_HOME: <tube-running-startup-location-path>

        Then you can reference any variable value via {var-name} in your tube 
        command arguments. eg:
            - PATH: {root_folder}
            # Go to tube home directory:
            - PATH: {TUBE_HOME}
            - COMMAND: ls {cmd_parameters}
            # The below {s:10} will be replaced by 10 space chars 
            - WRITE_LINE_IN_FILE: -f file -v {s:10}any line content here               
             
        The below commands will update the tube variables:
            - GET_XML_TAG_TEXT => xpath will be the variable name
            - GET_FILE_KEY_VALUE => key will be the variable name
            - COUNT => variable parameter will be stored into tube variables
            - SET_VARIABLE => update tube variable by name value
            - CHECK_CHAR_EXISTS => Result will be stored into tube variable
             
        ** Note: If variable was updated from console inputs, then it will become readonly. 
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

    Command Tube is a tool that can run a group of sequenced commands. You can get a full
    list of supportted tube commands from readme document.
    Using these commands you can easily build your own tube to do tasks like:
    Refresh Development Environment, Daily Run Test Cases etc.
    It's more user friendly and eaiser to use than PowerShell.

## How to run Command Tube    

    Command Tube is a Python 3 script. The most important two arguments 
    for Command Tube are '--yaml' and '--datetime'.    
    All the tube configurations are maintained by a YAML file, 
    using '--yaml file' you can specify the tube configurations. 
    From the 'tube.template.yaml' (tube help tempalte could output it) you could view it.
    Use '--datetime' argument you could set the execution time, 
    you could also run it at once by parameter '-f' or '-i'.
    For more information about input arguments please use following command 
    from your terminal (Needs Python >= 3.6):
        >>> python command-tube.py -h
    
    - Examples of running Command Tube with source code:
        1: Run at once and sent result via email: 
        >>> python command-tube.py -y tube.yaml -fe
        2: Run at 20:00 o'clock:
        >>> python command-tube.py -y tube.yaml -t20
        3: Run at every 6 o'clock for 100 days: 
        >>> python command-tube.py -y tube.yaml -t n6 -l 24 -times 100
        4: Run 10 times for every 5 minutes start from 10:00:
        >>> python command-tube.py -y tube.yaml -t t10 -l 5m -times 10
        5: Run tube at 9:00 AM Feb 1, 2022:
        >>> python command-tube.py -y tube.yaml -t '02/01/22 09:00:00'
        6: Find command syntax which name contains 'file' keyword:
        >>> python command-tube.py help file
    
        ** Find tube running result from tube.yaml.log file by default 

    - Binary Mode        
        Following below steps you can use it in binary mode:
        1. Download 'tube' for MacOS or 'tube.exe' for Windows from github homepage
        3. Using it from your terminal (Need exec right from MacOS):
        >>> tube -y tube.yaml -f
        
        Following below steps to build an executable package:
        1. Get source code from github: https://github.com/michael-hll/command-tube.git
        2. From terminal goto source code root directory
        3. Run below command to build the package:
           >>> python3 command-tube.py -y package-mac.yaml -f
        4. Run tube version command to verify it's built successfully:
           >>> ./tube --version 
    
## General Arguments & Tube Variables
    - General Arguments
        Description: All tube commands support additional --redo, --continue, 
                 --key and --if paramters. It could make your tube realize
                 more complex flow.         
%s
%s
%s
%s
%s
                '''
                help_all = help_all % (help_title, help_continue, help_redo, help_if, help_key, help_var)
                
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
    - IMPORT_TUBE: sub-tube.yaml
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
                # get the second argument value
                if len(args.help) == 2:
                    command_name = args.help[1]
                
                # check if help readme
                is_for_readme = False
                if command_name and command_name.upper() == 'README':
                    is_for_readme = True
                    
                # Prepare examples of each command
                command_examples = []
                command_examples.append('## Usage of Each Command:')
                #command_examples.append(Storage.I.C_STATUS_LINE + Storage.I.C_STATUS_LINE)
                keys = [k for k in Storage.I.TUBE_ARGS_CONFIG.keys()]
                keys.sort()                
                for index, key in enumerate(keys):
                    if is_for_readme:
                        command_examples.append('### %s: %s' % (str(index+1), key))
                        command_examples.append('<pre>%s\n' % TubeCommand.get_command_description(key, Storage.I.TUBE_ARGS_CONFIG)) 
                    else:
                        command_examples.append('[%s]: %s' % (str(index+1), key))                        
                        command_examples.append('%s\n' % TubeCommand.get_command_description(key, Storage.I.TUBE_ARGS_CONFIG)) 
                    
                    command_examples.append('%s' % TubeCommand.get_command_syntax(key, Storage.I.TUBE_ARGS_CONFIG)) 
                    command_examples.append('%s' % TubeCommand.get_command_parameters(key, Storage.I.TUBE_ARGS_CONFIG))
                    
                    if command_name == '' or command_name.upper() != 'README':
                        command_examples.append('[Support from version: %s]' % Storage.I.TUBE_ARGS_CONFIG[key][Storage.I.C_SUPPORT_FROM_VERSION])
                        command_examples.append(Storage.I.C_STATUS_LINE + Storage.I.C_STATUS_LINE)
                    else:
                        command_examples.append('Support from version: %s</pre>' % Storage.I.TUBE_ARGS_CONFIG[key][Storage.I.C_SUPPORT_FROM_VERSION])                    
                        
                # End of prepare examples of each command  
                
                found_match = False
                if command_name == '' or command_name.upper() == 'ALL':
                    # print all help
                    tprint(help_all)
                    for eg in command_examples:
                        tprint(eg)  
                    tprint(add_notes)                         
                    sys.exit()
                elif command_name.upper() == 'COMMANDS':
                    for eg in command_examples:
                        tprint(eg)
                    sys.exit()
                elif command_name.upper() == 'TEMPLATE':
                    # print template and write it to a file
                    found_match = True
                    try:    
                        file = 'tube.template.yaml'
                        with open(file, 'w') as f:
                            f.write(template)
                        tprint(template)
                        tprint('# ' + file + ' is generated.')
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
                        tprint(file + ' is generated.')
                    except Exception as e:
                        tprint('Generated readme exception: ' + str(e), type=Storage.I.C_PRINT_TYPE_ERROR) 
                elif command_name.upper() == 'VARS':
                    # print all tube variables
                    found_match = True
                    if not args.yaml_config:
                        tprint('-y/--yaml aragument is not passed.', type=Storage.I.C_PRINT_TYPE_WARNING)
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
                                if line.startswith(Storage.I.C_VARIABLES):    
                                    var_start = True
                                    continue
                                if var_start == True and line.startswith(' '):
                                    # inorder to print var name/value in different color
                                    if ':' in line:
                                        line = line.strip().replace('\n', '')
                                        i = line.index(':')
                                        var_name = line[:i+1]
                                        var_value = line[i+1:]
                                        tprint(color(var_name, fore=Storage.I.C_PRINT_COLOR_BLUE, style=Storage.I.C_PRINT_COLOR_STYLE) + var_value)
                                    continue
                                elif var_start == True and not line.startswith(' '):
                                    break
                            # print default tube variables
                            tprint(color('TUBE_HOME: ', fore=Storage.I.C_PRINT_COLOR_BLUE, style=Storage.I.C_PRINT_COLOR_STYLE) + Storage.I.C_CURR_DIR)                                                        
                            tprint(color('S: ' + '\' \'' + ' # S is a readonly tube variable and it holds a space character.', fore=Storage.I.C_PRINT_COLOR_GREY, style=Storage.I.C_PRINT_COLOR_STYLE))
                        sys.exit()
                    except Exception as e:
                        tprint('Read variables from yaml file errors:' + str(e), type=Storage.I.C_PRINT_TYPE_ERROR)
                        sys.exit()
                elif command_name.upper() == 'CONTINUE':
                    print(help_continue)
                    sys.exit()
                elif command_name.upper() == 'REDO':
                    print(help_redo)
                    sys.exit()
                elif command_name.upper() == 'IF':
                    print(help_if)
                    sys.exit()
                elif command_name.upper() == 'KEY':
                    print(help_key)
                    sys.exit()
                elif command_name.upper() == 'VARIABLE':
                    print(help_var)
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
                        if command_name.upper() in key:
                            found_match = True        
                            index += 1        
                            tprint('[%s]: %s' % (str(index),key), tcolor=Storage.I.C_PRINT_COLOR_YELLOW)
                            tprint(TubeCommand.get_command_description(key, Storage.I.TUBE_ARGS_CONFIG) + '\n')
                            tprint(TubeCommand.get_command_syntax(key, Storage.I.TUBE_ARGS_CONFIG))                   
                            tprint(TubeCommand.get_command_parameters(key, Storage.I.TUBE_ARGS_CONFIG))
                            tprint('[Support from version: %s]' % Storage.I.TUBE_ARGS_CONFIG[key][Storage.I.C_SUPPORT_FROM_VERSION])                            
                            tprint(Storage.I.C_STATUS_LINE)
                    if found_match == True:
                        tprint(add_notes)
                # found nothing match from help system
                # then raise error
                if found_match == False:                    
                    tprint('The command: %s doesnot found matched.' % (command_name), type=Storage.I.C_PRINT_TYPE_WARNING)
                    tprint(Storage.I.C_HELP)
                
            else:
                # help arguments count is not correct or not equal to HELP
                tprint(Storage.I.C_HELP)
                tprint('You entered value for help system: ' + str(args.help), tcolor=Storage.I.C_PRINT_COLOR_YELLOW)

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
            
def job_start(tube):
    current_command = None
    current_command_type = None
    pre_command: TubeCommand = None
    ssh = None
    
    # Update TUBE_HOME
    StorageUtility.update_key_value_dict(Storage.I.C_TUBE_HOME, Storage.I.C_CURR_DIR)
    
    if Storage.I.RUN_MODE == Storage.I.C_RUN_MODE_DEBUG:
        tprint('Current directory is: %s' % (Storage.I.C_CURR_DIR), type=Storage.I.C_PRINT_TYPE_DEBUG)

    try:
        # print job start initials into the log
        init_log_file()
        
        # revert tube command list to initial status
        # the new command list Storage.I.TUBE_RUN will be used in each loop
        Storage.I.TUBE_RUN = convert_tube_to_new(tube, True)
        
        command: TubeCommand
        for index, command in enumerate(Storage.I.TUBE_RUN):
            current_command = command.content
            current_command_type = command.cmd_type   
            command.index = index + 1         

            # initial log instance
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
            if pre_command != None and \
              (pre_command.log.status == Storage.I.C_FAILED and pre_command.is_failed_continue == False):               
                log.status = Storage.I.C_SKIPPED
                Storage.I.LOGS.append(log)
                # check if report tube command status
                command.self_report_progress()
                # continue with next loop item                
                continue
            
            # reset general arguments
            command.reset_general_arguments()
            
            # skip if_run == False cases
            if command.if_run == False:
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
                        
            # Log current running step
            running_command = ' >>> %s'
            msg = datetime.now().strftime(Storage.I.C_DATETIME_FORMAT) + running_command % command.get_formatted_type() + ': ' + \
                  str(command.get_formatted_content())
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
            tprint(msg, tcolor=Storage.I.C_PRINT_COLOR_YELLOW, type=Storage.I.C_PRINT_TYPE_INFO)

            # --------------------------------------------------------
            # Begin to run each tube command based on its command type
            # --------------------------------------------------------
            if current_command_type == Storage.I.C_LINUX_COMMAND:
                log.start_datetime = datetime.now()                

                # Check if we have a valid ssh connection
                if ssh == None:
                    msg = 'Please check your provide server information, ssh failed to connect to your server.'
                    tprint(msg, type=Storage.I.C_PRINT_TYPE_ERROR)
                    write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
                    log.end_datetime = datetime.now()
                    log.add_error(msg)
                    log.status = Storage.I.C_FAILED
                    Storage.I.LOGS.append(log)
                    pre_command = command
                    # check if report tube command status
                    command.self_report_progress()
                    continue   
                
                # Check Linux Server Disk Space, only checking on the first Linux Command
                check_disk_space(ssh)  
                
                # Check command
                parser = command.tube_argument_parser
                args, _ = parser.parse_known_args(command.content.split())
                                
                # replace placeholders
                command.content = TubeCommand.format_placeholders(command.content) 
                
                # check if log detial
                if args.is_log_detail:
                    command.content = command.content.replace('--log-detail', '').strip()

                # Execute any linux command
                Storage.I.GOTO_HOST_ROOT = 'cd %s;' % Storage.I.CURR_HOST_ROOT # update root path    
                _ , stdout, stderr = ssh.exec_command(Storage.I.CURR_HOST_PROFILE + Storage.I.GOTO_HOST_ROOT + command.content)                    
                
                # print linux command outputs
                while True:
                    line = stdout.readline()
                    if not line:
                        break
                    line = line.replace('\n', '')                    
                    tprint(line)
                    # log details to tube log file
                    if args.is_log_detail:
                        lines = line.split('\r')
                        if len(line) > 0 and len(lines) > 0:
                            # if the line contains multiple lines
                            # then we only output the last line
                            line = lines[len(lines) - 1]
                        write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', line)    
                log.end_datetime = datetime.now()
                log.status = Storage.I.C_SUCCESSFUL

                # print errors if there are any
                return_code = stdout.channel.recv_exit_status()
                errors = stderr.readlines()
                if return_code != 0:
                    log.status = Storage.I.C_FAILED
                    for error in errors:
                        tprint(error.replace('\n',''), type=Storage.I.C_PRINT_TYPE_ERROR)    
                        log.add_error(error.replace('\n',''))

            elif current_command_type == Storage.I.C_PATH:
                try:
                    log.start_datetime = datetime.now()
                    # replace placeholders
                    command.content = TubeCommand.format_placeholders(command.content) 
                    result = os.chdir(command.content)
                    log.status = Storage.I.C_SUCCESSFUL
                    log.end_datetime = datetime.now()
                except Exception as e:
                    log.status = Storage.I.C_FAILED
                    tprint(str(e), type=Storage.I.C_PRINT_TYPE_ERROR)                    
                    log.add_error(str(e))
                    log.end_datetime = datetime.now()
            
            elif current_command_type == Storage.I.C_PAUSE:
                try:                        
                    log.start_datetime = datetime.now()
                    command.content = TubeCommand.format_placeholders(command.content)
                    pasued_mins = float(command.content)
                    tprint('Command Tube is paused for ' + str(pasued_mins) + ' minutes.', type=Storage.I.C_PRINT_TYPE_INFO)
                    time.sleep(60 * pasued_mins)
                    log.status = Storage.I.C_SUCCESSFUL
                    log.end_datetime = datetime.now()
                except Exception as e:
                    log.status = Storage.I.C_FAILED
                    tprint(str(e), type=Storage.I.C_PRINT_TYPE_ERROR)
                    log.add_error(str(e))
                    log.end_datetime = datetime.now()

            elif current_command_type == Storage.I.C_COMMAND:
                try:
                    # replace placeholders
                    command.content = TubeCommand.format_placeholders(command.content) 
                    command_array = shlex.split(command.content, posix=False)
                    log.start_datetime = datetime.now()
                    result = None
                    if os.name.startswith('nt'):
                        result = subprocess.Popen(command_array, text=True, shell=True,stdout=sys.stdout,stderr=subprocess.PIPE) 
                    else:
                        result = subprocess.Popen(command_array, text=True, stdout=sys.stdout, stderr=subprocess.PIPE)

                    # terminate the process and get running result 
                    _, error = result.communicate()  
                    if error:
                        # TODO: it seems pyinstaller has a bug, output the result to the stderr
                        if 'PyInstaller' in command.content:
                            tprint(error, type=Storage.I.C_PRINT_TYPE_WARNING)
                        else:
                            tprint(error, type=Storage.I.C_PRINT_TYPE_ERROR)
                    
                    log.end_datetime = datetime.now()
                    if result.returncode != 0:  
                        log.status = Storage.I.C_FAILED 
                        log.add_error(error)                            
                    else:
                        log.status = Storage.I.C_SUCCESSFUL                                                     
                except Exception as e:
                    log.status = Storage.I.C_FAILED
                    tprint(str(e), type=Storage.I.C_PRINT_TYPE_ERROR)
                    log.add_error(str(e))
                    log.end_datetime = datetime.now()

            elif current_command_type == Storage.I.C_GET_XML_TAG_TEXT:
                try:
                    log.start_datetime = datetime.now()                        
                    returns = command.get_xml_tag_text()                      
                    if returns != None and len(returns[0]) > 0:
                        StorageUtility.update_key_value_dict(returns[2], returns[0], command)
                        command.results.append(returns[0])
                        log.status = Storage.I.C_SUCCESSFUL
                        log.end_datetime = datetime.now()
                    else:
                        log.status = Storage.I.C_FAILED
                        log.end_datetime = datetime.now()
                        msg = 'xml tag has no text value.'
                        log.add_error(msg)
                except Exception as e:
                    tprint(str(e), type=Storage.I.C_PRINT_TYPE_ERROR)
                    log.add_error(str(e))
                    log.status = Storage.I.C_FAILED
                    log.end_datetime = datetime.now() 

            elif current_command_type == Storage.I.C_SET_XML_TAG_TEXT:
                try:
                    log.start_datetime = datetime.now()                        
                    udpate_success = command.set_xml_tag_text()  
                    if udpate_success == True:                      
                        log.status = Storage.I.C_SUCCESSFUL
                    else:
                        log.status = Storage.I.C_FAILED
                    log.end_datetime = datetime.now()
                except Exception as e:
                    tprint(str(e), type=Storage.I.C_PRINT_TYPE_ERROR)
                    log.add_error(str(e))
                    log.status = Storage.I.C_FAILED
                    log.end_datetime = datetime.now()
            
            elif current_command_type == Storage.I.C_SET_FILE_KEY_VALUE:
                try:
                    log.start_datetime = datetime.now()                        
                    set_value_success = command.set_file_key_value()  
                    if set_value_success == True:                      
                        log.status = Storage.I.C_SUCCESSFUL
                    else:
                        log.status = Storage.I.C_FAILED
                    log.end_datetime = datetime.now()
                except Exception as e:
                    tprint(str(e), type=Storage.I.C_PRINT_TYPE_ERROR)
                    log.add_error(str(e))
                    log.status = Storage.I.C_FAILED
                    log.end_datetime = datetime.now()                                                                     

            elif current_command_type == Storage.I.C_WRITE_LINE_IN_FILE:
                try:
                    log.start_datetime = datetime.now()                        
                    set_value_success = command.write_line_in_file()  
                    if set_value_success == True:                      
                        log.status = Storage.I.C_SUCCESSFUL
                    else:
                        log.status = Storage.I.C_FAILED
                    log.end_datetime = datetime.now()
                except Exception as e:
                    tprint(str(e), type=Storage.I.C_PRINT_TYPE_ERROR)
                    log.add_error(str(e))
                    log.status = Storage.I.C_FAILED
                    log.end_datetime = datetime.now()

            elif current_command_type == Storage.I.C_DELETE_LINE_IN_FILE:
                try:
                    log.start_datetime = datetime.now()                        
                    set_value_success = command.delete_line_in_file()  
                    if set_value_success == True:                      
                        log.status = Storage.I.C_SUCCESSFUL
                    else:
                        log.status = Storage.I.C_FAILED
                    log.end_datetime = datetime.now()
                except Exception as e:
                    tprint(str(e), type=Storage.I.C_PRINT_TYPE_ERROR)
                    log.add_error(str(e))
                    log.status = Storage.I.C_FAILED
                    log.end_datetime = datetime.now()

            elif current_command_type == Storage.I.C_TAIL_FILE:
                try:
                    log.start_datetime = datetime.now()
                    results = command.tail_file()                    
                    tail_lines = results[0]
                    file = results[1]
                    lines_count = results[2]
                    keywords = results[3]
                    if keywords == None:
                        keywords = ''
                    if len(tail_lines) > 0:
                        header = Storage.I.C_TAIL_LINES_HEADER + str(lines_count) + ' LINES FROM FILE [KEYWORDS: ' + keywords + ' ] => '
                        Storage.I.FILE_TAIL_LINES.append(header + file)
                    for line in tail_lines:
                        Storage.I.FILE_TAIL_LINES.append(line)
                    log.status = Storage.I.C_SUCCESSFUL
                    log.end_datetime = datetime.now()
                except Exception as e:
                    tprint(str(e), type=Storage.I.C_PRINT_TYPE_ERROR)
                    log.add_error(str(e))
                    log.status = Storage.I.C_FAILED
                    log.end_datetime = datetime.now()
            
            elif current_command_type == Storage.I.C_CONNECT:
                try:
                    log.start_datetime = datetime.now()
                    # replace placeholders
                    command.content = TubeCommand.format_placeholders(command.content) 
                    host_name = command.content
                    host: Host = None
                    
                    # check if connect host name exists from configruations
                    host = StorageUtility.get_host(host=host_name, name=host_name)
                    if host != None:  
                        if host.is_connected:
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
                    
                    # update command status and datetime
                    if host.is_connected == True:
                        log.status = Storage.I.C_SUCCESSFUL
                    else:
                        log.status = Storage.I.C_FAILED
                        log.add_error('Please check your servers configurations.')
                        if host != None:
                            for error in host.errors:
                                log.add_error(error)                        
                    log.end_datetime = datetime.now()               
                    
                except Exception as e:
                    ssh = None
                    tprint(str(e), type=Storage.I.C_PRINT_TYPE_ERROR)
                    log.add_error(str(e))
                    log.status = Storage.I.C_FAILED
                    log.end_datetime = datetime.now()
            
            elif current_command_type == Storage.I.C_REPORT_PROGRESS:
                try:                        
                    log.start_datetime = datetime.now()   
                    command.log.status = Storage.I.C_SUCCESSFUL                
                    tprint('Command Tube is reporting progress via e-mail settings... ', type=Storage.I.C_PRINT_TYPE_INFO)
                    # replace placeholders
                    command.content = TubeCommand.format_placeholders(command.content) 
                    result = command.report_progress(Storage.I.TUBE_RUN)
                    if result == True:
                        log.status = Storage.I.C_SUCCESSFUL
                    else:
                        log.status = Storage.I.C_FAILED
                    log.end_datetime = datetime.now()
                except Exception as e:
                    tprint(str(e), type=Storage.I.C_PRINT_TYPE_ERROR)
                    log.add_error(str(e))
                    log.end_datetime = datetime.now()                    
            
            elif current_command_type == Storage.I.C_GET_FILE_KEY_VALUE:
                try:
                    log.start_datetime = datetime.now()
                    log.status = Storage.I.C_FAILED
                    result, values = command.get_file_key_value()
                    if result == True:
                        log.status = Storage.I.C_SUCCESSFUL
                        for item in values:
                            command.results.append(item)
                    log.end_datetime = datetime.now()                    
                except Exception as e:
                    log.status = Storage.I.C_FAILED
                    tprint(str(e), type=Storage.I.C_PRINT_TYPE_ERROR)
                    log.add_error(str(e))
                    log.end_datetime = datetime.now() 
            
            elif current_command_type == Storage.I.C_EMAIL:
                try:
                    log.start_datetime = datetime.now()
                    log.status = Storage.I.C_FAILED
                    result = command.send_email_via_command()
                    if result == True:
                        log.status = Storage.I.C_SUCCESSFUL
                    log.end_datetime = datetime.now()                    
                except Exception as e:
                    log.status = Storage.I.C_FAILED
                    tprint(str(e), type=Storage.I.C_PRINT_TYPE_ERROR)
                    log.add_error(str(e))
                    log.end_datetime = datetime.now() 
            
            elif current_command_type == Storage.I.C_IMPORT_TUBE:
                try:
                    log.start_datetime = datetime.now()
                    log.status = Storage.I.C_FAILED
                    result = command.import_tube(general_command_parser)
                    if result == True:
                        log.status = Storage.I.C_SUCCESSFUL
                    log.end_datetime = datetime.now()                    
                except Exception as e:
                    log.status = Storage.I.C_FAILED
                    tprint(str(e), type=Storage.I.C_PRINT_TYPE_ERROR)
                    log.add_error(str(e))
                    log.end_datetime = datetime.now()
            
            elif current_command_type == Storage.I.C_COUNT:
                try:
                    log.start_datetime = datetime.now()
                    log.status = Storage.I.C_SUCCESSFUL
                    result = command.count()
                    if result == False:
                        log.status = Storage.I.C_FAILED
                    log.end_datetime = datetime.now()                    
                except Exception as e:
                    log.status = Storage.I.C_FAILED
                    tprint(str(e), type=Storage.I.C_PRINT_TYPE_ERROR)
                    log.add_error(str(e))
                    log.end_datetime = datetime.now()
            
            elif current_command_type == Storage.I.C_SET_VARIABLE:
                try:
                    log.start_datetime = datetime.now()
                    log.status = Storage.I.C_SUCCESSFUL
                    result = command.set_variable()
                    if result == False:
                        log.status = Storage.I.C_SKIPPED
                    log.end_datetime = datetime.now()                    
                except Exception as e:
                    log.status = Storage.I.C_FAILED
                    tprint(str(e), type=Storage.I.C_PRINT_TYPE_ERROR)
                    log.add_error(str(e))
                    log.end_datetime = datetime.now()
            
            elif current_command_type == Storage.I.C_SFTP_GET or \
                 current_command_type == Storage.I.C_SFTP_PUT:
                # Check if we have a valid ssh connection
                if ssh == None:
                    msg = 'Please check your provide server information, ssh failed to connect to your server.'
                    tprint(msg, type=Storage.I.C_PRINT_TYPE_ERROR)
                    write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
                    log.end_datetime = datetime.now()
                    log.add_error(msg)
                    log.status = Storage.I.C_FAILED
                    Storage.I.LOGS.append(log)
                    pre_command = command
                    continue 
                
                try:
                    log.start_datetime = datetime.now()
                    log.status = Storage.I.C_FAILED
                    command.sftp_get_put(ssh)
                    log.status = Storage.I.C_SUCCESSFUL
                    log.end_datetime = datetime.now()                    
                except Exception as e:
                    log.status = Storage.I.C_FAILED
                    tprint(str(e), type=Storage.I.C_PRINT_TYPE_ERROR)
                    log.add_error(str(e))
                    log.end_datetime = datetime.now()
            
            elif current_command_type == Storage.I.C_CHECK_CHAR_EXISTS:
                try:
                    log.start_datetime = datetime.now()
                    log.status = Storage.I.C_FAILED
                    command.check_char_exists()
                    log.status = Storage.I.C_SUCCESSFUL
                    log.end_datetime = datetime.now()                    
                except Exception as e:
                    log.status = Storage.I.C_FAILED
                    tprint(str(e), type=Storage.I.C_PRINT_TYPE_ERROR)
                    log.add_error(str(e))
                    log.end_datetime = datetime.now()  
            
            elif current_command_type == Storage.I.C_REPLACE_CHAR:
                try:
                    log.start_datetime = datetime.now()
                    log.status = Storage.I.C_FAILED
                    replaced_count = command.replace_char()
                    msg = 'There are \'%s\' items replaced.' % replaced_count
                    tprint(msg, type=Storage.I.C_PRINT_TYPE_INFO)
                    write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
                    log.status = Storage.I.C_SUCCESSFUL
                    log.end_datetime = datetime.now()                    
                except Exception as e:
                    log.status = Storage.I.C_FAILED
                    tprint(str(e), type=Storage.I.C_PRINT_TYPE_ERROR)
                    log.add_error(str(e))
                    log.end_datetime = datetime.now()   
            
            elif current_command_type == Storage.I.C_PRINT_VARIABLES:
                try:
                    log.start_datetime = datetime.now()
                    log.status = Storage.I.C_FAILED
                    command.print_variables()
                    log.status = Storage.I.C_SUCCESSFUL
                    log.end_datetime = datetime.now()                    
                except Exception as e:
                    log.status = Storage.I.C_FAILED
                    tprint(str(e), type=Storage.I.C_PRINT_TYPE_ERROR)
                    log.add_error(str(e))
                    log.end_datetime = datetime.now() 
                        
            # not supported command found then log errors and continue next          
            else:
                log.status = Storage.I.C_FAILED 
                command.is_failed_continue = True
                pre_command = command
                msg = 'Not supported tube command found: ' + log.command.cmd_type
                tprint(msg, type=Storage.I.C_PRINT_TYPE_ERROR)
                log.add_error(msg)
                Storage.I.LOGS.append(log)
                continue
                
            # support --redo arguments logic
            if command.is_failed_redo == True and log.status == Storage.I.C_FAILED:
                TubeCommandUtility.insert_failed_redo_commands(Storage.I.TUBE_RUN, index, command)
            elif command.is_failed_redo == True and log.status == Storage.I.C_SUCCESSFUL and \
                 command.redo_steps > 0:
                TubeCommandUtility.insert_success_redo_commands(Storage.I.TUBE_RUN, index, command)                
                    
            # check continue conditional skip steps at the end of each command
            if command.is_failed_continue:
                TubeCommandUtility.reset_command_skip(Storage.I.TUBE_RUN, command)        
            
            # if command failed and errors then output to log
            if log.status == Storage.I.C_FAILED:
                log.write_errors_to_log()
                
            # check if report tube command status
            command.self_report_progress()
                                
            # Finnally append the command log
            Storage.I.LOGS.append(log)
            pre_command = command            
    except Exception as e:
        msg = 'When execute command type: %s, command: %s, exception: %s' % (current_command_type, current_command, str(e))
        tprint(msg, type=Storage.I.C_PRINT_TYPE_ERROR)  
        write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)        
    finally:
        try:
            os.chdir(Storage.I.C_CURR_DIR) # changing dir back if 'PATH' command changed current dir
        except Exception as e:
            write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', str(e)) 

        # close all connections         
        disconect_all_hosts(Storage.I.HOSTS)     
        ssh = None  
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
parser = ArgumentParser(allow_abbrev=False, formatter_class=RawTextHelpFormatter)    
general_command_parser = ArgumentParser(allow_abbrev=False)   

# init Command-Tube arguments and help document
init_arguments()   

# parse user inputs arguments
try:
    args = parser.parse_args()
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
print_tube_command_help(parser)

# ------------------------------------------------------------
# Check log file name
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
        read_run_mode()
    else:
        msg = "YAML file doesn't exist: " + Storage.I.TUBE_YAML_FILE
        tprint(msg, type=Storage.I.C_PRINT_TYPE_ERROR)
        # Log start
        write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', Storage.I.C_LOG_HEADER + datetime.now().strftime(Storage.I.C_DATETIME_FORMAT))
        write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
        sys.exit()         
else:
    msg = '-y or --yaml parameter is missing. \
          \nUse \'-h\' argument to view the usage of all the parameters.'
    tprint(msg, type=Storage.I.C_PRINT_TYPE_ERROR)
    # Log start
    write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', Storage.I.C_LOG_HEADER + datetime.now().strftime(Storage.I.C_DATETIME_FORMAT))
    write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
    sys.exit()  
# --------End of Check Log Files -----------------------------

# ------------------------------------------------
# Read configuration file & user arguments content
# Overrite input parameters from config file
# ------------------------------------------------
try:
    data = None
    if(Storage.I.TUBE_YAML_FILE and path.exists(Storage.I.TUBE_YAML_FILE)):
        with open(Storage.I.TUBE_YAML_FILE, 'r') as f:
            data = Utility.safe_load_with_upper_key(f) 
    
    # check if given configuration file is empty        
    if not data:
        msg = 'The content of given config file is empty: %s'
        msg = msg % Storage.I.TUBE_YAML_FILE
        tprint(msg, type=Storage.I.C_PRINT_TYPE_ERROR)
        write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
        sys.exit()

    # tprint(json.dumps(data, indent=4))   
    if Storage.I.C_TUBE in data.keys(): 
        Storage.I.TUBE = data[Storage.I.C_TUBE]
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

    # ------------------------------------
    # Begin to deal with all input parameters
    # ------------------------------------ 
        
    # Get servers to hosts
    StorageUtility.read_hosts(Storage.I.SERVERS)
    
    # Read variables 
    StorageUtility.read_variables(Storage.I.VARIABLES)
    
    # Read variables from console
    StorageUtility.read_variables_from_console(args.variables)

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
        
    # checking tube command syntax
    Storage.I.TUBE_RUN = convert_tube_to_new(Storage.I.TUBE)
    has_error, _ = StorageUtility.check_tube_command_arguments(Storage.I.TUBE_RUN, general_command_parser)
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
    msg = 'Command Tube process parameters error: ' + str(e)
    tprint(msg, type=Storage.I.C_PRINT_TYPE_ERROR)
    write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
    sys.exit()
# ----- END Of Reading Configuration --------- 

# Print input parameters and ask user to confirm
if not Storage.I.IS_FORCE_RUN:
    print_input_parameters()

if not confirm('Are those parameters correct [Y/N]? '):
    msg = 'user quit.'
    write_line_to_log(Storage.I.TUBE_LOG_FILE, 'a+', msg)
    sys.exit() 

# ----- Validations on User Inputs ------
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
            Storage.I.FILE_TAIL_LINES = []
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
        job_start(Storage.I.TUBE) 
        
        # stop matrix mode if it's started
        if Storage.I.IS_MATRIX_MODE:
            stop_matrix_terminal()
            
        print_logs(Storage.I.LOGS)
        write_logs_to_file(Storage.I.LOGS)        
        if Storage.I.IS_SENT_EMAIL:
            prepare_emails_content_and_sent(Storage.I.LOGS)
        output_disk_space_check()
        output_tail_lines(Storage.I.FILE_TAIL_LINES)
        
        # In loop mode, we need to update the next run time
        # do this time updates just on each iteration is fully done
        if Storage.I.IS_LOOP == True:
            Storage.I.EXEC_DATETIME += timedelta(hours=Storage.I.NEXT_REFRESH)       
#--------End of the LOOP ----------------------- 