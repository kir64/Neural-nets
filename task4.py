from re import sub
from xml.dom import minidom
from argparse import ArgumentParser
import xml.etree.cElementTree as ET


def read_files(textfile, input):
    mtx, idx = [], 0
    with open(textfile, 'r') as rf:
        v = [int(x) for x in rf.read().split(' ')]
    with open(input, 'r') as rf:
        txt = rf.readlines()

    for line in txt:
        idx += 1
        line = sub(r'[\[\]]', ' ', line)[1:-2].split('   ')
        tmp = []
        for x in line:
            x = x.split(' ')
            try:
                tmp.append([int(i) for i in x])
            except ValueError:
                print(f'Ошибка в строке {idx}')
                exit()
            if len(x) != len(v):
                print(f'Ошибка числа компонент нейронов в слоях {idx - 1} - {idx}')
                exit()
        mtx.append([tmp])

    return mtx, v


def evaluate(mtx, v):
    ans = []
    for layer in mtx:
        tmp = []
        for x in layer:
            for neuron in x:
                val = sum([neuron[i] * v[i] for i in range(len(v))])
                val /= (1 + abs(val))
                tmp.append(val)
            ans.append(tmp)
            v = tmp
    return ans


def main():
    parser = ArgumentParser()
    parser.add_argument('-m', required=True, help='Имя входного файла')
    parser.add_argument('-i', required=True, help='Имя файла с начальным вектором')
    parser.add_argument('-o', required=True, help='Имя выходного файла')
    args = parser.parse_args()

    mtx, v = read_files(args.i, args.m)
    new_mtx = evaluate(mtx, v)

    with open(args.o, 'w') as output:
        for x in new_mtx[-1]:
            output.write(str(x) + ' ')

    root = ET.Element('network')
    for layer in mtx:
        tmp = ''
        for x in layer:
            for y in x:
                tmp += f'{y} '
            break
        ET.SubElement(root, 'layer').text = tmp[:-1]

    ans = minidom.parseString(ET.tostring(root)).toprettyxml(indent='\t')
    with open('output.xml', 'w') as file:
        file.write(ans)


if __name__ == '__main__':
    main()
