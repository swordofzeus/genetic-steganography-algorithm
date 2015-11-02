# -*- coding: utf-8 -*-
import wave
import binascii
import audioop
import numpy as np
import random as random
import struct
import json
from stegolib import stegolib
from RouletteWheel import RouletteWheel
from RankSelection import RankSelection
from Chromosome import Chromosome as Chromosome
import ScatterPlot

SELECTION_ROULETTE = "roulette"
SELECTION_RANK = "rank"
SELECTIVE_PRESSURE = 2.0
MUTATION_FREQ = 0
ELITISM = 0
def main():	
	selection = "rank"
	fname = "piano2.wav"
	print "The file to encode is : \t" + fname 
	#get_from_user("enter a filename: ")
	steg = stegolib()
	config = steg.load_key("setup.conf")
	user_config =read_config(config)
	user_selection = user_config[0]
	user_pressure = user_config[1]
	user_mutation_freq = user_config[2]
	user_elitism = user_config[3]



	get_from_user("\nPress enter to continue.")
	

	
	af = steg.open_audio_file(fname)
	parameters = steg.get_audio_information(af)
	#message = "abc"
	#message = "It was the best of times, it was the worst of times, it was the age of wisdom, it was the age of foolishness, it was the epoch of belief, it was the epoch of incredulity, it was the season of Light, it was the season of Darkness, it was the spring of hope, it was the winter of despair, we had everything before us, we had nothing before us, we were all going direct to Heaven, we were all going direct the other way – in short, the period was so far like the present period, that some of its noisiest authorities insisted on its being received, for good or for evil, in the superlative degree of comparison only. "
	message = "It was the best of times, it was the worst of times, it was the age of wisdom, it was the age of foolishness, it was the epoch of belief, it was the epoch of incredulity, it was the season of Light, it was the season of Darkness, it was the spring of hope, it was the winter of despair, we had everything before us, we had nothing before us, we were all going direct to Heaven, we were all going direct the other way – in short, the period was so far like the present period, that some of its noisiest authorities insisted on its being received, for good or for evil, in the superlative degree of comparison only."
	print "Encoding message :\n" + message
	print "\n"
	message = message + message + message + message + message
	message_hex = binascii.hexlify(message)
	#The GA maintains a population of n chromosomes (solutions) with associated fitness values. Parents are selected to mate, on the basis of their fitness, producing offspring via a reproductive plan. Consequently highly fit solutions are given more opportunities to 
	audio = steg.as_hex(af)
	baseline_rms = steg.compute_rms_power(audio,"RMS power before added noise : ")
	num_individuals = 20
	print "Step 1) The first step of a genetic algorithm is to initialize a random population. The initial randomness creates genetic variation which is the basis for our search heuristic. \nWe measure the fitness function of each member of our population and use that as a metric for selecting the best individuals whose genes move to the next generation "
	
	get_from_user("Press enter to initialize a population")
	print "Initializing random population of " + str(num_individuals) + " individuals... \n"
	population = steg.init_population(audio,20,message_hex)
	population_fitness = steg.measure_population(audio,message_hex,population,baseline_rms)
	best_values = list()
	strongest_chromosomes = list()
	print_pop_fitness(population,best_values,"individual")
	ScatterPlot.plot(best_values)
	get_from_user("\nPress enter to continue")
	#best = handle_elitism(population,user_elitism)

	#print "\n BEST"
	#for x in range (0,len(best)):
	#	print str(best[x].fitness)
	

	###################################
	
	#get_parents()
	#survive = parents[0]
	#survive2 = parents[1]
	#print "parent one fitness: " + str(survive.fitness)
	#print "parent two fitness: " + str(survive2.fitness)	
	#exit()
	###################################
	
	##################################

	next_generation = list()
	print "Step 2 : Initialize new generation"
	print "The most fit individuals are selected using the RouletteWheel model to produce children. The fittest individuals cross genes in hopes that after multiple iterations future generations will \nbegin to converge towards an optimal or near optimal value."
	get_from_user("\nPress enter to continue")
	
	num_generations = 20
	for y in range(0,num_generations):
		print "ENTERING GENERATION : " + str(y)
		next_generation = handle_elitism(population,user_elitism,next_generation,user_mutation_freq,baseline_rms,steg,audio,message_hex)
		print "len " + str(len(next_generation))
		for x in range(0,len(next_generation)):
			print(next_generation[x].fitness)
		
		for x in range(0,len(population) - user_elitism):
			if x is 0 and y is 0:
				print "Spinning RouletteWheel..."
			parents = get_parents(population,user_selection,user_pressure)
			survive = parents[0]
			survive2 = parents[1]
			if x is 0 and y is 0:
				print "\nParents selected:"
				print "Parent one fitness: " + str(survive.fitness)
				print "Parent two fitness: " + str(survive2.fitness)	
				print "\nThe selected individuals are going to crossover genes to create a child chromosome that will hopefully adopt the best of both parents and move on to the next generation. The selection algorithm is called single split point selection "
			child_key = survive.crossover(survive2)
			child = Chromosome(child_key,-2)
			child.mutate(user_mutation_freq)

			#exit()
			child.fitness = steg.measure_individual(audio,message_hex,child,baseline_rms,)	
			if x is 0 and y is 0:
				print "the child fitness is : " + str(child.fitness) + ", and it is moving on to the next generation. \n" 
				get_from_user("Press enter to run this for all members of the population.")
			next_generation.append(child)
		print_pop_fitness(next_generation,best_values,"child")
		if y is 0:
			#print "X is:  " + str(x)
			print "\n\nWe just finished one generation. We kept the best value from our initial population and the best value from our first\n round of genetic combination."
			print ("Best values so far: " + str(best_values))
			get_from_user("Press Enter to repeat for " + str(num_generations) + " generations")
		population = list(next_generation)
		del next_generation[:]
		if y is 4 or y is 9 or y is 14:
			ScatterPlot.plot(best_values)

	
	print"\n\nFinished " + str(num_generations) +  "." + "Here is a list of the highest fitness values from each generation:"
	print "BEST VALUES " + str(best_values)

	ordered = result_tuples(best_values)
	print_analysis(ordered)
	ScatterPlot.plot(best_values)

	exit()
	#print population_fitness
	
	


	edited_info = steg.encode(audio,message_hex,best_values[0].key)	# inserts random hex values between 0 < x < 4							
	edited_audio = edited_info[0]
	key = edited_info[1]
	edited_rms = steg.compute_rms_power(edited_audio,"rms power after adding noise")		# computes the rms power of the edited file
	noise_fname = steg.get_noise_fname(fname)											
	steg.write_wave_file(noise_fname,edited_audio,parameters)	# writes a copy of the edited file to disk
	snr = steg.compute_fitness_function(baseline_rms,edited_rms)


	print ("The signal to noise ratio is: " , snr)
	print "The noise file has been saved as " + noise_fname 
	saved_keyname = get_from_user("Audio hidden in " + fname  + "\nEnter name for your stego key:")
	steg.save_key(key,saved_keyname)
	keyname = get_from_user("Enter a .key to decode the text from the audio file: ")
	key = steg.load_key(keyname)
	steg.decode_message(edited_audio,key)
	

