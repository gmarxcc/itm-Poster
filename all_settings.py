#!/usr/bin/python
from string import Template
import subprocess
import sys

with open('all_settings.tex', 'r') as f:
  template = Template(f.read())


themes = 'Default', 'Rays', 'Basic', 'Simple', 'Envelope', 'Wave', 'Board', 'Autumn', 'Desert'

colors = 'Default', 'Australia', 'Britain', 'Sweden', 'Spain', 'Russia', 'Denmark', 'Germany'

palettes = 'Default', 'BlueGrayOrange', 'GreenGrayViolet', 'PurpleGrayBlue', 'BrownBlueOrange'

backgrounds = 'Default', 'VerticalGradation', 'Rays', 'BottomVerticalGradation', 'Empty'

titles = 'Default', 'Basic', 'Empty', 'Filled', 'Envelope', 'Wave', 'VerticalShading'

blocks = 'Default', 'Basic', 'Minimal', 'Envelope', 'Corner', 'Slide', 'TornOut'

notes = 'Default', 'VerticalShading', 'Corner', 'Sticky'




##################################################################################
## This function creates a latex document from the template in
## "all_settings.tex" by substituting the values for the theme, and
## for the color, background, title, block and note commands, and
## adding a specific message as the title and a sub-message as the
## author of the document. Then it compiles this file (called
## "filename.tex"), keeps only the pdf file, and remembers its name
## for future.
## 
## We also need latex commands because the resulting pdf contains the
## code of the document. So we need to modify certain characters for
## latex.
## 
def createTexAndCompile( message, submessage, theme, colorcommand,
                         backgroundcommand, titlecommand,
                         blockcommand, notecommand, themelatexcommand,
                         colorlatexcommand, backgroundlatexcommand,
                         titlelatexcommand, blocklatexcommand,
                         notelatexcommand, filename, filelist ):

    page = template.substitute(
        {
            'messagevar': message,
            'submessagevar': submessage,
            'themevar': theme,
            'colorvar': colorcommand,
            'backgroundvar': backgroundcommand,
            'titlevar': titlecommand,
            'blockvar': blockcommand,
            'notevar': notecommand,
            'themestylevar': themelatexcommand,
            'colorstylevar': colorlatexcommand,
            'backgroundstylevar': backgroundlatexcommand,
            'titlestylevar': titlelatexcommand,
            'blockstylevar': blocklatexcommand,
            'notestylevar': notelatexcommand,
        }
    )

    ## create a tex file
    with open(filename + '.tex', 'w') as f:
        f.write(page)

    ## compile the tex file
    subprocess.call('pdflatex {}.tex'.format(filename).split())

    ## clean up auxiliary files (non-pdf)
    subprocess.call('rm -f {}.tex'.format(filename).split())
    subprocess.call('rm -f {}.aux'.format(filename).split())
    subprocess.call('rm -f {}.log'.format(filename).split())
    
    ## remember the name of the file for future
    filelist.append(filename)
    
    return
##################################################################################


