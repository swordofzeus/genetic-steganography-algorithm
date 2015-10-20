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
	message = get_from_user("enter a message: ")
	message_hex = binascii.hexlify(message)

	audio = steg.as_hex(af)
	baseline_rms = steg.compute_rms_power(audio,"rms power before added noise : ")
	
	population = steg.init_population(audio,3,message_hex)

	
	edited_info = steg.encode(audio,message_hex,population[0])	# inserts random hex values between 0 < x < 4							
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
main()
