import ast
import sys
from argparse import ArgumentParser


def read_files(input_file, description_file):
    try:
        samples = []
        with open(input_file, 'r') as rf:
            for line in rf:
                tmp = line.replace('\n', '').split('->')
                io = [nrn[1:-1].split(' ') for nrn in tmp]
                samples.append(io)
            for x in range(len(samples)):
                for y in range(len(samples[x])):
                    for z in range(len(samples[x][y])):
                        samples[x][y][z] = float(''.join(samples[x][y][z]))

        with open(description_file, 'r') as rf:
            nrns = ast.literal_eval(rf.read())

        return samples, nrns
    except:
        print(f'Ошибка чтения файла')
        exit()


class Training:
    def __init__(self, parameters, neurons, samples):
        self.params = parameters
        self.nrns = neurons
        self.samples = samples
        self.funs = []
        self.weights = []
        for i in range(len(neurons)):
            self.funs.append([])
            self.weights.append([])

    def activation(self, x):
        return x / (1 + abs(x))

    def derivative(self, x):
        return 1 / pow((1 + abs(x)), 2)

    def perceptron(self, input):
        ans = input.copy()

        for j in range(len(self.nrns)):
            n = len(ans)
            for k in range(len(self.nrns[j])):
                if n != len(self.nrns[j][k]):
                    print(f'Ошибка - число нейронов не совпадает с длиной массива весов')
                    exit()
                total = sum([ans[i] * self.nrns[j][k][i] for i in range(len(self.nrns[j][k]))])
                self.weights[j].append(total)
                total = self.activation(total)
                self.funs[j].append(total)
                ans.append(total)
            if n > 0:
                ans[:n] = []
        return ans

    def education(self, output):
        n, eps = self.params[0], self.params[1]
        ans_lines = [[] for _ in range(len(self.samples))]

        for sample in range(len(self.samples)):
            for count in range(n):
                input, exp = self.samples[sample][0], self.samples[sample][1]
                perc = self.perceptron(input)

                if not count % 100:
                    ans_lines[sample].append(f'{count // 100 + 1 + sample * n // 100}: {exp[0] - perc[0]}\n')

                sgm = [[] for x in range(len(self.nrns))]
                for i in range(len(perc)):
                    sgm[len(self.nrns) - 1] = [exp[i] - perc[i]]

                for i in range(len(self.nrns) - 1, 0, -1):
                    for j in range(len(self.nrns[i][i - 1])):
                        total = sum([abs(sgm[i][x]) * self.nrns[i][x][j] for x in range(len(sgm[i]))])
                        sgm[i - 1].append([total])

                for i in range(len(self.nrns[0])):
                    for w in range(len(self.nrns[0][i])):
                        dw = sgm[0][i] * self.derivative(self.weights[0][i]) * self.samples[sample][0][w] * eps
                        self.nrns[0][i][w] = self.nrns[0][i][w] + dw

                for i in range(1, len(self.nrns)):
                    for j in range(len(self.nrns[i])):
                        for w in range(len(self.nrns[i][j])):
                            dw = sgm[i][j] * self.derivative(self.weights[i][j]) * self.funs[i - 1][w] * eps
                            self.nrns[i][j][w] = self.nrns[i][j][w] + dw

        with open(output, 'w') as file:
            for line in ans_lines:
                for x in line:
                    file.write(x)


def main():
    parser = ArgumentParser()
    parser.add_argument('-i', required=1, help='Имя входного файла')
    parser.add_argument('-d', required=1, help='Имя файла с начальным вектором')
    parser.add_argument('-o', required=1, help='Имя выходного файла')
    parser.add_argument('-n', required=1, help='Число эпох')
    parser.add_argument('-e', required=1, help='Скорость обучения')
    args = parser.parse_args()

    samples, neurons = read_files(args.i, args.d)
    n, e = int(args.n), float(args.e)
    Training([n, e], neurons, samples).education(args.o)


if __name__ == '__main__':
    main()
