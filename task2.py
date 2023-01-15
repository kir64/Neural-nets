import argparse


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


def dfs_check(v, graph):
    global ans
    is_any, is_first = False, True
    for vertex in graph[v]:
        if not is_first:
            ans += ', '
        is_any = True
        if is_first:
            ans += str(v) + '('
            is_first = False
        dfs_check(vertex[1], graph)
    if is_any:
        ans += ')'
    elif is_first:
        ans += str(v)
    return ans


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
    v_lst = [v for v in d if d[v][1] == 0]
    for v in v_lst:
        cycle(v, graph, {}, {})


def check_cycle2(graph, d):
    v_lst = [v for v in d if d[v][1] == 0]
    if not v_lst:
        print(f'Ошибка - цикл между вершинами 1 и {len(d)}')
        exit()
    global ans
    ans = ''
    for v in range(len(v_lst)):
        ans = dfs_check(v_lst[v], graph)
        if v != len(v_lst) - 1:
            ans += ', '
    return ans


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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', required=True, help='Имя входного файла')
    parser.add_argument('-o', required=True, help='Имя выходного файла')
    args = parser.parse_args()
    edges_lst, lst = read_graph(args.i)
    check_cycle(edges_lst, lst)

    for i in range(1, len(lst) + 1):
        lst[i][0], lst[i][1] = lst[i][1], lst[i][0]
    rev_graph = reverse_graph(edges_lst)
    graph = [[]] * (len(edges_lst) + 1)
    i = 0
    for x in sorted(rev_graph.keys()):
        tmp = [[rev_graph[x][i]] for i in range(len(rev_graph[x]))]
        graph[i + 1] = tmp
        i += 1

    ans = []
    for i in graph:
        tmp = [[i[j][0][0], i[j][0][1]] for j in range(len(i))]
        tmp.sort(key=lambda x: x[0])
        ans.append(tmp)

    with open(args.o, 'w') as file:
        file.write(check_cycle2(ans, lst))


if __name__ == '__main__':
    main()
