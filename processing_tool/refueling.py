import os
import sys
import time
import re
import numpy as np
import logging
# from .model import *
from collections import defaultdict
from statistics import mean

FAs_num = [[i, i+20, i+40, i+60, i+80, i+100] for i in range(1,21)] #num of FA
IND = 2.4600E-03 #U235


def convert_type(val):
	try:
		return float(val)
	except Exception as e:
		print(e)
		return False

class Refueling():
	CWD = os.getcwd()
	INPUT_PATH = os.path.join(CWD, 'input')
	OUTPUT_PATH = os.path.join(CWD, 'output')
	PATTERN = re.compile(r'\.[A-Z]+')

	def __init__(self, name=None, data=None, *args, **kwargs):
		self.file_name = name
		if data is not None:
			self.data = data

	@property
	def load_data(self):
		print(f'openning file.... {self.file_name}')
		with open(os.path.join(self.INPUT_PATH, self.file_name), 'r') as f:
			return f.readlines()

	@property
	def q(self):
		return [(n,convert_type(i.split()[1])) for n,i in enumerate(self.data, start=1) if 'MATR' in i and convert_type(i.split()[1]) <= 121]

	def save(self):
		print(self.file_name)
		self.save_path = os.path.join(self.INPUT_PATH, self.file_name)
		with open(self.save_path, 'w') as out:
			return out.writelines(self.data)

	@property
	def for_download(self):
		with open(os.path.join(self.OUTPUT_PATH, self.file_name), 'w') as out:
			return out.writelines(self.data)


class Average(Refueling):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.data = kwargs['pdc']

	@property
	def U5_densities(self):
		upper_line_limit = [n for n,i in enumerate(self.data, start=1) if 'MATR' in i and convert_type(i.split()[1]) == 121]
		return [convert_type(nd.split()[1]) for line_num, nd in enumerate(self.data, start=1) if 'U235' in nd and line_num < upper_line_limit[0]]

	def insert_nulls(self, lst, indexes):
		for i in indexes:
			lst.insert(i, 0)
		return lst

	def matrix_and_save(self, obj):
		arr = np.array(obj).reshape((6,4))
		return arr, self.data
		 
	def average_burnup(self, FA_dic = defaultdict(list)):
		if len(FA_dic) > 0: FA_dic.clear()
		U5 = self.U5_densities
		for num, u5 in enumerate(U5, start=1):
			for N,FA in enumerate(FAs_num, start=1):
				for matr in FA:
					if matr==num:
						FA_dic[N].append(u5)
		average = self.insert_nulls([np.around((1 - mean(i)/IND)*100, decimals = 2) for n, i in FA_dic.items()], [9,10,13,14])
		FA_dic.clear()
		cells_map = np.array(average).reshape((6,4))
		return cells_map, self.data

class Fresh(Refueling):
	FRESH_FUEL: str = "U235 2.4600E-03\n--AL   5.3180E-02\n--U238 2.4600E-04\n--U234 2.7330E-05\n--O16  5.4660E-03\n" #* what to write
	
	def __init__(self, fresh_FA, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.data = kwargs["pdc"]
		self.fresh_FA = fresh_FA

	def replace_save(self, matrs):
		query = self.q #* get lines number
		try:
			for n in range(len(query)):
				for j in matrs:
					if j==query[n][1]:
						self.data[query[n][0]:query[n+1][0]-2] = self.FRESH_FUEL.split("--")
						query = self.q  #* update lines number after replacement
		except Exception as e:
			print(e)
		return Average(pdc=self.data).average_burnup()  # ---> ref to average

	def refueling(self):
		try:
			convert = int(self.fresh_FA)
			matrs = FAs_num[convert-1]
		except ValueError:
			convert = list(map(lambda x: int(x), self.fresh_FA.split(','))) 
			matrs = [j for i in convert for j in FAs_num[i-1]]
			print(f'got numbers - {matrs}')
		return self.replace_save(matrs)

class Swap(Refueling):
	def __init__(self, swap_FA, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.data = kwargs["pdc"]
		self.swap_FA = swap_FA
	
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

	def swap(self):
		convert = list(map(lambda x: int(x), self.swap_FA.split(','))) 
		first, second = FAs_num[convert[0]-1], FAs_num[convert[1]-1]
		store1, store2 = self.loop(first), self.loop(second)
		swstore1, swstore2 = {k1:v2 for (k1, _), (_,v2) in zip(store1.items(),store2.items())}, {k2:v1 for (_,v1), (k2,_) in zip(store1.items(),store2.items())}
		self.loop(first, store=swstore1, reverse=True), self.loop(second, store=swstore2, reverse=True)
		return Average(pdc=self.data).average_burnup()  # ---> ref to average



