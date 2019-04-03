# Author : Mohammadirfan H Yalabunachi
# Date : 09-03-2019
# Spell Check Functionality #

import datetime
from enum import Enum
import io
import os
from google.cloud import vision
from google.cloud.vision import types
from google.oauth2 import service_account
from PIL import Image, ImageDraw, ImageOps
import base64
import random
# from SuperPowers import SuperPowers
from nltk import word_tokenize
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')

# from app import serverLog

# from PDF_Image_Convert_thread import PDF_Image_Convert
from PDF_Image_Convert_thread import PDF_Image_Convert
from cropimage import CropImg

# API
from flask import Flask, request, render_template, send_file, send_from_directory, jsonify
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename
import shutil

#Spell#
import http.client
import urllib.parse
import json
from collections import namedtuple
import tempfile
import re

# Border
import numpy as np
import cv2
import pdf2image
import img2pdf

cwd = os.getcwd()
# Spell check
# Key1: bac99dd94f2f4ed49ff9e829fd288cf7
# Key2: 52e36dde3241412a8f5b53dca7534b32

key = "bac99dd94f2f4ed49ff9e829fd288cf7"
host = "api.cognitive.microsoft.com"
path = "/bing/v7.0/spellcheck?"
# params = "mkt=en-us&mode=proof"
headers = {"Ocp-Apim-Subscription-Key": key,
    "Content-Type": "application/x-www-form-urlencoded"}


class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5


