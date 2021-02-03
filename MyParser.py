INTEGER, PLUS, EOF, FUNC, CHAR, VAR, ASSIGN, WORD, ERROR = (
    "INTEGER",
    "PLUS",
    "EOF",
    "FUNC",
    "CHAR",
    "VAR",
    "=",
    "WORD",
    "ERROR",
)

decl_variable_statement = {}


CURRENT_SCOPE = {}
GLOBAL_SCOPE = {}

LOCAL_LOG = []


def switchScope(scope):
    global CURRENT_SCOPE
    CURRENT_SCOPE = scope


def my_print(*txt):
    for n in txt:
        LOCAL_LOG.append(n)


class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return "Token({type}, {value})".format(type=self.type, value=repr(self.value))

    def __repr__(self):
        return self.__str__()


class StatementDeclareVariable(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return "StatementDeclareVariable({name}, {value})".format(
            name=self.name, value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

    def execute(self):
        my_print("declaring variable:", self.name, "=", self.value)
        CURRENT_SCOPE[self.name] = self.value


class StatementDeclareFunction(object):
    def __init__(self, name, statements):
        self.name = name
        self.statements = statements

    def __str__(self):
        return "StatementDeclareFunction({name}, {statements})".format(
            name=self.name, statements=repr(self.statements)
        )

    def __repr__(self):
        return self.__str__()

    def execute(self):
        my_print("declaring function named:", self.name)
        GLOBAL_SCOPE[self.name] = self

    def INVOKE(self):
        LOCAL_SCOPE = {}
        switchScope(LOCAL_SCOPE)
        for statement in self.statements:
            statement.execute()
        switchScope(GLOBAL_SCOPE)


class StatementAdd(object):
    def __init__(self, var1, var2):
        self.var1 = var1
        self.var2 = var2

    def __str__(self):
        return "StatementAdd({var1}, {var2})".format(var1=self.var1, var2=self.var2)

    def __repr__(self):
        return self.__str__()

    def execute(self):
        var1 = CURRENT_SCOPE[self.var1]
        var2 = CURRENT_SCOPE[self.var2]

        var3 = var1 + var2
        CURRENT_SCOPE[self.var1] = var3
        my_print(
            "adding:", var1, "+", var2, "result =", var3, "saved under:" + self.var1
        )


class StatementPrint(object):
    def __init__(self, var1):
        self.var1 = var1

    def __str__(self):
        return "StatementPrint({var1})".format(var1=self.var1,)

    def __repr__(self):
        return self.__str__()

    def execute(self):

        if self.var1 in CURRENT_SCOPE:
            var1 = CURRENT_SCOPE[self.var1]
            my_print(var1)
        else:
            my_print(self.var1)


class StatementInvokeFunction(object):
    def __init__(self, var1):
        self.var1 = var1

    def __str__(self):
        return "StatementInvokeFunction({var1})".format(var1=self.var1,)

    def __repr__(self):
        return self.__str__()

    def execute(self):
        var1 = GLOBAL_SCOPE[self.var1]
        return var1.INVOKE()


class Interpreter(object):
    def __init__(self, split_words):
        self.current_word = 0
        self.split_words = split_words
        self.final_program = []

    def execute_program(self):
        for statement in self.final_program:
            statement.execute()

    def step(self):
        next_word = self.split_words[self.current_word]
        statement = self.interpret_token(next_word)
        self.final_program.append(statement)
        return self.current_word >= len(self.split_words)

    def add_statement(self):
        self.current_word = self.current_word + 1
        var1 = self.split_words[self.current_word]
        self.current_word = self.current_word + 1

        var2 = self.split_words[self.current_word]
        self.current_word = self.current_word + 1

        final_add_statement = StatementAdd(str(var1), str(var2))
        my_print(final_add_statement)
        return final_add_statement

    def function_statement(self):
        self.current_word = self.current_word + 1
        function_name = self.split_words[self.current_word]
        self.current_word = self.current_word + 1
        self.current_word = self.current_word + 1  # {

        statements = []
        while True:
            next_token = self.split_words[self.current_word]
            if next_token == "}":
                break

            statement = self.interpret_token(next_token)
            statements.append(statement)

        self.current_word = self.current_word + 1  # }

        final_function_statement = StatementDeclareFunction(function_name, statements)
        my_print(final_function_statement)
        return final_function_statement

    def variable_statement(self):
        ignore = self.split_words[self.current_word]
        self.current_word = self.current_word + 1

        variable_name = self.split_words[self.current_word]
        self.current_word = self.current_word + 1

        equation_sign = self.split_words[self.current_word]
        self.current_word = self.current_word + 1

        if equation_sign != "=":
            raise Exception("Expected =. Actual:" + equation_sign)

        variable_value = self.split_words[self.current_word]
        self.current_word = self.current_word + 1

        statement = StatementDeclareVariable(variable_name, int(variable_value))

        return statement

    def print_statement(self):
        ignore = self.split_words[self.current_word]
        self.current_word = self.current_word + 1

        variable_name = self.split_words[self.current_word]
        self.current_word = self.current_word + 1

        statement = StatementPrint(variable_name)
        return statement

    def invoke_statement(self):
        ignore = self.split_words[self.current_word]
        self.current_word = self.current_word + 1

        variable_name = self.split_words[self.current_word]
        self.current_word = self.current_word + 1

        statement = StatementInvokeFunction(variable_name)

        return statement

    def interpret_token(self, token):
        if token == "function":
            return self.function_statement()

        if token == "variable":
            return self.variable_statement()

        if token == "add":
            return self.add_statement()

        if token == "print":
            return self.print_statement()

        if token == "invoke":
            return self.invoke_statement()

        if True:
            raise Exception("Error invalid token:" + token)

    def error(self):
        raise Exception("Error parsing input")


def INTERPRET(text):

    splitted = text.split(" ")
    interpreter = Interpreter(splitted)

    while True:
        flag = interpreter.step()
        if flag == True:
            break
    return interpreter


def RUN_PROGRAM(interpreter):
    LOCAL_LOG.clear()
    interpreter.execute_program()
    return LOCAL_LOG


def main():

    text = "function hi { print hello } function something { variable z = 5 variable x = 150 add x z invoke hi } invoke something print x print x"
    interpreter = INTERPRET(text)
    ret = RUN_PROGRAM(interpreter)
    print(ret)
    return


if __name__ == "__main__":
    main()
