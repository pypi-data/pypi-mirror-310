#-*- coding: utf-8 -*-
"""
@author:MD.Nazmuddoha Ansary
"""
from __future__ import print_function
import warnings
warnings.filterwarnings('ignore')
#-------------------------
# imports
#-------------------------
from typing import Union
from .utils import localize_box,LOG_INFO
from .apsisnet import ApsisNet
from .paddledbnet import PaddleDBNet
import cv2
import copy
import pandas as pd
import numpy as np
#-------------------------
# class
#------------------------
class ApsisBNBaseOCR(object):
    """
    ApsisBNOCR processes images for Bangla Optical Character Recognition (OCR) using
    models for Bangla text recognition and a text detector

    Attributes:
        bn_rec (ApsisNet): Instance of ApsisNet for Bangla text recognition.
        detector (PaddleDBNet): Instance of PaddleDBNet for text detection.
    """

    def __init__(self) -> None:
        """
        Initialize ApsisOCR object with models for Bangla recognition and a text detector
        """        
        self.bn_rec=ApsisNet()
        LOG_INFO("Loaded Bangla Model")
        self.detector=PaddleDBNet(load_line_model=True)        
        LOG_INFO("Loaded Paddle detector")
        
    
    def __call__(self, img: Union[str,np.ndarray]) -> dict:
        """
        Perform OCR on an image.

        Args:
            img (Union[str,np.ndarray]): Path to the image file or the numpy array image

        Returns:
            dict: OCR results containing recognized text and associated information. The dictionary has the following structre
                  {
                    "text" : multiline text with newline separators
                    "result" : list a dictionaries that contains the following structre:
                              {
                                "line_no" : the line number of the word
                                "word_no" : the word number in the line 
                                "poly"    : the four point polygonal bounding box of the word in the image
                                "text"    : the recognized text 
                              }
                  }
        """  
        result=[]
        # -----------------------start-----------------------
        if type(img)==str:
            img=cv2.imread(img)
            img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        
        word_boxes=self.detector.get_word_boxes(img)
        crops=self.detector.get_crops(img,word_boxes)
        bn_text=self.bn_rec.infer(crops)
        df=pd.DataFrame({"poly":word_boxes,"text":bn_text})
        # format
        for idx in range(len(df)):
            data={}
            poly_res=  []
            poly    =  df.iloc[idx,0]
            poly    = np.array(poly).reshape(4,2)
            for pair in poly:
                _pair=[float(pair[0]),float(pair[1])]
                poly_res.append(_pair)
            
            data["poly"]   =poly_res
            data["text"]   =df.iloc[idx,-1]
            result.append(data)
        return result