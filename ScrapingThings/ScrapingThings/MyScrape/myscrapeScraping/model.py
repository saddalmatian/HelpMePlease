from typing import Text

# Pal -> Pal Element -> PalChild


class PostItem:
    def __init__(self, rank, title, id_post, link, point, user, time_post, comment):
        self.id_post = id_post
        self.rank = rank
        self.time_post = time_post
        self.link = link
        self.title = title
        self.point = point
        self.user = user
        self.comment = comment


class PalElement:
    overList = []

    def __init__(self, content, tag, inside, siblingContent):
        self.content = content
        self.inside = inside
        self.tag = tag
        self.Insidetext = ""
        self.siblingContent = siblingContent

    def getSibling(self, tagElement: str) -> list:
        palList = []
        nextPos = 0
        
        tagPos1 = self.siblingContent.find("<"+tagElement, nextPos)
        tagPos2 = self.siblingContent.find(">", tagPos1)
        palTag = self.siblingContent[tagPos1:tagPos2+1]
        
        checkPos = tagPos2
        tailPos = self.siblingContent.find("</"+tagElement+">", checkPos)
        
        while(self.siblingContent.find("<"+tagElement, nextPos) != -1):
            
            if(self.siblingContent[checkPos:tailPos].find("<"+tagElement) != -1):
                checkPos = self.siblingContent[checkPos:tailPos].find(
                    "<"+tagElement, checkPos+1)
                tailPos = self.siblingContent.find("</"+tagElement+">", tailPos+1)
                
            else:
                palInside = self.siblingContent[tagPos2 +
                                         1:self.siblingContent.find(">", tailPos)+1]
                palContent = self.siblingContent[tagPos1:tailPos+len(tagElement)+3]
                palList.append(PalElement(palContent, palTag, palInside, "None"))
                nextPos = tagPos2
                tagPos1 = self.siblingContent.find("<"+tagElement, nextPos)
                tagPos2 = self.siblingContent.find(">", tagPos1)
                palTag = self.siblingContent[tagPos1:tagPos2+1]
                checkPos = tagPos2
                tailPos = self.siblingContent.find("</"+tagElement+">", checkPos)
        self.overList.append(palList)
        return self.overList[len(self.overList)-1]

    def text(self) -> str:
        nextPos = 0
        trigPos1 = self.content.find(">", nextPos)
        trigPos2 = self.content.find("<", trigPos1)
        while(trigPos2 != -1):
            self.Insidetext += self.content[trigPos1+1:trigPos2]
            nextPos = trigPos2
            trigPos1 = self.content.find(">", nextPos)
            trigPos2 = self.content.find("<", trigPos1+1)
        return self.Insidetext

    def get(self, tag) -> str:
        """
        Get attribute of tagElement
        example: pal.findBy("tr","class.athing")[0].get('class')
        """
        if(self.tag.find(tag) != -1):
            resultPos1 = self.tag.find(tag)+len(tag)+2
            resultPos2 = self.tag.find(" ", resultPos1)-1
            return self.tag[resultPos1:resultPos2]
        else:
            return None

    def findBy(self, tagElement: str, detail: str) -> list:
        palList = []
        findType = detail[0:detail.find(".")]
        findWith = detail[detail.find(".")+1:len(detail)]
        nextPos = 0
        tagPos1 = self.content.find("<"+tagElement, nextPos)
        tagPos2 = self.content.find(">", tagPos1)
        palTag = self.content[tagPos1:tagPos2+1]
        checkPos = tagPos2
        tailPos = self.content.find("</"+tagElement+">", checkPos)
        while(self.content.find("<"+tagElement, nextPos) != -1):
            if(palTag.find(findType+"="+"'"+findWith+"'") != -1 or palTag.find(findType+"="+'"'+findWith+'"') != -1):
                if(self.content[checkPos:tailPos].find("<"+tagElement) != -1):
                    checkPos = self.content[checkPos:tailPos].find(
                        "<"+tagElement, checkPos+1)
                    tailPos = self.content.find("</"+tagElement+">", tailPos+1)
                else:
                    palInside = self.content[tagPos2 +
                                             1:self.content.find(">", tailPos)+1]
                    palContent = self.content[tagPos1:tailPos+len(tagElement)+3]                                      
                    palSiblingContent = self.content[tailPos+len(tagElement)+3:len(self.content)]                       
                    palList.append(PalElement(
                    palContent, palTag, palInside, palSiblingContent))
                    nextPos = tagPos2
                    tagPos1 = self.content.find("<"+tagElement, nextPos)
                    tagPos2 = self.content.find(">", tagPos1)
                    palTag = self.content[tagPos1:tagPos2+1]
                    checkPos = tagPos2
                    tailPos = self.content.find("</"+tagElement+">", checkPos)

            else:
                nextPos = tagPos2
                tagPos1 = self.content.find("<"+tagElement, nextPos)
                tagPos2 = self.content.find(">", tagPos1)
                palTag = self.content[tagPos1:tagPos2+1]
                checkPos = tagPos2
                tailPos = self.content.find("</"+tagElement+">", checkPos)

        self.overList.append(palList)
        return self.overList[len(self.overList)-1]

    def find(self, tagElement: str):

        palList = []
        nextPos = 0
        tagPos1 = self.content.find("<"+tagElement, nextPos)
        tagPos2 = self.content.find(">", tagPos1)
        palTag = self.content[tagPos1:tagPos2+1]
        checkPos = tagPos2
        tailPos = self.content.find("</"+tagElement+">", checkPos)
        while(self.content.find("<"+tagElement, nextPos) != -1):
            if(self.content[checkPos:tailPos].find("<"+tagElement) != -1):
                checkPos = self.content[checkPos:tailPos].find(
                    "<"+tagElement, checkPos+1)
                tailPos = self.content.find("</"+tagElement+">", tailPos+1)
            else:
                palInside = self.content[tagPos2 +
                                         1:self.content.find(">", tailPos)+1]
                palContent = self.content[tagPos1:tailPos+len(tagElement)+3]
                palSiblingContent = self.content[tailPos+len(tagElement)+3:len(self.content)]                       
                palList.append(PalElement(
                    palContent, palTag, palInside, palSiblingContent))
                nextPos = tagPos2
                tagPos1 = self.content.find("<"+tagElement, nextPos)
                tagPos2 = self.content.find(">", tagPos1)
                palTag = self.content[tagPos1:tagPos2+1]
                checkPos = tagPos2
                tailPos = self.content.find("</"+tagElement+">", checkPos)
        self.overList.append(palList)
        return self.overList[len(self.overList)-1]


