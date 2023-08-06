# -*- coding: utf-8 -*-
"""
Created on Sat May  8 12:37:45 2021

@author: avik_
"""
import datetime,os,sys

def logger(logger_no, function_name, task_status = '', path_output = '', other=''):
    '''
    You need to call this function at TRY block
    
    Var 1 : Pass the file name you want to create
    Var 2 : Pass Function name if you want to track function wise logs. To do this, you want keep this call at Function Level
    Var 3 : If you want to give any specific value as Task Status
    Var 4 : Path where you want to create the log file. Please pass value as string.
    Var 5 : If any other parameter you want keep track
    '''
    try :
        if logger_no == '':
            logger_no = "Mention Logger Number"
        if function_name == '':
            function_name = "Mention Funtion Name"
        if task_status == '':
            task_status = "Code Status Healthy"
        # if error == '':
        error = "No Error"
        
        if other == '':
            other = ""
        if path_output == '':
            log_file = open(os.getcwd() + '/' + logger_no + '.txt', 'a+')
            print("1.var1 = directory where log file will be created || 2.var2 = Logger number ||\
                  3.var3 = Function name || 4.var4 = Task status || 5.var5 = Error || 6.var6 = Output path || 7.var7 = other Link")
            log_file.write("========================================================\n")
            log_file.write("\n<<<<<<<<<<<<<<<<<<<< Logger Log Data >>>>>>>>>>>>>>>>>>>>>\n")
            log_file.write("========================================================\n")
            log_file.writelines(["<<<<<<<<<<<<<Logger Number : >>>>>>>>>>>> \n", logger_no]) 
            log_file.writelines(["\n<<<<<<<<<<<<<Funtion Name : >>>>>>>>>>>>> \n", function_name])
            log_file.writelines(["\n<<<<<<<<<<<<Task Status : >>>>>>>>>>>>>>> \n", task_status])
            log_file.writelines(["\n<<<<<<<<<<<< Error : >>>>>>>>>>>>>>>>>>>> \n", error])
            log_file.writelines(["\n<<<<<<<<<<<< Output Path : >>>>>>>>>>>>>> \n", path_output])
            log_file.writelines(["\n<<<<<<<<<<<< other Link : >>>>>>>>>>>>>>>>> \n", other])
            log_file.writelines(["\n<<<<<<<<<<<< Logged Time : >>>>>>>>>>>>>> \n", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
            log_file.write("\n===============================================\n")
            log_file.write("===============================================\n")
            log_file.close()
            print("Logger Logs Stored !!!") 
        else:
            log_file = open(path_output + '/' + logger_no + '.txt', 'a+')
            print("1.var1 = directory where log file will be created || 2.var2 = Logger number ||\
                  3.var3 = Function name || 4.var4 = Task status || 5.var5 = Error || 6.var6 = Output path || 7.var7 = other Link")
            log_file.write("========================================================\n")
            log_file.write("\n<<<<<<<<<<<<<<<<<<<< Logger Log Data >>>>>>>>>>>>>>>>>>>>>\n")
            log_file.write("========================================================\n")
            log_file.writelines(["<<<<<<<<<<<<<Logger Number : >>>>>>>>>>>> \n", logger_no]) 
            log_file.writelines(["\n<<<<<<<<<<<<<Funtion Name : >>>>>>>>>>>>> \n", function_name])
            log_file.writelines(["\n<<<<<<<<<<<<Task Status : >>>>>>>>>>>>>>> \n", task_status])
            log_file.writelines(["\n<<<<<<<<<<<< Error : >>>>>>>>>>>>>>>>>>>> \n", error])
            log_file.writelines(["\n<<<<<<<<<<<< Output Path : >>>>>>>>>>>>>> \n", path_output])
            log_file.writelines(["\n<<<<<<<<<<<< other Link : >>>>>>>>>>>>>>>>> \n", other])
            log_file.writelines(["\n<<<<<<<<<<<< Logged Time : >>>>>>>>>>>>>> \n", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
            log_file.write("\n===============================================\n")
            log_file.write("===============================================\n")
            log_file.close()
            print("Logger Logs Stored !!!") 
            
    except Exception as err:
        # pass
        if path_output == '':
            error = 'While running code Logger Exception Error occured'
            exception_type, exception_object, exception_traceback = sys.exc_info()
            print('Input Data issues: ',  exception_type, exception_object, exception_traceback)
            log_file = open(os.getcwd() +'/'+ logger_no + '.txt', 'a+')
            log_file.write("========================================================\n")
            log_file.write("\n<<<<<<<<<<<<<<<< Logger Exception Data >>>>>>>>>>>>>>>\n")
            log_file.write("========================================================\n")
            log_file.writelines(["\n<<<<<<<<<<< Logger_Exception_Error >>>>>>>>>>\n", str(err.args[0])])
            log_file.writelines(["<<<<<<<<<<<<<Logger Number : >>>>>>>>>>>> \n", logger_no]) 
            log_file.writelines(["\n<<<<<<<<<<<<<Funtion Name : >>>>>>>>>>>>> \n", function_name])
            log_file.writelines(["\n<<<<<<<<<<<<Task Status : >>>>>>>>>>>>>>> \n", task_status])
            log_file.writelines(["\n<<<<<<<<<<<< Error : >>>>>>>>>>>>>>>>>>>> \n", error])
            log_file.writelines(["\n<<<<<<<<<<<< Output Path : >>>>>>>>>>>>>> \n", path_output])
            log_file.writelines(["\n<<<<<<<<<<<< other Link : >>>>>>>>>>>>>>>>> \n", other])
            log_file.writelines(["\n<<<<<<<<< Exception Type : >>>>>>>>>>>>>> \n", str(exception_type)])
            log_file.writelines(["\n<<<<<<<<< Exception Object : >>>>>>>>>>>> \n", str(exception_object)])
            log_file.writelines(["\n<<<<<<< Exception Traceback : >>>>>>>>>>> \n", str(exception_traceback)])
            log_file.writelines(["\n<<<<<<<<<<<< Logged Time : >>>>>>>>>>>>>> \n", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
            log_file.write("\n===============================================\n")
            log_file.write("===============================================\n")
            log_file.close()
            print("Logger exception Logs Stored !!!")
        else:
            error = 'While running code Logger Exception Error occured'
            exception_type, exception_object, exception_traceback = sys.exc_info()
            print('Input Data issues: ',  exception_type, exception_object, exception_traceback)
            log_file = open(os.getcwd() +'/'+ logger_no + '.txt', 'a+')
            log_file.write("========================================================\n")
            log_file.write("\n<<<<<<<<<<<<<<<< Logger Exception Data >>>>>>>>>>>>>>>\n")
            log_file.write("========================================================\n")
            log_file.writelines(["\n<<<<<<<<<<< Logger_Exception_Error >>>>>>>>>>\n", str(err.args[0])])
            log_file.writelines(["<<<<<<<<<<<<<Logger Number : >>>>>>>>>>>> \n", logger_no]) 
            log_file.writelines(["\n<<<<<<<<<<<<<Funtion Name : >>>>>>>>>>>>> \n", function_name])
            log_file.writelines(["\n<<<<<<<<<<<<Task Status : >>>>>>>>>>>>>>> \n", task_status])
            log_file.writelines(["\n<<<<<<<<<<<< Error : >>>>>>>>>>>>>>>>>>>> \n", error])
            log_file.writelines(["\n<<<<<<<<<<<< Output Path : >>>>>>>>>>>>>> \n", path_output])
            log_file.writelines(["\n<<<<<<<<<<<< other Link : >>>>>>>>>>>>>>>>> \n", other])
            log_file.writelines(["\n<<<<<<<<< Exception Type : >>>>>>>>>>>>>> \n", str(exception_type)])
            log_file.writelines(["\n<<<<<<<<< Exception Object : >>>>>>>>>>>> \n", str(exception_object)])
            log_file.writelines(["\n<<<<<<< Exception Traceback : >>>>>>>>>>> \n", str(exception_traceback)])
            log_file.writelines(["\n<<<<<<<<<<<< Logged Time : >>>>>>>>>>>>>> \n", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
            log_file.write("\n===============================================\n")
            log_file.write("===============================================\n")
            log_file.close()
            print("Logger exception Logs Stored !!!")
    # return "Logs Stored !!!" 
    
##############################################################################################################
# Exception Logger
##############################################################################################################
def exceptionlogger(logger_no, function_name, task_status, path_output, other, e):
    '''
    You need to call this funcion at EXCEPTION bloack
    
    Var 1 : Pass the file name you want to create
    Var 2 : Pass Function name if you want to track function wise logs. To do this, you want keep this call at Function Level
    Var 3 : If you want to give any specific value as Task Status
    Var 4 : Path where you want to create the log file. Please pass value as string.
    Var 5 : If any other parameter you want keep track
    Var 6 : Please pass the exception value. Example : except Exception as e
    '''
    try :
        if logger_no == '':
            logger_no = "Mention Logger Number"
        if function_name == '':
            function_name = "Mention Funtion Name"
        if task_status == '':
            task_status = "Exception Occured"
        # if error == '':
        #     error = "No Error"
       
        if other == '':
            other = ""
        exception_type, exception_object, exception_traceback = sys.exc_info()
        if path_output == '':
            log_file = open(os.getcwd() + '/' + logger_no + '.txt', 'a+')
            print("1.var1 = directory where log file will be created || 2.var2 = Logger number ||\
                  3.var3 = Function name || 4.var4 = Task status || 5.var5 = Error || 6.var6 = Output path || 7.var7 = other Link")
            log_file.write("========================================================\n")
            log_file.write("\n<<<<<<<<<<<<<< ExceptionLogger Log Data >>>>>>>>>>>>>>\n")
            log_file.write("========================================================\n")
            log_file.writelines(["<<<<<<<<<<<<<Logger Number : >>>>>>>>>>>> \n", logger_no]) 
            log_file.writelines(["\n<<<<<<<<<<<<<Funtion Name : >>>>>>>>>>>>> \n", function_name])
            log_file.writelines(["\n<<<<<<<<<<<<Task Status : >>>>>>>>>>>>>>> \n", task_status])
            log_file.writelines(["\n<<<<<<<<<<<< Error : >>>>>>>>>>>>>>>>>>>> \n", str(e)])
            log_file.writelines(["\n<<<<<<<<<<<< Output Path : >>>>>>>>>>>>>> \n", path_output])
            log_file.writelines(["\n<<<<<<<<<<<< other Link : >>>>>>>>>>>>>>>>> \n", other])
            log_file.writelines(["\n<<<<<<<<< Exception Type : >>>>>>>>>>>>>> \n", str(exception_type)])
            log_file.writelines(["\n<<<<<<<<< Exception Object : >>>>>>>>>>>> \n", str(exception_object)])
            log_file.writelines(["\n<<<<<<< Exception Traceback : >>>>>>>>>>> \n", str(exception_traceback)])
            log_file.writelines(["\n<<<<<<<<<<<< Logged Time : >>>>>>>>>>>>>> \n", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
            log_file.write("\n===============================================\n")
            log_file.write("===============================================\n")
            log_file.close()
            print("Exception logger Logs Stored !!!")
        else:
            log_file = open(path_output + '/' + logger_no + '.txt', 'a+')
            print("1.var1 = directory where log file will be created || 2.var2 = Logger number ||\
                  3.var3 = Function name || 4.var4 = Task status || 5.var5 = Error || 6.var6 = Output path || 7.var7 = other Link")
            log_file.write("========================================================\n")
            log_file.write("\n<<<<<<<<<<<<<< ExceptionLogger Log Data >>>>>>>>>>>>>>\n")
            log_file.write("========================================================\n")
            log_file.writelines(["<<<<<<<<<<<<<Logger Number : >>>>>>>>>>>> \n", logger_no]) 
            log_file.writelines(["\n<<<<<<<<<<<<<Funtion Name : >>>>>>>>>>>>> \n", function_name])
            log_file.writelines(["\n<<<<<<<<<<<<Task Status : >>>>>>>>>>>>>>> \n", task_status])
            log_file.writelines(["\n<<<<<<<<<<<< Error : >>>>>>>>>>>>>>>>>>>> \n", str(e)])
            log_file.writelines(["\n<<<<<<<<<<<< Output Path : >>>>>>>>>>>>>> \n", path_output])
            log_file.writelines(["\n<<<<<<<<<<<< other Link : >>>>>>>>>>>>>>>>> \n", other])
            log_file.writelines(["\n<<<<<<<<< Exception Type : >>>>>>>>>>>>>> \n", str(exception_type)])
            log_file.writelines(["\n<<<<<<<<< Exception Object : >>>>>>>>>>>> \n", str(exception_object)])
            log_file.writelines(["\n<<<<<<< Exception Traceback : >>>>>>>>>>> \n", str(exception_traceback)])
            log_file.writelines(["\n<<<<<<<<<<<< Logged Time : >>>>>>>>>>>>>> \n", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
            log_file.write("\n===============================================\n")
            log_file.write("===============================================\n")
            log_file.close()
            print("Exception logger Logs Stored !!!")
    except Exception as err:
        # pass
        exception_type, exception_object, exception_traceback = sys.exc_info()
        # print('Input Data issues: ',  exception_type, exception_object, exception_traceback)
        if path_output == '':
            log_file = open(os.getcwd() +'/'+ logger_no + '.txt', 'a+')
            log_file.write("========================================================\n")
            log_file.write("\n<<<<<<<<< ExceptionLogger Log Exception Data >>>>>>>>>\n")
            log_file.write("========================================================\n")
            log_file.writelines(["\n<<<<<<<<<<<Exception Logger Exception Error >>>>>>>>>>\n", err.args[0]])
            log_file.writelines(["<<<<<<<<<<<<<Logger Number : >>>>>>>>>>>> \n", logger_no]) 
            log_file.writelines(["\n<<<<<<<<<<<<<Funtion Name : >>>>>>>>>>>>> \n", function_name])
            log_file.writelines(["\n<<<<<<<<<<<<Task Status : >>>>>>>>>>>>>>> \n", task_status])
            log_file.writelines(["\n<<<<<<<<<<<< Error : >>>>>>>>>>>>>>>>>>>> \n", e])
            log_file.writelines(["\n<<<<<<<<<<<< Output Path : >>>>>>>>>>>>>> \n", path_output])
            log_file.writelines(["\n<<<<<<<<<<<< other Link : >>>>>>>>>>>>>>>>> \n", other])
            log_file.writelines(["\n<<<<<<<<< Exception Type : >>>>>>>>>>>>>> \n", str(exception_type)])
            log_file.writelines(["\n<<<<<<<<< Exception Object : >>>>>>>>>>>> \n", str(exception_object)])
            log_file.writelines(["\n<<<<<<< Exception Traceback : >>>>>>>>>>> \n", str(exception_traceback)])
            log_file.writelines(["\n<<<<<<<<<<<< Logged Time : >>>>>>>>>>>>>> \n", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
            log_file.write("\n===============================================\n")
            log_file.write("===============================================\n")
            log_file.close()
            print("Exception Logger exception Logs Stored !!!")
        else:
            log_file = open(path_output +'/'+ logger_no + '.txt', 'a+')
            log_file.write("========================================================\n")
            log_file.write("\n<<<<<<<<< ExceptionLogger Log Exception Data >>>>>>>>>\n")
            log_file.write("========================================================\n")
            log_file.writelines(["\n<<<<<<<<<<<Exception Logger Exception Error >>>>>>>>>>\n", err.args[0]])
            log_file.writelines(["<<<<<<<<<<<<<Logger Number : >>>>>>>>>>>> \n", logger_no]) 
            log_file.writelines(["\n<<<<<<<<<<<<<Funtion Name : >>>>>>>>>>>>> \n", function_name])
            log_file.writelines(["\n<<<<<<<<<<<<Task Status : >>>>>>>>>>>>>>> \n", task_status])
            log_file.writelines(["\n<<<<<<<<<<<< Error : >>>>>>>>>>>>>>>>>>>> \n", e])
            log_file.writelines(["\n<<<<<<<<<<<< Output Path : >>>>>>>>>>>>>> \n", path_output])
            log_file.writelines(["\n<<<<<<<<<<<< other Link : >>>>>>>>>>>>>>>>> \n", other])
            log_file.writelines(["\n<<<<<<<<< Exception Type : >>>>>>>>>>>>>> \n", str(exception_type)])
            log_file.writelines(["\n<<<<<<<<< Exception Object : >>>>>>>>>>>> \n", str(exception_object)])
            log_file.writelines(["\n<<<<<<< Exception Traceback : >>>>>>>>>>> \n", str(exception_traceback)])
            log_file.writelines(["\n<<<<<<<<<<<< Logged Time : >>>>>>>>>>>>>> \n", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
            log_file.write("\n===============================================\n")
            log_file.write("===============================================\n")
            log_file.close()
            print("Exception Logger exception Logs Stored !!!")
        # log_file.close()
        # return "Logs Stored !!!"
##############################################################################################################         
# def exceptiondetail():
#     exception_type, exception_object, exception_traceback = sys.exc_info()
#     return exceptionlogger(logger_no, function_name, task_status, error, path_output, other,exception_type, exception_object, exception_traceback)

# logger('log3','loggertest','','/fgh','http://test.com123') #
