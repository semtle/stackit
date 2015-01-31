#!/usr/bin/env python
from __future__ import print_function
import sys
import stackexchange
from stackexchange import Sort

import requests
import bs4

so = stackexchange.Site(stackexchange.StackOverflow, impose_throttling=True)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        term = raw_input('Please provide a search term:')
    else:
        term = ' '.join(sys.argv[1:])
    print('Searching for %s...' % term,)
    sys.stdout.flush()

    questions = so.search(sort = Sort.Votes, intitle=term)

    for question in questions:
        if 'accepted_answer_id' in question.json:
            questionurl = question.json['link']
            answerid = question.json['accepted_answer_id']

            print('%8d %s\nAnswer ID %d' % (question.id, question.title, answerid))
            #questionurl gives the url of the SO question
            #the answer is under id "answer-answerid", and text of answer is in class post-text

            # Pulls the html from the StackOverflow site, converts to Beautiful Soup
            response = requests.get(questionurl)
            soup = bs4.BeautifulSoup(response.text)
            # Prints the accepted answer div, concatonated "answer-" and answerid
            print(soup.find("div", {"id": "answer-"+str(answerid)}))