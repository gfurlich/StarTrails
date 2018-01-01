# Star Trails

File : StarTrails/readme.md

Author : Greg Furlich

Copy Right : (c) 2017 Greg Furlich

License : MIT

# StarTrail.py

A python script simulate star trails for a random array of positions for <n_stars> around a randomly positioned rotational axis. The stars are then rotated for a length of a <rotation_angle>. A image is rendered from the star trails full rotation.

	Execution : ./StarTrails.py <n_stars> <rotation_angle>

	Outputs : Figures/Stars_Initial_v<YYYYMMDD_HHMMSS>.png
	Figures/Star_Trails_v<YYYYMMDD_HHMMSS>.png

![Star Trails Example Figure](https://github.com/gfurlich/Projects/blob/master/StarTrails/Figures/Star_Trails_example.png)

 # StarTrailMovementv1.py

A python script simulate star trails for a random array of positions for <n_stars> around a randomly positioned rotational axis. The stars are then rotated for a length of a <rotation_angle>. A image of each rotation iteration is rendered and then all iterations are combined into a GIF using Image Magick.

	Execution : ./StarTrailsMovementv1.py <n_stars> <rotation_angle>

	Outputs : Gif_Figures/Stars_Initial_<YYYYMMDD>.png
	Gif_Figures/Star_Trail_Movement_v<YYYYMMDD>/Stars_Trails_<IIII>.png
	GIFs/Star_Trail_v<YYYYMMDD>.gif

![Star Trail Movement Example GIF](https://github.com/gfurlich/Projects/blob/master/StarTrails/GIFs/Star_Trail_Movement_example.gif)

This does create large GIF files and takes a long time, hence version 2. Running with < n_stars> = 500 stars, dpi=500, and <rotation_angle> = 35 degrees, took 32925.481381 secs on my Surface Pro 4.
