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
from Chromosome import Chromosome as Chromosome
def main():
	fname = "ocarina.wav"
	print "The file to encode is : \t" + fname 
	#get_from_user("enter a filename: ")
	steg = stegolib()
	af = steg.open_audio_file(fname)
	parameters = steg.get_audio_information(af)
	#message = "abc"
	#message = "It was the best of times, it was the worst of times, it was the age of wisdom, it was the age of foolishness, it was the epoch of belief, it was the epoch of incredulity, it was the season of Light, it was the season of Darkness, it was the spring of hope, it was the winter of despair, we had everything before us, we had nothing before us, we were all going direct to Heaven, we were all going direct the other way – in short, the period was so far like the present period, that some of its noisiest authorities insisted on its being received, for good or for evil, in the superlative degree of comparison only. "
	message = "It was the best of times, it was the worst of times, it was the age of wisdom, it was the age of foolishness, it was the epoch of belief, it was the epoch of incredulity, it was the season of Light, it was the season of Darkness, it was the spring of hope, it was the winter of despair, we had everything before us, we had nothing before us, we were all going direct to Heaven, we were all going direct the other way – in short, the period was so far like the present period, that some of its noisiest authorities insisted on its being received, for good or for evil, in the superlative degree of comparison only."
	print "encoding message :\n " + message
	print "\n"
	message = message + message + message + message + message
	message_hex = binascii.hexlify(message)
	#The GA maintains a population of n chromosomes (solutions) with associated fitness values. Parents are selected to mate, on the basis of their fitness, producing offspring via a reproductive plan. Consequently highly fit solutions are given more opportunities to 
	audio = steg.as_hex(af)
	baseline_rms = steg.compute_rms_power(audio,"rms power before added noise : ")
	num_individuals = 20
	print "Step 1) The first step of a genetic algorithm is to initialize a random population. The initial randomness creates genetic variation which is the basis for our search heuristic. \nWe measure the fitness function of each member of our population and use that as a metric for selecting the best individuals whose genes move to the next generation "
	
	get_from_user("Press Enter to initialize a population")
	print "initializing random population of " + str(num_individuals) + " individuals... \n"
	population = steg.init_population(audio,20,message_hex)
	population_fitness = steg.measure_population(audio,message_hex,population,baseline_rms)
	best_values = list()
	print_pop_fitness(population,best_values,"individual")
	get_from_user("\npress enter to continue")
	
	rw = RouletteWheel(population)
	rw.create_wheel(population)
	next_generation = list()
	print "Step 2 : Initialize new generation"
	print "The most fit individuals are selected using the RouletteWheel model to produce children. The fittest individuals cross genes in hopes that after multiple iterations future generations will \nbegin to converge towards an optimal or near optimal value."
	get_from_user("\n press enter to continue")
	
	num_generations = 5
	for y in range(0,5):
		print "ENTERING GENERATION : " + str(y)
		for x in range(0,len(population)):
			if x is 0 and y is 0:
				print "Spinning RouletteWheel..."
			parents = rw.get_parents(population)
			survive = parents[0]
			survive2 = parents[1]
			if x is 0 and y is 0:
				print "\nparents selected:"
				print "parent one fitness: " + str(survive.fitness)
				print "parent two fitness: " + str(survive2.fitness)	
				print "\nThe selected individuals are going to crossover genes to create a child chromosome that will hopefully adopt the best of both parents and move on to the next generation. The selection algorithm is called single split point selection "
			child_key = survive.crossover(survive2)
			child = Chromosome(child_key,-2)
			child.fitness = steg.measure_individual(audio,message_hex,child,baseline_rms,)	
			if x is 0 and y is 0:
				print "the child fitness is : " + str(child.fitness) + ", and it is moving on to the next generation. \n" 
				get_from_user("Press enter to run this for all members of the population.")
			next_generation.append(child)
		print_pop_fitness(next_generation,best_values,"child")
		if y is 0:
			#print "X is:  " + str(x)
			print "\n\nWe just finished one generation. We kept the best value from our initial population and the best value from our first\n round of genetic combination. Press ENTER to repeat this process for five generations."
			print ("best values so far: " + str(best_values))
			get_from_user("")
		population = list(next_generation)
		del next_generation[:]
	
	print"\n\n Finished " + str(num_generations) +  "." + "Here is a list of the highest fitness values from each generation:"
	print "BEST VALUES " + str(best_values)
	exit()

	#print population_fitness
	
	


	edited_info = steg.encode(audio,message_hex,population[0].key)	# inserts random hex values between 0 < x < 4							
	edited_audio = edited_info[0]
	key = edited_info[1]
	edited_rms = steg.compute_rms_power(edited_audio,"rms power after adding noise")		# computes the rms power of the edited file
	noise_fname = steg.get_noise_fname(fname)											
	steg.write_wave_file(noise_fname,edited_audio,parameters)	# writes a copy of the edited file to disk
	snr = steg.compute_fitness_function(baseline_rms,edited_rms)


	print ("the signal to noise ratio is: " , snr)
	print "the noise file has been saved as " + noise_fname 
	saved_keyname = get_from_user("audio hidden in " + fname  + "\nenter name for your stego key:")
	steg.save_key(key,saved_keyname)
	keyname = get_from_user("enter a .key to decode the text from the audio file: ")
	key = steg.load_key(keyname)
	steg.decode_message(edited_audio,key)
	
	
def get_from_user(message):
		filename = raw_input(message)
		return filename

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
		print "individual " + type + " # " + str(x) + " fitness : \t " + str(population[x].fitness)
		#print "individial " + str(x) + ":\t" + str(population[x].fitness)
	print "best individual: \t" + str(lowest) + ": " + str(lowest_value)
	print "worst individual: \t" + str(highest) + ": " + str(highest_value)
	best_values.append(str(lowest_value))
	

main()