class SpellCheckCntroller():

    def convert_pdf_images(self, filename, temp_dir,language):
        print("convert_pdf_images .... ",filename)
        images = pdf2image.convert_from_path(filename, thread_count=3, dpi=150)
        count = 1
        subfolder_names = ["input_images", "output_images"]
        pagewise_result = []
        opImges = []
        total_result = {}
        total_spell_mis = 0
        for subfolder_name in subfolder_names:
            os.makedirs(os.path.join(temp_dir, subfolder_name))
        for page in images:
            print("image detail ", page.size)
            page.save(os.path.join(
                (os.path.join(temp_dir, "input_images")), ("temp"+str(count)+".jpg")), "png")
            pagewise_result.append(self.render_doc_text(os.path.join(temp_dir, "input_images"), os.path.join(
                temp_dir, "output_images"), ("temp"+str(count)+".jpg"), count,page.size,language))
            opImges.append(os.path.join(os.path.join(
                temp_dir, "output_images"), ("output_temp"+str(count)+".jpg")))
            count += 1
        pagewise_result_fil = []
        for pr in pagewise_result:
            for p in pr:
                if(p["spell_mis_count"] > 0):
                    pagewise_result_fil.append(pr)
                    # print(index)

                total_spell_mis += p["spell_mis_count"]

        # print(len(pagewise_result_fil))
        total_result["total_pages"] = len(pagewise_result)
        total_result["result"] = pagewise_result_fil
        # print(pagewise_result[0][0]["spell_mis_count"])

        total_result["total_spell_mistakes"] = total_spell_mis
        total_result["pth"] = opImges
        return total_result

    def render_doc_text(self, in_dir, out_dir, filein, pagenumber,imgSize,language):
        # bounds = exctract_text_from_image(filein, FeatureType.WORD,in_dir,out_dir,pagenumber)
        print("convert_pdf_images")
        result = self.exctract_text_from_image(
            filein, FeatureType.WORD, in_dir, out_dir, pagenumber,imgSize,language)
        self.draw_boxes(filein, result[1], in_dir, out_dir)
        # print(ipth)
        return result[0]

    def exctract_text_from_image(self, image_file, feature, in_dir, out_dir, pagenumber,imgSize,language):
        """Returns Final requirement"""
        
        print("exctract_text_from_image")
        only_spell_mis_words_list = []
        with io.open(os.path.join(in_dir, image_file), "rb") as image_file:
            content = image_file.read()
        image = types.Image(content=content)
        response_with_text = client.document_text_detection(image=image)
        document = response_with_text.full_text_annotation
        # Filtering text
        #filtered_text = document.text  
        # print("Before perform_spell_check")

        only_spell_mis_words_list = self.perform_spell_check(document.text,language)
        wordswithbox=self.getWordsBySymbols(document)
        # print(only_spell_mis_words_list)
        # wordswithbox=[]
        return self.get_document_bounds(document,wordswithbox, self.formatWords(only_spell_mis_words_list), feature, out_dir, pagenumber,imgSize)



    def filter_text(self, extracted_text): 

        text1 = re.sub("[0-9]", " ", extracted_text)
        return text1
        # return extracted_text 

    def formatWords(self,only_spell_mis_words_list):
        newlist=[]
        for w in only_spell_mis_words_list:
            # print(w)
            if(len(tokenizer.tokenize(w["wrongWords"]))>1):
                for s in tokenizer.tokenize(w["wrongWords"]):
                    if(len(s)>1):   
                        newlist.append({"wrongWords":s.strip(),"pos":w["pos"]})
            else:

                newlist.append(w)
             
        # print(newlist)
        return newlist
    # Spell check code API

    def perform_spell_check(self, textpage,language):
        try:
            # Check for more than 10000 character hitting to the Spell check api
            print("Performing spell check on pdf with language",language)
            text_as_list = self.slice_text(textpage)
            only_spell_mis_words_list = []
            # params = "mkt=en-us&mode=proof"
            params = "mkt="+language+"&mode=proof"

            for text in text_as_list:
                text = text.replace("\n", " ")
                data = {"text": text[0:9900]}
                conn = http.client.HTTPSConnection(host)
                body = urllib.parse.urlencode(data)
                conn.request("POST", path + params, body, headers)
                response = conn.getresponse()
                output = json.dumps(json.loads(response.read()), indent=2)
                spell_mis = json.loads(output)
                if spell_mis["flaggedTokens"] is not 0:
                    for mws in spell_mis["flaggedTokens"]:
                        only_spell_mis_words_list.append({"wrongWords":mws["token"],"pos":mws["offset"]})
                    print(only_spell_mis_words_list)
                return only_spell_mis_words_list
        except Exception as err:
            print(444)
            print(type(err).__name__, err)

    def get_document_bounds(self, document, wordwithbox,spell_mistakes, feature, out_dir, pagenumber,imgSize):
        """Returns document bounds given an image."""
        print("get_document_bounds")
        bounds = []
        words_with_bounds = []
        metadata = []
        result = []
        # Collect specified feature bounds by enumerating all document features
        print(spell_mistakes)
        if spell_mistakes:
            
            for w in wordwithbox[1]: 
                # print(w["word"].strip() +"------> "+str(w["wordindex"])) 
                for msw in spell_mistakes:
                    if(msw["wrongWords"].strip() == w["word"].strip() ):

                        if(abs(w["wordindex"]-msw['pos'])<5):
                            bounds.append(w["bondig_boxes"]) 
                            words_with_bounds.append({"word":msw["wrongWords"],"bounds":self.boxes_to_obj(w["bondig_boxes"])})
                            # words_with_bounds.append(msw)
 
 
        metadata.append({"page_number":pagenumber,"size":imgSize,"spell_mis_count":len(spell_mistakes),"spell_mistakes":words_with_bounds,"words":len(wordwithbox[0])})
        result.append(metadata)
        result.append(bounds)
        result.append(len(spell_mistakes))
        # print(json.dumps(metadata,indent=2))
        return result 

    def getWordsBySymbols(self, document):
        wds = []
        words_with_bounds = []
        i=0
        start=0
        # bds = []
        cretedtext=''
        txt=document.text
        # print(document)
        for page in document.pages:
            for block in page.blocks:
                for paragraph in block.paragraphs:
                    for word in paragraph.words:
                        new_word = ""
                        
                        for symbol in word.symbols:
                            # if(symbol.property.detected_break.type=='HYPHEN'):
                            #     print(symbol.property.detected_break.type)
                            # if(symbol.property.detected_break.type=='SPACE'):
                            #     new_word += symbol.text+" "
                            # else:
                            if(symbol.property.detected_break.type<2):
                                new_word += symbol.text+" "*symbol.property.detected_break.type
                                # if(new_word=='ever'):
                                #     print(symbol)
                            # elif(new_word=="'"):
                            #     
                            else:
                                new_word += symbol.text+"\n"
                            # if(new_word=='ever'  or new_word=='lasting' ):
                            #     print(symbol)
                        # if(new_word=="'" or new_word=='ment'):
                        #     print(symbol)
                        cretedtext=cretedtext+new_word
                        # start=
                        ind=txt.index(new_word,start)
                        # print(txt.index(new_word,start))
                        if( (not new_word.isdigit()) or (not  new_word.isdecimal())):
                            words_with_bounds.append(
                                {
                                "word": ''.join([i for i in new_word if not i.isdigit()]),
                                "wordindex": txt.index(new_word,start),
                                'bondig_boxes': (word.bounding_box)}
                                )
                        else:
                            words_with_bounds.append(
                                {
                                "word": new_word,
                                "wordindex": txt.index(new_word,start),
                                'bondig_boxes': (word.bounding_box)}
                                )

                        # bds.append(word.bounding_box)
                        wds.append(new_word)
                        i=i+1
                        start=start+len(new_word)
        # print(document.text)
        return wds, words_with_bounds,cretedtext
 
    def draw_boxes(self,image_name, bounds, in_dir, out_dir):
        try:
            print("draw_boxes")
            """Draw a border around the image using the hints in the vector list."""
            image = cv2.imread(os.path.join(in_dir, image_name), -1)
            ipth = os.path.join(out_dir, ("output_"+image_name))
            for bound in bounds:
                pts = np.array([[
                    bound.vertices[0].x-3, bound.vertices[0].y],
                    [bound.vertices[1].x+3, bound.vertices[1].y, ],
                    [bound.vertices[2].x+3, bound.vertices[2].y, ],
                    [bound.vertices[3].x-3, bound.vertices[3].y]], np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(image, [pts], True, (0, 0, 254), 3)
            # opImges.append()
            cv2.imwrite(ipth, image)

        except Exception as err:
            print(555)
            print("Error in  cv2.imwrite")
            print("error : ", type(err).__name__, err)
        # return ipth

    def pdfConverter(self,img_path, pdf_path):
        try:
            with open(pdf_path, "wb") as f:
                f.write(img2pdf.convert(img_path))
        except Exception as err:
            print(333)
            print("Error while converting images to pdf")
            print("error : ",type(err).__name__, err)
        

    # Slice the text
    def slice_text(self,words):
        print("slice_text")
        text_by_slices = []
        print(' slice_text ',len(words))
        if words.strip():
            text_len = len(words)
            # print(text_len)
            itrt = int(text_len / 9900)
            limit = 30
            count = 9900*itrt
            num = []
            for c in range(0, itrt):
                while count >= limit:
                    if words[count] == " ":
                        num.append(count)
                        break
                    count -= 1

                count = int(count-9900)

            num.append(0)
            num.insert(0, text_len)

            for c in range(0, len(num)):
                words[num[len(num)-1-c]: num[len(num)-2-c]].strip()
                text_by_slices.append(
                    words[num[len(num)-1-c]: num[len(num)-2-c]].strip())

        del text_by_slices[-1]
        # print("LLLLLLLLLLL ",len(text_by_slices))
        return (text_by_slices)



    def boxes_to_obj(self,bound):
       
        return {'x1': bound.vertices[0].x ,'x2':bound.vertices[1].x  ,
                    'y1':bound.vertices[0].y  ,'y2':bound.vertices[2].y  }



    # def boxes_to_obj(self,bound):
    #     vertices=[]
    #     for i in range(4):
    #         vertices.append({"x":bound.vertices[i].x,"y":bound.vertices[i].y})
    #     return vertices