##################################################################################
## This function is for testing styles using the Default theme, or for
## testing each theme without modifications.
##
## This function creates latex commands for each style, depending on
## the values of theme, color, palette, background, title, block and
## note.  Then calls function createTexAndCompile that uses these
## commands to create and compile the actual document.
## 
## The main difference of this function with
## createTexAndCompileAllOptions is follows. The generated pdf
## contains the code used to generate it, so that users could easily
## see the settings. In this function the code is kept minimal, so the
## commands of the form \usesomestyle{Default} are not
## displayed. Therefore, if one uses a non-Default theme and then, for
## instance, default block style, it would have effect in the
## generated pdf, but the code in the pdf would not be correct.
##
## Thus, in principle this function can be used for arbitrary
## combinations of options, but the correctness of the code in the pdf
## file is guaranteed only for testing styles using the Default theme,
## or for testing each theme without modifications.
##
def createTexAndCompileOneOption( message, submessage, theme, color, palette, 
                         background, title, block, note, filelist ):

    themelatexcommand = ''
    colorcommand = colorlatexcommand = ''
    backgroundcommand = backgroundlatexcommand = ''
    titlecommand = titlelatexcommand = ''
    blockcommand = blocklatexcommand = ''
    notecommand = notelatexcommand = ''
   
    ## only if theme is the default one, we also specify other styles
    if theme != 'Default' and theme != '':
        themelatexcommand = r'\bs usetheme\{' + theme + r'\}\\'
    
    if color != '':
        if palette != '': 
            colorcommand = r'\usecolorstyle[colorPalette=' + palette + ']{' + color + '}'
            colorlatexcommand = r'\bs usecolorstyle[colorPalette=' + palette + ']\{' + color + r'\}\\'
        else:
            colorcommand = r'\usecolorstyle{' + color + '}'
            colorlatexcommand = r'\bs usecolorstyle\{' + color + r'\}\\'
        if colorcommand == r'\usecolorstyle{Default}' or colorcommand == r'\usecolorstyle[colorPalette=Default]{Default}':
            colorcommand = colorlatexcommand = ''
    elif palette != '' and palette != 'Default':
        colorcommand = r'\usecolorstyle[colorPalette=' + palette + ']{Default}'
        colorlatexcommand = r'\bs usecolorstyle[colorPalette=' + palette + r']\{Default\}\\'
               
    if background != 'Default' and background != '':
        backgroundcommand = r'\usebackgroundstyle{' + background + '}'
        backgroundlatexcommand = r'\bs usebackgroundstyle\{' + background + r'\}\\'

    if title != 'Default' and title != '':
        titlecommand = r'\usetitlestyle{' + title + '}'
        titlelatexcommand = r'\bs usetitlestyle\{' + title + r'\}\\'

    if block != 'Default' and block != '':
        blockcommand = r'\useblockstyle{' + block + '}'
        blocklatexcommand = r'\bs useblockstyle\{' + block + r'\}\\'

    if note != 'Default' and note != '':
        notecommand = r'\usenotestyle{' + note + '}'
        notelatexcommand = r'\bs usenotestyle\{' + note + r'\}\\'
    
    filename = 'ff_' + theme + color + palette + background + title + block + note

    createTexAndCompile( message, submessage, theme, colorcommand,
                         backgroundcommand, titlecommand,
                         blockcommand, notecommand, themelatexcommand,
                         colorlatexcommand, backgroundlatexcommand,
                         titlelatexcommand, blocklatexcommand,
                         notelatexcommand, filename, filelist )

    return
##################################################################################


##################################################################################
## This function is for testing all combinations of styles.
##
## This function creates latex commands for each style, depending on
## the values of color, palette, background, title, block and note.
## Then calls function createTexAndCompile that uses these commands to
## create and compile the actual document.
##
def createTexAndCompileAllOptions( message, submessage, theme, color,
                                   palette, background, title, block, note,
                                   filelist ):

    themelatexcommand = ''
    colorcommand = colorlatexcommand = ''
    backgroundcommand = backgroundlatexcommand = ''
    titlecommand = titlelatexcommand = ''
    blockcommand = blocklatexcommand = ''
    notecommand = notelatexcommand = ''
   
    if theme != '':
        themelatexcommand = r'\bs usetheme\{' + theme + r'\}\\'
    else:
        themelatexcommand = r'\bs usetheme\{Default\}\\'
  
    if color != '':
        if palette != '': 
            colorcommand = r'\usecolorstyle[colorPalette=' + palette + ']{' + color + '}'
            colorlatexcommand = r'\bs usecolorstyle[colorPalette=' + palette + ']\{' + color + r'\}\\'
        else:
            colorcommand = r'\usecolorstyle{' + color + '}'
            colorlatexcommand = r'\bs usecolorstyle\{' + color + r'\}\\'
    elif palette != '':
            colorcommand = r'\usecolorstyle[colorPalette=' + palette + ']{Default}'
            colorlatexcommand = r'\bs usecolorstyle[colorPalette=' + palette + r']\{Default\}\\'
           
    if background != '':
        backgroundcommand = r'\usebackgroundstyle{' + background + '}'
        backgroundlatexcommand = r'\bs usebackgroundstyle\{' + background + r'\}\\'

    if title != '':
        titlecommand = r'\usetitlestyle{' + title + '}'
        titlelatexcommand = r'\bs usetitlestyle\{' + title + r'\}\\'

    if block != '':
        blockcommand = r'\useblockstyle{' + block + '}'
        blocklatexcommand = r'\bs useblockstyle\{' + block + r'\}\\'

    if note != '':
        notecommand = r'\usenotestyle{' + note + '}'
        notelatexcommand = r'\bs usenotestyle\{' + note + r'\}\\'
    
    
    filename = 'ff_' + theme + color + palette + background + title + block + note

    createTexAndCompile( message, submessage, theme, colorcommand,
                         backgroundcommand, titlecommand,
                         blockcommand, notecommand, themelatexcommand,
                         colorlatexcommand, backgroundlatexcommand,
                         titlelatexcommand, blocklatexcommand,
                         notelatexcommand, filename, filelist )
    
    return
