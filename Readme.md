# Programming Tube

#### Update Date: Feb 2022

---
## Introduction
    Programming Tube is a tool that can run a group of sequenced commands at a future datetime. 

    Those commands are added from a YAML config file, which I usually call a tube file. See the examples from the templates folder. When you run this program, you can use the -y | --yaml parameter to specify the config file.
    
    The commands could include normal terminal commands run from Windows, MacOS and Linux systems. Besides that, Programming Tube also adds additional tube commands which can achieve more tasks. From below 'Examples of Each Command' you could get more information.
---
## How to run Programming Tube
    Programming Tube is a Python 3 script. The most important two arguments for Programming Tube are '--yaml' and '--datetime'.    
    All the tube configurations are maintained by a YAML file, using '--yaml file' you can specify the tube configurations. From the 'xxx.template.yaml' you could view how it looks like.
    Use '--datetime' argument you could set the execution time, you could also run it at once by parameter '-f' or '-i'.
    For more information about input arguments please use following command from your terminal (In MacOS, you may need Python3):
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
        6: Find command name contains 'file' keyword:
        >>> python programming-tube.py help file
        
        ** Find tube running result from tube.yaml.log file
                 
### - Binary Mode        
        Following below steps you can use it in binary mode
        1. In order to generate binary exe file, you need to install pyinstaller
        >>> pip install pyinstaller
        2. Then compile programming-tube.py to exe file:
        (programming-tube.exe will be generated in the dist folder)
        >>> pyinstaller --onefile programmingtube.py
        3. Using it from your terminal (This exe don't need Python to run):
        (You need to change RUN_MODE from SRC to BIN in YAML config file)
        >>> programming-tube -y tube.yaml -f   
       
---
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
            bl_root_folder: C:\workspaces\\fin-trunk\\trunk
            fin_package_name: financials-qra-app
            cmd_parameters: -l
            # Below are default hidden variables:
            s: ' ' # Its value is a space char and can't be overridden
        Then you can reference any variable value via {var-name} in your tube 
        command arguments. eg:
            - PATH: {bl_root_folder}
            - COMMAND: ls {cmd_parameters}
            # The below {s:10} will be replaced by 10 space chars 
            - WRITE_LINE_IN_FILE: -f file -v {s:10}any line content here  
        The below commands will update the tube variables:
            - GET_XML_TAG_TEXT => xpath will be the variable name
            - GET_PACKAGE_VERSION => package will be the variable name
            - GET_FILE_KEY_VALUE => key(s) will be the variable name
            - COUNT => variable will be tored into tube
            - SET_VARIABLE => update tube variable by name value
        Note: If variable was updated from console inputs, then it can't be udpated again. 
---
## Examples of Each Command
    - LINUX_COMMAND
        Description: Run a Linux command from the previous connected server.
        Syntax: 
            LINUX_COMMAND: command [--redo [m]] [--continue [m] [n]] [--if run]
            
            
```json
    //  JSON format
    // --redo -1 means if this step failed, the previous step plus current step will be executed again
    {
        "LINUX_COMMAND" : "yab udpate --continue --redo -1"
    }
    // If current command failed, then 1 step will be skipped after current
    // If current command successful, then the second step will be skipped after current
    {
        "LINUX_COMMAND" : "yab udpate --continue --redo --continue 1 1"
    }
```
```yaml
    # YAML format
    # --redo -1 means if this step failed, the previous step plus current step will be execute again
    - LINUX_COMMAND: yab udpate --continue --redo -1
    # If current command failed, then 1 step will be skipped after current
    # If current command successful, then the second step will be skipped after current
    - LINUX_COMMAND: yab udpate --continue --redo -1 --continue 1 1
```

    - PATH
        Description: Go to specific directory.
        Syntax:
            PATH: directory [--continue [m][n]] [--redo [m]] [--if run]
      
        The following settings, program will goto directory 'c:/users'
```json
    // JSON format
    {
        "PATH" : "c:/users"
    }
```
```yml
    # YAML format
    - PATH: c:\users
```

    - COMMAND
        Description: Run any Windows/MacOS ternimal command.
        Syntax: 
            COMMAND: command [--redo [m]] [--continue [m] [n]] [--if run]

```json
    // JSON format
    // --redo -1 means if this step failed, the previous step plus current step will be execute again
    {
        "COMMAND" : "ant clean --continue"
    },
    {
        "COMMAND" : "ant clean --redo"
    },
    {
        "COMMAND" : "ant clean --redo -1 --continue"
    }
```
```yml
    # YAML format
    # --redo -1 means if this step failed, the previous step plus current step will be execute again
    - COMMAND: ant clean --continue
    - COMMAND: ant clean --redo
    - COMMAND: ant clean --redo -1 --continue
```

    - GET_XML_TAG_TEXT
        Description: Get a xml tag text value from xml file.
        Syntax:
            GET_XML_TAG_TEXT: -f file -x xpath [--continue [m][n]] [--redo [m] [--if run]
```json
    // JSON format
    {
        "GET_XML_TAG_TEXT": "-f pom.xml -x properties/financials-api-version"
    }
```
```yml
    # YAML format
    - GET_XML_TAG_TEXT: -f pom.xml -x properties/financials-api-version
```

    - SET_XML_TAG_TEXT
        Description: Update XML file tag text using xpath.
        Syntax:
            SET_XML_TAG_TEXT: -f file -x xpath -v value [--continue [m][n]] [--redo [m]] [--if run]
```json
    // JSON format
    {
        "SET_XML_TAG_TEXT": "-f pom.xml -x properties/financials-api-version -v 2022.1"
    }
```
```yml
    # YAML format
    - SET_XML_TAG_TEXT: -f pom.xml -x properties/financials-api-version -v 2022.1
```

    - SET_FILE_KEY_VALUE
        Description: Update key-value file.
        Syntax:
            SET_FILE_KEY_VALUE: -f file -k key -v value [--continue [m][n]] [--redo [m]] [--if run]
```json
    // JSON format
    {
        "SET_FILE_KEY_VALUE": "-f Trunk CopyJars Financials.bat -k SET VERSION -v {properties/financials-api-version}"
    }
```
```yml
    # YAML foramt
    - SET_FILE_KEY_VALUE: -f Trunk CopyJars Financials.bat -k SET VERSION -v {properties/financials-api-version}
```
        Below example will update the CopyJars bat file with a specific value
```json
    // JSON format
    {
        "SET_FILE_KEY_VALUE": "-f Trunk CopyJars Financials.bat -k SET VERSION -v 2.20220.0.152"
    }
```
```yml
    # YAML format
    - SET_FILE_KEY_VALUE: -f Trunk CopyJars Financials.bat -k SET VERSION -v 2.20220.0.152
```

        Below example will turn on 'command=update' and turn off for all others 'command=xxx'
```json
    // JSON format
    {
        "SET_FILE_KEY_VALUE": "-f build.properties -k command -v update"
    }
```
```yml
    # YAML format
    - SET_FILE_KEY_VALUE: -f build.properties -k command -v update
```

    - WRITE_LINE_IN_FILE
        Description: Write any characters into a file.
        Syntax:
            WRITE_LINE_IN_FILE: -f file [-n line-number] [-c contains] -v value | $file [--continue [m][n]] [--redo [m]] [--if run]

            The value also could be one of them: '$NLB' (NEW_LINE_BEFORE), '$NLA' (NEW_LINE_AFTER),'$DL (DELETE_LINE)
            If you need more than two space characters in the value content, you can use {s:m} (m > 0) 
            The 'm' means how many spaces you want.
            eg: -v {s:5}hello => will be translated to 5 space chars plus hello: '     hello'
```json
    // JSON format
    {
        "WRITE_LINE_IN_FILE": "-f pre-startup.sh -n 15 -v NEW_LINE_AFTER",
        "WRITE_LINE_IN_FILE": "-f pre-startup.sh -n 16 -v mounting /qad/local/sandbox/fin93 to /mnt/fin93 ..."
    }
```
```yml
    # YAML format
    - WRITE_LINE_IN_FILE: -f pre-startup.sh -n 15 -v NEW_LINE_AFTER
    - WRITE_LINE_IN_FILE: -f pre-startup.sh -n 16 -v mounting /qad/local/sandbox/fin93 to /mnt/fin93 ...
```
    - DELETE_LINE_IN_FILE
        Description: Delete line which characters begin or contains with given value. -e means delete empty line.
        Syntax:
            DELETE_LINE_IN_FILE: -f file [-b begins] [-c contains] [-e] [--continue [m][n]] [--redo [m]] [--if run]
            
```json
    // JSON format
    {
        "DELETE_LINE_IN_FILE": "-f configuration.properties -b packages.financials="
    }
```
```yml
    # YAML foramt
    - DELETE_LINE_IN_FILE: -f configuration.properties -b packages.financials=
```

    - PAUSE
        Description: Programming Tube will pasuse given minutes.
        Syntax:
            PAUSE: minutes [--continue [m][n]] [--redo [m]] [--if run]
            minutes is a float type parameter.
```json
    // JSON format
    {
        "PAUSE": 30.5  
    }
```
```yml
    # YAML foramt
    - PAUSE: 30.5
```

    - GET_PACKAGE_VERSION
        Description: Get latest version of package from packages.qad.com
        Syntax:
            GET_PACKAGE_VERSION: -p package -s start -e end [--continue [m][n]] [--redo [m]] [--if run]
```json
    // JSON format
    {
        "GET_PACKAGE_VERSION": "-p enterprise-financials-app -s 2020.1 -e 2020.2"
    },
    {
        "SET_FILE_KEY_VALUE": "-f configuration.properties -k packages.enterprise-financials-app -v {enterprise-financials-app}"
    }
```
```yml
    # YAML foramt
    - GET_PACKAGE_VERSION: -p enterprise-financials-app -s 2020.1 -e 2020.2
    - SET_FILE_KEY_VALUE: -f configuration.properties -k packages.enterprise-financials-app -v {enterprise-financials-app}
```

    - TAIL_FILE
        Description: Print/Log the last N lines given file. 
                     If keywords were given, then only tail the file
                     when the keywords exist from those lines.
        Syntax:
            TAIL_FILE: -f file -l lines [-k keywords] [--continue [m][n]] [--redo [m] [--if run]
```json
    // JSON format
    {
        "TAIL_FILE": "-f as-qra.server.log -l 25 -k error,failure"
    }
```
```yml
    # YAML format
    - TAIL_FILE: -f as-qra.server.log -l 25 -k error,failure
```

    - CONNECT
        Description: You can use this command to swith your server connection.
        Syntax:
            CONNECT: server [--redo [m]] [--continue [m][n]] [--if run]

```json
    // JSON format
    {
        "CONNECT": "vmlxxx0001.qad.com"
    }
```
```yml
    # YAML format
    - CONNECT: vmlxxx0001.qad.com
```

    - REPORT_PROGRESS
        Description: You can use this command to sent current progress via Email.
        Syntax:
            REPORT_PROGRESS: Email subject [--continue [m][n]] [--redo [m]] [--if run]
```json
    // JSON format
    {
        "REPORT_PROGRESS": "Email subject"
    }
```
```yml
    # YAML format
    - REPORT_PROGRESS: Email subject
```

    - GET_FILE_KEY_VALUE
        Description: Read key values from key-value file. These values are
                   stored into the tube variables.
        Syntax:
            GET_FILE_KEY_VALUE: -f file [-k key[,key][...]] [--continue [m][n]] [--redo [m] [--if run]
        
```json
    // JSON format
    {
        "GET_FILE_KEY_VALUE": "-k key -f file --continue 1 1 --redo"
    }
```
```yml
    # YAML format
    - GET_FILE_KEY_VALUE: -k key -f file --continue 1 1 --redo
```

    - EMAIL
        Description: Sent Email to somebody with given subject and content.
        Syntax:
            EMAIL: -t addressA[,addressB][...] -s subject -b body | $file [--continue [m][n]] [--redo [m] [--if run]

            The -b parameter supports text file content as email body when it's text file.
        
```json
    // JSON format
    {
        "EMAIL": "-t michael_hll@hotmail.com -s Hello to you -b email-body.txt"
    }
```
```yml
    # YAML format
    - EMAIL: -t michael_hll@hotmail.com -s Hello to you -b email-body.txt
```

    - IMPORT_TUBE
        Description: Import tube commands, servers, variables or emails from sub tube yaml file.
        Syntax:
            IMPORT_TUBE: file [--continue [m][n]] [--redo[m]] [--if run]

```json
    // JSON format
    {
        "IMPORT_TUBE": "sub-cmd.yaml"
    }
```
```yml
    # YAML format
    - IMPORT_TUBE: sub-cmd.yaml
```

    - COUNT
        Description: Count file lines number (-f) or tube command number by status (-t).                                      
            The -c flag means if count within current tube. Default no.                                        
            The -s flag means if skip COUNT command. Defalult no.
        Syntax:
            COUNT: -f file | -t statusA,B,.. -v variable [-c] [-s] [--continue [m][n]] [--redo [m]] [--if run]

```json
    // JSON format
    {
        "COUNT": "-f file -v line_number"
    }
```
```yml
    # YAML format
    - COUNT: -f file -v line_number
```

    - SET_VARIABLE
        Description: Set tube variable value.
        Syntax:
            SET_VARIABLE: -n name -v value [--continue [m][n]] [--redo [m]] [--if run]

```json
    // JSON format
    {
        "SET_VARIABLE": "-n var_name -v value"
    }
```
```yml
    # YAML format
    - SET_VARIABLE: -n var_name -v value
```


## - THE END -