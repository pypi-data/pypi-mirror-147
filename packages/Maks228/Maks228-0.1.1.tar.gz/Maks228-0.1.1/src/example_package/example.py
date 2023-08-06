import datetime
version = 0.2
def start():	
	import time
	wh = 0
	print("starting os pyos version 0.2 beta")
	time.sleep(1)
	while wh <= 5:
			print("loading.")
			time.sleep(0.5)
			print("loading..")
			time.sleep(0.5)
			print("loading...")
			time.sleep(0.5)
			wh += 1
	print("pyos started version "+version+" beta")
	time.sleep(0.5)
	print("добро пожаловать в ос pyos")
	while True:
		comm = input("Enter command:")
		if comm == "data":
			print(datetime.datetime.now())
		if comm == "info":
			print("ос: pyos")
			print("версия: " + version + " beta")
			print("создана: 21.04.2022")
			print("создатель: Maks")
		if comm == "help":
			print("калькулятор: calculator,информация: info,редактор текста: text redactor,команды: help,связь с разработчиком: conntact")
		if comm == "calculator":
			print("пожалуйсто ведите + или - или / или *")
			math = input()
			if math == "+":
				num1 = int(input("первое число"))
				num2 = int(input("второе число"))
				num3 = num1 + num2
				print(num3)
			if math == "-":
				num1 = int(input("первое число"))
				num2 = int(input("второе число"))
				num3 = num1 - num2
				print(num3)
			if math == "*":
				num1 = int(input("первое число"))
				num2 = int(input("второе число"))
				num3 = num1 * num2
				print(num3)
			if math == "/":
				num1 = int(input("первое число"))
				num2 = int(input("второе число"))
				num3 = num1 / num2
				print(num3)
		if comm == "text redactor":
			name = input("имя файла txt или py ")
			file = input("он создан? ответы да или нет")
			if file == "нет":
				redfile = open(name,"w")
				deistv = input("очистить clear, добавить add")
				if deistv == "clear":
					redfile = open(name,"w")
					redfile.close()
				if deistv == "add":
					text = input("текст для добавления")
					ent = input("сделать enter?")
					if ent == "да":
						redfile.write(text + " \n")
						redfile.close()
					if ent == "нет":
						redfile.write(text)
						redfile.close()
			if file == "да":
				redfile = open(name,"a")
				print(redfile.read())
				deistv = input("очистить clear, добавить add")
				if deistv == "clear":
					redfile = open(name,"w")
					redfile.close()
				if deistv == "add":
					text = input("текст для добавления")
					ent = input("сделать enter?")
					if ent == "да":
						redfile.write(text + " \n")
						redfile.close()
					if ent == "нет":
						redfile.write(text)
						redfile.close()
		if comm == "conntact":
			print("email: nmaks6381@gmail.com")
			