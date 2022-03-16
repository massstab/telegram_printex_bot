import subprocess
import os

def imagify(usercode):
    head = r"\documentclass[varwidth, border=1]{standalone}" \
           r"\begin{document}"
    tail = r"\end{document}"
    main = head + usercode + tail
    with open('tex/usercode.tex', 'w') as f:
        f.write(main)
    code = subprocess.call(['pdflatex', '-halt-on-error', '-output-directory', 'tex', 'tex/usercode.tex'])
    if code == 0:
        subprocess.call(['convert', '-density', '600', '-bordercolor', 'white', '-border', '0', 'tex/usercode.pdf', 'tex/usercode.jpg'])
        return True
    else:
        return False