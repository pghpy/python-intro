# Library 'o code:
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

# Fetch the content of a web page:
url = raw_input("give me a url ")
webpage = GetWebPage(url)
print webpage

# Identify how often each word occurs in the page:
def RecordOccurrences(url, webpage):
  words = webpage.split()
  for word in words:
    occurrences.RecordWordOccurrence(url, word)

RecordOccurrences(url, webpage)
occurrences.Print()

# Extract anchor tags from document:
def GetCleanedUpLinks(url):
  webpage = GetWebPage(url)
  links = GetLinks(webpage)
  cleaned_links = []
  for link in links:
    if link.startswith('http://'):
      cleaned_links.append(link)
    else:
     cleaned_links.append(url + link)
  return cleaned_links

print GetCleanedUpLinks(url)

# Visit each link and record how often each word occurs:
AllLinks = CrawlForLinks(url, GetCleanedUpLinks)
for link in AllLinks:
  webpage = GetWebPage(link)
  RecordOccurrences(link, webpage)
occurrences.Print()

# Provide a user interface to request best page for a word:
word = raw_input("word to search for ")
bestUrl = occurrences.GetBestUrlForWord(word)
print bestUrl
