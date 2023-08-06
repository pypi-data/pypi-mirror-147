# Cool logs
 Simple output beautifier for python 3

## Installation
You can install this package using `pip`:
```
pip install coollogs
```

## Basic usage
To use coollogs, you need to import `log` object from this module: 
```
from coollogs import log
log.success('Hello, logs!')
```  
The output will be as follows:  
![Examples](screenshots/basic_usage_output.png)

## Logging modes
When logging, each message will be prefixed with current time (hh:mm:ss) and
it's type. There are 10 built-in logging modes:
* Critical - for VERY important messages (red background)
* Error - for errors and stuff (red foreground)
* Warning - you guessed it: for warnings (orange foreground)
* Info - for defaulft logging (cyan foreground)
* Debug - for debugging purposes (purple foreground)
* Plus - when you discovered something new (green foreground)
* Minus - when you lose something important (red foreground)
* Success - for bragging about the success (green foreground)  
* Failure - to get upset about the failure  (red foreground)  
* Custom - Set it how you like (custom type and color, explained later)  

This is how it looks on my system:
![Examples](screenshots/logs_example.png)

## Advanced: Logger object
When creating logger object you can pass 3 different parameters to constructor:
```
log = coollogs.Logger(colorful=True, infolength=9, 
                      timecolor=coollogs.Colors.fg.CYAN)
```
| Parameter  |       Type      | Purpose                                                                                                                                             | Default value           |
|------------|:---------------:|-----------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------:|
|  colorful  |       bool      | Turns on/off color stylizing of the output                                                                                                          |           True          |
|  loglevel  |       int       | Sets log level for the logger                                                                                                                       |            31           |
|  labelsize |       int       | Determines amount of space for label block.  If information is longer than *labelsize*, it'll be cut; otherwise it'll be padded with spaces.        |            9            |
|  timecolor | coollogs.Colors | Sets color for time                                                                                                                                 | coollogs.Colors.fg.CYAN |

## Advanced: Custom logs
If provided log modes don't satisfy you, you can create your own, using .custom():
```
log.custom('Hello, custom!', infoname='', infocolor=Colors.fg.CYAN)
```
| Parameter |       Type      | Purpose                                                                                                         | Default value           |
|-----------|:---------------:|-----------------------------------------------------------------------------------------------------------------|:-----------------------:|
|  infoname |       str       | Sets text in custom information block                                                                           |            ""           |
| labelcolor| coollogs.Colors | Sets color of custom information block. Can be a sum of different coollogs.Colors values to create mixed styles | coollogs.Colors.fg.CYAN |

## Advanced: Logging level
Even though there are 10 built-in logging modes, only 5 of them are "basic": debug, info, warning, error and critical. You can set logging level by using .set_level(int) on your logger object, for example:
```
log.set_level(7)
```
This will set logging level to a 7, which means that only critical messages, errors and warnings will be displayed. THe value passed into set_level() function is calulated by summing up every log level, which you want to be showed.
Values for each level are as follows:
| Level    | Value |
|----------|:-----:|
| CRITICAL |   1   |
|   ERROR  |   2   |
|  WARNING |   4   |
|   INFO   |   8   |
|   DEBUG  |   16  |

So, for example, to show everything except debug messages, you have to set logging level to 1 + 2 + 4 + 8 = 15.  
You don't have to memorize all the values, there are constants in log_level class to help you with it:
```
coollogs.log_level.CRITICAL = 1
coollogs.log_level.ERROR    = 2
coollogs.log_level.WARNING  = 4
coollogs.log_level.INFO     = 8
coollogs.log_level.DEBUG    = 16
coollogs.log_level.ALL      = 31 ```