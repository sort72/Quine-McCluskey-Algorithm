#Clase encargada de agrupar según la cantidad de unos
class Group:
    def __init__(self, grouptable, type=0):
        if type == 0:
            self.table = grouptable
            self.container = {}
            self.size = self.table.size

            for k in range(self.size + 1):
                self.container[k] = {}

        else:
            self.container = grouptable
            self.size = type

    def make(self):
        for i in range(pow(2, self.size)):
            if self.table.getRow(i)[self.size] == 1:

                pivots = 0
                for x in self.table.getRowC(i):
                    if x == 1:
                        pivots += 1
                else:
                    self.container[pivots][i] = self.table.getRowC(i)