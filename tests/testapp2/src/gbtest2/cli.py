# -*- coding: utf-8 -*-

import gbextradata2

PREFIX = "[gbtest2]"


def main():
    print(PREFIX, "GravityBee Test App 2")
    print(PREFIX, "The name of the package is " + __package__)
    print(PREFIX, "Calling method in gbextradata2:")

    gbextradata2.main()


if __name__ == "__main__":

    main()
