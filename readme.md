main.py
how to configure:
	1) open setup.conf in a text editor
	<br>
	2) change values of selection type, selective pressure, mutation freq, elitism
	  <br>selective type : rank or roulette
	   <br> selective pressure : 1 <= x <= 2. only affects results when set to rank selection. read about rank selection if you are unfamiliar with what selective pressure does
	<br> 3) mutation frequency: the amount of genes that are mutated per crossover. i implemented a simple mutation which halfs the value at a random index
	<br> 4) determines the number of eletist organisms who genes (any number of which) always get pased down.
	 <br>  For example if set to 4, then 4 offspring will gaurentee to have genes from the top 4 parents.
	 <br>  The range is 1 < x <= size. It will not work properly if you run it with one (i set a rule that a chromsome cant mate with itself).
	  <br> if you set it to size, you are efficetively defeating the purpose of an elitist organism (since everyone is an elite).


computesnr.py:
<br<
<br>  input:	>>enter unedited_audio.wav
<br> input:	>>enter edited_audio.wav
<br> result : >> snr
