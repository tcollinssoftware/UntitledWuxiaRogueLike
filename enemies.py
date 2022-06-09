class Enemies:
#declare class and parameters
	def __init__(self, maxhp, curhp, damage, name, item):
		self.maxhp = maxhp
		self.curhp = curhp
		self.damage = damage
		self.name = name
		self.item = item


import random
import items

#lists of forenames and surnames for generation choice
eforename = [
    'Dun', 'Wei', 'Liao', 'Cao', 'Zhu', 'Yuan', 'Huang', 'He', 'Ren', 'Pi', 'Ji', 'De', 'Wenji', 'Xu', 'Yi', 'Jia', 'Jin', 'Dian',
    'Yu', 'Xun', 'Shang', 'Xiang', 'Ning', 'Jian', 'Ci', 'Meng', 'Gai', 'Tai', 'Tong', 'Ce', 'Quan', 'Qiao', 'Feng', 'Shi', 'Su',
    'Dang', 'Yun', 'Fei', 'Liang', 'Bei', 'Chao', 'Zhong', 'Yan', 'Ping', 'Tong', 'Ying', 'Cai', 'Shan', 'Dai', 'Suo', 'Sanniang',
    'Shu', 'Bao', 'Xing', 'Yin', 'Ping', 'Yinping', 'Zhao', 'Ai', 'Yuanji', 'Hui', 'Dan', 'Ba', 'Huai', 'Chong', 'Chun',
    'Chunhua', 'Hua', 'Yang', 'Chan', 'Bu', 'Zhuo', 'Shao', 'Jiao', 'Huo', 'Rong', 'Ci'
]

esurname = [
    'Xiahou', 'Dian', 'Cao', 'Xu', 'Zhang', 'Zhen', 'Pang', 'Cai', 'Jia', 'Wang', 'Guo', 'Yue', 'Li',
    'Zhou', 'Lu', 'Sun', 'Gan', 'Taishi', 'Huang', 'Ling', 'Xiao', 'Da', 'Ding', 'Lian', 'Han', 'Guan',
    'Zhuge', 'Liu', 'Ma', 'Wei', 'Yue', 'Jiang', 'Xing', 'Bao', 'Sima', 'Deng', 'Zhong', 'Wen', 'Diao',
    'Dong', 'Yuan', 'Meng', 'Zhu', 'Zuo'
]

#func to generate enemy
def generate_enemy():
	#choose a random int between 2 and 4 for the enemy's hp
	generate_maxhp = random.randint(2,4)
	#generate the enemy's parameters and store in var
	e1 = Enemies(generate_maxhp, generate_maxhp, 1, str(random.choice(esurname)) + " " + str(random.choice(eforename)), items.generate_item())
	#create a dict for the enemy to hold the information
	enemy = {'Max HP': e1.maxhp, 'Current HP': e1.curhp, 'Damage': e1.damage, 'Name': e1.name, 'Item': e1.item}
	#return the enemy for use in main and room
	return(enemy)

#functionally the same as generate_enemy(), but with specified values for keys in the dictionary
#to ensure that the boss is always the same
def generate_boss():
	e1 = Enemies(6, 6, 1, str(random.choice(esurname)) + " " + str(random.choice(eforename)), items.generate_item())
	enemy = {'Max HP': 6, 'Current HP': 6, 'Damage': e1.damage, 'Name': 'The Cursed Emperor', 'Item': e1.item}
	return (enemy)