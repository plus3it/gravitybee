# -*- coding: utf-8 -*-

import gbtestapp.gbextradata

PREFIX = "[gbtestapp]"


def main():
    print(PREFIX, "GravityBee Test App")

    print(PREFIX, "Calling method in gbextradata:")

    gbtestapp.gbextradata.main()


if __name__ == "__main__":

    main()