##################################################################################


##################################################################################
## A function to combine all pdfs whose names are given in the list filelist,
## in a file called outputFile
##
def combinePdfs( outputFile, filelist ):
    ## merging all pdfs in filelist
    command = 'gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=' + outputFile + '.pdf'
    subprocess.call(
        command.split() + [t + '.pdf' for t in filelist]
    )

    return
##################################################################################


##################################################################################
## A function to remove pdf files whose names are given in the list filelist
##
def removePdfs( filelist ):
    ## removing the pdfs
    for filename in filelist:
        subprocess.call('rm -f {}.pdf'.format(filename).split())

    return
##################################################################################


##################################################################################
## A function to combine all pdfs whose names are given in the list filelist,
## in a file called outputFile, then remove these files
##
def combineAndRemovePdfs( outputFile, filelist ):
    combinePdfs( outputFile, filelist )
    removePdfs( filelist )

    return
##################################################################################


##################################################################################
## A function to try all options: color palettes, color styles, backgrounds,
## titles, blocks and notes separately
def testAllOptionsSeparately( ):
    filenames = []
 
    ##########------------------------------##########
    ##########------------------------------##########
    ########## varying themes
    color = palette = background = title = block = note = ''
    submessage = 'All options are defined by the theme'
    outputFile = 'all_themes'

    for theme in themes:
        message = 'Using ' + theme + ' theme'
        createTexAndCompileOneOption(message, submessage, theme, color, palette, 
                                     background, title, block, note, filenames)
                        
    combineAndRemovePdfs(outputFile, filenames)

    ##########------------------------------##########
    ########## varying color styles
    del filenames[:] 
    theme = background = title = block = note = 'Default'
    palette = ''
    submessage = 'with the rest being Default'
    outputFile = 'all_colors'

    for color in colors:
        message = 'Using ' + color + ' color style'
        createTexAndCompileOneOption(message, submessage, theme, color, palette, 
                                     background, title, block, note, filenames)
                        
    combineAndRemovePdfs(outputFile, filenames)
 
    ########## varying color palettes
    del filenames[:] 
    theme = color = background = title = block = note = 'Default'
    submessage = 'with the Default color style'
    outputFile = 'all_palettes'

    for palette in palettes:
        message = 'Using ' + palette + ' color palette'
        createTexAndCompileOneOption(message, submessage, theme, color, palette, 
                                     background, title, block, note, filenames)
                        
    combineAndRemovePdfs(outputFile, filenames)

    ##########------------------------------##########
    ########## varying backgrounds
    del filenames[:] 
    theme = color = palette = title = block = note = 'Default'
    submessage = 'with the rest being Default'
    outputFile = 'all_backgrounds'

    for background in backgrounds:
        message = 'Using ' + background + ' background style'
        createTexAndCompileOneOption(message, submessage, theme, color, palette, 
                                     background, title, block, note, filenames)

    combineAndRemovePdfs(outputFile, filenames)

    ##########------------------------------##########
    ########## varying titles
    del filenames[:] 
    theme = color = palette = background = block = note = 'Default'
    submessage = 'with the rest being Default'
    outputFile = 'all_titles'

    for title in titles:
        message = 'Using ' + title + ' title style'
        createTexAndCompileOneOption(message, submessage, theme, color, palette, 
                                     background, title, block, note, filenames)
                        
    combineAndRemovePdfs(outputFile, filenames)

    ##########------------------------------##########
    ########## varying blocks
    del filenames[:] 
    theme = color = palette = background = title = note = 'Default'
    submessage = 'with the rest being Default'
    outputFile = 'all_blocks'

    for block in blocks:
        message = 'Using ' + block + ' block style'
        createTexAndCompileOneOption(message, submessage, theme, color, palette, 
                                     background, title, block, note, filenames)
                        
    combineAndRemovePdfs(outputFile, filenames)

    ##########------------------------------##########
    ########## varying notes
    del filenames[:] 
    theme = color = palette = background = title = block = 'Default'
    submessage = 'with the rest being Default'
    outputFile = 'all_notes'

    for note in notes:
        message = 'Using ' + note + ' note style'
        createTexAndCompileOneOption(message, submessage, theme, color, palette, 
                                     background, title, block, note, filenames)
                        
    combineAndRemovePdfs(outputFile, filenames)
    del filenames[:] 

    ###############--------------------###############
    ############### combine the 7 pdfs into one called all_settings
    outputs = 'all_themes', 'all_colors', 'all_palettes', 'all_backgrounds', 'all_titles', 'all_blocks', 'all_notes'
    combinePdfs('all_settings', outputs)

    return
