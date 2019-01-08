from sys import stderr


class GetData:
    def __init__(self, filename):
        self.line_list, self.start, self.end, self.train_numbers = self.get_data(
            filename)

    def get_data(self, filename):
        try:
            line_list = []
            stations = {}
            with open(filename) as file:
                for line in file:
                    
                    # get name of Line
                    if line.startswith('#'):
                        # if the station list is not empty
                        if stations:
                            line_list.append(Line(line_name, stations))
                            # empty the assigned station list of the current Line
                            stations = {}
                        # get the line name excluding the '#'    
                        line_name = line[1:].strip()
                    
                    # get the stations' id and name
                    elif line.split(':', 1)[0].strip().isdigit():
                        # when a line name is mistakenly deleted in the middle of the file
                        if int(line.split(':', 1)[0].strip()) is 1 and stations:
                            print('Invalid file')
                            exit(1)

                        station_id = int(line.split(':', 1)[0].strip())
                        station_name = line.split(':', 1)[1].strip()
                        stations[station_id] = station_name

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

                    # get the number of trains
                    elif line.startswith('TRAINS'):
                        train_number = line.split('=', 1)[1].strip()

            return line_list, start, end, int(train_number)

        # if error happens (KeyError, etc) -> Wrong format -> return Error
        except Exception:
            stderr.write('Invalid file\n')
            exit(1)
