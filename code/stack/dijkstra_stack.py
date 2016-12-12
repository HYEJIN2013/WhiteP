from container import stack

opers = stack()
vals = stack()
fom = '(1+((2+3)*(4*5)))'

def compute(formula):
  for item in formula:
	if '(' == item:
		pass
	elif item in '+-*/':
		opers.push(item)
	elif ')' == item:
		c_val = int(vals.pop())
		n_val = int(vals.pop())
		oper = opers.pop()
		if '+' == oper:
			c_val += n_val
		elif '-' == oper:
			c_val -= n_val
		elif '*' == oper:
			c_val *= n_val
		elif '/' == oper:
			c_val /= n_val
		vals.push(c_val)
	else:
		vals.push(item)
	return vals.pop()

print('-'*3,fom,'-'*3)
print(compute(fom))
