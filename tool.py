from psychopy import visual, event, core, data, logging
import os
import pandas as pd

def setAttrib(trialAttributes, attr, value):
    trialAttributes[attr] = value

def getAttrib(trialAttributes, attr):
    return trialAttributes[attr]

def init_intro(win, win_width):
    return visual.TextStim(win, 
        text="Please press left point finger when the central arrowhead points left \n \nand press right pointing finger when the central arrowhead points right",
        height=1.0, 
        wrapWidth=20, # Text wraps after 20 degrees
        font='DejaVu Sans',
        pos=(0, 0),
        color="black")

def init_goodbye(win, win_width):
    return visual.TextStim(win, 
        text="Thank-you for your attention. \n \nThis task is complete. Please wait.",
        height=1.0, 
        wrapWidth=20,
        font='DejaVu Sans',
        pos=(0, 0),
        color="black")

def run_intro(win, intro_text, trigger_keyList):
    intro_text.draw()
    win.flip()
    event.waitKeys(keyList=trigger_keyList, clearEvents=True)
    core.wait(0.5)

def run_goodbye(win, goodbye_text):
    goodbye_text.draw()
    win.flip()
    core.wait(2.0)

def run_behav(win, thisExp, fixation_text, warning_image_1, target_image, trialClock, rt_list, acc_list, results_dir, resultFile_name, used_keyList, correct_responses):
    current_dir = os.getcwd()
    stimList_name = 'run-all.csv'
    stimList_dir = os.path.join(current_dir, 'experiment_design', 'stim_lists', stimList_name)
    stim_dir = os.path.join(current_dir, 'experiment_design', 'stimuli')
    stimList = pd.read_csv(stimList_dir)
    
    # --- Degree-based Position Math ---
    # Assuming CSV values are pixels (e.g. 240, -240). 
    # Dividing by 50 moves the stimulus ~4.8 degrees from center.
    DEG_SCALE = 50 
    stimList['TargetPos_deg'] = (240 - stimList['TargetPosition']) / DEG_SCALE
    stimList['CuePos_deg'] = (240 - stimList['CuePositionY']) / DEG_SCALE

    trials = stimList.sample(frac=1).reset_index(drop=True)
    trialClock.reset()

    for index, row in trials.iterrows():
        trialAttributes = row.to_dict()
        
        # 1. First Fixation
        fixation_text.draw()
        win.flip()
        core.wait(getAttrib(trialAttributes, "DurationOfFixation") / 1000)

        # 2. Cue/Warning
        warning_image_1.setImage(os.path.join(stim_dir, "symbolstarbig.bmp"))
        warning_image_1.setPos((0, getAttrib(trialAttributes, "CuePos_deg")))
        warning_image_1.draw()
        fixation_text.draw()
        win.flip()
        core.wait(0.1)

        # 3. Middle Fixation
        fixation_text.draw()
        win.flip()
        core.wait(getAttrib(trialAttributes, "IntervalBetweenCueAndTarget") / 1000)

        # 4. Target (Arrows)
        target_image.setImage(os.path.join(stim_dir, getAttrib(trialAttributes, "TargetImage") + ".bmp"))
        target_image.setPos((0, getAttrib(trialAttributes, "TargetPos_deg")))
        target_image.draw()
        fixation_text.draw()
        win.flip()
        target_onsetTime = trialClock.getTime()

        # 5. Response
        keys = event.waitKeys(maxWait=getAttrib(trialAttributes, "DurationOfTarget")/1000, 
                             keyList=used_keyList, timeStamped=trialClock)
        
        acc = 0
        rt = None
        if keys:
            response, reaction_time = keys[0]
            if response == 'escape': core.quit()
            rt = reaction_time - target_onsetTime
            acc = 1 if response == correct_responses[trialAttributes['TargetDirection']] else 0
        
        rt_list.append(rt)
        acc_list.append(acc)
        
        # Logging
        thisExp.addData('RT', rt)
        thisExp.addData('ACC', acc)
        thisExp.nextEntry()

    return np.mean(acc_list), np.mean(rt_list)
