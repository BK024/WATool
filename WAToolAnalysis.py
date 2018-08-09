# -*- coding: utf-8 -*-
"""

"""

import pickle

filespec = "h"

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

WApostclasslist = pickle.load(open('WApostclasslist{}.p',format(filespec), 'rb'))

def extract_names(posts):
    names = {}
    for post in posts:
        names[post.author] = 0
    return names



def count_posts(posts, namesdict):
    for post in posts:
        namesdict[post.author] += 1
    postcount = list(namesdict.items())
    postcount.sort(key=lambda x: x[1], reverse=True)
    return postcount

def count_emos(posts):
    posemolist = ['😀', '😁', '😂', '😃', '😄', '😅', '😆', '😇', '😈', '😉', '😊', '😋', '😍', '😗', '😘', '😙', '😚']
    negemolist = ['😐', '😑', '😒', '😓', '😔', '😕', '😖', '😞', '😟', '😠', '😡', '😢', '😣', '😤', '😥', '😦', '😧', '😨', '😩', '😪', '😫', '😬', '😭', '😮', '😯', '😰', '😱', '😲', '😳', '😵']
    allmessages = ""
    for post in posts:
        allmessages += post.message
    poscount = 0
    negcount = 0
    for posemo in posemolist:
        poscount += allmessages.count(posemo)
    for negemo in negemolist:
        negcount += allmessages.count(negemo)
    if (poscount + negcount) > 0:
        percentagepos = int(poscount / ((poscount + negcount) / 100))
 
    else:
        percentagepos = 0
    percentagepos
    return {"pos": poscount, "neg": negcount, "dif": poscount - negcount, "percentage pos": percentagepos}


allnamesdict = extract_names(WApostclasslist)

postcountlist = count_posts(WApostclasslist, allnamesdict)



print(postcountlist)

for name in allnamesdict.keys():
    allposts = [p for p in WApostclasslist if p.author == name]
    emocount = count_emos(allposts)
    print([name, emocount])


