class Line:

    def __init__(self, line_name, info):

        self.name = line_name
        self.info = info

def remove_blank_space(text):
    while "" in text:
        if "" in text:
            text.remove("")
    return text

def list_of_lines(data):
    line_list = []
    for _lst in data:
        name = _lst[0]
        info = []
        for item in remove_blank_space(_lst[1:]):
            item = item.split(sep=":", maxsplit=1)
            item[1] = item[1].split(",")

            info.append([int(item[0]), item[1][0], int(item[1][1]), int(item[1][2])])
        line_list.append(Line(name, info))
    return line_list

def process_data(file_name):
    with open(file_name, "r") as f:
        content = f.read()

    content = content.split("#")
    # print(content)
    content = remove_blank_space(content)
    last_block_in_content = remove_blank_space(content[-1].split("\n"))
    # print(last_block_in_content)
    info = last_block_in_content[-3:]
    for index, item in enumerate(info):
        if index == len(info) - 1:
            info[index] = int(item.split('=')[1:][0])
        else:
            info[index] = item.split('=')[1:][0].split(":")
    data = []
    for index, item in enumerate(content):
        if index == len(content) - 1:
            item = remove_blank_space(item[:-1].split("\n"))
            data.append(item[:-3])
        else:
            data.append(item[:-1].split("\n"))
    # print(data)
    line_list = list_of_lines(data)
    # print(line_list)
    for line in line_list:
        print("{}: {}\n".format(line.name, line.info))
    return line_list
print(process_data('delhi_with_coordinates'))
