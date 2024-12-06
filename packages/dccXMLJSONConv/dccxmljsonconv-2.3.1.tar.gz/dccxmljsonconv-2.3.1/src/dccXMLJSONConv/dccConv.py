#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Created on Sun Dec 12 17:02:59 2021 by Thomas Bruns
# This file is part of dcc-xmljsonconv (https://gitlab1.ptb.de/digitaldynamicmeasurement/dcc_XMLJSONConv)
# Copyright 2024 [Thomas Bruns (PTB), Benedikt Seeger(PTB), Vanessa Stehr(PTB)]
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from jinja2 import Template
import lxml.etree as ElementTree
import json
import os
import warnings
import pathlib
from functools import reduce 
import operator

TRACBACKLENGTH = 40

try:
    script_location = pathlib.Path(__file__).resolve()
    path = script_location.parent / 'data' / 'listDCCElements.json'
    listDCCElements = json.load(open(path, 'r'))
except:
    # Path to the directory containing the script
    # Get the absolute path to the directory where the script is located
    script_location = pathlib.Path(__file__).resolve().parent.parent

    # Construct the path to the data file
    data_file_path = script_location.parent / 'data' / 'listDCCElements.json'
    listDCCElements = json.load(open(data_file_path, 'r'))

listElementsNames = listDCCElements['listTypeElements']
repeatedFieldNames = listDCCElements['repeatedFieldNames']
spaceSeperatedFieldNamesAndTypes = listDCCElements['spaceSeperatedFieldNamesAndTypes']

