import random, time, math


class Pointer:

	def __init__(self):
		self.size = 100000
		self.min = 1
		self.max = 1000000

	def run(self):
		points = self.random_points()
		Px, Py = sort_points(points[:])

		earlier = time.time()
		Cx, Cy = self.closest_pair_OG(Px, Py)
		later = time.time()
		speed = (later - earlier)
		print(f"OG closest path found pair {Cx} & {Cy} in {speed} seconds")

		earlier = time.time()
		Cx, Cy = self.closest_pair(Px, Py)
		later = time.time()
		speed = (later - earlier)
		print(f"New closest path found pair {Cx} & {Cy} in {speed} seconds")

		#earlier = time.time()
		#Bx, By = self.brute_force(Px)
		#later = time.time()
		#speed = (later - earlier)
		#print(f"Brute closest path found pair {Cx} & {Cy} in {speed} seconds")
		#if Cx == Bx and Cy == By:
		#	print('Success!')
		#else:
		#	print(f'Closest pair found ({Cx}, {Cy}) with {self.calc_dist(Cx, Cy)} distance as the closest pair where the brute force function found the pair ({Bx}, {By}) with {self.calc_dist(Bx, By)} distance')

	def brute_force(self, points):
		min_dist = float("inf")
		min_indices = [None, None]
		n = len(points)
		for i in range(n):
			for j in range(i + 1, n):
				point_dist = self.calc_dist(points[i], points[j])
				if min_dist > point_dist:
					min_dist = point_dist
					min_indices = [i, j]
		return points[min_indices[0]], points[min_indices[1]]

	def closest_pair_OG(self, Px, Py):
		if len(Px) <= 3:
			P1, Q1 = self.brute_force(Px)
			return P1, Q1
		Qx = Px[:(len(Px) >> 1)]
		Rx = Px[(len(Px) >> 1):]
		Qy = partition_sort(Qx[:], 1)
		Ry = partition_sort(Rx[:], 1)
		P1, Q1 = self.closest_pair(Qx, Qy)
		D1 = self.calc_dist(P1, Q1)
		P2, Q2 = self.closest_pair(Rx, Ry)
		D2 = self.calc_dist(P2, Q2)
		min_delta = min(D1, D2)
		P3, Q3, D3 = self.closest_split_pair(Px, Py, min_delta)
		if D1 <= D2 and D1 <= D3:
			return P1, Q1
		if D2 <= D1 and D2 <= D3:
			return P2, Q2
		if D3 <= D1 and D3 <= D2:
			return P3, Q3

	def closest_pair(self, Px, Py):
		if len(Px) <= 3:
			P1, Q1 = self.brute_force(Px)
			return P1, Q1
		mid_x = len(Px) >> 1
		Qx = Px[:mid_x]
		Rx = Px[mid_x:]
		Qy, Ry = [], []
		median_x = Px[mid_x]
		for point in Py:
			if point[0] < median_x[0]:
				Qy.append(point)
			else:
				Ry.append(point)
		P1, Q1 = self.closest_pair(Qx, Qy)
		D1 = self.calc_dist(P1, Q1)
		P2, Q2 = self.closest_pair(Rx, Ry)
		D2 = self.calc_dist(P2, Q2)
		min_delta = min(D1, D2)
		P3, Q3, D3 = self.closest_split_pair(Px, Py, min_delta)
		if D1 <= D2 and D1 <= D3:
			return P1, Q1
		if D2 <= D1 and D2 <= D3:
			return P2, Q2
		if D3 <= D1 and D3 <= D2:
			return P3, Q3

	def closest_split_pair(self, Px, Py, min_delta):
		xoi = Px[(len(Px) >> 1)][0]# Biggest x cordinate in left of P
		Sy = [point for point in Py if point[0] > (xoi - min_delta) and point[0] < (xoi + min_delta)]
		best = min_delta
		best_pair = [None, None]
		for i in range(len(Sy) - 1):
			for j in range(i + 1, min(i + 7, len(Sy))):
				delta = self.calc_dist(Sy[i], Sy[j])
				if delta < best:
						best = delta
						best_pair = [Sy[i], Sy[j]]
		if best == min_delta:
			best = min_delta + 1
		return best_pair[0], best_pair[1], best

	def random_points(self):
		return [[random.randint(self.min, self.max), random.randint(self.min, self.max)] for x in range(self.size)]

	def calc_dist(self, P1, P2):
		a = P1[0] - P2[0]
		b = P1[1] - P2[1]
		return math.sqrt(abs(a**2) + abs(b**2))

def confirm_sort(points, xoy):
	for ind, point in enumerate(points[:-1]):
		if point[xoy] > points[ind + 1][xoy]:
			return False
	return True

def partition_sort(points, xoy = None):
	if len(points) <= 1:
		return points
	partition = random.randint(0, len(points) - 1)
	points[0], points[partition] = points[partition], points[0]
	j = 1
	for i in range(1, len(points)):
		if points[i][xoy] < points[0][xoy]:
			points[i], points[j] = points[j], points[i]
			j += 1
	points[0], points[j - 1] = points[j - 1], points[0]
	points[:(j - 1)] = partition_sort(points[:(j - 1)], xoy)
	points[j:] = partition_sort(points[j:], xoy)
	return points

def sort_points(points):
	Px = partition_sort(points[:], 0)
	confirmation = confirm_sort(Px, 0)
	if confirmation == False:
		print('Partition sort failed on Px!')
	Py = partition_sort(points[:], 1)
	confirmation = confirm_sort(Py, 1)
	if confirmation == False:
		print("Partition sort failed on Py!")
	return Px, Py
