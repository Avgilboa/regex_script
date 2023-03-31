# Regular expression finder script

I asked to implement a Python script that searches for matching regular expressions. The script should accept a regular expression and either a text or a file as input. The script should then search for lines that match the regular expression and print them to the console.

## Regular expression Explain:

Regular expressions (regex) are a powerful and flexible tool for searching and manipulating text data in computer programs.  
They allow you to define patterns of text that match specific formats or structures, such as phone numbers, email addresses, URLs, dates, or any other kind of textual data.

For example, to find an email address using a regular expression, you could use the pattern **".*[@].+[.]com"**. This pattern consists of several special characters and quantifiers that define the rules for finding an email address. The **'.*'** means zero or more characters, the **'@'** symbol specifies the location of the '@' symbol in the email address, and the **'.+'** means one or more characters before the **'.com'** domain name.  

Overall, regular expressions allow us to express complex patterns and rules in a concise and formal language that can be easily understood by computers. By using regular expressions, we can automate the process of searching, matching, and extracting information from text, saving us time and effort.

You can read more about regex here: [LINK](https://docs.python.org/3/howto/regex.html)  
Try your regex on a text here: [LINK](https://regex101.com/)

## Implementing a Regex Matching script
I have created a custom script that is capable of receiving a regular expression and either a file name or text from STDIN as input. It then proceeds to search for lines that match the regex expression and prints them.

## Flags the script can get:
1. **‘ -r ’ (‘--regex’) :**  This flag is mandatory and should be used to specify the regular expression to search for.  

2. **‘ -f ’ (‘--files’) :** This flag is optional and should be   used to specify the names of the files the script should   read from.
If no **'-f'** flag is provided, the script should read from STDIN.  

The script should accept only one of the following mutually exclusive flags as a list of parameters, or none of them:  

3.  **'-u' ('--underscore'):** If this flag is provided, the script should print '^' under the matching text.  

4.  **'-c' or '--color':** If this flag is provided, the script should highlight the matching text.  

5. **'-m' or '--machine':** If this flag is provided, the script should generate machine-readable output in the format of:
"file_name:no_line:start_pos:matched_text".


## Usage/Examples

```shell
python3 -regex_finder.py --regex "[p][r]" -f out.py
```

```python3
out.py:
    print("Hello-world!")
    for i in {2, 3, 4}:
        print(i)
```
```shell
output:
    print("Hello-world!")
    print(i)
```

You can see more input and output examples in the tests file

## My implementation technique

I implemented the script using the chain of responsibility design pattern, breaking down the problem into smaller tasks that are handled by individual components.  
1. First, I get the user input from the CLI and validate it to ensure that it is in the correct format. If the input is not in the correct format, an error is raised. If the input is in the correct format, it is passed to the regex handler. 
2. Second, I split the input and pass the regex expression to the regex handler.for definenig the regex, and move on to the next handler, the file handler.
3. The theard handler reads in the specified files or reads from the standard input if no file names are provided. This handler open each dile and passes it to the next handler, the match handler.
4. The match handler loop at each line on the file and checks if there is a match with the regex expression. If a match is found, the line is passed to the printer handler.
5. The printer handler looks for the appropriate flag and prints the line accordingly.  
This process continues until all lines have been processed.
