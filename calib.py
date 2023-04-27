import numpy
x = [220,190,180,170,160,150,110,90]
y = [90,80,70,60,50,40,30,20]
a,b,c = numpy.polyfit(x,y,2)
print(a,b,c)