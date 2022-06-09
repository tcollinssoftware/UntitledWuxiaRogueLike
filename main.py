#####Tanner Collins#####

import room
import map
import random
import player

#instantiate variables for position, room spawning direction, if the first room is in the process of being created
#if the player is in combat, and which turn the player is current in in combat
currentposition = {'y': 7, 'x': 7}
intended_direction = {'y': 7, 'x': 7}
creating_first_room = True
is_in_combat = False
current_turn = 0

#define function for defeat condition screen
def defeat_screen():
    global is_in_combat
    #if the player is still in combat, remove from combat to prevent the rest of the combat func from firing
    if is_in_combat == True:
        is_in_combat == False
    print('You have been slain.')
    print('Game Over')
    print('Relaunch the game to try again.')
    quit()

#define function for victory condition screen
def victory_screen():
    global is_in_combat
    # if the player is still in combat, remove from combat to prevent the rest of the combat func from firing
    if is_in_combat == True:
        is_in_combat == False
    print('The Cursed Emperor grovels before you as he mutters his last breath.')
    print('He is finally defeated, and our lands shall enjoy peace and harmony...')
    print('For the time being.')
    print('********************')
    print('You have completed my short and janky game!')
    print("Congratulations! I probably wouldn't brag too much about it.")
    quit()

def start_game():
    #get global var to determine that the first room is being created
    global creating_first_room
    #call function from map to generate first room
    map.first_room(currentposition, intended_direction, creating_first_room)
    #set first room's status to visited to prevent creation of additional rooms attached to it on revisit
    map.mapmatrix[7][7]['visited'] = True
    #proceed to input handling phase (core game loop)
    player_input_phase()


