import re

# [e1, e2, e3] ->  "[e1, e2, e3]"
# Function assumes elements can be concatenated to a string
def StringifyArray(array):
            out = "["
            for e in array:
                out += str(e) + ", "
            if len(array) > 0:
                out = out[:-2]
            out += "]"
            return out      

#"[a, b, c]" -> ["a","b","c"]
#Note that this method will split objects that contain ',' in their string representations
def ArrayifyString(arrayString):
        comma_sep = arrayString[1:-1]
        elements = re.split(",", comma_sep)
        arr = []
        if elements[0] == "":
            return arr
        for element in elements:
            arr.append(element.strip())
        return arr
    
