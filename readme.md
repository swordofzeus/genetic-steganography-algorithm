main.py
how to configure:
	1) open setup.conf in a text editor
	2) change values of selection type, selective pressure, mutation freq, elitism
	   selective type : rank or roulette
	   selective pressure : 1 <= x <= 2. only affects results when set to rank selection. read about rank selection if you are unfamiliar with what selective pressure does
	3) mutation frequency: the amount of genes that are mutated per crossover. i implemented a simple mutation which halfs the value at a random index
	4) determines the number of eletist organisms who genes (any number of which) always get pased down.
	   For example if set to 4, then 4 offspring will gaurentee to have genes from the top 4 parents.
	   The range is 1 < x <= size. It will not work properly if you run it with one (i set a rule that a chromsome cant mate with itself).
	   if you set it to size, you are efficetively defeating the purpose of an elitist organism (since everyone is an elite).


computesnr.py:

input:	>>enter unedited_audio.wav
input:	>>enter edited_audio.wav
result : >> snr
