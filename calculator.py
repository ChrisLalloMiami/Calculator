import tkinter as tk
from tkinter import *
import math
from pynput.keyboard import Listener
import threading
from decimal import Decimal

operators = ["+", "-", "x", "/"]

def simplifyBySymbol(symbol, expression):
    #look for operator
    operatorIdx = 0
    while operatorIdx != -1:
        operatorIdx = expression.find(symbol)
        if operatorIdx == -1 or operatorIdx == 0:
            break
        else:
            # scan left
            leftIdx = operatorIdx - 1
            while leftIdx >= 0:
                if expression[leftIdx] in operators:
                    break
                else:
                    leftIdx -= 1
            leftOperand = Decimal(expression[leftIdx + 1:operatorIdx])
            
            # scan right
            rightIdx = operatorIdx + 1
            while rightIdx < len(expression):
                if expression[rightIdx] in operators:
                    break
                else:
                    rightIdx += 1
            rightOperand = Decimal(expression[operatorIdx + 1:rightIdx])

            # combine expressions
            multRes = 0
            match symbol:
                case "+":
                    multRes = (leftOperand + rightOperand).normalize()
                case "-":
                    multRes = (leftOperand - rightOperand).normalize()
                case "x":
                    multRes = (leftOperand * rightOperand).normalize()
                case "/":
                    multRes = (leftOperand / rightOperand).normalize()
            
            leftHalf = expression[0:leftIdx+1]
            rightHalf = expression[rightIdx:len(expression)]
            expression = leftHalf + str(multRes) + rightHalf
    return expression

def parseExpression(expression):
    expression = simplifyBySymbol("x", expression)
    expression = simplifyBySymbol("/", expression)
    expression = simplifyBySymbol("+", expression)
    expression = simplifyBySymbol("-", expression)
    return expression

def isOperatorValid():
    expression = resultVar.get()
    if len(expression) == 1 and expression[0] == ".":
        return False
    if len(expression) > 0:
        lastChar = expression[len(expression)-1:len(expression)]
        if lastChar != "+" and lastChar != "-" and lastChar != "x" and lastChar != "/" and lastChar != ".":
            return True
    return False

def isDecimalValid():
    expression = resultVar.get()
    if len(expression) > 0:
        lastChar = expression[len(expression)-1:]
        if lastChar == ".":
            return False
        else:
            currentIdx = len(expression) - 1
            while currentIdx >= 0:
                if expression[currentIdx] in operators:
                    break
                else:
                    currentIdx -= 1

            lastWord = expression[currentIdx+1:]
            if lastWord.find(".") == -1:
                return True
            else:
                return False
    else:
        return True
    
def isExpressionValid():
    expression = resultVar.get()
    if len(expression) == 0:
        return False
    elif len(expression) == 1 and expression[0] == ".":
        return False
    elif len(expression) > 0:
        lastChar = expression[len(expression) - 1]
        if lastChar in operators or lastChar == ".":
            return False
        else:
            return True
    
def isSingleNumOpValid():
    expression = resultVar.get()
    if len(expression) == 0:
        return False
    elif expression[0] == "+" or expression[0] == "x" or expression[0] == "/":
        return False
    elif expression[0] == "-":
        word = expression[1:]
        if word.find("+") == -1 and word.find("-") == -1 and word.find("x") == -1 and word.find("/") == -1:
            return True
        else:
            return False
    else:
        if expression.find("+") == -1 and expression.find("-") == -1 and expression.find("x") == -1 and expression.find("/") == -1:
            return True
        else:
            return False

def funcKey(key):
    match key:
        case "0":
            resultVar.set(resultVar.get() + "0")
        case "1":
            resultVar.set(resultVar.get() + "1")
        case "2":
            resultVar.set(resultVar.get() + "2")
        case "3":
            resultVar.set(resultVar.get() + "3")
        case "4":
            resultVar.set(resultVar.get() + "4")
        case "5":
            resultVar.set(resultVar.get() + "5")
        case "6":
            resultVar.set(resultVar.get() + "6")
        case "7":
            resultVar.set(resultVar.get() + "7")
        case "8":
            resultVar.set(resultVar.get() + "8")
        case "9":
            resultVar.set(resultVar.get() + "9")
        case ".":
            if isDecimalValid():
                resultVar.set(resultVar.get() + ".")
        case "+":
            if isOperatorValid():
                resultVar.set(resultVar.get() + "+")
        case "-":
            if isOperatorValid():
                resultVar.set(resultVar.get() + "-")
        case "x":
            if isOperatorValid():
                resultVar.set(resultVar.get() + "x")
        case "/":
            if isOperatorValid():
                resultVar.set(resultVar.get() + "/")
        case "=":
            if isExpressionValid():
                resultVar.set(parseExpression(resultVar.get()))
        case "C":
            resultVar.set("")
        case "+/-":
            if isSingleNumOpValid():
                resultVar.set(str(-1 * Decimal(resultVar.get())))
        case "^2":
            if isSingleNumOpValid():
                resultVar.set(str(Decimal(Decimal(resultVar.get()) * Decimal(resultVar.get())).normalize()))
        case "sqrt":
            if isSingleNumOpValid() and resultVar.get()[0] != "-":
                resultVar.set(str(Decimal(math.sqrt(Decimal(resultVar.get()))).normalize()))
        case "1/x":
            if isSingleNumOpValid():
                resultVar.set(str(Decimal(1 / Decimal(resultVar.get())).normalize()))
        case "del":
            resultVar.set(resultVar.get()[0:len(resultVar.get())-1])
        case _:
            resultVar.set("ERROR")


