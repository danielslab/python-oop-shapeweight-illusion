# -*- coding: utf-8 -*-

import itertools
import random
import time

def ask_for_name():
    rawText = input("Please enter your name: ")
    return rawText

def ask_for_age():
    rawText = input("Please enter your age in years: ")
    return int(rawText)

def create_questions_from_stimuli(stimuli):
    # with our 6 stimuli, we can get all possible combinations
    stimuliCombinations = itertools.combinations(stimuli, 2)
    # then we can create a 'question' for each object combination
    questions = []
    for combo in stimuliCombinations:
        tq = Question(combo[0], combo[1])
        questions.append(tq)    
    return questions

def create_trials_from_questions(participant, questions):
    n=0
    trials=[]
    for q in questions:
        n += 1
        trials.append(Trial(n, participant, q))
    return trials
    
class Participant:
    def __init__(self, name, age):
        # set fields to values passed via arguments
        self.name = name
        self.age = age
    
class Stimulus:
    def __init__(self, number, shape, weight):
        # set fields to values passed via arguments
        self.number = number
        self.shape = shape
        self.weight = weight
        
class Question:
    def __init__(self, left_stimulus, right_stimulus):
        # set fields to values passed via arguments
        self.left_stimulus = left_stimulus
        self.right_stimulus = right_stimulus
        # calculate heaviest
        if left_stimulus.weight > right_stimulus.weight:
            self.heaviestPosition = "L"
            self.heaviestStimulus = left_stimulus
        else:
            self.heaviestPosition = "R"
            self.heaviestStimulus = right_stimulus
        # calculate weight difference
        self.weightDifference = abs(left_stimulus.weight - right_stimulus.weight)
    
    def ask_question(self):
        rawText = ""
        while rawText != 'L' and rawText != 'R':
            print("\n\r\n\r* Object %d vs %d * " % (self.left_stimulus.number,
                                                    self.right_stimulus.number))
            rawText = input("Which is heaver? Type (L) or (R): ").upper()
        self.answer = rawText
        self.correct = (self.answer == self.heaviestPosition)
    
    def present_feedback(self):
        if self.correct:
            message = "Correct!"
        else:
            message = ("Incorrect! %s was heavier by %dg"
                       % (self.heaviestPosition, self.weightDifference))
        print(message)
        time.sleep(0)
        
        
        
class Trial:
    def __init__(self, number, participant, question):
        # set fields to values passed via arguments
        self.number = number
        self.participant = participant
        self.question = question
    
    def list_objects(self):
        # returns comma-separated string array
        trialData = [self.number,
                     self.participant.name,
                     self.participant.age,
                     self.question.correct,
                     self.question.left_stimulus.number,
                     self.question.left_stimulus.shape,
                     self.question.left_stimulus.weight,
                     self.question.right_stimulus.number,
                     self.question.right_stimulus.shape,
                     self.question.right_stimulus.weight,
                     self.question.weightDifference,
                     self.question.heaviestPosition]                     
        return trialData
        
class Logger:
    def __init__(self, filename):
        self.filename = filename
        # open file
        self.file = open(filename,"r")
        # read file to check if it already has data...
        existingLines = self.file.read();        
        # if file was empty, we set mode to write and write headers
        if existingLines == "":
            self.file = open(filename,"w")
            headers = self.list_headers()
            self.write_comma_separated(headers)
        # else, set mode to append
        else:
            self.file = open(filename,"a")
        
        
    def list_headers(self):
        headers = ["TrialNumber",
                   "ParticipantName",
                   "ParticipantAge",
                   "TrialResult",
                   "LeftStimulusNumber",
                   "LeftStimulusShape",
                   "LeftStimulusWeight",
                   "RightStimulusNumber",
                   "RightStimulusShape",
                   "RightStimulusWeight",
                   "WeightDifference",
                   "HeaviestPosition"]
        return headers
        
    def write_comma_separated(self, objectList):
        # convert all abjects to strings and separate with comma
        line = ', '.join(str(x) for x in objectList)
        self.file.write(line + "\n")            
        
    def close(self):
        print("Data logged to %s" % self.filename)
        self.file.close()     
        
#                
# MAIN PROGRAM    
#
       
# get participant details
entered_name = ask_for_name()
entered_age = ask_for_age()
# create our new class!
participant = Participant(entered_name, entered_age) 

# define our stimuli here (could be created dynamically from file later)
s1 = Stimulus(1, 'cube', 140)
s2 = Stimulus(2, 'cube', 90)
s3 = Stimulus(3, 'cube', 70)
s4 = Stimulus(4, 'sphere', 150)
s5 = Stimulus(5, 'sphere', 100)
s6 = Stimulus(6, 'sphere', 50)
stimuli = [s1,s2,s3,s4,s5,s6]
random.shuffle(stimuli)

# create our 'questions' from our 'stimuli'
questions = create_questions_from_stimuli(stimuli)
random.shuffle(questions)

# create our 'trials' from our 'questions'
trials = create_trials_from_questions(participant, questions)

# create our Logger
logger = Logger("output_data.csv")

# run the experiment
for t in trials:
    # ask question
    t.question.ask_question()
    # present feedback
    t.question.present_feedback()
    # log data to file
    trial_data = t.list_objects()
    logger.write_comma_separated(trial_data)
    
# finish up
print("\n\rThanks for playing, %s!" % participant.name)
logger.close()
    
    