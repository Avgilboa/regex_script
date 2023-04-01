import os
import pytest
## testing files from the 'files' folder and the results from 'res' folder
## using pytest tp check the script.


@pytest.mark.parametrize("command ,out_file",[
    ('echo "hello world! \n hello world" | python3 regex_finder.py -r !' , 'cat res/hello-world.txt'),
    ('python3 regex_finder.py -r or -f files/song1.txt' , 'cat res/song1_test1.txt'),
    ('python3 regex_finder.py -r "[()].*[)]" -f files/song2.txt' , 'cat res/song2_test1.txt' ),
    ('python3 regex_finder.py -r [0-9]{4} < files/username-or-email.csv ', 'cat res/susername-or-email_num_test.txt'),
    ('python3 regex_finder.py -r .*[@].*[.]com < files/username-or-email.csv' , 'cat res/susername-or-email_mail_test.txt'),
    ('python3 regex_finder.py -r m < files/color.txt ', 'cat res/color_num_test1.txt'),
    ('python3 regex_finder.py -r print < files/try.py' , 'cat res/try_test1.txt ')
])  
def test_regex_without_flags(command, out_file):
    assert os.popen(command).readlines() == os.popen(out_file).readlines()
    

@pytest.mark.parametrize("command ,out_file",[
    ('echo "" | python3 regex_finder.py -r h -c' , 'cat res/empty_test2.txt'),
    ('python3 regex_finder.py -r happy -c < files/song2.txt' , 'cat res/song2_color_test.txt'),
    ('python3 regex_finder.py -r \[\(\].*\[\)\] -u -f files/song2.txt' , 'cat res/song2_underscore_test.txt'),
    ('python3 regex_finder.py --regex ".*[@].*[.][a-z]{3}" -u --files files/email.csv' , 'cat res/mail_text_underscore.txt'),
    ('python3 regex_finder.py -r "[a-z]{1}[o][a-z]{1}" -u < files/song1.txt' , 'cat res/song1_underscore_test.txt'),
    ('python3 regex_finder.py -r m -u < files/color.txt' , 'cat res/color_num_test1_underscore.txt'),
    ('python3 regex_finder.py -r m -c < files/color.txt' ,'cat res/color_num_test1_color.txt'),
    ('python3 regex_finder.py -r m -m < files/color.txt ' , 'cat res/color_num_test1_machine.txt'),
    ('python3 regex_finder.py -r print -u < files/try.py ' ,'cat res/try_test1_underscore.txt' ),
    ('python3 regex_finder.py -r print -c  < files/try.py ' , 'cat res/try_test1_color.txt'),
    ('python3 regex_finder.py -r print -m< files/try.py' , 'cat res/try_test1_machine.txt')
])
def test_regex_with_flags(command, out_file):
    assert os.popen(command).readlines() == os.popen(out_file).readlines()
