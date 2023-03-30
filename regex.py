import re
import argparse
import sys
""" 
    Input: python3 regex.py -r <regex> -f(Optional) <files>
    output: <file_name> <no_page>: <line>
"""
class my_text:
    """
    This class hold:
        (1) name of the file [with the path to avoid duplicate files]
        (2) list of the lines of the text: ["line1", "line2"]
    """
    def __init__(self, file_name , txt_lst) -> None:
        self.txt_lst, self.my_name = txt_lst , file_name

    def get_name(self):
        return self.my_name

    def __str__(self) -> str:
        st = ''
        for num_line,exp in enumerate(self.txt_lst):
            st += f"{num_line}: {exp}"
        return st

""""""
class handler:
    def set_next(self, handler):
        pass
    def handle(self,regex, files,flags):
        pass  


class regex_handler(handler):
    def __init__(self) -> None:
        self.next_handler = None
    def set_next(self, handler):
        self.next_handler = handler
        return handler
    def handle(self, regex, files, flags):
    # not gonna happend because regex is required to be
        if regex is None:
            raise Exception("Usage -r <regex> (optional) -f <regex>")
        regex = r""+regex
        self.next_handler.handle(regex, files, flags)


class file_handler(handler):
    def __init__(self) -> None:
        self.next_handler = None

    def set_next(self, handler):
        self.next_handler = handler
        return handler
    
    def handle(self, regex, files, flags):
        if files is None:
            self.next_handler.handle(regex, my_text("input".strip(),
                                    [st.strip() for st in sys.stdin.readlines()]), flags)
        else:
            for txt in files:
                self.next_handler.handle(regex, my_text(txt, self.file_to_lst(txt)) , flags)

    def file_to_lst(self, file_name):
        if file_name is None:
            raise Exception("need a file name")
        try:
            with open(str(file_name)) as file:
                return file.readlines()
        except:
            raise Exception("no such file {}".format(str(file_name)))


class match_handler(handler):
    def __init__(self) -> None:
        self.next_handler = None
    
    def set_next(self, handler):
        self.next_handler = handler
        return handler
    
    def handle(self, regex, files: my_text, flags):
            pattern = re.compile(regex)
            for line,exp in enumerate(files.txt_lst):
                match = pattern.finditer(exp.strip())
                place = [i for i in match]
                if len(place) > 0:
                    self.next_handler.handle(line+1, exp.strip(), place, files.get_name(), flags)


class printer_handler:
    def __init__(self) -> None:
        self.next_handler = None
    
    def set_next(self, handler):
        self.next_handler = handler
        return handler
    
    def handle(line: int, exp:str, place: object, file_name: str, flags):
        if flags["machine"] is True:
            print("[{}:{}:{}:{}]".format(file_name, line, place[0].start(), place[0].group()))
            return
        header ="[{}::{}]".format(file_name, line)
        if flags["color"] is True:
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
            
        if flags["under_score"] is True:
            exp2 =""
            for match in place:
                exp2 += " " * (match.start() - len(exp2))
                exp2 += "^" * (match.end() - match.start())
            exp = exp.strip() + "\n"  + " "*(len(header)) + exp2
        print(header + exp)


class init():
    def __init__(self) -> None:
        files , regex , flags = self.split_from_terminal()
        self.handler = regex_handler()
        self.handler.set_next(file_handler()).set_next(match_handler()).set_next(printer_handler)
        self.handler.handle(regex, files, flags)
    

    def split_from_terminal(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-r", "--regex",dest= "regex" ,required=True ,help= "our regex")
        parser.add_argument("-f", "--files",dest="file", nargs='+' ,help="The file name")
        parser.add_argument("-u","--underscore",dest= "under_score" ,action='store_true',
                            help="add '^ under the found regex text")
        parser.add_argument("-c","--color" ,action='store_true',
                            help="color the found regex text")
        parser.add_argument("-m","--machine" ,action='store_true',
                            help="generate macine readable output")
        args = parser.parse_args()
        # regex = find_the_regex(args.regex, args.under_score, 
        #                     args.color, args.machine)
        return args.file, args.regex, {"under_score" :args.under_score,
                                        "color" : args.color,
                                        "machine" : args.machine}
   
init()
