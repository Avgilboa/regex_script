import re
import argparse
import sys

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

"""
abstract method of "Chain of Responsibility", the design pattern, i decide to implement.


function:
    1. Set_next -> the next handler of the procces
    2. Handle   -> the handler preform his responsibility before move it to the next handler.
"""
class handler:
    def set_next(self, handler):
        self.next_handler = handler
        return handler
    def handle(self,regex, files,flags):
        pass  

"""
(1) The first method of the chain.
get from the terminal the definition of the regex string
and make it easy to use by converte it a raw string.


beacuse the regex is the same for all the files we first convert.
raw string - for using characters that has spcial meaning (escpe charcter) as part of the string.

next(2) handler will deal with the text input (files or STDIN).

"""
class regex_handler(handler):
    def __init__(self) -> None:
        self.next_handler = None
    def set_next(self, handler):
        return super().set_next(handler)
    def handle(self, regex, files, flags):
    # not gonna happend because regex is required to be
        if regex is None:
            raise Exception("Usage -r <regex> (optional) -f <regex>")
        regex = r""+regex
        self.next_handler.handle(regex, files, flags)

"""
(2) convert each file from the name to my_text type.

my_text - hold list that hold each text line on diffrent index and the name of the file.
If there is no -f (--files) flags the code make the input string to a list and named it "input".

next(3) handler will deal with each file separately and search in each line if the regex found.

"""
class file_handler(handler):
    def __init__(self) -> None:
        self.next_handler = None

    def set_next(self, handler):
        return super().set_next(handler)
    
    def handle(self, regex, files, flags):
        if files is None:
            self.next_handler.handle(regex, my_text("input".strip(),
                                    [st.strip() for st in sys.stdin.readlines()]), flags)
        else:
            for file in files:
                self.next_handler.handle(regex, my_text(file, self.file_to_lst(file)) , flags) for file in files

    def file_to_lst(self, file_name):
        if file_name is None:
            raise Exception("need a file name")
        try:
            with open(str(file_name)) as file:
                return file.readlines()
        except:
            raise Exception("no such file {}".format(str(file_name)))

"""
(3) iterate each line of the file and check for the regex

using re module for finding if the regex string exist in the line.
if it doesn't exist -> iterate to the next line
if it does exist    -> send to the next handler(4) for printing the line.
"""
class match_handler(handler):
    def __init__(self) -> None:
        self.next_handler = None
    
    def set_next(self, handler):
        return super().set_next(handler)
    
    def handle(self, regex, files: my_text, flags):
            # search for the regex with the re module
            pattern = re.compile(regex)
            for line,exp in enumerate(files.txt_lst):
                place = [i for i in pattern.finditer(exp.strip())]
                if len(place) > 0:
                    self.next_handler.handle(line+1, exp.strip(), place, files.get_name(), flags)

"""
(4) check the flags given from the termnial for printing and print respectively.

there is three flags: 
-m (machine mode) -->  format: file_name:no_line:start_pos:matched_text. 
-c (color mode)   -->  highlight the matching text (i choose to paintng it with yellow).
-u (underscore)   -->  which prints '^' under the.

using dictionary to know which flags we get in the terminal
"""
class printer_handler:
    def __init__(self) -> None:
        self.next_handler = None
    
    def set_next(self, handler):
        return super().set_next(handler)
    
    def handle(line: int, exp:str, place: object, file_name: str, flags):
        if flags["machine"] is True:
            print("[{}:{}:{}:{}]".format(file_name, line, place[0].start(), place[0].group()))
            return
        
        #define header for print the file_name (with the path) and the number line before the text.
        header ="[{}::{}]".format(file_name, line)


        if flags["color"] is True:
            #list of the highlighting string and the index of them in the proginal strings.
            color_name =[]
            #save the index will need to reflace for save the original indexs for any char on exp
            # and print eventually the exprtion with the color. 
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
            print(header + exp)
            return
            

        if flags["under_score"] is True:
            # make anothr string that will be with '^' where it match the regex in the original string 
            exp2 =""
            for match in place:
                exp2 += " " * (match.start() - len(exp2))
                exp2 += "^" * (match.end() - match.start())
            exp = exp.strip() + "\n"  + " "*(len(header)) + exp2
            print(header + exp)
            return
        

        print(header + exp)

        

"""
(0) This is the init class of the project

It define the order of the handlers.
Get the text from the terminal and split it according to the flags
and send to the first handler the input.

"""
class init():
    def __init__(self) -> None:
        files , regex , flags = self.split_from_terminal()
        if [value for value in flags.values()].count(True) > 1:
            raise Exception("you can use only one of this flags: -u -c -m")
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

        # return (-f or --files values ) , (-r or --regex value) ,
        # dictionary of {"under_score" :(-u or --underscore value),
        # "color" : (-c or --color value),"machine" : (-m or --machine value)}

        return args.file, args.regex, {"under_score" :args.under_score,
                                        "color" : args.color,
                                        "machine" : args.machine}
   


init()
