import wave
import binascii
import audioop
import numpy as np
import random as random
import struct
import json
def main():
	fname = get_from_user("enter a filename: ")
	af = open_audio_file(fname)				# returns a byte string of the audio file
	message = get_from_user("message: ")
	print "original message: " + message
	message_hex = binascii.hexlify(message)
	print "message as hex: " + message_hex
	decoded = message_hex.decode("hex")
	print decoded
	parameters = get_audio_information(af)	# displays audio information
	audio = load_into_memory(af)			# copies the byte string into hex format
	baseline_rms = compute_rms_power(audio,"rms power before added noise : ")	# computes the rms power to the unedited file
	print "adding message to file : " + fname
	edited_info = add_random_noise(audio,message_hex)	# inserts random hex values between 0 < x < 4							
	edited_audio = edited_info[0]
	key = edited_info[1]
	edited_rms = compute_rms_power(edited_audio,"rms power after adding noise")		# computes the rms power of the edited file
	noise_fname = get_noise_fname(fname)											
	write_wave_file(noise_fname,edited_audio,parameters)	# writes a copy of the edited file to disk
	snr = compute_fitness_function(baseline_rms,edited_rms)	# computes the signal to noise ratio, measuring the ratio of important information to junk/noise
	print ("the signal to noise ratio is: " , snr)
	print "the noise file has been saved as " + noise_fname 
	saved_keyname = get_from_user("audio hidden in " + fname  + "\nenter name for your stego key:")
	save_key(key,saved_keyname)
	keyname = get_from_user("enter a .key to decode the text from the audio file: ")
	key = load_key(keyname)
	decode_message(edited_audio,key)
def decode_message(audio,key):
	hex_msg = ""
	for x in range (0, len(key)):
		hex_msg = hex_msg + audio[int(key[x])]
	print hex_msg
	decoded_msg = hex_msg.decode("hex")
	#[::-1]
	print decoded_msg
	exit()	
def save_key(key,fname):
	with open(fname + ".key", 'w') as f:
  		json.dump(key, f, ensure_ascii=False)
  		print "\nthe file " + fname + ".key" + " has been saved.\n"
  		print "this file will help you recover your text" 

def load_key(fname):
	with open(fname,'r') as f:
		x = json.load(f)
		return x
def get_from_user(message):
	filename = raw_input(message)
	return filename
def get_noise_fname(fname):
	token = fname.split('.')
	noise_fname = token[0] + "_edited.wav"
	return noise_fname
def add_random_noise(audio_hex,message):
	audio_list = list(audio_hex)
	hidden_key = list()
	#400000
	for x in range (0,len(message)): 
		#string = str(message[x-400000])
		randhex = message[x]
		hidden_key.append(x) 
		print randhex + " original : " + audio_list[x]
		audio_list[x] = randhex
	edited_audio =  ''.join(audio_list)
	return edited_audio,hidden_key
def write_wave_file(fname,hexdata,parameters):
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
def open_audio_file(fname):
        audio_file = wave.open(fname,'rb')
        print("audio file opened....OK.\n")
	return audio_file
def get_audio_information(af):
	parameters = af.getparams()
	print "number of channels : " , parameters[0]
	print "sampwidth : " , parameters[1]
	print "framerate " , parameters[2]
	print "number of frames " , parameters[3]
	print "compression type" , parameters[4]
	print "compression name " , parameters[5]
	print("reading information....OK.\n")
	return parameters
def load_into_memory(af):
	num_frames = af.getnframes()
	frames = af.readframes(num_frames)	
	hex_array = binascii.hexlify(frames)
	return hex_array
def compute_rms_power(audio,message):
	audio_byte_arr = bytearray.fromhex(audio)
	ad = ''.join(str(audio_byte_arr))
	rms = audioop.rms(ad,2)	
	print(message , rms)
	return rms
def compute_fitness_function(baseline_stream,noisy_stream):
	return float(baseline_stream)/float(noisy_stream)


main()