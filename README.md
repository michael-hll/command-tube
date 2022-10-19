
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
#### Alias: 
<pre>Description: Check if given characters exists from a file. Result was updated into a tube variable.

Syntax: - CHECK_CHAR_EXISTS: -f|--file file -c|--char characters -r|--result result [-u|--force] [-g|--global] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--note note]
Parameters:
   -f/--file:   The file you want to check.
   -c/--char:   The characters you want to check.
   -r/--result: The tube variable name to store the checking result.
   -u/--force:  Force update even the variable is readonly. Default no. [2.0.2]
   -g/--global: If update the variable in global tube variables. Default no. [2.0.2]

Support from version: 2.0.1</pre>
### 2: COMMAND
#### Alias: CMD
<pre>Description: Run any Windows/MacOS terminal command.

Syntax: - COMMAND: command [--no-shell] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--note note]
Parameters:
   command:      Any command you want to run.
   --no-shell:   Do not use 'Shell' to run the command. Default no. 
                 This is used for Mac/Linux OS. For Windows it will always use shell. [2.0.2]

Support from version: 2.0.0</pre>
### 3: CONNECT
#### Alias: 
<pre>Description: You can use this command to switch your server connection.

Syntax: - CONNECT: host [--continue [m][n]] [--redo [m]] [--if run] [--key] [--note note]
Parameters:
   host:  The Linux server host or name you want to connect using SSH protocal.

Support from version: 2.0.0</pre>
### 4: COUNT
#### Alias: 
<pre>Description: Count file lines number (-f) or Count tube command number by status (-t).

Syntax: - COUNT: [-f|--file file] [-t|--tube tube] -v|--variable variable [-c|--current] [-s|--skip] [-u|--force] [-g|--global] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--note note]
Parameters:
   -f/--file:     The file you want to count line numbers.
   -t/--tube:     The tube status you want to count.
   -v/--variable: The tube variable name to store the count result.
   -c/--current:  If only count current tube. Default no.
   -s/--skip:     If skip COUNT command. Default no.
   -u/--force:    Force update even the variable is readonly. Default no. [2.0.2]
   -g/--global:   If update the variable in global tube variables. Default no. [2.0.2]

Support from version: 2.0.0</pre>
### 5: DELETE_LINE_IN_FILE
#### Alias: DELETE_LINE
<pre>Description: Conditionally delete lines from a file.

Syntax: - DELETE_LINE_IN_FILE: -f|--file file [-n|--number number] [-b|--begins begins] [-c|--contains contains] [-e|--empty] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--note note]
Parameters:
   -f/--file:     The file you want to delete lines from.
   -n/--number:   The line number you want to delete. 1 is the first line, -1 is the last line. If the number is greater than file lines then return the last line.
   -b/--begins:   The line begins with character you want to delete.
   -c/--contains: The line contains with character you want to delete.
   -e/--empty:    A flag to tell if delete empty line. Default no.

Support from version: 2.0.0</pre>
### 6: DEL_VARIABLE
#### Alias: DEL_VAR
<pre>Description: Delete tube variables.

Syntax: - DEL_VARIABLE: -n|--name name [-g|--global] [-a|--all] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--note note]
Parameters:
   -n/--name:   The tube variable name you want to delete from current tube.
   -g/--global: With --global parameter you can delete it from current and its parent tubes.
   -a/--all:    With --all parameter you can delete it from all tubes.

Support from version: 2.0.2</pre>
### 7: DIR_CREATE
#### Alias: 
<pre>Description: Create a directory if it doesnot exist.

Syntax: - DIR_CREATE: -d|--dir directory [--continue [m][n]] [--redo [m]] [--if run] [--key] [--note note]
Parameters:
   -d/--dir:   The directory you want to check.

Support from version: 2.0.2</pre>
### 8: DIR_DELETE
#### Alias: 
<pre>Description: Delete a directory and its sub-directories.

Syntax: - DIR_DELETE: -d|--dir directory [-f|--force] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--note note]
Parameters:
   -d/--dir:   The directory you want to delete.
   -f/--force: Force delete if the director is not empty. Default no.

