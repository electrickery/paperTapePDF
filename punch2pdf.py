#!/bin/python3
#
from fpdf import FPDF

import sys

version = "0.1.0"

fileName = sys.argv[1]
file = open(fileName, "r") 
lines = file.readlines()

# https://en.wikipedia.org/wiki/Punched_tape
# Dimensions

# Tape for punching was usually 0.00394 inches (0.1 mm) thick. The two most common widths 
# were 11/16 inch (17.46 mm) for five bit codes, and 1 inch (25.4 mm) for tapes with six or 
# more bits. 
# Hole spacing was 0.1 inch (2.54 mm) in both directions. 
# Data holes were 0.072 inches (1.83 mm) in diameter; 
# sprocket feed holes were 0.046 inches (1.17 mm). 

pdf = FPDF()
pdf.add_page()

inch = 25.4

grid = 0.1 * inch
hole = 0.072 * inch
sprocketHole = 0.046 * inch

lineStartX = 4.0
lineStartY = 12.5
pageLength = 280
columns = 8

# plot a hole
def plotHole (canvas, xOffset, yOffset, grid, hole):
    x = xOffset + (grid - hole) / 2
    w = hole
    y = yOffset + (grid - hole) / 2
    h = hole
    canvas.ellipse(x, y, w, h, style='F')

# plot a byte, including sprocket hole
def plotByte (canvas, char, xOffset, yOffset, grid, hole, sprocketHole):
    sprocketOffset = grid
    pattern = ""
    plotHole(canvas, xOffset + grid * 3, yOffset, grid, sprocketHole)
    for bit in range(7, -1, -1):
        if (bit < 3):
            sprocketOffset = 0
        if (ord(char) & 1 << bit):
            bitVal = 1
            plotHole(canvas, sprocketOffset + xOffset + grid * bit, yOffset, grid, hole)
        else:
            bitVal = "0"
        pattern += str(bitVal)
    print(pattern)

def linesNumbers (canvas, inch, lineStartX, lineStartY, pageLength, columns, startCol):
    # Column numbers
    for col in range(0, 8):
        colNumX =  (col + 1) * inch - inch / 2
        canvas.set_xy(colNumX, 4)
        canvas.set_font('arial', 'B', 13.0)
        canvas.cell(ln=0, h=5.0, align='L', w=0, txt=str(col + startCol), border=0)
    # Lines vertical
    lineEndX = lineStartX + (columns) * inch
    lineEndY = pageLength + lineStartY - grid
    for lin in range(0, columns + 1):
        lineX = lineStartX + lin * inch
        canvas.line(lineX, lineStartY, lineX, lineEndY)
    # Lines horizontal
    canvas.line(lineStartX, lineStartY, lineEndX, lineStartY)
    canvas.line(lineStartX, lineEndY, lineEndX, lineEndY)

startCol = 0
linesNumbers (pdf, inch, lineStartX, lineStartY, pageLength, columns, startCol)
startCol += 8

runningX = lineStartX + 1
runningY = lineStartY

for line in lines:
    bytesPerColumn = pageLength + lineStartY - grid * 2
    lineStrip = line.strip()
    for chr in lineStrip:
        plotByte(pdf, chr, runningX, runningY, grid, hole, sprocketHole)
        runningY += grid
#        print(str(round(runningY, 2)) + " : " + chr)
        if (runningY > bytesPerColumn):
            if (runningX > 7 * inch):
                pdf.add_page()
                linesNumbers (pdf, inch, lineStartX, lineStartY, pageLength, columns, startCol)
                startCol += 8
                runningX = lineStartX + 1 - inch
                runningY = lineStartY
                next
            runningX += inch
            runningY = lineStartY
            
pdf.output(fileName + '.pdf', 'F')
#
