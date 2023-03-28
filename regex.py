import re
import argparse

""" 
    Input: python3 regex.py -r <regex> -f(Optional) <files>
    output: <file_name> <no_page>: <line>
"""
class my_text:


    def __init__(self, file_name) -> None:
        self.txt_lst, self.my_name = self.file_to_lst(file_name), file_name


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


class Definitions:
    def __init__(self, under_score: bool, color: bool, machine: bool ) -> None:
        self.under_score, self.color, self.machine = under_score, color, machine

class find_the_regex(Definitions):
    def __init__(self, regex, under_score: bool, color: bool, machine: bool) -> None:
        super().__init__(under_score, color, machine)
        self.regex = self.regex_to_str(regex)
    

    def regex_to_str(self, regex) -> str:
        if regex is None:
            raise Exception("Usage -r <regex> (optional) -f <regex>")
            # not gonna happend because regex is required to be
        return r""+str(regex)
    
    
    def find_regex(self, text: my_text):
        pattern = re.compile(self.regex)
        for line,exp in enumerate(text.txt_lst):
            match = pattern.finditer(exp.strip())
            place = [i for i in match]
            if len(place) > 0:
                self.printer(line+1, exp.strip(), place, text.get_name())
    

    def printer(self, line: int, exp:str, place: object, file_name: str): 
        if self.color is True:
            color_name =[]
            start = 0
            for match in place:
                color_expr = ((start, match.start()) ,
                              "\033[93m" + exp[match.start():match.end()] + "\033[0m" )
                color_name.append(color_expr)
                start = match.end()
            exp2 =""
            for (start_pos,end_pos) , st in color_name:
                exp2 += exp[start_pos: end_pos] + st
            exp2 = exp2 + exp[start:]
            exp = exp2
            
        if self.under_score is True:
            exp2 =""
            for match in place:
                exp2 += " " * (match.start() - len(exp2))
                exp2 += "^" * (match.end() - match.start())
            exp = exp.strip() + "\n" + exp2
            #print(exp)
        if self.machine is True:
            print("[{}:{}:{}]".format(file_name, line,exp.strip()))
        print(exp)
        


def split_from_terminal():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--regex",required=True ,help= "our regex")
    parser.add_argument("-f", "--file",nargs='+' ,help="The file name")
    parser.add_argument("-u","--under_score" ,action='store_true',
                         help="add '^ under the found regex text")
    parser.add_argument("-c","--color" ,action='store_true',
                        help="color the found regex text")
    parser.add_argument("-m","--machine" ,action='store_true',
                        help="generate macine readable output")
    args = parser.parse_args()
    regex = find_the_regex(args.regex, args.under_score, 
                           args.color, args.machine)
    for txt in args.file:
        regex.find_regex(my_text(txt))
    

split_from_terminal()
#print("\033[35m" + "This text will be blue." + "\033[0m" + "and this in the defualt color")