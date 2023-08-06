import random

#class Integers:
#    def __init__(self, lowerBound, upperBound):
#        self.lowerBound = lowerBound
#        self.upperBound = upperBound

def exprIsSafe(expr):
    whitelist = "0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM()*/+-=<>!%.\\\"\', "
    if all(c in whitelist for c in expr):
        return True
    else:
        return False

dic = {"__builtins__":None}

specialValues = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, -10, 10, 100, -100, 210, -210]

def forAll(variable, vtype, logicExpr, lowerBound = -1000000000, upperBound = 1000000000):
    """
    This function takes in the name of a new variable, its domain and a logical expresion that is checked againt many values of the variable. Also a lower bound and upper bound can be specified, but are not necesary.
    """
    #only integers for now

    if vtype == 'integer':
        for i in range(200):
            dic[variable] = random.randrange(lowerBound, upperBound)

            if boolEval(logicExpr) == False:
                return False

        for i in specialValues:
            dic[variable] = i

            if lowerBound <= i and i <= upperBound and boolEval(logicExpr) == False:
                return False
        
        return True

def boolEval(expr):
    """
    This function takes in a mathematical expresion as a string, checks it against many random and some special values and returns true if and only if none of the tests proved the expresion wrong. The mathimatical expresion can have several sybols:
    - aritmetic operators such as +, -, *, /, %, and **,
    - logical operators sush as not, and and or,
    - parentheses ( and ),
    - some functions such as sin() and sqrt() may be added later on,
    - equals and greater signs: ==, >, <, !=,
    - quotes and backslashes for escaping
    - the logical quantifier "for all".
    The quantifier "for all" is to be written in the form forAll('variable', 'type', "logical expresion", lowerBound, upperBound). This is a function that has to be executed after the pieces of the mathematical expresion that it is inside of, so code of the form boolEval(forAll(a, 'integer', forAll('b', 'integer', a*b > 0))) wouldn't work. This is why the logical expresion has to be a string. 
    All operators should be written in python syntax, e.g. * for multiplication, not x. 
    Example: boolEval("forAll('a', 'integer', \"(a < 0) or (forAll('b', 'integer', \\\"a*b*b >= 0\\\")))\") should return true.
    The type argument can be equal to 'integer', 'real', 'prime', and 'natural'.
    """ 
    if exprIsSafe(expr):
        return eval(expr, dic, {"forAll":forAll})

#print(exprIsSafe("abc"))
#print(exprIsSafe("forAll('a', 'integer', \"forAll('b', 'integer', \\\"a*b > 0\\\")\")"))
#print(boolEval("forAll('a', 'integer', \"forAll('b', 'integer', \\\"a*a > 0\\\")\")"))
