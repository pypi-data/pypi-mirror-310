import sys 


DEBUG = "DEBUG"
OK = "OK"
WARN = "WARN"
WARNING = "WARNING"
CRITICAL = "CRITICAL"
ERROR = "ERROR"
UNKNOWN = "UNKNOWN"



def terminate_check(status, msg):
    # -----------------------------------------   
    #   DO NOT MODIFY THIS FUNCTION
    # -----------------------------------------    
    print(f"{status} - {msg}")
    if status == OK:
        sys.exit(0)
    elif status == WARNING:
        sys.exit(1)
    elif status == CRITICAL:
        sys.exit(2)
    else:
        sys.exit(3)
