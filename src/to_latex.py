import subprocess
import os

def imagify(usercode):
    head = r"\documentclass{standalone}\begin{document}"
    tail = r"\end{document}"
    main = head + usercode + tail
    print(os.getcwd())
    with open('tex/usercode.tex', 'w') as f:
        f.write(main)
    os.chdir('tex')
    code = subprocess.call(['pdflatex', '-halt-on-error', 'usercode.tex'])
    if code == 0:
        subprocess.call(['convert', '-density', '600', '-bordercolor', 'white', '-border', '10', 'usercode.pdf', 'usercode.png'])
        return True
    else:
        return False