def read_config(config):
	
	print "Opening & reading setup.config...."
	for x in range(0,len(config),2):
		print str(config[x]) + "\t" + str(config[x+1])
		user_selection = config[1]
		user_pressure = config[3]
		user_mutation_freq = config[5]
		user_elitism = config[7]
	return (user_selection,user_pressure,user_mutation_freq,user_elitism)
	
def get_parents(population,selection,user_pressure):
	if(selection == SELECTION_ROULETTE):
		rw = RouletteWheel(population)
		rw.create_wheel(population)
		return rw.get_parents(population)
	elif(selection == SELECTION_RANK):
		rs = RankSelection(population)
		rs.setup(population,user_pressure)
		return rs.get_parents(population)	
def get_from_user(message):
		filename = raw_input(message)
		return filename

def handle_elitism(population,user_elitism,next_generation,user_mutation_freq,baseline_rms,steg,audio,message_hex):
	ordered_list = sorted(population, key=lambda x: x.fitness, reverse=True)
	for x in range(0,len(population)):
		print(ordered_list[x].fitness)
	best = list()
	for x in range(0,user_elitism):
		best.append(ordered_list[x])
	N = len(best)	
	next_gen = list()
	for x in range(0,N):
			parent_one = random.randint(0,N-1)
			parent_two = -1
			while parent_two != parent_one:
				parent_two = random.randint(0,N-1)
				print "Parent 1 " + str(parent_one)
				print "Parent 2 " + str(parent_two)
			child_key = best[parent_one].crossover(best[parent_two])
			child = Chromosome(child_key,-2)
			child.mutate(user_mutation_freq)
			child.fitness = steg.measure_individual(audio,message_hex,child,baseline_rms,)
			print "Child " + str(child.fitness)
			next_gen.append(child)
	return next_gen
def print_pop_fitness(population,best_values,type):
	lowest = 0
	lowest_value = population[0].fitness
	highest_value = population[0].fitness
	highest = 0
	for x in range(0,len(population)):
		if(population[x].fitness < lowest_value):
			lowest = x
			lowest_value = population[lowest].fitness
		if(population[x].fitness > highest_value):
			highest = x
			highest_value = population[highest].fitness
		print "Individual " + type + " # " + str(x) + " Fitness : \t " + str(population[x].fitness)
		#print "individial " + str(x) + ":\t" + str(population[x].fitness)
	print "Worst individual: \t" + str(lowest) + ": " + str(lowest_value)
	print "Best individual: \t" + str(highest) + ": " + str(highest_value)
	best_values.append(str(highest_value))

def print_results(results):
	for x in range(len(results)):
		print "Generation " + str(x) + ":\t" + str(results[x])

def result_tuples(results):
	tuple_list = list()
	for x in range(len(results)):
		value = results[x],x
		tuple_list.append(value)
		#print "tuple : " + str(value)
	#tuple_list.sort(key=lambda tup: tup[0])
	tuple_list.sort()
	print(str(tuple_list))
	return tuple_list

def print_analysis(results):
	print "** Analysis of Results **"
	print "The list of generations from worse to best."
	for x in range(0,len(results)):
		generation = results[x]
		print "Generation " + str(generation[1]) + ":\t" + str(generation[0])

main()
