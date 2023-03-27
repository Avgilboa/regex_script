import re
import argparse

parser = argparse.ArgumentParser()


parser.add_argument("-f", "--file", help="User name")


args = parser.parse_args()

st = r""+str(args.file)
print(st)
with open('file1.txt') as file:
    pattern = re.compile(st)
    lst = file.readlines()
    for line in lst:
        match = pattern.finditer(line)
        place = [i for i in match]
        # print(place)
        for str in place:
            print(str)
            # print(line.strip())