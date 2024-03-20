from fontTools.pens.basePen import BasePen
from fontTools.pens.pointPen import AbstractPointPen  # from robofab.pens.pointPen import AbstractPointPen


def calcArea(points):
    l = len(points)
    area = 0
    for i in range(l):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % l]
        area += (x1 * y2) - (x2 * y1)
    return area / 2


class FilterPointPen(AbstractPointPen):

    def __init__(self, glyphSet=None):
        self.glyphSet = glyphSet
        self.contours = []
        self.components = []

    def beginPath(self, identifier=None):
        self.currentContour = []

    def addPoint(self, pt, segmentType=None, smooth=False, name=None, *args, **kwargs):
        point = {
            'pt': pt,
            'segmentType': segmentType,
            'smooth': smooth,
            'name': name
        }
        self.currentContour.append(point)

    def endPath(self):
        area = calcArea([point['pt'] for point in self.currentContour])
        if abs(area) >= 25:
            self.contours.append(self.currentContour)

    def addComponent(self, baseGlyphName, transformation, identifier=None):
        self.components.append((baseGlyphName, transformation))

    def extract(self, pointPen):
        for baseGlyphName, transformation in self.components:
            pointPen.addComponent(baseGlyphName, transformation)
        for contour in self.contours:
            pointPen.beginPath()
            for point in contour:
                pointPen.addPoint(**point)
            pointPen.endPath()


class CollectComponentsPen(BasePen):

    def __init__(self):
        self.components = []

    def ignore(self, *args):
        pass

    _moveTo = _lineTo = _curveToOne = endPath = closePath = ignore

    def addComponent(self, baseGlyphName, transformation):
        self.components.append((baseGlyphName, transformation))

    def get(self):
        return self.components


class CounterPen(BasePen):

    def __init__(self):
        self.pointCount = 0

    def _moveTo(self, pt):
        self.pointCount += 1

    def _lineTo(self, pt):
        self.pointCount += 1

    def _curveToOne(self, pt1, pt2, pt3):
        self.pointCount += 1

    def endPath(self):
        pass

    def closePath(self):
        pass

    def getPointCount(self):
        return self.pointCount

    def addComponent(self, baseGlyphName, transformation):
        pass
