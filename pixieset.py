#!/bin/python
# -*- coding: utf-8 -*-

import csv
import fire
import json
import os.path
from pathlib import Path
import re
import shutil


def load_order_file(csv_orders_file):
    if(not os.path.isfile(csv_orders_file)):
        return None
    order_no = re.findall('-([0-9]*)\.', csv_orders_file)
    if(not order_no):
        return None
    order_no = int(order_no[0])
    csv_orders = csv.DictReader(open(csv_orders_file), quotechar='"')
    return [Order(order_no, order) for order in csv_orders]


def create_order_dirs(order, dst_dir):
    for d in ['%s/%s' % (dst_dir, d) for d in order.get_dst_dirs()]:
        if(not os.path.exists(d)):
            os.makedirs(d)


def find_file(filename, src_dir):
    p = Path(src_dir)
    q = p.rglob(filename)
    files = [f for f in q]
    if not files:
        return None
    return files[0]


class Order(object):
    def __init__(self, order_no, order_dict):
        self.order_no = order_no
        self.filename = order_dict['Filename']
        self.quantity = int(order_dict['Quantity'])
        self.product = order_dict['Product']
        self.format = re.findall('([0-9]*)x', self.product)
        if self.format:
            self.format = self.format[0]
        else:
            self.format = None
        self.digital = 'plik' in self.product.lower()

    def get_dst_dirs(self, dst_root_dir='.'):
        return [re.sub(r'(.*)/[^/]*', r'\1', dst_file) for dst_file in self.get_dst_files(dst_root_dir)]

    def get_dst_files(self, dst_root_dir='.'):
        dirs = []
        if(self.format):
            if(self.quantity==1):
                dirs.append('%s/%s/%s/%s' % (dst_root_dir, self.order_no, self.format, self.filename))
            else:
                dirs.append('%s/%s/%s/%s/%s' % (dst_root_dir, self.order_no, self.format, self.quantity, self.filename))
        if(self.digital):
            dirs.append('%s/%s/d/%s' % (dst_root_dir, self.order_no, self.filename))
        return dirs

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)


class Pixieset(object):
    def order(self, csv_orders_file, src_dir='../photos', dst_dir='../orders'):
        orders = load_order_file(csv_orders_file)
        if(not orders):
            print('!!! order file %s does not exists or has wrong order number' % (csv_orders_file))
            return

        for order in orders:
            create_order_dirs(order, dst_dir)
            src_file = find_file(order.filename, src_dir)
            for dst_file in order.get_dst_files(dst_dir):
                if not src_file:
                    print('!!! source file %s does not exist' % (order.filename))
                    continue
                print('  - copying %s -> %s' % (src_file, dst_file))
                shutil.copy('%s' % src_file, dst_file)


###############################################################################
if __name__ == '__main__':
    fire.Fire(Pixieset)
