import pandoc
import os

pandoc.core.PANDOC_PATH = '/path/to/pandoc'

doc = pandoc.Document()
doc.markdown = open('README.md').read()
f = open('README.txt','w+')
f.write(doc.rst)
f.close()
os.system("setup.py register")
os.remove('README.txt')