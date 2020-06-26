import tkinter as tk
from tkinter import PhotoImage
import time
from threading import Timer
from tkinter import *
from operator import pow, truediv, mul, add, sub  
from math import sqrt
import re

win = tk.Tk()

#Set Title and Icon of the window
win.title("Calculator")
calculatoricon = PhotoImage(file = "calculatoricon.png")
win.iconphoto(False, calculatoricon)
#Set size of the window
win.geometry("500x375")
#Set the window as unresizeable
win.resizable(False, False)

mainTextDisplay = tk.Text(win, height=1, width=28, bg="white", bd=3, font=("Helvetica", 23))
mainTextDisplay.grid(row=0, column=0, columnspan=4, padx=10, pady=10)


once = True
exponentSCs = "⁰¹²³⁴⁵⁶⁷⁸⁹"
exponentChars = False
def button_click(s):
	global exponentChars
	global firstExponent
	global once
	print(s)
	if s == "ˣ":
		if exponentChars == True:
			exponentChars = False
			print("TURNED OFF")
			return 0
		if mainTextDisplay.get("end-2c").isdigit() == True:
			print(mainTextDisplay.get("end-2c"))
			exponentChars = True
			mainTextDisplay.insert("end-1c", "​")
			print("TURNED ON")
		return 0


	#If s is an int:
	if isinstance(s, int) == True:
		if exponentChars == False and mainTextDisplay.get("end-2c") in exponentSCs:
			return 0
		if exponentChars == True:
			mainTextDisplay.insert("end-1c", exponentSCs[s])
			return 0
		#Add s to the end of main text display
		mainTextDisplay.insert("end-1c", s)
		return 0


	#If its the square root symbol
	if s == '√':
		#Cancel event if last character is the square root symbol (To prevent 2 square root symbols being wrote one after the other)
		if mainTextDisplay.get("end-2c") == '√':
			return 0
		else:
			#If there is no square root symbol at the end, then put one at the end
			mainTextDisplay.insert(END, s)


	#If s is an operator symbol:
	if s in ops.keys():
		#Prevents any operator symbols from being typed if exponent characters is on
		if exponentChars == True:
			return 0
		#Prevents any operator symbols from being typed if the display is empty
		if len(mainTextDisplay.get("1.0")) == 1:
			if mainTextDisplay.get("end-2c").isdigit():
				mainTextDisplay.insert(END, s)
				return 0
			return 0
		#If the display is not empty add it to main display
		elif mainTextDisplay.get("end-2c") not in ops.keys():
			mainTextDisplay.insert(END, s)

	#Self explanatory
	if s == "!backspace":
		mainTextDisplay.delete("end-2c")
	elif s == "!clear":
		mainTextDisplay.delete("1.0", END)
		once = False



#DONT FORGET TO ADD EXPONENT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
ops = {
	'+': add,
	'-': sub,
	'x': mul,
	'÷': truediv
}


def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub)

calculationHistory = {}
def handle():
	text = mainTextDisplay.get("1.0", "end-1c")

	#Exponent handling
	for i in list(find_all(text, '​')):
		text = text[:i] + "**" + text[i:]

	
	text = text.replace('​', "")
	text = text.replace("⁰", "0")
	text = text.replace("¹", "1")
	text = text.replace("²", "2")
	text = text.replace("³", "3")
	text = text.replace("⁴", "4")
	text = text.replace("⁵", "5")
	text = text.replace("⁶", "6")
	text = text.replace("⁷", "7")
	text = text.replace("⁸", "8")
	text = text.replace("⁹", "9")

	for i in range(text.count("**")):
		print(text)
		aa = re.search(r"\d*(\*\*)\d*", text)
		aaspan = aa.span()
		aa = aa.group().split("**")
		aare = pow(float(aa[0]), float(aa[1]))
		print("aare         " + str(aare))

		text = text[:aaspan[0]] + str(aare) + text[aaspan[1]:]
		if len(aa) == 2:
			result = "{:.3f}".format(aare)
			button_click("!clear")
			mainTextDisplay.insert("end-1c", result)
			calculationHistory[f'{mainTextDisplay.get("1.0", "end-1c")}'] = result
			return 0


	#Square root handling
	count = 0
	for i in list(find_all(text, "√")):
		try:
			a = text[text.index("√") + 1:text.index("+", i+count)]
		except ValueError:
			try:
				a = text[text.index("√") + 1:text.index("-", i+count)]
			except ValueError:
				try:
					a = text[text.index("√") + 1:text.index("x", i+count)]
				except ValueError:
					try:
						a = text[text.index("√") + 1:text.index("÷", i+count)]
					except ValueError:
						a = text[text.index("√") + 1:]

		na = sqrt(float(a))
		text = text.replace(f"√{a}", str(na), 1)
		count = count + len(str(na))

	calculate(text)


