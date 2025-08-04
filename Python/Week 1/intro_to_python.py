"""A Basic Calculator Program
- Reads two(2) numbers and and operator
- performs arithematic operation on the numbers using the operator
- Output the result to the console.
"""

def calc(fNum, sNum, opertr):
    
    if opertr == '+':
        return fNum + sNum
    elif opertr == '-':
        return fNum - sNum
    elif opertr == '*':
        return fNum * sNum
    elif opertr == '/':
        if sNum != 0:
            return fNum / sNum
        else:
            return "Division by Zero not allowed"
    else:
        return "No Basic Valid operator given"


fNum = int(input("Enter the first number: "))
sNum = int(input("Enter the second number: "))
opertr = str(input("Enter the operator: "))

res = calc(fNum, sNum, opertr)

print("Result:", res)
