import random, time
import matplotlib as plt
import numpy as np


# First try I found 2397819672 inversion on project
# Second - 2397875107
# Third - 2398596411

class inversion_counter:
	def __init__(self):
		self.min_value = 1
		self.max_value = 11
		self.size = 10
		self.new_list(self.size)

	def new_list(self, size):
		self.list = random.sample(range(self.min_value, self.max_value), size)

	def load_assignment(self):
		f = open('unsorted_array.txt', 'r')
		contents = f.read()
		self.list = contents.split('\n')
		self.list.pop()
		self.list = [int(item) for item in self.list]

	def run(self):
		#print(self.list)

		earlier = time.time()
		brute_inversion_count = self.geeksforgeeks_getInvCount(self.list)
		later = time.time()
		speed = (later - earlier)
		print(f"Geeksforgeeks inversion count function finished in {speed} seconds and found {brute_inversion_count} inversions...")

		earlier = time.time()
		brute_inversion_count = self.brute_count(self.list)
		later = time.time()
		speed = (later - earlier)
		print(f"Brute inversion count finished in {speed} seconds and found {brute_inversion_count} inversions...")

		earlier = time.time()
		array, merge_sort_count = self.mergesort(self.list)
		later = time.time()
		speed = (later - earlier)
		print(f"sort inversion count finished in {speed} seconds and found {merge_sort_count} inversions...")



	def brute_count(self, array):
		inversions = 0
		i = 0
		while i < len(array) - 1:
			j = i + 1
			while j < len(array):
				if array[i] > array[j]:
					inversions += 1
				j += 1
			i += 1
		return inversions

	def geeksforgeeks_getInvCount(self, arr):
		inv_count = 0
		n = len(arr)
		for i in range(n):
			for j in range(i + 1, n):
				if (arr[i] > arr[j]):
					inv_count += 1
		return inv_count


	def mergesort(self, array):

		if len(array) == 1:
			return array, 0

		inversions = count = 0

		mid = len(array) >> 1
		first_array = array[:mid]
		second_array = array[mid:]

		first_array, count = self.mergesort(array[:mid])
		inversions += count
		second_array, count = self.mergesort(array[mid:])
		inversions += count
		array, count = self.merge(first_array, second_array)
		inversions += count

		return array, inversions


	def merge(self, first_array, second_array):
		inversions = i = j = 0
		array = []

		while i < len(first_array) and j < len(second_array):
			if first_array[i] < second_array[j]:
				array.append(first_array[i])
				i += 1
			else:
				array.append(second_array[j])
				inversions += len(first_array) - i
				j += 1

		while i < len(first_array):
			array.append(first_array[i])
			i += 1
		while j < len(second_array):
			array.append(second_array[j])
			j += 1

		return array, inversions
