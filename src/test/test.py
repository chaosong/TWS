#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2016年10月02日
@author: gongqingyi
@email:  gongqingyi@qq.com
"""

import unittest


class Test(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_1(self):
        self.assertEqual(1, 1)

    def test_2(self):
        self.assertEqual(1, 2)

if __name__ == '__main__':
    unittest.main()