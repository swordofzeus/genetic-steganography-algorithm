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