import os
import sys
import time, datetime
import re
import numpy as np
import pandas as pd
import typing
import logging
from collections import defaultdict
from statistics import mean
from typing import List, Any


class MyLogger:
	def __init__(self, name, text):
		self.name = name
		self.text = text
		self.logger = logging.getLogger(self.name)

	def stream(self):
		stream = logging.StreamHandler()
		self.logger.addHandler(stream)
		self.logger.setLevel(logging.INFO)
		return self.logger.info(self.text)

def timeit(func):
	def wrapper(*args, **kwargs):
		time_before = datetime.datetime.now()
		func(*args, **kwargs)
		time_diff = datetime.datetime.now() - time_before
		return print(f'execution time of "{func.__name__}" function - {time_diff.total_seconds()}')
	return wrapper


FAs_num: List[List[int]] = [[i, i+20, i+40, i+60, i+80, i+100] for i in range(1,21)] #num of FA
IND: float = 2.4600E-03 #U235


def convert_type(val: str) -> float:
	try:
		val = float(val)
		return val
	except Exception as e:
		print(e)
		return False		

class Refueling:
	CWD = os.getcwd()
	INPUT_PATH = os.path.join(CWD, 'input')
	OUTPUT_PATH = os.path.join(CWD, 'output')
	PATTERN = re.compile(r'\.[A-Z]+')

	def __init__(self, name):
		self.file_name = name
		self.data = self.get_data

	@property
	def get_data(self):
		print(f'openning file.... {self.file_name}')
		with open(os.path.join(self.INPUT_PATH, self.file_name), 'r') as f:
			return f.readlines()

	@property
	def q(self):
		return [(n,convert_type(i.split()[1])) for n,i in enumerate(self.data, start=1) if 'MATR' in i and convert_type(i.split()[1]) <= 121]

	def save(self):
		with open(f'out_{self.file_name}', 'w') as out:
			return out.writelines(self.data)


class Average(Refueling):
	def __init__(self, name):
		super().__init__(name)

	@property
	def U5_densities(self):
		upper_line_limit = [n for n,i in enumerate(self.data, start=1) if 'MATR' in i and convert_type(i.split()[1]) == 121]
		return [convert_type(nd.split()[1]) for line_num, nd in enumerate(self.data, start=1) if 'U235' in nd and line_num < upper_line_limit[0]]

	def insert_nulls(self, lst, indexes):
		for i in indexes:
			lst.insert(i, None)
		return lst

	def matrix_and_save(self, obj):
		arr = np.array(obj).reshape((6,4))
		print(arr)
		return pd.DataFrame(arr).to_excel(f'out_{self.file_name}.xlsx')
		 
	@timeit
	def average_burnup(self, FA_dic = defaultdict(list)):
		U5 = self.U5_densities
		for num, u5 in enumerate(U5, start=1):
			for N,FA in enumerate(FAs_num, start=1):
				for matr in FA:
					if matr==num:
						FA_dic[N].append(u5)
		average = self.insert_nulls([1 - mean(i)/IND for n, i in FA_dic.items()], [9,10,13,14])
		return self.matrix_and_save(average)

class Fresh(Refueling):
	FRESH_FUEL: str = "U235 2.4600E-03\nAL   5.3180E-02\nU238 2.4600E-04\nU234 2.7330E-05\nO16  5.4660E-03\n" #* what to write
	
	def __init__(self, name):
		super().__init__(name)

	def replace_save(self, matrs):
		query = self.q
		try:
			for n in range(len(query)):
				for j in matrs:
					if j==query[n][1]:
						self.data[query[n][0]:query[n+1][0]-2] = self.FRESH_FUEL
						query = self.q		
		except Exception as e:
			print(e)
		return self.save()

	@timeit
	def refueling(self):
		fresh_FA = input('Type numbers of FA to refuel: ')
		try:
			convert = int(fresh_FA)
			matrs = FAs_num[convert-1]
			
		except ValueError as VE:
			convert = list(map(lambda x: int(x), fresh_FA.split(','))) 
			matrs = [j for i in convert for j in FAs_num[i-1]]
		return self.replace_save(matrs)

class Swap(Refueling):
	def __init__(self, name):
		super().__init__(name)
	
	def loop(self, matrs, store=None, reverse=False):
		query = self.q
		temp_store = {}
		for num in range(len(query)):
			for n,i in enumerate(matrs):
				if i == query[num][1]:
					if reverse is False:
						temp_store[i] = self.data[query[num][0]:query[num+1][0]-2]
					else:
						self.data[query[num][0]:query[num+1][0]-2] = store[i]
						query = self.q
		return temp_store

	@timeit
	def swap(self):
		swap_num = input('Type numbers of FA to swap: ')
		convert = list(map(lambda x: int(x), self.swap_num.split(','))) 
		first, second = FAs_num[convert[0]-1], FAs_num[convert[1]-1]
		store1, store2 = self.loop(first), self.loop(second)
		swstore1, swstore2 = {k1:v2 for (k1,v1), (k2,v2) in zip(store1.items(),store2.items())}, {k2:v1 for (k1,v1), (k2,v2) in zip(store1.items(),store2.items())}
		self.loop(first, store=swstore1, reverse=True), self.loop(second, store=swstore2, reverse=True)
		return self.save()

if __name__ == '__main__':
	*args, extracted_name = os.path.split(sys.argv[1])
	# extracted_name = sys.argv[1]
	option = int(input('Type option: 1-average burnup, 2-refueling, 3-swap fuel: '))
	if option==1: Average(extracted_name).average_burnup()
	elif option==2: Fresh(extracted_name).refueling()
	elif option==3: Swap(extracted_name).swap()
	
		# print(d)


