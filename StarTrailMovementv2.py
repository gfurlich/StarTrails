#!/usr/bin/env python
'''

File : 		StarTrailMovementv2.py
Author : 	Greg Furlich
Date Created : 	01/06/2018
Copyright : 	(c) 2018, Greg Furlich
License :	MIT License

Purpose : A python script simulate star trails for a random array of positions for <n_stars> around a randomly positioned rotational axis. The stars are then rotated for a length of a <rotation_angle>. A gif is created using the animation tools in matplotlib.

Execution : ./StarTrailMovementv2.py <n_stars> <rotation_angle>

Example Execution : ./StarTrailMovementv2.py 200 30

Animation based on : rain.py by Nicolas P. Rougier (https://matplotlib.org/examples/animation/rain.html)

'''


#--- Start of Script ---#

#--- Importing Python Modules ---#

import sys
import numpy as np
import math
import time
import os, errno
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import animation
from matplotlib.colors import hsv_to_rgb

#--- Initial Parameters ---#

t_start = time.time()

# date generated :
#date = time.strftime('v%Y%m%d_%H%M%S')	# with sec percision
date = time.strftime('v%Y%m%d') # with day percision

pi = 3.14159265359

# Defining Rectangular window for plot :
# 16:9 aspect ratio

w = 16.		# width
h = 9.		# height

# Number of Stars :
n_stars = int(sys.argv[1])

# Angle of Rotation (in Radians):
rotation_angle = float(sys.argv[2]) * pi / 180

# Angle Steps :
delta_angle = 1
delta_angle = delta_angle * pi / 180	# convert to radians

# Steps of Rotation :
n_rotations = int(rotation_angle / delta_angle)

#--- Star Initial Positions ---#

# Initialize Star Data Arrays :
stars = np.zeros(n_stars, dtype=[('position', float, 2),
	('component', 	float, 2),
	('radial', 	float, 1),
	('angle', 	float, 1),
	('size',     	float, 1),
	('alpha',    	float, 1),
	('color',    	float, 3)])

#hsv = np.zeros( (n_stars,3))

# Rotational Axis :
rotational_axis_x = np.random.uniform(0, w)
rotational_axis_y = np.random.uniform(0, h)

#print rotational_axis_x, rotational_axis_y

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

# Stars Random Positions :
stars['position'][:,0] = np.random.uniform(rotational_axis_x - r_max, rotational_axis_x + r_max, n_stars)
stars['position'][:,1] = np.random.uniform(rotational_axis_y - r_max, rotational_axis_y + r_max, n_stars)

# Initial Configuration from Rotational Axis :
stars['component'][:,0] = stars['position'][:,0] - rotational_axis_x
stars['component'][:,1] = stars['position'][:,1] - rotational_axis_y

stars['radial'] = np.power( np.power( stars['component'][:,0] ,2 ) + np.power( stars['component'][:,1] ,2 ) , .5)

stars['angle'] = np.arctan( stars['component'][:,0] / stars['component'][:,1])

#--- Star Characteristics ---#

# Star Alpha (Transparency) :
# Beta Distribution Sampling 
# (0 - 1 skewed distribution towards 0):
stars['alpha'] = 1 - np.random.beta(2,15) 

# Star Size :
stars['size'] = np.random.beta(2,4)	

# Star Random Color Variation from White :
# White in HSV (0,0,1)

# Add Normal Colored Stars
hsv = np.random.uniform(0, 1, (n_stars, 3) ) 	# Hue

# Convert HSV to RGB
stars['color'] = hsv_to_rgb( hsv )

#h = np.random.uniform(0, 1) 		# Hue
#s = np.random.beta(1, 15)		# Saturation
#v = 1 - np.random.beta(1, 15)	# Value

#--- Plot Initial Star and Rotational Positions ---#

stars_initial = plt.figure(1)		# Initialize First Plot

# Legend Labes :
star_label = 'n_stars = '+str(n_stars)
rotation_label = 'Axis of Rotation, rotate = '+str(sys.argv[2])

# Scatter Plots :
plt.scatter( stars['position'][:, 0], stars['position'][:, 1], marker='*', label = star_label)	# Star Plot
plt.scatter(rotational_axis_x, rotational_axis_y, marker='o', label = rotation_label)			# Rotation Axis Plot

# Plot Limits :
plt.xlim([0, w])		# X Range
plt.ylim([0, h])		# Y Range

# Legend :
plt.legend(loc='upper left')

print "Rendering Initial Figure : Figures/Stars_Initial_"+date+".png"

# Save Plot :
plt.savefig("Figures/Stars_Initial_"+date+".png")

#--- Star Rotation Scatter plot ---#
# Updated during animation as the stars rotate

star_trails = plt.figure(2)

# Plot Limits :
plt.xlim([0, w])		# X Range
plt.ylim([0, h])		# Y Range

# Remove Plot Frame and Axes :	
ax = star_trails.gca()
#ax.set_frame_on(False)
#ax.set_aspect('equal')	# Set equal aspect ratio
#ax.set_xticks([])
#ax.set_yticks([])
#plt.axis('off')

# Save Figure Title :
out_dir = "Gif_Figures/Star_Trail_Movement_%s/" % (date,)

# Background colors for the sky:
background_color = '#000814'

# Create Directory for Out Figures :
try:
	os.makedirs(out_dir)
except OSError as e:
	if e.errno != errno.EEXIST:
		raise

star_scat = ax.scatter(stars['position'][:, 0], stars['position'][:, 1], s=stars['size'], lw=0.5, edgecolors = stars['color'], facecolors = stars['color'])

#--- Update Star Trail Rotation Function ---#
def update_star_trail(i_rotation):

	# Rotate Stars Position :
	stars['position'][:,0] = rotational_axis_x + stars['radial'] * np.cos( stars['angle'] + i_rotation * np.pi / 180 )
	stars['position'][:,1] = rotational_axis_y + stars['radial'] * np.sin( stars['angle'] + i_rotation * np.pi / 180 )

	# Update Star Position on Scatter Plot :
	star_scat.set_offsets(stars['position'])

	#print stars['position'][1,0], stars['position'][1,1]

	# Save Figure Title :
	#out_fig = out_dir+"Star_Trails_%04d.png" % (i_rotation,)

	# Save Plot w/ Colored Background :
	#star_trails.savefig(out_fig, dpi=500, facecolor = background_color, bbox_inches='tight', pad_inches=0)

	#print '\rRendering Rotation {:04d} / {:d} '.format(i_rotation, n_rotations)

#--- Create Star Trail Animation ---#

# Star Trail Animation
# using the update function as the animation director.
star_anim = animation.FuncAnimation(star_trails, update_star_trail, frames = n_rotations)

#--- Create GIF ---#

# Define GIF Name :
out_gif = 'GIFs/Star_Trail_Movement_%s.gif' % (date)

print 'Rendering GIF : '+out_gif

# Save Animation as GIF :
star_anim.save( out_gif, writer='imagemagick', fps=20)

# GIF Size :
os.system('du -sh '+out_gif)

#--- Time Elapsed ---#

# Total time elapsed :
t_total = time.time() - t_start

print 'total time : %f secs' % (t_total)

#--- End of Script ---#