##################################################################################


##################################################################################
## A function to try all combinations of options: themes, palettes,
## color, background, title, block and note styles
##
def testAllOptionsCombined( ):
    filenames = [] 
    outputFile = 'all_combinations'

    for theme in themes:
        for color in colors:
            for palette in palettes:
                for background in backgrounds:
                    for title in titles:
                        for block in blocks:
                            for note in notes:
                                message = 'Using ' + theme + ', ' + palette
                                submessage = color + background + title + block + note 
                            
                                createTexAndCompileAllOptions(message,
                                                              submessage,
                                                              theme, color,
                                                              palette,
                                                              background,
                                                              title, block,
                                                              note,
                                                              filenames)
                            
    combineAndRemovePdfs(outputFile, filenames)
    del filenames[:] 

    return
##################################################################################


##################################################################################
## A function to test all predefined themes
def testThemes( ):
    filenames = [] 
    color = palette = background = title = block = note = ''
    submessage = 'All options are defined by the theme'
    outputFile = 'all_themes'

    for theme in themes:
        message = 'Using ' + theme + ' theme'
        createTexAndCompileOneOption(message, submessage, theme, color, palette, 
                                     background, title, block, note, filenames)
                        
    combineAndRemovePdfs(outputFile, filenames)
    del filenames[:] 

    return
##################################################################################


##################################################################################
def usageMessage():
    print 'usage: '
    print '  all_settings.py'
    print '      produces all_settings.pdf by '
    print '          testing all themes and all options separately, and '
    print '          combining them into one file.'
    print r'  all_settings.py all'
    print r'      tests all combinations of all options. Be careful! 352800 combinations'

    return
##################################################################################


##################################################################################
############################## Main Body #########################################
##################################################################################

def main():
    if len(sys.argv) == 1:
        ## tests all options separately, and generates files all_settings,
        ## all_themes, all_colors, all_palettes, all_backgrounds,
        ## all_titles, all_blocks, and all_notes
        testAllOptionsSeparately()

    elif len(sys.argv) == 2:
        if sys.argv[1] == 'all':
            testAllOptionsCombined()
        else:
            ## in future we can allow more parameters, for instance compiling
            ## all options for a particular theme
            usageMessage()
            sys.exit(2)
    else:
        usageMessage()
        sys.exit(2)


if __name__ == "__main__":
    main()
