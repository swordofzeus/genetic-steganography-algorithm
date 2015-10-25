import random as random
class Chromosome:
	def __init__(self,key,fitness):
		self.key = key
		self.fitness = fitness

	def mutate():
			pass

	def get_gene(self,i):
		return self.key[i]

	def set_gene(self,i,value):
		self.key[i] = value

	def all_genes(self):
		return self.key

	def crossover(self,partner):
		#print "self : " + str(self.key)
		#print "partner " + str(partner.key)
		split_point = random.randint(0,len(self.key)-1)
		#print "split_point " + str(split_point)
		begining = self.key[0:split_point]
		end = partner.key[split_point:len(self.key)]
		child_key = begining + end
		#print "begining " + str(begining)
		#print "end " + str(end)
		#print "child_key " + str(child_key)
		return child_key