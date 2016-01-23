def read_matrix():
	#read matrix
	matrix = {}
	#reading
	f = open('input.txt', 'r')
	#set of chars
	matrix['chars'] = f.readline().replace(' ', '')
	#first state
	matrix['fstate'] = None
	#matrix
	for line in f:
		#matrix.append(line.split())
		a = line.split()
		matrix[a[0]] = a[1:]
		#remember first state
		if not matrix['fstate']:
			matrix['fstate'] = a[0]
	f.close()
	return matrix

#function to check string according to matrix
def check(string, matrix):
	state = matrix['fstate']
	chars = matrix['chars']
	for c in string:
		#if forbidden symbols, return false
		if c not in chars:
			return False
		state = matrix[state][chars.find(c)]
	#if it is final state - return true
	if matrix[state][-1] == '1':
		return True
	return False

def rightGramma(matrix):
	result = ''
	chars = matrix['chars']
	a = list(matrix.keys())
	a.remove('fstate')
	a.remove('chars')
	a.sort()
	for key in a:
		result += key + '::='
		for i in range(len(chars) - 1):
			result += chars[i] + matrix[key][i] + '|'
		if matrix[key][-1] == '1':
			result += 'eps'
		result += '\n'
	return result