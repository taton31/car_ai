import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "Point[x={}, y={}]".format(self.x, self.y)


class Segment:
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point

    def __str__(self):
        return "Segment[start = {}, end = {}".format(self.start_point, self.end_point)


class Vector:
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point
        self.x_component = end_point.x-start_point.x
        self.y_component = end_point.y - start_point.y

    def __str__(self):
        return "Vector [start = {}, end = {}]".format(self.start_point, self.end_point)


def vector_cross_product(vector_1, vector_2):
    return vector_1.x_component * vector_2.y_component - vector_2.x_component * vector_1.y_component


def range_intersection(range_1_s, range_1_e, range_2_s, range_2_e):
    if range_1_s > range_1_e:
        range_1_s, range_1_e = range_1_e, range_1_s
    if range_2_s > range_2_e:
        range_2_s, range_2_e = range_2_e, range_2_s
    return max(range_1_s, range_2_s) <= min(range_1_e, range_2_e)


def bounding_box(segment_1, segment_2):
    x1 = segment_1.start_point.x
    x2 = segment_1.end_point.x
    x3 = segment_2.start_point.x
    x4 = segment_2.end_point.x
    y1 = segment_1.start_point.y
    y2 = segment_1.end_point.y
    y3 = segment_2.start_point.y
    y4 = segment_2.end_point.y
    return range_intersection(x1, x2, x3, x4) and range_intersection(y1, y2, y3, y4)


def check_segment_intersection(segment_1, segment_2):
    if not bounding_box(segment_1, segment_2):
        return False
    vector_ab = Vector(segment_1.start_point, segment_1.end_point)
    vector_ac = Vector(segment_1.start_point, segment_2.start_point)
    vector_ad = Vector(segment_1.start_point, segment_2.end_point)

    vector_cd = Vector(segment_2.start_point, segment_2.end_point)
    vector_ca = Vector(segment_2.start_point, segment_1.start_point)
    vector_cb = Vector(segment_2.start_point, segment_1 .end_point)

    d1 = vector_cross_product(vector_ab, vector_ac)
    d2 = vector_cross_product(vector_ab, vector_ad)
    d3 = vector_cross_product(vector_cd, vector_ca)
    d4 = vector_cross_product(vector_cd, vector_cb)

    if ((d1 <= 0 and d2 >= 0) or (d1 >= 0 and d2 <= 0)) and ((d3 <= 0 and d4 >= 0) or (d3 >= 0 and d4 <= 0)):
        return intersection([segment_1.start_point.x, segment_1.start_point.y], [segment_1.end_point.x, segment_1.end_point.y], [segment_2.start_point.x, segment_2.start_point.y], [segment_2.end_point.x, segment_2.end_point.y])
    return False


def line_intersection(a, b):
    points = []
    goal_point=[0,0]
    dist = 2000
    for i in range(0,len(a)-1): 
        for j in range(0,len(b)-1):
            point_a = Point(a[i][0], a[i][1])
            point_b = Point(a[i+1][0], a[i+1][1])
            point_c = Point(b[j][0], b[j][1])
            point_d = Point(b[j+1][0], b[j+1][1])

            segment_1 = Segment(point_a, point_b)
            segment_2 = Segment(point_c, point_d)
            if check_segment_intersection(segment_1, segment_2):
                points.append(check_segment_intersection(segment_1, segment_2))
    mid_x = (a[0][0])  
    mid_y = (a[0][1]) 
    for k in points:
        if dist > math.sqrt((mid_x - k[0])**2 + (mid_y - k[1])**2):
            dist = math.sqrt((mid_x - k[0])**2 + (mid_y - k[1])**2)
            goal_point = k
    return False if dist == 2000 else goal_point

def line_intersection_car(a, b):
    points = []
    goal_point=[0,0]
    dist = 2000
    for i in range(0,len(a)-1): 
        for j in range(0,len(b)-1):
            point_a = Point(a[i][0], a[i][1])
            point_b = Point(a[i+1][0], a[i+1][1])
            point_c = Point(b[j][0], b[j][1])
            point_d = Point(b[j+1][0], b[j+1][1])

            len_car = 100
            len_CD = math.sqrt((point_c.x - point_d.x) ** 2 + (point_c.y - point_d.y) ** 2) / 2
            mid_CD = Point((point_c.x + point_d.x) / 2, (point_c.y + point_d.y) / 2)
            len_car_CD = math.sqrt((mid_CD.x - point_a.x) ** 2 + (mid_CD.y - point_a.y) ** 2)
            if len_car_CD > len_car + len_CD: continue

            segment_1 = Segment(point_a, point_b)
            segment_2 = Segment(point_c, point_d)
            if check_segment_intersection(segment_1, segment_2):
                points.append(check_segment_intersection(segment_1, segment_2))
    mid_x = (a[0][0])  
    mid_y = (a[0][1]) 
    for k in points:
        if dist > math.sqrt((mid_x - k[0])**2 + (mid_y - k[1])**2):
            dist = math.sqrt((mid_x - k[0])**2 + (mid_y - k[1])**2)
            goal_point = k
    return False if dist == 2000 else goal_point


def intersection(x1y1, x2y2, x3y3, x4y4):
        try:
            px= ( (x1y1[0]*x2y2[1]-x1y1[1]*x2y2[0])*(x3y3[0]-x4y4[0])-(x1y1[0]-x2y2[0])*(x3y3[0]*x4y4[1]-x3y3[1]*x4y4[0]) ) / ( (x1y1[0]-x2y2[0])*(x3y3[1]-x4y4[1])-(x1y1[1]-x2y2[1])*(x3y3[0]-x4y4[0]) ) 
            py= ( (x1y1[0]*x2y2[1]-x1y1[1]*x2y2[0])*(x3y3[1]-x4y4[1])-(x1y1[1]-x2y2[1])*(x3y3[0]*x4y4[1]-x3y3[1]*x4y4[0]) ) / ( (x1y1[0]-x2y2[0])*(x3y3[1]-x4y4[1])-(x1y1[1]-x2y2[1])*(x3y3[0]-x4y4[0]) )
        except ZeroDivisionError:
            px = 0
            py = 0
        return px, py
