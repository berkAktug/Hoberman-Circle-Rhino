
import rhinoscriptsyntax as rs
import Rhino
import scriptcontext
import System.Guid

import math # for  cos, sin, acos, tan

def RotateAround(Point, pivot, angle):
	# Calculating sine and cosines:
	angleSin = math.sin(angle)
	angleCos = math.cos(angle)

	# Translating pivot to 0,0:
	Point.X = Point.X - pivot.X
	Point.Y = Point.Y - pivot.Y

	# Rotating the Point 
	newX = Point.X * angleCos - Point.Y * angleSin
	newY = Point.X * angleSin + Point.Y * angleCos

	# Translate Point back to its pivot
	Point.X = newX + pivot.X
	Point.Y = newY + pivot.Y


def FormHobermanCircle(edgeCount, radius, closednessUnit):
    Origin = rs.CreatePoint(0.0, 0.0, 5.0)
	    
    # Calculate single angle in polygon with count = edgeCount:
    theta = (360 / edgeCount)

    # Degree to Radians:
    toRadians = math.pi / 180

    toDegrees = 180 / math.pi

    # Theta in Terms of radians:
    thetaRadian = theta * toRadians

    # Calculate Distance Between Point A and B:
    distanceAB = radius * math.sin(thetaRadian/2)

    # Calculate Angles Alpha and Epsilon:
    #		# Epsilon is the Angle between A and line perpendicular to hypotenuse drawn from point B.
	#		# Alpha is the one third of the angle ABC^.
    alpha = 45 * toRadians  - (thetaRadian / 4)

    # Calculate Distance Between Points C and B:
    distanceCB = math.tan(alpha) * distanceAB

    # Define Closedness:
    closedness = (closednessUnit * (radius - distanceCB))

    # Calculate Point B:
    Bx = (radius - closedness) * math.cos(thetaRadian/2)
    By = (radius - closedness) * math.sin(thetaRadian/2)
        
    epsilon = math.acos(By / distanceAB)

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
    hobermanArcList = []

    # Define Sign Which Will Be Used to Create Other Chain of Hoberman Circle:
    sign = 1

    for j in range(2):
    	for i in range(edgeCount):
            # Calculate Current Angle in Radians:
            currentAngleRadians = currentAngle * toRadians
    
            # Define Points A, B and C:
            pointB = rs.CreatePoint(Bx + Origin.X, sign * By + Origin.Y)
            pointA = rs.CreatePoint(Ax + Origin.X, sign * Ay + Origin.Y)
            pointC = rs.CreatePoint(Cx + Origin.X, sign * Cy + Origin.Y)
    
            # Rotate the points:
            RotateAround(pointB, Origin, currentAngleRadians)
            RotateAround(pointA, Origin, currentAngleRadians)
            RotateAround(pointC, Origin, currentAngleRadians)
            
            # Store hoberman arc (point A, point B and point C):
            hobermanArc = rs.AddPolyline([pointA, pointB, pointC])
            hobermanArcList.append(hobermanArc)

            # Increment Rotation Angle:
            currentAngle = theta + currentAngle
        
        # Flip the Sign and Refresh Starting Angle:
        sign = -1 * sign
        currentAngle = 0
    
    return hobermanArcList


def AddPipe(hobermanArcList, pipeRadius):
    # curve = rs.GetObject("Select curve to create pipe around", rs.filter.curve, True)
    for arc in hobermanArcList:
        domain = rs.CurveDomain(arc)
        rs.AddPipe(arc, 0, pipeRadius)


if __name__== "__main__":
    radius = rs.GetInteger("Please enter radius for hoberman circle:", 10, 1)
    edgeCount = rs.GetInteger("Please enter edge count for hoberman circle:", 10, 9)
    closednessUnit = rs.GetInteger("Please enter percentale of circle compression:", 0, 0, 100)
    pipeRadius = rs.GetReal("Please enter radius for surrounding pipe:", 0.01, 0.01, 3)
    # For debug.
    # radius = 10
    # edgeCount = 10
    # closednessUnit = 50

    hobermanArcList = FormHobermanCircle(edgeCount, radius, closednessUnit /100)
    AddPipe(hobermanArcList, pipeRadius)
