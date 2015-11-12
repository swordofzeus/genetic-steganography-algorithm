##################		stegolib.py					####################
##	contains information relating to .wav I/O, encoding and decoding,
##  and evaluating fitness

import wave
import binascii
import audioop
import numpy as np
import random as random
import struct
import json
from Chromosome import Chromosome as Chromosome
class stegolib:

	#takes a string of hex values and the corresponding key 
	# and returns the ascii decoded message
	def decode_message(self,audio,key):
		hex_msg = ""
		for x in range (0, len(key)):
			hex_msg = hex_msg + audio[int(key[x])]
		decoded_msg = hex_msg.decode("hex")
		print decoded_msg

	#takes a list object and dumps it into a file.
	#the list should be full of integers representing 
	#the various indicies where the message has been hidden
	def save_key(self,key,fname):
		with open(fname, 'w') as f:
	  		json.dump(key, f, ensure_ascii=False)
	  		print "\nThe file " + fname + ".key" + " has been saved.\n"
	  		print "This file will help you recover your text" 

	#loads a file containing the stego key into a list structure 		
	def load_key(self,fname):
		with open(fname,'r') as f:
			x = json.load(f)
			return x

	#returns the name of the edited audio file.
	#tacks on _edited.wav to the original filename
	def get_noise_fname(self,fname):
		token = fname.split('.')
		noise_fname = token[0] + "_edited.wav"
		return noise_fname

	#encodes the message into the audio file
	def encode(self,audio_hex,message,population):
		audio_list = list(audio_hex)
		hidden_key = list()
		#400000
		offset = 0
		for x in range (0 + offset,offset + len(population)): 
			#string = str(message[x-400000])
			randhex = message[x-offset]
			hidden_key.append(population[x]) 
			#print randhex + " original : " + audio_list[x]
			audio_list[population[x]] = randhex
		edited_audio =  ''.join(audio_list)
		return edited_audio,hidden_key
	
	#writes a wav file with the given filename, audio as a string of hex values
	#and a tuple of parameters (number of channels,samplewidth,framerate,number of frames,encoding type, encoding name)
	def write_wave_file(self,fname,hexdata,parameters):
		noise_output = wave.open(fname,'w')
		num_channels = parameters[0]
		sample_width = parameters[1]
		framerate = parameters[2]
		number_frames = parameters[3]
		compression_type = parameters[4]
		compression_name = parameters[5]
		noise_output.setparams((num_channels,sample_width,framerate,number_frames,compression_type,compression_name))
		audio_bytes = bytearray.fromhex(hexdata)
		noise_output.writeframes(audio_bytes)
		noise_output.close()		
	
	#returns a string of bytes representing the audio file
	def open_audio_file(self,fname):
	        audio_file = wave.open(fname,'rb')
	        print("Audio file opened....OK.\n")
		return audio_file

	#writes information about the audio to console
	def get_audio_information(self,af):
		parameters = af.getparams()
		print "Number of channels : " , parameters[0]
		print "Sampwidth : " , parameters[1]
		print "Framerate " , parameters[2]
		print "Number of frames " , parameters[3]
		print "Compression type" , parameters[4]
		print "Compression name " , parameters[5]
		print("Reading information....OK.\n")
		return parameters

	#returns the hex representation of a string of audio bytes
	def as_hex(self,af):
		num_frames = af.getnframes()
		frames = af.readframes(num_frames)	
		hex_array = binascii.hexlify(frames)
		return hex_array
	#computes the root mean square power of an audio given
	#a string of bytes (audio). (message) is anything
	#you want to print to console. doesn't affect audio.
	def compute_rms_power(self,audio,message):
		audio_byte_arr = bytearray.fromhex(audio)
		ad = ''.join(str(audio_byte_arr))
		rms = audioop.rms(ad,2)	
		#print(message , rms)
		return rms

	#returns the signal to noise ratio, used to determine 
	#population fitness
	def compute_fitness_function(self,baseline_stream,noisy_stream):
		return float(baseline_stream)/float(noisy_stream)

	def new_chromosome(self,message,audio):
		key = list()
		for x in range(0,len(message)):
			random_index = random.randint(0,len(audio))
			while random_index in key:
				
				random_index = random.randint(0,len(audio))
			key.append(random_index)
		chromosome = Chromosome(key,-1)
		#	print "random index " + str(random_index)

		#print "\n"
		#print chromosome
		return chromosome

	def init_population(self,audio,pop_size,message):
		pop_list = list()
		for x in range(0,pop_size):
			#print "new chromosome created! : " + str(x)
			chromosome = self.new_chromosome(message,audio)
			pop_list.append(chromosome)
		return pop_list

	def measure_population(self,audio,message,population,baseline_rms):
		fitness = list()
		for x in range(0,len(population)):
			curr_chromosome = population[x]
			audio_info = self.encode(audio,message,curr_chromosome.all_genes())
			audio_edited = audio_info[0]
			audio_key = audio_info[1]
			edited_rms = self.compute_rms_power(audio_edited," ")
			curr_fitness = self.compute_fitness_function(baseline_rms,edited_rms)
			curr_chromosome.fitness = curr_fitness
			fitness.append(curr_fitness)
		return fitness

	def measure_individual(self,audio,message,individual,baseline_rms):
		fitness = list()
		curr_chromosome = individual
		audio_info = self.encode(audio,message,curr_chromosome.all_genes())
		audio_edited = audio_info[0]
		audio_key = audio_info[1]
		edited_rms = self.compute_rms_power(audio_edited," ")
		curr_fitness = self.compute_fitness_function(baseline_rms,edited_rms)
		curr_chromosome.fitness = curr_fitness
		return curr_chromosome.fitness