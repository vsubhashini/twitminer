# NLP Programming Assignment #3
# NaiveBayes
# 2012

#
# The area for you to implement is marked with TODO!
# Generally, you should not need to touch things *not* marked TODO
#
# Remember that when you submit your code, it is not run from the command line 
# and your main() will *not* be run. To be safest, restrict your changes to
# addExample() and classify() and anything you further invoke from there.
#


import sys
import getopt
import os
import math

class NaiveBayes:
  class TrainSplit:
    """Represents a set of training/testing data. self.train is a list of Examples, as is self.test. 
    """
    def __init__(self):
      self.train = []
      self.test = []

  class Example:
    """Represents a document with a label. klass is 'Politics' or 'Sports' by convention.
       words is a list of strings in the tweet message.
       tweetid is the tweet id
    """
    def __init__(self):
      self.klass = ''
      self.words = []
      self.tweetid= ''


  def __init__(self):
    """NaiveBayes initialization"""
    self.FILTER_STOP_WORDS = False
    self.stopList = set(self.readFile('english.stop'))
    self.numFolds = 10
    self.posDict={};
    self.negDict={};
    self.vocabulary=set();

  #############################################################################
  # TODO TODO TODO TODO TODO 
  
  def wordCount(self, dictionary):
    """ My method 
      to count the total words in each class (Politics and Sports dictionaries)
    """
    count=0;
    for item in dictionary:
      count+=dictionary.get(item);
    return count

  def classify(self, words):
    """ TODO
      'words' is a list of words to classify. Return 'Politics' or 'Sports' classification.
    """
    posSentenceProb = 0.0;
    negSentenceProb = 0.0;
    posCount = self.wordCount(self.posDict);
    negCount = self.wordCount(self.negDict);
    vocabLen = len(self.vocabulary);
    for word in words:
      poswordCount = self.posDict.get(word);
      if poswordCount is None:
      	poswordCount=0;
      posWordProb = (poswordCount+1.0)/(posCount + vocabLen);
      posSentenceProb += math.log(posWordProb);
      negwordCount = self.negDict.get(word);
      if negwordCount is None:
      	negwordCount=0;
      negWordProb = (negwordCount+1.0)/(negCount + vocabLen);
      negSentenceProb += math.log(negWordProb);
    #print (words, negSentenceProb, posSentenceProb);
    if negSentenceProb>posSentenceProb:
      return 'Sports'
    return 'Politics'
  

  def addExample(self, klass, words):
    """
     * TODO
     * Train your model on an example document with label klass ('Politics' or 'Sports') and
     * words, a list of strings.
     * You should store whatever data structures you use for your classifier 
     * in the NaiveBayes class.
     * Returns nothing
    """
    for word in words:
      if klass=='Politics':
        count=self.posDict.get(word);
	if count is None:
	  count=0;
	self.posDict[word]=count+1;
        #print(klass, word);
      elif klass=='Sports':
        count=self.negDict.get(word);
	if count is None:
	  count=0;
	self.negDict[word]=count+1;
        #print(klass, word);
      self.vocabulary.add(word); 
    pass
      

  # TODO TODO TODO TODO TODO 
  #############################################################################
  
  def readFile(self, fileName):
    """
     * Code for reading a file.  you probably don't want to modify anything here, 
     * unless you don't like the way we segment files.
    """
    contents = []
    f = open(fileName)
    for line in f:
      contents.append(line)
    f.close()
    result = self.segmentWords('\n'.join(contents)) 
    return result

  def readTweet(self, tweetSample, test):
    """
     * Code for reading a tweet message.
     *   Leaves out first 2 values corresponding to id and class if train sample
     *   Leaves out first value corresponding to id if test sample
    """
    if test:
      return (tweetSample[1:])
    return (tweetSample[2:])

  
  def segmentWords(self, s):
    """
     * Splits lines on whitespace for file reading
    """
    return s.split()

  
  def trainSplit(self, trainFile):
    """Takes in a trainFile, returns one TrainSplit with train set."""
    split = self.TrainSplit()
    with open(trainFile) as fid:
      for line in fid:
	tweetsample = line.split()
        example = self.Example()
        example.words = self.readTweet(tweetsample, False)
        example.klass = tweetsample[1]
        example.tweetid = tweetsample[0]
        split.train.append(example)
    return split

  def train(self, split):
    for example in split.train:
      words = example.words
      if self.FILTER_STOP_WORDS:
        words =  self.filterStopWords(words)
      self.addExample(example.klass, words)

  def test(self, split):
    """Returns a list of labels for split.test."""
    labels = []
    for example in split.test:
      words = example.words
      if self.FILTER_STOP_WORDS:
        words =  self.filterStopWords(words)
      guess = self.classify(words)
      labels.append(guess)
    return labels
  
  def buildSplits(self, args):
    """Builds the splits for training/testing"""
    splits = []
    trainFile = args[0]
    if len(args) == 2:
      testFile = args[1]
    if len(args) < 1: 
      print '[Usage] trainFile [testFile]'

    split = self.TrainSplit()
    with open(trainFile) as fid:
      for line in fid:
        tweetsample = line.split()
        example = self.Example()
        example.tweetid = tweetsample[0]
        example.klass = tweetsample[1]
        example.words = self.readTweet(tweetsample, False)
        split.train.append(example)
    with open(testFile) as fid:
      for line in fid:
        tweetsample = line.split()
        example = self.Example()
        example.tweetid = tweetsample[0]
        #example.klass = tweetsample[1] #comment
        example.words = self.readTweet(tweetsample, True)
        #example.words = self.readTweet(tweetsample, False)
        split.test.append(example)
    splits.append(split)
    return splits


  def buildCrossValidationSplits(self, args):
    """Builds the splits for training/testing"""
    splits = []
    trainFile = args[0]
    if len(args) == 2:
      testFile = args[1]
    if len(args) < 1: 
      print '[Usage] trainFile [testFile] %Input just trainfile for 10fold cross validation'

    """Create splits to perform n-fold cross validation"""
    fid = open(trainFile);
    numSamples = sum(1 for line in fid);
    fid.close();
    for fold in range(0, self.numFolds):
      split = self.TrainSplit()
      testStartLine = (numSamples * fold) / self.numFolds;
      testEndLine = testStartLine + (numSamples / self.numFolds);
      with open(trainFile) as fid:
        lineCounter=0;
        for line in fid:
	  if (lineCounter >= testStartLine) and (lineCounter <= testEndLine):
            tweetsample = line.split()
            example = self.Example()
            example.words = self.readTweet(tweetsample, False)
            example.klass = tweetsample[1]
            example.tweetid = tweetsample[0]
            split.test.append(example)
          else:
            tweetsample = line.split()
            example = self.Example()
            example.words = self.readTweet(tweetsample, False)
            example.klass = tweetsample[1]
            example.tweetid = tweetsample[0]
            split.train.append(example)
          lineCounter+=1;
      splits.append(split)
    return splits
  
  def filterStopWords(self, words):
    """Filters stop words."""
    filtered = []
    for word in words:
      if not word in self.stopList and word.strip() != '':
        filtered.append(word)
    return filtered



