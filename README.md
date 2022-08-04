
-------------------------------           
# Welcome to Command Tube
## version: 2.0.2 Beta
-------------------------------
                                      
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
        Following below steps you can use it in binary mode
        1. Download 'tube' for MacOS or 'tube.exe' for Windows from github homepage
        3. Using it from your terminal (Need exec right from MacOS):
        >>> tube -y tube.yaml -f
    
## General Arguments & Tube Variables
    - General Arguments
        Description: All tube commands support additional --redo, --continue, 
                 --key and --if paramters. It could make your tube realize
                 more complex flow.         

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
                

        Redo: 
            Syntax: --redo [m]
            Description: 
                Without m parameter, if current command failed it  
                will be re-executed once.

                With m (m < 0) parameter, and current command failed, it will  
                redo commands from previous m steps.

                With m (m > 0) parameter, and current command success, it will
                redo this command for m times.
                

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
                

        Key:
            Syntax: --key
            Description:
                This flag can tell the tube which commands are the key commands. If there are
                key commands exist, only all of them run successfully, the tube result will be 
                marked as successfull. (If the command's --if condition is False, then --key
                will be skipped.)
                

    - Tube Variables            
        From tube YAML file, you can add tube variables under 'VARIABLES' property. 
        e.g.:       
        VARIABLES:  
            root_folder: C:\workspaces	runk
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
                
                
## Usage of Each Command:
### 1: CHECK_CHAR_EXISTS
<pre>Description: Check if given characters exists from a file. Result was updated into a tube variable.

Syntax: - CHECK_CHAR_EXISTS: -f|--file file -c|--char characters -r|--result result [--continue [m][n]] [--redo [m]] [--if run] [--key]
Parameters:
   -f/--file:   The file you want to check.
   -c/--char:   The characters you want to check.
   -r/--result: The tube variable name to store the checking result.

Support from version: 2.0.1</pre>
### 2: COMMAND
<pre>Description: Run any Windows/MacOS terminal command.

Syntax: - COMMAND: command [--continue [m][n]] [--redo [m]] [--if run] [--key]
Parameters:
   command:  Any command you want to run.

Support from version: 2.0.0</pre>
### 3: CONNECT
<pre>Description: You can use this command to switch your server connection.

Syntax: - CONNECT: host [--continue [m][n]] [--redo [m]] [--if run] [--key]
Parameters:
   host:  The Linux host name you want to connect using SSH.

Support from version: 2.0.0</pre>
### 4: COUNT
<pre>Description: Count file lines number (-f) or Count tube command number by status (-t).

Syntax: - COUNT: [-f|--file file] [-t|--tube tube] -v|--variable variable [-c|--current current_tube] [-s|--skip skip_count] [--continue [m][n]] [--redo [m]] [--if run] [--key]
Parameters:
   -f/--file:     The file you want to count line numbers.
   -t/--tube:     The tube status you want to count.
   -v/--variable: The tube variable name to store the count result.
   -c/--current:  If only count current tube. Default no.
   -s/--skip:     If skip COUNT command. Default no.

Support from version: 2.0.0</pre>
### 5: DELETE_LINE_IN_FILE
<pre>Description: Conditionally delete lines from a file.

Syntax: - DELETE_LINE_IN_FILE: -f|--file file [-b|--begins begins] [-c|--contains contains] [-e|--empty del_empty] [--continue [m][n]] [--redo [m]] [--if run] [--key]
Parameters:
   -f/--file:     The file you want to delete lines from.
   -b/--begins:   The line begins with character you want to delete.
   -c/--contains: The line contains with character you want to delete.
   -e/--empty:    A flag to tell if delete empty line. Default no.

Support from version: 2.0.0</pre>
### 6: EMAIL
<pre>Description: Sent Email to someone with given subject and content.

Syntax: - EMAIL: -t|--to to -s|--subject subject -b|--body body [--continue [m][n]] [--redo [m]] [--if run] [--key]
Parameters:
   -t/--to:      The sending email addresses.
   -s/--subject: The email title.
   -b/--body:    The email content. If it's text file name, then the content of the file will be as the email content.

Support from version: 2.0.0</pre>
### 7: GET_FILE_KEY_VALUE
<pre>Description: Read key values from key-value file.                                            
The key-value results will be stored into tube variables.

Syntax: - GET_FILE_KEY_VALUE: -f|--file file [-k|--keywords keywords] [--continue [m][n]] [--redo [m]] [--if run] [--key]
Parameters:
   -f/--file:     The file you want to get key-value from.
   -k/--keywords: Set the key you can get specific value of a given key.

Support from version: 2.0.0</pre>
### 8: GET_XML_TAG_TEXT
<pre>Description: Get XML file tag text value.                                            
The result will be stored into a tube variable and xpath will be used as the variable name.

Syntax: - GET_XML_TAG_TEXT: -f|--file file -x|--xpath xpath [--continue [m][n]] [--redo [m]] [--if run] [--key]
Parameters:
   -f/--file:  The XML file you want to get tag text.
   -x/--xpath: The xpath of the XML tag.

Support from version: 2.0.0</pre>
### 9: IMPORT_TUBE
<pre>Description: Import tube commands from a sub-tube file, servers, variables or emails can also be imported.

Syntax: - IMPORT_TUBE: file [--continue [m][n]] [--redo [m]] [--if run] [--key]
Parameters:
   file:  Sub tube file with YAML format.

Support from version: 2.0.0</pre>
### 10: LINUX_COMMAND
<pre>Description: Run a Linux command from the previous connected server.

Syntax: - LINUX_COMMAND: command [--continue [m][n]] [--redo [m]] [--if run] [--key]
Parameters:
   command:  Any Linux command you want to run.

