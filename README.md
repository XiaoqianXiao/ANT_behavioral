# ANT_behavioral
* __About this ANT version:__
	- behavioral version of ANT.
	- time for each practice: 4s/trial * 24 trial/run = 1.6m
	- time for each run: 4s/trial * 72 trial/run = 4.8m
	- 3 runs in total, total time is around 15m
	- 36 trials in each 3 cue * 2 target conditions
	<img width="476" alt="image" src="https://github.com/user-attachments/assets/581bea5b-f24c-4400-ba84-f8f85772cb42">

* __Adapt from the [e-prime short version](http://people.qc.cuny.edu/Faculty/Jin.Fan/Pages/Downloads.aspx) ([Fan et al., 2002](https://www.sciencedirect.com/science/article/abs/pii/S1053811905000984?via%3Dihub)). You can find describtion of the short version in detail [here](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3526671/).__
- Not using the [Fan et al., 2002 version](https://pubmed.ncbi.nlm.nih.gov/11970796/) directly since its design (see figure below) included "double cue" and "neutral target" trials which were not were interested in research of attention network nowadays.
  <img width="576" alt="image" src="https://github.com/user-attachments/assets/be9f0e76-d243-4b39-816e-1037bf6152e4">

- 3 runs in total * 72 trails/run [the original one is 3 runs * 48 trails/run]
- Simplify the instruction
	- in original e-prime version:
	- "Welcome to Attention Experiment\nPress a button to continue. \n\nPress and hold all 5 buttons to contact Technologist."
	- " \nInstruction\n\nPlease press left point finger when the cental arrowhead points left and press right pointing finger when the central arrowhead poin" &_ 
				"ts right.\n\n\nPress any button if you are ready.. "
	- in current version:
	- "Please press left point finger when the cental arrowhead points left \n \nand press right pointing finger when the central arrowhead poin right"
- Using norm (Normalized) as the representation units to addapt easily to differen size of screens.
