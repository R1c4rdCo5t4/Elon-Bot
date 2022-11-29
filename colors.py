from enum import Enum

# ANSI Escape Codes enum class
class Colors(Enum):
    red='\033[31m'
    green='\033[32m'
    lightgrey='\033[37m'
    darkgrey='\033[90m'
    lightred='\033[91m' 
    yellow='\033[93m'
    black= '\033[30m'
    blue= '\033[34m'
    magenta= '\033[35m'
    cyan= '\033[36m'
    white= '\033[37m'
    
