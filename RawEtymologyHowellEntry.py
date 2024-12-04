import string_tools as ST
import re

class RawEtymologyHowellEntry():
    
    def __init__(
        self,
        kanji,
        kanji_stroke_count, #int
        shinjitai,
        shinjitai_stroke_count, #int
        onyomi, # list of strings
        kunyomi, # list of string
        raw_etymology, # string
        tags #list of strings; 
        
    ):
        self.kanji = kanji
        self.kanji_stroke_count = kanji_stroke_count
        self.shinjitai = shinjitai
        self.shinjitai_stroke_count = shinjitai_stroke_count
        self.onyomi = onyomi
        self.kunyomi = kunyomi
        self.raw_etymology = raw_etymology
        self.tags = tags
        
        
    # An intermediate file format for howell entry
    # if this is updated, BuildFromStringified should be updated
    def Stringify(self):
        out_string = ""
        out_string += "kanji:" + self.kanji + "\n"
        out_string += "kanji_stroke_count:" + str(self.kanji_stroke_count) + "\n"
        if self.shinjitai:
            out_string += "shinjitai:" + self.shinjitai + "\n"
            out_string += "shinjitai_stroke_count:" + str(self.shinjitai_stroke_count) + "\n"
        else:
            out_string += "shinjitai:NONE\n"
            out_string += "shinjitai_stroke_count:0\n"
        out_string += "onyomi:" + ST.StringifyArray(self.onyomi) + "\n"
        out_string += "kunyomi:" + ST.StringifyArray(self.kunyomi) + "\n"
        
        out_string += "raw_etymology:" + self.raw_etymology + "\n"
        out_string += "tags:" + ST.StringifyArray(self.tags)
        return out_string
    
    def BuildFromStringified(string_rep):
        lines = re.split("\n", string_rep)
        
        #For each line in the ordered sequence, strip the associated label and process the data
        kanji = lines[0][len("kanji:"):]
        kanji_stroke_count = int(lines[1][len("kanji_stroke_count:"):])
        #out of order for shinjitai entry
        shinjitai_stroke_count = lines[3][len("shinjitai_stroke_count:"):]
        if shinjitai_stroke_count == 0:
            shinjitai = None
        else:
            shinjitai = lines[2][len("shinjitai:"):]
        onyomi = ST.ArrayifyString(lines[4][len("onyomi:"):])
        kunyomi = ST.ArrayifyString(lines[5][len("kunyomi:"):])
        raw_etymology = lines[6][len("raw_etymology:"):]
        tags = ST.ArrayifyString(lines[7][len("tags:"):])
        
        
        return RawEtymologyHowellEntry(
            kanji,
            kanji_stroke_count, #int
            shinjitai,
            shinjitai_stroke_count, #int
            onyomi, # list of strings
            kunyomi, # list of string
            raw_etymology, # string
            tags #list of strings; 
            
        )
        
    
    # writes a list of stringified entries to the file with the given delimiter 
    def writeOutEntries(file_name, string_entries:list, delim = "___\n"):
        with open(file_name, "w", encoding="utf-8") as output_file:
            i = 0
            for entry in string_entries:
                output_file.write(entry)
                output_file.write("\n" + delim)
    
    # reads in a list of stringified entries from the file specified and construct a list of RawEtymologyHowellEntry objects   
    def readInEntries(file_name, delim="___\n"):
        entries = []
        with open(file_name, "r", encoding="utf-8") as input_file:
            entry = ""
            for line in input_file:
                if line != "___\n":
                    entry = entry + line
                else:
                    entries.append(RawEtymologyHowellEntry.BuildFromStringified(entry))
                    entry = ""
        
        return entries