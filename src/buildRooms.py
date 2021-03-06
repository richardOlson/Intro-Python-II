
from room import Room
from monster import Monster
from  item import *
from random import sample , choice
# Declare all the rooms

room = {
    'outside':  Room("Outside Cave Entrance",
                     "North of you, the cave mount beckons.", is_light=True, items_in_room=[Item("rope", "a long old rope")], 
                     animal_monster=Monster("Jerry", weakness="rope", description="ravenous warthog")),

    'foyer':    Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east.""", is_light=True, items_in_room=[LightSource("flashlight",  "battery operated flashlight")]),

    'overlook': Room("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm.""", dark_description=""""Wow, It is so dark in here!
Ahead to the north, a small light flickers"""
,items_in_room=[Shovel("shovel", "long old shovel")]),

    'narrow':   Room("Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air.""", dark_description="""The smell of gold permeates the air"""),

    'treasure': Room("Treasure Chamber", """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exits are to the south and a small tunnel to the east""", 
dark_description="""You are close, don't give up!"""),

    "tunnel": Room("Tunnel", """Your inside a tunnel.  
This tunnel is only large enough to crawl through continuing to the east. """, dark_description="""You can't see anything.
But you managed to begin crawling into the tunnel. You just felt something touch your hand!""",
 is_light=False, animal_monster=Monster("Dirk the snake", "shovel", description="a rattle snake")),

    "great chamber": Room("Great Chamber", dark_description="""Man it is dark inside here. You can't here anything but you can hear 
some water flowing.""" ,description="""Wow, this is a big room!""" , items_in_room=[Item("key", "This key looks familar?"), Item("diamond", """My jeweler, says that diamonds are 
the way to a womans heart""")])


}



# Link rooms together

room['outside'].n_to = room['foyer']
room['foyer'].s_to = room['outside']
room['foyer'].n_to = room['overlook']
room['foyer'].e_to = room['narrow']
room['overlook'].s_to = room['foyer']
room['narrow'].w_to = room['foyer']
room['narrow'].n_to = room['treasure']
room['treasure'].s_to = room['narrow']
room["treasure"].e_to = room["tunnel"]
room["tunnel"].w_to = room["treasure"]
room["tunnel"].e_to = room["great chamber"]
room["great chamber"].w_to = room["tunnel"]



# This is a method that is used to replace the descriptions of all the rooms with 
# a made one that will tell you the which directions to go
def set_directions(room_dict):
    # looping through the list
    theLinksList = None
    dirctions = ["north", "south", "east", "west"]
    newDescription = "From here you can go "
    
    # looping through the dictionary
    for key in room_dict:
        more_than_one = False
        newDescription = "From here you can go "
        theLinksList = room_dict[key].return_room_links()
        # now need to add the words
        for i in range(len(theLinksList)):
            if theLinksList[i] == 1:
                if more_than_one == False:
                    newDescription = newDescription + dirctions[i]
                    more_than_one = True
                else:
                    newDescription = newDescription + " and " + dirctions[i]
        # now doing adding the new description
        room_dict[key].description = newDescription



def set_all_to_none(theRoom):
    theRoom.set_next_to_attr(n_to=None, s_to=None, e_to=None, w_to=None)

def link(theDir, key_to_link_to, key):
    if theDir == 0:
        room[key_to_link_to].n_to = room[key]
        room[key].s_to = room[key_to_link_to]
        
    elif theDir == 1:
        room[key_to_link_to].s_to = room[key]
        room[key].n_to = room[key_to_link_to]
    elif theDir == 2:
        room[key_to_link_to].e_to = room[key]
        room[key].w_to = room[key_to_link_to]
    elif theDir == 3:
        room[key_to_link_to].w_to = room[key]
        room[key].e_to = room[key_to_link_to]
    return
    


def is_available(link_to_key, thedir, ):
    if thedir == 0:
        if room[link_to_key].n_to == None:
            return True
    elif thedir == 1:
        if room[link_to_key].s_to == None:
            return True
    elif thedir == 2:
        if room[link_to_key].e_to == None:
            return True
    elif thedir == 3:
        if room[link_to_key].w_to == None:
            return True
    return False


def pick_to_link_to(linkedList):
    link_to_key = None
    keepTrying = True
    theDir = None
    while keepTrying: # picking a room to link to and then the direction
        link_to_key = choice(linkedList)
        theDirections = [0,1,2,3]
        # looping the number of times that you can choose a direction from the room
        for i in range(4):
            theDir = choice(theDirections)
            # check if is available
            if is_available(link_to_key=link_to_key, thedir=theDir):
                #breakpoint()
                keepTrying = False
                break
            else:
                theDirections.pop(theDir)
               
    # Will return the dir and who to link to
    return theDir, link_to_key



def link_inner(linkedList, toLinkList):
    # base case
    if len(toLinkList) < 1:
        return 
    # choose which room randomly then remove that one from the 
    # toLinkList.
    key = toLinkList.pop(choice(range(0, len(toLinkList))))
    # choosing one from the linkedList randomly and then linking to it
    theDir , key_to_link_to = pick_to_link_to(linkedList)
    # linking
    link(theDir, key_to_link_to, key)
    # add to the linkedList
    linkedList.append(key)

    return link_inner(linkedList, toLinkList)



# making some of the rooms have light in them
def link_rooms():
    """ 
    This is a method that can link the rooms.
    If you would like to have the rooms linked in a different order
    """
    # Will always begin with the outside and then the foyer.
    # setting up for the inner function
    # starting all the links with None
    for key in room:
        set_all_to_none(room[key])
    # linking
    room['outside'].n_to = room['foyer']
    room['foyer'].s_to = room['outside']

    linkedList = ["foyer"]
    # creating the list of the rooms not connected
    toLinkList = []
    for key in room:
        if key not in linkedList and key != "outside":
            toLinkList.append(key)
    
    
    return link_inner(linkedList=linkedList, toLinkList=toLinkList)