def main():
  nb = NaiveBayes()
  (options, args) = getopt.getopt(sys.argv[1:], 'f')
  if ('-f','') in options:
    nb.FILTER_STOP_WORDS = True
  
  testing=False
  if len(args)==1:
    splits = nb.buildCrossValidationSplits(args)
  elif len(args)==2:
    splits = nb.buildSplits(args)
    testing=True
  else:
    print '[Usage] trainFile testFile'
  avgAccuracy = 0.0
  fold = 0
  for split in splits:
    classifier = NaiveBayes()
    accuracy = 0.0
    for example in split.train:
      words = example.words
      if nb.FILTER_STOP_WORDS:
        words =  classifier.filterStopWords(words)
      classifier.addExample(example.klass, words)
  
    with open('outputPredictions.txt', 'w+') as opfid:
      for example in split.test:
        words = example.words
        if nb.FILTER_STOP_WORDS:
          words =  classifier.filterStopWords(words)
        guess = classifier.classify(words)
        if example.klass!=None:
          if example.klass == guess:
            accuracy += 1.0
        opfid.write(example.tweetid);
	opfid.write(" ");
	opfid.write(guess);
	opfid.write("\n");

    accuracy = accuracy / len(split.test)
    avgAccuracy += accuracy
    if not testing:
      print '[INFO]\tFold %d Accuracy: %f' % (fold, accuracy) 
    fold += 1
  avgAccuracy = avgAccuracy / fold
  if not testing:
    print '[INFO]\tAccuracy: %f' % avgAccuracy
  else:
    print 'Predictions in outputPredictions.txt';

if __name__ == "__main__":
    main()
