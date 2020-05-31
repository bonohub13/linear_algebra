#!/usr/bin/python3
#! -*- coding: utf-8 -*-
class Matrix:
    def __init__(self, init_matrix: list=[]):
        # initializer for making a new matrix
        self.init_matrix = self.get_init_matrix(init_matrix)
        if type(init_matrix[0]) == list:
            ver_len = len(init_matrix[0])
            hor_len_check = [len(hor_vector) == ver_len for hor_vector in init_matrix[1:]]
            if False not in hor_len_check:
                self.size = {'horizontal':len(init_matrix[0]), 'vertical':len(init_matrix), 'type':'matrix'}
                self.matrix = [[float(x) for x in init_matrix[i]] for i in range(len(init_matrix))]
            else:
                raise ValueError('The horizontal length for \"init_matrix\" does not match!')
        elif len(init_matrix) > 1:
            self.size = {'horizontal':None, 'vertical':len(init_matrix), 'type':'vector'}
            self.matrix = init_matrix
        else:
            self.matrix = init_matrix[0]
        
        self.T = self.transpose
        self.det = self.determinate

    def __repr__(self):
        return "Matrix({})".format(self.init_matrix)

    def __str__(self):
        if self.size['type'] == 'matrix' or self.size['vertical'] != None:
            output_str = '['
            for i in range(len(self.matrix) - 1):
                output_str += '{}\n '.format(self.matrix[i])
            output_str += '{}]'.format(self.matrix[-1])
        else:
            output_str = '['
            splitter = ''
            for i in range(len(self.matrix)):
                output_str += splitter + '{}'.format(self.matrix[i])
                splitter = ', '
            output_str += ']'
        
        return output_str

    def __len__(self):
        length = (self.size['horizontal'], self.size['vertical'])
        if self.size['type'] == 'vector':
            if length[0] == None:
                return length[1]
            else:
                return length[0]
        else:
            raise TypeError('Cannot return value for len() for matrix, only vector is possible. Please access Matrix().size for size of matrix.')

    def __add__(self, other):
        if type(other) == Matrix:
            return Matrix(self.matrixAdd(other))

    def __radd__(self, other):
        if type(other) == Matrix:
            return Matrix(self.matrixAdd(other))

    def __sub__(self, other):
        if type(other) == Matrix:
            return Matrix(self.matrixSub(other))

    def __rsub__(self, other):
        if type(other) == Matrix:
            return Matrix(self.matrixSub(other))

    def __mul__(self, other):
        if type(other) == Matrix:
            matrix = Matrix(self.matrixMul(other))
            if type(matrix.matrix) == float or type(matrix.matrix) == int:
                return matrix.matrix
            elif self.size['type'] == 'matrix' or self.size['type'] == 'vector':
                matrix.size = self.size
            return matrix
        else:
            return Matrix(self.scala(other))

    def __rmul__(self, other):
        if type(other) == Matrix:
            matrix = Matrix(self.matrixMul(other))
            if type(matrix.matrix) == float or type(matrix.matrix) == int:
                return matrix.matrix
            elif self.size['type'] == 'matrix' or self.size['type'] == 'vector':
                matrix.size = self.size
            return matrix
        else:
            return Matrix(self.scala(other))

    def get_init_matrix(self, init_matrix: list):
        return init_matrix

    def scala(self, x, matrix=None):
        if type(x) != int and type(x) != float:
            raise TypeError('The value of x must be either int or float.')
        return_matrix = []
        if matrix == None:
            tmp_matrix = self.matrix
        else:
            tmp_matrix = matrix
        if self.size['type'] == 'vector':
            for m_i in tmp_matrix:
                return_matrix.append(round(x * m_i, 3))
            return return_matrix
        else:
            for m_i in tmp_matrix:
                ret_m_i = []
                for m_j in m_i:
                    ret_m_i.append(round(x * m_j, 3))
                return_matrix.append(ret_m_i)
            return return_matrix
    
    def transpose(self): #transpose
        if self.size['type'] == 'matrix':
            hor, ver = self.size['horizontal'], self.size['vertical']
            tmp_matrix = []
            for i in range(hor):
                tmp_M_i = []
                for j in range(ver):
                    tmp_M_i.append(self.matrix[j][i])
                tmp_matrix.append(tmp_M_i)
            self.size = {'horizontal':len(tmp_matrix[0]), 'vertical':len(tmp_matrix), 'type':'matrix'}
            self.matrix = tmp_matrix[:]
        elif self.size['type'] == 'vector':
            self.size = {'horizontal':self.size['vertical'], 'vertical':self.size['horizontal'], 'type':'vector'}

    def matrixAdd(self, other):
        if self.size == other.size:
            if self.size['type'] == 'matrix':
                M_out = []
                for i in range(self.size['vertical']):
                    m_i = []
                    for j in range(self.size['horizontal']):
                        m_i.append(round(self.matrix[i][j] + other.matrix[i][j], 3))
                    M_out.append(m_i)
                return M_out
            else:
                M_out = []
                for i in range(len(self.matrix)):
                    M_out.append(round(self.matrix[i] + other.matrix[i], 3))
                return M_out
        raise ValueError('The size of both matrix/vector must match.')

    def matrixSub(self, other):
        if self.size == other.size:
            if self.size['type'] == 'matrix':
                M_out = []
                for i in range(self.size['vertical']):
                    m_i = []
                    for j in range(self.size['horizontal']):
                        m_i.append(round(self.matrix[i][j] - other.matrix[i][j], 3))
                    M_out.append(m_i)
                return M_out
            else:
                M_out = []
                for i in range(len(self.matrix)):
                    M_out.append(round(self.matrix[i] - other.matrix[i], 3))
                return M_out
        raise ValueError('The size of both matrix/vector must match.')
    
    def matrixMul(self, other):
        if self.size['type'] == 'matrix' and other.size['type'] == 'matrix':
            if self.size['horizontal'] == other.size['vertical']:
                M_out = []
                for i in range(self.size['vertical']):
                    m_i = []
                    for j in range(other.size['horizontal']):
                        m_i.append(round(sum([self.matrix[i][k] * other.matrix[k][j] for k in range(self.size['horizontal'])]), 3))
                    M_out.append(m_i)
                self.size = {'horizontal':len(M_out[0]), 'vertical':len(M_out), 'type':'matrix'}
                return M_out
            raise ValueError('The horizontal length of the first matrix and the vertical length of second matrix must match')
        elif self.size['type'] == 'matrix' and other.size['type'] == 'vector':
            M_out = []
            if self.size['horizontal'] == other.size['vertical']:
                for i in range(self.size['vertical']):
                    M_out.append(round(sum([A_i * B_i for A_i, B_i in zip(self.matrix[i], other.matrix)]), 3))
                self.size = {'horizontal':None, 'vertical':len(M_out), 'type':'vector'}
                return M_out
            else:
                raise TypeError('The horizontal length and vertical length of vector must match')
        elif self.size['type'] == 'vector' and other.size['type'] == 'matrix':
            M_out = []
            if self.size['horizontal'] == other.size['vertical']:
                for i in range(other.size['horizontal']):
                    M_out.append(round(sum([A_i * B_i for A_i, B_i in zip(self.matrix, other.matrix[i])]), 3))
                self.size = {'horizontal':len(M_out), 'vertical':None, 'type':'vector'}
                return M_out
        elif self.size['type'] == 'vector' and other.size['type'] == 'vector':
            M_out = []
            if self.size['vertical'] != None and other.size['horizontal'] != None:
                for i in range(self.size['vertical']):
                    m_i = []
                    for j in range(other.size['horizontal']):
                        m_i.append(round(self.matrix[i] * other.matrix[j]))
                    M_out.append(m_i)
                self.size = {'horizontal':len(M_out[0]), 'vertical':len(M_out), 'type':'matrix'}
                return M_out
            elif self.size['horizontal'] != None and other.size['vertical'] != None:
                if self.size['horizontal'] == other.size['vertical']:
                    M_out.append(round(sum([a_i * b_j for a_i, b_j in zip(self.matrix, other.matrix)]), 3))
                    self.size = {'type':type(M_out[0])}
                    return M_out
                else:
                    raise ValueError('When calculating "horizontal vector" * "vertical vector", the size of two vectors must match')
            else:
                raise TypeError('Vector calculation must be either of \"horizontal vector\" * \"vertical vector\" or \"vertical vector\" * \"horizontal vector\"')

    def matrixDiv(self, other):
            pass

    def determinate(self):
        hor, ver = self.size['horizontal'], self.size['vertical']
        if self.size['type'] == 'vector':
            raise TypeError('A determinate cannot be caluculated from a vector')
        elif hor == ver:
            def det2d(matrix:list):
                return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
            def det3d(matrix:list):
                tmp_det = []
                for i in range(len(matrix)):
                    tmp_matrix = []
                    n = 0
                    while len(tmp_matrix) < 2:
                        if n != i:
                            tmp_matrix.append(matrix[n][-2:])
                        n += 1
                    if i%2 == 0:
                        tmp_det.append(det2d(tmp_matrix))
                    else:
                        tmp_det.append(-1 * det2d(tmp_matrix))
                return sum(tmp_det)
            def det4d(matrix:list):
                tmp_det = []
                for i in range(len(matrix)):
                    tmp_matrix = []
                    n = 0
                    while len(tmp_matrix) < 3:
                        if n != i:
                            tmp_matrix.append(matrix[n][-3:])
                        n += 1
                    if i%2 == 0:
                        tmp_det.append(det3d(tmp_matrix))
                    else:
                        tmp_det.append(-1 * det3d(tmp_matrix))
                return sum(tmp_det)
            if ver == 2:
                tmp_M = self.matrix[:]
                return det2d(tmp_M)
            if ver == 3:
                tmp_M = self.matrix[:]
                return det3d(tmp_M)
            if ver == 4:
                tmp_matrix = self.matrix[:]
                return det4d(tmp_matrix)
        else:
            raise ValueError('The horizontal size and vertical size of the matrix must match')

    def matrixRev(self):
        pass

    def GaussianEliminiation(self):
        if self.size['type'] == 'vector':
            raise TypeError('Cannot execute Gaussian Elimination with vector!')
        elif self.size['horizontal'] is not (self.size['vertical'] + 1):
            raise ValueError('The size of matrix must be ({}, {}) in order to execute Gaussian Elimination.'.format(self.size['vertical']+1, self.size['vertical']))
        
        tmp_matrix = [Matrix(hor_vector) for hor_vector in self.matrix]
        for M in tmp_matrix:
            M.T()

        def elimination(loopTimes: int):
            outer_layer = int(self.size['vertical'] - (loopTimes + 1))
            for i in range(loopTimes):
                if tmp_matrix[i+1].matrix[outer_layer] is not 0:
                    tmp_matrix[i+1] = Matrix(tmp_matrix[i+1].scala(tmp_matrix[outer_layer].matrix[outer_layer]/tmp_matrix[i+1].matrix[outer_layer]))
                    tmp_matrix[i+1].T()
                    tmp_matrix[i+1] = tmp_matrix[outer_layer] - tmp_matrix[i+1]

        counter = 1
        while counter < self.size['vertical']:
            elimination(self.size['vertical'] - counter)
            counter += 1

        output_x = [0 for i in range(len(tmp_matrix))]

        for i in range(self.size['vertical']):
            if i == 0:
                output_x[-1] = tmp_matrix[-1].matrix[-1]/tmp_matrix[-1].matrix[-2]
            else:
                for j in range(i):
                    tmp_matrix[-i-1].matrix[-j-2] = tmp_matrix[-i-1].matrix[-j-2] * output_x[-j-1]
                output_x[-i+1] = (tmp_matrix[-i-1].matrix[-1] - sum(tmp_matrix[-i-1].matrix[-i-1:-1]))/tmp_matrix[-i-1].matrix[-i-2]
        
        return output_x

    def InverseMatrix(self):
        if self.size['horizontal'] is not self.size['vertical']:
            raise TypeError('The matrix must be square to inverse.')
        det = self.det()
        tmp_matrix = self.matrix[:]
        identity_matrix = []
        for y in range(self.size['vertical']):
            identity_matrix.append([])
            for x in range(self.size['horizontal']):
                if y == x:
                    tmp_matrix[y].append(1.0)
                    identity_matrix[y].append(1.0)
                else:
                    tmp_matrix[y].append(0.0)
                    identity_matrix[y].append(0.0)

        tmp_matrix = [Matrix(hor_vector) for hor_vector in tmp_matrix]

        for hor_vector in tmp_matrix:
            if hor_vector.size['vertical'] == None:
                hor_vector.T()

        def GaussSeidelElimination(loop_times: int, start: int=0):
            outer_layer = start%self.size['vertical']
            for y in range(loop_times):
                if tmp_matrix[outer_layer].matrix[outer_layer] != 0.0 and y != outer_layer:
                    if tmp_matrix[y].size['vertical'] == None:
                        tmp_matrix[y].T()
                    tmp_matrix[y] = Matrix(tmp_matrix[outer_layer].scala(tmp_matrix[y].matrix[outer_layer]/tmp_matrix[outer_layer].matrix[outer_layer])) - tmp_matrix[y]

        for counter in range(self.size['vertical']):
            GaussSeidelElimination(self.size['vertical'], start=counter)
            print('{}\n'.format(tmp_matrix[counter]) + '-'*20 + '\n')

        for i in range(len(tmp_matrix)):
            if tmp_matrix[i].matrix[i] != 0.0:
                if tmp_matrix[i].matrix[i] < 0:
                    tmp_matrix[i] = tmp_matrix[i].scala(-1/abs(tmp_matrix[i].matrix[i]))
                else:
                    tmp_matrix[i] = tmp_matrix[i].scala(1/tmp_matrix[i].matrix[i])
            else:
                tmp_matrix[i] = tmp_matrix[i].matrix

        check = [tmp_matrix[i][:self.size['vertical']] == identity_matrix[i] for i in range(self.size['vertical'])]
        if False in check:
            for i in range(self.size['vertical']):
                print('{}'.format(tmp_matrix[i]))
            print('Failed to Inverse matrix.')
        else:
            print(Matrix(tmp_matrix))
            tmp_matrix = Matrix([M[(self.size['vertical']-1):] for M in tmp_matrix])
            return tmp_matrix
