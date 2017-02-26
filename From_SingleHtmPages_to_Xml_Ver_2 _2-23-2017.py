'''
Created on Oct 13, 2016

@author: Andrea Siotto
'''
import os
import codecs
import re
from bs4 import BeautifulSoup

Entry_Edition = "eb11"
Entry_Volume = 23
Entry_Letter = "r"
Entry_PageStart = 765
Entry_PageEnd = 976

def main():

    
    
    DirPath ="C:\\Users\\Andrea\\Google Drive\\Aptana Studio Environment\\Enciclopedia_Britannica_htm_List_to_single_xml\\all pages with @@@ renamed"
    files = [f for f in os.listdir(DirPath) if os.path.isfile(os.path.join(DirPath, f))] #make a list of the files in the directory   
    files.sort()# to be sure that the list is alphabetically sorted
    #print(files)
    nameBigFile = "all pages with @@@ renamed\\results\\FinalXml_6th_Version_Separated_Entries.xml"
    with codecs.open(nameBigFile,"w",encoding='utf8') as finalXmlFile: # erase or create from scratch the new file
        pass
    with codecs.open(nameBigFile,"a",encoding='utf8') as finalXmlFile:# append the data of the single files
        finalXmlFile.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        finalXmlFile.write("<body>\n")
        
        pageNumber = Entry_PageStart
        endVolume = Entry_PageEnd
        Volume = Entry_Volume
         
        allPagesString =""
        for filename in files:# for every file in the directory
            #finalXmlFile.write("<pb n=\"eb11-pg"+str(pageNumber)+"\"/>\n")
            #allPagesString+="<pb n=\"eb11-pg"+str(pageNumber)+"\"/>\n" #add the page number tag
            
            longfile= DirPath+filename#create full address of the file
            data = codecs.open(os.path.join(DirPath, filename), 'r', encoding='utf-8').read() #read the file
            soup = BeautifulSoup(data,'lxml')# Using beautifulsoup collect all the paragraphs; if there is one or more then collect them all and write them on the final file
            #if len(soup.findAll('p'))>0:
            #    paragraphs = soup.findAll('p')
            #    for paragraph in paragraphs:
            #        finalXmlFile.write(paragraph.prettify())
            soup.head.decompose()# delete the head
            soup2 = BeautifulSoup(soup.body.prettify(),'lxml')
            soup2.html.replaceWithChildren()
            soup2.body.replaceWithChildren()
            page = soup2.prettify()#formatter=lambda s: s.replace(u'\xa0', ' '))
            
            page = cleanPage(page)
            page = moveNotes(page)
            page = findEntry(page, pageNumber)# find the single entries
            page = rreplace(page,"</p>","</p>\n")
            
            allPagesString+='<pbn="'+Entry_Edition+"-"+str(Volume)+"-"+Entry_Letter+"-"+'{:04d}'.format(pageNumber)+'"/>\n' #add the new page tag
            
            allPagesString+=page
            allPagesString+="\n"
            pageNumber += 1
            if pageNumber>endVolume:
                pageNumber=1
                Volume += 1 
        
        #finalXmlFile.write("</div>\n")
        #finalXmlFile.write("</body>\n")
        allPagesString =allPagesString.replace("</div>","",1)
        allPagesString+="</div>\n"
        allPagesString+="</body>\n"
        finalXmlFile.write(allPagesString)
        finalXmlFile.close()
        allPagesString=cleanAllPages(allPagesString)
        numentries = parseInFiles(os.path.join(DirPath, "results"),allPagesString)
#         digestedData = codecs.open(nameBigFile,'r', encoding='utf-8').read()
#         digestedData.replace("</div>","",1)
#         digestedSoup = BeautifulSoup(digestedData, 'lxml-xml')
#         
#         listEntries = digestedSoup.findAll(type="entry")
#         print(len(listEntries))
def cleanPage(page):
    #page = page.replace(u'\xa0', u"\u0020")
    #page = page.replace("&nbsp;"," ")
    page = re.sub("<font.+?>","",page)# clean all fonts
    page = page.replace("</font>","")
    #page = re.sub("\s\n","\n",page)
    page = page.replace("\n","")
    page = re.sub("\s+"," ",page)
    #page = re.sub("\n{2,}","\n",page)
    page = page.replace("<div></div>","")#cleaning empty breaks
    page = page.replace("<br clear=\"all\"/>","")#cleaning clear=all
    page = re.sub (r'<a.+?>',"",page)# eliminate all the links 
    page = re.sub (r'</a.+?>{0}',"",page)
    page = re.sub (r'<td','<cell',page)
    page = re.sub (r'</td','</cell',page)
    page = re.sub (r'<tr','<row',page)
    page = re.sub (r'</tr','</row',page)
    page = re.sub (r'rowspan=','rows=',page)
    page = re.sub (r'colspan=','<cols=',page)
    return page      