Support from version: 2.0.0</pre>
### 11: PATH
<pre>Description: Go to specific directory.

Syntax: - PATH: directory [--continue [m][n]] [--redo [m]] [--if run] [--key]
Parameters:
   directory:  The directory you want to goto.

Support from version: 2.0.0</pre>
### 12: PAUSE
<pre>Description: Command Tube will pause with given minutes.

Syntax: - PAUSE: minutes [--continue [m][n]] [--redo [m]] [--if run] [--key]
Parameters:
   minutes:  The minutes you want to pause.

Support from version: 2.0.0</pre>
### 13: PRINT_VARS
<pre>Description: Print all tube variable values by given name for debugging purpose.

Syntax: - PRINT_VARS: -n|--name name [--continue [m][n]] [--redo [m]] [--if run] [--key]
Parameters:
   -n/--name: Tube variable name parameter (* means print all).

Support from version: 2.0.2</pre>
### 14: REPLACE_CHAR
<pre>Description: Replace file line content which contains/matches given value.

Syntax: - REPLACE_CHAR: -f|--file file -o|--oldvalue oldvalue -n|--newvalue newvalue [-c|--count count] [--continue [m][n]] [--redo [m]] [--if run] [--key]
Parameters:
   -f/--file:     The file you want to replace given characters.
   -o/--oldvalue: The oldvalue you want to replace (Support regular expressions).
   -n/--newvalue: The newvalue to replace.
   -c/--count:    The replaced times you want to set. Default no limitation.

Support from version: 2.0.1</pre>
### 15: REPORT_PROGRESS
<pre>Description: You can use this command to sent current progress via Email.

Syntax: - REPORT_PROGRESS: subject [--continue [m][n]] [--redo [m]] [--if run] [--key]
Parameters:
   subject:  The email subject/title you want to set.

Support from version: 2.0.0</pre>
### 16: SET_FILE_KEY_VALUE
<pre>Description: Update key-value file.

Syntax: - SET_FILE_KEY_VALUE: -f|--file file -k|--keywords keywords -v|--value value [--continue [m][n]] [--redo [m]] [--if run] [--key]
Parameters:
   -f/--file:     The file you want to update.
   -k/--keywords: The key in the left side of '='.
   -v/--value:    The value in the right side of '='.

Support from version: 2.0.0</pre>
### 17: SET_VARIABLE
<pre>Description: Set tube variable value.

Syntax: - SET_VARIABLE: -n|--name name -v|--value value [--continue [m][n]] [--redo [m]] [--if run] [--key]
Parameters:
   -n/--name:  The tube variable name you want to set.
   -v/--value: The tube variable value you want to set.

Support from version: 2.0.0</pre>
### 18: SET_XML_TAG_TEXT
<pre>Description: Update XML file tag text using xpath.

Syntax: - SET_XML_TAG_TEXT: -f|--file file -x|--xpath xpath -v|--value value [--continue [m][n]] [--redo [m]] [--if run] [--key]
Parameters:
   -f/--file:  The XML file you want tup set tag text.
   -x/--xpath: The xpath of the XML tag
   -v/--value: The new value of the tag.

Support from version: 2.0.0</pre>
### 19: SFTP_GET
<pre>Description: Using SSHClient to copy remote server file to local.                                            
When copy multiple files using *.* then localpath must be a directory.

Syntax: - SFTP_GET: -r|--remotepath remotepath -l|--localpath localpath [--continue [m][n]] [--redo [m]] [--if run] [--key]
Parameters:
   -r/--remotepath: The file full remotepath.
   -l/--localpath:  The file localpath.

Support from version: 2.0.1</pre>
### 20: SFTP_PUT
<pre>Description: Using SSHClient to put local file to remote server.                                            
When copy multiple files using *.* then remotepath must be a directory.

Syntax: - SFTP_PUT: -l|--localpath localpath -r|--remotepath remotepath [--continue [m][n]] [--redo [m]] [--if run] [--key]
Parameters:
   -l/--localpath:  The file localpath.
   -r/--remotepath: The file full remotepath.

Support from version: 2.0.1</pre>
### 21: TAIL_FILE
<pre>Description: Print/Log the last N lines of given file.

Syntax: - TAIL_FILE: -f|--file file -l|--lines lines [-k|--keywords keywords] [--continue [m][n]] [--redo [m]] [--if run] [--key]
Parameters:
   -f/--file:     The text file you want to tail.
   -l/--lines:    The lines count you want to output.
   -k/--keywords: Output file content only if it contains the given keywords.

Support from version: 2.0.0</pre>
### 22: WRITE_LINE_IN_FILE
<pre>Description: Write any characters into a file.                      
The written characters also could be one of them: '$NLB' (NEW_LINE_BEFORE), '$NLA' (NEW_LINE_AFTER),'$DL' (DELETE_LINE).                     
If you need more than two space characters in the value content, you can use {s:m} (m > 0) formular.                     
The 'm' means how many spaces you want to write.                     
eg: -v {s:5}hello => will be translated to 5 space chars plus hello: '     hello'

Syntax: - WRITE_LINE_IN_FILE: -f|--file file -v|--value value [-n|--number number] [-c|--contains contains] [--continue [m][n]] [--redo [m]] [--if run] [--key]
Parameters:
   -f/--file:     The file you want to update.
   -v/--value:    The character value you want to update in the file.
   -n/--number:   The line number you want to update.
   -c/--contains: Only update the line if it contains the given characters content.

Support from version: 2.0.0</pre>

## Tube File Samples 
### For samples tube file, please check templates folder.
<pre>
    Sample-refresh-dev.yaml
    Sample-conditional-build.yaml
</pre>
                