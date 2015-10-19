Currently our project adds a secret message to the begining of the audio file and creates a (.key) file for recovery. It computes the SNR (Signal to Noise ratio) of the edited file 
and the one with the message. The audio file has tens of thousnads of bytes so if your message is small, it will most likely be 1.

Usage : 		
	enter a filename: ocarina.wav
	audio file opened....OK.

	message: secr3tpassw0rd
	original message: secr3tpassw0rd
	message as hex: 7365637233747061737377307264
	<audio info>
	number of channels :  2
	sampwidth :  2
	framerate  44100
	number of frames  464896
	compression type NONE
	compression name  not compressed
	reading information....OK.

	('rms power before added noise : ', 4820)
	adding message to file : ocarina.wav
	('rms power after adding noise', 4821)
	('the signal to noise ratio is: ', 0.9997925741547397)
	the noise file has been saved as ocarina_edited.wav
	audio hidden in ocarina.wav
	enter name for your stego key:mykey
	the file mykey.key has been saved.
	this file will help you recover your text

	enter a .key to decode the text from the audio file: mykey.key
	7365637233747061737377307264
	secr3tpassw0rd

	


I did this in order to verify that I was correctly calculating the SNR since you need two values (baseline audio) and (noisy audio).
This is a ratio between how strong our actual meaningful information is to the noise that is produced by our editing. Our goal, of course is to minimze
this value by decreasing its denominator, the noisy audio. 

If you haven't already, read up a bit on the general procedure to genetic algorithms.
Essentially we will need 3 functions:

selection - 
	which equates to survival of the fittest. The first part, computing the fitness function to judge each individual in the population has already been complete. 
	The next and more challenging part is figuring out how to use this to select a population. Simply selecting the best individuals wont work.
	Here are some possible technqiues: http://www.obitko.com/tutorials/genetic-algorithms/selection.php

crossover - 
	which represents mating between individuals. We could for example, have two arrays  trade indexes that hide information. The ones that figured out the best way to hide information will keep trading with each
	other and eventually converge to an optimal.

mutation - which introduces random modifications. Probably the easiest of the three, just select random indexes to throw information into.
 

Our Algorithm will look something like this:	<br />
1. init population <br />
2. determine initial fitness	<br />
loop:	<br />
3. select population()	<br />
4. crossover()	<br />
5. mutate()	<br />
6. determine fitness()	<br />
7. break: when the population stops changing or set # iterations	<br />

