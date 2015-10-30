import random as random
import hashlib
class RankSelection:
	def __init__(self,population):
		self.population = population
		self.rankedList = list()

	def setup(self,population,SP):

		print "Preparing for RankSelection\nSoring List...",
		self.rankedList = sorted(population, key=lambda x: x.fitness, reverse=True)
		for x in range(0,len(self.rankedList)):
			print self.rankedList[x].fitness

		N = len(self.rankedList)
		self.sum = len(population)
		sums = 0
		for x in range (0,len(population)):
			pos = N - x
			self.rankedList[x].fitness = 2 - SP + 2 * (SP - 1) * (pos - 1) / (N - 1) 
			sums = sums + self.rankedList[x].fitness
			print(self.rankedList[x].fitness)
		print(sums)
		
		print "[done]"
		
	################################################################
	def select_individual(self,population):
		R = 0
		N = len(self.rankedList)-1
		R = R + random.uniform(0,N)
		print("Threshold : " + str(R))
		weight = 0
		while weight < len(population):
			random_index = random.randint(0,N)
			weight = weight + self.rankedList[random_index].fitness
		return self.rankedList[random_index]

	def select_mate(self,population,partner):
		R = 0
		N = len(self.rankedList)-1
		R = R + random.uniform(0,N)
		print("Threshold : " + str(R))
		weight = 0
		while weight < len(population):
			random_index = random.randint(0,N)
			weight = weight + self.rankedList[random_index].fitness
			if(weight >= len(population) and self.rankedList[random_index] == partner):
				weight = 0	
		return self.rankedList[random_index]

	
	#################################################################	
	def get_parents(self,population):
		print "selecting parent one :\n"
		parent_one = self.select_individual(population)
		print "\nselecting parent two: \n"
		parent_two = self.select_mate(population,parent_one)
		return parent_one,parent_two