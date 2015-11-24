# EasyHTMLParser

The Python module HTMLParser, which is part of every actual python installation, is practically not very usable. It requires absolute correct HTML and how many websites are completly OK? Sure not all. If HTMLParser parses a website with incorrect HTML, it simply crashes (gives an exception) and though the rest of the page is not parsed.

An example:

    ...title=Georgia O'Keefe ...

correct HTML would be

    ...title="Georgia O'Keefe" ...

or best

    ...title="Georgia O&#39;Keefe" ...

HTMLParser crashes on the ', gives you an exception and leaves the rest of the page unparsed.

That's why I programmed EasyHTMLParser. It behaves exactly the same way HTMLParser does, but tolerates invalid HTML. In the first example it gives you the attribute "title" with the value "Georgia". You can get incorrect or incomplete data on HTML errors, but you can parse the complete page.

# How to use

EasyHTMLParser is a python class. You have to derive your own parser class from EasyHTMLParser.
    

    class myEasyHTMLParser(EasyHTMLParser):

In your myEasyHTMLParser class you have to implement the handle_starttag, handle_data, handle_endtag etc. methods as needed, to check the HTML of the page. 

# Storage

In the Python web framework web2py theres an extension of the python dictionary called "Storage".

I recommend using this class together with EasyHTMLParser. It makes access to the attributes of an HTML tag much easier.
With Python dictionary you have to check for an attribute value with this code
  
    if tag == "img" and attrs.has_key("rel") and attrs["rel"] == "lightbox":

With Storage you don't have the check for not existing keys, it simply gives you None.
     
    if tag == "img" and attrs["rel"] == "lightbox":
    
or with the "." syntax of Storage

    if tag == "img" and attrs.rel == "lightbox":

As you can see, you need much less code for the same logic.

For license reason I don't include the Storage class here, please copy it from the web2py project by yourself. 
