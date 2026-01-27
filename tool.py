from psychopy import visual, event, core, data, logging
import os
import pandas as pd

def setAttrib(trialAttributes, attr, value):
    trialAttributes[attr] = value

def getAttrib(trialAttributes, attr):
    return trialAttributes[attr]

def init_intro(win, win_width):
    # 'Initializing' appeared because the previous code used a placeholder.
    # Updated height to ~0.8 degrees (standard reading size)
    # Updated wrapWidth to 20 degrees (standard reading column width)
    intro_text = visual.TextStim(win, 
                                 text="Please press left point finger when the central arrowhead points left \n \nand press right pointing finger when the central arrowhead points right",
                                 height=0.8,  
                                 bold=False,
                                 wrapWidth=20, 
                                 font='DejaVu Sans',
                                 pos=(0, 0),
                                 color="black")
    return intro_text

def init_goodbye(win, win_width):
    goodbye_text = visual.TextStim(win, 
                                   text="Thank-you for your attention. \n \nThis task is complete. Please wait.",
                                   height=0.8,
                                   bold=False,
                                   wrapWidth=20,
                                   font='DejaVu Sans',
                                   pos=(0, 0),
                                   color="black")
    return goodbye_text

# ... [run_intro and run_goodbye remain the same] ...

def run_behav(win, thisExp, fixation_text, warning_image_1, target_image, trialClock, rt_list, acc_list, results_dir, resultFile_name, used_keyList, correct_responses):
    current_dir = os.getcwd()
    stimList_name = 'run-all.csv'
    stimList_dir = os.path.join(current_dir, 'experiment_design', 'stim_lists', stimList_name)
    stim_dir = os.path.join(current_dir, 'experiment_design', 'stimuli')
    stimList = pd.read_csv(stimList_dir)
    
    # CRITICAL: Re-calculate positions for Degrees of Visual Angle
    # In your old code, you divided by 240 to get a ratio for 'norm'.
    # For 'deg', we usually want small offsets (e.g., 1 or 2 degrees up/down).
    # If your CSV 'TargetPosition' is in pixels, we convert it here:
    # This logic assumes 0 is center, and values like 50 are pixels.
    # Adjust the '45' (pixels per degree) based on your MON_SIZE and MON_WIDTH
    pix_to_deg = 45 
    
    stimList['TargetPosition_center0'] = (stimList['TargetPosition'] / pix_to_deg)
    stimList['CuePositionY_center0'] = (stimList['CuePositionY'] / pix_to_deg)

    trials = stimList.sample(frac=1).reset_index(drop=True)
    trialClock.reset()
    
    for index, row in trials.iterrows():
        trialAttributes = row.to_dict()
        # [Log Data as before...]
        
        # Fixation start
        fixation_text.setAutoDraw(True)
        win.flip()
        core.wait(getAttrib(trialAttributes, "DurationOfFixation") / 1000)
        fixation_text.setAutoDraw(False)

        # Warning slide
        warning_image_1.setImage(os.path.join(stim_dir, "symbolstarbig.bmp"))
        # Using the new degree-based position
        warning_image_1.setPos((0, getAttrib(trialAttributes, "CuePositionY_center0")))
        warning_image_1.draw()
        fixation_text.draw() # Keep fixation visible during cue
        win.flip()
        core.wait(0.1)

        # Middle fixation
        fixation_text.draw()
        win.flip()
        core.wait(getAttrib(trialAttributes, "IntervalBetweenCueAndTarget") / 1000)

        # Target slide
        target_image.setImage(os.path.join(stim_dir, getAttrib(trialAttributes, "TargetImage") + ".bmp"))
        target_image.setPos((0, getAttrib(trialAttributes, "TargetPosition_center0")))
        target_image.draw()
        fixation_text.draw()
        win.flip()
        
        # [Response collection and data logging as before...]
        # Ensure the rest of your timing and logging logic follows
