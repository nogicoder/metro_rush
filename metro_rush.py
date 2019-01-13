#!/usr/bin/env python3
from metro import *
from PathFinder import *


def main():
    metro = Metro('Delhi')
    metro.build_graph('delhi')
    path, cost = PathFinding(metro).path, PathFinding(metro).cost
    converted_path = PathFinding(metro).converted_path
    print((path, cost))
    print(converted_path)



if __name__ == '__main__':
    main()