root = tk.Tk()
root.geometry("250x425")
root.title("Calculator")

resultVar = tk.StringVar()

frm = tk.Frame(root, padx=10, pady=10)
frm.grid()

result = tk.Label(frm, textvariable=resultVar, bg="lightgrey", width=30, height=2, wraplength=200)
result.grid(column=0, row=0, columnspan=5)

reciprocal = tk.Button(frm, text="1/x", height=4, width=5, command=lambda: funcKey("1/x"))
reciprocal.grid(column=0, row=1)

square = tk.Button(frm, text="x^2", height=4, width=5, command=lambda: funcKey("^2"))
square.grid(column=1, row=1)

squareRoot = tk.Button(frm, text = "sqrt(x)", height=4, width=5, command=lambda: funcKey("sqrt"))
squareRoot.grid(column=2, row=1)

divide = tk.Button(frm, text = "/", height=4, width=5, command=lambda: funcKey("/"))
divide.grid(column=3, row=1)

seven = tk.Button(frm, text="7", height=4, width=5, command=lambda: funcKey("7"))
seven.grid(column=0, row=2)

eight = tk.Button(frm, text="8", height=4, width=5, command=lambda: funcKey("8"))
eight.grid(column=1, row=2)

nine = tk.Button(frm, text="9", height=4, width=5, command=lambda: funcKey("9"))
nine.grid(column=2, row=2)

multiply = tk.Button(frm, text="x", height=4, width=5, command=lambda: funcKey("x"))
multiply.grid(column=3, row=2)

four = tk.Button(frm, text="4", height=4, width=5, command=lambda: funcKey("4"))
four.grid(column=0, row=3)

five = tk.Button(frm, text="5", height=4, width=5, command=lambda: funcKey("5"))
five.grid(column=1, row=3)

six = tk.Button(frm, text="6", height=4, width=5, command=lambda: funcKey("6"))
six.grid(column=2, row=3)

subtract = tk.Button(frm, text="-", height=4, width=5, command=lambda: funcKey("-"))
subtract.grid(column=3, row=3)

one = tk.Button(frm, text="1", height=4, width=5, command=lambda: funcKey("1"))
one.grid(column=0, row=4)

two = tk.Button(frm, text="2", height=4, width=5, command=lambda: funcKey("2"))
two.grid(column=1, row=4)

three = tk.Button(frm, text="3", height=4, width=5, command=lambda: funcKey("3"))
three.grid(column=2, row=4)

add = tk.Button(frm, text="+", height=4, width=5, command=lambda: funcKey("+"))
add.grid(column=3, row=4)

plusMinus = tk.Button(frm, text="+/-", height=4, width=5, command=lambda: funcKey("+/-"))
plusMinus.grid(column=0, row=5)

zero = tk.Button(frm, text="0", height=4, width=5, command=lambda: funcKey("0"))
zero.grid(column=1, row=5)

decimal = tk.Button(frm, text=".", height=4, width=5, command=lambda: funcKey("."))
decimal.grid(column=2, row=5)

equals = tk.Button(frm, text="=", height=4, width=5, command=lambda: funcKey("="))
equals.grid(column=3, row=5)

clear = tk.Button(frm, text="C", height=4, width=5, command=lambda: funcKey("C"))
clear.grid(column=4, row=1)

delete = tk.Button(frm, text="del", height=4, width=5, command=lambda: funcKey("del"))
delete.grid(column=4, row=2)

def getInput():
    def on_release(key):
        match str(key).strip():
            case "<96>":
                funcKey("0")
            case "'0'":
                funcKey("0")
            case "<97>":
                funcKey("1")
            case "'1'":
                funcKey("1")
            case "<98>":
                funcKey("2")
            case "'2'":
                funcKey("2")
            case "<99>":
                funcKey("3")
            case "'3'":
                funcKey("3")
            case "<100>":
                funcKey("4")
            case "'4'":
                funcKey("4")
            case "<101>":
                funcKey("5")
            case "'5'":
                funcKey("5")
            case "<102>":
                funcKey("6")
            case "'6'":
                funcKey("6")
            case "<103>":
                funcKey("7")
            case "'7'":
                funcKey("7")
            case "<104>":
                funcKey("8")
            case "'8'":
                funcKey("8")
            case "<105>":
                funcKey("9")
            case "'9'":
                funcKey("9")
            case "'/'":
                funcKey("/")
            case "'*'":
                funcKey("x")
            case "'+'":
                funcKey("+")
            case "'-'":
                funcKey("-")
            case "<110>":
                funcKey(".")
            case "'.'":
                funcKey(".")
            case "Key.enter":
                funcKey("=")
            case "Key.backspace":
                funcKey("del")
            case "Key.delete":
                funcKey("del")
            case "Key.esc":
                root.destroy()
                return

    with Listener(on_press=on_release) as listener:
        listener.join()

t = threading.Thread(target=getInput)
t.daemon = True
t.start()

root.mainloop()
