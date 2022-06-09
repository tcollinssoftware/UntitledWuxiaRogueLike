class Room:
#declare class and parameters
    def __init__(self, roomid, roomtype, name, enemy, mapx, mapy, visited, connectedrooms):
        self.roomid = roomid
        self.roomtype = roomtype
        self.name = name
        self.enemy = enemy
        self.mapx = mapx
        self.mapy = mapy
        self.visited = visited
        self.connectedrooms = connectedrooms

import random
import map
import enemies

#global var to keep track of how many rooms can be generated
roomcount = 0

#list of available room types
roomtypes = [
    'Barracks', 'Hall', 'Temple', 'Armory', 'Courtyard', 'Vault', 'Throne Room', 'Library', 'Dungeon',
    'War Room', 'Garden', 'Tea Room', 'Shrine', 'Pond'
]

#list of parts of the room's name
namesubj = [
    'Orchid', 'Lion', 'Dragon', 'Phoenix', 'Tiger', 'Monkey', 'Bull', 'Ox', 'Crane', 'Leopard', 'Hornet', 'Bear', 'Swallow', 'Widow', 'Carp',
    'Rooster', 'Swan', 'Cicada', 'Raven', 'Stag', 'Dragonfly', 'Elk', 'Falcon', 'Toad', 'Tortoise', 'Serpent', 'Fox', 'Wolf', 'Panda',
    'Grasshopper', 'Hare', 'Stallion', 'Ibex', 'Ibis', 'Kingfisher', 'Locust', 'Magpie', 'Mongoose', 'Otter', 'Peacock', 'Swine', 'Swan',
    'Mastiff', 'Peony', 'Chrysanthemum', 'Camellia', 'Azalea', 'Hibiscus', 'Magnolia', 'Arrow', 'Serpent', 'Down', 'Gale', 'Wind'
]

#list of parts of the room's name
nameadj = [
    'Pale', 'Ancient', 'Antique', 'Blue', 'Broken', 'Early', 'Fine', 'Howling', 'Mighty', 'Singing', 'Bronzen', 'Coral', 'Diamond',
    'Jade', 'Golden', 'Silver', 'Opal', 'Turquoise', 'Amber', 'Amethyst', 'Sapphire', 'Ruby', 'Crimson', 'Onyx', 'Blood', 'Topaz',
    'Noble', 'Pure', 'Immortal', 'Eternal', 'Shining', 'Vivid', 'Iron', 'Lunar', 'Solar', 'Celestial', 'Sacred', 'Divine', 'Yellow', 'Red', 'White',
    'Black', 'Dancing', 'Hidden', 'Blind', 'Deaf', 'Imperial', 'Silent', 'Joyous', 'Forbidden'
]

#define func to create the starting room
def create_starting_room(currentposition, intended_direction, creating_first_room):
    global roomcount
    #generate the room and store in a var, assigning random choices per parameter
    r1 = Room(roomcount + 1, str(random.choice(roomtypes)), str(random.choice(nameadj) + " " + random.choice(namesubj)), enemies.generate_enemy(), 0, 0, False, [])
    #create room dictionary to contain generated information
    roomdict = {'roomid': r1.roomid, 'roomtype': 'Gate', 'roomname': r1.name, 'roomenemy': 'None', 'roomx': 7, 'roomy': 7, 'visited': False, 'connectedrooms': []}
    #set the room dictionary as the value at the index of the map matrix
    map.mapmatrix[7][7] = roomdict
    #increase room count by one
    roomcount = roomcount + 1
    #create adjacent rooms
    create_rooms(currentposition, intended_direction, creating_first_room)

