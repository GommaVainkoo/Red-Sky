import random


def get_tile_cordinates(self, t_x1, t_y1):
    t_y1 = t_y1 - self.loop_no
    x1 = self.start_index_x(t_x1)
    y1 = self.start_index_y(t_y1)
    return x1, y1


def update_tile(self):
    for i in range(0, self.no_tiles):
        tile_cord = self.tiles_cord[i]
        xmin, ymin = self.get_tile_cordinates(tile_cord[0], tile_cord[1])
        xmax, ymax = self.get_tile_cordinates(tile_cord[0] + 1, tile_cord[1] + 1)
        x1, y1 = self.transform(xmin, ymin)
        x2, y2 = self.transform(xmax, ymin)
        x3, y3 = self.transform(xmax, ymax)
        x4, y4 = self.transform(xmin, ymax)
        self.Tile[i].points = [x1, y1, x2, y2, x3, y3, x4, y4]



def generate_tiles(self):
    last_y=0
    last_x=0
    start_index = -int(self.no_lines / 2) + 1
    end_index=start_index+self.no_lines-2
#deleteing previous tiles
    for i in range (len(self.tiles_cord)-1,-1,-1):
        if(self.tiles_cord[i][1]<self.loop_no):
            del self.tiles_cord[i]
        if(len(self.tiles_cord)>0):
            last_cord=self.tiles_cord[-1]
            last_y=last_cord[1]+1
            last_x=last_cord[0]

#adding new tiles to screen
    for i in range(len(self.tiles_cord),self.no_tiles):
        r=random.randint(0,2)
        #r values
        #0 means straight
        #1 means right
        #2 means left
        if last_x<=start_index:
            r=1

        if last_x>=end_index:
            r=2
        self.tiles_cord.append((last_x, last_y))
        if r==1:
            last_x+=1
            self.tiles_cord.append((last_x, last_y))
            last_y+= 1
            self.tiles_cord.append((last_x, last_y))
        if r==2:
            last_x-=1
            self.tiles_cord.append((last_x, last_y))
            last_y += 1
            self.tiles_cord.append((last_x, last_y))
        last_y+=1