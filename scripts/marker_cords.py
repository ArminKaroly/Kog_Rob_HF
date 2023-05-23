
class Markers:
    def __init__(self):
        self.markers=[]

    def markers_build(self):
        for y in range(9):
            for x in range(9):
                self.markers.append([-4+x,-2+y,2.5,0,0,0])
        
        self.markers.append([-5,5,2.5,0,0,0])
        self.markers.append([-6,5,2.5,0,0,0])
        self.markers.append([-5,6,2.5,0,0,0])
        self.markers.append([-6,6,2.5,0,0,0])
    
    def markers_array(self):
        self.markers_build()
        return self.markers
        
if __name__ == '__main__':
    marker=Markers()
    print(marker.markers_array())