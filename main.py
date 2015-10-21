import wave
import binascii
import audioop
import numpy as np
import random as random
import struct
import json
from stegolib import stegolib
def main():
	fname = get_from_user("enter a filename: ")
	steg = stegolib()
	af = steg.open_audio_file(fname)
	parameters = steg.get_audio_information(af)
	message = "#The GA maintains a population of n chromosomes (solutions) with associated fitness values. Parents are selected to mate, on the basis of their fitness, producing offspring via a reproductive plan. Consequently highly fit solutions are given more opportunities to A population of individualsare is maintained within search space for a GA, each representing a possible solution to a given problem. Each individual is coded as a finite length vector of components, or variables, in terms of some alphabet, usually the binary "
	message = message + message
	message_hex = binascii.hexlify(message)
	#The GA maintains a population of n chromosomes (solutions) with associated fitness values. Parents are selected to mate, on the basis of their fitness, producing offspring via a reproductive plan. Consequently highly fit solutions are given more opportunities to 
	audio = steg.as_hex(af)
	baseline_rms = steg.compute_rms_power(audio,"rms power before added noise : ")
	
	population = steg.init_population(audio,20,message_hex)
	population_fitness = steg.measure_population(audio,message_hex,population,baseline_rms)
	print_pop_fitness(population)
	

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

def print_pop_fitness(population):
	lowest = 0
	lowest_value = population[0].fitness
	for x in range(0,len(population)):
		if(population[x].fitness < lowest_value):
			lowest = x
			lowest_value = population[lowest].fitness
		print "individial " + str(x) + ":\t" + str(population[x].fitness)
	print "best individual: \t" + str(lowest) + ": " + str(lowest_value)

main()
