# Programming Tube

Author: Han LiangLiang

Email: michael_hll@hotmail.com

Update Date: May 2022

---
## Introduction
    Programming Tube is a tool that can run a group of sequenced commands.    
    Those commands are added from a YAML config file, which I usually call it a tube file. 
    See the examples from the template YAML file ('help template' could output it).
    When you run this program, you can use the -y | --yaml parameter to specify the config file.
    From help you could find all types of supported commands.
---
## How to run Programming Tube
    Programming Tube is a Python 3 script. The most important two arguments 
    for Programming Tube are '--yaml' and '--datetime'.    
    All the tube configurations are maintained by a YAML file, 
    using '--yaml file' you can specify the tube configurations. 
    From the 'tube.template.yaml' you could view how it looks like.
    Use '--datetime' argument you could set the execution time, 
    you could also run it at once by parameter '-f' or '-i'.
    For more information about input arguments please use following command 
    from your terminal (In MacOS, you may need Python3 >= 3.7):
        >>> python programming-tube.py -h
    
### - Examples of running Programming Tube:
        1: Run at once and sent email result: 
        >>> python programming-tube.py -y tube.yaml -fe
        2: Run at 20:00 o'clock:
        >>> python programming-tube.py -y tube.yaml -t20
        3: Run at every 6 o'clock for 100 days: 
        >>> python programming-tube.py -y tube.yaml -t n6 -l 24 -times 100
        4: Run 10 times for every 5 minutes start from 10:00:
        >>> python programming-tube.py -y tube.yaml -t t10 -l 5m -times 10
        5: Run tube at 9:00 AM Feb 1, 2022:
        >>> python programming-tube.py -y tube.yaml -t '02/01/22 09:00:00'
        6: Find command syntax which name contains 'file' keyword:
        >>> python programming-tube.py help file
    
        ** Find tube running result from tube.yaml.log file
                 
### - Binary Mode        
        Following below steps you can use it in binary mode
        1. Download 'tube' for MacOS or 'tube.exe' for Windows from github homepage
        3. Using it from your terminal:
        (You need to change RUN_MODE from SRC to BIN in YAML config file)
        >>> tube -y tube.yaml -f  
        Note: In MacOS you need give the 'tube' exec right first.
       

## General Arguments & Tube Variables
    - General Arguments
        Description: All tube commands support additional --redo, --continue,
                 --key and --if paramters. It could make your tube realize
                 more complex flow.

        Redo: 
            Syntax: --redo [m]
            Description: Without m parameter, if current command failed it  
            will be re-executed once.

            With m (m < 0) parameter, and current command failed, it will  
            redo commands from previous m steps.

            With m (m > 0) parameter, and current command success, it will
            redo this command for m times.
        
        Continue:
            Syntax: --continue [m] [n]
            Description:
            If current command failed the later tube commands will be 
            conditional skiped.

            Normally if current command failed, the later tube commands 
            will be skipped. But use --continue parameter could change
            this.

            Without m and n parameters: the tube will run continuely.
                    
            With m (m >= 1) parameter only: If current command failed,
            the later m steps will be skipped. Otherwise the later m steps
            will be executed as normal.

            With m & n ( m,n >=0 ) both parameters: If current command faild,
            the later m steps after current will be skiped, the later n steps
            after m will be executed.
            If current command successful, the previous senario will be swapped.
            The later m steps after current will be executed and the later n steps
            after m will be skipped.

        If:
            Syntax: --if {tube_variable} | value=={tube_variable} | value!={tube_variable}
            Description:
                If {tube_variable} uppercase equals 'FALSE' or 'NO' then the tube command
                will be skipped.
                For value=={tube_variable} condition, if value not equal {tube_variable} then this
                command will be skipped.
                For value!={tube_variable} condition, if value equal {tube_variable} then this
                command will be skipped.
                It also support >, >=, <, <= cases, make sure the values are numbers before 
                comparison.
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
            root_folder: C:\workspaces\trunk
            package_name: xxx-app
            cmd_parameters: -l
            # Below are default hidden variables:
            s: ' ' # Its value is a space char and can't be overridden
        Then you can reference any variable value via {var-name} in your tube 
        command arguments. eg:
            - PATH: {root_folder}
            - COMMAND: ls {cmd_parameters}
            # The below {s:10} will be replaced by 10 space chars 
            - WRITE_LINE_IN_FILE: -f file -v {s:10}any line content here  
        The below commands will update the tube variables:
            - GET_XML_TAG_TEXT => xpath will be the variable name
            - GET_FILE_KEY_VALUE => key(s) will be the variable name
            - COUNT => variable parameter will be stored into tube variables
            - SET_VARIABLE => update tube variable by name value
        Note: If variable was updated from console inputs, then it will become readonly. 
