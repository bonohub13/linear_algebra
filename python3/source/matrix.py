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
        self.det = self.determinant
        self.inv = self.InverseMatrix

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
            tmp_matrix = Matrix(self.matrixAdd(other))
            if tmp_matrix.size['type'] == 'vector' and tmp_matrix.size['horizontal'] != None:
                tmp_matrix.T()
            return tmp_matrix

    def __radd__(self, other):
        if type(other) == Matrix:
            tmp_matrix = Matrix(self.matrixAdd(other))
            if tmp_matrix.size['type'] == 'vector' and tmp_matrix.size['horizontal'] != None:
                tmp_matrix.T()
            return tmp_matrix

    def __sub__(self, other):
        if type(other) == Matrix:
            tmp_matrix = Matrix(self.matrixSub(other))
            if tmp_matrix.size['type'] == 'vector' and tmp_matrix.size['horizontal'] != None:
                tmp_matrix.T()
            return tmp_matrix

    def __rsub__(self, other):
        if type(other) == Matrix:
            tmp_matrix = Matrix(self.matrixSub(other))
            if tmp_matrix.size['type'] == 'vector' and tmp_matrix.size['horizontal'] != None:
                tmp_matrix.T()
            return tmp_matrix

    def __mul__(self, other):
        if type(other) == Matrix:
            matrix = Matrix(self.matrixMul(other))
            if type(matrix.matrix) == float or type(matrix.matrix) == int:
                return matrix.matrix
            elif self.size['type'] == 'matrix' or self.size['type'] == 'vector':
                matrix.size = self.size
            return matrix
        else:
            tmp_matrix = Matrix(self.scala(other))
            if tmp_matrix.size['type'] == 'vector' and tmp_matrix.size['horizontal'] != None:
                tmp_matrix.T()
            return tmp_matrix

    def __rmul__(self, other):
        if type(other) == Matrix:
            matrix = Matrix(self.matrixMul(other))
            if type(matrix.matrix) == float or type(matrix.matrix) == int:
                return matrix.matrix
            elif self.size['type'] == 'matrix' or self.size['type'] == 'vector':
                matrix.size = self.size
            return matrix
        else:
            tmp_matrix = Matrix(self.scala(other))
            if tmp_matrix.size['type'] == 'vector' and tmp_matrix.size['horizontal'] != None:
                tmp_matrix.T()
            return tmp_matrix

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

    def determinant(self):
        hor, ver = self.size['horizontal'], self.size['vertical']
        if self.size['type'] == 'vector':
            raise TypeError('A determinate cannot be caluculated from a vector')
        elif hor == ver:
            def det2d():
                return self.matrix[0][0] * self.matrix[1][1] - self.matrix[0][1] * self.matrix[1][0]

            def triangularMatrix():
                det = 1.0
                tmp_matrix = [Matrix(vector) for vector in self.matrix]
                #switching rows if the diagonal line includes a 0
                for diag in range(len(tmp_matrix)):
                    if tmp_matrix[diag].matrix[diag] == 0.0:
                        tmp_copy = tmp_matrix[:]
                        for i in range(len(tmp_matrix)-1):
                            if 0.0 not in tmp_matrix[i].matrix[:diag+1]:
                                tmp_matrix[diag] = tmp_copy[i]
                                tmp_matrix[i] = tmp_copy[diag]
                                det = -1*det

                #Checking if the matrix is already triangular
                check = ['construct' if 0.0 not in tmp_matrix[check_range+1].matrix[:check_range+1] else 'pass' for check_range in range(len(tmp_matrix)-1)]
                
                if 'construct' in check:
                    #construct triangular matrix out of original matrix
                    for inner in range(len(tmp_matrix)-1):
                        for outer in range(len(tmp_matrix)-1):
                            if tmp_matrix[outer+1].matrix[inner] != 0.0 and (outer + 1) != inner:
                                if tmp_matrix[inner].matrix[inner] != 0.0:
                                    scalar = tmp_matrix[outer+1].matrix[inner]/tmp_matrix[inner].matrix[inner]
                                    placeholder = inner
                                else:
                                    for tmp_outer in range(len(tmp_matrix)):
                                        if tmp_outer != outer and tmp_matrix[tmp_outer].matrix[inner] != 0.0:
                                            scalar = tmp_matrix[outer+1].matrix[inner]/tmp_matrix[tmp_outer].matrix[inner]
                                            placeholder = tmp_outer
                                            if tmp_outer < (len(tmp_matrix)-1):
                                                break
                                        
                                tmp_matrix[outer+1] = tmp_matrix[outer+1] - scalar*tmp_matrix[placeholder]
                
                for diag in range(len(tmp_matrix)):
                    det *= tmp_matrix[diag].matrix[diag]

                tmp_matrix = Matrix([vector.matrix for vector in tmp_matrix])

                return float(round(det, 4))

            if len(self.matrix) == 2:
                return det2d()
            else:
                return triangularMatrix()
        else:
            raise ValueError('The horizontal size and vertical size of the matrix must match')

    def GaussianEliminiation(self):
        if self.size['type'] == 'vector':
            raise TypeError('Cannot execute Gaussian Elimination with vector!')
        elif self.size['horizontal'] is not (self.size['vertical'] + 1):
            raise ValueError('The size of matrix must be ({}, {}) in order to execute Gaussian Elimination.'.format(self.size['vertical']+1, self.size['vertical']))
        
        tmp_matrix = [Matrix(hor_vector) for hor_vector in self.matrix]

        def elimination(loopTimes: int):
            outer_layer = int(self.size['vertical'] - (loopTimes + 1))
            for i in range(loopTimes):
                if tmp_matrix[i+1].matrix[outer_layer] is not 0:
                    tmp_matrix[i+1] = Matrix(tmp_matrix[i+1].scala(tmp_matrix[outer_layer].matrix[outer_layer]/tmp_matrix[i+1].matrix[outer_layer]))
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

        def GaussJordanElimination(matrix: list, identity_matrix: list):
            #compute triangular matrix
            for inner in range(len(matrix)-1):
                for outer in range(len(matrix)-1):
                    if matrix[outer+1].matrix[inner] != 0.0 and (outer+1) != inner:
                        if matrix[inner].matrix[inner] != 0.0:
                            scalar = matrix[outer+1].matrix[inner]/matrix[inner].matrix[inner]
                            placeholder = inner
                        else:
                            for tmp_outer in range(len(matrix)):
                                if tmp_outer != outer and matrix[tmp_outer].matrix[inner] != 0.0:
                                    scalar = matrix[outer+1].matrix[inner]/matrix[tmp_outer].matrix[inner]
                                    placeholder = tmp_outer
                                    if tmp_outer < (len(matrix)-1):
                                        break
                        matrix[outer+1] = matrix[outer+1] - scalar*matrix[placeholder]
                        identity_matrix[outer+1] = identity_matrix[outer+1] - scalar*identity_matrix[placeholder]

            #make the value of the diagonal line into 1.0
            for diag in range(len(matrix)-1):
                if matrix[diag+1].matrix[diag+1] != 0.0:
                    matrix[diag+1] = 1/matrix[diag+1].matrix[diag+1]*matrix[diag+1]
                    identity_matrix[diag+1] = 1/matrix[diag+1].matrix[diag+1]*identity_matrix[diag+1]

            #compute using the GaussJordanElimination method on triangular matrix to find the inverse matrix
            for inner in range(len(matrix)-1):
                for outer in range(len(matrix)):
                    if matrix[outer].matrix[inner+1] != 0.0 and matrix[inner+1].matrix[inner+1] != 0.0 and inner+1 != outer:
                        scalar = matrix[outer].matrix[inner+1]/matrix[inner+1].matrix[inner+1]
                        matrix[outer] -= scalar*matrix[inner+1]
                        identity_matrix[outer] -= scalar*identity_matrix[inner+1]
                        
            return matrix, identity_matrix

        det = self.det()
        if det != 0.0:
            tmp_matrix = [Matrix(vector) for vector in self.matrix]
            identity_matrix = [Matrix([1.0 if inner == outer else 0.0 for inner in range(len(tmp_matrix))]) for outer in range(len(tmp_matrix))]
            idmatrix_cp = identity_matrix[:]

            #formatting the matrices to make the value of the diagonal line not a 0
            for diag in range(len(tmp_matrix)):
                if tmp_matrix[diag].matrix[diag] == 0.0:
                    tmp_copy = tmp_matrix[:]
                    for i in range(len(tmp_matrix)-1):
                        if 0.0 not in tmp_matrix[i].matrix[:diag+1]:
                            tmp_matrix[diag] = tmp_copy[i]
                            tmp_matrix[i] = tmp_copy[diag]
                            identity_matrix[diag] = idmatrix_cp[i]
                            identity_matrix[i] = idmatrix_cp[diag]

            tmp_matrix, identity_matrix = GaussJordanElimination(tmp_matrix, identity_matrix)

            tmp_matrix = Matrix([vector.matrix for vector in tmp_matrix])
            identity_matrix = Matrix([vector.matrix for vector in identity_matrix])
            idmatrix_cp = Matrix([vector.matrix for vector in idmatrix_cp])
            
            if tmp_matrix.matrix == idmatrix_cp.matrix:
                print('Successfully inverted matrix!')
                return identity_matrix

            else:
                print('Failed to invert matrix') 

        else:
            print('This matrix does not have an inverse matrix.')
