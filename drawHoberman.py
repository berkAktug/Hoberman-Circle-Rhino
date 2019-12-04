import rhinoscriptsyntax as rs

import math # for  cos, sin, acos, tan


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def RotateAround(self, pivot, angle):
        # Calculating sine and cosines:
        angleSin = math.sin(angle)
        angleCos = math.cos(angle)

        # Translating pivot to 0,0:
        point[0] = self.x - pivot[0]
        point[1] = self.y - pivot.y[1]

        # Rotating the point 
        newX = point[0] * angleCos - point[1] * angleSin
        newY = point[0] * angleSin - point[1] * angleCos

        # Translate point back to its pivot
        point[0] = newX + pivot[0]
        point[1] = newY + pivot[1]

    def GetRhinoPoint(self):
        return rs.CreatePoint(x,y,z)



class HobermanGroup:
    def __init__(self, pointB, pointA, pointC):
        self.PointB = pointB
        self.PointA = pointA
        self.PointC = pointC

    def DrawLines(self):
        LineBA_ID = rs.AddLine(self.PointB, self.PointA)
        LineBC_ID = rs.AddLine(self.PointB, self.PointC)


# class Point:
# 	def __init__(self,x,y, z=1):
# 		self.x = x
# 		self.y = y
#         self.z = z

# 	def RotateAround(self, pivot, angle):
# 		# Calculating sine and cosines:
# 		angleSin = math.sin(angle)
# 		angleCos = math.cos(angle)

# 		# Translating pivot to 0,0:
# 		self.x = self.y - pivot.x
# 		self.y = self.x - pivot.y

# 		# Rotating the point 
# 		newX = self.x * angleCos - self.y * angleSin
# 		newY = self.x * angleSin - self.y * angleCos

# 		# Translate point back to its pivot
# 		self.x = newX + pivot.x
# 		self.y = newY + pivot.y


# class HobermanGroup:
# 	def __init__(self, PointB, PointA, PointC):
# 		self.PointB = PointB
# 		self.PointA = PointA
# 		self.PointC = PointC

# 	def DrawLines(self):
#         linePoint_B = [self.PointB.x, self.PointB.y, self.PointB.z]
#         linePoint_A = [self.PointA.x, self.PointA.y, self.PointA.z]
#         linePoint_C = [self.PointC.x, self.PointC.y, self.PointC.z]

#         lineBA = [linePoint_B, linePoint_A]
#         lineBC = [linePoint_B, linePoint_C]

#         rs.AddLine(lineBA[0], lineBA[1])
#         rs.AddLine(lineBC[0], lineBC[1])


def RotateAround(point, pivot, angle):
	# Calculating sine and cosines:
	angleSin = math.sin(angle)
	angleCos = math.cos(angle)

	# Translating pivot to 0,0:
	point[0] = point[0] - pivot[0]
	point[1] = point[1] - pivot[1]

	# Rotating the point 
	newX = point[0] * angleCos - point[1] * angleSin
	newY = point[0] * angleSin - point[1] * angleCos

	# Translate point back to its pivot
	point[0] = newX + pivot[0]
	point[1] = newY + pivot[1]



