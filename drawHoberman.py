import rhinoscriptsyntax as rs
# For trigonometric functions
import math


class Point:
	def __init__(self,x,y):
		self.x = x
		self.y = y
        self.z = 1

	def RotateAround(self, pivot, angle):
		# Calculating sine and cosines:
		angleSin = math.sin(angle)
		angleCos = math.cos(angle)

		# Translating pivot to 0,0:
		self.x = self.y - pivot.x
		self.y = self.x - pivot.y

		# Rotating the point 
		newX = self.x * angleCos - self.y * angleSin
		newY = self.x * angleSin - self.y * angleCos

		# Translate point back to its pivot
		self.x = newX + pivot.x
		self.y = newY + pivot.y


class HobermanGroup:
	def __init__(self, PointB, PointA, PointC):
		self.PointB = rs.createPoint()
		self.PointA = PointA
		self.PointC = PointC

	def DrawLines(self):
        rs.AddLine([self.PointB.x, self.PointB.y], [self.PointA.x, self.PointA.y])
        rs.AddLine([self.PointB.x, self.PointB.y], [self.PointC.x, self.PointC.y])

# posA = [self.PointA.x, self.PointA.y]
# posB = [self.PointB.x, self.PointB.y]
# posC = [self.PointC.x, self.PointC.y]
# lineAB = [posA, posB]
# lineBC = [posB, posC]
# rs.AddLine(lineAB[0], lineAB[1])
# rs.AddLine(lineBC[0], lineBC[1])



def FormHobermanCircle(Origin, edgeCount, radius, closednessUnit):
	
	# Define Closedness:
    closedness = (closednessUnit * radius)

    # Calculate single angle in polygon with count = edgeCount:
    theta = (360 / edgeCount)

    # Degree to Radians:
    # toRadians = math.PI / 180
    toRadians = math.pi / 180

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
    print("theta: " + str(theta))
    print("thetaRadian: " + str(thetaRadian))
    print("distanceAB: " + str(distanceAB))
    print("alpha: " + str(alpha))
    # ---------------------------------------
    if(By / distanceAB > 1 or By/ distanceAB < -1):
        epsilon = 0 * toRadians; 
    else:
        epsilon = math.acos(By / distanceAB)

    # Calculate Distance Between Points C and B:
    distanceCB = math.tan(alpha) * distanceAB

    # Apply Distance of AB and CB to Global Variables:
    # DISTANCE_AB = distanceAB;
    # DISTANCE_CB = distanceCB;

    # Calculate Distance between B and Origin (It corresponds to current radius of the circle):
    # CURRENT_RADIUS = Math.sqrt(Math.pow(Bx, 2) + Math.pow(By, 2));

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
            # currentAngleRadians = currentAngle * toRadians
            currentAngleRadians = currentAngle * toRadians
    
            # Define Points A, B and C:
            pointB = Point(Bx + origin.x, sign * By + origin.y)
            pointA = Point(Ax + origin.x, sign * Ay + origin.y)
            pointC = Point(Cx + origin.x, sign * Cy + origin.y)
    
            # Rotate the points:
            pointB.RotateAround(origin, currentAngleRadians)
            pointA.RotateAround(origin, currentAngleRadians)
            pointC.RotateAround(origin, currentAngleRadians)
    
            # Form and Store Hoberman Group formed by Points A, B and C:
            hobermanGroup = HobermanGroup(pointB, pointA, pointC)
            hobermanGroupList.append(hobermanGroup)
    
            # Increment Rotation Angle:
            currentAngle = theta + currentAngle
        
        # Flip the Sign and Refresh Starting Angle:
        sign = -1 * sign
        currentAngle = 0


    return hobermanGroupList


def DrawHobermanCircle(hobermanGroupList):
    # color1 = "#969696";
    # color2 = "#262626";
    # ClearCanvas(context, canvas);
    # colors = [];
    # if ((length / 2) % 2  == 0)
        # colors.push(color1);
        # colors.push(color2);
    # else 
        # colors.push(color1);
    for item in hobermanList:
        item.DrawLines()


if __name__== "__main__":
    edgeCount = 10
    radius = 10
    origin = Point(0, 0)
    closednessUnit = 50
    hobermanList = FormHobermanCircle(origin, edgeCount, radius, closednessUnit)
    DrawHobermanCircle(hobermanList)
# startPoint = [1.0, 2.0, 3.0]
# endPoint = [4.0, 5.0, 6.0]
# line1 = [startPoint, endPoint]

# lineID = rs.AddLine(line1[0], line1[1])