#define func to create rooms
def create_rooms(currentposition, intended_direction, creating_first_room):
    #if you've just created the first room and are creating the rooms attached to it, use your current position as the origin
    #if not, use your intended movement direction (so rooms are created attached to the room that you're moving into)
    if creating_first_room == True:
        room_origin = currentposition
    if creating_first_room == False:
        room_origin = intended_direction

    global roomcount

    #if roomcount is less than seven
    if roomcount < 7:
        #instantiate variable to hold amount of rooms needing to be created
        rooms_to_make = 0
        #flip a coin
        room_flip = random.randint(0,2)
        #instantiate two lists for the directions the rooms are intended to be placed
        intended_dir_1 = []
        intended_dir_2 = []
        #if the coin flip returned 0, make one room, if 1, make two rooms
        if room_flip == 0 or room_flip == 1:
            rooms_to_make = 1
        if room_flip == 2:
            rooms_to_make = 2
        #list of all cardinal directions for room generation to select from
        available_directions = ['north', 'south', 'west', 'east']

        #per each cardinal direction, if there is a room already in that direction, remove that direction from the list
        #of available directions to place a new room
        if map.mapmatrix[room_origin['y']][room_origin['x'] - 1]:
            available_directions.remove('west')
        if map.mapmatrix[room_origin['y']][room_origin['x'] + 1]:
            available_directions.remove('east')
        if map.mapmatrix[room_origin['y'] - 1][room_origin['x']]:
            available_directions.remove('north')
        if map.mapmatrix[room_origin['y'] + 1][room_origin['x']]:
            available_directions.remove('south')

        #if there are two or more available directions
        if len(available_directions) >= 2:
            #sample two directions from the available directions list
            intended_direction = random.sample(available_directions, 2)
            #iterating the int for how many rooms to make
            for i in range(rooms_to_make):
                #generate the room procedurally, using choices
                r1 = Room(roomcount + 1, str(random.choice(roomtypes)), str(random.choice(nameadj) + " " + random.choice(namesubj)), enemies.generate_enemy(), 0, 0, False, [])
                #create the room dictionary
                roomdict = {'roomid': r1.roomid, 'roomtype': r1.roomtype, 'roomname': r1.name, 'roomenemy': r1.enemy, 'roomx': room_origin['x'] - 1, 'roomy': room_origin['y'], 'visited': False, 'connectedrooms': []}
                #if this is the final room, make it the Boss Room, and generate Boss as enemy
                if roomdict['roomid'] == 8:
                    roomdict['roomtype'] = 'Throne'
                    roomdict['roomname'] = 'Cursed Emperor'
                    roomdict['roomenemy'] = enemies.generate_boss()
                #add the current room as a neighbor to the new room
                roomdict['connectedrooms'].append(map.mapmatrix[room_origin['y']][room_origin['x']]['roomid'])
                #add the new room as a neighbor to the current room
                map.mapmatrix[room_origin['y']][room_origin['x']]['connectedrooms'].append(roomdict['roomid'])
                #per direction selected from the available, set the room's vector2 (xy) coordinates accordingly
                if intended_direction[i] == 'north':
                    roomdict['roomx'] = room_origin['x']
                    roomdict['roomy'] = room_origin['y'] - 1
                if intended_direction[i] == 'south':
                    roomdict['roomx'] = room_origin['x']
                    roomdict['roomy'] = room_origin['y'] + 1
                if intended_direction[i] == 'west':
                    roomdict['roomx'] = room_origin['x'] - 1
                    roomdict['roomy'] = room_origin['y']
                if intended_direction[i] == 'east':
                    roomdict['roomx'] = room_origin['x'] + 1
                    roomdict['roomy'] = room_origin['y']
                #place the new room in the mapmatrix at it's coordinates
                map.mapmatrix[roomdict['roomy']][roomdict['roomx']] = roomdict
                #increase roomcount
                roomcount += 1
        #if available directions is only one
        if len(available_directions) == 1:
            #ensure only one room is made
            rooms_to_make = 1
            #sample one intended direction
            intended_direction = random.sample(available_directions, 1)
            #these steps are the same as the above steps
            for i in range(rooms_to_make):
                r1 = Room(roomcount + 1, str(random.choice(roomtypes)), str(random.choice(nameadj) + " " + random.choice(namesubj)), enemies.generate_enemy(), 0, 0, False, [])
                roomdict = {'roomid': r1.roomid, 'roomtype': r1.roomtype, 'roomname': r1.name, 'roomenemy': r1.enemy, 'roomx': room_origin['x'] - 1, 'roomy': room_origin['y'], 'visited': False, 'connectedrooms': []}
                if roomdict['roomid'] == 8:
                    roomdict['roomtype'] = 'Throne'
                    roomdict['roomname'] = 'Cursed Emperor'
                    roomdict['roomenemy'] = enemies.generate_boss()
                roomdict['connectedrooms'].append(map.mapmatrix[room_origin['y']][room_origin['x']]['roomid'])
                map.mapmatrix[room_origin['y']][room_origin['x']]['connectedrooms'].append(roomdict['roomid'])
                if intended_direction[i] == 'north':
                    roomdict['roomx'] = room_origin['x']
                    roomdict['roomy'] = room_origin['y'] - 1
                if intended_direction[i] == 'south':
                    roomdict['roomx'] = room_origin['x']
                    roomdict['roomy'] = room_origin['y'] + 1
                if intended_direction[i] == 'west':
                    roomdict['roomx'] = room_origin['x'] - 1
                    roomdict['roomy'] = room_origin['y']
                if intended_direction[i] == 'east':
                    roomdict['roomx'] = room_origin['x'] + 1
                    roomdict['roomy'] = room_origin['y']
                map.mapmatrix[roomdict['roomy']][roomdict['roomx']] = roomdict
                roomcount += 1
        #if there are less than one available directions, don't make a room
        if len(available_directions) < 1:
            pass

    #if room count is 7, ensure that only one room is made
    #other than that, the rest of this functions the same as the above code
    if roomcount == 7:

        rooms_to_make = 1
        intended_dir_1 = []
        intended_dir_2 = []

        available_directions = ['north', 'south', 'west', 'east']

        if map.mapmatrix[room_origin['y']][room_origin['x'] - 1]:
            available_directions.remove('west')
        if map.mapmatrix[room_origin['y']][room_origin['x'] + 1]:
            available_directions.remove('east')
        if map.mapmatrix[room_origin['y'] - 1][room_origin['x']]:
            available_directions.remove('north')
        if map.mapmatrix[room_origin['y'] + 1][room_origin['x']]:
            available_directions.remove('south')

        if len(available_directions) >= 2:
            intended_direction = random.sample(available_directions, 2)
            for i in range(rooms_to_make):
                r1 = Room(roomcount + 1, str(random.choice(roomtypes)), str(random.choice(nameadj) + " " + random.choice(namesubj)), enemies.generate_enemy(), 0, 0, False, [])
                roomdict = {'roomid': r1.roomid, 'roomtype': r1.roomtype, 'roomname': r1.name, 'roomenemy': r1.enemy, 'roomx': room_origin['x'] - 1, 'roomy': room_origin['y'], 'visited': False, 'connectedrooms': []}
                if roomdict['roomid'] == 8:
                    roomdict['roomtype'] = 'Throne'
                    roomdict['roomname'] = 'Cursed Emperor'
                    roomdict['roomenemy'] = enemies.generate_boss()
                roomdict['connectedrooms'].append(map.mapmatrix[room_origin['y']][room_origin['x']]['roomid'])
                map.mapmatrix[room_origin['y']][room_origin['x']]['connectedrooms'].append(roomdict['roomid'])
                if intended_direction[i] == 'north':
                    roomdict['roomx'] = room_origin['x']
                    roomdict['roomy'] = room_origin['y'] - 1
                if intended_direction[i] == 'south':
                    roomdict['roomx'] = room_origin['x']
                    roomdict['roomy'] = room_origin['y'] + 1
                if intended_direction[i] == 'west':
                    roomdict['roomx'] = room_origin['x'] - 1
                    roomdict['roomy'] = room_origin['y']
                if intended_direction[i] == 'east':
                    roomdict['roomx'] = room_origin['x'] + 1
                    roomdict['roomy'] = room_origin['y']
                map.mapmatrix[roomdict['roomy']][roomdict['roomx']] = roomdict
                roomcount += 1
        if len(available_directions) == 1:
            rooms_to_make = 1
            intended_direction = random.sample(available_directions, 1)
            for i in range(rooms_to_make):
                r1 = Room(roomcount + 1, str(random.choice(roomtypes)), str(random.choice(nameadj) + " " + random.choice(namesubj)), enemies.generate_enemy(), 0, 0, False, [])
                roomdict = {'roomid': r1.roomid, 'roomtype': r1.roomtype, 'roomname': r1.name, 'roomenemy': r1.enemy, 'roomx': room_origin['x'] - 1, 'roomy': room_origin['y'], 'visited': False, 'connectedrooms': []}
                if roomdict['roomid'] == 8:
                    roomdict['roomtype'] = 'Throne'
                    roomdict['roomname'] = 'Cursed Emperor'
                    roomdict['roomenemy'] = enemies.generate_boss()
                roomdict['connectedrooms'].append(map.mapmatrix[room_origin['y']][room_origin['x']]['roomid'])
                map.mapmatrix[room_origin['y']][room_origin['x']]['connectedrooms'].append(roomdict['roomid'])
                if intended_direction[i] == 'north':
                    roomdict['roomx'] = room_origin['x']
                    roomdict['roomy'] = room_origin['y'] - 1
                if intended_direction[i] == 'south':
                    roomdict['roomx'] = room_origin['x']
                    roomdict['roomy'] = room_origin['y'] + 1
                if intended_direction[i] == 'west':
                    roomdict['roomx'] = room_origin['x'] - 1
                    roomdict['roomy'] = room_origin['y']
                if intended_direction[i] == 'east':
                    roomdict['roomx'] = room_origin['x'] + 1
                    roomdict['roomy'] = room_origin['y']
                map.mapmatrix[roomdict['roomy']][roomdict['roomx']] = roomdict
                roomcount += 1
        if len(available_directions) < 1:
            pass