#!/bin/python
# -*- coding: utf-8 -*-

import fire
import csv

class Pixieset(object):
    def order(self, verb, base_dir=".", order_csv="*.csv"):
        print("verb: %s, base_dir: %s, order_csv: %s" % (verb, base_dir, order_csv))

###############################################################################
if __name__ == '__main__':
    fire.Fire(Pixieset)
