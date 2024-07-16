# ANT_behavioral
* __About this ANT version:__
  - behavioral version of ANT.
  - time for each practice: 4s/trial * 24 trial/run = 1.6m
  - time for each run: 4s/trial * 72 trial/run = 4.8m
  - 3 runs in total, total time is around 20m
    <img width="476" alt="image" src="https://github.com/user-attachments/assets/581bea5b-f24c-4400-ba84-f8f85772cb42">

* __Adapt from the [e-prime fMRI version](http://people.qc.cuny.edu/Faculty/Jin.Fan/Pages/Downloads.aspx) ([Fan et al., 2005](https://www.sciencedirect.com/science/article/abs/pii/S1053811905000984?via%3Dihub)).__
Changes including:
	* Use the same trial sets as the [Fan et al., 2002].(https://pubmed.ncbi.nlm.nih.gov/11970796/)
  * simplify the instruction
	- in original e-prime version:
	- "Welcome to Attention Experiment\nPress a button to continue. \n\nPress and hold all 5 buttons to contact Technologist."
	- " \nInstruction\n\nPlease press left point finger when the cental arrowhead points left and press right pointing finger when the central arrowhead poin" &_ 
				"ts right.\n\n\nPress any button if you are ready.. "
	- in current version:
	- "Please press left point finger when the cental arrowhead points left \n \nand press right pointing finger when the central arrowhead poin right"
   
	* using norm (Normalized) as the representation units to addapt easily to differen size of screens.
