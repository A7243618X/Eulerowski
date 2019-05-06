import Eulerian
from Eulerian import *
import unittest

class KnownValues(unittest.TestCase):
    def testSmallest(self):
        matrix=[[0,1],
                [1,0]]
        self.assertEqual(getEulerian(matrix), [0,1])

    def test2(self):
        matrix=[[0, 1, 1], [1, 0, 1], [1, 1, 0]]
        self.assertEqual(getEulerian(matrix), [0,1,2,0])

    def test3(self):
        matrix=[[0, 1, 0], [1, 0, 1], [0, 1, 0]]
        self.assertEqual(getEulerian(matrix), [0,1,2])

    #testy podane w przykładzie, efekt się rózni
    def testFromLesson1(self):
        matrix=[[0, 1, 1, 0, 0, 0, 0],
                [1, 0, 1, 1, 1, 0, 0],
                [1, 1, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 1, 0, 0],
                [0, 1, 0, 1, 0, 1, 1],
                [0, 0, 0, 0, 1, 0, 1],
                [0, 0, 0, 0, 1, 1, 0]]
        self.assertEqual(getEulerian(matrix), [0,1,3,4,5,6,4,1,2,0])

    def testFromLesson2(self):
        matrix=[[0, 1, 1, 0, 0, 0],
                [1, 0, 1, 1, 0, 0],
                [1, 1, 0, 0, 0, 0],
                [0, 1, 0, 0, 1, 1],
                [0, 0, 0, 1, 0, 1],
                [0, 0, 0, 1, 1, 0]]
        self.assertEqual(getEulerian(matrix), [1,0,2,1,3,4,5,3])
