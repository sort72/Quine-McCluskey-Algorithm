class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Inputs:
    def __init__(self, input_size, input_lit):
        self.input_size = input_size
        self.input_list = input_lit

        fIn = "f("
        for i in range(self.input_size):
            fIn = fIn + chr(65 + i) + ", "

        fIn = fIn[0:len(fIn)-2]
        fIn = fIn + ") = Sm("

        for x in self.input_list:
            fIn = fIn + x + ", "

        fIn = fIn[0:len(fIn) - 2] + ")"

        print("-" * 150)
        print(f"{bcolors.WARNING}{bcolors.BOLD}Método de minimización de Quine-McCluskey{bcolors.ENDC}")
        print(f"\n{bcolors.OKBLUE}Realizado por:\nAlejandro Ortega\nNicole Rios")

        print(f"\n{bcolors.HEADER}{fIn}{bcolors.ENDC}\n\n")


    #Validar que los datos introducidos sean validos para su utilización
    def validate(self):
        valid = 1
        if self.input_size < 4 or self.input_size > 8:
            print(f"{bcolors.WARNING}ERROR: {bcolors.FAIL}Debe introducir mínimo 4 entradas, máximo 8.")
            valid = 0
        elif len(self.input_list) > pow(2, self.input_size):
            print(
                f"{bcolors.WARNING}ERROR: {bcolors.FAIL}Está utilizando algún valor fuera de las posibles soluciones (> 2^n).")
            valid = 0
        else:
            for i in self.input_list:
                if i.isnumeric() == 0 or int(i) < 0 or int(i) > pow(2, self.input_size) - 1:
                    print(
                        f"{bcolors.WARNING}ERROR: {bcolors.FAIL}Está utilizando algún valor erróneo en la función solución.")
                    valid = 0
                    break

        return valid


# https://stackoverflow.com/questions/14745199/how-to-merge-two-tuples-in-python/14745275#14745275
def merge_tuples(t):
    if isinstance(t, int): return t
    fin = t
    stop = ()
    while fin != stop:
        stop = fin
        fin = tuple(j for i in (fin) for j in (i if isinstance(i, tuple) else (i,)))
    return fin

logging = 0