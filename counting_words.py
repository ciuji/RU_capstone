import os

def count(s):
	return len(s.split())

if __name__ == '__main__':
	index = 0
	path = os.path.split(os.path.realpath(__file__))[0]
	words = 0
	while True:
		index += 1
		try:
			f = open(path + '\\' + f'{index}.lab', 'r')
			s = f.read()
			f.close()
			words += count(s)
		except FileNotFoundError:
			if index > 1189:
				break
			continue
	print(f'The number of words in total is: {words}')