def calculate(s):
	if s == None:
		return 0
	try:
		if s.isdigit():
			return float(s)
	except:
		pass

	print("a")
	for c in ops.keys():
		left, operator, right = s.partition(c)
		if operator in ops:

			result = ops[operator](calculate(left), calculate(right))
			result = "{:.2f}".format(float(result))
			button_click("!clear")
			mainTextDisplay.insert("end-1c", result)
			calculationHistory[f'{mainTextDisplay.get("1.0", "end-1c")}'] = result






buttonOne = Button(win, text="1", padx=35, pady=4, bg="black", fg="white", font=("Helvetica", 20), command=lambda: button_click(1))
buttonTwo = Button(win, text="2", padx=35, pady=4, bg="black", fg="white", font=("Helvetica", 20), command=lambda: button_click(2))
buttonThree = Button(win, text="3", padx=35, pady=4, bg="black", fg="white", font=("Helvetica", 20), command=lambda: button_click(3))
buttonFour = Button(win, text="4", padx=35, pady=4, bg="black", fg="white", font=("Helvetica", 20), command=lambda: button_click(4))
buttonFive = Button(win, text="5", padx=35, pady=4, bg="black", fg="white", font=("Helvetica", 20), command=lambda: button_click(5))
buttonSix = Button(win, text="6", padx=35, pady=4, bg="black", fg="white", font=("Helvetica", 20), command=lambda: button_click(6))
buttonSeven = Button(win, text="7", padx=35, pady=4, bg="black", fg="white", font=("Helvetica", 20), command=lambda: button_click(7))
buttonEight = Button(win, text="8", padx=35, pady=4, bg="black", fg="white", font=("Helvetica", 20), command=lambda: button_click(8))
buttonNine = Button(win, text="9", padx=35, pady=4, bg="black", fg="white", font=("Helvetica", 20), command=lambda: button_click(9))
buttonZero = Button(win, text="0", padx=35, pady=3, bg="black", fg="white", font=("Helvetica", 20), command=lambda: button_click(0))

buttonPlus = Button(win, text="+", padx=24, pady=2.8, bg="grey", fg="white", font=("Helvetica", 19), command=lambda: button_click("+"))
buttonSub = Button(win, text="-", padx=26.24, pady=0.2, bg="grey", fg="white", font=("Helvetica", 21), command=lambda: button_click("-"))
buttonMultiply = Button(win, text="x", padx=26.5, pady=5, bg="grey", fg="white", font=("Helvetica", 18), command=lambda: button_click("x"))
buttonDivide = Button(win, text="÷", padx=24, pady=1, bg="grey", fg="white", font=("Helvetica", 20), command=lambda: button_click("÷"))
buttonExponent = Button(win, text="xˣ", padx=24, pady=1, bg="grey", fg="white", font=("Helvetica", 20), command=lambda: button_click("ˣ"))
buttonRoot = Button(win, text="√", padx=30, pady=4.1, bg="grey", fg="white", font=("Helvetica", 19), command=lambda: button_click("√"))
buttonEqual = Button(win, text="=", padx=101, pady=3, bg="#42b6f5", fg="white", font=("Helvetica", 19), command=lambda: handle())

buttonBackspace = Button(win, text="⌫", padx=30, pady=5, bg="grey", fg="white", font=("Helvetica", 17), command=lambda: button_click("!backspace"))
buttonClear = Button(win, text="C", padx=36, pady=5, bg="grey", fg="white", font=("Helvetica", 17), command=lambda: button_click("!clear"))

# Put the buttons on the screen
buttonBackspace.grid(row=1, column=1)
buttonClear.grid(row=1,column=0)
buttonSeven.grid(row=2, column=0)
buttonEight.grid(row=2, column=1)
buttonNine.grid(row=2, column=2)
buttonFour.grid(row=3, column=0)
buttonFive.grid(row=3, column=1)
buttonSix.grid(row=3, column=2)
buttonOne.grid(row=4, column=0)
buttonTwo.grid(row=4, column=1)
buttonThree.grid(row=4, column=2)
buttonZero.grid(row=5, column=0)
buttonPlus.grid(row=5, column=3)
buttonSub.grid(row=4, column=3)
buttonMultiply.grid(row=3, column=3)
buttonDivide.grid(row=2, column=3)
buttonEqual.grid(row=5, column=1, columnspan=2)
buttonRoot.grid(row=1, column=2)
buttonExponent.grid(row=1, column=3)





win.mainloop()

historywin = tk.Tk()

historywin.title("History")
calculatoricon = PhotoImage(file = "calculatoricon.png")
historywin.iconphoto(False, calculatoricon)
historywin.geometry(f"250x{str(len(calculationHistory) * 15)}")
historywin.resizable(False, False)

for i in calculationHistory.keys():
	txt = f"{i}  =  {calculationHistory[i]}"
	Label(text=i).pack()

historywin.mainloop()