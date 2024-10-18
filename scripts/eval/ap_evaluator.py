import os, sys

def add_path(path):
    if path not in sys.path:
        sys.path.insert(0, path)

currentPath = os.path.dirname(os.path.realpath(__file__))

libPath = os.path.join(currentPath, 'aplib')
add_path(libPath)

from BoundingBox import BoundingBox
from BoundingBoxes import BoundingBoxes
from Evaluator import *
from utils import *


class APEvaluator:
    def __init__(self):
        self.all_boundingboxes=BoundingBoxes()
        

    def add_box(self, nameOfImage, x, y, w, h, confidence, typpe):

        if typpe=="PRED":
            predType=BBType.Detected
        else:
            predType=BBType.GroundTruth

        idClass=0

        bb = BoundingBox(nameOfImage, idClass,x,y,w,h,CoordinatesType.Absolute, (200,200), predType, confidence, format=BBFormat.XYX2Y2)
        return bb

    def evaluate_all(self):
        evaluator = Evaluator()
        metricsPerClass = evaluator.GetPascalVOCMetrics(
            self.all_boundingboxes,  # Object containing all bounding boxes (ground truths and detections)
            IOUThreshold=0.5,  # IOU threshold
            method=MethodAveragePrecision.EveryPointInterpolation)
        for mc in metricsPerClass:
            average_precision = mc['AP']
            print("ALL AP: %.3f" % average_precision)

    def add_mov(self, boxes, mov):

        mov_boxes=BoundingBoxes()
        
        for name, x1, y1, x2, y2, conf, cat in boxes:
            self.all_boundingboxes.addBoundingBox(self.add_box(name, x1, y1, x2, y2, conf, cat))
            mov_boxes.addBoundingBox(self.add_box(name, x1, y1, x2, y2, conf, cat))

        mov_evaluator = Evaluator()
                
        metricsPerClass = mov_evaluator.GetPascalVOCMetrics(
        mov_boxes,  # Object containing all bounding boxes (ground truths and detections)
        IOUThreshold=0.5,  # IOU threshold
        method=MethodAveragePrecision.EveryPointInterpolation)
        for mc in metricsPerClass:
            average_precision = mc['AP']
            print("%.3f\t%s\tAP\tMOV" % (average_precision, mov))



