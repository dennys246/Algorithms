import time
import random
import matplotlib.pyplot as plt
import numpy as np

class sorter():

	def __init__(self):
		self.min_value = 2000
		self.max_value = 20000
		self.step = 2000
		self.sort_functions = [self.bubble_sort, self.merge_sort, self.n_merge_sort, self.n_merge_sort, self.n_merge_sort, self.n_merge_sort, self.n_merge_sort, self.n_merge_sort, self.n_merge_sort]
		self.function_parameters = [None, None, 2, 5, 10, 100, 200, 300, 400]
		self.function_names = ['Bubble Sort', 'Merge Sort'] # Add on non n-split merge functions names
		self.function_names += [f'N-Split Merge Sort - {parameter} Splits' for parameter in self.function_parameters if parameter is not None]
		self.function_timings = []
		self.list_sizes = range(self.min_value, self.max_value, self.step)

	def new_list(self, size):
		self.array = random.sample(range(self.max_value), size)

	def run(self, report = True):
		for function, name, parameter in zip(self.sort_functions, self.function_names, self.function_parameters):
			timing = []
			for size in self.list_sizes:
				self.new_list(size)
				earlier = time.time()
				array = function(parameter = parameter)
				later = time.time()
				confirmation = self.confirm_sort(array)
				if confirmation == False:
					print(f"{name} Failed!")
					return
				speed = (later - earlier)
				timing.append(speed)
				if report == True:
					print(f"{name} on list of {size} values took {round(speed, 3)} seconds")
			self.function_timings.append(timing)

		self.compare_timings()
		self.plot_timings()


	def compare_timings(self):	# Compare times
		bubble_timing = self.function_timings[0]
		merge_timing = self.function_timings[1]
		for t_ind in range(len(bubble_timing)):
			print(f"Size {self.list_sizes[t_ind]} - Speed Improvement of {bubble_timing[t_ind] - merge_timing[t_ind]} seconds")

	def plot_timings(self):
		for ind, name in enumerate(self.function_names):
			plt.plot(self.list_sizes, self.function_timings[ind], label = name)
		plt.xlabel("List Size")
		plt.ylabel("Sort Time (Seconds)")
		plt.title("Sort Functions Timings over List Size")
		plt.legend()
		plt.show()
		plt.close()
		return


	def bubble_sort(self, array = None, parameter = None):
		if array is None: # If no array was passed in
			array = self.array # Grab main class list
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

	def merge_sort(self, array = None, parameter = None):
		if array is None: # If no array was passed in
			array = self.array # Grab the main list attached to the sorted class
		if len(array) <= 1: # Ignore base case of empty or 1 length array (Usual for recursive algorithm)
			return array # Return the already sorted list
		split_pos = round((len(array) - 1)/2) # Calculate split position
		a, b = self.bubble_sort(array[:split_pos]), self.bubble_sort(array[split_pos:]) # Split and sort arrays
		i, j = 0, 0 # Declare first and second list indices
		for k in range(len(array)): # Merge two halfs
			if a[i] < b[j]: # If first list datum is smaller
				array[k] = a[i] # Append first list datum
				i += 1 # Increment first list index
			else: # If second list datum is smaller
				array[k] = b[j] # Append second list datum
				j += 1 # Increment second list index
			if i == len(a) or j == len(b): # If at the end of the list
				while j < len(b):
					array[k + 1] = b[j] # Replace the last data point
					k += 1
					j += 1
				while i < len(a):
					array[k + 1] = a[i]
					k += 1
					i += 1
				break
		return array


	def n_merge_sort(self, array = None, parameter = None):
		if array is None: # If no array was passed in
			array = self.array # Grab the main list attached to the sorted class
		if len(array) <= 1: # Ignore base case of empty or 1 length array (Usual for recursive algorithm)
			return array # Return the already sorted list

		n_splits = parameter # Declare how many times to split the list before merging
		split_size = len(array)/n_splits
		splits = []
		split_indices = [0]*n_splits
		for n in range(n_splits):
			split_start = round(n*split_size)
			split_end = round((n + 1)*split_size) # Calculate split position
			splits.append(self.bubble_sort(array[split_start:split_end])) # Split and sort arrays

		next_values = [splits[split_indice][split_position] for split_indice, split_position in enumerate(split_indices)]
		for k in range(len(array)): # Merge all splits
			min_indice = next_values.index(min(next_values))
			array[k] = next_values[min_indice]
			split_indices[min_indice] += 1
			if split_indices[min_indice] == len(splits[min_indice]):
				split_indices[min_indice] = None
				next_values[min_indice] = self.max_value + 1
			else:
				next_values[min_indice] = splits[min_indice][split_indices[min_indice]]
		return array

	def confirm_sort(self, array):
		for ind, datum in enumerate(array[:(len(array) - 1)]):
			if datum > array[ind + 1]:
				return False
		return True
		
