import random as random
import hashlib
class RouletteWheel:
	def __init__(self,population):
		self.population = population
		self.sum = 0

	def create_wheel(self,population):
		S = self.sum_fitness(population)
		self.sum = S
		
		
	def sum_fitness(self,population):
		sum = 0
		for x in range(0,len(population)):
			sum = sum + population[x].fitness
		return sum


	def get_parents(self,population):
		print "selecting parent one :\n"
		parent_one = self.select_individual(population)
		print "\nselecting parent two: \n"
		parent_two = self.select_mate(population,parent_one)
		return parent_one,parent_two

	def select_individual(self,population):
		R = 0
		R = R + random.uniform(0,self.sum)
		print("Threshold : " + str(R))
		weight = 0
		for x in range(0,len(population)):
			weight = weight + population[x].fitness	
			print("spinning: " + str(weight))
			if(weight >= R):
				return population[x]
		return -1

	def select_mate(self,population,partner):
		R = 0
		R = R + random.uniform(0,self.sum)
		print("Threshold : " + str(R))
		weight = 0
		for x in range(0,len(population)):
			weight = weight + population[x].fitness	
			print("spinning: " + str(weight))
			if(weight >= R):
				if(population[x] == partner):
					return self.select_mate(population,partner)
				else:
					return population[x]
		return -1

	def select_matew(self,population,partner):
		R = 0
		for x in range(0,len(population)):
			R = R + random.uniform(0,self.sum)
			print("R : " + str(R))
			print("S : " + str(self.sum))
			if(self.sum <= R):
				print "population[x] : " + str(population[x].get_gene(4))
				print "partner : " + str(partner.get_gene(4))
				return population[x]
			#if (population[x] == partner):
			#	self.select_mate(population,partner)


		return -1