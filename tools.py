# Function to update attributes
from psychopy import visual, event, core, data, logging
import os
import pandas as pd

def setAttrib(trialAttributes, attr, value):
    trialAttributes[attr] = value

def getAttrib(trialAttributes, attr):
    return trialAttributes[attr]

def init_intro(win, win_width):
    intro_text = visual.TextStim(win, text="Please press left point finger when the cental arrowhead points left \n \nand press right pointing finger when the central arrowhead poin right",
                                 height=0.08,  # Font size
                                 bold=False,  # Font bold
                                 wrapWidth=0.8 * win_width,  # 5% of window width
                                 font='DejaVu Sans',
                                 pos=(0, 0),
                                 color="black")
    return intro_text

def init_goodbye(win, win_width):
    goodbye_text = visual.TextStim(win, text="Thank-you for your attention. \n \nThis task is complete. Please wait.",
                                   height=0.08,  # Font size
                                   bold=False,  # Font bold
                                   wrapWidth=0.8 * win_width,  # 5% of window width
                                   font='DejaVu Sans',
                                   pos=(0, 0),
                                   color="black")
    return goodbye_text

def run_intro(win, intro_text, trigger_keyList):
    intro_text.draw()
    win.flip()
    keys = event.waitKeys(keyList=trigger_keyList, clearEvents=True)
    core.wait(1)
    return keys

def run_goodbye(win, goodbye_text):
    goodbye_text.draw()
    win.flip()
    core.wait(1)
    #event.waitKeys()

