from Settings import bcolors, logging, merge_tuples
from tabulate import tabulate

#Proceso de agrupamiento y comprobación
class Cluster:
    def __init__(self, container, size, input_list):
        self.container = container
        self.firstimp = {}
        self.size = size
        self.answer = {}
        self.answerT = {}
        self.input_list = input_list

    def print(self):

        until = len(self.container)

        for i in range(until):

            multiplier = 0
            for key, value in self.container[i].items():

                multiplier = 3
                if not isinstance(key, int):
                    multiplier = 3 * len(merge_tuples(key))

                print(f"{bcolors.OKBLUE}{merge_tuples(key)}{bcolors.ENDC} {value}")

            if len(self.container[i].values()) != 0:
                print("-" * (multiplier), sep="--", end='')
                print("-" * (3 * self.size), sep="---")

    # Proceso de agrupamiento
    def Join(self):
        newGroup = {}
        couples = 0
        for k in range(self.size):
            newGroup[k] = {}

        for i in range(self.size):

            for key, value in self.container[i].items():

                # Evitar que siga iterando cuando es el último elemento para que no compare el último elemento con el último +1
                if i != self.size - 1:
                    for keyN, valueN in self.container[i + 1].items():

                        vars = len(valueN)
                        position = -1
                        tolerance = 0
                        # Almacenamos una copia de la fila para posteriormente colocarle el - y almacenarla en un nuevo diccionario
                        result = value.copy()
                        for x in range(vars):
                            if value[x] != valueN[x]:
                                position = x
                                tolerance += 1

                        else:
                            if tolerance == 1:
                                result[position] = '-'
                                if logging:
                                    print(f"Se pueden formar las parejas {key} y {keyN}")
                                newKey = key, keyN
                                newGroup[i][newKey] = result
                                couples += 1

        empty = 0
        for i in range(len(newGroup)):
            if len(newGroup[i].values()) == 0:
                empty += 1

        if empty < len(newGroup):

            # los que nunca se relacionaron con ninguno, 'primeros implicantes'
            for mainKey in self.container.values():

                # Added, remove if problems detected
                if len(mainKey) < 0:
                    continue

                for keys, values in mainKey.items():
                    found = 0
                    aux = 0
                    for i in range(self.size):

                        for newKeys in newGroup[i].keys():
                            # print(f"Buscando {keys} en {newKeys}")

                            if keys in newKeys:
                                # print(f"{bcolors.WARNING}{keys} fue encontrado!! Dejar de buscar{bcolors.ENDC}")
                                found = 1
                                aux = 1
                                break

                        if found == 1:
                            break
                    # Si entra a este else, no fue encontrado
                    else:
                        print(f"{bcolors.FAIL}{keys} marcado como primer implicante{bcolors.ENDC}")
                        self.firstimp[keys] = values

                    if found == 1:
                        continue

        if couples == 0:
            return 1
        else:
            self.container = newGroup
            self.print()
            return 0

    # Eliminar los elementos repetidos
    def purge(self):
        newGroup = {}

        if logging == 1:
            print(f"{bcolors.OKBLUE}Eliminar elementos repetidos:")
        for i in range(len(self.container)):
            if (len(self.container[i])):
                repeatedKey = []
                repeatedValue = []
                for key, value in self.container[i].items():
                    if len(repeatedValue) == 0:
                        repeatedValue = value.copy()
                        repeatedKey = list(key)
                    elif repeatedValue == value:
                        if logging == 1:
                            print(f"{bcolors.FAIL} {key} {value} es igual a {repeatedKey} {repeatedValue}{bcolors.ENDC}")
                        repeatedValue = []
                        continue
                    newGroup[key] = value
        del self.container
        self.container = newGroup

        self.Purge2()

    def Purge2(self):

        if logging == 1:
            print(f"{bcolors.OKBLUE}Eliminar elementos repetidos 2.0:")

        end = 0
        while end == 0:
            newGroup = {}

            repeatedKey = []
            repeatedValue = []
            for key, value in self.container.items():
                if len(repeatedValue) == 0:
                    repeatedValue = value.copy()
                    repeatedKey = list(key)
                elif repeatedValue == value:
                    if logging == 1:
                        print(f"{bcolors.FAIL} {key} {value} es igual a {repeatedKey} {repeatedValue}{bcolors.ENDC}")
                    repeatedValue = []
                    continue
                newGroup[key] = value

            if self.container == newGroup:
                end = 1
            del self.container
            self.container = newGroup

        print(f"{bcolors.OKGREEN}Elementos duplicados eliminados.{bcolors.ENDC}")

    # Añadimos al diccionario los primeros implicantes
    def firstImplicants(self):
        self.container = {**self.container, **self.firstimp}

    # Mostrar la respuesta bonita
    def getAnswer(self):
        response = {}
        # answer = ""
        for key, value in self.container.items():

            letter = 0
            answer = ""
            for i in value:

                if i == 1:
                    answer += chr(65 + letter)
                elif i == 0:
                    answer += chr(65 + letter) + "'"

                letter += 1

            response[answer] = {}

            tupla = merge_tuples(key)
            #Armamos la tabla
            for one in self.input_list:
                #Workaround 'object is not iterable'
                if isinstance(tupla, int):
                    if int(one) == tupla:
                        response[answer][one] = 'x'
                    else:
                        if one not in response[answer]:
                            response[answer][one] = ' '
                else:
                    for k in tupla:

                        if int(one) == k:
                            response[answer][one] = 'x'
                        else:
                            if one not in response[answer]:
                                response[answer][one] = ' '

            answer += ' + '

        arr = ""
        for x in response:
            arr += x + " + "
        self.answer = response
        self.transposed()
        return arr[0: len(arr) - 3]

    #Generar la traspuesta de la tabla que se utilizará en check
    def transposed(self):
        responseT = {}

        for one in self.input_list:
            responseT[one] = {}

            for key, value in self.answer.items():
                responseT[one][key] = self.answer[key][one]

        self.answerT = responseT

    # Inicio comprobación
    def check(self):

        self.check_print('N')
        #self.check_print('T')

        first_implicants = []
        neighbors = []
        contenido = []
        # Recorrer primero columnas luego filas
        for key, value in self.answerT.items():
            current_implicant = ''
            hola = []
            # key = numero de la fila, ejemplo: 0, 5, 6 ... (No uno seguido de otro necesariamente)

            # Elementos de cada columna
            # columnaNombre = nombre de la columna, ejemplo: A'BD
            # dato = X o espacio en blanco
            for columnaNombre, dato in value.items():
                if (dato == 'x'):
                    if (current_implicant == ''):
                        current_implicant = columnaNombre
                    else:
                        current_implicant = '0'
                    hola.append(columnaNombre)
            # print(f"[{key}][{columnaNombre}]: '{dato}'")
            # Ambos son lo mismo, la unica diferencia es el for externo, que uno itera en la 'matriz' normal, el otro en la traspuesta
            # Pero el funcionamiento sería el mismo
            if (current_implicant != '0' and first_implicants.count(current_implicant) < 1):
                first_implicants.append(current_implicant)
            else:
                neighbors.append(hola)
        if (len(first_implicants) == 0):
            no_implicantes = []
            for key, value in self.answer.items():
                cnumx = 0
                numx = []
                for columnaNombre, dato in value.items():
                    if (dato == 'x' and contenido.count(columnaNombre) != 1):
                        cnumx += 1
                        numx.append(columnaNombre)
                if (first_implicants.count(key) == 0):
                    no_implicantes.append((key, cnumx, numx))
            while (len(self.input_list) != len(contenido)):
                key = ''
                numx = []
                hay_mayor = False
                for i in range(len(no_implicantes) - 1):
                    if (no_implicantes[i][1] > no_implicantes[i + 1][1]):
                        hay_mayor = True
                        key = no_implicantes[i][0]
                        numx = no_implicantes[i][2]
                if (hay_mayor):
                    first_implicants.append(key)
                    contenido.append(numx)
                else:
                    for i in range(len(no_implicantes)):
                        habilitado = True
                        for j in range(len(no_implicantes[i][2])):
                            if (contenido.count(no_implicantes[i][2][j]) != 0):
                                habilitado = False

                        if (habilitado):
                            first_implicants.append(no_implicantes[i][0])
                            for k in range(len(no_implicantes[i][2])):
                                contenido.append(no_implicantes[i][2][k])
        elif (len(self.answer) != len(first_implicants)):
            neighbors_implicants = []
            for implicant in first_implicants:
                for i in range(len(neighbors)):
                    if (neighbors[i].count(implicant) != 0):
                        for j in range(len(neighbors[i])):
                            if (neighbors[i][j] != implicant):
                                neighbors_implicants.append(neighbors[i][j])
            for implicant in first_implicants:
                k = 0
                while (k < (len(neighbors_implicants))):
                    if (neighbors_implicants[k] == implicant):
                        neighbors_implicants.remove(neighbors_implicants[k])
                    else:
                        k = k + 1
            no_implicantes = []
            for key, value in self.answer.items():
                cnumx = 0
                numx = []
                for columnaNombre, dato in value.items():
                    if (first_implicants.count(key) != 0):
                        if (contenido.count(columnaNombre) < 1 and dato == 'x'):
                            contenido.append(columnaNombre)
                    else:
                        if (dato == 'x' and contenido.count(columnaNombre) != 1):
                            cnumx += 1
                            numx.append(columnaNombre)
                if (first_implicants.count(key) == 0 and neighbors_implicants.count(key) == 0):
                    no_implicantes.append((key, cnumx, numx))
            # print(len(input_list),len(contenido))
            while (len(self.input_list) != len(contenido)):
                key = ''
                numx = []
                hay_mayor = False
                for i in range(len(no_implicantes) - 1):
                    if (no_implicantes[i][1] > no_implicantes[i + 1][1]):
                        hay_mayor = True
                        key = no_implicantes[i][0]
                        numx = no_implicantes[i][2]
                if (hay_mayor):
                    first_implicants.append(key)
                    contenido.append(numx)
                else:
                    for i in range(len(no_implicantes)):
                        habilitado = True
                        for j in range(len(no_implicantes[i][2])):
                            if (contenido.count(no_implicantes[i][2][j]) != 0):
                                habilitado = False

                        if (habilitado):
                            first_implicants.append(no_implicantes[i][0])
                            for k in range(len(no_implicantes[i][2])):
                                contenido.append(no_implicantes[i][2][k])

        #Imprimir respuesta
        print(f"{bcolors.OKGREEN}{bcolors.BOLD}Z = ", end = "")
        final = ""
        for x in first_implicants:
            final = final + x + " + "

        print(f"{final[0:len(final)-3]}{bcolors.ENDC}")



    def check_print(self, type):
        headers = ['/']
        table = []
        # imprimir original
        if type != 'T':

            for x in self.input_list:
                headers.append(x)

            for key, value in self.answer.items():
                row = [key]

                for x in value.values():
                    row.append(x)

                table.append(row)


        # imprimir la traspuesta
        else:
            for x in self.answer.keys():
                headers.append(x)

            for key, value in self.answerT.items():
                row = [key]
                for x in value.values():
                    row.append(x)

                table.append(row)

        print(tabulate(table, headers, tablefmt="fancy_grid", stralign='center'))