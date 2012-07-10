#!/usr/bin/env python2
# coding=UTF-8

import cairo
import pango
import pangocairo
import sys

## Variables, depending on range you want you may need to adjust size
fontname = "Envy Code R"
fontsize = "10"
imgwidth = 2048
imgheight = 4096
margin = 0

surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, imgwidth, imgheight)
context = cairo.Context(surf)
context.rectangle(0,0,imgwidth,imgheight)
context.set_source_rgba(0,0,0,0)
context.fill()

pangocairo_context = pangocairo.CairoContext(context)
layout = pangocairo_context.create_layout()
font = pango.FontDescription( "%s %s" % (fontname,fontsize) )
layout.set_font_description(font)
context.set_source_rgb(1, 1, 1)

filename = fontname.lower().replace(' ','_')
fontfile = open(filename+'.wfd', 'w')
fontfile.write("// WARSOW Mudfont. version=\"1.1\" encoding=\"UTF-8\"\n //\"<texture width>\" \"<texture height>\"\n")
fontfile.write( "%d %d\n" % (imgwidth,imgheight) )
fontfile.write( "// \"<char>\" \"<x>\" \"<y>\" \"<width>\" \"<height>\"\n" )

x = margin
y = margin
maxwidth = 0
maxheight = 0
context.translate(margin,margin)
n = 31
while n < 0x9FFF:
	## print/draw/measure the character
	layout.set_text( unichr(n) )
	pangocairo_context.update_layout(layout)
	pangocairo_context.show_layout(layout)
	x1, y1, width, height = layout.get_pixel_extents()[1]
	fontfile.write( "%d %d %d %d %d\n" % (n,x,y,width,height) )

	## record sizes if necessary
	if width > maxwidth: maxwidth = width
	if height > maxheight: maxheight = height

	## Move for next character
	if x + maxwidth + 2*margin > imgwidth:
		context.translate( margin-x, maxheight+1 )
		x += margin-x
		y += maxheight+1
	else:
		context.translate(width,0)
		x += width
	n += 1
	## Jump ahead
	if n == 256: n = 0x4E00 
fontfile.write("end")
fontfile.close()

with open(fontname.lower().replace(' ','_')+'.png', "wb") as image_file:
	surf.write_to_png(image_file)