Support from version: 2.0.2</pre>
### 9: DIR_EXIST
#### Alias: 
<pre>Description: Check if a directory exists.

Syntax: - DIR_EXIST: -d|--dir directory -v|--variable variable [-u|--force] [-g|--global] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--note note]
Parameters:
   -d/--dir:      The directory you want to check.
   -v/--variable: The tube variable name to store the exist result. (True/False)
   -u/--force:    Force update even the variable is readonly. Default no.
   -g/--global:   If update the variable in global tube variables. Default no.

Support from version: 2.0.2</pre>
### 10: EMAIL
#### Alias: 
<pre>Description: Sent Email to someone with given subject and content.

Syntax: - EMAIL: -t|--to to -s|--subject subject -b|--body body [--continue [m][n]] [--redo [m]] [--if run] [--key] [--note note]
Parameters:
   -t/--to:      The sending email addresses.
   -s/--subject: The email title.
   -b/--body:    The email content. If it's text file name, then the content of the file will be as the email content.

Support from version: 2.0.0</pre>
### 11: FILE_APPEND
#### Alias: 
<pre>Description: Append the content to the last line of the given text file.

Syntax: - FILE_APPEND: -f|--file file -v|--value value [--continue [m][n]] [--redo [m]] [--if run] [--key] [--note note]
Parameters:
   -f/--file:  The text file name you want to append.
   -v/--value: The content you want to append to the text file.

Support from version: 2.0.2</pre>
### 12: FILE_COPY
#### Alias: 
<pre>Description: Copy any files to target.

Syntax: - FILE_COPY: -s|--src src -d|--dest dest [--continue [m][n]] [--redo [m]] [--if run] [--key] [--note note]
Parameters:
   -s/--src:  The source file name you want to copy.
   -d/--dest: The target file or folder

Support from version: 2.0.2</pre>
### 13: FILE_CREATE
#### Alias: 
<pre>Description: Create an empty file.

Syntax: - FILE_CREATE: -f|--file file [--continue [m][n]] [--redo [m]] [--if run] [--key] [--note note]
Parameters:
   -f/--file: The text file name you want to create.

Support from version: 2.0.2</pre>
### 14: FILE_DELETE
#### Alias: 
<pre>Description: Delete any files math the file name.

Syntax: - FILE_DELETE: -f|--file file [--continue [m][n]] [--redo [m]] [--if run] [--key] [--note note]
Parameters:
   -f/--file: The file name you want to delete.

Support from version: 2.0.2</pre>
### 15: FILE_EMPTY
#### Alias: 
<pre>Description: Clear an existing text file or create a new empty file.

Syntax: - FILE_EMPTY: -f|--file file [-c|--create] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--note note]
Parameters:
   -f/--file:   The text file name you want to empty.
   -c/--create: If the give file doesnot exist if create a new empty file. Default No.

Support from version: 2.0.2</pre>
### 16: FILE_EXIST
#### Alias: 
<pre>Description: Check if a file exists.

Syntax: - FILE_EXIST: -f|--file file -v|--variable variable [-u|--force] [-g|--global] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--note note]
Parameters:
   -f/--file:     The file name you want to check.
   -v/--variable: The tube variable name to store the exist result. (True/False)
   -u/--force:    Force update even the variable is readonly. Default no.
   -g/--global:   If update the variable in global tube variables. Default no.

Support from version: 2.0.2</pre>
### 17: FILE_MOVE
#### Alias: 
<pre>Description: Move any files to target.

Syntax: - FILE_MOVE: -s|--src src -d|--dest dest [--continue [m][n]] [--redo [m]] [--if run] [--key] [--note note]
Parameters:
   -s/--src:  The source file name you want to move.
   -d/--dest: The target file or folder

Support from version: 2.0.2</pre>
### 18: FILE_POP
#### Alias: 
<pre>Description: Pop the first line of the given text file. If there is no line there then store empty.

Syntax: - FILE_POP: -f|--file file [-v|--variable variable] [-u|--force] [-g|--global] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--note note]
Parameters:
   -f/--file:     The text file name you want to pop.
   -v/--variable: The tube variable name to store the line content result.
   -u/--force:    Force update even the variable is readonly. Default no.
   -g/--global:   If update the variable in global tube variables. Default no.

