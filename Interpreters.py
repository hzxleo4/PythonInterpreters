Variables = {} 
while True:
	Lines = input(">>>")
	if Lines == "exit()":
		break
	if "=" in Lines:
		LeftExp,RightExp = Lines.split("=")
		LeftExp = LeftExp.rstrip()
		Variableslist =  sorted([key for key in Variables],key = lambda x:len(x),reverse = True)
		for key in Variableslist:
			if str(key) in RightExp:
				if type(Variables[key]) == str:
					RightExp =  RightExp.replace(str(key),'\''+str(Variables[key]+'\''))
				else:
					RightExp =  RightExp.replace(str(key),str(Variables[key]))
		Variables[LeftExp] = eval(RightExp)
	elif Lines in Variables:
		print(Variables[Lines])
	else:
		print(eval(Lines))
	print(Variables)
