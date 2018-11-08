#!/usr/bin/python

import subprocess
import all_settings


## tests all options separately by executing all_settings.py
all_settings.main()


## then compiles mytheme.tex and styleguide.tex,
filesToCompile = 'mytheme', 'styleguide'
for filename in filesToCompile:
    subprocess.call('pdflatex {}.tex'.format(filename).split())
    ## compile twice because of beamer in styleguide
    subprocess.call('pdflatex {}.tex'.format(filename).split())

    ## clean up auxiliary files (non-pdf and non-tex)
    subprocess.call('rm -f {}.aux'.format(filename).split())
    subprocess.call('rm -f {}.log'.format(filename).split())
    subprocess.call('rm -f {}.nav'.format(filename).split())
    subprocess.call('rm -f {}.out'.format(filename).split())
    subprocess.call('rm -f {}.snm'.format(filename).split())
    subprocess.call('rm -f {}.toc'.format(filename).split())


## removes the pdfs created beafore  
filesToDelete = 'all_themes', 'all_colors', 'all_palettes', 'all_backgrounds', 'all_titles', 'all_blocks', 'all_notes', 'mytheme'
all_settings.removePdfs(filesToDelete)

## and removes the file created from importing all_settings
subprocess.call('rm -f all_settings.pyc')


## The generated files are all_settings.pdf and styleguide.pdf
