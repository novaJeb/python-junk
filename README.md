# python-junk
Some 100% grade-A trash built with Python 3.whatever

## AutoFormatter
Thing used to replace & update the headers/footers of lots of html files at once.
Works by locating  
\<div class='content'>  
and  
\<div class='footer'>  
then copying the data found between those tags, as well as special data like title tags.
Wipes document, writes in new header, writes in copied data, then writes in new footer, while filling in the special data along the way.
