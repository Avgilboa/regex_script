# Regular expression finder script

I Asked to implement a Python script that searches for matching regular expressions. The script should accept a regular expression and either a text or a file as input. The script should then search for lines that match the regular expression and print them to the console.

## flags for the script and their meanings:
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
Terminal:
  python3 regex.py --regex "[p][r]" -f files/out.py
```

```python3
out.py:
    print("Hello-world!")
    for i in {2, 3, 4}:
        print(i)
```
```shell
output:
    [files/out.py::1]print("Hello-world!")
    [files/out.py::3]print(i)
```
