import re
import os.path
from RawEtymologyHowellEntry import RawEtymologyHowellEntry


CURRENT_DIR = os.path.dirname(__file__)
INPUT_FILE = os.path.join(CURRENT_DIR, "data", "howell_etymology.txt")
OUTPUT_FILE =  os.path.join(CURRENT_DIR, "data", "howell_etymology_text_database.txt")


# These entries are relatively raw (obtained as a text file directly from the PDF).
# See howell_pdf_to_txt.py for the processing done
def readInRawTextEntries(file_name, strip_first_entry):
    
    entries = []
    
    with open(file_name, "r" , encoding="utf-8") as input_file:
        entry = ""
        for line in input_file:
            #print(line)
            if line != "___\n":
                entry = entry + line
            else:
                entries.append(entry)
                entry = ""
        entries.append(entry)
        
    if strip_first_entry:
        return entries[1:] # strip the first entry since it is copyright and other information
    else:
        return entries
        


LP = "\uff08" # not equivalent to the english keyboard (
RP = "\uff09" # not equivalent to the english keyboard )
#RE_KUNYOMI = "[\u3040-\u309F]+(\uff08.+?\uff09)*"
RE_KUNYOMI = "[\u3040-\u309f]+(?:\uff08.+?\uff09)*"
RE_ONYOMI = "[\u30A0-\u30FA\u30FC-\u30FE]+" # dot being used to separate kunyomi entries has value \u30FB

RE_KANJI = "[\u4E00-\u9FBF\U00020000\U0002A6DF]"
RE_SHINJITAI = "[\u4E00-\u9FBF\U00020000\U0002A6DF]"

RE_KANJI_STROKE_COUNT = "\\d+"
RE_SHINJITAI_STROKE_COUNT = "-?\\d+"



# REGEX for etymology

def get_x_yomi(regex, text):
    matches = re.findall(regex, text)
    return matches

def get_kanji(line):
    return line[0]

# After the first kanji (original form) is its stroke count
def get_kanji_stoke_count(regex, line):
    matches = re.findall(regex, line)
    return int(matches[0])

# The second kanji in the first line will be the shinjitai form (if it exists)
def get_shinjitai(regex,line):
    matches = re.findall(regex,line)
    if len(matches) > 1:
        return matches[1]
    else:
        return None
    
# After the first kanji (original form) is its stroke count
def get_shinjitai_stoke_count(regex, line):
    matches = re.findall(regex, line)
    if len(matches) == 1:
        return matches[0]
    else:
        return int(matches[1])
    

# The entries produced from howell_pdf_to_raw_txt.py can be mal-formed on page-splits when the split occurs
#   between the first line and the etymology.
# This function will split the line between the first line format and the etymology that follows
def SplitFirstLineOnMisformat(line, second_line):
    paren_shinjitai = re.search("\\(Shinjitai\\)",line)
    shinjitai = re.search("Shinjitai", line)
    
    # When this form appears, no shinjitai kanji or stroke-count are given
    # Hence, assume same as kanji and reformat the line to conform with others
    if paren_shinjitai:
        span = paren_shinjitai.span()
        front_half = line[0:span[0]] + "Shinjitai "
        stroke_span = re.search(RE_KANJI_STROKE_COUNT, line).span()
        front_half = front_half + line[0:stroke_span[1]+1]
        back_half = ""
        if span[1]+1 < len(line):
            back_half = line[span[1]+1:len(line)]
            
        return front_half, back_half
    
    elif shinjitai:
        span = shinjitai.span()
        if span[1]+3 < len(line):
            if line[span[1]+3] == "(" and "0" <= line[span[1]+4] and line[span[1]+4] <= "9": #check that we have a number and bracket where we expect to
                end_index = len(line)-1 # Sometimes Shinjitai DOES NOT HAVE A STOKE COUNT AND HENCE DOES NOT HAVE A ")"
                for i in range(span[1]+5, len(line)):
                    if line[i] == ")":
                        end_index = i
                        break
                    
                front_half = line[0:end_index+1]
                back_half = ""
                if end_index + 1 < len(line):
                    back_half = line[end_index+1:len(line)]
                    
                return front_half,back_half
        else:
            front_half = line[0 : span[1]+3] + "(-1)"
            back_half = line[span[1]+3:len(line)]
            
            print("Front_half: " + front_half)
            print("Back_half: " + back_half)
            return front_half, back_half
                
    else:
        index = 6 # magic number which pushes past kanji and stroke-count
        while index < len(line):
            first_etym_chara_if_broken = re.search("([a-zA-Z0-9]|[\u4E00-\u9FBF\U00020000\U0002A6DF])", line[index])
            if first_etym_chara_if_broken:
                return line[0:index], line[index:]
            
            index +=1
                
        
        return line, ""
    


if __name__ == "__main__":
    entries = readInRawTextEntries(INPUT_FILE, True)
    rawEtymHEntryStrings = []
    for entry in entries:
        lines = re.split("\n", entry)
        
        # ENTRIES BEING READ-IN may be mal-formed because of page splits in the original document.
        # In-particular a split between the kanji/readings line and the etymology line results in the etymology beginning on the same line as the kanji.
        # for example, see 御 and 意
        # If a kanji line contains any english characters that are not exactly the word "Shinjitai", then split and add to the next line
        front, back = SplitFirstLineOnMisformat(lines[0], lines[1])
        print("__________________")
        print("Front: " + front)
        print("Back: " + back)
        lines[0] = front
        lines[1] = re.sub("  +", " ", back + lines[1]) # adjoin the misformated text back to where it should be and remove extra spacing
        
        # Parse data
        kanji = get_kanji(lines[0])
        kanji_stroke_count = get_kanji_stoke_count(RE_KANJI_STROKE_COUNT, lines[0])
        
        print(kanji)        
        shinjitai = get_shinjitai(RE_SHINJITAI, lines[0])
        if shinjitai:
            shinjitai_stroke_count = get_shinjitai_stoke_count(RE_SHINJITAI_STROKE_COUNT, lines[0])
            if shinjitai_stroke_count == -1: # -1 here is an indicator set from SplitFirstLineOnMisformat for a single entry that had too many readings
                # There is only 1 entry with such a formatting issue
                shinji_span = re.search("\\d+", lines[1]).span()
                assert (shinji_span[0] == 1 and shinji_span[1] == 3) # Ensures we delete only appropriate info
                shinjitai_stroke_count = int(lines[1][shinji_span[0] : shinji_span[1]])
                lines[1] = lines[1][4:] # Remove the misplace data
        else:
            shinjitai_stroke_count = None
            
        kunyomi = get_x_yomi(RE_KUNYOMI, lines[0])
        onyomi = get_x_yomi(RE_ONYOMI, lines[0])
        tags = []
        
        
        rawEtymHEntry = RawEtymologyHowellEntry(
            kanji,
            kanji_stroke_count,
            shinjitai,
            shinjitai_stroke_count,
            onyomi,
            kunyomi,
            lines[1], #raw etymology
            tags
        )
        
        rawEtymHEntryStrings.append(rawEtymHEntry.Stringify())
        
    RawEtymologyHowellEntry.writeOutEntries(OUTPUT_FILE, rawEtymHEntryStrings, delim = "___\n")