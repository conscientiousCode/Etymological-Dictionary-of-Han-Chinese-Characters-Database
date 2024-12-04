from pypdf import PdfReader
import os.path
import re

"""
    This file, when run, produces a stripped down txt only version of: 
        "Etymological Dictionary of Han/Chinese Characters" 
            By Lawrence J. Howell
        Research Collaborator
            Hikaru Morimoto
            
    This text has had its encoding corrected and has had its individual entries segmented.
    Entries are delimited by "___"
    
"""


CURRENT_DIR = os.path.dirname(__file__)
PDF_LOCATION = os.path.join(CURRENT_DIR, "data", "EtymologicalDictionaryOfHanChineseCharacters-HowellAndMorimoto.pdf")
OUTPUT_FILE =  os.path.join(CURRENT_DIR, "data", "howell_etymology.txt")


# Function begins read
def read_in_etymology():
    reader = PdfReader(PDF_LOCATION)
    
    book_pages = []
    
    for page in reader.pages[7:len(reader.pages)]:
    #for page in reader.pages[7:20]:
        text = page.extract_text(0) #text is a string
        """
            Python 3 strings are either utf-16 or utf-32.
            My python is "wide" (sys.maxunicode == 1114111 == 0x10FFFF)
            I do not know exactly what is in 'text', but it is probably a mix of utf-32 and utf-16 surrogates
            I suspect that whatever I was reading in was utf-16 originally and was using surrogate encodings
            for characters beyond the Basic Multilingual Plane (CJK extended characters). 
            (UTF-16 surrogates seem to have defined unicode ranges and hence can be identified as surrogates even when 
            present in a different encoding?)
            
            Everything that was not a surrogate encoding was converted to utf-32, giving me this odd, mixed string
            I think by "ignoring the surrogates" and encoding everything else to utf-16 we get back to homogenized utf-16. 
            By now decoding, we get back a homogenized utf-8 string
        """
        

        text = text.encode('utf-16', 'surrogatepass').decode("utf-16")
        book_pages.append(text)
        
    raw_text = ''.join(book_pages)
    
    raw_text = raw_text.split('\n')    
    #line_regex = "([\u3400-\u4DB5\u4E00-\u9FCB\uF900-\uFA6A]\\s\\(\\d+\\))" # regex to match the starting of a new entry
    line_regex = "([\u1000-\uFFFF]\\s\\(\\d+\\))" # regex to match the starting of a new entry
    out_text = [] # Will hold the newly formatted lines of text after pattern matching
    
    previous_line_matched = False
    
    for i in range(len(raw_text)):
        if previous_line_matched:
            out_text.append('\n')
            previous_line_matched = False
        line = raw_text[i]
        
        match = re.search(line_regex, line)
        
        # Sometimes on page ends a kanji entry will not be on its own line once read in
        if(match):
            left_split = line[:match.start()]
            right_split = line[match.start():]
            out_text.append(left_split)
            out_text.append("\n___\n")
            out_text.append(right_split)
            previous_line_matched = True
        else:
            out_text.append(line)
    
    out_text[len(out_text)-1] = out_text[len(out_text)-1][:-25] # remove "© 2016 Lawrence J. Howell" from final entry
    out_text.insert(0, "© 2016 Lawrence J. Howell\n") # add copyright to the top
    
    out_text = ''.join(out_text)
    
    return out_text
    
    
def main():
    out_text = read_in_etymology()
    
    
    #print(out_text)
        
            
    with open(OUTPUT_FILE, 'w', encoding='utf-8', errors='surrogatepass') as output:
        output.write(out_text)
        #print("END")
     
     
if __name__ == "__main__":
    main()