class dcc():
    def __init__(self):
        self.root = None
        self.xml = ""
        self.json = ""
        self.nsmap = {}
        self.dic = {}
        self.parsingErrorInRecursionOccured = False  # flag if an error occurred within the recursive parsing
        self.TpComment = Template("\n<!-- {{ comment }} -->\n")  # Jinja template for a comment
        self.TpTag = Template("<{{ name }}{{attributes}}>{{ text }}</{{ name }}>\n")  # jinja template for a tag

    # --------------- generate a dict from (DCC)-XML ---------------
    def read_dcc_file(self, filename):
        """
        Reads the XML-file in filename into self.xml

        Parameters
        ----------
        filename : existing filepath
            Path to an existing XML-file

        Returns
        -------

        """
        print("read_dcc_file:... %s" % filename)
        with open(filename, "r") as file:
            self.xml = file.read()
        return

    def read_dcc_string(self, xml):
        """
        Setter method takes xml and puts it into self.xml

        Parameters
        ----------
        xml : string
            xml-document as string

        Returns
        -------

        """
        self.xml = xml
        return

    def read_json_file(self, filename):
        """
        Reads the JSON-file in filename into self.json

        Parameters
        ----------
        filename : existing filepath
            Path to an existing XML-file

        Returns
        -------

        """
        print("read_json_file:... %s" % filename)
        with open(filename, "r") as file:
            self.json = file.read()
        return

    def read_json_string(self, json):
        """
        Setter method takes xml and puts it into self.xml

        Parameters
        ----------
        xml : string
            xml-document as string

        Returns
        -------

        """
        self.json = json
        return

    def __update_tree__(self):

        """
        updates self.tree (lxml structure) from self.xml
        sets self.root
        sets self.nsmap

        Parameters
        ----------
        xml : string
            xml-document as string

        Returns
        -------

        """
        try:
            parser = ElementTree.XMLParser(recover=True)  # recover from bad characters.
            self.tree = ElementTree.fromstring(self.xml.encode(), parser=parser)  # encode->bytes necessary!
            if self.tree.nsmap:
                self.nsmap = self.tree.nsmap
            return
        except:
            print("dcc_stuff.__update_tree__() validation failed for given xml-string!")
            return

    def __tree2dict__(self, node):
        """
        traverses the XML-tree starting at the root element and transforms it into
        a python dict of dicts of dicts ...

        Parameters
        ----------
        root : lxml.etree Element (not necessarilly the root of the tree)
            The starting point of traversal. Get it like:

            import lxml.etree as ElementTree
            with open(filename,"r") as file:
                tree = ElementTree.parse(file)
            root = tree.getroot()

        Returns
        -------
        ret : dict
            the information from the xml in a dict of dicts
        forceArrayTopLevel : bool default=False
            flag if the top level is forced to be an array
            the parser found a repeated field on the actual level so the top level must be an array
        """
        dc = {}
        forceArray = False
        forceArrayTopLevel = False
        if node.nsmap and (node == self.tree):
            tmp = {"@xmlns:" + key: node.nsmap[key] for key in node.nsmap}
            self.merge_dicts(dc, tmp)

        if node.attrib:
            tmp = {"@" + self.ns_clean(key): node.attrib[key] for key in node.attrib}
            self.merge_dicts(dc, tmp)

        if isinstance(node, ElementTree._Comment):
            tmp = json.loads(json.dumps({"@_Comment": node.text}))
            self.merge_dicts(dc, tmp)
            return (dc,False)

        elif isinstance(node, ElementTree._Element):

            if node.text:
                if not node.text.isspace():
                    self.merge_dicts(dc, json.loads(json.dumps({"#text": node.text})))
            if node.tag.split('}')[-1].split(':')[-1] in listElementsNames:  # check if this Element is a listType
                # print("Found listType: " + node.tag)
                forceArray = True  # set flag for listForcing
            if node.tag.split('}')[-1].split(':')[-1] in repeatedFieldNames:  # check if this Element is a repeatable field
                forceArrayTopLevel = True  # set flag to force the top level to be an array
            if node.tag.split('}')[-1].split(':')[-1] in spaceSeperatedFieldNamesAndTypes:
                try:
                    splitted = node.text.split()
                except AttributeError as e:
                    if not node.text:
                        e.add_note("This probably occurred due to an empty element in the XML.")
                    raise e
                if "" in splitted:
                    warnings.warn("Space separated field contains excessive white space characters. This is not allowed, the spaces have been stripped!")
                splitted = ' '.join(splitted).split()
                
                # try:
                #     if node.text[0]== ' ' or node.text[-1]== ' ':
                #         splitted = node.text.strip().split(' ')
                #         warnings.warn("Space separated field is starting or ending with an Space this is not allowed, the spaces have been stripped!")
                #     else:
                #         splitted = node.text.split(' ')
                # except:
                #     print("DEBUG")
                if spaceSeperatedFieldNamesAndTypes[node.tag.split('}')[-1].split(':')[-1]]=='float':                  
                    splitted=list(map(float, splitted))
                self.merge_dicts(dc, json.loads(json.dumps({"#list": splitted})))

            if len(node) > 0:
                for i, child in enumerate(node):
                    cildresult, forceArrayForMemberFlag = self.__tree2dict__(child)
                    self.merge_dicts(dc, cildresult, forceArray=forceArray or forceArrayForMemberFlag)

            return {self.ns_clean(str(node.tag)): dc}, forceArrayTopLevel

    def xml2dict(self):
        """
        takes the self.xml attribute and by using lxml converts it into
        self.tree and by by using self.__tree2dict__ fills the
        self.dic attribute

        Parameters
        ----------
        None

        Returns
        -------
        None

        """

        if self.xml == "":
            print("dcc_stuff.xml2dict: ERROR xml-string is empty!")
            return {}
        else:
            self.__update_tree__()  # update the xml-tree from self.xml
            self.dic, retunFlag = self.__tree2dict__(self.tree)  # pares the tree from root
            return

    def dict2json(self):
        """
        takes self.dic and generates self.json as json-textstring

        Parameters
        ----------
        xml : string
            xml-document as string

        Returns
        -------

        """

        try:
            self.json = json.dumps(self.dic)
        except Exception:
            print("<ERROR>dcc.dict2json failed in json.dumps()</ERROR>")

    def get_json(self, beauty=True, indent=4):
        """
        returns the (beautyfied) json string of self.

        Parameters
        ----------
        beauty : bool (True)
            sets whether the string is beautyfied (for humans)

        indent : integer
            sets the indentation width for beautification

        Returns
        -------
        json-string

        """

        self.dict2json()  # update the json from self.dic
        if beauty:
            ret = json.dumps(self.dic, indent=indent)  # dump the dict to string
        else:
            ret = json.dumps(self.dic)
        return ret

    def ns_clean(self, tag):
        """
        shortens namespace information in xml-tags

        Parameters
        ----------
        tag : string
            the tag that has to be checked for know namespaces

        Returns
        -------
        tag : string
            the shortened version of the tag.

        """
        for k, v in self.nsmap.items():  # check for the namespaces in nsmap
            if "{" + str(v) + "}" in tag:
                tag = tag.replace("{" + str(v) + "}", k + ":")
                break
        return tag

    def merge_dicts(self, d1, d2, forceArray=False):
        """
        merge dict d2 into d1 without loosing entries in either of both.
        If a key of d2 already exists in d1,
        make the element of d1 an array if neccessary and append the
        value from d2 to that array

        Parameters
        ----------
        d1 : dict
            target of the merger
        d2 : dict
            source of the merger
        forceArray : bool (False)
            sets whether d1 is forced to be an array.
            The default is False.
        Returns
        -------
        d1 : dict
            merged dict

        """
        for k, v in d2.items():  # iterate of d2
            if k in d1:  # emergency array check if keys are doubled it must be an array even if forceArray is False

                if isinstance(d1[k], list):
                    d1[k].append(v)
                else:
                    warnings.warn(
                        str("Key " + str(k) + " is doubled in dict1 and dict2. It will be forced to be an array!"),
                        RuntimeWarning)
                    d1[k] = [d1[k], v]
            elif forceArray:
                d1[k] = [v]  # convert v to list this is the effect of forceArray
            else:
                d1[k] = v
        return d1

    # ------------ Generate XML from dict ---------
    def __dict2attrib__(self, value):
        attrib = ""
        if isinstance(value, dict):
            for k, v in value.items():
                if self.__isattribute__(k):
                    if v[0] != '"':
                        v = '"' + v
                    if v[-1] != '"':
                        v = v + '"'
                    attrib = attrib + (" %s=%s" % (k[1:], v))  # index 1 removes leading @
        if isinstance(value, list):
            for v in value:
                attrib += self.dict2attrib(v)
        return attrib

    def __isattribute__(self, key):
        """
        Checks whether the key is meant to indicate an attribute
        i.e. the first character is "@"

        Parameters
        ----------
        key : dict key
            The Key which is checked for being an attribute

        Returns
        -------
        ret : boolean
            True="the key is an attribute", False="the key is a tag"

        """
        # ret = (key in ["schemaVersion","schemaLocation","lang","id","refType"]) or ("xmlns" in key)
        ret = (str(key)[0] == "@" and str(key) != "@_Comment")
        return ret

    def __dict2text__(self, value):
        # search for "#text" keys and return the value
        text = ""
        if isinstance(value, dict):
            for k, v in value.items():
                if k[0] == "#":
                    text = v

        return text

    def json2dict(self):
        """
        Takes the self.json attribute and parses it to a dict
        sets self.dic to the resulting dict.

        Parameters
        ----------

        Returns
        -------

        """
        self.dic = json.loads(self.json)
        return

    def __dict2xml__(self, dic):
        """
        Takes the dict representation and generates an xml-string
        Operates recursive and return the string, therefore.
        (it does not set self.xml!)

        Parameters
        ----------
        dic : dict with the dcc information

        Returns
        -------

        """

        attribs = ""  # collect the attributes for this tag
        ret = ""  # collect the text in this tag

        try:
            if '#text' in dic and '#list' in dic:
                warnings.warn("Both #text and #list are present in the same tag. #List will be ignored", RuntimeWarning)
                del dic['#list']
            if '#list' in dic and not '#text' in dic:
                warnings.warn("Only #list is present in the tag. #List will be converted to text", RuntimeWarning)
                dic['#text'] = " ".join(str(item) for item in dic['#list'])
                del dic['#list']
            for k, v in dic.items():
                if isinstance(v, list):  # repeated tags of same type
                    for item in v:  # unroll
                        ret += self.__dict2xml__({k: item})  # process each as single dict
                else:
                    if k == "@_Comment":
                        ret += self.TpComment.render(comment=v) + "\n"  # Exceptional case for comments
                    elif k == "#text":
                        ret = str(v)  # exceptional case for the tag-content
                    elif k == "#list":
                        pass # TODO change parsing to use list if it exists instead of #text
                    else:  # remaining are attributes and usual tags
                        attribs = self.__dict2attrib__(v)  # collect all attributes
                        if k[0] == "@":
                            pass  # ignore attributes here
                        else:  # work on the single tag with template
                            ret += "\n" + self.TpTag.render(name=k,
                                                            attributes=attribs,
                                                            text=self.__dict2xml__(v)) + "\n"
                # print(ret)  debugPrint   add option for that to reactivate
        # Exception Handling
        except Exception as exceptInst:
            if not self.parsingErrorInRecursionOccured:
                # OK we are at the cause of the Error
                self.firstParsingError = str(exceptInst)  # save the fist error Message
                # create an list with the first chars of the dict we ware parsing at the moment
                if len(str(dic)) > TRACBACKLENGTH:
                    self.parsingErrorTraceBack = [str(dic)[:TRACBACKLENGTH].replace('\n', '\\n')]
                else:
                    self.parsingErrorTraceBack = [str(dic).replace('\n', '\\n')]
                self.parsingErrorInRecursionOccured = True
            else:
                # we had an error before so we don't want the error message but the first chars of the dict at this recursion level
                if len(str(dic)) > TRACBACKLENGTH:
                    self.parsingErrorTraceBack.append(str(dic)[:TRACBACKLENGTH].replace('\n', '\\n'))
                else:
                    self.parsingErrorTraceBack.append(str(dic).replace('\n', '\\n'))
            raise exceptInst
        # End Exception Handling
        return ret

    def dict2xml(self):
        """
        Takes the self.dic attribute and generates an xml-string
        and sets it in self.xml
        (calls the recursive privat version __dict2xml__)

        Parameters
        ----------

        Returns
        -------

        """
        xml = self.__dict2xml__(self.dic)  # the private method runs recursively!
        # now remove blank lines in xml
        self.xml = os.linesep.join([s for s in xml.splitlines() if s.strip()])
        return

    def get_xml(self, beauty=True):
        """
        returns the (beautyfied) xml string of self.

        Parameters
        ----------
        beauty : bool (True)
            sets whether the string is beautyfied (for humans)

        Returns
        -------
        xml-string

        """
        self.__update_tree__()  # update the tree from the current self.xml
        try:
            ret = ElementTree.tostring(self.tree, pretty_print=beauty, encoding="unicode")

        except:
            print("<ERROR>dcc_stuff.get_xml() failed </ERROR>")
            ret = self.xml
        return ret


