# WATool
A tool to analyze WhatsApp export files.

A tool written in Python 3 that can analyze the export .txt file of a WhatApp chat. It can parse all lines in such a text file to recognize system messages (eg. 'You have added John to the group') and real conversational messages. Also posts that people make with newline character in the message of the post itself are new lines in the text file. The tool will recognize those as well and append those 'continuation lines' to the message they belong to. It then stores all lines in a custom class called 'Post'. Date, time, author and message are the main attributes of this class. Those instantiations are store in a list, so still ordered, and that list is dumped using pickle.

That file can be loaded to make an analysis. Two thing can be calculated. 1. The number of posts per participant. 2. What the percentage is of the positive smileys people used of the total of positive ánd negative smileys.
These results are dumped using pickle.

Then there is a module that visualizes these analytical results.
