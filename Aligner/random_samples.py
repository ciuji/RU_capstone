import shutil
import os
import random


if __name__ == '__main__':
	indices = [i for i in range(1, 1190)]
	samples = random.sample(indices, 40)
	print(samples)
	src = r'C:\Urim&Thummim\Rutgers\Spring 2019\Capstone Design\montreal-forced-aligner_win64\montreal-forced-aligner\corpus\czech\Bible'
	des = r'C:\Urim&Thummim\Rutgers\Spring 2019\Capstone Design\montreal-forced-aligner_win64\montreal-forced-aligner\corpus\czech\Bible\Sample_4'
	print(src)
	print(des)
	for i in samples:
		try:
			shutil.copy(src + '\\' + str(i) + '.wav', des + '\\' + str(i) + '.wav')
			shutil.copy(src + '\\' + str(i) + '.lab', des + '\\' + str(i) + '.lab')
		except FileNotFoundError:
			j = random.randint(1, 1189)
			while (j in samples) == True:
				j = random.randint(1, 1189)
			samples.append(j)
		

		
