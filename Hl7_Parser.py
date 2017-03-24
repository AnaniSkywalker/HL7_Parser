## Author: Anani A. Assoutovi
import json
import io
import os
import re
from hl7apy.parser import parse_message
from hl7apy.exceptions import UnsupportedVersion

#receives the name of the file and reads the messages in the file
def readMessageFile(filename):
    #read the file
    message = open(filename, 'r').read()
    print("Step 1: File read successfully")
    return message

#This method splits the 3 messages based on the blank line that is between messages
def splitMessages(strmsg):
    messageslist = re.split('\\n\\n', strmsg)
    print("Step 2: Messages splitted successfully")
    return messageslist



def hl7StrToDictionary(hl7string, use_long_name=True):
        """ Takes a string parameter and converts it to a Dictionary
        :param hl7string: HL7 string that is passed to the method
        :returns: A dictionary representation of the HL7 message
        """
        hl7string = hl7string.replace("\n", "\r")
        try :
            m = parse_message(hl7string)
        except UnsupportedVersion:
            print(" Error! : The specified version in the file is unsurpoted.")
            print(" Kindly change the version number in the text file to 2.5")

        #We create a dictionary to ensure it is json serializable
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
        #we want to write all messages into one file so we append
        #to file first and then delete any previously writen file
        with io.open('ml7tojson.json', 'a', encoding='utf8') as outfile:
            str_ = json.dumps(dictionary,
                              indent=4, sort_keys=False,
                              separators=(',', ':'), ensure_ascii=False)
            outfile.write(to_unicode(str_))


#read messages from file
strmsg = readMessageFile("HL7_Final.hl7")

#split the messages based on the blank line between messages
msgList = splitMessages(strmsg)
#lets remove a previously writen json file if the file exists, delete it
if os.path.isfile('ml7tojson.json'):
    os.remove('ml7tojson.json')
    print("Step 3: Previous json file deleted Successfully")

#Loop through the message to handle each message at a time
for message in msgList:
    # Convert it to a dictionary
    d = hl7StrToDictionary(message)
    #write JSON file
    writeJsonFile(d)

print ("A jason file with the message has been created")