def combat_phase():
    #separator for legibility
    print('---------------')
    #if the player just entered combat, set combat variable to True
    global is_in_combat
    if is_in_combat == False:
        is_in_combat = True

    #instantiate enemy variable (to get enemy of current room)
    enemy = map.mapmatrix[currentposition['y']][currentposition['x']]['roomenemy']

    #if the player is at 0 hp or below, show defeat screen
    if player.curhp <= 0:
        defeat_screen()

    #core combat loop
    while is_in_combat == True:
        #if the enemy's hp is 0 or below, show exit combat processing
        #if the enemy's name is The Cursed Emperor and the above is also true, show victory screen
        if enemy['Current HP'] <= 0 and enemy['Name'] != 'The Cursed Emperor':
            print('You are victorious! ' + enemy['Name'] + ' has fallen!')
            is_in_combat = False
            player_input_phase()
            return
        if enemy['Current HP'] <= 0 and enemy['Name'] == 'The Cursed Emperor':
            victory_screen()

        #provide enemy and player info (current hp, max hp)
        print('You : ' + str(player.curhp) + '/' + str(player.maxhp) + 'HP')
        print(enemy['Name'] + ' : ' + str(enemy['Current HP']) + '/' + str(enemy['Max HP']) + 'HP')

        #get global combat turn variable
        global current_turn

        #if if the current turn is 0 it's the player's turn, if 1 it's the enemy's turn
        if current_turn == 0:
            #obligatory input prompts
            print('(Type \'commands\' for a list of the in-game commands.)')
            print('It is your turn, what would you like to do?')

            #instantiate input handling variable
            a = input()

            #if player inputs inventory, for each index in the length of the inventory array in the player class
            #print the item's name, type, and count, as well as the description
            #if the player's inventory is empty, tell them
            #return to combat phase (checking inventory doesn't consume your turn)
            if a == 'inventory':
                if len(player.inventory) != 0:
                    for i in player.inventory:
                        print(i['Name'] + ' : ' + i['Item Type'] + ', ' + str(i['Count']))
                        print(i['Desc'])

                if len(player.inventory) == 0:
                    print('You have no items currently.')
                combat_phase()

            #if the player inputs use, get the string and remove the 'use ' portion to get the item name
            if 'use' in a:
                use_string_raw = a
                use_string_new = use_string_raw.replace('use ', '')
                #for each index in the range of the length of the player's inventory
                for i in range(len(player.inventory)):
                    #if the inputted item's name matches the iterated inventory items name
                    if use_string_new in player.inventory[i]['Name']:
                        #and if the iterated item's type is consumable
                        if player.inventory[i]['Item Type'] == 'Consumable':
                            #branch to determine effects of the item
                            #harm adjusts the enemy's hp accordingly
                            #heal adjusts the player's hp accordingly
                            if player.inventory[i]['Use Effect'] == 'Harm':
                                enemy['Current HP'] -= 1
                                print('You used a ' + use_string_new + '.')
                                print(enemy['Name'] + ' took one damage.')
                                #adjust inventory after use
                                if player.inventory[i]['Count'] > 1:
                                    player.inventory[i]['Count'] -= 1
                                if player.inventory[i]['Count'] == 1:
                                    player.inventory.pop(i)
                                #set turn to enemy turn
                                current_turn = 1
                                combat_phase()
                            if player.inventory[i]['Use Effect'] == 'Heal':
                                player.curhp += 1
                                print('You used a ' + use_string_new + '.')
                                print('You have recovered one HP.')
                                print('Your current HP is ' + str(player.curhp) + '/' + str(player.maxhp) + '.')
                                if player.inventory[i]['Count'] > 1:
                                    player.inventory[i]['Count'] -= 1
                                if player.inventory[i]['Count'] == 1:
                                    player.inventory.pop(i)
                                current_turn = 1
                                combat_phase()
                        #if the item type isn't consumable, inform the player that the item can't be used (and is a passive)
                        if player.inventory[i]['Item Type'] != 'Consumable':
                            print('That item is not usable.')
                current_turn = 1
                combat_phase()

            #display list of commands for combat, don't consume turn
            if 'commands' in a:
                print('Player Turn : {attack left, attack up, attack right, use <item name>, inventory}')
                print('Enemy Turn : {defend left, defend up, defend right}')
                combat_phase()

            #for the input attack direction, since there are three attack directions
            #there is a one in three chance of the enemy attacking or defending in that direction
            if a == 'attack left':
                #generate a random number from one to three
                enemy_defended = random.randint(1,3)
                #if the enemy rolled the highest, they successfully defended
                if enemy_defended == 3:
                    print(enemy['Name'] + ' defended your attack and took no damage.')
                #if they rolled the other two options, they took the damage
                if enemy_defended != 3:
                    print(enemy['Name'] + ' took ' + str(player.damage) + ' damage.')
                    enemy['Current HP'] -= player.damage
                current_turn = 1
                combat_phase()
            if a == 'attack up':
                enemy_defended = random.randint(1,3)
                if enemy_defended == 3:
                    print(enemy['Name'] + ' defended your attack and took no damage.')
                if enemy_defended != 3:
                    print(enemy['Name'] + ' took ' + str(player.damage) + ' damage.')
                    enemy['Current HP'] -= player.damage
                current_turn = 1
                combat_phase()
            if a == 'attack right':
                enemy_defended = random.randint(1,3)
                if enemy_defended == 3:
                    print(enemy['Name'] + ' defended your attack and took no damage.')
                if enemy_defended != 3:
                    print(enemy['Name'] + ' took ' + str(player.damage) + ' damage.')
                    enemy['Current HP'] -= player.damage
                current_turn = 1
                combat_phase()

        #set turn to enemy's turn
        if current_turn == 1:
            print('(Type \'commands\' for a list of the in-game commands.)')
            print("It is the enemy's turn, what would you like to do?")
            a = input()
            if 'commands' in a:
                print('Player Turn : {attack left, attack up, attack right, use <item name>, inventory}')
                print('Enemy Turn : {defend left, defend up, defend right}')
                combat_phase()

            #the player can still check inventory on the player's turn
            if a == 'inventory':
                if len(player.inventory) != 0:
                    for i in player.inventory:
                        print(i['Name'] + ' : ' + i['Item Type'] + ', ' + str(i['Count']))
                        print(i['Desc'])

                if len(player.inventory) == 0:
                    print('You have no items currently.')
                combat_phase()

            #defending works just like attacking, but the attack direction is being rolled
            if a == 'defend left':
                enemy_attacked = random.randint(1, 3)
                if enemy_attacked == 3:
                    print('You defended ' + enemy['Name'] + "'s attack and took no damage.")
                if enemy_attacked != 3:
                    print('You took ' + str(enemy['Damage']) + ' damage')
                    player.curhp -= enemy['Damage']
                current_turn = 0
                combat_phase()
            if a == 'defend up':
                enemy_attacked = random.randint(1, 3)
                if enemy_attacked == 3:
                    print('You defended ' + enemy['Name'] + "'s attack and took no damage.")
                if enemy_attacked != 3:
                    print('You took ' + str(enemy['Damage']) + ' damage')
                    player.curhp -= enemy['Damage']
                current_turn = 0
                combat_phase()
            if a == 'defend right':
                enemy_attacked = random.randint(1, 3)
                if enemy_attacked == 3:
                    print('You defended ' + enemy['Name'] + "'s attack and took no damage.")
                if enemy_attacked != 3:
                    print('You took ' + str(enemy['Damage']) + ' damage.')
                    player.curhp -= enemy['Damage']
                current_turn = 0
                combat_phase()