---
## Examples of Each Command

    Notes: The tube variables and general arguments are play important roles in Programming Tube. They can be used in all suppported commands. In order to show the examples of how to use variables and general arguments, only list some examples in the first COMMAND, you can use them similarly in other support commands.

    - COMMAND
        Description: Run any Windows/MacOS terminal command.
        Syntax: 
            COMMAND: command [--continue [m][n]] [--redo [m]] [--if run] [--key]
```yml
    # YAML format
    # Assume we want to run a code build command 'ant deploy':
    # If 'ant deploy' run successfully, then tube will continue run next command
    # otherwise tube will stop if it failed
    - COMMAND: ant deploy
    # With --continue argument tube will continue exec next command if current failed:
    - COMMAND: ant deploy --continue
    # With --redo argument tube will re-run current if it failed:  
    - COMMAND: ant deploy --redo 
    # - With --redo and --continue arguments together, tube will continue exec next command if redo also failed:
    - COMMAND: ant deploy --redo --continue
    # With --redo -1 tube will re-run previous plus current command again if it failed:
    - COMMAND: ant deploy --redo -1 --continue
    # Assume we have one tube variable 'run_deploy' and it equals 'Yes', then below
    # --if condition will return true and the 'ant deploy' command will be exec as normal.
    # If 'run_deploy' variable equals 'No', then the below command will be skipped:
    - COMMAND: ant deploy --if {run_deploy}
    # For some cases you can also use --if with comparison simples: ==, >, <, != etc.
    # if tube variable 'run_deploy' equals character 'run' then this command will be executed:
    - COMMAND: ant deploy --if {run_deploy}==run
    # Since there could be lots of command within a tube, then using the --key
    # argument can determine which tube commands can deside the final tube exec result:
    - COMMAND: ant deploy --key
```

    - CONNECT
        Description: You can use this command to switch your server connection.
        Syntax: 
            CONNECT: xxx.xxx.com [--continue [m][n]] [--redo[m]] [--if run] [--key]

```yml
    # YAML format
    # You need to config your servers from your tube file first
    - CONNECT: server1.xxx.com
```

    - LINUX_COMMAND
        Description: Run a Linux command from the previous connected server.
        Syntax: 
            LINUX_COMMAND: command [--continue [m][n]] [--redo [m]] [--if run] [--key]
            
```yaml
    # YAML format
    # If we want to do a 'ant deploy' from a Linux server (assume you have connected 
    # a server from a previously CONNECT command):
    - LINUX_COMMAND: ant deploy
```

    - PATH
        Description: Go to specific directory.
        Syntax: 
            PATH: directory [--continue [m][n]] [--redo [m]] [--if run] [--key]

```yml
    # YAML format
    # Go to directory c:\users
    - PATH: c:\users
```

    - GET_XML_TAG_TEXT
        Description: Get a xml tag text value from xml file.                                         
                     The result will be stored into tube variables.
        Syntax: 
            GET_XML_TAG_TEXT: -f file -x xpath [--continue [m][n]] [--redo [m]] [--if run]  [--key]
```yml
    # YAML format
    # Get app-api-version value from pom.xml file using xpath:
    - GET_XML_TAG_TEXT: -f pom.xml -x properties/app-api-version
```

    - SET_XML_TAG_TEXT
        Description: Update XML file tag text using xpath.
        Syntax: 
            SET_XML_TAG_TEXT: -f file -x xpath -v value [--continue [m][n]] [--redo [m]] [--if run] [--key] 
```yml
    # YAML format
    # Set app-api-version value from pom.xml file using xpath:
    - SET_XML_TAG_TEXT: -f pom.xml -x properties/app-api-version -v 2022.1
```

    - SET_FILE_KEY_VALUE
        Description: Update key-value file.
        Syntax: 
            SET_FILE_KEY_VALUE: -f file -k key -v value [--continue [m][n]] [--redo [m]] [--if run] [--key]