Support from version: 2.0.2</pre>
### 19: FILE_PUSH
#### Alias: 
<pre>Description: Push the content to the first line of the given text file.

Syntax: - FILE_PUSH: -f|--file file -v|--value value [--continue [m][n]] [--redo [m]] [--if run] [--key] [--note note]
Parameters:
   -f/--file:  The text file name you want to push.
   -v/--value: The content you want to push to the text file.

Support from version: 2.0.2</pre>
### 20: FILE_READ
#### Alias: 
<pre>Description: Read a file content to tube variable.

Syntax: - FILE_READ: -f|--file file -v|--variable variable [-u|--force] [-g|--global] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--note note]
Parameters:
   -f/--file:     The file name you want to read its whole content.
   -v/--variable: The tube variable name to store the read result.
   -u/--force:    Force update even the variable is readonly. Default no.
   -g/--global:   If update the variable in global tube variables. Default no.

Support from version: 2.0.2</pre>
### 21: GET_FILE_KEY_VALUE
#### Alias: GET_KEYS
<pre>Description: Read key values from key-value file.                                            
It also supports to read key-value from Yaml file with simple type: string, number.                                            
The key-value results will be stored into tube variables.

Syntax: - GET_FILE_KEY_VALUE: -f|--file file [-k|--keywords keywords] [-u|--force] [-g|--global] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--note note]
Parameters:
   -f/--file:     The file you want to get key-value from.
   -k/--keywords: Set the key you can get specific value of a given key.
   -u/--force:    Force update even the variable is readonly. Default no. [2.0.2]
   -g/--global:   If update the variable in global tube variables. Default no. [2.0.2]

Support from version: 2.0.0</pre>
### 22: GET_XML_TAG_TEXT
#### Alias: GET_XML_TAG
<pre>Description: Get XML file tag text value.                                            
The result will be stored into a tube variable and xpath will be used as the variable name.

Syntax: - GET_XML_TAG_TEXT: -f|--file file -x|--xpath xpath [-v|--variable variable] [-u|--force] [-g|--global] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--note note]
Parameters:
   -f/--file:     The XML file you want to get tag text.
   -x/--xpath:    The xpath of the XML tag.
   -v/--variable: The tube variable name to store the value. [2.0.2]
   -u/--force:    Force update even the variable is readonly. Default no. [2.0.2]
   -g/--global:   If update the variable in global tube variables. Default no. [2.0.2]

Support from version: 2.0.0</pre>
### 23: LINUX_COMMAND
#### Alias: LCMD, SSHCMD
<pre>Description: Run a Linux command from the previous connected server.

Syntax: - LINUX_COMMAND: command [--log-detail] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--note note]
Parameters:
   command:        Any Linux command you want to run.
   --log-detail:   Log command output to tube log file. Default no. [2.0.2]

Support from version: 2.0.0</pre>
### 24: LIST_DIRS
#### Alias: 
<pre>Description: Got all sub directories for the given directory, and save the result list to a text file.

Syntax: - LIST_DIRS: -d|--directory directory -r|--result file [-s|--sort sort] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--note note]
Parameters:
   -d/--directory: The directory you want to list its sub directories.
   -r/--result:    The text file to store the list result.
   -s/--sort:      It accepts 'asc' or 'desc' value for the sorting. Default is 'asc'.

Support from version: 2.0.2</pre>
### 25: LIST_FILES
#### Alias: 
<pre>Description: Get matched files list and save it to a text file.

