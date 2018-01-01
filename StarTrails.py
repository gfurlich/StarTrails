#!/usr/bin/env python
'''
File : StarTrails.py
Author : Greg Furlich
Date Created : 11/24/2017

Purpose : A python script simulate star trails for a random array of positions for <n_stars> around a randomly positioned rotational axis. The stars are then rotated for a length of a <rotation_angle>. A image is rendered from the star trails full rotation.

Execution : StarTrails.py <n_stars> <rotation_angle>

Example Execution : ./StarTrails.py 20 30

'''

#--- Start of Script ---#


#--- Importing Python Modules ---#

import sys
import random
from matplotlib import pyplot as plt
import time
import math
from colorsys import hsv_to_rgb

#--- Initial Parameters ---#

t_start = time.time()

# date generated :
date = time.strftime('v%Y%m%d_%H%M%S')	# with sec percision
#date = time.strftime('v%Y%m%d') # with day percision

pi = 3.14159265359

# Defining Rectangular window for plot :
# 16:9 aspect ratio

w = 16		# width
h = 9		# height

# Number of Stars :
n_stars = int(sys.argv[1])

# Angle of Rotation (in Radians):
rotation_angle = float(sys.argv[2]) * pi / 180

# Rotational Angle Steps :
delta_angle = .01	# in degrees
delta_angle =  delta_angle * pi / 180	# Convert to radians

# Steps of Rotation :
n_rotations = int( rotation_angle / delta_angle )

#--- Star Initial Positions ---#
#print 'Star Initial Positions :'

# defining nstar and preallocate array :
star_x = [[] for _ in xrange(n_stars)]	# stars x position nested list
star_y = [[] for _ in xrange(n_stars)]	# stars y position nested list

star_initial_x =  []	# stars x position list
star_initial_y =  []	# stars y position list

# Defining Random Rotational Axis :
rotational_axis_x = random.uniform(0,w)
rotational_axis_y = random.uniform(0,h)

# Find max radius from rotational axis to corners

def radialDistance(x1,y1,x2,y2):
	'''
	Function for determining the radial distance between two points using pythagreons theorem.
	'''
	r = math.sqrt( math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2) )
	return r ;

r1 = radialDistance( 0,  0, rotational_axis_x, rotational_axis_y)
r2 = radialDistance( 0,  w, rotational_axis_x, rotational_axis_y)
r3 = radialDistance( h,  0, rotational_axis_x, rotational_axis_y)
r4 = radialDistance( h,  w, rotational_axis_x, rotational_axis_y)

r = [r1, r2, r3, r4]

r.sort()

r_max = r[-1]

#print rotational_axis_x, rotational_axis_y, r

# Randomly Defining Stars Position :
for i in range(0,n_stars):
	star_initial_x.append( random.uniform( rotational_axis_x - r_max, rotational_axis_x + r_max) )
	star_initial_y.append( random.uniform( rotational_axis_y - r_max , rotational_axis_y + r_max) )

	#print 'Star '+str(i+1)+' (star_x, star_y) = \t('+str(star_initial_x[i])+','+str(star_initial_y[i])+')'

#--- Plot Initial Star and Rotational Positions ---#

plt.figure(1)		# Initialize First Plot

# Legend Labes :
star_label = 'n_stars = '+str(n_stars)
rotation_label = 'Axis of Rotation, rotate = '+str(sys.argv[2])

plt.plot(star_initial_x, star_initial_y, '*', label = star_label)	# Star Plot
plt.plot(rotational_axis_x, rotational_axis_y, 'o',label = rotation_label)			# Rotation Axis Plot

plt.xlim([0,w])		# X Range
plt.ylim([0,h])		# Y Range

plt.legend(loc='upper left')

print "Rendering Initial Figure : Figures/Stars_Initial_"+date+".png"

plt.savefig("Figures/Stars_Initial_"+date+".png")	# Save Plot

#--- Rotate Stars ---#

# preallocate star array
star_r = [] 			# stars r list
star_initial_angle_d = [] 	# stars initial angle from rotational axis in degrees
star_initial_angle = []		# stars initial angle from rotational axis

