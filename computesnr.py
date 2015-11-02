import wave
import binascii
import audioop
import numpy as np
import random as random
import struct
def main():
	fname = get_file_from_user()
	af = open_audio_file(fname)				# returns a byte string of the audio file
	parameters = get_audio_information(af)	# displays audio information
	audio = load_into_memory(af)			# copies the byte string into hex format
	baseline_rms = compute_rms_power(audio,"rms power before added noise : ")	# computes the rms power to the unedited file
	print "Adding noise to file : " + fname
	

	fname2 = get_file_from_user()
	af2 = open_audio_file(fname2)
	parameters = get_audio_information(af2)
	audio2 = load_into_memory(af2)
	#edited_audio = add_random_noise(audio)	# inserts random hex values between 0 < x < 4							
	edited_rms = compute_rms_power(audio2,"rms with noise")		# computes the rms power of the edited file												
	#write_wave_file(noise_fname,edited_audio,parameters)	# writes a copy of the edited file to disk
	snr = compute_fitness_function(baseline_rms,edited_rms)	# computes the signal to noise ratio, measuring the ratio of important information to junk/noise
	print ("The signal to noise ratio is: " , snr)
	#print "the noise file has been saved as " + noise_fname 
def get_file_from_user():
	filename = raw_input('Enter a file name: ')
	return filename
def get_noise_fname(fname):
	token = fname.split('.')
	noise_fname = token[0] + "_edited.wav"
	return noise_fname
def add_random_noise(audio_hex):
	audio_list = list(audio_hex)
	for x in range (0,999900): 
		randinteger = random.randint(0, 4)
		string = str(randinteger)
		randhex = binascii.hexlify(string)
		audio_list[x] = randhex
	edited_audio =  ''.join(audio_list)
	return edited_audio
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
def load_segment(af,epoch,frame_ration): 
	num_frames = af.getnframes()
def open_audio_file(fname):
        audio_file = wave.open(fname,'rb')
        print("Audio file opened....OK.\n")
	return audio_file
def get_audio_information(af):
	parameters = af.getparams()
	print "Number of channels : " , parameters[0]
	print "Sampwidth : " , parameters[1]
	print "Framerate " , parameters[2]
	print "Number of frames " , parameters[3]
	print "Compression type" , parameters[4]
	print "Compression name " , parameters[5]
	print("Reading information....OK.\n")
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

