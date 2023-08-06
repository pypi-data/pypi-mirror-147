**#Developer : Avik Das**

*##Steps to run the package :*

1. pip install pkglogger==<version number>
2. from pkglogger import pkglogger

*logger()*
'''
You need to call this function at TRY block

Var 1 : Pass the file name you want to create
Var 2 : Pass Function name if you want to track function wise logs. To do this, you want keep this call at Function Level
Var 3 : If you want to give any specific value as Task Status
Var 4 : Path where you want to create the log file. Please pass value as string.
Var 5 : If any other parameter you want keep track
'''

*exceptionlogger()*
'''
You need to call this funcion at EXCEPTION bloack

Var 1 : Pass the file name you want to create
Var 2 : Pass Function name if you want to track function wise logs. To do this, you want keep this call at Function Level
Var 3 : If you want to give any specific value as Task Status
Var 4 : Path where you want to create the log file. Please pass value as string.
Var 5 : If any other parameter you want keep track
Var 6 : Please pass the exception value. Example : except Exception as e
'''

*Return the exception details as well *
