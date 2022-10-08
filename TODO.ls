TODO LIST

- FILE 
    exists, delete, copy, move, create. etc
    FILE_READ: -f|--file file -v|--variable variable
    FILE_POP: -f file -v variable
    FILE_APPEND: -f file -v value
    FILE_PUSH: -f file -v value
    FILE_EXIST: -f|--file
    FILE_DELETE: -f|--file
    FILE_CREATE: -f|--file
    FILE_COPY: -f|--file file -t|--to to (file or directory) 
    FILE_MOVE: -f|--file file -t|--to to (file or directory) 
    
- DIR
    exists, delete, copy, move, create. etc
    DIR_EXIST: -d|--directory directory
    DIR_DELETE: -d
    DIR_CREATE: -d
    DIR_COPY: -d directory -t to (directory)

- DISCONNECT command ??

- System Test

- Refactor run method

- check --rodo log

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



