import matplotlib.pyplot as plt
import numpy as np
import math

#Triangles that calculate the change of X and Y coordinate
#with one side and one angle
def triangleX(v,theta):
    X = v * math.sin(theta)
    Y = v * math.cos(theta)
    return(X,Y)

def triangleY(v,theta):
    X = v * math.cos(theta)
    Y = v * math.sin(theta)
    return(X,Y)

#Starts creation of plots
fig, ax = plt.subplots()

#Force of hit
#This should be left the same to ease calculations
force = 100

#Data that the user should enter
#Cue distance should be inputed as centimetres, maybe even millimetres
#AngleHit is from north clockwise
cueDistance = 10 / 100         #/1000 if milli
angleHit = 315

#Limits the range of angle to 0-360 degrees
angleHit %= 360

#Sets the mass of a pool ball (kg)
#This assumes all balls are the same mass
mass = 0.05

#Calculation for the velocity of a ball
velocity = math.sqrt((2 * force * cueDistance)/mass)

#Gravity force constant
gravity = 9.8

#Coefficient of friction
#Basically the constant effect of friction onto the ball due to pool table
coefficient = 0.03

#Calculates deceleration
#Negative because formula originally calculates acceleration
deceleration = (coefficient * gravity) * -1

#Calculate distance ball has travelled
distance = (velocity**2) / (2 * coefficient * gravity)

#Calculates time
time = math.sqrt((2*distance)/-deceleration)

#Ranges for X,Y
rangeX = 1
rangeY = 1

hitX = 0
hitY = 0

#Changes where ball goes according to angle
if angleHit > 270:
    hitX, hitY = triangleX(distance,(angleHit%90))
    rangeY = -1
    #-x,y
elif angleHit == 270:
    hitX = distance
    #x,y
elif angleHit > 180:
    hitX, hitY = triangleY(distance,(angleHit%90))
    #x,y
elif angleHit == 180:
    hitY = distance
    #x,y
elif angleHit > 90:
    hitX, hitY = triangleX(distance,(angleHit%90))
    rangeX = -1
    #-x,y
elif angleHit == 90:
    hitX = distance
    rangeX = -1
    #-x,y
elif angleHit > 0:
    hitX, hitY = triangleY(distance,(angleHit%90))
    rangeX = -1
    rangeY = -1
    #-x,-y
else:
    hitY = distance
    rangeY = -1
    #x,-y



#Ball starting location
startX = 0
startY = 0

#Calculate hypotenuse for distance travelled
hypotenuse = velocity * time

#Calculates where it ends
endX = startX + (hitX * rangeX)
endY = startY + (hitY * rangeY)

#Graph for velocity
#Uncomment to see
""" t = np.arange(velocity, 0, deceleration)

ax = plt.subplot()
ax.plot((0, time), (velocity,0), marker='.')
ax.set_xlabel('time')
ax.set_ylabel('speed')
ax.set_xlim(xmin=0)
ax.set_ylim(ymin=0) """

#Graph for Distance
#Uncomment to see
""" t = np.arange(velocity, 0, deceleration)
ax = plt.subplot()
ax.plot((startX,endX), (startY,endY), marker='.')
ax.set_xlim(-1000,1000)
ax.set_ylim(-1000,1000) """

plt.show()
