import copy
from fractions import Fraction
import math

def round(fraction, gap_size, level, direction):
		multiplyer = 1
		for i in range(1,level+1):
			multiplyer = multiplyer * gap_size
		if (direction == 'u'):
			if ((multiplyer * fraction.numerator) % fraction.denominator == 0):
				numerator = (multiplyer*fraction.numerator) // fraction.denominator
			else:
				numerator = (multiplyer*fraction.numerator) // fraction.denominator + 1
			rounded_fraction = Fraction(numerator, multiplyer)
			return rounded_fraction
	
		if (direction == 'd'):
			numerator = (multiplyer * fraction.numerator) // fraction.denominator
			rounded_fraction = Fraction(numerator, multiplyer)
			return rounded_fraction
		return Fraction(0,1)	

class PathPointValue:
	def __init__(self, value, level, rounding_direction):
		self.value = value
		self.level = level
		self.rounding_direction = rounding_direction
	
	def duplicate(self):
		duplicated_path_point_value = PathPointValue(Fraction(self.value.numerator, self.value.denominator), self.level, self.rounding_direction)
		return duplicated_path_point_value

class PathPoint:
	def __init__(self, path_point = []):
		self.path_point = []
		for i in range(0, len(path_point)):
			duplicated_path_point_value = path_point[i].duplicate()
			self.path_point.append(duplicated_path_point_value)
	
	def append(self, path_point_value):
		self.path_point.append(path_point_value.duplicate())
	
	def change_one_coordinate(self, coordinate, new_path_point_value):
		new_path_point = PathPoint()
		for i in range(0, len(self.path_point)):
			if (i == coordinate):
				new_path_point.append(new_path_point_value)
			else:
				new_path_point.append(self.path_point[i])
		return new_path_point



class CoordinateInterval:
	def __init__(self, x, y):
		self.x = x
		self.y = y

