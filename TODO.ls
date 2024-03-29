
TODO LIST

- test search images and download images via tube

- Output Command.results to Email content - future

- DONE LIST
    1. Email content format - done
    2. TUBE yaml version check - done
    3. Test cases udpates - done
    4. Release version 2.0.0 Beta - done
    5. help vars: display 's', 'TUBE_HOME' - done
    6. FTP_GET, FTP_PUT support *.* or *.log files - done
    7. Read emails, servers from other yaml file - done
    8. CHECK_CHAR_EXISTS new command - done
    9. Run SQL: https://fedingo.com/python-script-to-run-sql-query/ ??
    10. Report status for each step via Email - done
    11. Set variable support expressions - done
    12. Read YAML file key values to variables - done
    13. Init LCB, RCB => Left Curly Bracket/Right Curly Bracket - done
    14. Disable print colors setting : has improved blue color for windows     
    15. --if condition use eval : keep currently
    16. update tube variable remove the warning keyword from the log message
    17. Add --debug-mode Enable debug mode, print tube variables update details
    18. COMMAND, LINUX_COMMAND: --disable-placeholder 
        not needed, since the missing placehoder from tube variables are fixed  
    19. Add TubeCommand run method to refactor the code 
    20.  - Command log output to logfile ??
        Now the error can output to the terminal and log file both
        stdout will always output to the terminal
    21. - Add TubeRunner class to to refactor the code    
    22. - RUN_TUBE -y|--yaml tube.yaml -w|--while conditions
    23. - IMPORT_TUBE 
        delete it, since it's replaced by RUN_TUBE
    24. - DELETE_LINE_IN_FILE 
        -n|--number: The line number you want to delete. eg: 1, -1
    25. - READ_LINE_IN_FILE 
        Read one line from a file
        -f file
        -n line number
        -v variable name
    26. 
        - LIST
        LIST_FILES: -d|--directory -r|--result file [-s|--sort time|name|size [asc|desc]] - done
        LIST_DIRS: -d|--directory -r|--result file [-s|--sort asc|desc] - done
    
    27. - RUN_TUBE: support internal tube
        RUN_TUBE: -y tube
        RUN_TUBE: -y x[tube]
        RUN_TUBE: -y y[tube]
        RUN_TUBE: -y z.yaml|z.yml

    28. - Change RUN_TUBE -y|--yaml parameter to -t|--tube
        Also change it to the command-tube input arguments

    29. - sub tube variable (local/scope tube variable) - done
        pass tube variable to sub tube - done

    30.
        - Adjust the tube commands that have the ability to store tube variables
        1. Need to decide if need is_override/is_force argument value
        2. Need to decide update globally or not?
        3. Need to rethink of this due to the local tube variables introduced

        Ans: 1. No need for the is_override argument, default override is set to true
            2. Should provide the is_force argument, to udpate readonly tube variable
            3. Provide the global argument, if the command is within sub tube, then default
                update the tube value in sub tube, otherwize or global is true, then
                update the tube value in global tube variables
    
    31. - Add console argument -c|--clear-log
        With this flag provided, then empty the log file content first

    32. - Add note property for each command: --note: note
        Then in the last status of each command, we can add this notes section

    33. - we need to set the tube command status to failed when update global tube variable failed

    34. - FILE 
        exists, delete, copy, move, create. etc
        FILE_READ: -f|--file file -v|--variable variable            - done
        FILE_POP: -f file [-v variable]                             - done
        FILE_APPEND: -f file -v value                               - done
        FILE_PUSH: -f file -v value                                 - done
        FILE_INSERT: -f file -v value -n line_number                - done
        FILE_EMPTY: -f file                                         - done
        FILE_EXIST: -f file -v variable                             - done
        FILE_DELETE: -f|--file                                      - done
        FILE_COPY: -f|--file file -t|--to to (file or directory)    - done
        FILE_MOVE: -f|--file file -t|--to to (file or directory)    - done
        FILE_CREATE: -f file                                        - done    
        FILE_SORT: -f file [-n] [-s asc|dsc]                        - done        

    35. - DIR
        exists, delete, copy, move, create. etc
        DIR_EXIST: -d|--directory directory         - done
        DIR_DELETE: -d                              - done
        DIR_CREATE: -d                              - done

    36. - Refactor run method
    
    37. - SET_VARIABLE
        local variable should be available in itself and its parent tube

    38. - TAIL_FILE
        should support -r|--result argument to store the tail lines into result file  

    39. - DEL_VARIABLE -n name -g 

    40. - COMMAND alias

    41. - FILE_DELETE: -r|--result result
        - DIR_DELETE: -r|--result result

    42. - PRINT_VARS: '*' -r|--result result

    43. - DELETE_LINE_IN_FILE: -r|--result to store the deleted content

    44. - System Test
        - auto test each command script         - done
        - check all command debug message       - done

    45. - position arguments for each commands
        some commands only has one must have argument that use position arguments

    46. - SET_VARIABLE: var["key"] = value

    47. - update help 
    
    48. - BREAK: break the tube loop

    49. - CONTINUE: continue the next loop

    50. - PRINT: message [--color red]

    51. - refactor help system
        support more argument: help command-name [name|desc|syntax|parameters|support]

    52. - set_var: ls[index] = expression

    53. - run_tube: --each item in ls

    54. - list_f: --variable to store the list result
        - tail_fail: --variable to store the tail result
        - list_dir: --variable to store the list result
    
    55. - keep user inputs tube command name (do not make it to upper cases)

    56. - Check 'Tube' key exists from the main yaml file 

    57. - Main tube name should always be 'TUBE', 'Tube', or 'tube'
          The other tube names are case sensitive
    
    58. - exec command was added

    59. - set command supplirt multiple dimension list
          - set: ls[0][0] = expression

    60. - --raw general argument was added to disable the placehodler specific command

    61. - positional argument can directly input tube yaml file to override the --tube argument value

    62. - Tube variable name can't use the python keywords

    63. - set_var: support assign plus expression
            eg: - set: x += 1
    
    64. - SET_TUBE command, can set tube's property:
            continue
            redo
            ending logic
    
    65. - Add --no-log flag to disable writting log file feature

    66. - placehoder can access object type variable's property - 2.0.2

    67. - print: --json 
            With --json argument print json data with formated structure - 2.0.3

    68. - Back to parent run folder when run command is finished - 2.0.3

    69. - SET_VARIABLE support '-=' now - 2.0.3
        - set: x -= -0.5

    70. - Add --raw-log general argument - 2.0.3
        This flag is handy when the command content's placehoder value is very long
        Then in the console log it's hard to distinguish command content and output content
        With this flag you can easily disable log command content placehoder values
    
    71. - CREATE_OJBECT: name tube command is added - 2.0.3
        use this command you can create a new object() type instance

    72. - set_var: support update object type variable's property value - 2.0.3
        - set: obj.property = value
        Note: When add requests method then this feature could be used
    
    73. - Requests popular methods to tube commands - 2.0.3
            - requests.get -- done
            - requests.post -- done
            - requests.delete -- done
            - requests.head -- done
            - requests.patch -- done
            - requests.options -- done
            - requests.put -- done
    
    74. - validation: check tube and variable names valid - 2.0.3

    75. - FILE_DOWNLOAD: --url url --file file - 2.0.3

    76. - GET_KEYS: -f file -k key1 > k1 - 2.0.3

    77. - EXEC: ls.reverse() - 2.0.3
          run tube variable's method
    
    - Integrate 3rd party or customized scripts as tube commands?? -- Thinking
      Added IMPORT_MODULE command can achieve this - 2.0.5
          
    - Bug list:
        1. A string value has position format, then it doesn't work: '{i:02d}' - workaround fixed 2.0.2
        2. GET_KEYS: If the value is number then convert it to number or float - fixed 2.0.2
        3. If the 'COMMAND' tube command has user prompt questions, the user can't see the question - fixed 2.0.2
        4. If one tube interation failed the tube continue run next, the tube should stopped running
           once one interation failed. -- fixed 2.0.2
        5. Fixed a python recursive issue
           Python default recursive stack is 1000
           Changed the TubeRunner from recursive to run in a loop to fix this issue
        6. Bug fix for --if condition logic
           Fixed case: s.starswith('test') doesn't work
        7. Make the total time more precise
           Make the command time more precise
        8. Add $-, {-} two system placehoders to used as '-' character


