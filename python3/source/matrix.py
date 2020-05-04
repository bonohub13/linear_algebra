#!/usr/bin/python3
#! -*- coding: utf-8 -*-
class Matrix:
    def __init__(self, init_matrix: list=[]):
        # initializer for making a new matrix
        self.init_matrix = self.get_init_matrix(init_matrix)
        if init_matrix != [] and len(init_matrix) > 1 and type(init_matrix[0]) == list:
            len_check = 0
            for i in range(len(init_matrix) - 1):
                if init_matrix[i].__len__() != init_matrix[i+1].__len__():
                    len_check += 1
            if len_check == 0:
                self.size = {'horizontal':len(init_matrix[0]), 'vertical':len(init_matrix), 'type':'matrix'}
                self.matrix = init_matrix
            else:
                raise ValueError('The size for the argument \"init_matrix\" does not match. The size of the matrix must be the same.')
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
        return (self.size['horizontal'], self.size['vertical'])

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
            if self.size['type'] == 'matrix' or self.size['type'] == 'vector':
                matrix.size = self.size
            return matrix
        else:
            return Matrix(self.scala(other))

    def __rmul__(self, other):
        if type(other) == Matrix:
            matrix = Matrix(self.matrixMul(other))
            if self.size['type'] == 'matrix' or self.size['type'] == 'vector':
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
                return_matrix.append(x * m_i)
            return return_matrix
        else:
            for m_i in tmp_matrix:
                ret_m_i = []
                for m_j in m_i:
                    ret_m_i.append(x * m_j)
                return_matrix.append(ret_m_i)
            return return_matrix
    
    def transpose(self): #transpose
        if self.size['type'] == 'matrix':
            hor, ver = self.__len__()
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
                        m_i.append(self.matrix[i][j] + other.matrix[i][j])
                    M_out.append(m_i)
                return M_out
            else:
                M_out = []
                for i in range(len(self.matrix)):
                    M_out.append(self.matrix[i] + other.matrix[i])
                return M_out
        raise ValueError('The size of both matrix/vector must match.')

    def matrixSub(self, other):
        if self.size == other.size:
            if self.size['type'] == 'matrix':
                M_out = []
                for i in range(self.size['vertical']):
                    m_i = []
                    for j in range(self.size['horizontal']):
                        m_i.append(self.matrix[i][j] - other.matrix[i][j])
                    M_out.append(m_i)
                return M_out
            else:
                M_out = []
                for i in range(len(self.matrix)):
                    M_out.append(self.matrix[i] - other.matrix[i])
                return M_out
        raise ValueError('The size of both matrix/vector must match.')
    
    def matrixMul(self, other):
        if self.size['type'] == 'matrix' and other.size['type'] == 'matrix':
            if self.size['horizontal'] == other.size['vertical']:
                M_out = []
                for i in range(self.size['vertical']):
                    m_i = []
                    for j in range(other.size['horizontal']):
                        m_i.append(sum([self.matrix[i][k] * other.matrix[k][j] for k in range(self.size['horizontal'])]))
                    M_out.append(m_i)
                self.size = {'horizontal':len(M_out[0]), 'vertical':len(M_out), 'type':'matrix'}
                return M_out
            raise ValueError('The horizontal length of the first matrix and the vertical length of second matrix must match')
        elif self.size['type'] == 'matrix' and other.size['type'] == 'vector':
            M_out = []
            if self.size['horizontal'] == other.size['vertical']:
                for i in range(self.size['vertical']):
                    M_out.append(sum([A_i * B_i for A_i, B_i in zip(self.matrix[i], other.matrix)]))
                self.size = {'horizontal':None, 'vertical':len(M_out), 'type':'vector'}
                return M_out
            else:
                raise TypeError('The horizontal length and vertical length of vector must match')
        elif self.size['type'] == 'vector' and other.size['type'] == 'matrix':
            M_out = []
            if self.size['horizontal'] == other.size['vertical']:
                for i in range(other.size['horizontal']):
                    M_out.append(sum([A_i * B_i for A_i, B_i in zip(self.matrix, other.matrix[i])]))
                self.size = {'horizontal':len(M_out), 'vertical':None, 'type':'vector'}
                return M_out
        elif self.size['type'] == 'vector' and other.size['type'] == 'vector':
            M_out = []
            if self.size['vertical'] != None and other.size['horizontal'] != None:
                for i in range(self.size['vertical']):
                    m_i = []
                    for j in range(other.size['horizontal']):
                        m_i.append(self.matrix[i] * other.matrix[j])
                    M_out.append(m_i)
                self.size = {'horizontal':len(M_out[0]), 'vertical':len(M_out), 'type':'matrix'}
                return M_out
            elif self.size['horizontal'] != None and other.size['vertical'] != None:
                if self.size['horizontal'] == other.size['vertical']:
                    M_out.append(sum([a_i * b_j for a_i, b_j in zip(self.matrix, other.matrix)]))
                    self.size = {'type':type(M_out[0])}
                    return M_out
                else:
                    raise ValueError('When calculating "horizontal vector" * "vertical vector", the size of two vectors must match')
            else:
                raise TypeError('Vector calculation must be either of \"horizontal vector\" * \"vertical vector\" or \"vertical vector\" * \"horizontal vector\"')
    def matrixDiv(self, other):
        pass

    def determinate(self):
        if self.size['type'] == 'vector':
            raise TypeError('A determinate cannot be caluculated from a vector')
        elif self.__len__()[0] == self.__len__()[1]:
            hor, ver = self.__len__()
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
                tmp_M = self.matrix[:]
                return det4d(tmp_M)
        else:
            raise ValueError('The horizontal size and vertical size of the matrix must match')

    def matrixRev(self):
        pass
