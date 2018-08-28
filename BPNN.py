# Back-Propagation Neural Networks


import math
import random

import string
import csv
import sys

random.seed(0)

# calculate a random number where:  a <= rand < b
def rand(a, b):
    return (b-a)*random.random() + a

# Make a matrix (we could use NumPy to speed this up)
def makeMatrix(I, J, fill=0.0):
    m = []
    for i in range(I):
        m.append([fill]*J)
    return m

# our sigmoid function, tanh is somewhat better than the standard 1/(1+e^-x)
def sigmoid(x):
    return math.tanh(x)

# derivative of our sigmoid function, in terms of the output (i.e. y)
def dsigmoid(y):
    return 1.0 - y**2

class NN:
    def __init__(self, number_of_input, number_of_hidden, number_of_output):
        # number of input, hidden, and output nodes
        self.number_of_input = number_of_input + 1 # +1 for bias node
        self.number_of_hidden = number_of_hidden
        self.number_of_output = number_of_output

        # activations for nodes
        self.activation_input = [1.0]*self.number_of_input
        self.activation_hidden = [1.0]*self.number_of_hidden
        self.activation_output = [1.0]*self.number_of_output
        
        # create weights
        self.weight_input = makeMatrix(self.number_of_input, self.number_of_hidden)
        self.weight_output = makeMatrix(self.number_of_hidden, self.number_of_output)
        
        # set them to random vaules
        for i in range(self.number_of_input):
            for j in range(self.number_of_hidden):
                self.weight_input[i][j] = rand(-0.2, 0.2)
        for j in range(self.number_of_hidden):
            for k in range(self.number_of_output):
                self.weight_output[j][k] = rand(-2.0, 2.0)

        # last change in weights for momentum   
        self.ci = makeMatrix(self.number_of_input, self.number_of_hidden)
        self.co = makeMatrix(self.number_of_hidden, self.number_of_output)

    def update(self, inputs):
        if len(inputs) != self.number_of_input-1:
            raise ValueError('wrong number of inputs')

        # input activations
        for i in range(self.number_of_input-1):
            #self.activation_input[i] = sigmoid(inputs[i])
            self.activation_input[i] = inputs[i]

        # hidden activations
        for j in range(self.number_of_hidden):
            sum = 0.0
            for i in range(self.number_of_input):
                sum = sum + self.activation_input[i] * self.weight_input[i][j]
            self.activation_hidden[j] = sigmoid(sum)

        # output activations
        for k in range(self.number_of_output):
            sum = 0.0
            for j in range(self.number_of_hidden):
                sum = sum + self.activation_hidden[j] * self.weight_output[j][k]
            self.activation_output[k] = sigmoid(sum)

        return self.activation_output


    def backPropagate(self, targets, N, M):
        if len(targets) != self.number_of_output:
            raise ValueError('wrong number of target values')

        # calculate error terms for output
        output_deltas = [0.0] * self.number_of_output
        for k in range(self.number_of_output):
            error = targets[k]-self.activation_output[k]
            output_deltas[k] = dsigmoid(self.activation_output[k]) * error

        # calculate error terms for hidden
        hidden_deltas = [0.0] * self.number_of_hidden
        for j in range(self.number_of_hidden):
            error = 0.0
            for k in range(self.number_of_output):
                error = error + output_deltas[k]*self.weight_output[j][k]
            hidden_deltas[j] = dsigmoid(self.activation_hidden[j]) * error

        # update output weights
        for j in range(self.number_of_hidden):
            for k in range(self.number_of_output):
                change = output_deltas[k]*self.activation_hidden[j]
                self.weight_output[j][k] = self.weight_output[j][k] + N*change + M*self.co[j][k]
                self.co[j][k] = change
                #print N*change, M*self.co[j][k]

        # update input weights
        for i in range(self.number_of_input):
            for j in range(self.number_of_hidden):
                change = hidden_deltas[j]*self.activation_input[i]
                self.weight_input[i][j] = self.weight_input[i][j] + N*change + M*self.ci[i][j]
                self.ci[i][j] = change

        # calculate error
        error = 0.0
        for k in range(len(targets)):
            error = error + 0.5*(targets[k]-self.activation_output[k])**2
        return error


    def test(self, patterns):
        for p in patterns:
            print(p[0], '->', self.update(p[0]))

    def weights(self):
        print('Input weights:')
        for i in range(self.number_of_input):
            print(self.weight_input[i])
        print()
        print('Output weights:')
        for j in range(self.number_of_hidden):
            print(self.weight_output[j])

    def train(self, patterns, iterations=100, N=0.5, M=0.1):
        # N: learning rate
        # M: momentum factor
        j = 0;
        for i in range(iterations):
            error = 0.0
            for p in patterns:
                inputs = p[0]
                targets = p[1]
                self.update(inputs)
                error = error + self.backPropagate(targets, N, M)
            if i % 10 == 0:
                j = j + 1;
                print(' ' ,[j],'error  %-.5f' % error)


def demo():
    # Teach network XOR function
    pat = [];
    inputData = [];
    outputData = [];

    def getArrayData():
        f = open('Excel/OutputFile.csv', 'rt')
        reader = csv.reader(f);
        count = 0;
        for row in reader:
            if count==0:
                count += 1;
                continue;
            else:
                inputData = [];
                i=0;
                while(i<2):
                    inputData.append(float(row[i]));
                    i+=1;
                outputData = float(row[len(row)-1]);
                pat.append([inputData,[outputData]]);
            count += 1;
        f.close();

    getArrayData();
    print(pat);
    # create a network with two input, two hidden, and one output nodes
    n = NN(2, 2, 1)
    # train it with some patterns
    n.train(pat)
    # test it
    n.test(pat)



if __name__ == '__main__':
    demo()
