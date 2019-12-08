import rhinoscriptsyntax as rs
import Rhino
import scriptcontext
import System.Guid

import math # for  cos, sin, acos, tan


class HobermanGroup:
    def __init__(self, pointB, pointA, pointC):
        self.PointB = pointB
        self.PointA = pointA
        self.PointC = pointC

    def DrawLines(self):
        rs.AddLine(self.PointB, self.PointA)
        rs.AddLine(self.PointB, self.PointC)


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
    Origin = rs.CreatePoint(0.0, 0.0, 0.0)
	    
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
    hobermanGroupList = []

    # Define Sign Which Will Be Used to Create Other Chain of Hoberman Circle:
    sign = 1

    # debug print
    # ---------------------------------------
    print("Bx: " + str(Bx), "By: " + str(By))
    print("Ax: " + str(Ax), "Ay: " + str(Ay))
    print("Cx: " + str(Cx), "Cy: " + str(Cy))
    print("theta: " + str(theta * toDegrees))
    print("thetaRadian: " + str(thetaRadian))
    print("distanceAB: " + str(distanceAB))
    print("alpha: " + str(alpha * toDegrees))
    # ---------------------------------------

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
            
            # Form and Store Hoberman Group formed by Points A, B and C:
            hobermanGroup = HobermanGroup(pointB, pointA, pointC)
            hobermanGroupList.append(hobermanGroup)

            # Increment Rotation Angle:
            currentAngle = theta + currentAngle
        
        # Flip the Sign and Refresh Starting Angle:
        sign = -1 * sign
        currentAngle = 0
    
    return hobermanGroupList


def AddCylinder(cylinder_center, cylinder_radius, cylinder_max):
    zaxis = cylinder_center-cylinder_max
    plane = Rhino.Geometry.Plane(cylinder_center, zaxis)
    circle = Rhino.Geometry.Circle(plane, cylinder_radius)
    cylinder = Rhino.Geometry.Cylinder(circle, zaxis.Length)
    brep = cylinder.ToBrep(True, True)
    if brep:
        if scriptcontext.doc.Objects.AddBrep(brep)!=System.Guid.Empty:
            scriptcontext.doc.Views.Redraw()
            return Rhino.Commands.Result.Success
    return Rhino.Commands.Result.Failure


def DrawHobermanCircle(hobermanGroupList):
    for item in hobermanList:
        item.DrawLines()
        AddCylinder(item.PointB, 2, item.PointA)
        AddCylinder(item.PointB, 2, item.PointC)

if __name__== "__main__":
    radius = rs.GetInteger("Please enter radius for hoberman circle:", 10, 1)
    edgeCount = rs.GetInteger("Please enter edge count for hoberman circle:", 10, 9)
    closednessUnit = rs.GetInteger("Please enter percentale of circle compression:", 0, 0, 100)
    hobermanList = FormHobermanCircle(edgeCount, radius, closednessUnit/100)
    DrawHobermanCircle(hobermanList)