def run_runs(win, runID, thisExp, fixation_text, warning_image_1, target_image, trialClock, rt_list, acc_list, results_dir, resultFile_name, used_keyList, correct_responses):
    current_dir = os.getcwd()
    stimList_name = 'run-' + str(runID) + '.csv'
    stimList_dir = os.path.join(current_dir, 'experiment_design', 'stim_lists', stimList_name)
    stim_dir = os.path.join(current_dir, 'experiment_design', 'stimuli')
    stimList = pd.read_csv(stimList_dir)
    stimList['TargetPosition_center0'] = (240 - stimList['TargetPosition'])/240
    stimList.loc[stimList['TargetPosition']==-100,'TargetPosition_center0'] = -1000
    stimList['CuePositionY_center0'] = (240-stimList['CuePositionY'])/240
    stimList.loc[stimList['CuePositionY']==-100,'CuePositionY_center0'] = -1000
    # Clock for timing
    trialClock.reset()
    for index, row in stimList.iterrows():
        trialAttributes = row.to_dict()
        thisExp.addData('TrialNumber', trialAttributes['TrialNumber'])
        thisExp.addData('WarningType', trialAttributes['WarningType'])
        thisExp.addData('TargetType', trialAttributes['TargetType'])
        thisExp.addData('FlankingType', trialAttributes['FlankingType'])
        thisExp.addData('TargetDirection', trialAttributes['TargetDirection'])
        thisExp.addData('CorrectAnswer', correct_responses[trialAttributes['TargetDirection']])
        # Duration of fixation
        setAttrib(trialAttributes, "DurationOfFixation", getAttrib(trialAttributes, "DurationOfFixation"))
        setAttrib(trialAttributes, "IntervalBetweenCueAndTarget", getAttrib(trialAttributes, "IntervalBetweenCueAndTarget") + 300)
        # Fixation start
        #fixation_text.draw()
        fixation_text.setAutoDraw(True)
        win.flip()
        thisExp.addData('fixationStart_onsetTime', trialClock.getTime())
        core.wait(getAttrib(trialAttributes, "DurationOfFixation") / 1000)
        fixation_text.setAutoDraw(False)
        # Warning slide
        fixation_text.setAutoDraw(True)
        warning_image_1.setImage(os.path.join(stim_dir, "symbolstarbig.bmp"))
        warning_image_1.setPos((0, getAttrib(trialAttributes, "CuePositionY_center0")))
        warning_image_1.draw()
        win.flip()
        thisExp.addData('cue_onsetTime', trialClock.getTime())
        core.wait(0.2)  # Assume some duration for the warning
        fixation_text.setAutoDraw(False)
        # Middle fixation
        fixation_text.setAutoDraw(True)
        win.flip()
        thisExp.addData('fixationMiddle_onsetTime', trialClock.getTime())
        core.wait(getAttrib(trialAttributes, "IntervalBetweenCueAndTarget") / 1000)
        fixation_text.setAutoDraw(False)
        # Target slide
        fixation_text.setAutoDraw(True)
        target_image.setImage(os.path.join(stim_dir, getAttrib(trialAttributes, "TargetImage") + ".bmp"))
        target_image.setPos((0, getAttrib(trialAttributes, "TargetPosition_center0")))
        target_image.draw()
        win.flip()
        target_onsetTime = trialClock.getTime()
        thisExp.addData('target_onsetTime', target_onsetTime)
        # Response collection
        keys = event.waitKeys(maxWait=getAttrib(trialAttributes, "DurationOfTarget")/ 1000, keyList=used_keyList, timeStamped=trialClock)
        if keys:
            response, reaction_time = keys[0]
            if response == 'escape':
                resultFile_name = "tmp_" + resultFile_name
                resultFile_path = os.path.join(results_dir, resultFile_name)
                thisExp.saveAsWideText(resultFile_path)
                core.quit()
            acc = 1 if response == correct_responses[trialAttributes['TargetDirection']] else 0
            thisExp.addData('reaction_time', reaction_time)
            rt = reaction_time - target_onsetTime
        else:
            response = None
            reaction_time = None
            rt = None
            acc = 0
        rt_list.append(rt)  # Store rt for current trial
        acc_list.append(acc)  # Store rt for current trial
        fixation_text.setAutoDraw(False)
        thisExp.addData('reaction_time', reaction_time)
        thisExp.addData('RT', rt)
        thisExp.addData('response', response)
        thisExp.addData('ACC', acc)

        # Fixation end
        if reaction_time is not None:
            setAttrib(trialAttributes, "DurationOfFixationEnd", getAttrib(trialAttributes, "DurationOfFixationEnd") - getAttrib(trialAttributes, "DurationOfFixation") + (2000 - rt * 1000) + 1000 - 40)
        else:
            setAttrib(trialAttributes, "DurationOfFixationEnd", getAttrib(trialAttributes, "DurationOfFixationEnd") - getAttrib(trialAttributes, "DurationOfFixation") + 1000 - 40)

        fixation_text.setAutoDraw(True)
        win.flip()
        thisExp.addData('fixationEnd_onsetTime', target_onsetTime)
        core.wait(getAttrib(trialAttributes, "DurationOfFixationEnd") / 1000)
        fixation_text.setAutoDraw(False)
        # end of trial - move to next line in data output
        thisExp.nextEntry()
    return rt_list, acc_list