def FormHobermanCircle(Origin, edgeCount, radius, closednessUnit):
	# Define Closedness:
    closedness = (closednessUnit * radius)

    # Calculate single angle in polygon with count = edgeCount:
    theta = (360 / edgeCount)

    # Degree to Radians:
    toRadians = math.pi / 180
    toDegrees = 180 / math.pi

    # Theta in Terms of radians:
    thetaRadian = theta * toRadians

    # Calculate Point B:
    Bx = (radius - closedness) * math.cos(thetaRadian/2)
    By = (radius - closedness) * math.sin(thetaRadian/2)
    
    # Calculate Distance Between Point A and B:
    distanceAB = radius * math.sin(thetaRadian/2)

    # Calculate Angles Alpha and Epsilon:
    #		# Epsilon is the Angle between A and line perpendicular to hypotenuse drawn from point B.
	#		# Alpha is the one third of the angle ABC^.
    alpha = 45 * toRadians  - (thetaRadian / 4)
    
    # debug print
    # ---------------------------------------
    print("By: " + str(By))
    print("Bx: " + str(Bx))
    print("theta: " + str(theta * toDegrees))
    print("thetaRadian: " + str(thetaRadian))
    print("distanceAB: " + str(distanceAB))
    print("alpha: " + str(alpha * toDegrees))
    # ---------------------------------------
    # if(By / distanceAB > 1 or By/ distanceAB < -1):
        # epsilon = 0 * toRadians; 
    # else:
    epsilon = math.acos(By / distanceAB)

    # Calculate Distance Between Points C and B:
    distanceCB = math.tan(alpha) * distanceAB

    # Calculate Distance of A From The Origin:
    distanceOA = Bx + (distanceAB * math.sin(epsilon))

    # Calculate Point A:
    Ax = distanceOA * math.cos(thetaRadian)
    Ay = distanceOA * math.sin(thetaRadian)

    # Calculate Point C:
    Cx = Bx - (distanceCB * math.sin(alpha + epsilon))
    Cy = 0

    # Define Initial Angle:
    currentAngle = 0

    # Define The List That Will Store Hoberman Groups Formed By 3 Points:
    hobermanGroupList = []

    # Define Sign Which Will Be Used to Create Other Chain of Hoberman Circle:
    sign = 1
    
    for j in range(1,2):
    	for i in range(edgeCount):
            # Calculate Current Angle in Radians:
            currentAngleRadians = currentAngle * toRadians
    
            # Define Points A, B and C:
            pointB = rs.CreatePoint(Bx + Origin[0], sign * By + Origin[1])
            pointA = rs.CreatePoint(Ax + Origin[0], sign * Ay + Origin[1])
            pointC = rs.CreatePoint(Cx + Origin[0], sign * Cy + Origin[1])
    
            # Rotate the points:
            # pointB.RotateAround(origin, currentAngleRadians)
            # pointA.RotateAround(origin, currentAngleRadians)
            # pointC.RotateAround(origin, currentAngleRadians)
            RotateAround(pointB, Origin, currentAngleRadians)
            RotateAround(pointA, Origin, currentAngleRadians)
            RotateAround(pointC, Origin, currentAngleRadians)
            
            # Form and Store Hoberman Group formed by Points A, B and C:
            hobermanGroup = HobermanGroup(pointB, pointA, pointC)
            hobermanGroupList.append(hobermanGroup)

            # Increment Rotation Angle:
            currentAngle = theta + currentAngle
        
        # Flip the Sign and Refresh Starting Angle:
        sign = -1 * sign
        currentAngle = 0


    return hobermanGroupList


# def DrawLines(PointB, PointA, PointC):
#     LineBA_ID = rs.AddLine(PointB, PointA)
#     LineBC_ID = rs.AddLine(PointB, PointC)
 
#     return tuple(LineBA_ID, LineBC_ID)

def DrawHobermanCircle(hobermanGroupList):
    list_lineBA_ID = []
    list_lineBC_ID = []

    for item in hobermanList:
        item.DrawLines()
        # LineBA_ID = rs.AddLine(item[0], item[1])
        # LineBC_ID = rs.AddLine(item[0], item[2])

        # 
        # rs.AddLine(item[0], item[1])
        # rs.AddLine(item[0], item[2])
        # 

        # lineIDs = DrawLines(item[0], item[1], item[2])
        # list_lineBA_ID.append(LineBA_ID)
        # list_lineBC_ID.append(LineBC_ID)


if __name__== "__main__":
    edgeCount = 10
    radius = 10
    origin = rs.CreatePoint(0.0, 0.0, 0.0)
    closednessUnit = 0
    hobermanList = FormHobermanCircle(origin, edgeCount, radius, closednessUnit)
    DrawHobermanCircle(hobermanList)

# startPoint = [1.0, 2.0, 3.0]
# endPoint = [4.0, 5.0, 6.0]
# line1 = [startPoint, endPoint]

# lineID = rs.AddLine(line1[0], line1[1])