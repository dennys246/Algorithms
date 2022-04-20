import random, time
import matplotlib as plt
import numpy as np
import statistics

class sorter:
	def __init__(self):
		self.min_value = 1
		self.max_value = 10000000
		self.size = 1000000
		self.new_list(self.size)

	def new_list(self, size):
		self.list = random.sample(range(self.min_value, self.max_value), size)

	def download_list(self):
		f = open('unsorted_array_2.txt', 'r')
		contents = f.read()
		self.list = contents.split('\n')
		self.list.pop()
		self.list = [int(value) for value in self.list]


	def run(self):

		self.download_list()
		new_list, comparisons = self.quicksort_left(self.list)
		if self.confirm_sort(new_list) == False:
			print('Quicksort with left partition failed!')
		print(f"Quicksort using left index as partition made {comparisons} comparisons...")

		self.download_list()
		new_list, comparisons = self.quicksort_right(self.list)
		if self.confirm_sort(new_list) == False:
			print('Quicksort with right partition failed!')
		print(f"Quicksort using right index as partition made {comparisons} comparisons...")

		self.download_list()
		new_list, comparisons = self.quicksort_median(self.list)
		if self.confirm_sort(new_list) == False:
			print('Quicksort with median partition failed!')
		print(f"Quicksort using median index as partition made {comparisons} comparisons...")


	def confirm_sort(self, array):
		for ind, datum in enumerate(array[:(len(array) - 1)]):
			if datum > array[ind + 1]:
				return False
		return True

	def average(self, array):
		avg = 0
		for number in array:
			avg += number
		return avg/len(array)

	def inplace_quicksort_while(self, array = None):
		if array is None:
			array = self.list
		if len(array) <= 1:
			return array
		i = j = 1
		pivot_ind = self.random_pivot(array)
		if pivot_ind != 0:
			array[0], array[pivot_ind] = array[pivot_ind], array[0]
		pivot = array[0]
		while j < len(array):
			if array[j] < pivot:
				array[j], array[i] = array[i], array[j]
				i += 1
			j += 1
		array[0], array[i - 1] = array[i - 1], array[0]
		array[:(i - 1)] = self.inplace_quicksort_while(array[:(i - 1)])
		array[i:] = self.inplace_quicksort_while(array[i:])
		return array

	def quicksort_left(self, array = None):
		if array is None:
			array = self.list
		if len(array) <= 1:
			return array, 0
		i = j = 1
		pivot_ind = 0
		comparisons = 0
		additional_comparisions = 0
		if pivot_ind != 0:
			array[0], array[pivot_ind] = array[pivot_ind], array[0]
		pivot = array[0]
		comparisons += len(array) - 1
		for j in range(1, len(array)):
			if array[j] < pivot:
				array[j], array[i] = array[i], array[j]
				i += 1
		array[0], array[i - 1] = array[i - 1], array[0]
		array[:(i - 1)], additional_comparisions = self.quicksort_left(array[:(i - 1)])
		comparisons += additional_comparisions
		array[i:], additional_comparisions = self.quicksort_left(array[i:])
		comparisons += additional_comparisions
		return array, comparisons

	def quicksort_right(self, array = None):
		if array is None:
			array = self.list
		if len(array) <= 1:
			return array, 0
		i = j = 1
		pivot_ind = len(array) - 1
		comparisons = 0
		additional_comparisions = 0
		if pivot_ind != 0:
			array[0], array[pivot_ind] = array[pivot_ind], array[0]
		pivot = array[0]
		comparisons += len(array) - 1
		for j in range(1, len(array)):
			if array[j] < pivot:
				array[j], array[i] = array[i], array[j]
				i += 1
		array[0], array[i - 1] = array[i - 1], array[0]
		array[:(i - 1)], additional_comparisions = self.quicksort_right(array[:(i - 1)])
		comparisons += additional_comparisions
		array[i:], additional_comparisions = self.quicksort_right(array[i:])
		comparisons += additional_comparisions
		return array, comparisons

	def quicksort_median(self, array = None):
		if array is None:
			array = self.list
		if len(array) <= 1:
			return array, 0
		i = j = 1

		first = array[0] # Find pivot
		if len(array) % 2 == 0: # If number is even
			middle = array[int((len(array)/2) - 1)]
		else:
			middle = array[len(array) >> 1]
		last = array[-1]
		median_list, count = self.quicksort_left([first, middle, last])
		if first == median_list[1]:
			pivot_ind = 0
		if middle == median_list[1]:
			if len(array) % 2 == 0: # If number is even
				pivot_ind = int((len(array)/2) - 1)
			else:
				pivot_ind = len(array) >> 1
		if last == median_list[1]:
			pivot_ind = len(array) - 1

		comparisons = 0
		additional_comparisions = 0
		if pivot_ind != 0:
			array[0], array[pivot_ind] = array[pivot_ind], array[0]
		pivot = array[0]
		comparisons += len(array) - 1
		for j in range(1, len(array)):
			if array[j] < pivot:
				array[j], array[i] = array[i], array[j]
				i += 1
		array[0], array[i - 1] = array[i - 1], array[0]
		array[:(i - 1)], additional_comparisions = self.quicksort_median(array[:(i - 1)])
		comparisons += additional_comparisions
		array[i:], additional_comparisions = self.quicksort_median(array[i:])
		comparisons += additional_comparisions
		return array, comparisons


	def random_pivot(self, array):
		return random.randint(0, len(array) - 1)

	def bubble_sort(self, array = None, parameter = None):
		if array is None: # If no array was passed in
			array = self.list # Grab main class list
		if len(array) < 2: # If list is too small to sort
			return array # Return already sorted list
		unsorted = True # Declare the list as unsorted
		while unsorted == True: # Continue sorting protocal until sorted
			unsorted = False # Declare that the list could potentially be sorted
			for ind, datum in enumerate(array[:(len(array) - 1)]): # Iterate through list except last indice
				if datum > array[ind + 1]: # If current indice is bigger than the next
					unsorted = True # Declare the list as unsorted
					array[ind], array[ind + 1] = array[ind + 1], array[ind] # Switch the array datum
		return array # Once sorted return the array