#define input phase function (core gameplay loop)
def player_input_phase():
    #get globals for combat, set them to default values of 0 and False (player turn and out of combat)
    global current_turn
    if current_turn == 1:
        current_turn = 0
    global is_in_combat
    if is_in_combat == True:
        is_in_combat == False
    global creating_first_room
    #print map info
    map.print_map(currentposition)
    #tell the player where they are and what they see by calling the map matrix and getting info from it's stored dict for your position
    print('You find yourself at the ' + map.mapmatrix[currentposition['y']][currentposition['x']]['roomtype'] + ' of the ' + map.mapmatrix[currentposition['y']][currentposition['x']]['roomname'] + '.')
    #if the room has an enemy, inform the player
    #if the enemy is defeated, inform the player
    if map.mapmatrix[currentposition['y']][currentposition['x']]['roomenemy'] != 'None':
        if map.mapmatrix[currentposition['y']][currentposition['x']]['roomenemy']['Current HP'] > 0:
            print('The enemy ' + map.mapmatrix[currentposition['y']][currentposition['x']]['roomenemy']['Name'] + ' stands before you.')
        if map.mapmatrix[currentposition['y']][currentposition['x']]['roomenemy']['Current HP'] <= 0:
            print('The enemy ' + map.mapmatrix[currentposition['y']][currentposition['x']]['roomenemy']['Name'] + ' lay defeated at your feet.')
    # check neighboring rooms, append to a list of neighboring rooms
    neighborrooms = []
    if map.mapmatrix[currentposition['y'] - 1][currentposition['x']]:
        neighborrooms.append('north')
    if map.mapmatrix[currentposition['y'] + 1][currentposition['x']]:
        neighborrooms.append('south')
    if map.mapmatrix[currentposition['y']][currentposition['x'] - 1]:
        neighborrooms.append('west')
    if map.mapmatrix[currentposition['y']][currentposition['x'] + 1]:
        neighborrooms.append('east')
    #if there are rooms adjacent to the player's current position (and there will be), inform the player
    #differentiate between singular and plural
    if len(neighborrooms) == 1:
        print('There is a room to the ' + neighborrooms[0] + ' of you.')
    if len(neighborrooms) == 2:
        print('There are rooms to the ' + neighborrooms[0] + ' and ' + neighborrooms[1] + ' of you.')
    if len(neighborrooms) == 3:
        print('There are rooms to the ' + neighborrooms[0] + ', ' + neighborrooms[1] + ', and ' + neighborrooms[
            2] + ' of you.')
    if len(neighborrooms) == 4:
        print('There are rooms to the ' + neighborrooms[0] + ', ' + neighborrooms[1] + ', ' + neighborrooms[
            2] + ', and ' + neighborrooms[3] + ' of you.')

    #display prompt for input and help information
    print('(Type \'commands\' for a list of the in-game commands.)')
    print(str(room.roomcount) + ' rooms discovered.')
    print('What would you like to do?')

    #get player input
    a = input()

    #if player inputs commands
    if a == 'commands':
        command_list = [
            {'Command': 'commands', 'Description': 'Shows list of commands.'},
            {'Command': 'travel <cardinal direction>', 'Description': 'Moves in user-specified direction.'},
            {'Command': 'challenge', 'Description': 'Challenges the enemy in your current room to combat.'},
            {'Command': 'loot', 'Description': 'Picks item up from defeated enemy corpse.'},
            {'Command': 'inventory', 'Description': 'Displays current player inventory and descriptions.'},
            {'Command': 'use <item name>', 'Description': 'Uses specified item from inventory.'}
        ]
        #iterate over the command list, and print each command and it's description
        for i in command_list:
            print(i['Command'] + ' : ' + i['Description'])
        player_input_phase()

    #if player inputs inventory, iterate the length of inventory and print each item's name, type, count, and description
    #if the player's inventory is empty, inform them
    if a == 'inventory':
        if len(player.inventory) != 0:
            for i in player.inventory:
                print(i['Name'] + ' : ' + i['Item Type'] + ', ' + str(i['Count']))
                print(i['Desc'])

        if len(player.inventory) == 0:
            print('You have no items currently.')
        player_input_phase()

    #if the player inputs use, get the string and remove the 'use ' portion to get the item name
    if 'use' in a:
        use_string_raw = a
        use_string_new = use_string_raw.replace('use ', '')
        #iterate over the range of the length of the player inventory
        for i in range(len(player.inventory)):
            #if the item's name matches the name of the iteration index
            if use_string_new in player.inventory[i]['Name']:
                #and if the item type is consumable
                if player.inventory[i]['Item Type'] == 'Consumable':
                    #branch to determine use effects
                    if player.inventory[i]['Use Effect'] == 'Harm':
                        #since Harm targets enemies, it can only be used in combat
                        print('You can only use this item in combat.')
                    #heal gives the player back a health point
                    if player.inventory[i]['Use Effect'] == 'Heal':
                        player.curhp += 1
                        print('You used a ' + use_string_new + '.')
                        print('You have recovered one HP.')
                        print('Your current HP is ' + str(player.curhp) + '/' + str(player.maxhp) + '.')
                        #adjust inventory accordingly
                        if player.inventory[i]['Count'] > 1:
                            player.inventory[i]['Count'] -= 1
                        if player.inventory[i]['Count'] == 1:
                            player.inventory.pop(i)
                        player_input_phase()
                #if the item isn't consumable, tell the player
                if player.inventory[i]['Item Type'] != 'Consumable':
                    print('That item is not usable.')
        player_input_phase()

    #if player inputs loot
    if a == 'loot':
        #instantiate variables to hold enemy and enemy's item information
        room_enemy = map.mapmatrix[currentposition['y']][currentposition['x']]['roomenemy']
        room_item = map.mapmatrix[currentposition['y']][currentposition['x']]['roomenemy']['Item']
        #if there is an enemy
        if room_enemy != 'None':
            #and if that enemy is defeated
            if room_enemy['Current HP'] <= 0:
                #and if the enemy is still holding an item
                if room_enemy['Item'] != '':
                    #tell the player they've looted the item
                    print('You obtained ' + str(room_item['Count']) + ' ' + room_item['Name'] + '!')
                    #branch if the item is Equipment, and has a passive bonus
                    if room_enemy['Item']['Item Type'] == 'Equipment':
                        #if HP Up is the buff, increase current and max hp, inform the player
                        if room_enemy['Item']['Buff'] == 'HP Up':
                            player.curhp += 1
                            player.maxhp += 1
                            print('Your current and maximum HP have been increased by one.')
                        #if Damage Up is the buff, increase the player's damage int, inform the player
                        if room_enemy['Item']['Buff'] == 'Damage Up':
                            player.damage += 1
                            print('Your damage has been increased by one.')
                    #append the item to the player's inventory
                    player.inventory.append(room_item)
                    #remove the item from the enemy
                    room_enemy['Item'] = ''
                    player_input_phase()
                #if the enemy corpse is empty, tell the player
                if room_enemy['Item'] == '':
                    print("You've already looted this enemy.")
                    player_input_phase()
            #if the enemy isn't defeated, tell the player
            if room_enemy['Current HP'] > 0:
                print('That enemy is still alive.')
                player_input_phase()
        #if there isn't an enemy in the room, tell the player
        if room_enemy == 'None':
            print('There is no enemy here.')
            player_input_phase()

    #if input is challenge
    if a == 'challenge':
        #if there is an enemy in the room
        if map.mapmatrix[currentposition['y']][currentposition['x']]['roomenemy'] != 'None':
            #and if the enemy isn't defeated
            if map.mapmatrix[currentposition['y']][currentposition['x']]['roomenemy']['Current HP'] > 0:
                #start combat
                combat_phase()
                return
            #if the enemy is defeated, tell the player
            if map.mapmatrix[currentposition['y']][currentposition['x']]['roomenemy']['Current HP'] <= 0:
                print(map.mapmatrix[currentposition['y']][currentposition['x']]['roomenemy']['Name'] + ' is already defeated.')
                player_input_phase()
        #if there isn't an enemy in the room, tell the player
        if map.mapmatrix[currentposition['y']][currentposition['x']]['roomenemy'] == "None":
            print('There is no enemy to challenge here.')
            player_input_phase()

    #if input is travel
    kwtravel = 'travel'
    if kwtravel in a:
        #because this will be ran the first time the player travels, this stops the first room creation process
        #this allows every new room to generate rooms as you move into them
        creating_first_room = False
        #if the player inputs travel and a direction, and there IS a room in that direction, and that room is a neighboring room to your current room
        #each of the branches per cardinal direction are the same functionally, so I'm only commenting the first one
        if a == 'travel north' and map.mapmatrix[currentposition['y'] - 1][currentposition['x']] and map.mapmatrix[currentposition['y']][currentposition['x']]['roomid'] in map.mapmatrix[currentposition['y'] - 1][currentposition['x']]['connectedrooms']:
            #update the intended direction of movement
            intended_direction.update({'y': currentposition['y'] - 1, 'x': currentposition['x']})
            #if the room in the intended direction hasn't been visited before
            if not map.mapmatrix[currentposition['y'] - 1][currentposition['x']]['visited'] == True:
                #run room creation function in room class
                room.create_rooms(currentposition, intended_direction, creating_first_room)
                #set the room to visited (as you are moving into the room) so it doesn't generate more rooms
                map.mapmatrix[currentposition['y'] - 1][currentposition['x']]['visited'] = True
            #update player's current position to the new position
            currentposition['y'] = currentposition['y'] - 1
            #return to input processing
            player_input_phase()
        elif a == 'travel south' and map.mapmatrix[currentposition['y'] + 1][currentposition['x']] and map.mapmatrix[currentposition['y']][currentposition['x']]['roomid'] in map.mapmatrix[currentposition['y'] + 1][currentposition['x']]['connectedrooms']:
            intended_direction.update({'y': currentposition['y'] + 1, 'x': currentposition['x']})
            if not map.mapmatrix[currentposition['y'] + 1][currentposition['x']]['visited'] == True:
                room.create_rooms(currentposition, intended_direction, creating_first_room)
                map.mapmatrix[currentposition['y'] + 1][currentposition['x']]['visited'] = True
            currentposition['y'] = currentposition['y'] + 1
            player_input_phase()
        elif a == 'travel west' and map.mapmatrix[currentposition['y']][currentposition['x'] - 1] and map.mapmatrix[currentposition['y']][currentposition['x']]['roomid'] in map.mapmatrix[currentposition['y']][currentposition['x'] - 1]['connectedrooms']:
            intended_direction.update({'y': currentposition['y'], 'x': currentposition['x'] - 1})
            if not map.mapmatrix[currentposition['y']][currentposition['x'] - 1]['visited'] == True:
                room.create_rooms(currentposition, intended_direction, creating_first_room)
                map.mapmatrix[currentposition['y']][currentposition['x'] - 1]['visited'] = True
            currentposition['x'] = currentposition['x'] - 1
            player_input_phase()
        elif a == 'travel east' and map.mapmatrix[currentposition['y']][currentposition['x'] + 1] and map.mapmatrix[currentposition['y']][currentposition['x']]['roomid'] in map.mapmatrix[currentposition['y']][currentposition['x'] + 1]['connectedrooms']:
            intended_direction.update({'y': currentposition['y'], 'x': currentposition['x'] + 1})
            if not map.mapmatrix[currentposition['y']][currentposition['x'] + 1]['visited'] == True:
                room.create_rooms(currentposition, intended_direction, creating_first_room)
                map.mapmatrix[currentposition['y']][currentposition['x'] + 1]['visited'] = True
            currentposition['x'] = currentposition['x'] + 1
            player_input_phase()
        #if player JUST inputs travel, inform them to add a direction to their input
        elif a == 'travel':
            print('Please specify the direction you would like to travel.')
            print('Ex:\'travel east\'')
            player_input_phase()
        #else there's not a room in that direction, inform the player
        else:
            print('There is no room in that direction.')
            player_input_phase()

#start the game
start_game()

