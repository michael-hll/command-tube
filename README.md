
-------------------------------           
# Welcome to Command Tube
-------------------------------
<table border="0">
 <tr>
    <td><b style="font-size:12px">Version: 2.0.5</b></td>
    <td><b style="font-size:12px"><a href="https://github.com/michael-hll/command-tube/blob/main/CommandTube.pdf">Slides</a></b></td>
 </tr>
</table>
                                      
## Introduction

    Command Tube is a tool that can run a group of sequenced commands. 
    You can get a full list of supportted tube commands from readme document.
    Using these commands you can easily build your own tube to do tasks like:
    Refresh Development Environment, Daily Run Test Cases etc.
    For some cases, it's more user friendly and eaiser to use than PowerShell or Bash.

## How to run Command Tube    

    Command Tube is a Python 3 script. The most important argument
    is '-t|--tube file' parameter. All the tube commands are maintained by this
    file content with YAML format.
    Within this YAML file, there must be a key called 'Tube' (like other 
    language's main method). And this 'Tube' is list type object, each item in 
    the list is a tube command. eg: A sample.yaml file contains content:

    Tube:
        - PRINT: Hello World of Command Tube

    From your terminal to run this sample.yaml (Needs Python >= 3.6):
        >>> python command-tube.py -t sample.yaml -f
    For more Command Tube arguments you can use below commands:
        >>> python command-tube.py -h
    * Notes: Command Tube will use some other module need to be installed first.
      It's better to install below packages before run a tube:
      Mac OS:
        >>> python3 -m pip install 'Colr' 'paramiko' 'beautifulsoup4' 'lxml' 'requests' 'PyYAML'
      Windows:
        >>> python -m pip install 'Colr' 'paramiko' 'beautifulsoup4' 'lxml' 'requests' 'PyYAML'
    
    - Some other examples of running Command Tube via source code:
        1: Run at once and sent result via email: 
        >>> python command-tube.py -t tube.yaml -fe
        2: Run at 20:00 o'clock:
        >>> python command-tube.py -t tube.yaml --datetime t20
        3: Run at every 6 o'clock for 100 days: 
        >>> python command-tube.py -t tube.yaml --datetime n6 -l 24 -times 100
        4: Run 10 times for every 5 minutes start from 10:00:
        >>> python command-tube.py -t tube.yaml --datetime t10 -l 5m -times 10
        5: Run tube at 9:00 AM Feb 1, 2022:
        >>> python command-tube.py -t tube.yaml --datetime '02/01/22 09:00:00'
        6: Find command syntax which name contains 'file' keyword:
        >>> python command-tube.py help file
    
        ** Find tube running result from tube.yaml.log file

    - Binary Mode (Package)       
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
    
    - More YAML file examples could reference the yaml files within test folder.

## Tube
    Tube is a container to include all tube commands. It's defined in a YAML file.
    The tube name is a YAML's content key, and the value of the key is a YAML list 
    type object. You can define 1 or many tube commands within a tube.
    There is only one main tube and maybe many sub-tubes within a yaml file. 
    The main tube name can be one of these: 'Tube', 'tube' or 'TUBE'. 
    Using command RUN_TUBE you can run a sub-tube:

        Tube:
            - RUN: SubTube
        SubTube:
            - PRINT: I'm a command from sub tube

#### Tube Chain
    A tube and it's all parents' tubes composed a tube chain.
    From previous example, tubes 'SubTube' and 'Tube' is one tube chain.

#### Each Loop
    You can run a tube in each loop mode using --each argument.
    In the below example, SubTube will be run two times since 
    ls variable has two elements.

        Tube:
            - SET: ls = ['hello', 'world']
            - RUN: SubTube --each i, item in ls
        SubTube:
            - PRINT: SubTube is running in loop: {i}, item: {item}     

#### While Loop
    You can run a tube in while loop mode using --while argument.
    In the below example, SubTube will be also run two times until
    variable i is greater than 2.

        Tube:
            - SET: i = 1
            - RUN: SubTube --while i <= 2
        SubTube:
            - PRINT: SubTube is running in loop: {i}
            - SET: i += 1 --global


#### Tube Ending
    Use SET_TUBE command's -e|--ending|--finally argument you can set a tube's
    ending tube. A ending tube will always be executed at the end.
    
        Tube:
            - SET_TUBE: --ending EndingLogic
            - PRINT: add main tube commands here            
        EndingLogic:
            - PRINT: add ending tube commands here

## Tube Commands
    For all supported tube commands you could use below commands:
    >>> python command-tube.py help commands
    You can find each command's description, syntax there.

## Naming Convention
    All sub-tube names and tube variables name could using following characters:
      a~z,A-Z,0-9,_
    Note: Python keywords are not allowed to use in tube name or variable names.
    
## Arguments & General Arguments

    Each tube command has its own arguments, you can find it from command syntax. 
    There are also some general arguments which can be used for most of tube commands. 
    Most of tube commands support additional --continue, --redo, --key, --if, --raw and 
    --note general arguments. It could make your tube realize more complex flow.  

    Notes: Since argument starts with '-' character, if you want to contain
           '-' char in your argument value you can use system placeholder to 
           achieve that: $- or {-}

        Continue:
            Syntax: --continue [m] [n]
            Description:
                - If current command failed the later tube commands will be 
                conditional skiped.
                - Normally if current command failed, the later tube commands 
                will be skipped. But use --continue parameter could change
                this.
                - Without m and n parameters: tube will run next command.                        
                - With m (m >= 1) parameter only: If current command failed,
                the later m steps will be skipped. Otherwise the later m steps
                will be executed as normal.
                - With m & n ( m,n >=0 ) both parameters: If current command faild,
                the later m steps after current will be skiped, the later n steps
                after m will be executed.
                - If current command successful, the previous senario will be swapped.
                The later m steps after current will be executed and the later n steps
                after m will be skipped.
                
        Redo: 
            Syntax: --redo [m]
            Description: 
                - Without m parameter, if current command failed it  
                will be re-executed once.
                - With m (m < 0) parameter, and current command failed, it will  
                redo commands from previous m steps.
                - With m (m > 0) parameter, and current command success, it will
                redo this command for m times.
                
        If:            
            Syntax: --if {tube_variable} | value=={tube_variable} | value!={tube_variable}
            Description:
                - If {tube_variable} uppercase equals 'FALSE' or 'NO' then the current tube
                command will be skipped.
                - For value=={tube_variable} condition, if value not equal {tube_variable}
                then current command will be skipped.
                - For value!={tube_variable} condition, if value equal {tube_variable} then
                this command will be skipped.
                - It also support >, >=, <, <= cases, make sure the values are numbers.
                Note: Extra spaces are NOT allowed in the compare expression.
                
        Key:
            Syntax: --key
            Description:
                This flag can tell the tube which commands are the key commands. If there are
                key commands exist, only all of them run successfully, the tube result will be 
                marked as successfull. 
                
        Raw:
            Syntax: --raw
            Description:
                The flag can fully disable the command placeholder logic.
                
        Raw-log:
            Syntax: --raw-log
            Description:
                The flag can disable the command placeholder logic when logging command content.
                
        Note:
            Syntax: --note notes
            Description:
                Add a note to the command.
                
## Tube Variables  

        Like other language's variables, Command Tube has its own variable called
        Tube Variable. You can define and use it for more complex cases and make
        the tool more convenient.

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
            - When get a tube variable value, it will find the first matching variable
            name in current tube chain.
            - When set a tube variable value without -g|--global argument, it will udpate 
            the tube variable value in current tube.
            - When set a tube variable value with -g|--global argument, it will update 
            the first matching variable name in current tube chain. If no matched, then 
            udpate the tube variable in the main tube.            

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
            In SET_VARIABLE command or in --if <condtiion> and --while <condition>, 
            you can omit the curly brackets:
                - SET: x = 1
                - SET: y = x + 1   
                - PRINT: testing condition --if x == 1    
                - RUN: SubTube --while x < 10  
             
        ** Note: If variable was updated from terminal console inputs, then it will 
                 become readonly. 
                
                
## Usage of Each Command:
### 1: BREAK
#### Alias: BREAK
<pre>Description: The command can break a tube's running.

Syntax: - BREAK: [reason] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   reason:  The reason you want to break. [Optional]

Support from version: 2.0.2</pre>
### 2: CHECK_CHAR_EXISTS
#### Alias: CHECK_CHAR, FIND
<pre>Description: Check or find characters from a file. Result was updated into tube variables.

Syntax: - CHECK_CHAR_EXISTS: -f|--file file -c|--char characters -v|-e|--variable|--exist result [-n|--number number] [-l|--line line] [-u|--force] [-g|--global] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   -f|--file:                The file you want to check or find.
   -c|--char:                The characters you want to check or find (Support regular expression).
   -v|-e|--variable|--exist: The tube variable name to store the checking result.
   -n|--number:              The tube variable name to store the line number.
   -l|--line:                The tube variable name to store the line content.
   -u|--force:               Force update even the variable is readonly. Default no. [2.0.2]
   -g|--global:              If update the variable in global tube variables. Default no. [2.0.2]

Support from version: 2.0.1</pre>
### 3: COMMAND
#### Alias: CMD
<pre>Description: Run any Windows/MacOS terminal command.

Syntax: - COMMAND: command [--result result] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   command:    Any command you want to run.
   --result:   The text file to store command outputs. [2.0.2]

Support from version: 2.0.0</pre>
### 4: CONNECT
#### Alias: CONN
<pre>Description: You can use this command to switch your server connection.

Syntax: - CONNECT: host [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   host:  The Linux server host or name you want to connect using SSH protocal.

Support from version: 2.0.0</pre>
### 5: CONTINUE
#### Alias: CONTINUE
<pre>Description: The command can continue a tube's running while it's in a loop.

Syntax: - CONTINUE: [reason] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   reason:  The reason you want to continue. [Optional]

Support from version: 2.0.2</pre>
### 6: COUNT
#### Alias: CNT
<pre>Description: Count file lines number (-f) or Count tube command number by status (-t).

Syntax: - COUNT: [-f|--file file] [-t|--tube|--status tube] -v|--variable variable [-c|--current] [-s|--skip] [-u|--force] [-g|--global] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   -f|--file:          The file you want to count line numbers.
   -t|--tube|--status: The tube command status you want to count.
   -v|--variable:      The tube variable name to store the count result.
   -c|--current:       If only count current tube. Default no.
   -s|--skip:          If skip COUNT command. Default no.
   -u|--force:         Force update even the variable is readonly. Default no. [2.0.2]
   -g|--global:        If update the variable in global tube variables. Default no. [2.0.2]

Support from version: 2.0.0</pre>
### 7: CREATE_OBJECT
#### Alias: CREATE, NEW
<pre>Description: Create a new object instance.

Syntax: - CREATE_OBJECT: name [-u|--force] [-g|--global] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   name:        The object instance name (Tube variable name).
   -u|--force:  Force update even the variable is readonly. Default no.
   -g|--global: If update the variable in global tube variables. Default no.

Support from version: 2.0.3</pre>
### 8: DELETE_LINE_IN_FILE
#### Alias: DEL_LN, DEL_LINE, DELETE_LINE
<pre>Description: Conditionally delete lines from a file.

Syntax: - DELETE_LINE_IN_FILE: -f|--file file [-n|--number number] [-b|--begins begins] [-c|--contains contains] [-e|--empty] [-r|--result result] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   -f|--file:     The file you want to delete lines from.
   -n|--number:   The line number you want to delete. 1 is the first line, -1 is the last line.
   -b|--begins:   The line begins with character you want to delete.
   -c|--contains: The line contains with character you want to delete.
   -e|--empty:    A flag to tell if delete empty line. Default no.
   -r|--result:   The text file to store deleted result.

Support from version: 2.0.0</pre>
### 9: DELETE_VARIABLE
#### Alias: DELETE_VAR, DEL_VAR
<pre>Description: Delete tube variables.

Syntax: - DELETE_VARIABLE: name [-g|--global] [-a|--all] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   name:        The tube variable name you want to delete from current tube.
   -g|--global: With --global parameter you can delete it from current and its parent tubes.
   -a|--all:    With --all parameter you can delete it from all tubes.

Support from version: 2.0.2</pre>
### 10: DIR_CREATE
#### Alias: D_CREATE
<pre>Description: Create a directory if it doesnot exist.

Syntax: - DIR_CREATE: directory [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   directory:  The directory you want to create.

Support from version: 2.0.2</pre>
### 11: DIR_DELETE
#### Alias: D_DEL, D_DELETE
<pre>Description: Delete a directory and its sub-directories.

Syntax: - DIR_DELETE: directory [-f|--force] [-r|--result result] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   directory:   The directory you want to delete.
   -f|--force:  Force delete if the director is not empty. Default no.
   -r|--result: The text file to store deleted directory result.

Support from version: 2.0.2</pre>
### 12: DIR_EXIST
#### Alias: D_EXIST
<pre>Description: Check if a directory exists.

Syntax: - DIR_EXIST: -d|--dir directory -v|--variable variable [-u|--force] [-g|--global] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   -d|--dir:      The directory you want to check.
   -v|--variable: The tube variable name to store the exist result. (True/False)
   -u|--force:    Force update even the variable is readonly. Default no.
   -g|--global:   If update the variable in global tube variables. Default no.

Support from version: 2.0.2</pre>
### 13: EMAIL
#### Alias: MAIL
<pre>Description: Sent Email to someone with given subject and content.

Syntax: - EMAIL: -t|--to to -s|--subject subject -b|--body body [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   -t|--to:      The sending email addresses.
   -s|--subject: The email title.
   -b|--body:    The email content. If it's text file name, then the content of the file will be as the email content.

Support from version: 2.0.0</pre>
### 14: EXEC
#### Alias: EXEC
<pre>Description: Run tube variable's method.

Syntax: - EXEC: commands [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   commands:  The tube variable's method you want to run. eg: my_list.reverse()

Support from version: 2.0.2</pre>
### 15: FILE_APPEND
#### Alias: F_APPEND
<pre>Description: Append the content to the last line of the given text file.

Syntax: - FILE_APPEND: -f|--file file -v|--value value [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   -f|--file:  The text file name you want to append.
   -v|--value: The content you want to append to the text file.

Support from version: 2.0.2</pre>
### 16: FILE_COPY
#### Alias: F_COPY, F_CP
<pre>Description: Copy any files to target.

Syntax: - FILE_COPY: -s|-f|--src|--from src -d|-t|--dest|--to dest [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   -s|-f|--src|--from: The source file name you want to copy.
   -d|-t|--dest|--to:  The target file or folder

Support from version: 2.0.2</pre>
### 17: FILE_CREATE
#### Alias: F_CREATE
<pre>Description: Create an empty file.

Syntax: - FILE_CREATE: [file] [-f|--file afile] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   file:      The text file name you want to create.
   -f|--file: The text file name you want to create. It will override the file argument.

Support from version: 2.0.2</pre>
### 18: FILE_DELETE
#### Alias: F_DEL, F_DELETE
<pre>Description: Delete any files math the file name.

Syntax: - FILE_DELETE: [file] [-f|--file afile] [-r|--result result] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   file:        The file name you want to delete.
   -f|--file:   The text file name you want to delete. It will override the file argument.
   -r|--result: The text file to store deleted files result.

Support from version: 2.0.2</pre>
### 19: FILE_DOWNLOAD
#### Alias: DOWNLOAD
<pre>Description: Download a file from internet using requests.get().

Syntax: - FILE_DOWNLOAD: -u|--url url -f|--file file [--timeout timeout] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   -u|--url:    The file url.
   -f|--file:   The file name to save.
   --timeout:   The timeout seconds to download the file. Default no timeout.

Support from version: 2.0.3</pre>
### 20: FILE_EMPTY
#### Alias: F_EMPTY
<pre>Description: Clear an existing text file or create a new empty file.

Syntax: - FILE_EMPTY: [file] [-f|--file afile] [-c|--create] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   file:        The text file name you want to empty.
   -f|--file:   The text file name you want to empty. It will override the file argument.
   -c|--create: If the give file doesnot exist if create a new empty file. Default No.

Support from version: 2.0.2</pre>
### 21: FILE_EXIST
#### Alias: F_EXIST
<pre>Description: Check if a file exists.

Syntax: - FILE_EXIST: -f|--file file -v|--variable variable [-u|--force] [-g|--global] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   -f|--file:     The file name you want to check.
   -v|--variable: The tube variable name to store the exist result. (True/False)
   -u|--force:    Force update even the variable is readonly. Default no.
   -g|--global:   If update the variable in global tube variables. Default no.

Support from version: 2.0.2</pre>
### 22: FILE_INSERT
#### Alias: F_INSERT
<pre>Description: Insert a line before given line number. If line number doesnot exist then insert to the end.

Syntax: - FILE_INSERT: -f|--file file -n|--number number -v|--value value [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   -f|--file:   The file you want to insert.
   -n|--number: The line number you want to inert. 1 means the first line, -1 means the last line.
   -v|--value:  The line you want to insert into the file.

Support from version: 2.0.2</pre>
### 23: FILE_MOVE
#### Alias: F_MOVE, F_MV
<pre>Description: Move any files to target.

Syntax: - FILE_MOVE: -s|-f|--src|--from src -d|-t|--dest|--to dest [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   -s|-f|--src|--from: The source file name you want to move.
   -d|-t|--dest|--to:  The target file or folder

Support from version: 2.0.2</pre>
### 24: FILE_POP
#### Alias: F_POP
<pre>Description: Pop one line of the given text file. If there is no line there then store empty.

Syntax: - FILE_POP: [file] [-f|--file afile] [-v|--variable variable] [-n|--number number] [-u|--force] [-g|--global] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   file:          The text file name you want to pop.
   -f|--file:     The text file name you want to pop. It will override the file argument.
   -v|--variable: The tube variable name to store the line content result.
   -n|--number:   The line number you want to pop. Default 1 to pop the first line. -1 to pop the last line.
   -u|--force:    Force update even the variable is readonly. Default no.
   -g|--global:   If update the variable in global tube variables. Default no.

Support from version: 2.0.2</pre>
### 25: FILE_PUSH
#### Alias: F_PUSH
<pre>Description: Push the content to the first line of the given text file.

Syntax: - FILE_PUSH: -f|--file file -v|--value value [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   -f|--file:  The text file name you want to push.
   -v|--value: The content you want to push to the text file.

Support from version: 2.0.2</pre>
### 26: FILE_READ
#### Alias: F_READ
<pre>Description: Read a file content to tube variable. Doesn't include the new-line (\n) char.

Syntax: - FILE_READ: -f|--file file [-c|--content content] [-l|--lines lines] [-s|--skip-empty] [-u|--force] [-g|--global] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   -f|--file:       The file name you want to read its whole content.
   -c|--content:    The tube variable name to store the file content.
   -l|--lines:      The tube variable name to store the file content as lines.
   -s|--skip-empty: If skip empty lines. Default no.
   -u|--force:      Force update even the variable is readonly. Default no.
   -g|--global:     If update the variable in global tube variables. Default no.

Support from version: 2.0.2</pre>
### 27: FILE_SORT
#### Alias: F_SORT
<pre>Description: Sort a text file lines content.

Syntax: - FILE_SORT: [file] [-f|--file afile] [-n|--number] [-s|--sort sort] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   file:        The file you want to sort.
   -f|--file:   The file you want to sort. It will override file argument.
   -n|--number: If sort file line content as numbers. Default No.
   -s|--sort:   Default value is asc. You can set value 'desc' to reverse the sorting.

Support from version: 2.0.2</pre>
### 28: GET_FILE_KEY_VALUE
#### Alias: GET_KEYS
<pre>Description: Read key values from key-value file.                                            
It also supports to read key-value from Yaml file.                                            
The key-value results will be stored into tube variables.

Syntax: - GET_FILE_KEY_VALUE: -f|--file file [-k|--keywords keywords] [-u|--force] [-g|--global] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   -f|--file:     The file you want to get key-value from.
   -k|--keywords: The key you want to get values from the file. It supports comma seperated format for multiple keys.                           
                    eg1: -k key1, key2 # It will read key1, key2 values and save to tube variables key1, key2;                           
                    eg2: -k key1 > k1, key2 > k2 # It will read key1, key2 values and save to tube variables k1, k2
   -u|--force:    Force update even the variable is readonly. Default no. [2.0.2]
   -g|--global:   If update the variable in global tube variables. Default no. [2.0.2]

Support from version: 2.0.0</pre>
### 29: GET_XML_TAG_TEXT
#### Alias: GET_XML_TAG
<pre>Description: Get XML file tag text value.                                            
The result will be stored into a tube variable and xpath will be used as the variable name.

Syntax: - GET_XML_TAG_TEXT: -f|--file file -x|--xpath xpath [-v|--variable variable] [-u|--force] [-g|--global] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   -f|--file:     The XML file you want to get tag text.
   -x|--xpath:    The xpath of the XML tag.
   -v|--variable: The tube variable name to store the value. [2.0.2]
   -u|--force:    Force update even the variable is readonly. Default no. [2.0.2]
   -g|--global:   If update the variable in global tube variables. Default no. [2.0.2]

Support from version: 2.0.0</pre>
### 30: IMPORT_MODULE
#### Alias: IMPORT
<pre>Description: Import other python modules to command tube.

Syntax: - IMPORT_MODULE: imports [--if run] [--key] [--raw-log] [--note note]
Parameters:
   imports:  The import module command. eg: import pandas as pd

Support from version: 2.0.5</pre>
### 31: LINUX_COMMAND
#### Alias: LCMD, SSHCMD
<pre>Description: Run a Linux command from the previous connected server.

Syntax: - LINUX_COMMAND: command [--log-detail] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   command:        Any Linux command you want to run.
   --log-detail:   Log command output to tube log file. Default no. [2.0.2]

Support from version: 2.0.0</pre>
### 32: LIST_DIRS
#### Alias: LIST_D
<pre>Description: Got all sub directories for the given directory, and save the result list to a text file or variable.

Syntax: - LIST_DIRS: -d|--dir directory [-r|--result result] [-s|--sort sort] [-c|--count count] [-v|--variable variable] [-u|--force] [-g|--global] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   -d|--dir:      The directory you want to list its sub directories.
   -r|--result:   The text file to store the list result.
   -s|--sort:     It accepts 'asc' or 'desc' value for the sorting. Default is 'asc'.
   -c|--count:    The tube variable name to store the directories count.
   -v|--variable: The tube variable name to store the list result.
   -u|--force:    Force update even the variable is readonly. Default no.
   -g|--global:   If update the variable in global tube variables. Default no.

Support from version: 2.0.2</pre>
### 33: LIST_FILES
#### Alias: LIST_F
<pre>Description: Get matched files list and save it to a text file or variable.

Syntax: - LIST_FILES: [-d|--dir directory] [-f|--file afile] [-e|--exclude exclude] [-r|--result result] [-s|--sort sort] [-c|--count count] [-v|--variable variable] [-u|--force] [-g|--global] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   -d|--dir:      The directory with file name matchings. If not provided then use default *.* to list all files. eg: <directory>/*.* or *.jpg
   -f|--file:     The files name you want to list. If not provided then use default *.* to list all files. eg: <directory>/*.* or *.jpg
   -e|--exclude:  The excluded file names. eg: -e .txt|.log
   -r|--result:   The text file to store the search result.
   -s|--sort:     Using '-s atime|mtime|ctime|name|size [asc|desc]' to set the sort properties. Default uses the file modification mtime (mtime asc) to sort the result.
   -c|--count:    The tube variable name to store the files count.
   -v|--variable: The tube variable name to store the list result.
   -u|--force:    Force update even the variable is readonly. Default no.
   -g|--global:   If update the variable in global tube variables. Default no.

Support from version: 2.0.2</pre>
### 34: PATH
#### Alias: CD
<pre>Description: Go to specific directory.

Syntax: - PATH: directory [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   directory:  The directory you want to goto.

Support from version: 2.0.0</pre>
### 35: PAUSE
#### Alias: PAUZE
<pre>Description: Command Tube will pause with given minutes/seconds.

Syntax: - PAUSE: minutes [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   minutes:  The minutes you want to pause. You can end it with 's' char to pause for xxx seconds.

Support from version: 2.0.0</pre>
### 36: PRINT
#### Alias: ECHO
<pre>Description: Print a message to the console for debugging purpose.

Syntax: - PRINT: message [-c|--color color] [--json] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   message:      The message you want to print in the terminal.
   -c|--color:   The message color you want to use. You can use color name 'red' or 'FF0000' to set the color value.
   --json:       Print message in json format. Default no. [2.0.3]

Support from version: 2.0.2</pre>
### 37: PRINT_VARIABLES
#### Alias: PRINT_VARS
<pre>Description: Print tube variable values for debugging purpose.

Syntax: - PRINT_VARIABLES: name [-r|--result result] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   name:        The tube variable name. With value '*' or '.' can print all variables.
   -r|--result: The text file to store the result.

Support from version: 2.0.2</pre>
### 38: READ_LINE_IN_FILE
#### Alias: READ_LN, READ_LINE
<pre>Description: Read one line by given line number, and save the line content to tube variable.

Syntax: - READ_LINE_IN_FILE: -f|--file file -n|--number number -v|--variable variable [-u|--force] [-g|--global] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   -f|--file:     The file you want to read a line from.
   -n|--number:   The line number you want to read. 1 is the first line, -1 is the last line. If the number is greater than file lines then return the last line.
   -v|--variable: The tube variable name to save the line content.
   -u|--force:    Force update even the varialbe is readonly. Default no.
   -g|--global:   If update the variable in global tube variables. Default no.

Support from version: 2.0.2</pre>
### 39: REPLACE_CHAR
#### Alias: REPLACE
<pre>Description: Replace file line content which contains/matches given value.

Syntax: - REPLACE_CHAR: -f|--file file -o|--oldvalue oldvalue -n|--newvalue newvalue [-c|--count count] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   -f|--file:     The file you want to replace given characters.
   -o|--oldvalue: The oldvalue you want to replace (Support regular expressions).
   -n|--newvalue: The newvalue to replace.
   -c|--count:    The replaced times you want to set. Default 1.

Support from version: 2.0.1</pre>
### 40: REPORT_PROGRESS
#### Alias: REPORT_PRO
<pre>Description: You can use this command to sent current progress via Email.

Syntax: - REPORT_PROGRESS: subject [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   subject:  The email subject/title you want to set.

Support from version: 2.0.0</pre>
### 41: REQUESTS_DELETE
#### Alias: HTTP_DELETE
<pre>Description: Sent a HTTP Delete request. Save the response to tube variable.

Syntax: - REQUESTS_DELETE: url [-a|--args parameters] -r|--resp response [-u|--force] [-g|--global] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   url:         The request url.
   -a|--args:   The parameters of requests.delete() method. eg: --args params=xxx, data=yyy
   -r|--resp:   The tube variable name to store http get response.                          
                Then you can access response properties: status_code, url, headers, text, json(), etc.                          
                Refer to: https://requests.readthedocs.io/en/latest/user/quickstart/#response-content
   -u|--force:  Force update even the variable is readonly. Default no.
   -g|--global: If update the variable in global tube variables. Default no.

Support from version: 2.0.3</pre>
### 42: REQUESTS_GET
#### Alias: HTTP_GET
<pre>Description: Sent a HTTP Get request. Save the response to tube variable.

Syntax: - REQUESTS_GET: url [-a|--args parameters] [-r|--resp response] [-s|--soup soup] [-u|--force] [-g|--global] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   url:         The request url.
   -a|--args:   The parameters of requests.get() method. eg: --args params=xxx, data=yyy
   -r|--resp:   The tube variable name to store http get response.                          
                Then you can access response properties: status_code, url, headers, text, json(), etc.                          
                Refer to: https://requests.readthedocs.io/en/latest/user/quickstart/#response-content
   -s|--soup:   Tube variable name of BeautifulSoup object. (Use Response.Text content with lxml parser)
   -u|--force:  Force update even the variable is readonly. Default no.
   -g|--global: If update the variable in global tube variables. Default no.

Support from version: 2.0.3</pre>
### 43: REQUESTS_HEAD
#### Alias: HTTP_HEAD
<pre>Description: Sent a HTTP Head request. Save the response to tube variable.

Syntax: - REQUESTS_HEAD: url [-a|--args parameters] -r|--resp response [-u|--force] [-g|--global] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   url:         The request url.
   -a|--args:   The parameters of requests.head() method. eg: --args params=xxx, data=yyy
   -r|--resp:   The tube variable name to store http get response.                          
                Then you can access response properties: status_code, url, headers, text, json(), etc.                          
                Refer to: https://requests.readthedocs.io/en/latest/user/quickstart/#response-content
   -u|--force:  Force update even the variable is readonly. Default no.
   -g|--global: If update the variable in global tube variables. Default no.

Support from version: 2.0.3</pre>
### 44: REQUESTS_OPTIONS
#### Alias: HTTP_OPTIONS
<pre>Description: Sent a HTTP Options request. Save the response to tube variable.

Syntax: - REQUESTS_OPTIONS: url [-a|--args parameters] -r|--resp response [-u|--force] [-g|--global] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   url:         The request url.
   -a|--args:   The parameters of requests.options() method. eg: --args params=xxx, data=yyy
   -r|--resp:   The tube variable name to store http get response.                          
                Then you can access response properties: status_code, url, headers, text, json(), etc.                          
                Refer to: https://requests.readthedocs.io/en/latest/user/quickstart/#response-content
   -u|--force:  Force update even the variable is readonly. Default no.
   -g|--global: If update the variable in global tube variables. Default no.

Support from version: 2.0.3</pre>
### 45: REQUESTS_PATCH
#### Alias: HTTP_PATCH
<pre>Description: Sent a HTTP Patch request. Save the response to tube variable.

Syntax: - REQUESTS_PATCH: url [-a|--args parameters] -r|--resp response [-u|--force] [-g|--global] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   url:         The request url.
   -a|--args:   The parameters of requests.patch() method. eg: --args params=xxx, data=yyy
   -r|--resp:   The tube variable name to store http get response.                          
                Then you can access response properties: status_code, url, headers, text, json(), etc.                          
                Refer to: https://requests.readthedocs.io/en/latest/user/quickstart/#response-content
   -u|--force:  Force update even the variable is readonly. Default no.
   -g|--global: If update the variable in global tube variables. Default no.

Support from version: 2.0.3</pre>
### 46: REQUESTS_POST
#### Alias: HTTP_POST
<pre>Description: Sent a HTTP Post request. Save the response to tube variable.

Syntax: - REQUESTS_POST: url [-a|--args parameters] -r|--resp response [-u|--force] [-g|--global] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   url:         The request url.
   -a|--args:   The parameters of requests.post() method. eg: --args params=xxx, data=yyy
   -r|--resp:   The tube variable name to store http get response.                          
                Then you can access response properties: status_code, url, headers, text, json(), etc.                          
                Refer to: https://requests.readthedocs.io/en/latest/user/quickstart/#response-content
   -u|--force:  Force update even the variable is readonly. Default no.
   -g|--global: If update the variable in global tube variables. Default no.

Support from version: 2.0.3</pre>
### 47: REQUESTS_PUT
#### Alias: HTTP_PUT
<pre>Description: Sent a HTTP Put request. Save the response to tube variable.

Syntax: - REQUESTS_PUT: url [-a|--args parameters] -r|--resp response [-u|--force] [-g|--global] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   url:         The request url.
   -a|--args:   The parameters of requests.put() method. eg: --args params=xxx, data=yyy
   -r|--resp:   The tube variable name to store http get response.                          
                Then you can access response properties: status_code, url, headers, text, json(), etc.                          
                Refer to: https://requests.readthedocs.io/en/latest/user/quickstart/#response-content
   -u|--force:  Force update even the variable is readonly. Default no.
   -g|--global: If update the variable in global tube variables. Default no.

Support from version: 2.0.3</pre>
### 48: RUN_TUBE
#### Alias: RUN
<pre>Description: Run a sub-tube. 
             With the '--while' conditions provided, RUN_TUBE will continuely run and stop when conditions return false.                                              
             With the '--each' parameters provided, RUN_TUBE will iterate the list variable and run the sub-tube.

Syntax: - RUN_TUBE: tube [-v|--variables variables] [-w|--while conditions] [-e|--each each] [-f|--for each] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   tube:           The tube you want to run. It supports 3 formats:                          
                     - 'file.yaml': Run TUBE from file.yaml file. With this format the global variables in file.xml will also be imported.                          
                     - 'file[X]': Run tube X from file.yaml file.                          
                     - 'X': Run tube X from the current yaml file.
   -v|--variables: Pass local variable key values to sub tube. format: -v v1 = 1, v2 = 'Command Tube'
   -w|--while:     Set the while condtions to run the tube: --while <eval-expression-condition>
   -e|--each:      Set the foreach loop arguments with format: --each [index_name,] item_name in list_name
   -f|--for:       The alias of --each argument.

Support from version: 2.0.2</pre>
### 49: SET_FILE_KEY_VALUE
#### Alias: SET_KEY
<pre>Description: Update key-value file.

Syntax: - SET_FILE_KEY_VALUE: -f|--file file -k|--keywords keywords -v|--value value [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   -f|--file:     The file you want to update.
   -k|--keywords: The key in the left side of '='.
   -v|--value:    The value in the right side of '='.

Support from version: 2.0.0</pre>
### 50: SET_TUBE
#### Alias: SET_T
<pre>Description: Enable or disable tube commands general arguments for: --continue, --redo or --key.                         
Set tube's ending tube.

Syntax: - SET_TUBE: [-c|--continue-all continue_all] [-r|--redo-all redo_all] [-k|--key-all key_all] [-e|--ending|--finally ending_tube] [--key-ending] [--if run] [--raw] [--raw-log] [--note note]
Parameters:
   -c|--continue-all:     Enable/disable tube's command --continue status. Values: yes/no, true/false.
   -r|--redo-all:         Enable/disable tube's command --redo status. Values: yes/no, true/false.
   -k|--key-all:          Enable/disable tube's command --key status. Values: yes/no, true/false.
   -e|--ending|--finally: The tube you want to run for ending. It supports 3 formats:                          
                            - 'file.yaml': Run TUBE from file.yaml file. With this format the global variables in file.xml will also be imported.                          
                            - 'file[X]': Run tube X from file.yaml file.                          
                            - 'X': Run tube X from the current yaml file.
   --key-ending:          Add ending tube --key argument.

Support from version: 2.0.2</pre>
### 51: SET_VARIABLE
#### Alias: SET_VAR, SET
<pre>Description: Set tube variable value.

Syntax: - SET_VARIABLE: [expression] [-n|--name name] [-k|--keyword keyword] [-i|--index index] [-v|--value value] [-r|--readonly] [-u|--force] [-g|--global] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   expression:    Assign variable value with format: var_name = expression, var_name["keyword"] = expression or var_name[index] = expression;                          
                  You can also use operator +=, -=, *=, /+ to make the assignment eaiser: i += 1, i *= -1 etc;                           
                  Or you can use --name, --keyword, --index, --value arguments to set the variable value explicitly.
   -n|--name:     The tube variable name you want to set.
   -k|--keyword:  If update a dictional type variable, this --keyword value is to set the dict key.
   -i|--index:    If update a list type variable, this --index value is to set list index.
   -v|--value:    The tube variable value you want to set. 
                  Note: The backend is using 'eval(expression)' so you can do more things, eg: 
                     - set_var: -n dayOfWeek -v datetime.today().weekday() # Tube variable dayOfWeek will be set to weekday() value. 
                     - set_var: ls = [1,2,3] # Tube variable ls was updated to list value: [1,2,3]. 
                     - set_var: ls = ls.append(4) # Tube variable ls appended value 4 to its end: [1,2,3,4].
   -r|--readonly: Mark the variable as readonly after updating. Default no. [2.0.2]
   -u|--force:    Force update even the varialbe is readonly. Default no. [2.0.2]
   -g|--global:   If set the variable to global (Main TUBE).
                  With this flag, it will try to find the first variable from current and its parent tube chain that mathes the input variable name, and update its value. 
                  If found nothing then the variable will be updated in the main tube. 
                  Without this flag, it will update the variable in current tube. 
                  Default no. [2.0.2]

Support from version: 2.0.0</pre>
### 52: SET_XML_TAG_TEXT
#### Alias: SET_XML_TAG
<pre>Description: Update XML file tag text using xpath.

Syntax: - SET_XML_TAG_TEXT: -f|--file file -x|--xpath xpath -v|--value value [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   -f|--file:  The XML file you want tup set tag text.
   -x|--xpath: The xpath of the XML tag
   -v|--value: The new value of the tag.

Support from version: 2.0.0</pre>
### 53: SFTP_GET
#### Alias: FTP_GET
<pre>Description: Using SSHClient to copy remote server file to local.                                            
When copy multiple files using *.* then localpath must be a directory.

Syntax: - SFTP_GET: -r|--remotepath remotepath -l|--localpath localpath [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   -r|--remotepath: The file full remotepath.
   -l|--localpath:  The file localpath.

Support from version: 2.0.1</pre>
### 54: SFTP_PUT
#### Alias: FTP_PUT
<pre>Description: Using SSHClient to put local file to remote server.                                            
When copy multiple files using *.* then remotepath must be a directory.

Syntax: - SFTP_PUT: -l|--localpath localpath -r|--remotepath remotepath [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   -l|--localpath:  The file localpath.
   -r|--remotepath: The file full remotepath.

Support from version: 2.0.1</pre>
### 55: TAIL_FILE
#### Alias: TAIL
<pre>Description: Print/Log the last N lines of given file.

Syntax: - TAIL_FILE: -f|--file file -l|--lines lines [-k|--keywords keywords] [-r|--result result] [-v|--variable variable] [-u|--force] [-g|--global] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   -f|--file:     The text file you want to tail.
   -l|--lines:    The lines count you want to output.
   -k|--keywords: Output start from the given keywords.
   -r|--result:   The text file to store the tail result.
   -v|--variable: The tube variable name to store the tail result as lines.
   -u|--force:    Force update even the variable is readonly. Default no.
   -g|--global:   If update the variable in global tube variables. Default no.

Support from version: 2.0.0</pre>
### 56: WRITE_LINE_IN_FILE
#### Alias: WRITE_LN, WRITE_LINE
<pre>Description: Write any characters into a file.

Syntax: - WRITE_LINE_IN_FILE: -f|--file file -v|--value value [-n|--number number] [-c|--contains contains] [--continue [m][n]] [--redo [m]] [--if run] [--key] [--raw] [--raw-log] [--note note]
Parameters:
   -f|--file:     The file you want to update.
   -v|--value:    The character value you want to update in the file.
   -n|--number:   The line number you want to update. If not provided then append the value to the file.
   -c|--contains: Only update the line if it contains the given characters content.

Support from version: 2.0.0</pre>

## Tube File Samples 
### For samples tube file, please check templates folder.
<pre>
    Sample-refresh-dev.yaml
    Sample-conditional-build.yaml
    Sample-FFMPEG.yaml
</pre>
                