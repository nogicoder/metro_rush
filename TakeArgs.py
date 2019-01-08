from argparse import ArgumentParser


class TakeArgs:

    def __init__(self):
        args = self.get_args()
        self.filename = args.filename
        self.algorithm = args.algo

    def get_args(self):
        algo_choice = ['Algo1', 'Algo2']
        parser = ArgumentParser(description='Solution for Metro Rush')
        parser.add_argument('filename', type=str)
        parser.add_argument('-a', '--algo',
                            metavar='algorithm',
                            nargs='?',
                            const='Algo1',
                            default='Algo1',
                            choices=algo_choice,
                            help="choose from " + str(algo_choice))
        args = parser.parse_args()
        return args
