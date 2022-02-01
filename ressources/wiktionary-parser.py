from bz2file import BZ2File
from wiktionary_de_parser import Parser

import json 

bzfile_path = '/Users/gogabarabadze/Desktop/de.xml.bz2'
bz = BZ2File(bzfile_path)

textfile = open("/Users/gogabarabadze/Desktop/example.txt", "a")

for record in Parser(bz):
    if 'langCode' not in record or record['langCode'] != 'de':
      continue
    
    a = textfile.write(json.dumps(record))

textfile.close()
