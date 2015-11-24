# -*- coding: utf-8 -*-
import re

# Use Storage if you have the web2py Storage class in project
#__all__ = ['Storage', 'easyhtmlparser']
__all__ = ['EasyHTMLParser']


class EasyHTMLParser(object):

    def __init__(self, msg="", position=(None, None)):
        self.data = ""
        self.msg = msg
        self.lineno = position[0]
        self.offset = position[1]
        self.arraytags = []
        self.dataLength = 0
        self.script_content = False
        self.script_count = 0


    def classifytags(self, tagcontent):
        # tag types:
        # 1. start, 2. end, 3. comment, 4. declaration
        tagtype = 0
        if self.script_content:
            self.script_count += 1
        tagcontent = tagcontent.strip().lower()
        if tagcontent[0:1] == "/" or tagcontent[:0] == "/":
            tagtype = 2
            if (tagcontent.startswith("script") or tagcontent.endswith("script")) and self.script_content:
                self.script_content = False
                self.script_count = 0
        elif tagcontent.startswith("!--"):
            tagtype = 3
        elif tagcontent.startswith("!"):
            tagtype = 4
        else:
            tagtype = 1
            if tagcontent.startswith("script") and not tagcontent.endswith("/"):
                self.script_content = True
        return tagtype


    def feed(self, data):
        self.data = data
        self.dataLength = len(self.data)
        # parse for tags and give them a type
        self.gettags()
        cntTags = len(self.arraytags)
        for i in range(0, cntTags):
            if self.arraytags[i][2]==1:
                tagcontent = self.data[self.arraytags[i][0]:self.arraytags[i][1]].strip()
                # Use Storage if you have the web2py Storage class in project
                # dictAttr = Storage()
                dictAttr = {}
                idxValueStart = 0
                idxValueEnd = tagcontent.find(" ")
                if idxValueEnd==-1:
                    self.handle_starttag(tagcontent[1:-1].lower(), dictAttr)
                else:
                    # tag mit attributen, diese koennen name oder name=value sein
                    eol = False
                    # nur den tagname ermitteln, dann von vorn
                    tagname = tagcontent[1:idxValueEnd]
                    # Algo: je nach Zeichen nach dem = ('," oder ohne) wird bis zum naechsten zeichen verfahren
                    idxValueEnd = tagcontent.find("=")
                    if idxValueStart==-1:
                        # es stehen keine Name-Value-Paare in attr, aber eventuell mehrere Props
                        for a in arrTag:
                            attrName = a.strip()
                            if not attrName=="":
                                dictAttr[attrName] = ""
                    else:
                        lenght = len(tagcontent)
                        idxStart = 0
                        idxEnd = tagcontent.find(" ")
                        while not (idxStart == -1 or idxEnd == -1):
                            idxStart = idxEnd+1
                            idxEnd = tagcontent.find("=", idxStart)
                            if not idxEnd == -1:
                                attrName = tagcontent[idxStart:idxEnd].strip().lower()
                                #print "attrName"
                                #print attrName
                                idxStart = idxEnd + 1
                                if tagcontent[idxStart:idxStart+1].strip() == '"':
                                    # Bsp: type="text/javascript"
                                    idxEnd = tagcontent.find('"', idxStart+1)
                                elif tagcontent[idxStart:idxStart+1].strip() == "'":
                                    # Bsp: type='text/javascript'
                                    idxEnd = tagcontent.find("'", idxStart+1)
                                else:
                                    # Bsp: type=text/javascript
                                    idxEnd = tagcontent.find(" ", idxStart)
                                    if idxEnd == -1:
                                        # Wenn kein " " gefunden ist der gesamte Rest von
                                        # tagcontent als attr zu betrachten
                                        idxEnd = len(tagcontent)-2
                                attrValue = self.doUnquote(tagcontent[idxStart:idxEnd+1])
                                dictAttr[attrName] = attrValue.strip()
                    self.handle_starttag(tagname[0:].lower(), dictAttr)
            elif self.arraytags[i][2] == 2:
                tagname = self.data[self.arraytags[i][0]+1:self.arraytags[i][1]-1]
                self.handle_endtag(tagname.replace("/", "").lower())
            elif self.arraytags[i][2] == 3:
                self.handle_comment(self.data[self.arraytags[i][0]:self.arraytags[i][1]])
            elif self.arraytags[i][2] == 4:
                self.handle_decl(self.data[self.arraytags[i][0]:self.arraytags[i][1]])

            j = self.arraytags[i][1]
            if not i+1 == cntTags:
                k = self.arraytags[i+1][0]
            else:
                k = self.dataLength
            if not self.data[j:k].strip() == "":
                self.handle_data(self.data[j:k])


    def gettags(self):
        tag = re.compile('<[^>]*>')
        eof = False
        idxopen = 0
        while not eof:
            re_tag = tag.search(self.data, idxopen)
            if re_tag is not None:
                tagtype = self.classifytags(re_tag.group()[1:-1])
                if not self.script_content or self.script_count == 0:
                    self.arraytags.append([re_tag.span()[0], re_tag.span()[1], tagtype])
                idxopen = re_tag.span()[0] + 1
            else:
                eof = True


    def doUnquote(self, content):
        if content.startswith("'") or content.startswith('"'):
            return content[1:-1]
        elif content.startswith("<") and content.endswith(">"):
            return content[1:-1]
        else:
            return content


    def handle_startendtag(self, tag, attrs):
        pass


    def handle_starttag(self, tag, attrs):
        pass


    def handle_endtag(self, tag):
        pass


    def handle_charref(self, name):
        pass


    def handle_entityref(self, name):
        pass


    def handle_data(self, data):
        pass


    def handle_comment(self, data):
        pass


    def handle_decl(self, decl):
        pass