def XMLToJson(xml):
    dccInst = dcc()
    if isinstance(xml, str):
        dccInst.read_dcc_string(xml)
    else:
        dccInst.read_dcc_string(str(xml))
    dccInst.xml2dict()
    return json.loads(dccInst.get_json())


def JSONToXML(jsonData):
    dccInst = dcc()
    if isinstance(jsonData, str):
        dccInst.read_json_string(jsonData)
    elif isinstance(jsonData, dict):
        dccInst.read_json_string(json.dumps(jsonData))
    else:
        dccInst.read_json_string(str(jsonData))
    dccInst.json2dict()
    dccInst.dict2xml()
    return dccInst.get_xml()

def beautify_xml(text):
    parser = ElementTree.XMLParser(remove_blank_text=True, ns_clean=True)
    test = text.replace("\\\"", "\"")
    # print(test)
    try:
        tree = ElementTree.fromstring(test, parser=parser)
        ret = ElementTree.tostring(tree, pretty_print=True, encoding="unicode")
    except:
        ret = "<ERROR>dcc_stuff:beautyfy_xml failed </ERROR>"
    return ret

#TODO Add Unit Test
def getFromDict(dataDict, mapList):
     return reduce(operator.getitem, mapList, dataDict) 
     
#TODO Add Unit Test
def setInDict(dataDict, mapList, value): 
    getFromDict(dataDict, mapList[:-1])[mapList[-1]] = value