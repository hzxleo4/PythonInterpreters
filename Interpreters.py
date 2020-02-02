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
	Operator = ['+', '-', '*', '/', '&', '|', '~', '>>', '<<', '//', '**']
	LeftExp,RightExp = Lines.split("=")
	for i in Operator:
		if i in LeftExp:
			LeftExp = LeftExp[:LeftExp.find(i)]
			RightExp =  LeftExp + i + RightExp
			break
	#print(RightExp)
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
def Branch(Lines):
	Stack = []
	while True:
		Stack.append(Lines)
		Lines = input('...')
		#print("-->",Lines)
		try:
			if Lines[:4] != "    " and Lines[:4] != 'elif' and Lines[:5] != 'else:' and Lines[0] !='\t':
				break
		except:
			break
	IsTrue = 0
	for Lines in Stack:
		if ('elif' in Lines or 'else' in Lines) and IsTrue == 1:
			break
		elif 'if' in Lines or 'elif' in Lines:
			Expression = Lines[2:Lines.find(":")] if 'if' in Lines else Lines[5:Lines.find(":")]
			Expression = eval(ChangeVariables(Expression))
			#print("exp =",Expression)
			if Expression == True:
				IsTrue = 1
		elif 'else' in Lines:
			IsTrue = 1
		elif IsTrue == 1:
			Run_Code(Lines)


def Run_Code(Lines):
	if Lines == "exit()":
		return 1
	if Lines[:2] == 'if':
		Branch(Lines)
	elif "=" in Lines and not "==" in Lines:
		Assign(Lines)
	elif Lines in Variables:
		print("A",Variables[Lines])
	elif '[' in Lines:
		Lines = ChangeVariables(Lines)
		print(eval(Lines))
	else:
		print("B",eval(Lines))
	return 0
#Lines = "a = [1,2,[3,4]]"
#print(">>>",end='')
IsEnd = 0
while not IsEnd:
	Lines = input(">>>")
	Lines = Lines.strip()
	IsEnd = Run_Code(Lines)
	print(Variables)
	#Lines = input(">>>")



