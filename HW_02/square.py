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

    v = VarArray(n, 1, top)
    model = Model([
        # global
        AllDiff(v),
        v[0] == 1,
        # width
        v[24] == v[23] + v[19] + v[18],
        v[18] == v[5] + v[15],
        v[12] + v[11] == v[19] + v[5],
        v[15] == v[1] + v[14],
        v[13] == v[11] + v[1],
        v[13] + v[14] == v[22],
        v[23] + v[12] == v[17] + v[7] + v[10] + v[16],
        v[7] == v[6] + v[4],
        v[4] == v[3] + v[0],
        v[6] + v[3] + v[2] == v[8],
        v[7] + v[10] == v[8] + v[9],
        v[16] + v[9] == v[21],
        v[17] + v[8] == v[20],
        v[20] + v[21] + v[22] == v[24],
        # height
        v[24] == v[23] + v[17] + v[20],
        v[17] == v[7] + v[6] + v[8],
        v[6] == v[4] + v[3],
        v[3] == v[0] + v[2],
        v[7] + v[4] + v[0] == v[10],
        v[17] + v[20] == v[16] + v[21],
        v[16] == v[10] + v[9],
        v[23] == v[19] + v[12],
        v[19] == v[18] + v[5],
        v[11] + v[13] + v[22] == v[12] + v[16] + v[21],
        v[11] + v[5] == v[15] + v[1],
        v[13] + v[1] == v[14],
        v[18] + v[15] + v[14] + v[22] == v[24],
        # area
        reduce(lambda x,y: x + y*y, v[:24]) == v[24] * v[24],
        ])

    # order
    for i in range(n-1):
        model.add(v[i] < v[i+1])

    return model

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
