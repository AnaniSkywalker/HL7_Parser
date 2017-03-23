## Author: Anani A. Assoutovi
import json
import io
from hl7apy.parser import parse_message
from hl7apy.exceptions import UnsupportedVersion


# receives the name of the file and reads the messages in the file
def readMessageFile(filename):
    # read the file
    message = open(filename, 'r').read()
    return message


def hl7StrToDictionary(hl7string, use_long_name=True):
    """ Takes a string parameter and converts it to a Dictionary
    :param hl7string: HL7 string that is passed to the method
    :returns: A dictionary representation of the HL7 message
    """
    hl7string = hl7string.replace("\n", "\r")
    try:
        m = parse_message(hl7string)
    except UnsupportedVersion:
        print(" Error! : The specified version in the file is unsurpoted.")
        print(" Kindly change the version number in the text file to 2.5")

    return hl7MessageToDictionary(m, use_long_name=use_long_name)


def hl7MessageToDictionary(m, use_long_name=True):
    """Convert an HL7 message to a dictionary
    """
    if m.children:
        d = {}
        for c in m.children:
            name = c.name.lower()
            if use_long_name:
                name = c.long_name.lower() if c.long_name else name
            dictified = hl7MessageToDictionary(c, use_long_name=use_long_name)
            if name in d:
                if not isinstance(d[name], list):
                    d[name] = [d[name]]
                d[name].append(dictified)
            else:
                d[name] = dictified
        return d
    else:
        return m.to_er7()


def writeJsonFile(dictionary):
    # Write JSON file
    try:
        to_unicode = unicode
    except NameError:
        to_unicode = str
    with io.open('jsonmessage.json', 'w', encoding='utf8') as outfile:
        str_ = json.dumps(dictionary,
                          indent=4, sort_keys=True,
                          separators=(',', ':'), ensure_ascii=False)
        outfile.write(to_unicode(str_))


message = readMessageFile("HL7_Final.txt")
# Convert it to a dictionary
d = hl7StrToDictionary(message)
# write JSON file
writeJsonFile(d)
# Dump it as a JSON string
print("A jason file with the message has been created")




