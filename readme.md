Currently our project adds random noise to a wav file and computes the SNR (Signal to Noise ratio).
Usage : 		
	Enter a file name: ocarina.wav			// you can enter any wav file, i provided a sample one i was using to test.
	audio file opened....OK.

	< some info about audio,channels, samplewidth, etc. >	

	('rms power before added noise : ', 4820)
	adding noise to file : ocarina.wav
	('rms power after adding noise', 9147)
	('the signal to noise ratio is: ', 0.5269487263583689)
	the noise file has been saved as ocarina_edited.wav

I did this in order to verify that I was correctly calculating the SNR since you need two values (baseline audio) and (noisy audio).
This is a ratio between how strong our actual meaningful information is to the noise that is produced by our editing. Our goal, of course is to minimze
this value by decreasing its denominator, the noisy audio. 

If you haven't already, read up a bit on the general procedure to genetic algorithms.
Essentially we will need 3 functions:

selection - 
	which equates to survival of the fittest. The first part, computing the fitness function to judge each individual in the population has already been complete. 
	The next and more challenging part is figuring out how to use this to select a population. Simply selecting the best individuals wont work.
	Here are some possible technqiues: 

crossover - 
	which represents mating between individuals. We could for example, have two arrays  trade indexes that hide information. The ones that figured out the best way to hide information will keep trading with each
	other and eventually converge to an optimal.

mutation - which introduces random modifications. Probably the easiest of the three, just select random indexes to throw information into.
 

Our Algorithm will look something like this:
	init population
	determine initial fitness
	loop:
		select population()
		crossover()
		mutate()
		determine fitness()
	break when the population stops changing or set # iterations

