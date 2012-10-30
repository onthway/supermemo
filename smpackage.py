#!/usr/bin/python
# coding: UTF-8
import struct
import zlib
import xpath
import xml.dom.minidom

class smPackage:
    headerMap = {"sign" : (0, 8, "8s"),
                 "version" : (8, 10, "2s"),
                 "locked" : (10, 12, "H"),
                 "entry_offset" : (12, 16, "I"),
                 "name_offset" : (16, 20, "I")}
    headerMapNew = {"sign" : (0, 8, "8s"),
                    "version" : (8, 10, "2s"),
                    "locked" : (10, 12, "H"),
                    "entry_offset" : (26, 30, "I"),
                    "name_offset" : (30, 34, "I")}
    def __init__(self, path):
        self.data = {}
        try:
            self.stream = open(path, "rb")
            header_data = self.stream.read(34)
            flag=self.stream.read(8)
            if flag == "DataChnk":
                if header_data[:8] == "-SMArch-":
                    for tag, (start, end, t) in self.headerMap.items():
                        self.data[tag], = struct.unpack(t, header_data[start:end])
                    self.__read_entries()
                    self.__read_entry_name()
            else
                if header_data[:8] == "-SMArch-":
                    for tag, (start, end, t) in self.headerMap.items():
                        self.data[tag], = struct.unpack(t, header_data[start:end])
                    self.__read_entries()
                    self.__read_entry_name()
            
        except IOError:
            print "IOError"
            pass
    def __read_entries(self):
        entry_offset = self.data["entry_offset"]
        self.stream.seek(entry_offset)
        self.entry_count, = struct.unpack("I", self.stream.read(4))
        self.entries = []
        for i in range(self.entry_count):
            entry = {}
            entry["name_offset"], = struct.unpack("I", self.stream.read(4))
            entry["name_len"], = struct.unpack("H", self.stream.read(2))
            entry["mode"], = struct.unpack("H", self.stream.read(2))
            entry["data_offset"], = struct.unpack("I", self.stream.read(4))
            entry["data_size"], = struct.unpack("I", self.stream.read(4))
            self.entries.append(entry)
    def __read_entry_name(self):
        self.files = {}
        #四个字节itme名称长度，3个字节变长，3个字节对于不同的文件会发生变化
        self.stream.seek(self.data["name_offset"]+7)
        #self.stream.seek(self.data["name_offset"])
        #name_chunk_size, = struct.unpack("I", self.stream.read(4))
        #print name_chunk_size
        #self.stream.seek(-name_chunk_size, 2)
        name_chunk_begin = self.stream.tell()
        for entry in self.entries:
            self.stream.seek(name_chunk_begin + entry["name_offset"])
            entry_name = self.stream.read(entry["name_len"])
            entry["name"] = entry_name
            self.files[entry_name] = entry
    def read_file(self, name):
        if self.files.has_key(name):
            entry = self.files[name]
            self.stream.seek(entry["data_offset"])
            data = self.stream.read(entry["data_size"])
            if entry["mode"] == 1:
                data = zlib.decompress(data, -15)
            return data
    def get_xpath_word(self):  
        doc = xml.dom.minidom.parse(".\\course.xml")
        #寻找单词所在条目，id对应item名称，keywords对应单词名称
        for node in xpath.find("//element[@subtype = $subtype]", doc, subtype = "1"):
            #print (node, node.tagName, node.getAttribute("keywords"), node.getAttribute("id"))
            number=node.getAttribute("id")
            wordname=node.getAttribute("keywords")
            count=len(number)
            i=0
            while i < (5-count):
                number='0'+number
                i+=1
            entryname="media/"+number+"b.png"
            filename=wordname+".png"
            filename = filename.replace("/", "_")
            filename = filename.replace("?", "")
            if self.files.has_key(entryname):
                print (entryname+"==>"+filename)
                f = open(filename, "wb")
                f.write(self.read_file(entryname))
                f.close()
            entryname="media/"+number+"a.mp3"
            filename=wordname+".mp3"
            filename = filename.replace("/", "_")
            filename = filename.replace("?", "")
            if self.files.has_key(entryname):
                print (entryname+"==>"+filename)
                f = open(filename, "wb")
                f.write(self.read_file(entryname))
                f.close()
    def unpack(self):
        for entry in self.entries:
            #print entry["name"]
            filename = entry["name"].replace("/", "_")
            if filename.find('course.xml') == -1:
                #print filename
                continue
            print entry["name"]
            f = open(filename, "wb")
            f.write(self.read_file(entry["name"]))
            f.close()
            break
        self.get_xpath_word()
    def __getitem__(self, key): return self.data[key]
    def __setitem__(self, key, item): self.data[key] = item

if __name__ == "__main__":
    smpak = smPackage(".\\course.smpak")
    smpak.unpack()
    smpak = smPackage(".\\course.smdif2")
    smpak.unpack()


