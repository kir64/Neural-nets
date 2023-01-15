from argparse import ArgumentParser
from math import exp


def read_graph(input_file):
    with open(input_file, 'r') as graph:
        edges_lst, lst = {}, {}
        file = graph.read().replace(' ', '').split('\n')
        for i in range(len(file)):
            if '-' in file[i]:
                print(f'Ошибка в строке {i + 1}')
                exit()
            for j in file[i]:
                if j.isalpha():
                    print(f'Ошибка в строке {i + 1}')
                    exit()

        edges = ''.join(file).split('),(')
        max_v = int(edges[0][1]) if int(edges[0][1]) > int(edges[0][3]) else int(edges[0][3])
        for i in range(1, len(edges)):
            if max_v < int(edges[i][0]):
                max_v = int(edges[i][0])
            elif max_v < int(edges[i][2]):
                max_v = int(edges[i][2])

        tmp = [''] * max_v
        for i in range(len(edges)):
            if i == 0:
                edges[i] = edges[i][1:]
            elif i == len(edges) - 1:
                edges[i] = edges[i][:len(edges[i]) - 2] if edges[i][len(edges[i]) - 1] == '\n' else edges[i][:-1]

            try:
                edge = eval(edges[i])
                if len(edge) != 3:
                    edge = str(edge).replace(' ', '')
                    for j in range(len(file)):
                        if edge in file[j]:
                            print(f'Ошибка в строке {j + 1}')
                            exit()
            except:
                edge = str(edge).replace(' ', '')
                for j in range(len(file)):
                    if edge in file[j]:
                        print(f'Ошибка в строке {j + 1}')
                        exit()

            if edge[0] not in edges_lst:
                edges_lst[edge[0]] = []
                lst[edge[0]] = [1, 0]
            else:
                lst[edge[0]][0] += 1
            if edge[1] not in edges_lst:
                edges_lst[edge[1]] = []
                lst[edge[1]] = [0, 1]
            else:
                lst[edge[1]][1] += 1

            tmp[edge[1] - 1] = tmp[edge[1] - 1] + ' ' + str(edge[2])
            edges_lst[edge[0]].append([edge[2], edge[1]])

    y = [x.split(' ') for x in tmp]
    for i in range(len(y)):
        num = [int(y[i][j]) for j in range(1, len(y[i]))]
        num.sort()
        if len(num) == 1 and num[0] != 1:
            print(f'Неправильная нумерация в строке {len(file)}')
            exit()
        for j in range(len(num) - 1):
            if num[j] == num[j + 1] or num[j + 1] - num[j] != 1:
                print(f'Неправильная нумерация в строке {len(file)}')
                exit()

    graph = {}
    for j in range(1, len(edges_lst) + 1):
        graph[j] = []
        for i in range(len(edges_lst[j])):
            graph[j].append([edges_lst[j][i][0], edges_lst[j][i][1]])

    return graph, lst


def dfs_check(x, graph):
    is_any, is_first = False, True
    global output, tmp

    for v in graph[x]:
        is_any = True
        if is_first:
            output += f'{x}('
            tmp += f'{x}('
            is_first = False
        else:
            output += ', '
            tmp += ', '
        dfs_check(v[1], graph)

    if is_any:
        output += ')'
        tmp += ')'
    else:
        if is_first:
            output += str(x)
            tmp += str(x)

    return output, tmp


def cycle(x, graph, used, tmp):
    used[x] = True
    dfs_graph = {x: []}

    for v in graph[x]:
        if v[1] not in used:
            dfs_graph[x].append(cycle(v[1], graph, used, tmp))
        else:
            if v[1] not in tmp:
                print(f'Ошибка - цикл между вершинами {x} и {v[1]}')
                exit()
            else:
                dfs_graph[x].append({v[1]: tmp[v[1]]})
    tmp[x] = dfs_graph[x]

    return dfs_graph


def check_cycle(graph, d):
    v_lst = [vertex for vertex in d if d[vertex][1] == 0]
    for v in v_lst:
        cycle(v, graph, {}, {})


def check_cycle2(graph, d):
    v_lst = [vertex for vertex in d if d[vertex][1] == 0]
    if not v_lst:
        print(f'Ошибка - цикл между вершинами 1 и {len(d)}')
        exit()

    global output, fun, tmp
    tmp, fun, output = '', [], '',

    for v in range(len(v_lst)):
        output, tmp = dfs_check(v_lst[v], graph)
        if v != len(v_lst) - 1:
            output += ', '
            fun.append(tmp)
            tmp = ''
        fun.append(tmp)

    return output, fun


