class Items:
#declare class and parameters
	def __init__(self, itemtype, name, count, useeffect, buff, desc):
		self.itemtype = itemtype
		self.name = name
		self.count = count
		self.useeffect = useeffect
		self.buff = buff
		self.desc = desc

import random

#instantiate lists of variables (for procedural generation)
itemtypes = ['Equipment', 'Consumable']
cons_effect_types = ['Harm', 'Heal']
equip_effect_types = ['HP Up', 'Damage Up']

#define item generation func
def generate_item():
	#generate random values of the item being generated
	c1 = Items(random.choice(itemtypes), 'Namestuff', random.randint(1,2), random.choice(cons_effect_types), '', '')
	#assign them to values per key in dict
	item = {'Item Type': c1.itemtype, 'Name': c1.name, 'Count': c1.count, 'Use Effect': c1.useeffect, 'Buff': c1.buff, 'Desc': ''} #finish this, think about how consumables will be used in combat (combat branch)
	#if the item is equipment
	if item['Item Type'] == 'Equipment':
		#max count is one, it has no use effect (because it can't be used), and it's assigned a random buff
		item['Count'] = 1
		item['Use Effect'] = ''
		item['Buff'] = random.choice(equip_effect_types)
		#assign names and descriptions based on buff
		if item['Buff'] == 'HP Up':
			item['Name'] = 'Jade Beads'
			item['Desc'] = str(item['Item Type'] + '. ' + 'Increases current and maximum HP by one while held.')
		if item['Buff'] == 'Damage Up':
			item['Name'] = 'Crimson Talisman'
			item['Desc'] = str(item['Item Type'] + '. ' + 'Increases player damage by one while held.')
	#if the item is consumable
	if item['Item Type'] == 'Consumable':
		#set the count to a random number between 1 and 2, assign a random use effect, and buff is empty (because it's not equipment)
		item['Count'] = random.randint(1,2)
		item['Use Effect'] = random.choice(cons_effect_types)
		item['Buff'] = ''
		#assign name and description based on use effect
		if item['Use Effect'] == 'Harm':
			item['Name'] = 'Orb of Decay'
			item['Desc'] = str(item['Item Type'] + '. ' + 'Deals one damage to enemy. Undefendable.')
		if item['Use Effect'] == 'Heal':
			item['Name'] = 'Mote of Healing'
			item['Desc'] = str(item['Item Type'] + '. ' + 'Recovers one HP to player.')
	#return the item that was generated (for use in main)
	return(item)