import re
import argparse
import sys
""" 
    Input: python3 regex.py -r <regex> -f(Optional) <files>
    output: <file_name> <no_page>: <line>
"""
class my_text:
    def __init__(self, file_name) -> None:
        self.txt_lst = self.file_to_lst(file_name)
        self.my_name = file_name


    def file_to_lst(self, file_name):
        if file_name is None:
            raise Exception("need a file name")
        try:
            with open(str(file_name)) as file:
                return file.readlines()
        except:
            raise Exception("no such file {}".format(str(file_name)))


    def get_name(self):
        return self.my_name


    def __str__(self) -> str:
        st = ''
        for num_line,exp in enumerate(self.txt_lst):
            st += f"{num_line}: {exp}"
        return st


    def find_regex(self, regex: str):
        pattern = re.compile(regex)
        for line,exp in enumerate(self.txt_lst):
            match = pattern.finditer(exp)
            place = [i for i in match]
            if '-u' in sys.argv:
                
            if len(place) > 0:
                print(f"{self.get_name()} {line+1}: {exp.strip()}")

def regex_to_str(regex) -> str:
    if regex is None:
        raise Exception("Usage -r <regex> (optional) -f <regex>")
        # not gonna happend because regex is required to be
    return r""+str(regex)


def split_from_terminal():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--regex",required=True ,help= "our regex")
    parser.add_argument("-f", "--file",nargs='+' ,help="The file name")
    args = parser.parse_args()
    regex = regex_to_str(args.regex)
    print(type(args.file))
    for txt in args.file:
        my_text(txt).find_regex(regex)
    

split_from_terminal()