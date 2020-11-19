from Settings import bcolors

#Generar la tabla de valores
class Table:
    def __init__(self, size, z):
        self.size = size
        self.table = {}

        global fillColumn
        for i in range(self.size):
            fillColumn = [0] * pow(2, self.size)
            self.table[chr(65 + i)] = fillColumn

        fillColumn = [0] * pow(2, self.size)
        self.table['Z'] = fillColumn

        currentcol = self.size
        for i in range(self.size):
            k = 0
            number = 1
            for x in self.getColumn(chr(65 + i)):
                if k % (pow(2, currentcol) / 2) == 0:
                    if (number == 0):
                        number = 1
                    else:
                        number = 0

                self.table[chr(65 + i)][k] = number
                k += 1
            currentcol -= 1
        for o in range(pow(2, self.size)):
            try:
                valid = z.index(str(o))
            except ValueError:
                valid = -1

            if valid >= 0:
                self.table['Z'][o] = 1

    def print(self):
        print('-' * 7, end='')
        print('-' * (4 * (self.size + 1)))
        print("|", bcolors.WARNING, "#", bcolors.ENDC, end=" |")
        for column in self.table.keys():
            if column == chr(65 + self.size - 1):
                print(bcolors.HEADER, column, bcolors.FAIL, end="|")
            else:
                print(bcolors.HEADER, column, bcolors.ENDC, end="|")
        else:
            print("")
            print('-' * 7, end='')
            print('-' * (4 * (self.size + 1)))

        rowid = 0
        for i in range(pow(2, self.size)):
            # print("| %3d" % rowid, end = " | ")
            print(f"|{bcolors.OKGREEN} {rowid: <3}{bcolors.ENDC}".format('ddd'), end=" |")

            rowsize = self.getRowSize(i)
            kstep = 0
            for k in self.getRow(i):
                if k == 1 and rowsize - 1 == kstep:
                    print(bcolors.OKBLUE, k, bcolors.ENDC, end="|")
                elif rowsize - 2 == kstep:
                    print(bcolors.ENDC, k, bcolors.FAIL, end="|")
                else:
                    print(bcolors.ENDC, k, end=" |")

                kstep += 1

            else:
                print("")
                print('-' * 7, end='')
                print('-' * (4 * (self.size + 1)))
            rowid += 1

    def getRow(self, rowNumber):
        row = []
        for i in self.table.values():
            k = 0
            for j in i:
                if k == rowNumber: row.append(j)
                k += 1
        return row

    # Devuelve la fila introducida sin la columna z
    def getRowC(self, rowNumber):
        row = self.getRow(rowNumber)
        return row[0:self.size]

    def getColumn(self, columnLetter):
        return self.table[columnLetter]

    def getRowSize(self, rowNumber):
        return len(self.getRow(rowNumber))
