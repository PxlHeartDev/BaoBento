import matplotlib.pyplot as mpl
import numpy as np

# line 1 points
x1 = [1,2,3,4]
y1 = [2,4,1,3]
# plotting the line 1 points 
#mpl.plot(x1, y1, label = "line 1")
 
# line 2 points
x2 = [1,2,3,4]
y2 = [4,1,3,2]
# plotting the line 2 points 
#mpl.plot(x2, y2, label = "line 2")
 
# naming the x axis
mpl.xlabel('x - axis')
# naming the y axis
mpl.ylabel('y - axis')
# giving a title to my graph
mpl.title('Two lines on same graph!')

 
graphData = {"Chimken": [0, 2, 1, 5], "Pongo": [1, 4, 9, 0]}
xTicks = []
maxy = 0
for k, v in graphData.items():
    xTicks.append(k)
    for y in v:
        if(y > maxy): maxy = y
    mpl.plot([0] + [i for i in range(0, len(v))], [0] + v, label=k)
    
mpl.xticks([1, 2], xTicks)
mpl.yticks([y for y in range(0, maxy + 1)])
# y = np.array([[1, 2], [3, 4], [5, 6]])
# mpl.plot(x, y)

# show a legend on the plot
mpl.legend()
 
# function to show the plot#
mpl.show()



