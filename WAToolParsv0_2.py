# -*- coding: utf-8 -*-
"""
This module opens a txt file and assumes it is the export file of a
WhatsApp chat. 
It will process all the lines in the chat and determine whether those are
real conversational messages, continuation lines or system messages.
Real messages are posts by participants in the WhatsApp chat. 
These messages are always one line. 
This module will split the file along all lines. 

If chat participants make a
post with multiple lines those new lines will be recognized as a new post
but should not be considered as such since they are part of the message 
that was started in the lines above. These lines are called continuation lines
and the text of these lines is added to the message of the previous real message.

The above options (real or continuation) describe almost all lines. 
The rest are system messages. These are not considered
as real posts and are recognized by deviating from the structure of a normal post,
but more structured then a continuation line. 

Real posts and system messages are parsed and the info is stored in a Post class. 
Continuation lines are added to the previous Post class to which they belong and
therefore are not parsed and not stored in a new class.
 
The result is a list with instantiations of Post classes. They resemble the 
order in which the lines occured in the original export file. 
This list is then saved by using pickle dump. 
"""

import pickle

lastpost = None
postclasslist = []

class Post:
    """The class the contains the data from a real post or system message
    """
    def __init__(self, postdata, other=False):       
        """Stores data extracted from a real post or a system message.
        It receives postdata as a list with strings as elements. That
        list is the result of splitting the line from the chat file
        along the first three whitespaces. It receivers 'other' as a boolean.
        That variable signifies a system message.

        The date, time, author and message are stored as strings.
        When it is a system message the author is always "System". 

        There is one boolean variable called "edited". 
        When False the message has not been edited after
        instantiation. When a continuation line is discovered while parsing that belongs to this post
        the message is appended with that line and the variable "edited" becomes True.
        
        When it is a system message no author has to be extracted. 
        When not a system message that parsing is done in this function. 
        
        Todo: 
            *Check if the parsing should not be removed from this init function. 
             It seems out of place.  
            *Create DateTime objects to replace the date and time strings for 
             better analysis in the future. 
        Version 0.2
        """

        self.date = postdata[0]
        self.time = postdata[1]
        self.edited = False
        self.author = 'System'
        if not other:     
            self.author_message = postdata[3].split(sep=":", maxsplit=1)
            self.author = self.author_message[0]
            self.message = self.author_message[1]
        else:
            self.message = postdata[3]

    def edit(self, continuation):
        """Concatenate a string to the existing "self.message" string"""
        self.message += "{}".format(continuation)     
        self.edited = True



def make_line_gen(txtfile):
    """Creates a generator object.
       It receives a text file and
       yields one line at a time. 
       That line is read using readline() so always has
       a new line character at the end. 
    """
    while True:
        line = txtfile.readline()
        if not line:
            break
        else:
            yield line

def parse_line(line):
    """Parses the string it is given. 
       
       There are three types of lines: - Real message
                                       - Continuation line
                                       - System message
       Real message and System message look similar starting with 
       date and time. 
       Examples:
       "09-11-16 14:12 - Bart van Berkel: Aah.." is a real message.
       "08-03-18 14:46 - U hebt Bart van Berkel toegevoegd" is a system message.
       The difference is that system messages do not have a ":" in the message.
       Real messages do have a name then a ":" and then 
       message. 
       Continuation lines are assumed to not have the structure with date 
       and time.

       The first code filters deviant messages (not containing 
       at least 3 whitespaces) and handles those as continuation lines.
 
       Then the structure of date and time is checked. If that structure is
       present the line is considered real or system. Otherwise continuation.
       When real or system, the difference is determined by the ":" in the
       message.
       
       Continuation lines are added to the last real post. By the 'edit' attr.
       If there was no previous instantiation of a Post class a warning is 
       printed and nothing is done before returning "None".

       Real or system messages are stored in a new instantiation of the Post
       class and then that instatiation is returned.
       
       Todo:
            * Make reoccuring code redundant by restructuring the logic.
            * Remove prints that were used to develop. Or make those 
              dependant on a 'verbose' variable.
            * Determine structure (starting with a date and time) by
              using regular expressions.                 
    """
    global lastpost     
    splitlinelist = line.split(maxsplit=3)    
    if len(splitlinelist) < 3:
        #this has to be a continuation line. So attach it to last posts message 
        if not lastpost:
            print("No post has been stored and yet we find a continuation line??")
            print(line, "This line is discarded, please check validity of txt file")
            print("Press enter to continue")
            input() 
            return None
        else:
            print("continuation line! type1", line) 
            lastpost.edit(line)
        return None

    #check if this line starts with a date
    #check if the date is followed by a time 
    #check if followed by a dash
    if len(splitlinelist[0]) == 8 and \
        splitlinelist[0][0].isnumeric() and \
        splitlinelist[0][1].isnumeric() and \
        splitlinelist[0][2] == "-" and \
        splitlinelist[0][3].isnumeric() and \
        splitlinelist[0][4].isnumeric() and \
        splitlinelist[0][5] == "-" and \
        splitlinelist[0][6].isnumeric() and \
        splitlinelist[0][7].isnumeric() and \
        splitlinelist[1][0].isnumeric() and \
        splitlinelist[1][1].isnumeric() and \
        splitlinelist[1][2] == ":" and \
        splitlinelist[1][3].isnumeric() and \
        splitlinelist[1][4].isnumeric() and \
        splitlinelist[2][0] == "-":
            #we now know that the line is either a real post or a system message
            if splitlinelist[3].find(":") != -1:
                #this has to be a real post
                newpost = Post(splitlinelist, other=False)
                lastpost = newpost
                print("real post!")                
                return newpost
            else:
                #this has to be a system message
                print("system message!") 
                return Post(splitlinelist, other=True)
    else:
        #this has to be a continuation line. So attach it to last posts message 
        if not lastpost:
            print("No post has been documented and yet we find a continuation line??")
            print(line, "This line is discarded, please check validity of txt file")
            print("Press enter to continue")
            input() 
            return None
        else:
            print("continuation line! type2", line) 
            lastpost.edit(line)
        return  None


WAtxt = open('WAgroepN.txt', 'r')

linegen = make_line_gen(WAtxt)
"""generator object: yields every line in the WAtxt file. """

while True:
    try:
        nextline = next(linegen)
    except StopIteration:
        break
    nextpostclass = parse_line(nextline)
    if nextpostclass:
        postclasslist.append(nextpostclass)
    else:
        continue

#a quick print just for checking the code. 
tempdict = {}
for post in postclasslist:
    cnt = tempdict.get(post.author)
    if not cnt:
        tempdict[post.author] = 1
    else:
        tempdict[post.author] += 1
print(tempdict.items())

pickle.dump(postclasslist, open("WApostclasslist.p", "wb"))

