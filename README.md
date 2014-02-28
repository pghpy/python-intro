# Intro to Python

- [Advertisement](#advertisement)
- [Overview & Intro](#overview--intro)
- [Set up PythonAnywhere account; hello world; initial code](#set-up-pythonanywhere-account-hello-world-initial-code)
- [Fetch the content of a web page](#fetch-the-content-of-a-web-page)
- [Identify how often each word occurs in the page](#identify-how-often-each-word-occurs-in-the-page)
- [Extract anchor tags from document](#extract-anchor-tags-from-document)
- [Visit each link and record how often each word occurs](#visit-each-link-and-record-how-often-each-word-occurs)
- [Provide a user interface to request which page(s) are best matches for which word(s)](#provide-a-user-interface-to-request-which-pages-are-best-matches-for-which-words)


## Advertisement

“Tired of Java, C++, Go, Ada, Pascal, Assembler, JavaScript, PHP, Ruby, and Visual Basic?
Longing to learn Python?
Jealous of how cool your Pythonista friends are?
Bored by lesser serpents?
LEARN PYTHON WITH THE PITTSBURGH PYTHON GROUP!

Join us as Steve Gross guides you on a wondrous journey of Writing a Search Engine! We'll traverse the web! Index its contents!”

This doc: https://github.com/pghpy/python-intro
Editor site: http://www.pythonanywhere.com


## Overview & Intro

Hi everyone!
I'm Steve, a Googler! Now let's learn everyone's name :)
Most importantly, before anything else: happy hour @ Social afterwards!
What's Pittsburgh Python? Who's involved?
Recruiting @ Google.
Stratification by talent: who's totally new to coding? Who's ok at coding but new to Python? Who's good with python?
We'll divide into groups of 5. Please make sure to link up with at least someone in each of those 3 groups.
This workshop is structured in 6 15-minute increments. We'll keep it on schedule!
Pull out that laptop and connect to the free free free Google WiFi!!!
BTW: You'll notice that I embedded lots of links in this doc. They're there to help you!
Note also that each exercise builds on the last one. Don't delete your work when you're done with an exercise; the next one will use the work from the last one.
If you are really stuck, there's a full solution [here](https://github.com/pghpy/python-intro/blob/master/solutions.py).

This class is intended for people with little programming background, but a decent understanding of logic, arithmetic, etc.

Let’s build a search engine! It will give us the opportunity to learn some Python basics and bit-by-bit make it more complicated. We’ll work towards an application that can crawl the web, analyze its contents, index them, and provide a basic interface for searching.

## Set up PythonAnywhere account; hello world; initial code

Setup account: Go to www.pythonanywhere.com and create an account. There should be a free option!

Hello World: Create a new file (e.g.: "mycode.py"); copy-and-paste the following code into it: print "Hello, World!" Click "Save & Run". Luxuriate in the glory that is a console screen with the words "Hello, World!". You ARE a programmer today!

Tonight's library 'o code: Delete the contents from mycode.py; replace by copy-and-pasting the following chunk 'o code:

```python
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
```

## Fetch the content of a web page

So, we're going to grab a web page. That's actually something called an "HTTP get" operation. A web page is actually a document, right? Let's see what that document looks like (we'll pull up CNN.com and inspect the source). Woohoo! A text document! No pretty pictures, but if you dig through it you can find parts that look familiar. So to get a web page we need to specify a URL to some web-page-fetching mechanism.
Also, to do this we're going to let the user specify on the console which URL to get. That means we'll need to get user input working.
Also: Note that I've embedded clickable links in the coding challenge to help you look up how to do things. Saving you time, right?
Also: Note that Pythonanywhere may restrict which URLs you can use; see this document for a list.

Coding challenge: Ask the user for a URL, fetch the webpage and print it to the screen.

```python
# CHALLENGE BEGINS
# Fetch user input with raw_input(), and store it in a variable
#url = CallTheRawInputFunction("WithAPromptHere")
# Invoke GetWebPage() and store the result in a variable
#result = CallTheGetWebPageFunction(WithTheUrlHere)
# Print the result to the screen
#CallThePrintFunction(WithTheResultHere)
# CHALLENGE ENDS
```

## Identify how often each word occurs in the page

Great, we fetched a web page. But we want to a build a search engine, right? Fetching a page is only the beginning. Typically, when you search on the web you do so with a keyword. For instance, will Google please tell me where to find "apples"? Aha! A search result page; each page has the word "apples" on it in some meaningful way. Plus, Google probably has done a little more work figuring out the best pages for my search. Probably, right?

Let's dig deeper into this problem. Let's identify all the words on a web page and count how often each one occurs. To do this, we'll use a the WordOccurences class supplied in the library at the top. The instance of this class is called "occurrences"; it provides several functions. The function you'll care about in this exercise is called "RecordOccurrence".

Coding challenge: Identify how often each word occurs in the page.

```python
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
```

## Extract anchor tags from document

I seem to recall that a webpage often has links in it, right? I mean, isn't that the whole idea of the web? What does a link actually look like?

It looks like this!
  `<a href="http://someotherpage.com/some/path/here">My link!</a>`
And sometimes it looks like this:
  `<a href="/some/path/here">My link!</a>`
Ummmmm.... What happened to the "http://someotherpage.com" part? It's implicitly on the same site!

In order to build a search engine, we need to spider the web (also called "crawling"). To start with that, we need to identify all the links in a page. Fortunately for you, you do not have to learn HTML/XML parsing or RegEx (regular expressions). But somehow, we need to get all the links out of our webpage, right? Mercifully, this workshop has already included a function to get the links out of a page. 

Coding challenge: Extract all the links from your page, and make sure all of them include a leading "http://somesite" portion.

```python
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
```

## Visit each link and record how often each word occurs

Now we start putting this all together into something useful. We'll start with the initial user-supplied URL, and crawl that page to get all possible anchor tags. Fortunately, we don't have to write our own recursive algorithm. That's already supplied in the library (called "CrawlForLinks".

Coding challenge: Crawl the web, and record word occurences for each crawled page.

```python
# CHALLENGE BEGINS
AllLinks = CallTheCrawlForLinksFunction(GetCleanedUpLinks)
# Loop across the links; for each one, fetch the webpage and
# record the word occurrences:
#  for link in AllLinks:
#    webpage = CallTheGetWebPageFunction(WithALink)
#    CallTheRecordOccurrencesFunction(WithTheWebPage)
occurrences.Print()
# CHALLENGE ENDS
```

## Provide a user interface to request which page(s) are best matches for which word(s)

Let's tie it all together. We'll have the user request a particular word, and our application will reply with the URL that contains the most occurrences of that word.

Coding challenge: Ask the user for a word to search for, and report the best URL for that word.

```python
# CHALLENGE BEGINS
# Ask the user for a word to search for:
#WordToSearchFor = CallTheRawInputFunction("WithAPromptHere")
# Get the best URL for that word:
#bestUrl = occurrences.CallTheGetBestFunction(ForTheWord)
# Print the best URL to the screen:
#CallThePrintFunction(WithTheBestUrl)
# CHALLENGE ENDS
```

Contact info:

Steve Gross
mrstevegross@gmail.com
@mrstevegross (twitter)
