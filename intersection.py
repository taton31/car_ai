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



def shape_intersection_car_AI(a, b):
    points = []
    for i in range(0,len(a)-1): 
        for j in range(0,len(b)-1):
            point = line_intersection_AI (a[i][0], a[i][1], a[i+1][0], a[i+1][1], b[j][0], b[j][1], b[j+1][0], b[j+1][1])
            if point:
                points.append(point)
    return find_closest_point_AI([a[0][0], a[0][1]], points)



def line_intersection_AI(x1, y1, x2, y2, x3, y3, x4, y4):
    # Calculate the intersection of two lines
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    

    if denom == 0:
        return False
    else:
        numx = (x1*y2 - y1*x2) * (x3 - x4) - (x1 - x2) * (x3*y4 - y3*x4)
        numy = (x1*y2 - y1*x2) * (y3 - y4) - (y1 - y2) * (x3*y4 - y3*x4)
        intersection_x = numx / denom
        intersection_y = numy / denom

    # Check if intersection point lies on both line segments
    if ((intersection_x < min(x1, x2) or intersection_x > max(x1, x2)) or
        (intersection_x < min(x3, x4) or intersection_x > max(x3, x4))):
        return False

    if ((intersection_y < min(y1, y2) or intersection_y > max(y1, y2)) or
        (intersection_y < min(y3, y4) or intersection_y > max(y3, y4))):
        return False

    return (intersection_x, intersection_y)


def find_closest_point_AI(A, points):
    if not points: return False
    # Set the initial closest distance to a large number
    closest_distance = float('inf')
    # Iterate over the points in the list
    for p in points:
        # Calculate the distance between A and p
        distance = ((A[0] - p[0]) ** 2 + (A[1] - p[1]) ** 2) ** 0.5
        # Update the closest distance and point if the current point is closer
        if distance < closest_distance:
            closest_distance = distance
            closest_point = p
    # Return the closest point
    return closest_point


def GTP_intersect(x1, y1, x2, y2, x3, y3, x4, y4):

    # Calculate the coefficients of the lines passing through each segment
    k1 = (y2 - y1) / (x2 - x1) if x1 != x2 else float('inf')
    k2 = (y4 - y3) / (x4 - x3) if x3 != x4 else float('inf')

    # Calculate the free terms of the equations
    b1 = y1 - k1 * x1
    b2 = y3 - k2 * x3

    # If the equations of the lines passing through the segments are the same, the segments coincide
    if k1 == k2 and b1 == b2:
        return (x1, y1)

    # If the equations of the lines are parallel, the segments do not intersect
    if k1 == k2:
        return False

    # Calculate the point of intersection
    x = (b2 - b1) / (k1 - k2)
    y = k1 * x + b1

    # Check if the intersection point is on the segments
    if (x1 <= x <= x2 or x2 <= x <= x1) and (x3 <= x <= x4 or x4 <= x <= x3):
        return (x, y)
    else:
        return False


def GPT_nearest_point(A, ls):
    # Set the initial minimum distance to a large value
    min_distance = float('inf')
    # Set the initial nearest point to None
    nearest_point = None
    
    # Iterate through the list of points
    for point in ls:
        # Calculate the distance between A and the current point
        distance = math.sqrt((point[0] - A[0])**2 + (point[1] - A[1])**2)
        # If the distance is smaller than the current minimum distance,
        # update the minimum distance and set the current point as the nearest point
        if distance < min_distance:
            min_distance = distance
            nearest_point = point
    
    # Return the nearest point
    return nearest_point


def GPT_line_intersection_car(a, b):
    points = []
    for i in range(0,len(a)-1): 
        for j in range(0,len(b)-1):
            point = GTP_intersect (a[i][0], a[i][1], a[i+1][0], a[i+1][1], b[j][0], b[j][1], b[j+1][0], b[j+1][1])
            if point:
                points.append(point)
    return GPT_nearest_point([a[0][0], a[0][1]], points)