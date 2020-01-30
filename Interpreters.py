Variables = {} 
def ChangeVariables(Expression):
	Variableslist =  sorted([key for key in Variables],key = lambda x:len(x),reverse = True)
	for key in Variableslist:
		if str(key) in Expression:
			if type(Variables[key]) == str:
				Expression =  Expression.replace(str(key),'\''+str(Variables[key]+'\''))
			else:
				Expression =  Expression.replace(str(key),str(Variables[key]))
	return Expression
def Assign(Lines):
	LeftExp,RightExp = Lines.split("=")
	LeftExp = LeftExp.strip()
	RightExp = ChangeVariables(RightExp)
	LeftExp = LeftExp.split(",")
	LeftExp = [Var.strip() for Var in LeftExp]
	RightExp = eval(RightExp)
	#print(type(LeftExp),len(LeftExp))
	#print(RightExp)
	#print(LeftExp)
	for i in range(len(LeftExp)):
		if '[' in LeftExp[i]:
			Name = LeftExp[i][:LeftExp[i].find("[")]
			Name = Variables[Name]
			Key = LeftExp[i][LeftExp[i].find('[')+1:LeftExp[i].find(']')]
			Key = int(Key) if Key.isdigit() else Key 
			LeftExp[i] = LeftExp[i][LeftExp[i].find("]")+1:]
			while LeftExp[i].count("[") != 0:
				Name = Name[Key]
				Key = LeftExp[i][LeftExp[i].find('[')+1:LeftExp[i].find(']')]
				Key = int(Key) if Key.isdigit() else Key 
				LeftExp[i] = LeftExp[i][LeftExp[i].find("]")+1:]
			if len(LeftExp) == 1:
				Name[Key] = RightExp
			else:
				Name[Key] = RightExp
		else:
			if len(LeftExp) == 1:
				Variables[LeftExp[i]] = RightExp
			else:
				Variables[LeftExp[i]] = RightExp[i]

#Lines = "a = [1,2,[3,4]]"
#print(">>>",end='')
while True:
	Lines = input(">>>")
	if Lines == "exit()":
		break
	if "=" in Lines and not "==" in Lines:
		Assign(Lines)
	elif Lines in Variables:
		print("A",Variables[Lines])
	elif '[' in Lines:
		Lines = ChangeVariables(Lines)
		print(eval(Lines))
	else:
		print("B",eval(Lines))
	print(Variables)
	#Lines = input(">>>")