Syntax: - LIST_FILES: -d|--directory directory -r|--result file [-s|--sort sort] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--note note]
Parameters:
   -d/--directory: The directory with file name matchings. If not provided then use default *.* to list all files. eg: <directory>/*.* or *.jpg
   -r/--result:    The text file to store the search result.
   -s/--sort:      Using '-s time|name|size [asc|desc]' to set the sort properties. Default uses the file modification time (time asc) to sort the result.

Support from version: 2.0.2</pre>
### 26: PATH
#### Alias: 
<pre>Description: Go to specific directory.

Syntax: - PATH: directory [--continue [m][n]] [--redo [m]] [--if run] [--key] [--note note]
Parameters:
   directory:  The directory you want to goto.

Support from version: 2.0.0</pre>
### 27: PAUSE
#### Alias: 
<pre>Description: Command Tube will pause with given minutes/seconds.

Syntax: - PAUSE: minutes [--continue [m][n]] [--redo [m]] [--if run] [--key] [--note note]
Parameters:
   minutes:  The minutes you want to pause. You can end it with 's' char to pause for xxx seconds.

Support from version: 2.0.0</pre>
### 28: PRINT_VARS
#### Alias: PRINT_VARS
<pre>Description: Print tube variable values for debugging purpose.

Syntax: - PRINT_VARS: name [--continue [m][n]] [--redo [m]] [--if run] [--key] [--note note]
Parameters:
   name:  The tube variable name. Provide value '*' can print all variable.

Support from version: 2.0.2</pre>
### 29: READ_LINE_IN_FILE
#### Alias: READ_LINE
<pre>Description: Read one line by given line number, and save the line content to tube variable.

Syntax: - READ_LINE_IN_FILE: -f|--file file -n|--number number -v|--variable variable [-u|--force] [-g|--global] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--note note]
Parameters:
   -f/--file:     The file you want to read a line from.
   -n/--number:   The line number you want to read. 1 is the first line, -1 is the last line. If the number is greater than file lines then return the last line.
   -v/--variable: The tube variable name to save the line content.
   -u/--force:    Force update even the varialbe is readonly. Default no.
   -g/--global:   If update the variable in global tube variables. Default no.

Support from version: 2.0.2</pre>
### 30: REPLACE_CHAR
#### Alias: 
<pre>Description: Replace file line content which contains/matches given value.

Syntax: - REPLACE_CHAR: -f|--file file -o|--oldvalue oldvalue -n|--newvalue newvalue [-c|--count count] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--note note]
Parameters:
   -f/--file:     The file you want to replace given characters.
   -o/--oldvalue: The oldvalue you want to replace (Support regular expressions).
   -n/--newvalue: The newvalue to replace.
   -c/--count:    The replaced times you want to set. Default no limitation.

Support from version: 2.0.1</pre>
### 31: REPORT_PROGRESS
#### Alias: 
<pre>Description: You can use this command to sent current progress via Email.

Syntax: - REPORT_PROGRESS: subject [--continue [m][n]] [--redo [m]] [--if run] [--key] [--note note]
Parameters:
   subject:  The email subject/title you want to set.

Support from version: 2.0.0</pre>
### 32: RUN_TUBE
#### Alias: 
<pre>Description: Run a sub-tube. 
             With the '--while' conditions provided, RUN_TUBE will continuely run and stop when conditions return false.

Syntax: - RUN_TUBE: -t|--tube tube [-v|--variables variables] [-w|--while conditions] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--note note]
Parameters:
   -t/--tube:      The tube you want to run. It supports 3 formats:                          
                     - 'file.yaml': Run TUBE from file.yaml file. With this format the global variables in file.xml will also be imported.                          
                     - 'file[X]': Run tube X from file.yaml file.                          
                     - 'X': Run tube X from the current yaml file.
   -v/--variables: Pass local variable key values to sub tube. format: -v v1 = 1, v2 = 2
   -w/--while:     Set the condtions to run the tube.

Support from version: 2.0.2</pre>
### 33: SET_FILE_KEY_VALUE
#### Alias: SET_KEY
<pre>Description: Update key-value file.

Syntax: - SET_FILE_KEY_VALUE: -f|--file file -k|--keywords keywords -v|--value value [--continue [m][n]] [--redo [m]] [--if run] [--key] [--note note]
Parameters:
   -f/--file:     The file you want to update.
   -k/--keywords: The key in the left side of '='.
   -v/--value:    The value in the right side of '='.

Support from version: 2.0.0</pre>
### 34: SET_VARIABLE
#### Alias: SET_VAR
<pre>Description: Set tube variable value.

Syntax: - SET_VARIABLE: -n|--name name -v|--value value [-r|--readonly] [-f|--force] [-g|--global] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--note note]
Parameters:
   -n/--name:     The tube variable name you want to set.
   -v/--value:    The tube variable value you want to set. 
                  Note: The 'eval(expression)' is also supported, eg: 
                     - SET_VARIABLE: -n dayOfWeek -v datetime.today().weekday() # Tube variable dayOfWeek will be set to weekday() value. 
                     - SET_VARIABLE: -n sum -v {var1}+{var2} # Tube variable sum will be set to the result of var1 + var2.
   -r/--readonly: Mark the variable as readonly after updating. Default no. [2.0.2]
   -f/--force:    Force update even the varialbe is readonly. Default no. [2.0.2]
   -g/--global:   If set the variable to global (Main TUBE). Within a sub-tube, it will default set the value within the sub tube scope. Default no. [2.0.2]

Support from version: 2.0.0</pre>
### 35: SET_XML_TAG_TEXT
#### Alias: SET_XML_TAG
<pre>Description: Update XML file tag text using xpath.

Syntax: - SET_XML_TAG_TEXT: -f|--file file -x|--xpath xpath -v|--value value [--continue [m][n]] [--redo [m]] [--if run] [--key] [--note note]
Parameters:
   -f/--file:  The XML file you want tup set tag text.
   -x/--xpath: The xpath of the XML tag
   -v/--value: The new value of the tag.

Support from version: 2.0.0</pre>
### 36: SFTP_GET
#### Alias: 
<pre>Description: Using SSHClient to copy remote server file to local.                                            
When copy multiple files using *.* then localpath must be a directory.

Syntax: - SFTP_GET: -r|--remotepath remotepath -l|--localpath localpath [--continue [m][n]] [--redo [m]] [--if run] [--key] [--note note]
Parameters:
   -r/--remotepath: The file full remotepath.
   -l/--localpath:  The file localpath.

Support from version: 2.0.1</pre>
### 37: SFTP_PUT
#### Alias: 
<pre>Description: Using SSHClient to put local file to remote server.                                            
When copy multiple files using *.* then remotepath must be a directory.

Syntax: - SFTP_PUT: -l|--localpath localpath -r|--remotepath remotepath [--continue [m][n]] [--redo [m]] [--if run] [--key] [--note note]
Parameters:
   -l/--localpath:  The file localpath.
   -r/--remotepath: The file full remotepath.

Support from version: 2.0.1</pre>
### 38: TAIL_FILE
#### Alias: 
<pre>Description: Print/Log the last N lines of given file.

Syntax: - TAIL_FILE: -f|--file file -l|--lines lines [-k|--keywords keywords] [-r|--result result_file] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--note note]
Parameters:
   -f/--file:     The text file you want to tail.
   -l/--lines:    The lines count you want to output.
   -k/--keywords: Output start from the given keywords.
   -r/--result:   The text file to store the tail result.

Support from version: 2.0.0</pre>
### 39: WRITE_LINE_IN_FILE
#### Alias: WRITE_LINE
<pre>Description: Write any characters into a file.                      
The written characters also could be one of them: '$NLB' (NEW_LINE_BEFORE), '$NLA' (NEW_LINE_AFTER),'$DL' (DELETE_LINE).                     
If you need more than two space characters in the value content, you can use {s:m} (m > 0) formular.                     
The 'm' means how many spaces you want to write.                     
eg: -v {s:5}hello => will be translated to 5 space chars plus hello: '     hello'

Syntax: - WRITE_LINE_IN_FILE: -f|--file file -v|--value value [-n|--number number] [-c|--contains contains] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--note note]
Parameters:
   -f/--file:     The file you want to update.
   -v/--value:    The character value you want to update in the file.
   -n/--number:   The line number you want to update. If not provided then append the value to the file.
   -c/--contains: Only update the line if it contains the given characters content.

Support from version: 2.0.0</pre>

## Tube File Samples 
### For samples tube file, please check templates folder.
<pre>
    Sample-refresh-dev.yaml
    Sample-conditional-build.yaml
</pre>
                