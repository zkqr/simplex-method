from help_functions import *
class SimplexMethod:
    def __init__(self, A, b, c):
        self.A = A
        self.b = b
        self.c = c
        self.d = []
        self.basic_vars = []
        self.non_basic_vars = []
        self.simplex_table = []
        self.m = len(b)
        self.n = len(c)

        if len(self.A) != len(self.b):
            raise ValueError("А и b должны быть одинакового размера")

        for i in self.b:
            if i < 0:
                raise ValueError("Все коэффициенты должны быть больше 0")

    def delta_calculation(self):
        basic = []
        for i in self.basic_vars:
            basic.append(self.c[i])

        for i in range(len(self.basic_vars) + len(self.non_basic_vars) + 1):
            if i == 0:
                self.d.append(dot(basic, get_col(self.simplex_table, i)))
            else:
                self.d.append(dot(basic, get_col(self.simplex_table, i)) - self.c[i - 1])
    def simplex_recalculation(self, lead_element_row, lead_element_col):

        lead_element_element = self.simplex_table[lead_element_row][lead_element_col]
        self.simplex_table[lead_element_row] = [element / lead_element_element
                                                for element in self.simplex_table[lead_element_row]]

        for i in range(len(self.simplex_table)):
            if i != lead_element_row:
                multiplier = self.simplex_table[i][lead_element_col]
                self.simplex_table[i] = [self.simplex_table[i][j] - multiplier * self.simplex_table[lead_element_row][j]
                                         for j in range(len(self.simplex_table[i]))]

        self.basic_vars[lead_element_row] = lead_element_col - 1
        self.non_basic_vars[lead_element_col - 1] = lead_element_row

        self.d = []
        self.delta_calculation()

    def add_basis(self):
        self.c += [0] * len(self.A)
        self.A = [row + [0] * i + [1] + [0] * (len(self.b) - i - 1) for i, row in enumerate(self.A)]

    def init_simplex_table(self):
        self.non_basic_vars = list(range(self.n))
        self.basic_vars = list(range(self.n, self.n + self.m))

        self.simplex_table = self.A

        for i, j in enumerate(self.simplex_table):
            j.insert(0, (self.b[i]))

    def simplex_calculation(self):
        self.delta_calculation()

        while any(delta > 0 for delta in self.d[1:]):
            lead_element_col = self.d[1:].index(max(delta for delta in self.d[1:])) + 1
            lead_element_row = min([i for i in range(self.m) if self.simplex_table[i][lead_element_col] > 0],
                                   key=lambda i: self.simplex_table[i][0] / self.simplex_table[i][lead_element_col])

            self.simplex_recalculation(lead_element_row, lead_element_col)

    def ouput_result(self):
        print("Y(X^*) =", round(self.d[0], 2))

        if 0 in self.basic_vars:
            print("X1 =", round(get_col(self.simplex_table, 0)[self.basic_vars.index(0)], 2))
        else:
            print("X1 = 0")

        if 1 in self.basic_vars:
            print("X2 =", round(get_col(self.simplex_table, 0)[self.basic_vars.index(1)], 2) )
        else:
            print("X2 = 0")

    def solve(self):
        self.add_basis()
        self.init_simplex_table()
        self.simplex_calculation()
        self.ouput_result()

