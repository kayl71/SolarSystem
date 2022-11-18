# coding: utf-8
# license: GPLv3
import copy
from copy import deepcopy as copy
import matplotlib.pyplot as plt

from Data.solar_input import write_space_objects_data_to_file
class StatisticManager:

    def __init__(self):
        self.data = []
        self.dataTime = []

    def add(self, space_objects, time):

        self.data.append(copy(space_objects))
        self.dataTime.append(time)

    def get(self):
        self.__write_result_data_to_file()
        self.__write_graph_to_file()

    def __write_graph_to_file(self):
        x, y = [], []
        for i in range(len(self.data)):
            for drawObj in self.data[i]:
                obj = drawObj.obj
                x.append(self.dataTime[i])
                y.append(obj.R)
            plt.plot(x, y, '.')

        plt.savefig("Output/Graph.png")

    def __write_result_data_to_file(self):
        print(len(self.data))
        write_space_objects_data_to_file("Output/statistic.txt", self.data[len(self.data)-1])
