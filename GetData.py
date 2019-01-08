from sys import stderr
from metro import *


class GetData:
    def __init__(self, filename):
        self.max_train = self.get_max_train(filename)
        self.line_list, self.start, self.end = self.get_data(
            filename)

    # get the maximum number of trains
    def get_max_train(self, filename):
        try:
            with open(filename) as file:
                    for line in file:
                        if line.startswith('TRAINS'):
                            train_number = line.split('=', 1)[1].strip()
                            return int(train_number)
        except Exception:
            stderr.write('Invalid file\n')
            exit(1)

    def get_data(self, filename):
        try:
            line_list = []
            stations = []
            with open(filename) as file:
                for line in file:

                    # get name of Line and create a Line instance
                    if line.startswith('#'):
                        # if the station list is not empty
                        if stations:

                            # Create a Line instance
                            line_list.append(Line(line_name))

                            # Add Station instances to Line instance
                            for station in stations:
                                Line.add_station(station)
                            # empty the assigned station list of the current Line
                            stations = {}
                        # get the line name excluding the '#'    
                        line_name = line[1:].strip()
                    
                    # get the station name and create a Station instance
                    elif line.split(':', 1)[0].strip().isdigit():
                        # when a line name is mistakenly deleted in the middle of the file
                        if int(line.split(':', 1)[0].strip()) is 1 and stations:
                            print('Invalid file')
                            exit(1)

                        station_name = line.split(':', 1)[1].strip()
                        stations.append(Station(station_name, line_name, self.max_train))

                    # get the starting station's linename and id
                    elif line.startswith('START'):
                        starting_line = line.split(
                            '=', 1)[1].split(':')[0].strip()
                        starting_station_id = line.split(
                            '=', 1)[1].split(':')[1].strip()

                        # in case some character is typed besides the station's id
                        if starting_station_id.isdigit():
                            start = (starting_line, int(starting_station_id))

                    # get the ending station's linename and id
                    elif line.startswith('END'):

                        ending_line = line.split(
                            '=', 1)[1].split(':')[0].strip()
                        ending_station_id = line.split(
                            '=', 1)[1].split(':')[1].strip()

                        if ending_station_id.isdigit():
                            end = (ending_line, int(ending_station_id))

            return line_list, start, end

        # if error happens (KeyError, etc) -> Wrong format -> return Error
        except Exception:
            stderr.write('Invalid file\n')
            exit(1)