# Calculate the radial distance between each star and axis :
for i in range(0,n_stars):
	delta_x = star_initial_x[i] - rotational_axis_x
	delta_y = star_initial_y[i] - rotational_axis_y
	star_r.append( math.sqrt(math.pow(delta_x,2) + math.pow(delta_y,2) ) )
	star_initial_angle_d.append( math.atan2( delta_y, delta_x ) * 180 / pi )
	star_initial_angle.append( math.atan2( delta_y, delta_x ) )
	#print 'Star '+str(i+1)+' (Radial Dist, angle) = \t('+str(star_r[i])+', '+str(star_initial_angle[i])+')'
	#print 'Star '+str(i+1)+' (delta_x, delta_y) = \t('+str(delta_x)+', '+str(delta_y)+')'

# Initialize Plot :
star_trail = plt.figure(2, frameon=False)

plt.xlim([0,w])		# X Range
plt.ylim([0,h])		# Y Range

# List for Star Size, Alpha, and Color:
star_size = []
star_color = []
star_alpha = []

# Background colors for the sky:
#bg = '#152033'
background_color = '#000814'

# Calculate star rotation :
for j in range(0,n_stars):

	print 'Rendering Trail for Star {0}\r'.format(j+1),

	# Star Random Size and Alpha :

	# Uniform Distribution Sampling :
	#star_size.append(float(random.uniform(.001,1)))
	#star_alpha.append(float(random.uniform(.5,1)))

	# Gaussian Distribution Sampling :
	#star_size.append(float(random.gauss(.01,.1) ) )
	star_alpha.append(float(random.gauss(.9,.01) ) )

	# Beta Distribution Sampling 
	# (0 - 1 skewed distribution towards 0):
	star_size.append( random.betavariate(2,4) )	

	# Star Random Color Variation from White :
	# White in HSV (0,0,1)
	if ( j % 50 == 0 ) :
		h = random.uniform(0, 1) 	# Hue
		s = random.uniform(0, 1)	# Saturation
		v = random.uniform(0, 1)	# Value

	else :
		h = random.uniform(0, 1) 		# Hue
		s = random.betavariate(1, 15)		# Saturation
		v = 1 -  random.betavariate(1, 15)	# Value

	# Give Every # Stars better Color :

	#print h, s, v

	# Conver HSV to RGB
	r, g, b = hsv_to_rgb(h, s, v)

	for i in range(1,n_rotations):
		angle_step = float(delta_angle * i)
		angle = star_initial_angle[j] + angle_step
		step_x = star_r[j]*math.cos( angle )
		step_y = star_r[j]*math.sin( angle )
		star_x[j].append( rotational_axis_x + step_x)
		star_y[j].append( rotational_axis_y + step_y)

	# Plot Star Trail :
	#plt.plot(star_x[j], star_y[j], '.', markersize=star_size[-1],  alpha=star_alpha[-1], color=(r,g,b))
	plt.plot(star_x[j], star_y[j], '.', markersize = star_size[-1], markeredgewidth = star_size[-1], alpha=.5, color=(r,g,b))

#--- Plot ---#

# Save Star Trail Plot :
print "\nRendering Star Trail Figure : Figures/Star_Trails_"+date+".png"

# Remove Frame and Axes :
ax = star_trail.gca()
ax.set_frame_on(False)
ax.set_aspect('equal')	# Set equal aspect ratio
ax.set_xticks([])
ax.set_yticks([])
plt.axis('off')

# High Quality:
star_trail.savefig("Figures/Star_Trails_"+date+".png", dpi=2000, facecolor = background_color, bbox_inches='tight', pad_inches=0)

# Fast, Low Quality :
#star_trail.savefig("Star_Trails_"+date+".png", facecolor='#152033', bbox_inches='tight', pad_inches=0)

#--- Time Elapsed ---#

# Total time elapsed :
t_total = time.time() - t_start

print 'total time : %f secs' % (t_total)

#--- End of Script ---#
