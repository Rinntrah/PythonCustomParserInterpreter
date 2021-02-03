# PythonCustomParserInterpreter
1.Run MAIN.py
2.Choose example program
3.Click run

Extensible code parser and interpreter.
Currently allows to do following operations:

-declare integer variables:
variable [variable_name] = [integer_value]
example: variable x = 150

-declare functions:
function [function_name] { [statement_1] [statement_2] [statement_3...] }
function HelloWorld { print HelloWorld }

-invoke functions:
invoke [function_name]
example: invoke HelloWorld

-print variables or text
example: print Hello print x

-add two integer variables and store result in first argument
variable x = 10
variable y = 5
add x y
print x
>(prints 15)

Syntax can be extended by declaring more statements like:
StatementDeclareFunction or StatementAdd, which are implementing "execute()" method
And then extending "interpret_token(self,token)" function of Interpreter class

To run custom program just call:
1.INTERPRET_PROGRAM(text) which returns interpreter
and then pass returned interpreter via
2.RUN_PROGRAM(interpreter)
Result log is stored in list and returned from RUN_PROGRAM and can be viewed by printing (eg. log = RUN_PROGRAM(interpreter) print(log))


![alt text](https://github.com/Rinntrah/PythonCustomParserInterpreter/blob/main/example_image.png?raw=true)
