#Please help me to return the right list.
x = [['magic','fireball','Powerful firemagic that hits all enemys one time','fire.png'],[], [[[[['phy'],'hp', '!!!!']]]]]

def parseop(tmpsp):
	for num, nam in enumerate (tmpsp):
		if type(nam) == list: 
			parseop(tmpsp[num])
		if nam=='!!!!': # do something
			print 'parseop2', nam
			nam = 'success'
print parseop(x)
input()
