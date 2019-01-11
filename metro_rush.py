#!/usr/bin/env python3
from metro import *
from PathFinder import *


def main():
    metro = Metro('Delhi')
    metro.build_graph('delhi')
    path, cost = PathFinding(metro).path
    print((path, cost))

main()
