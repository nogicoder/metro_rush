#!/usr/bin/env python3
from metro import *
from PathFinder import *


def main():
        try:
                metro = Metro('Delhi')
                metro.build_graph('delhi')
                pathfinding = PathFinding(metro)
                actionlist = pathfinding.get_action_list_1()

                for turn in actionlist:
                        # inital state
                        metro.update(turn)
                        print('turn:', metro.turns)
                        metro.print_train_location(-1)
                        print()
        except Exception:
                pass


if __name__ == '__main__':
    main()
