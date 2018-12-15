import random
import math
import os
import subprocess

# Importing numpy

try:

    import numpy

except ModuleNotFoundError:

    try:

        answer = subprocess.check_output('pip3 install numpy', shell=True).read()
        
    except subprocess.CalledProcessError:

        os.system('sudo apt install python3-pip')
        os.system('pip3 install numpy')

    import numpy

def sigmoid(value):

        try:

            return 1/(1+math.exp(-value))

        except OverflowError:

            return 1/1+math.exp(709)

def sigmoidDerivate(value):

    return value * (1 - value)

sigmoid = numpy.vectorize(sigmoid)
sigmoidDerivate = numpy.vectorize(sigmoidDerivate)

def randommatrix2d(x, y):

    matrix = []

    for i in range(x):

        matrix.append([])

        for j in range(y):

            matrix[i].append(random.uniform(0,1))

    return numpy.array(matrix, dtype=numpy.float64)

def randommatrix1d(x):

    matrix = []

    for i in range(x):

        matrix.append(random.uniform(0,1))

    return numpy.array(matrix, dtype=numpy.float64)

class NeuralNetwork:

    def __init__(self):

        self.learningRate = 0.1
        self.numOfLayers = 3
        self.numOfNeurons = [784, 16, 10]
        self.programName = 'neuralnetwork'
        self.weights = []
        self.bias = [0]

    def generateNeurons(self):

        self.neurons = []

        for i in range(self.numOfLayers):

            self.neurons.append(numpy.array([0]*self.numOfNeurons[i], dtype=numpy.float64)[numpy.newaxis])

    def generateRandWeights(self):

        for i in range(self.numOfLayers-1):
            
            matrix = randommatrix2d(self.numOfNeurons[i+1], self.numOfNeurons[i])
            self.weights.append(matrix)

    def storeWeights(self):

        try:

            os.mkdir(self.programName)

        except FileExistsError:

            pass

        for i in range(self.numOfLayers-1):

            numpy.save('{}/weight{}.npy'.format(self.programName, i), self.weights[i])

    def useStoredWeights(self):

        try:

            for i in range(self.numOfLayers-1):

                self.weights.append(numpy.load('{}/weight{}.npy'.format(self.programName, i)))

        except FileNotFoundError:
            
            self.generateRandWeights()
            self.storeWeights()

    def storeBias(self):

        try:

            os.mkdir(self.programName)

        except FileExistsError:

            pass

        for i in range(1, self.numOfLayers):

            numpy.save('{}/bias{}.npy'.format(self.programName, i), self.bias[i])

    def useStoredBias(self):

        try:

            for i in range(1, self.numOfLayers):

                self.bias.append(numpy.load('{}/bias{}.npy'.format(self.programName, i)))

        except FileNotFoundError:
            
            self.generateRandBias()
            self.storeBias()

    def generateRandBias(self):
        
        for i in range(1, self.numOfLayers):

            matrix = randommatrix1d(self.numOfNeurons[i])
            self.bias.append(matrix)

    def propagate(self, layerToPropagate):

        newmatrix = numpy.dot(self.weights[layerToPropagate-1], self.neurons[layerToPropagate-1])
        newmatrix += self.bias[layerToPropagate]
        newmatrix = sigmoid(newmatrix)
        self.neurons[layerToPropagate] = newmatrix

    def guess(self, inputData):

        if len(inputData) == self.numOfNeurons[0]:

            self.neurons[0] = numpy.array(inputData, dtype=numpy.float64)

            for i in range(1, self.numOfLayers):

                self.propagate(i)

            return self.neurons[-1]
        
        else:

            return False

    def train(self, inputData, expectedGuess):
        
        if len(inputData) == self.numOfNeurons[0] and len(expectedGuess) == self.numOfNeurons[-1]:

            guess = self.guess(inputData)

            error = []

            for i in range(self.numOfLayers):

                error.append(numpy.array([0]*self.numOfNeurons[i], dtype=numpy.float64))

            error[-1] = numpy.array(expectedGuess, dtype=numpy.float64) - guess

            for i in range(self.numOfLayers-2, -1, -1):

                weightTranspose = self.weights[i].transpose()
                matrix = numpy.dot(weightTranspose, error[i+1])
                error[i] = matrix

            for i in range(self.numOfLayers-1):
                dlayer = sigmoidDerivate(self.neurons[i+1])

                matrix1 = self.neurons[i][numpy.newaxis].T
                matrix2 = self.learningRate * numpy.multiply(dlayer, error[i+1])[numpy.newaxis]
                
                newmatrix = numpy.dot(matrix1, matrix2).T

                self.weights[i] += newmatrix
                self.bias[i+1] += self.learningRate*numpy.multiply(error[i+1], self.neurons[i+1]*(-1)*(self.neurons[i+1]-1))

            return guess

        else:
            return False