def run_prac(win, thisExp, fixation_text, warning_image_1, target_image, trialClock, rt_list, acc_list, results_dir, resultFile_name, used_keyList, correct_responses):
    current_dir = os.getcwd()
    stimList_name = 'run-prac.csv'
    stimList_dir = os.path.join(current_dir, 'experiment_design', 'stim_lists', stimList_name)
    stim_dir = os.path.join(current_dir, 'experiment_design', 'stimuli')
    stimList = pd.read_csv(stimList_dir)
    stimList['TargetPosition_center0'] = (240 - stimList['TargetPosition'])/240
    stimList.loc[stimList['TargetPosition']==-100,'TargetPosition_center0'] = -1000
    stimList['CuePositionY_center0'] = (240-stimList['CuePositionY'])/240
    stimList.loc[stimList['CuePositionY']==-100,'CuePositionY_center0'] = -1000
    trials_all = stimList.sample(frac=1).reset_index(drop=True)
    trials = trials_all.iloc[0:23,:]
    # Clock for timing
    trialClock.reset()
    for index, row in trials.iterrows():
        trialAttributes = row.to_dict()
        thisExp.addData('TrialNumber', trialAttributes['TrialNumber'])
        thisExp.addData('WarningType', trialAttributes['WarningType'])
        thisExp.addData('TargetType', trialAttributes['TargetType'])
        thisExp.addData('FlankingType', trialAttributes['FlankingType'])
        thisExp.addData('TargetDirection', trialAttributes['TargetDirection'])
        thisExp.addData('CorrectAnswer', correct_responses[trialAttributes['TargetDirection']])
        # Duration of fixation
        setAttrib(trialAttributes, "DurationOfFixation", getAttrib(trialAttributes, "DurationOfFixation"))
        setAttrib(trialAttributes, "IntervalBetweenCueAndTarget", getAttrib(trialAttributes, "IntervalBetweenCueAndTarget") + 300)
        # Fixation start
        #fixation_text.draw()
        fixation_text.setAutoDraw(True)
        win.flip()
        thisExp.addData('fixationStart_onsetTime', trialClock.getTime())
        core.wait(getAttrib(trialAttributes, "DurationOfFixation") / 1000)
        fixation_text.setAutoDraw(False)
        # Warning slide
        fixation_text.setAutoDraw(True)
        warning_image_1.setImage(os.path.join(stim_dir, "symbolstarbig.bmp"))
        warning_image_1.setPos((0, getAttrib(trialAttributes, "CuePositionY_center0")))
        warning_image_1.draw()
        win.flip()
        thisExp.addData('cue_onsetTime', trialClock.getTime())
        core.wait(0.2)  # Assume some duration for the warning
        fixation_text.setAutoDraw(False)
        # Middle fixation
        fixation_text.setAutoDraw(True)
        win.flip()
        thisExp.addData('fixationMiddle_onsetTime', trialClock.getTime())
        core.wait(getAttrib(trialAttributes, "IntervalBetweenCueAndTarget") / 1000)
        fixation_text.setAutoDraw(False)
        # Target slide
        fixation_text.setAutoDraw(True)
        target_image.setImage(os.path.join(stim_dir, getAttrib(trialAttributes, "TargetImage") + ".bmp"))
        target_image.setPos((0, getAttrib(trialAttributes, "TargetPosition_center0")))
        target_image.draw()
        win.flip()
        target_onsetTime = trialClock.getTime()
        thisExp.addData('target_onsetTime', target_onsetTime)
        # Response collection
        keys = event.waitKeys(maxWait=getAttrib(trialAttributes, "DurationOfTarget")/ 1000, keyList=['f', 'j', 'escape', '1', '2', '3', '4'], timeStamped=trialClock)
        if keys:
            response, reaction_time = keys[0]
            if response == 'escape':
                resultFile_name = "tmp_prac" + resultFile_name
                resultFile_path = os.path.join(results_dir, resultFile_name)
                thisExp.saveAsWideText(resultFile_path)
                core.quit()
            acc = 1 if response == correct_responses[trialAttributes['TargetDirection']] else 0
            thisExp.addData('reaction_time', reaction_time)
            rt = reaction_time - target_onsetTime
        else:
            response = None
            reaction_time = None
            rt = None
            acc = 0
        rt_list.append(rt)  # Store rt for current trial
        acc_list.append(acc)  # Store rt for current trial
        fixation_text.setAutoDraw(False)
        thisExp.addData('reaction_time', reaction_time)
        thisExp.addData('RT', rt)
        thisExp.addData('response', response)
        thisExp.addData('ACC', acc)

        # Fixation end
        if reaction_time is not None:
            setAttrib(trialAttributes, "DurationOfFixationEnd", getAttrib(trialAttributes, "DurationOfFixationEnd") - getAttrib(trialAttributes, "DurationOfFixation") + (2000 - rt * 1000) + 1000 - 40)
        else:
            setAttrib(trialAttributes, "DurationOfFixationEnd", getAttrib(trialAttributes, "DurationOfFixationEnd") - getAttrib(trialAttributes, "DurationOfFixation") + 1000 - 40)

        fixation_text.setAutoDraw(True)
        win.flip()
        thisExp.addData('fixationEnd_onsetTime', target_onsetTime)
        core.wait(getAttrib(trialAttributes, "DurationOfFixationEnd") / 1000)
        fixation_text.setAutoDraw(False)
        # end of trial - move to next line in data output
        thisExp.nextEntry()
    return rt_list, acc_list