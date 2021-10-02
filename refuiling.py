import os
import sys
import time
import re
import numpy as np
import pandas as pd
from collections import defaultdict
from statistics import mean

pattern = re.compile(r'\.[A-Z]+')
cwd = os.getcwd()
name = sys.argv[1] # gets name of file from cmd
name = name[2:] if name.startswith('.') else name
print(name)
query = [i for i in os.listdir(cwd) if re.search(pattern, i) is not None and name in i]

FAs_num = [[i, i+20, i+40, i+60, i+80, i+100] for i in range(1,21)] #num of FA
# print(FAs_num)
ind = 2.4600E-03 #U235
refuilng = "U235 2.4600E-03\nAL   5.3180E-02\nU238 2.4600E-04\nU234 2.7330E-05\nO16  5.4660E-03\n" #* what to write

def convert_type(val):
	try:
		bool(float(val))
		return float(val)
	except Exception as e:
		print(e)
		return False

def work_with_store(dic, itr, value):
	check = [dic[FAs_num.index(i)+1].append(value) for i in FAs_num for j in i if j==itr]

def q(data):
	return [(n,convert_type(i.split()[1]))  for n,i in enumerate(data, start=1) if 'MATR' in i and convert_type(i.split()[1]) <= 121]

def drawing(file, average):
	for i in range(4):
		if i < 2:
			average.insert(11, None)
		elif i >= 2:
			average.insert(9, None)
	arr_to_print = np.array(average)
	reshaped = arr_to_print.reshape(6,4)
	print(reshaped)
	pd.DataFrame(reshaped).to_excel(f"out_{re.search(r'[a-zA-Z0-9]+', file).group(0)}.xlsx", index=False, header=False)
		

def average_burnup(l, data, file, store):
	for num in range(0,len(l)):
		try:
			for nd in data[l[num][0]:l[num+1][0]-2]:
				if 'U235' in nd:
					work_with_store(store, num+1, convert_type(nd.split()[1]))
		except IndexError as e:
			print(e)
	# aver = [format((1-mean(i)/ind)*100, '.3f') for i in store.values()]
	aver = [1-mean(i)/ind for i in store.values()]
	print(aver)
	drawing(file, aver)
	print(time.process_time())

def fresh_fuel(l, data, file):
	reset_FA = input('Type numbers of FA to reset: ')
	try:
		convert = int(reset_FA)
		matrs = FAs_num[convert-1]
	except ValueError as VE:
		convert = list(map(lambda x: int(x), reset_FA.split(','))) 
		matrs = [j for i in convert for j in FAs_num[i-1]]
	print(matrs)
	print(l)
	for num in range(0,len(l)):
		for n,i in enumerate(matrs):
			if i == l[num][1]:
				data[l[num][0]:l[num+1][0]-2] = refuilng
				l = q(data)
	print(time.process_time())
	with open(f'out_{file}', 'w') as o:
		o.writelines(data)

class Refueling:
	# def __init__(self):
	def get_data(self):
		for file in query:
			print(f'openning file.... {file}')
			store = defaultdict(list)
			with open(file, 'r') as f:
				self.data = f.readlines()
			self.l = q(self.data)
			option = int(input('Type option: 1-average, 2-reset densities, 3-swap fuel: '))
			if option==1: average_burnup(self.l, self.data, file, store)
			elif option==2: fresh_fuel(self.l, self.data, file)
			elif option==3: self.FA_swap(file)


	def loop(self, matrs, store=None, reverse=False):
		temp_store = {}
		for num in range(0,len(self.l)):
			for n,i in enumerate(matrs):
				if i == self.l[num][1]:
					if reverse is False:
						temp_store[i] = self.data[self.l[num][0]:self.l[num+1][0]-2]
					else:
						self.data[self.l[num][0]:self.l[num+1][0]-2] = store[i]
						self.l = q(self.data)
		return temp_store

	def FA_swap(self,file):
		swap_num = input('Type numbers of FA to swap: ')
		convert = list(map(lambda x: int(x), swap_num.split(','))) 
		first, second = FAs_num[convert[0]-1], FAs_num[convert[1]-1]
		print(first)
		store1, store2 = self.loop(first), self.loop(second)
		swstore1, swstore2 = {k1:v2 for (k1,v1), (k2,v2) in zip(store1.items(),store2.items())}, {k2:v1 for (k1,v1), (k2,v2) in zip(store1.items(),store2.items())}
		self.loop(first, store=swstore1, reverse=True), self.loop(second, store=swstore2, reverse=True)
		with open(f'out_{file}', 'w') as o:
			o.writelines(self.data)



			

if __name__ == '__main__':
	Refueling(). get_data()
		# print(d)