def reverse_graph(graph):
    ans = {}
    for u in sorted(graph.keys()):
        for v in graph[u]:
            if u not in ans:
                ans[u] = []
            if v[1] not in ans:
                ans[v[1]] = []
            ans[v[1]].append([v[0], u])
    return ans


def read_operations(v_lst, file):
    ops, i = {}, 0
    op_lst = ['+', '*', 'exp']

    with open(file, 'r') as input_operations:
        for line in input_operations:
            line = line[:(len(line) - 1)].replace(' ', '')
            j = line.find(':')
            if j == -1:
                print(f'Ошибка операции, строка {i + 1}')
                exit()
            v = int(line[:j])
            if v not in v_lst:
                print(f'Ошибка вершины, строка {i + 1}')
                exit()

            op = str(line[(j + 1):])
            try:
                ops[str(v)] = int(op) if op not in op_lst else op
            except:
                print(f'Ошибка операции, строка {i + 1}')
                exit()
            i += 1
    return ops


def check_operations(graph, ops):
    for v in graph.keys():
        if type(ops[str(v)]) == int:
            if len(graph[v]) == 0:
                continue
            print(f'Ошибка операции - {ops[str(v)]}, вершина {v}')
            exit()
        elif ops[str(v)] == '+' or ops[str(v)] == '*':
            if len(graph[v]) > 1:
                continue
            print(f'Ошибка операции - {ops[str(v)]}, вершина {v}')
            exit()
        elif ops[str(v)] == 'exp':
            if len(graph[v]) == 1:
                continue
            print(f'Ошибка операции - {ops[str(v)]}, вершина {v}')
            exit()


def dfs_ops(x, graph, ops, used, vals):
    used[x] = True
    tmp = {x: -1}
    if type(ops[str(x)]) == int:
        tmp[x] = ops[str(x)]
    elif ops[str(x)] == '+':
        tmp[x] = 0
    elif ops[str(x)] == '*' or ops[str(x)] == 'exp':
        tmp[x] = 1

    if not len(graph[x]):
        vals[x] = tmp[x]
        return vals
    for v in graph[x]:
        if v[1] not in used:
            val = dfs_ops(v[1], graph, ops, used, vals)
            if ops[str(x)] == '+':
                tmp[x] += val[v[1]]
            elif ops[str(x)] == '*':
                tmp[x] *= val[v[1]]
            elif ops[str(x)] == 'exp':
                tmp[x] = exp(val[v[1]])
        else:
            if ops[str(x)] == '+':
                tmp[x] += vals[v[1]]
            elif ops[str(x)] == '*':
                tmp[x] *= vals[v[1]]
            elif ops[str(x)] == 'exp':
                tmp[x] = exp(vals[v[1]])
    vals[x] = tmp[x]
    return vals


def evaluating(graph, started_vertex, operations):
    used, vals = {}, {}
    for v in started_vertex:
        dfs_ops(v, graph, operations, used, vals)
    return vals


def main():
    parser = ArgumentParser()
    parser.add_argument('-i', required=True, help='Имя входного файла')
    parser.add_argument('-f', required=True, help='Имя файла с операциями')
    parser.add_argument('-o', required=True, help='Имя выходного файла')
    args = parser.parse_args()

    v_lst, lst = read_graph(args.i)
    start = []
    for x in v_lst:
        if not len(v_lst[x]):
            start.append(x)

    check_cycle(v_lst, lst)
    for x in range(1, len(lst) + 1):
        lst[x][0], lst[x][1] = lst[x][1], lst[x][0]

    rev_graph = reverse_graph(v_lst)
    graph = [[]] * (len(v_lst) + 1)

    k = 0
    for x in sorted(rev_graph.keys()):
        tmp = [[rev_graph[x][i]] for i in range(len(rev_graph[x]))]
        graph[k + 1] = tmp
        k += 1

    new_graph = []
    for i in graph:
        tmp = [[i[j][0][0], i[j][0][1]] for j in range(len(i))]
        tmp.sort(key=lambda x: x[0])
        new_graph.append(tmp)

    output, fun = check_cycle2(new_graph, lst)
    fun = [y for y in fun if y != '']
    ops = read_operations(v_lst, args.f)
    new_fun = []
    fun_string = ''

    for x in fun:
        for char in x:
            tmp = char
            if char.isdigit():
                tmp = ops[str(char)]
            fun_string += str(tmp)
        new_fun.append(fun_string)
        fun_string = ''

    check_operations(rev_graph, ops)

    vals = evaluating(rev_graph, start, ops)
    with open(args.o, 'w') as output:
        for i in range(len(start)):
            txt = [''.join(fun[i]), ''.join(new_fun[i]), str(vals[start[i]])]
            print(*txt, sep=' = ', file=output)


if __name__ == '__main__':
    main()
