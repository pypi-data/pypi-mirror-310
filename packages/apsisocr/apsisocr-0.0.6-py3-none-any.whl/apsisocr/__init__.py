#-*- coding: utf-8 -*-
import warnings
warnings.filterwarnings('ignore')
from .ocr import ApsisOCR,ApsisNet,SVTRLCNet,PaddleDBNet,DenseNet121BnEnClassifier
from .base import BaseOCR 
from .bnocr import ApsisBNOCR 