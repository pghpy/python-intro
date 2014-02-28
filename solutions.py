# Library 'o code:
import re
import urllib2


class WordOccurrences:

    def __init__(self):
        self.occurrences = dict()

    def __repr__(self):
        output = ''
        for word in self.occurrences:
            output += '{}:\n'.format(word)
            for url in self.occurrences[word]:
                output += '  {}: {}\n'.format(url, self.occurrences[word][url])
        return output

    def record_word_occurrence(self, url, word):
        if word in self.occurrences:
            if url in self.occurrences[word]:
                self.occurrences[word][url] += 1
            else:
                self.occurrences[word][url] = 1
        else:
            self.occurrences[word] = {url: 1}

    #def print(self):
    #    print self.occurrences

    def get_best_url_for_word(self, word):
        if word in self.occurrences:
            inverted = dict([
                (v, k) for k, v in self.occurrences[word].iteritems()])
            highest = sorted(inverted.keys())[-1]
            return "Best URL is " + inverted[highest]
        else:
            return "Word not available anywhere"

occurrences = WordOccurrences()


def get_web_page(url):
    print 'Getting webpage for: ', url
    try:
        return urllib2.urlopen(url).read()
    except:
        return ''


def get_links(page):
    return re.compile("href\s*=\s*\"\s*([^\"]+)\"").findall(page)


def crawl_for_links(url, extract_links_function, depth=0):
    if depth > 1:
        return []
    links = extract_links_function(url)
    for link in links:
        links += crawl_for_links(link, extract_links_function, depth + 1)
    return set(links)

# Fetch the content of a web page:
url = raw_input("give me a url: ")
webpage = get_web_page(url)
print webpage

# Identify how often each word occurs in the page:


def record_occurrences(url, webpage):
    words = webpage.split()
    for word in words:
        occurrences.record_word_occurrence(url, word)

record_occurrences(url, webpage)
print occurrences

# Extract anchor tags from document:


def get_cleaned_links(url):
    webpage = get_web_page(url)
    links = get_links(webpage)
    cleaned_links = []
    for link in links:
        if link.startswith('http://'):
            cleaned_links.append(link)
        else:
            cleaned_links.append(url + link)
    return cleaned_links

print get_cleaned_links(url)

# Visit each link and record how often each word occurs:
all_links = crawl_for_links(url, get_cleaned_links)
for link in all_links:
    webpage = get_web_page(link)
    record_occurrences(link, webpage)

print occurrences

# Provide a user interface to request best page for a word:
word = raw_input("word to search for: ")
best_url = occurrences.get_best_url_for_word(word)
print best_url
