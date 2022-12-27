import argparse
import xml.etree.cElementTree as ET
from xml.dom import minidom


def read_graph(input_file):
    with open(input_file, 'r') as input_graph:
        all_edges = {}
        file = input_graph.read().replace(' ', '').split('\n')
        for j in range(len(file)):
            if '-' in file[j]:
                print(f'Ошибка в строке {j + 1}')
                exit()
            for i in file[j]:
                if i.isalpha():
                    print(f'Ошибка в строке {j + 1}')
                    exit()
        edges = ''.join(file).split('),(')
        if int(edges[0][1]) > int(edges[0][3]):
            max_vertex = int(edges[0][1])
        else:
            max_vertex = int(edges[0][3])
        for i in range(1, len(edges)):
            if max_vertex < int(edges[i][0]):
                max_vertex = int(edges[i][0])
            if max_vertex < int(edges[i][2]):
                max_vertex = int(edges[i][2])
        in_number = [""] * max_vertex
        for i in range(len(edges)):
            if i == 0:
                edges[i] = edges[i][1:]
            if i == len(edges) - 1:
                if edges[i][len(edges[i]) - 1] == '\n':
                    edges[i] = edges[i][:len(edges[i]) - 2]
                else:
                    edges[i] = edges[i][:-1]
            try:
                edge = eval(edges[i])
                if len(edge) != 3:
                    edge = str(edge).replace(" ", '')
                    for j in range(len(file)):
                        if edge in file[j]:
                            print(f'Ошибка в строке {j + 1}')
                            exit()
            except:
                edge = str(edge).replace(" ", '')
                for j in range(len(file)):
                    if edge in file[j]:
                        print(f'Ошибка в строке {j + 1}')
                        exit()
            if edge[0] not in all_edges:
                all_edges[edge[0]] = []
            if edge[1] not in all_edges:
                all_edges[edge[1]] = []
            in_number[edge[1] - 1] = in_number[edge[1] - 1] + " " + str(edge[2])
            all_edges[edge[0]].append([edge[2], edge[1]])
    y = []
    for x in in_number:
        y.append(x.split(" "))
    for i in range(len(y)):
        num = []
        for j in range(1, len(y[i])):
            num.append(int(y[i][j]))
        num.sort()
        if len(num) == 1 and num[0] != 1:
            print('Ошибка в строке ' + str(len(file)) + ' - неправильная нумерация')
            exit()
        for j in range(0, len(num) - 1):
            if num[j] == num[j + 1]:
                print('Ошибка в строке ' + str(len(file)) + ' - неправильная нумерация')
                exit()
            if num[j + 1] - num[j] != 1:
                print('Ошибка в строке ' + str(len(file)) + ' - неправильная нумерация')
                exit()
    return all_edges


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', required=True, help='Имя входного файла')
    parser.add_argument('-o', required=True, help='Имя выходного файла')
    args = parser.parse_args()
    all_edges = read_graph(args.i)
    root = ET.Element("graph")
    for x in range(len(all_edges)):
        ET.SubElement(root, "vertex").text = 'v' + str(x + 1)
    for x in range(1, len(all_edges)):
        for z in range(len(all_edges[x])):
            arc = ET.SubElement(root, "arc")
            From = ET.SubElement(arc, 'from').text = 'v' + str(x)
            To = ET.SubElement(arc, 'to').text = 'v' + str(all_edges[x][z][1])
            Order = ET.SubElement(arc, 'order').text = str(all_edges[x][z][0])
    dom = minidom.parseString(ET.tostring(root))
    tree = dom.toprettyxml(indent='\t')
    with open(args.o, 'w') as file:
        file.write(tree)


if __name__ == '__main__':
    main()
