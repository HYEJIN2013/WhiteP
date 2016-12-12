import random

def make_tree_from_file(filename):	
	tree = {}
	with open(filename) as f:
		sheet = f.readlines()
	node_names = sheet[0].split()
	for row in sheet[1:]:
		vector = row.split()
		node = vector[0]
		if not (node in tree):
			tree[node] = '' 
		for name,value in zip(node_names,vector[1:]):
			value = int(value)
			if value:
				tree[node]+= name
	return(tree)
	
def random_points(tree):
	start = random.choice([x for x in tree])
	flag = 1
	while flag:
		 finish = random.choice([x for x in tree])
		 flag = (finish == start)
	return start,finish
	
def traverse(tree,start,finish):
	node = [start,tree[start]]
	out = [node]
	while out:
		node = out.pop(0)
		path = node[0]
		points = list(node[1])
		for point in points:
			if not (point in path):
				new_path = path+point
				new_points = tree[point]
				new_node = [new_path,new_points]
				if point == finish:
					print(new_path)
				else:
					out.append(new_node)

#Добавить:
	#Генерация рандомного графа
	
if __name__ == '__main__':
	#filename = input('Enter the filename: ')
	filename = '/home/vlad/test.txt'
	tree = make_tree_from_file(filename)
	print(tree)
	start,finish = random_points(tree)
	print(start,finish)
	traverse(tree,start,finish)