class Pal:

    overList = []

    def __init__(self, content):
        self.content = content

    def findBy(self, tagElement: str, detail: str) -> list:
        palList = []
        findType = detail[0:detail.find(".")]
        findWith = detail[detail.find(".")+1:len(detail)]
        nextPos = 0
        tagPos1 = self.content.find("<"+tagElement, nextPos)
        tagPos2 = self.content.find(">", tagPos1)
        palTag = self.content[tagPos1:tagPos2+1]
        checkPos = tagPos2
        tailPos = self.content.find("</"+tagElement+">", checkPos)
        while(self.content.find("<"+tagElement, nextPos) != -1):
            if(palTag.find(findType+"="+"'"+findWith+"'") != -1 or palTag.find(findType+"="+'"'+findWith+'"') != -1):
                if(self.content[checkPos:tailPos].find("<"+tagElement) != -1):
                    checkPos = self.content[checkPos:tailPos].find(
                        "<"+tagElement, checkPos+1)
                    tailPos = self.content.find("</"+tagElement+">", tailPos+1)
                else:
                    palInside = self.content[tagPos2 +
                                             1:self.content.find(">", tailPos)+1]
                    palContent = self.content[tagPos1:tailPos +
                                              len(tagElement)+3]
                    palSiblingContent = self.content[tailPos+len(tagElement)+3:len(self.content)]                       
                    palList.append(PalElement(
                    palContent, palTag, palInside, palSiblingContent))
                    nextPos = tagPos2
                    tagPos1 = self.content.find("<"+tagElement, nextPos)
                    tagPos2 = self.content.find(">", tagPos1)
                    palTag = self.content[tagPos1:tagPos2+1]
                    checkPos = tagPos2
                    tailPos = self.content.find("</"+tagElement+">", checkPos)
            else:
                nextPos = tagPos2
                tagPos1 = self.content.find("<"+tagElement, nextPos)
                tagPos2 = self.content.find(">", tagPos1)
                palTag = self.content[tagPos1:tagPos2+1]
                checkPos = tagPos2
                tailPos = self.content.find("</"+tagElement+">", checkPos)
        self.overList.append(palList)
        return self.overList[len(self.overList)-1]

    def find(self, tagElement: str):
        palList = []
        nextPos = 0
        tagPos1 = self.content.find("<"+tagElement, nextPos)
        tagPos2 = self.content.find(">", tagPos1)
        palTag = self.content[tagPos1:tagPos2+1]
        checkPos = tagPos2
        tailPos = self.content.find("</"+tagElement+">", checkPos)
        while(self.content.find("<"+tagElement, nextPos) != -1):
            if(self.content[checkPos:tailPos].find("<"+tagElement) != -1):
                checkPos = self.content[checkPos:tailPos].find(
                    "<"+tagElement, checkPos+1)
                tailPos = self.content.find("</"+tagElement+">", tailPos+1)
            else:
                palInside = self.content[tagPos2 +
                                         1:self.content.find(">", tailPos)+1]
                palContent = self.content[tagPos1:tailPos+len(tagElement)+3] 
                palSiblingContent = self.content[tailPos+len(tagElement)+3:len(self.content)]                       
                palList.append(PalElement(
                    palContent, palTag, palInside, palSiblingContent))
                nextPos = tagPos2
                tagPos1 = self.content.find("<"+tagElement, nextPos)
                tagPos2 = self.content.find(">", tagPos1)
                palTag = self.content[tagPos1:tagPos2+1]
                checkPos = tagPos2
                tailPos = self.content.find("</"+tagElement+">", checkPos)

        self.overList.append(palList)
        return self.overList[len(self.overList)-1]