def cleanAllPages(allpages):
    allpages = re.sub(r'(?<!\.)</p>\s?\n?<p>'," ",allpages)#clean the additional paragraphs coming for being in different pages but not in different phrases
    allpages = re.sub(r' +'," ",allpages)
    
    return allpages
     
def findEntry(page,pageNumber):
    #if int>0:=\
    page = re.sub(r'(?P<namesub>(<p>[\s]?[R][A-Z,\s\u00c0-\u00DC-]+)(\((c.)?(fl.)?(\s)?\d+-\d+\))?)',"\n</div>\n<div xmlns=\"http://www.tei-c.org/ns/1.0\" xml:id=\""+Entry_Edition+"-"+str(Entry_Volume)+"-"+Entry_Letter+"-"+'{:04d}'.format(pageNumber)+"\" type=\"entry\">\n<label>\g<namesub></label>\n",page)

    #page = re.sub(r'(?P<namesub>(<p>[\s]?[A-Z,\s\u00c0-\u00DC-]+)(\((c.)?(fl.)?(\s)?\d+-\d+\))?)',"\n</div>\n<div xmlns=\"http://www.tei-c.org/ns/1.0\" xml:id=\"eb11-r-"+str(pageNumber).zfill(4)+"\" type=\"entry\">\n<label>\g<namesub></label>\n",page)
    #else:
    #   page = re.sub(r'(?P<namesub>(?:(<p>[\s]?[R][A-Z,\s]+)(?:(\(\d+-\d+\))))|(?:(<p>[\s]?[R][A-Z,\s-]+)(?:(\(c. \d+-\d+\))))|(?:(<p>[\s]?[R][A-Z,\s-]{2,})(?=[\s:,<.])))',"\n</div>\n<div xmlns=\"http://www.tei-c.org/ns/1.0\" xml:id=\"eb11-r-"+str(pageNumber).zfill(4)+"\" type=\"entry\">\n<label>\g<namesub></label>\n",page)
    page = re.sub(r'<label><p>',"<p><label>",page)
    
    return page

def moveNotes(page):
    pattern1 = re.compile(r'(<p>[\s]?<sup>[\s]?@{3}[\s]?.[\s]?</sup>)')#'@{3}'
    pattern2 ='@{2}'
    pattern3 ='@{3}'
    listref = pattern1.split(page,1) #split the page by @@@
    if len(listref)>1: #if there are notes
        # split the page by references
        pageBlocks = re.split(pattern2,listref[0])# split the page by references

        cleanNotes = re.sub("<sup>|</sup>|<p>|</p>","",listref[-1])# clean the notes from tags
        noteBlocks = re.split(pattern3,cleanNotes)#split the notes
        page2=pageBlocks[0]
        for index,note in enumerate(noteBlocks):# add the necessary tags and identifiers
            textBlock = re.sub(r'(<sup>(\s+)?..(\s+)?</sup>)',"",pageBlocks[index+1],1)
            page2+='<ref xml:id="r'+str(index+1)+'" target="n'+str(index+1)+'">'+str(index+1)+'</ref>'+'<note xml:id="n'+str(index+1)+'" n="'+str(index+1)+'">'+note+'</note>'+textBlock
    else:
        page2=page
    newpage=page2
    return page2