class CoordinateIntervalFractalContext:
	def __init__(self, coordinate_interval, precision):
		self.coordinate_interval = coordinate_interval
		self.gaps_contains = None
		self.gaps_contained = []
		self.backtracking_level = None
		self.intermediate_path_level = None
		self.intermediate_path_points = None
		self.extra_backtracking_distance = None

	def set_gaps_contains(self, gap_size, precision):
		if (self.coordinate_interval.x == self.coordinate_interval.y):
			return
		level = 1
		module = (gap_size-1) // 2
		multiplyer = gap_size
		while(level <= precision):
			fraction = Fraction(1, multiplyer)
			if (fraction <= self.coordinate_interval.y - self.coordinate_interval.x):
				if (self.coordinate_interval.x.denominator == multiplyer and self.coordinate_interval.x.numerator%gap_size == module):
					self.gaps_contains = level
				if (self.coordinate_interval.x.numerator*multiplyer%self.coordinate_interval.x.denominator == 0):
					numerator = (self.coordinate_interval.x.numerator*multiplyer) // self.coordinate_interval.x.denominator
				else:
					numerator = ((self.coordinate_interval.x.numerator*multiplyer) // self.coordinate_interval.x.denominator) + 1
				if (numerator % gap_size > module):
					numerator = numerator + gap_size -numerator % gap_size + module
				else:
					numerator = numerator + module - numerator % gap_size
				fraction = Fraction(numerator + 1, multiplyer)
				if (fraction <= self.coordinate_interval.y):
					self.gaps_contains = level
					return
			multiplyer = multiplyer * gap_size
			level = level + 1
	
	def set_gaps_contained(self, gap_size, precision, min_gaps_contains):
		level = 1
		module = (gap_size-1) // 2
		multiplyer = gap_size
		while (level <= precision):
			if (level >= min_gaps_contains):
				numerator = self.coordinate_interval.x.numerator*multiplyer // self.coordinate_interval.x.denominator
				fraction = Fraction(numerator, multiplyer)
				if (fraction >= self.coordinate_interval.x):
					numerator = numerator - 1
				if (numerator % gap_size < module):
					numerator = numerator - numerator % gap_size - (gap_size - module)
				else:
					numerator = numerator - (numerator % gap_size - module)
				fraction = Fraction(numerator+1, multiplyer)
				if(fraction > self.coordinate_interval.y):
					self.gaps_contained.append(level)
			level = level + 1
			multiplyer = multiplyer * gap_size

	def extra_distance_up(self, gap_size, level):
		rounded_up = round(self.coordinate_interval.x, gap_size, level, 'u')
		return (rounded_up - self.coordinate_interval.x) + (rounded_up - self.coordinate_interval.y) - (self.coordinate_interval.y - self.coordinate_interval.x)

	def extra_distance_down(self, gap_size, level):
		rounded_down = round(self.coordinate_interval.x, gap_size, level, 'd')
		return (self.coordinate_interval.x - rounded_down) + (self.coordinate_interval.y - rounded_down) - (self.coordinate_interval.y - self.coordinate_interval.x)

	def set_backtracking_level(self, backtracking_level):
		self.backtracking_level = backtracking_level
	
	def set_backtracking_type(self, gap_size):
		extra_distance_up = self.extra_distance_up(gap_size, self.backtracking_level)
		extra_distance_down = self.extra_distance_down(gap_size, self.backtracking_level)
		if (extra_distance_down < extra_distance_up):
			self.type = 'Bd'
			return
		self.type = 'Bi'
	
	def set_monotone_constant_type(self):
		if (self.coordinate_interval.x == self.coordinate_interval.y):
			self.type = 'C'
			return
		self.type = 'M'
	
	def set_extra_backtracking_distance(self, gap_size):
		if (self.type == 'Bd'):
			self.extra_backtracking_distance = self.extra_distance_down(gap_size, self.backtracking_level)
		else:
			self.extra_backtracking_distance = self.extra_distance_up(gap_size, self.backtracking_level)

	
	def set_intermediate_path_level(self, gap_size, precision):
		for i in range(0, precision + 1):
			if (round(self.coordinate_interval.x, gap_size, i, 'u') <= round(self.coordinate_interval.y, gap_size, i, 'd')):
				self.intermediate_path_level = i
				return

	def set_intermediate_path_points(self, gap_size):
		intermediate_path_points = self.coordinate_interval.x, self.coordinate_interval.y
		if (self.type == 'C'):
			intermediate_path_points = CoordinateInterval(self.coordinate_interval.x, self.coordinate_interval.y)
		if (self.type == 'M'):
			intermediate_path_points = CoordinateInterval(round(self.coordinate_interval.x, gap_size, self.intermediate_path_level, 'u'), round(self.coordinate_interval.y, gap_size, self.intermediate_path_level, 'd'))
		if (self.type == 'Bd'):
			intermediate_path_points = CoordinateInterval(round(self.coordinate_interval.x, gap_size, self.backtracking_level, 'd'), round(self.coordinate_interval.y, gap_size, self.backtracking_level, 'd'))
		if (self.type == 'Bi'):
			intermediate_path_points = CoordinateInterval(round(self.coordinate_interval.x, gap_size, self.backtracking_level, 'u'), round(self.coordinate_interval.y, gap_size, self.backtracking_level, 'u'))
		self.intermediate_path_points = intermediate_path_points

	
class Fractal:
	def __init__(self, dimension, tunnel_number, gap_size, precision = 10):
		self.dimension = dimension
		self.tunnel_number = tunnel_number
		self.gap_size = gap_size
		self.precision = precision
		self.validate_fractal()
		self.coordinate_interval_fractal_context_list = []
		self.min_gaps_contains = None
		self.containment_table = [ [ 0 for i in range(0, dimension) ] for j in range(0, precision + 1) ]
		self.backtracking_data = []
		self.P2_path_list = []
		self.P3_path_list = []
		self.P1_path_list = []
		self.shortest_taxicab_path_length = None

	def validate_fractal(self):
		if (not isinstance(self.dimension, int)):
			raise Exception("The dimension has to be int type.")
		if (not isinstance(self.tunnel_number, int)):
			raise Exception("The dimension has to be int type.")
		if (not isinstance(self.gap_size, int)):
			raise Exception("The gap_size has to be int type.")
		if (self.dimension <= 0):
			raise Exception("The dimension has to be a positive integer.")
		if (self.dimension > 1000000):
			raise Exception("The dimension is too large for the computing purposes.")
		if (self.tunnel_number <= 0):
			raise Exception("The tunnel number has to be a positive integer.")
		if (self.tunnel_number > self.dimension):
			raise Exception("The tunnel number can't be greater than dimension.")
		if (self.gap_size % 2 == 0 or self.gap_size <= 1):
			raise Exception("The gap size has to be an odd integer greater than 1.")
		max_precision = math.log(2**31 - 1) // math.log(self.gap_size)
		if (self.precision > max_precision):
			raise Exception("The precision is too large for the given gap size. Try at most ", max_precision, "for this gap size.")

	def set_background_information(self):
		#setting gaps_contains for all coordinate intervals and setting the minimum
		min_gaps_contains = self.precision + 1
		for i in range(0, self.dimension):
			self.coordinate_interval_fractal_context_list[i].set_gaps_contains(self.gap_size, self.precision)
			if (self.coordinate_interval_fractal_context_list[i].gaps_contains != None):
				if (self.coordinate_interval_fractal_context_list[i].gaps_contains < min_gaps_contains):
					min_gaps_contains = self.coordinate_interval_fractal_context_list[i].gaps_contains
		self.min_gaps_contains = min_gaps_contains

		#setting gaps_contained for all coondinate intervals
		for i in range(0, self.dimension):
			self.coordinate_interval_fractal_context_list[i].set_gaps_contained(self.gap_size, self.precision, self.min_gaps_contains)
		
		#setting containment table
		for i in range(0, self.dimension):
			for j in range(0, len(self.coordinate_interval_fractal_context_list[i].gaps_contained)):
				self.containment_table[self.coordinate_interval_fractal_context_list[i].gaps_contained[j]][i] = 1

		#setting backtracking data
		dinamic_containment_table = copy.deepcopy(self.containment_table)
		possible_backtracking = []
		for i in range(0, self.precision + 1):
			contained = 0
			possible_backtracking.clear()
			for j in range(0, self.dimension):
				if (dinamic_containment_table[i][j] == 1):
					contained = contained + 1
					possible_backtracking.append(j)
			if (contained == self.tunnel_number - 1):
				backtracking_level = i
				least_extra_distance = 1
				for k in range(0, self.tunnel_number - 1):
					extra_distance = min(self.coordinate_interval_fractal_context_list[possible_backtracking[k]].extra_distance_up(self.gap_size, backtracking_level), self.coordinate_interval_fractal_context_list[possible_backtracking[k]].extra_distance_down(self.gap_size, backtracking_level))
					if (extra_distance < least_extra_distance):
						least_extra_distance = extra_distance
						coordinate = possible_backtracking[k]
				backtracking = [coordinate, backtracking_level]
				self.backtracking_data.append(backtracking)
				for k in range(0, self.precision + 1):
					dinamic_containment_table[k][coordinate] = 0

		#setting backtracking levels for each coordinate interval
		for i in range(0, len(self.backtracking_data)):
			self.coordinate_interval_fractal_context_list[self.backtracking_data[i][0]].set_backtracking_level(self.backtracking_data[i][1])
		
		#setting type for each coordinate interval
		for i in range(0, self.dimension):
			if (self.coordinate_interval_fractal_context_list[i].backtracking_level != None):
				self.coordinate_interval_fractal_context_list[i].set_backtracking_type(self.gap_size)
			else:
				self.coordinate_interval_fractal_context_list[i].set_monotone_constant_type()
		
		#setting extra sistance backtracking coordinates travel
		for i in range(0, self.dimension):
			if (self.coordinate_interval_fractal_context_list[i].type == 'Bd' or self.coordinate_interval_fractal_context_list[i].type == 'Bi'):
				self.coordinate_interval_fractal_context_list[i].set_extra_backtracking_distance(self.gap_size)

		#setting intermediate path level for each coordinate interval of type M
		for i in range(0, self.dimension):
			if(self.coordinate_interval_fractal_context_list[i].type == 'M'):
				self.coordinate_interval_fractal_context_list[i].set_intermediate_path_level(self.gap_size, self.precision)
		
		#set intermediate points
		for i in range(0, self.dimension):
			self.coordinate_interval_fractal_context_list[i].set_intermediate_path_points(self.gap_size)


	def find_path(self):
		#find P2: Path from intermediate_path_value.x to intermediate_path_value.y
		path_point = PathPoint()
		for i in range(0, self.dimension):
			path_point.append(PathPointValue(self.coordinate_interval_fractal_context_list[i].intermediate_path_points.x, None, None))
		self.P2_path_list.append(path_point)
		for i in range(0, self.dimension):
			if (path_point.path_point[i].value != self.coordinate_interval_fractal_context_list[i].intermediate_path_points.y):
				new_path_point_value = PathPointValue(self.coordinate_interval_fractal_context_list[i].intermediate_path_points.y, None, None)
				path_point = path_point.change_one_coordinate(i, new_path_point_value)
				self.P2_path_list.append(path_point)
		
		#find P3: Path from intermediate_path_value.y to coordinate_interval.y
		path_point = PathPoint()
		for i in range(0, self.dimension):
			if (self.coordinate_interval_fractal_context_list[i].type == 'C'):
				path_point.append(PathPointValue(self.coordinate_interval_fractal_context_list[i].intermediate_path_points.y, None, None))
			if (self.coordinate_interval_fractal_context_list[i].type == 'M'):
				path_point.append(PathPointValue(self.coordinate_interval_fractal_context_list[i].intermediate_path_points.y, self.coordinate_interval_fractal_context_list[i].intermediate_path_level, 'd'))
			if (self.coordinate_interval_fractal_context_list[i].type == 'Bd'):
				path_point.append(PathPointValue(self.coordinate_interval_fractal_context_list[i].intermediate_path_points.y, self.coordinate_interval_fractal_context_list[i].backtracking_level, 'd'))
			if (self.coordinate_interval_fractal_context_list[i].type == 'Bi'):
				path_point.append(PathPointValue(self.coordinate_interval_fractal_context_list[i].intermediate_path_points.y, self.coordinate_interval_fractal_context_list[i].backtracking_level, 'u'))
		self.P3_path_list.append(path_point)
		for k in range(0, self.precision+1):
			for i in range(0, self.dimension):
				if (path_point.path_point[i].level == k and path_point.path_point[i].value != self.coordinate_interval_fractal_context_list[i].coordinate_interval.y):
					new_value = round(self.coordinate_interval_fractal_context_list[i].coordinate_interval.y, self.gap_size, k+1, path_point.path_point[i].rounding_direction)
					new_path_point_value = PathPointValue(new_value, k+1, path_point.path_point[i].rounding_direction)
					path_point = path_point.change_one_coordinate(i, new_path_point_value)
					self.P3_path_list.append(path_point)
		for i in range(0, self.dimension):
			if (path_point.path_point[i].value != self.coordinate_interval_fractal_context_list[i].coordinate_interval.y):
				new_value = self.coordinate_interval_fractal_context_list[i].coordinate_interval.y
				new_path_point_value = PathPointValue(new_value, None, None)
				self.P1_path_list.append(path_point)
		
		#find P1: Path from intermediate_path_value.x to coordinate_interval_x
		path_point = PathPoint()
		for i in range(0, self.dimension):
			if (self.coordinate_interval_fractal_context_list[i].type == 'C'):
				path_point.append(PathPointValue(self.coordinate_interval_fractal_context_list[i].intermediate_path_points.x, None, None))
			if (self.coordinate_interval_fractal_context_list[i].type == 'M'):
				path_point.append(PathPointValue(self.coordinate_interval_fractal_context_list[i].intermediate_path_points.x, self.coordinate_interval_fractal_context_list[i].intermediate_path_level, 'u'))
			if (self.coordinate_interval_fractal_context_list[i].type == 'Bd'):
				path_point.append(PathPointValue(self.coordinate_interval_fractal_context_list[i].intermediate_path_points.x, self.coordinate_interval_fractal_context_list[i].backtracking_level, 'd'))
			if (self.coordinate_interval_fractal_context_list[i].type == 'Bi'):
				path_point.append(PathPointValue(self.coordinate_interval_fractal_context_list[i].intermediate_path_points.x, self.coordinate_interval_fractal_context_list[i].backtracking_level, 'd'))
		self.P1_path_list.append(path_point)
		for k in range(0, self.precision+1):
			for i in range(0, self.dimension):
				if (path_point.path_point[i].level == k and path_point.path_point[i].value != self.coordinate_interval_fractal_context_list[i].coordinate_interval.x):
					new_value = round(self.coordinate_interval_fractal_context_list[i].coordinate_interval.x, self.gap_size, k+1, path_point.path_point[i].rounding_direction)
					new_path_point_value = PathPointValue(new_value, k+1, path_point.path_point[i].rounding_direction)
					path_point = path_point.change_one_coordinate(i, new_path_point_value)
					self.P1_path_list.append(path_point)
		for i in range(0, self.dimension):
			if (path_point.path_point[i].value != self.coordinate_interval_fractal_context_list[i].coordinate_interval.x):
				new_value = self.coordinate_interval_fractal_context_list[i].coordinate_interval.x
				new_path_point_value = PathPointValue(new_value, None, None)
				self.P1_path_list.append(path_point)
		
	def find_shortest_taxicab_path(self, start_point, finish_point):
		self.validate_points(start_point, finish_point)
		for i in range (0, self.dimension):
			coordinate_interval = CoordinateInterval(start_point[i], finish_point[i])
			coordinate_interval_fractal_context = CoordinateIntervalFractalContext(coordinate_interval, self.precision)
			self.coordinate_interval_fractal_context_list.append(coordinate_interval_fractal_context)

		self.set_background_information()
		self.find_path()

		#combine the complete path
		path = []
		point = []
		for i in range(len(self.P1_path_list)-1, -1, -1):
			point.clear()
			for j in range(0, self.dimension):
				value = Fraction(self.P1_path_list[i].path_point[j].value.numerator, self.P1_path_list[i].path_point[j].value.denominator)
				point.append(value)
			path.append(copy.deepcopy(point))
		for i in range(1, len(self.P2_path_list)):
			point.clear()
			for j in range(0, self.dimension):
				value = Fraction(self.P2_path_list[i].path_point[j].value.numerator, self.P2_path_list[i].path_point[j].value.denominator)
				point.append(value)
			path.append(copy.deepcopy(point))
		for i in range(1, len(self.P3_path_list)):
			point.clear()
			for j in range(0, self.dimension):
				value = Fraction(self.P3_path_list[i].path_point[j].value.numerator, self.P3_path_list[i].path_point[j].value.denominator)
				point.append(value)
			path.append(copy.deepcopy(point))
		
		#set the length of the path
		distance = Fraction(0, 1)
		for i in range(0, self.dimension):
			if (self.coordinate_interval_fractal_context_list[i].type == 'Bd' or self.coordinate_interval_fractal_context_list[i].type == 'Bi'):
				distance = distance + (self.coordinate_interval_fractal_context_list[i].coordinate_interval.y - self.coordinate_interval_fractal_context_list[i].coordinate_interval.x) + self.coordinate_interval_fractal_context_list[i].extra_backtracking_distance
			else:
				distance = distance + (self.coordinate_interval_fractal_context_list[i].coordinate_interval.y - self.coordinate_interval_fractal_context_list[i].coordinate_interval.x)
		self.shortest_taxicab_path_length = distance
		return path

	def insideFractal(self, point):
		multiplyer = self.gap_size
		module = (self.gap_size - 1) // 2
		for k in range(1, self.precision + 1):
			number_of_coordinates_inside_k_gaps = 0
			for i in range (0, self.dimension):
				numerator = round(point[i], self.gap_size, k, 'd') * multiplyer
				if (numerator % self.gap_size == module and point[i]!= round(point[i], self.gap_size, k, 'd')):
					number_of_coordinates_inside_k_gaps = number_of_coordinates_inside_k_gaps + 1
			if (number_of_coordinates_inside_k_gaps >= self.tunnel_number):
				return False
		return True

	def validate_points(self, start_point, finish_point):
		if (len(start_point) != self.dimension or len(finish_point) != self.dimension):
			raise Exception("The dimension of points doesn't match the dimension of the fractal.")
		for i in range(0, self.dimension):
			if((not isinstance(start_point[i],Fraction)) or (not isinstance(finish_point[i], Fraction))):
				raise Exception("Points should be Fraction type.")
		if (not self.insideFractal(start_point)):
			raise Exception("Starting point should be inside the fractal.")
		if (not self.insideFractal(finish_point)):
			raise Exception("Finishing point should be inside the fractal.")
		for i in range (0, self.dimension):
			if (start_point[i] > finish_point[i]):
				raise Exception("Sorry, currently this algorithm only works if each coordinate of the starting point is less then or equal to the corresponding coordinate of finishing point.")
	