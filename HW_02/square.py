#----------------------------------------------------------------------------#
#
# [CS470] Introduction to Artificial Intelligence
# 2015 Fall
# Assignment2 Part2: Finding the length of the shaded square
#
#----------------------------------------------------------------------------#

from Numberjack import *
import time

def model(top, n):
# [Problem2: A and B]
# formulates the problem into CSP model.
# top represents the maximum possible length of the squares.
# n represents the number of squares in total, indexed from 0 to n-1.
# returns the Model()

	pass

def solve(param):
	m = model(param['Top'], param['N'])
	solver = m.load(param['solver'])
	start_time = time.time()
	solver.solve()
	end_time = time.time()
	print 'Length of squares\n', solver.get_solution()
	print 'The length of the 17th square is {0}'.format(solver.get_solution()[16])
	print 'Time taken: %.10f' % (end_time-start_time, )

solve(input({'solver':'Mistral', 'Top':200, 'N':25}))