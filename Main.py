from Settings import bcolors, Inputs
from Table import Table
from Group import Group
from Cluster import Cluster

# input_size = int(input(f"{bcolors.OKGREEN}Ingrese la cantidad de entradas: "))
# input_function = input(f"{bcolors.OKGREEN}Ingrese los valores donde la salida es 1 separados por espacio {bcolors.FAIL}(En formato decimal): ")
# input_list = input_function.split()

#input_size = 4
#input_list = ['0', '5', '6', '7', '8', '10', '11', '12', '14', '15']

#input_size = 5
#input_list = ['0', '1', '2', '3', '6', '8', '9', '10', '11', '17', '20', '21', '23', '25', '28', '30', '31']

#input_size = 6
#input_list = ['0', '3', '6', '25', '26', '27', '30', '54', '55', '56', '57', '63']

#input_size = 8
#input_list = ['0', '1',  '6', '8', '21', '23','25', '49', '51', '52', '56', '58', '60', '70', '150', '240']
#input_list = ['0', '1', '2', '6', '8', '21', '23','25', '27', '49', '51', '52', '56', '58', '59','60','72','73','74','75', '77','78','96','97','98','99','100','103','128','129','130','131','225','226','227','228','235','237','239','243','246','249','254','255']

#Examples
input_size = 4
#input_list = ['0','5','6','7','8','10','11','12','14','15']
input_list = ['0', '4', '5', '7', '8', '11', '12', '15']

#input_size = 5
#input_list = ['0', '1', '2', '3', '6', '8', '9', '10', '11', '17', '20', '21', '23', '25', '28', '30', '31']

#input_size = 8
#input_list = ['0', '1', '3', '4', '7', '8', '15', '16', '22', '23', '31', '32', '63', '64', '127', '128']


result = Inputs(input_size, input_list).validate()
if result == 1:
    print(f"{bcolors.OKBLUE}Listado:{bcolors.ENDC}")
    table = Table(input_size, input_list)
    table.print()
    print(f"{bcolors.OKBLUE}\nAgrupación:{bcolors.ENDC}")

    group = Group(table)
    group.make()

    cluster = Cluster(group.container, input_size + 1, input_list)
    cluster.print()
    print(f"{bcolors.OKBLUE}\nProceso de agrupamiento:{bcolors.ENDC}")

    finish = 0
    while finish == 0:
        finish = cluster.Join()
        if finish != 1:
            print(f"{bcolors.OKGREEN}\n----------------------{bcolors.ENDC}")

    cluster.purge()
    cluster.firstImplicants()

    print(f"{bcolors.OKGREEN}{bcolors.BOLD}Z = {cluster.getAnswer()}")

    print(f"{bcolors.WARNING}\nComprobación:{bcolors.ENDC}")

    cluster.check()

    print("-" * 150)

