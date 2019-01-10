# -*- coding: utf-8 -*-

import os

SOME_CONSTANT = "success"

pkg_dir = os.path.dirname(os.path.realpath(__file__))

some_data = open(os.path.join(pkg_dir, 'data_file.txt'), "r").read()

PREFIX = "[gbextradata]"


def main():
    print(PREFIX, "GravityBee Extra Data")
    print(PREFIX, "SOME_CONSTANT:", SOME_CONSTANT)
    print(PREFIX, "some_data:", some_data)


if __name__ == "__main__":
    main()
