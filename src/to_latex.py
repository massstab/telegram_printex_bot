import subprocess
import os
import time

def imagify(usercode):
    head = r"\documentclass[convert={density=600, outext=.png}]{standalone}\begin{document}"
    tail = r"\end{document}"
    main = head + usercode + tail
    print(os.getcwd())
    with open('tex/usercode.tex', 'w') as f:
        f.write(main)
    os.chdir('tex')
    os.system('latex -shell-escape usercode.tex')


