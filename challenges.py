import re
import urllib2
class WordOccurrences:
  def __init__(self):
    self.occurrences = dict()
  def RecordWordOccurrence(self, url, word):
    if word in self.occurrences:
      if url in self.occurrences[word]:
        self.occurrences[word][url] += 1
      else:
        self.occurrences[word][url] = 1
    else:
      self.occurrences[word] = { url: 1 }
  def Print(self):
    print self.occurrences
  def GetBestUrlForWord(self, word):
    if word in self.occurrences:
      inverted = dict([
        (v, k) for k, v in self.occurrences[word].iteritems()])
      highest = sorted(inverted.keys())[-1]
      return "Best URL is " + inverted[highest]
    else:
      return "Word not available anywhere"

occurrences = WordOccurrences()
def GetWebPage(url):
  print 'Getting webpage for', url
  try:
    return urllib2.urlopen(url).read()
  except:
    return ''

def GetLinks(page):
  return re.compile("href\s*=\s*\"\s*([^\"]+)\"").findall(page)

def CrawlForLinks(url, ExtractLinksFunction, depth=0):
  if depth > 1:
    return []
  links = ExtractLinksFunction(url)
  for link in links:
    links += CrawlForLinks(link, ExtractLinksFunction, depth + 1)
  return set(links)
# CHALLENGE BEGINS
# Fetch user input with raw_input(), and store it in a variable
#url = CallTheRawInputFunction("WithAPromptHere")
# Invoke GetWebPage() and store the result in a variable
#result = CallTheGetWebPageFunction(WithTheUrlHere)
# Print the result to the screen
#CallThePrintFunction(WithTheResultHere)
# CHALLENGE ENDS


# CHALLENGE BEGINS
def RecordOccurrences(url, webpage):
# Split the page into words, and store those words in a list:
#   mywords = myresult.SomeSplitFunction()
# Loop across the words and record each occurrence:
#   for SomeWord in MyListOfWords:
#     InvokeRecordOccurrenceSomeHowHere(UsingSomeWord)
RecordOccurrences(url, webpage)
occurrences.Print()
# CHALLENGE ENDS


# CHALLENGE BEGINS
def GetCleanedUpLinks(url):
# InvokeTheGetLinksFunction and store the results in a list:
#  ListOfLinks = CallTheGetLinksFunction(WithYourWebPageHere)
# Create a new empty list of cleaned-up links:
#  ListOfCleanedUpLinks = New Empty List
# Loop across the links; add each one to the cleaned up list,
# ensuring that it starts with a valid "http://..." portion.
#  for link in ListOfLinks:
#    if link starts with "http://":
#      Just add it to ListOfCleanedUpLinks
#    else:
#      Add together URL and the link, then add THAT to the
#      ListOfCleanedUpLinks
#  return ListOfCleanedUpLinks
print GetCleanedUpLinks(url)
# CHALLENGE ENDS


# CHALLENGE BEGINS
AllLinks = CallTheCrawlForLinksFunction(GetCleanedUpLinks)
# Loop across the links; for each one, fetch the webpage and
# record the word occurrences:
#  for link in AllLinks:
#    webpage = CallTheGetWebPageFunction(WithALink)
#    CallTheRecordOccurrencesFunction(WithTheWebPage)
occurrences.Print()
# CHALLENGE ENDS


# CHALLENGE BEGINS
# Ask the user for a word to search for:
#WordToSearchFor = CallTheRawInputFunction("WithAPromptHere")
# Get the best URL for that word:
#bestUrl = occurrences.CallTheGetBestFunction(ForTheWord)
# Print the best URL to the screen:
#CallThePrintFunction(WithTheBestUrl)
# CHALLENGE ENDS
