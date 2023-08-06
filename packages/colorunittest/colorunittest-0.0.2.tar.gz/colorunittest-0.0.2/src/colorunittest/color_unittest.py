import io
import contextlib
import re
import unittest
from termcolor import colored
import re

def run_unittest(tcls):
    suite = unittest.TestLoader().loadTestsFromTestCase(tcls)
    with io.StringIO() as buf:
        with contextlib.redirect_stdout(buf):
            unittest.TextTestRunner(stream=buf, verbosity=2).run(suite)
        s = return_unittest_output(buf.getvalue())
        print(s)

def return_color(s):
    if 'fail' in s:
        return 'red'
    if 'error' in s:
        return 'yellow'
    if 'ok' in s:
        return 'blue'
    return 'black'
    
def return_unittest_output(s):
    # move bottom statement to top
    beg_str_ind = re.search(r'Ran \d', s).start()
    if beg_str_ind:
        s = s[beg_str_ind:] + s[:beg_str_ind]
    # find terms to color
    pattern = r'(?=\bok|\bOK|\bERROR|\bFAIL)(.+?)(?=\n)'
    prev_end = 0
    colored_output = []
    indices_list = [(m.start(0), m.end(0)) for m in re.finditer(pattern, s)]
    if indices_list:
        for n, (start, end) in enumerate(indices_list):
            if n == 0:
                colored_output = s[prev_end:start]
            else: 
                colored_output += s[prev_end:start]
            status = s[start:end]
            status_label = status.strip().lower()
            color = return_color(status_label)
            if status_label[0:1] == 'ok':
                status = status.replace('ok', 'OK')
            colored_output += colored(status, color, attrs=['bold'])
            prev_end = end
        colored_output += s[end:]
    else:
        colored_output = s
    return colored_output