```yml
    # YAML format
    # Update command=update in build.properties file:
    - SET_FILE_KEY_VALUE: -f build.properties -k command -v update
```

    - WRITE_LINE_IN_FILE
        Description: Write any characters into a file.
        The value also could be one of them: '$NLB' (NEW_LINE_BEFORE), '$NLA' (NEW_LINE_AFTER),'$DL (DELETE_LINE) 
        If you need more than two space characters in the value content, you can use {s:m} (m > 0) 
        The 'm' means how many spaces you want.
        eg: -v {s:5}hello => will be translated to 5 space chars plus hello: '     hello'
        Parameters:
        -n parameter: Write line in which line number.
        -c parameter: Write line which line contains specific characters.
        -v parameter: The character (content) you want to write into the file.
        Syntax: 
            WRITE_LINE_IN_FILE: -f file [-n line-number] [-c contains] -v value | $file [--continue [m][n]] [--redo [m]] [--if run] [--key]

```yml
    # YAML format
    # Append 'command=update' into build.properties file:
    - WRITE_LINE_IN_FILE: -f build.properties -v command=update
```
    - DELETE_LINE_IN_FILE
        Description: Delete line which characters begin or contains with given value. -e means delete empty line.
        Syntax: 
            DELETE_LINE_IN_FILE: -f file [-b begins] [-c contains] [-e] [--continue [m][n]] [--redo [m]] [--if run] [--key]
            
```yml
    # YAML foramt
    # Delete line which begin with 'command='
    - DELETE_LINE_IN_FILE: -f build.properties -b command=
```

    - PAUSE
        Description: Programming Tube will pause with given minutes.
        Syntax: 
            PAUSE: minutes [--continue [m][n]] [--redo [m]] [--if run] [--key]

```yml
    # YAML foramt
    # Pause for 30.5 minutes:
    - PAUSE: 30.5
```

    - TAIL_FILE
        Description: Print/Log the last N lines given file.                                 
                     If keywords were given, then only tail the file                                 
                     when the keywords exist from those lines.
        Syntax: 
            TAIL_FILE: -f file -l lines [-k keywords] [--continue [m][n]] [--redo [m]] [--if run] [--key]

```yml
    # YAML format
    # Output last 25 lines if it contains 'error' or 'failure' keywords
    - TAIL_FILE: -f build.log -l 25 -k error,failure
```

    - REPORT_PROGRESS
        Description: You can use this command to sent current progress via Email.
        Syntax: 
            REPORT_PROGRESS: subject [--continue [m][n]] [--redo [m]] [--if run] [--key]

```yml
    # YAML format
    - REPORT_PROGRESS: Email subject
```

    - GET_FILE_KEY_VALUE
        Description: Read key values from key-value file.                                         
                     The key-value results will be stored into tube variables.
        Syntax: 
            GET_FILE_KEY_VALUE: -f file [-k key[,key][...]] [--continue [m][n]] [--redo [m]] [--if run] [--key]
        
```yml
    # YAML format
    - GET_FILE_KEY_VALUE: -k key -f file
```

    - EMAIL
        Description: Sent Email to somebody with given subject and content.
                     The -b parameter supports text file content as email body when it's text file.
        Syntax: 
            EMAIL: -t addressA[,addressB][...] -s subject -b body | $file [--continue [m][n]] [--redo [m]] [--if run] [--key]
        
```yml
    # YAML format
    - EMAIL: -t michael_hll@hotmail.com -s Hello to you -b email-body.txt
```

    - IMPORT_TUBE
        Description: Import tube commands, servers, variables or emails from sub tube yaml file.
        Syntax: 
            IMPORT_TUBE: file [--continue [m][n]] [--redo [m]] [--if run] [--key]

```yml
    # YAML format
    - IMPORT_TUBE: sub-tube.yaml
```

    - COUNT
        Description: Count file lines number (-f) or tube command number by status (-t).                                          
                The -c flag means if count within current tube. Default no.                                          
                The -s flag means if skip COUNT command. Defalult no.                                          
                The count result will be stored into tube variable using -v parameter.
        Syntax: 
            COUNT: -f file | -t statusA,B,.. -v variable [-c] [-s] [--continue [m][n]] [--redo [m]] [--if run] [--key]

```yml
    # YAML format
    - COUNT: -f file -v lines_count
```

    - SET_VARIABLE
        Description: Set tube variable value.
        Syntax: 
            SET_VARIABLE: -n name -v value [--continue [m][n]] [--redo [m]] [--if run] [--key]

```yml
    # YAML format
    - SET_VARIABLE: -n var_name -v value
```
