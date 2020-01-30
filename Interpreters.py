Variables = {} 
def Assign(Lines):
	LeftExp,RightExp = Lines.split("=")
	LeftExp = LeftExp.rstrip()
	Variableslist =  sorted([key for key in Variables],key = lambda x:len(x),reverse = True)
	for key in Variableslist:
		if str(key) in RightExp:
			if type(Variables[key]) == str:
				RightExp =  RightExp.replace(str(key),'\''+str(Variables[key]+'\''))
			else:
				RightExp =  RightExp.replace(str(key),str(Variables[key]))
	LeftExp = LeftExp.split(",")
	LeftExp = [Var.strip() for Var in LeftExp]
	RightExp = eval(RightExp)
	#print(type(LeftExp),len(LeftExp))
	#print(RightExp)
	try:
		for i in range(len(LeftExp)):
			Variables[LeftExp[i]] = RightExp[i]
	except TypeError:
		#print("wdwd",LeftExp,RightExp)
		Variables[LeftExp[0]] = RightExp

while True:
	Lines = input(">>>")
	if Lines == "exit()":
		break
	if "=" in Lines and not "==" in Lines:
		Assign(Lines)
	elif Lines in Variables:
		print("A",Variables[Lines])
	else:
		print("B",eval(Lines))
	print(Variables)