def parseInFiles(dirPath,allPagesString):
    entryCounter = 0
    PageEntryCounter = 0
    noteCounter = 0
    refCounter = 0
    entryBreak = ['type="entry"','</body>']
    
    lines = allPagesString.split("\n")
    newEntryLines =[] #the list of all the lines of an entry
    oldEntryLines =[]
    nameEntry =""
    pageEntry =""
    nameFile=""
    
    for index,line in enumerate(lines):
        line = line.replace("</div>","\n</div>")
        if ("<pbn=" in line): # when it founds the pagecode grabs the number of the page and put to zero the Counter of entries for the page
            CodeOfPage = line.replace('<pbn="',"")
            CodeOfPage = CodeOfPage.replace('"/>',"")
            PageEntryCounter = 0
            
            
        if any(x in line for x in entryBreak): # if the line is the one that starts an entry
            if entryCounter==0: # first entry case
                nameFile = CodeOfPage+"_"+'{:02d}'.format(PageEntryCounter)                
                OldNameFile=nameFile
                
            else:# all the other entries cases
                OldNameFile = nameFile
                nameFile = CodeOfPage+"_"+'{:02d}'.format(PageEntryCounter)# 
                noteCounter = 0
                refCounter = 0
                
            line = re.sub(r'xml:id=".+?"',"xml:id="+'"'+nameFile+'"',line)
            line = line+"\n"
            print(line)
            
            oldEntryLines= list(newEntryLines)
            newEntryLines[:]=[]
            if entryCounter != 0:
                if len(oldEntryLines)>0:
                    
                    pageEntry = re.search(r'\d{4}',oldEntryLines[0])#change the page parameter
                    
                    if pageEntry:
                        page = str(pageEntry.group(0))
                        print (page)
                    else:
                        page = "0000"
                    #print (page,oldEntryLines[1])    
                    #nameFile = page+'-'+oldEntryLines[1].replace("<label>","").replace("</label>","").replace("<p>","").strip() #the name for the file: page-name of the entry
                    #nameFile = Entry_Edition+"-"+str(Entry_Volume)+"-"+Entry_Letter+"-"+page+"_"'-'+oldEntryLines[1].replace("<label>","").replace("</label>","").replace("<p>","").strip() #+str(entryCounter)
                     
                    allLines = "\n".join(oldEntryLines)
                    allLines = re.sub(r'</p><p>','</p>\n<p>',allLines)
                    allLines = refineSup(allLines)
                    writeEntry(dirPath,OldNameFile,allLines)#oldEntryLines)
                    
            PageEntryCounter +=1# 
            entryCounter+=1
            newEntryLines.append(line)
        else:
            if "<label>" in line:
                line = line.replace("<label><p>","<p><label>")
                line = line.replace("</label><p>","</label>")
            if ("<ref xml:id" in line):
                parts = re.split('(<ref xml:id.+?/ref>)|(<note xml:id.+?/note>)',line)
                refCounter=1
                noteCounter=1
                newlist=[]
                if parts!=None:
                    for part in parts[:]:
                        if part==None:
                            part=""
                            newlist.append(part)
                        elif ("<ref xml:id" in part):
                            print ("found: "+part)
                            part = re.sub(r'<ref xml:id=".+?"',"<ref xml:id="+'"'+nameFile+"-"+'r'+str(refCounter)+'"',part)                           
                            part = re.sub(r'target=".+?"','target="'+nameFile+"-"+'n'+str(refCounter)+'"',part)
                            newlist.append(part)
                            refCounter+=1
                            print ("after: "+part)
                        elif ("<note xml:id" in part):
                            print("foundnote: "+part)
                            part = re.sub(r'<note xml:id=".+?"',"<note xml:id="+'"'+nameFile+"-"+'n'+str(noteCounter)+'"',part)
                            newlist.append(part)
                            noteCounter += 1
                            print ("afternote: "+part)
                        else:
                            newlist.append(part)
                parts= [x for x in newlist if x is not None]#clear all None (I don't understand why they appear
                print(parts)
                line="".join(parts)
#                 numnotes=re.findall(r'>\d+<',line)
#                 numnote = numnotes[0]
#                 numnote=numnote.replace('>',"")
#                 numnote=numnote.replace('<',"")
#                 line = re.sub(r'<ref xml:id=".+?"',"<ref xml:id="+'"'+nameFile+"-"+'r'+numnote+'"',line)
#                 line = re.sub(r'target=".+?"','target="'+nameFile+"-"+'n'+numnote+'"',line)
#                 refCounter += 1
#                 print(refCounter)
#             if ("<note xml:id" in line):
#                 numnotes=re.findall(r'>\d+<',line)
#                 numnote = numnotes[0]
#                 numnote=numnote.replace('>',"")
#                 numnote=numnote.replace('<',"")  
#                 line = re.sub(r'<note xml:id=".+?"',"<note xml:id="+'"'+nameFile+"-"+'n'+numnote+'"',line)
#                 noteCounter += 1
#                 #line = line+"\n"
            if line!="\n": 
                newEntryLines.append(line)       
    return entryCounter

# def modifyNoteId(LinesList,NameFile):# takes a list and changes the id of the note based on the name of the file
#     for line in LineList:
#         line=re.sub(r'<ref xml:id=".+?"') 

def refineSup(Astring):
    Astring = re.sub(r'\s<sup>\s[r,t,f]\s</sup>\s',"",Astring)
    Astring = re.sub(r'\s<sup>\s11\s</sup>\s','"',Astring)
    Astring = re.sub(r'\s<sup>\sif\s</sup>\s','"',Astring)
    Astring = re.sub(r'\s<sup>\s9\s</sup>\s',"'",Astring)
    Astring = re.sub(r'\s<sup>\s0\s</sup>\s','°',Astring)


    
    return Astring

def writeEntry(Dir,Name,lineslist):
    nameFilex = Name+".xml"
    separator = ""
    allEntry= separator.join(lineslist)
   
    
    with codecs.open(os.path.join(Dir,nameFilex),"w",encoding='utf8') as entryFile: # write the file with name from oldline
        entryFile.write('<?xml version="1.0" encoding="UTF-8"?>\n')# add the xml file declaration
        entryFile.write(allEntry)
        #print (nameFilex)


def rreplace(s,old,new):
    li = s.rsplit(old,1)
    return new.join(li)
    
            
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    main()