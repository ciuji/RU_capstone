import re
import os

class Interval():

	def __init__(self, index, xmin, xmax):
		self.index = index
		self.xmin = xmin
		self.xmax = xmax
		self.time = self.xmax - self.xmin


def get_total_time(t):
	xmin = float(t[0].split()[-1])
	xmax = float(t[1].split()[-1])
	return xmax-xmin


def get_interval_size(w):
	return int(w.split()[-1])


def find_all_intervals(s):
	p = re.compile(r'\s*name\s=\s"words"')
	lines = s.split('\n')
	# find the information of the TextGrid file
	while not p.fullmatch(lines.pop(0)):
		pass
	# get the total time length
	t = (lines.pop(0), lines.pop(0))
	total_time = get_total_time(t)
	# get the number of words
	w = lines.pop(0)
	interval_size = get_interval_size(w)
	# find all words
	p = re.compile(r'\s*intervals\s\[\d+\]:')
	words = []
	for i in range(interval_size):
		while not p.fullmatch(lines.pop(0)):
			pass
		xmin = float(lines.pop(0).split()[-1])
		xmax = float(lines.pop(0).split()[-1])
		text = lines.pop(0).split()[-1]
		if text != "\"\"":
			words.append(Interval(i, xmin, xmax))	
	return total_time, words


if __name__ == '__main__':
	path = os.path.split(os.path.realpath(__file__))[0]
	total_time = 0
	aligned_time = 0
	index = 0
	while True:
		index += 1
		file_name = f'{index}.TextGrid'
		try:
			f = open(path + '\\' + file_name, 'r')
			s = f.read()
			f.close()
			t, words = find_all_intervals(s)
			# add the duration of the current resource to the total time
			total_time += t
			# add all aligned intervals duration to the total aligned time
			for i in words:
				aligned_time += i.time
		except FileNotFoundError:
			break
	print(f'The total time is: {total_time}')
	print(f'The aligned time is: {aligned_time}')
	print('The matching rate is: {:.2f}%'.format(aligned_time / total_time * 100))

	'''
	total_time, words = find_all_intervals(s)
	aligned_time = 0
	for i in words:
		aligned_time += i.time
	print(aligned_time)
	print(total_time)
	'''
	
