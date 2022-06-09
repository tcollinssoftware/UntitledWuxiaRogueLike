class Map:

    def __init__(self):
        print(mapmatrix)
        return

import room
import copy

#####Establish the map matrix that will house rooms and be used for coordinates#####
mapmatrix = [
    [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}],
    [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}],
    [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}],
    [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}],
    [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}],
    [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}],
    [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}],
    [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}],
    [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}],
    [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}],
    [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}],
    [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}],
    [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}],
    [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}],
    [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}]
]

def first_room(currentposition, intended_direction, creating_first_room):
    room.create_starting_room(currentposition, intended_direction, creating_first_room)

#####Make and Output the Display of the Map#####
def print_map(currentposition):
    mapdisplay = copy.deepcopy(mapmatrix)

    #assign character representation to matrix values
    mapstr_array = []
    for y in range(len(mapdisplay)):
        mapstr = ""
        for x in range(len(mapdisplay[y])):
            if mapdisplay[y][x]:
                if y == currentposition['y'] and x == currentposition['x']:
                    mapdisplay[y][x] = '@'
                else:
                    mapdisplay[y][x] = '\u25A0'
                mapstr += str(mapdisplay[y][x])
            if not mapdisplay[y][x]:
                mapdisplay[y][x] = 'x'
                mapstr += str(mapdisplay[y][x])

        mapstr_array.append(mapstr)
    #flip displayed map to proper layout
    # for i in reversed(mapstr_array):
    #     print(i)
    for i in mapstr_array:
        print(i)
    print('---------------')
