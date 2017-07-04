import matplotlib
import csv


taglist = []
print "hi"
f=open("collection.csv",'a')
writer=csv.writer(f)
reader=csv.reader(f)

#f.write("hohoho,gdddddddddddggggga")
writer.writerow(['a','b','c'])
f.close()

def plotter():
    print