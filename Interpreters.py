Variables = {'a' : [1,2,3,4,5],'b':7} 

def ChangeVariables(Expression):
	#print(Expression)
	Variableslist =  sorted([key for key in Variables],key = lambda x:len(x),reverse = True)
	for key in Variableslist:
		if str(key) in Expression:
			if not '\'' in Expression and not "\"" in Expression:
				#print("jekfefhe\n")
				if type(Variables[key]) == str:
					Expression =  Expression.replace(str(key),'\''+str(Variables[key]+'\''))
				else:
					Expression =  Expression.replace(str(key),str(Variables[key]))
			else:
				NewExp = ''
				while Expression:
					Double = Expression.find('\"') if Expression.find('\"') != -1 else 10000
					Single = Expression.find('\'') if Expression.find('\'') != -1 else 10000
					#print(Double,Single)
					Varposition = Expression.find((str(key))) if Expression.find(str(key)) != -1 else 10000
					while Varposition < Double and Varposition < Single:
						NewExp += Expression[:Expression.find(str(key))] + '\'' + str(Variables[key]) +'\''
						Expression = Expression[Expression.find(str(key))+len(str(key)):]
						Varposition = Expression.find((str(key))) if Expression.find(str(key)) != -1 else 10000
					if Double < Single:
						NewExp += Expression[:Double+1]
						Expression = Expression[Double+1:]
						NewExp += Expression[:Expression.find("\"")+1]
						Expression = Expression[Expression.find("\"")+1:]
					else:
						NewExp += Expression[:Single+1]
						Expression = Expression[Single+1:]
						NewExp += Expression[:Expression.find('\'')+1]
						Expression = Expression[Expression.find('\'')+1:]

				Expression = NewExp
		#print(Expression)
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

def Branch(Stack):
	#print("fueohif")
	IsTrue = {}
	#IsTrue[0] = IsTrue[1] = IsTrue[2] = -1
	#Stack = ['if a == 6:','\tif b == 7:','\t\tc = 10','else:','\tif b == 8:','\t\tc = 10','\telse:','\t\tc = 12']
	for Lines in Stack:
		flag = 0
		nest = Lines.count("\t")
		for i in range(nest+1):
			if IsTrue[i] == 0:
				flag = 1
				break
		if flag == 1:
			continue
		if ('else' in Lines or 'elif' in Lines) and IsTrue[nest+1] == 1:
			IsTrue[nest+1] = 0
			continue
		else:
			if 'if' in Lines or 'elif' in Lines:
				Expression = Lines[Lines.find('if')+2:Lines.find(":")] if 'if' in Lines else Lines[Lines.find('elif')+4:Lines.find(":")]
				Expression = eval(ChangeVariables(Expression))
				print(Expression)
				if Expression == True:
					nest = Lines.count('\t')
					IsTrue[nest+1] = 1
				else:
					IsTrue[nest+1] = 0
			elif 'else' in Lines:
				nest = Lines.count('\t')
				IsTrue[nest+1] = 1
			else:
				print(Lines)
				Run_Code(Lines)

def Loop(case,Stack):
	if case == 0:
		Test = Stack[0][Stack[0].find('while')+5:Stack[0].find(':')]
		test = ChangeVariables(Test)
		Stack.pop(0)
		#print(Stack)
		while eval(test) == True:
			for i in range(len(Stack)):
				if 'if' in Stack[i]:
					stack = []
					stack.append(Stack[i])
					i += 1
					while Stack[i].count('\t') > 1:
						stack.append(Stack[i])
						i += 1
					Branch(stack)
				else:
					Run_Code(Stack[i])
			test = ChangeVariables(Test)
	else:
		LeftExp = Stack[0][Stack[0].find('for')+3:Stack[0].find('in')]
		RightExp = Stack[0][Stack[0].find('in')+2:Stack[0].find(':')]
		Stack.pop(0)
		#print(len(ChangeVariables(RightExp)))
		for j in range(len(eval(ChangeVariables(RightExp)))):
			Lines = LeftExp + '=' + RightExp + '[' + str(j) + ']'
			#print(Lines)
			Assign(Lines)
			for i in range(len(Stack)):	
				if 'if' in Stack[i]:
						stack = []
						stack.append(Stack[i])
						i += 1
						while Stack[i].count('\t') > 1:
							stack.append(Stack[i])
							i += 1
						Branch(stack)
				else:	
					Run_Code(Stack[i])
			#print(Variables['b'])



def Built_in_Function(Lines):
	Object,Attribute = Lines.split(".")
	if Attribute.find(')') - Attribute.find('(') != 1:
		Key = Attribute[Attribute.find('(')+1:Attribute.find(')')]
		Key = int(Key) if Key.isdigit() else Key
		getattr(Variables[Object],str(Attribute[:Attribute.find('(')]))(Key)
		return 0
	else:
		return getattr(Variables[Object],str(Attribute[:Attribute.find('(')]))()

def Run_Code(Lines):
	if Lines == "exit()":
		return 1
	if Lines[:2] == 'if':
		Stack = []
		while True:
			try:
				if Lines[:4] != 'elif' and Lines[:5] != 'else:' and Lines[0] !='\t' and not 'if' in Lines:
					break
			except:
				break
			IsTrue[Lines.count('\t')+1] = -1
			Stack.append(Lines)
			Lines = input('...')
		Branch(Stack)
	elif "=" in Lines and not "==" in Lines:
		Assign(Lines)
	elif Lines in Variables:
		print("A",Variables[Lines])
	elif '[' in Lines:
		Lines = ChangeVariables(Lines)
		print(eval(Lines))
	elif '.' in Lines:
		Lines = Built_in_Function(Lines)
		if str(Lines):
			print(Lines)
	elif 'while' in Lines or 'for' in Lines:
		Stack = []
		while True:
			try:
				if Lines[:4] != 'while' and Lines[0] !='\t' in Lines and not 'for' in Lines:
					break
			except:
				break
			Stack.append(Lines)
			Lines = input('...')
		if 'while' in Lines:
			Loop(0,Stack)
		else:
			Loop(1,Stack)
	else:
		Lines = ChangeVariables(Lines)
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

#Branch(None)


