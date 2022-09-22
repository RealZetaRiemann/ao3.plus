"""Flask app for ao3graph.com"""
import re
import secrets
from datetime import datetime
from flask import Flask, render_template, request, session, flash
import requests
from bs4 import BeautifulSoup
from flask_mail import Message, Mail
from database import list_to_table, dict_to_table, table_to_dict, table_to_list
from funcs import wordcloud_from_dict, ContactForm

mail = Mail()

app = Flask(__name__)

app.secret_key = secrets.token_bytes(32)   # check for tampering

app.config['MAIL_SERVER'] = '192.168.1.10'

mail.init_app(app)

@app.route("/")
def index():
    """ Renders user input screen and home page """
    failure = False
    return render_template('index.html', failure = failure)

@app.route('/dash/', methods = ['POST', 'GET]'])
def dashboard():
    """ Renders dashboard for given username """
    if request.method == 'GET':
        return "The URL /dash is accessed directly. Try going to the home page to enter your username."
    if request.method == 'POST':
        user = request.form.get("username")                                     # get username
        session["user"] = user                                                  # save username during session across pages

        url = "https://archiveofourown.org/users/" + user + "/profile"          # url of user's profile page

        session["url"] = url
        urlb = "https://archiveofourown.org/users/" + user + "/bookmarks"       # url of user's bookmarks page
        urlw = "https://archiveofourown.org/users/" + user + "/works"           # url of user's works page

        profile = requests.get(url)                                             # get profile url contents
        soup = BeautifulSoup(profile.text, "html.parser")                       # formats profile results

        user_check = soup.find('div', class_="flash error")
        if user_check:
            user_check = user_check.text
        if user_check == "Sorry, there's no user by that name.":               # check if username exists
            failure = True
            return render_template('index.html',  failure = failure)            # if user doesn't exist, return to index

        icon = soup.find_all('img', class_="icon")[0]['src']                    # url of user's profile picture
        session["icon"] = icon
        date_created = datetime.fromisoformat(soup.find('dl', class_="meta").find_all('dd')[1].text)
        current_date = datetime.now()
        days_active = str(current_date - date_created).split(' ')                                              
        years_active = round((float(days_active[0]) / 365.25),2)
        session["years"] = years_active

        # initialize bookmarks data storage:
        blinks = []
        btitles = []
        bauthorsd = {}
        bgifteesd = {}
        bfandomsd = {}
        bratingsd = {
            "General Audiences": 0,
            "Teen And Up Audiences": 0,
            "Explicit": 0,
            "Mature": 0,
            "Not Rated": 0
        }
        bwarningsd = {
            "No Archive Warnings Apply": 0,
            "Choose Not To Use Archive Warnings": 0,
            "Major Character Death": 0,
            "Graphic Depictions Of Violence": 0,
            "Rape/Non-Con": 0,
            "Underage": 0
        }
        bcategoriesd = {
            "F/M": 0,
            "F/F": 0,
            "M/M": 0,
            "Gen": 0,
            "Multi": 0,
            "Other": 0,
            "No category": 0
        }
        bcompletiond = {
            "Complete Work": 0,
            "Work in Progress": 0,
            "Series in Progress": 0,
            "Complete Series": 0
        }
        brelationshipsd = {}
        bcharactersd = {}
        btagsd = {}
        blanguagesd = {}
        bwords = []
        bcollections = []
        bcomments = []
        bkudos = []
        bbookmarks = []
        bhits = []
        bdatesp = []
        bdatesbm = []

        # initialize works data storage:
        wlinks = []
        wtitles = []
        wauthorsd = {}
        wgifteesd = {}
        wfandomsd = {}
        wratingsd = {
            "General Audiences": 0,
            "Teen And Up Audiences": 0,
            "Explicit": 0,
            "Mature": 0,
            "Not Rated": 0
        }
        wwarningsd = {
            "No Archive Warnings Apply": 0,
            "Choose Not To Use Archive Warnings": 0,
            "Major Character Death": 0,
            "Graphic Depictions Of Violence": 0,
            "Rape/Non-Con": 0,
            "Underage": 0
        }
        wcategoriesd = {
            "F/M": 0,
            "F/F": 0,
            "M/M": 0,
            "Gen": 0,
            "Multi": 0,
            "Other": 0,
            "No category": 0
        }
        wcompletiond = {
            "Complete Work": 0,
            "Work in Progress": 0,
            "Series in Progress": 0,
            "Complete Series": 0
        }
        wrelationshipsd = {}
        wcharactersd = {}
        wtagsd = {}
        wlanguagesd = {}
        wwords = []
        wcollections = []
        wcomments = []
        wkudos = []
        wbookmarks = []
        whits = []
        wdatesp = []

        bookmarks = requests.get(urlb)                                                 # get bookmarks url contents
        bsoup = BeautifulSoup(bookmarks.text, "html.parser")                           # formats bookmarks results

        fanfics = bsoup.find_all('li', role="article")                                 # stores individual fanfic data
        pages = bsoup.find('ol', class_="pagination actions").find_all('li') \
            if bsoup.find('ol', class_="pagination actions") else [0,0]                # stores page navigation data

        count = 1

        while count < len(pages):
            for fic in fanfics:                                                                            # loop through every fic on the page
                if fic.find('p', text = "This has been deleted, sorry!") is None:                          # make sure fic hasn't been deleted
                    link = fic.div.h4.a['href']                                                            # get work link
                    blinks.append(link)                                                                    # add work link to list

                    title = fic.div.h4.a.text                                                              # get fanfic title
                    btitles.append(title)                                                                  # add fanfic title to list

                    authors = fic.div.h4.find_all('a', rel="author") \
                        if fic.div.h4.find('a', rel="author") else 'Anonymous'                             # get author name(s)
                    if authors != 'Anonymous':
                        for a in authors:
                            author = a.text
                            if author in bauthorsd:
                                bauthorsd[author] += 1                                                     # increase that author's count
                            else:
                                bauthorsd[author] = 1                                                      # or add author to dictionary

                    giftee = fic.div.h4.find_all('a', href=re.compile("/gifts")) \
                        if fic.div.h4.find('a', href=re.compile("/gifts")) else 'None'                     # get giftee name
                    if giftee != 'None':
                        for g in giftee:
                            gift = g.text
                            if gift in bgifteesd:
                                bgifteesd[gift] += 1                                                       # increase that giftees's count
                            else:
                                bgifteesd[gift] = 1                                                        # or add giftee to dictionary

                    fandoms = fic.div.h5.find_all('a')                                                     # get list of fandoms
                    for f in fandoms:
                        fandom = f.text
                        if fandom in bfandomsd:
                            bfandomsd[fandom] += 1                                                         # increase that fandom's count
                        else:
                            bfandomsd[fandom] = 1                                                          # or add fandom to dictionary

                    ratings = fic.div.ul.find('span', class_=re.compile("rating")).text.split(", ")        # get list of ratings
                    for r in ratings:                                                                      # add each rating to dictionary count
                        bratingsd[r] += 1

                    warnings = fic.div.ul.find('span', class_=re.compile("warnings")).text.split(", ")     # get list of warnings
                    for w in warnings:                                                                     # add each warning to dictionary count
                        bwarningsd[w] += 1

                    categories = fic.div.ul.find('span', class_=re.compile("category")).text.split(", ")   # get list categories
                    for c in categories:                                                                   # add each category to dictionary count
                        bcategoriesd[c] += 1

                    completion = fic.div.ul.find('span', class_=re.compile("iswip")).text.split(", ")      # get list of statuses
                    for c in completion:                                                                   # add completion statuses to dictionary count
                        bcompletiond[c] += 1

                    relationships = fic.find_all('li', class_='relationships') \
                        if fic.find('li', class_='relationships') else 'None'                              # get relationships
                    if relationships != 'None':
                        for r in relationships:
                            ship = r.text
                            if ship in brelationshipsd:                                                        # increase that relationship's count
                                brelationshipsd[ship] += 1
                            else:                                                                              # or add relationship to dictionary
                                brelationshipsd[ship] = 1

                    characters = fic.find_all('li', class_='characters') \
                        if fic.find('li', class_='characters') else 'None'                                 # get relationships
                    if characters != 'None':
                        for c in characters:
                            character = c.text
                            if character in bcharactersd:                                                      # increase that character's count
                                bcharactersd[character] += 1
                            else:                                                                              # or add character to dictionary
                                bcharactersd[character] = 1

                    tags = fic.find_all('li', class_='freeforms') \
                        if fic.find('li', class_='freeforms') else 'None'                                  # get tags
                    if tags != 'None':
                        for t in tags:
                            tag = t.text
                            if tag in btagsd:                                                              # increase that tag's count
                                btagsd[tag] += 1
                            else:                                                                          # or add tag to dictionary
                                btagsd[tag] = 1

                    languages = fic.find_all('dd', class_="language")                                      # get list of languages
                    for l in languages:
                        language = l.text
                        if language in blanguagesd:                                                        # increase that language's count
                            blanguagesd[language] += 1
                        else:                                                                              # or add language to dictionary
                            blanguagesd[language] = 1

                    words = fic.find('dd', class_="words").text \
                        if fic.find('dd', class_="words") else \
                            fic.dd.text                                                                    # get word count (for works OR series)
                    bwords.append(words)                                                                   # add word count to list

                    collections = fic.find('dd', class_="collections").text \
                        if fic.find('dd', class_="collections") else 0                                     # get collection count
                    bcollections.append(collections)                                                       # add collection count to list

                    comments = fic.find('dd', class_="comments").text \
                        if fic.find('dd', class_="comments") else 0                                        # get comment count
                    bcomments.append(comments)                                                             # add comment count to list

                    kudos = fic.find('dd', class_="kudos").text \
                        if fic.find('dd', class_="kudos") else 0                                           # get kudos count
                    bkudos.append(kudos)                                                                   # add kudos count to list

                    bookmarks = fic.dl.find('a', href=re.compile("/bookmarks")).text \
                        if fic.dl.find('a', href=re.compile("/bookmarks")) else 0                          # get bookmarks count
                    bbookmarks.append(bookmarks)                                                           # add bookmarks count to list

                    hits = fic.find('dd', class_="hits").text \
                        if fic.find('dd', class_="hits") else 0                                            # get kudos count
                    bhits.append(hits)                                                                     # add kudos count to list

                    date_posted = fic.div.find('p', class_=("datetime")).text                              # get date posted
                    bdatesp.append(date_posted)                                                            # add date posted to list

                    date_bookmarked = fic.select('div')[2].find('p', class_="datetime").text               # get date bookmarked
                    bdatesbm.append(date_bookmarked)                                                       # add date bookmarked to list

            count += 1
            urlb = "https://archiveofourown.org/users/" + user + "/bookmarks" + "?page=" + str(count)      # url of next bookmarks page
            bookmarks = requests.get(urlb)                                                                 # next bookmarks page contents
            bsoup = BeautifulSoup(bookmarks.text, "html.parser")                                           # formats bookmarks results
            fanfics = bsoup.find_all('li', role="article")                                                 # stores individual fanfic data

        # update database tables
        list_to_table(user, blinks, "BLINKS")
        list_to_table(user, btitles, "BTITLES")
        dict_to_table(user, bauthorsd, "BAUTHORS")
        dict_to_table(user, bgifteesd, "BGIFTEES")
        dict_to_table(user, bfandomsd, "BFANDOMS")
        dict_to_table(user, bratingsd, "BRATINGS")
        dict_to_table(user, bwarningsd, "BWARNINGS")
        dict_to_table(user, bcategoriesd, "BCATEGORIES")
        dict_to_table(user, bcompletiond, "BCOMPLETION")
        dict_to_table(user, brelationshipsd, "BRELATIONSHIPS")
        dict_to_table(user, bcharactersd, "BCHARACTERS")
        dict_to_table(user, btagsd, "BTAGS")
        dict_to_table(user, blanguagesd, "BLANGUAGES")
        list_to_table(user, bwords, "BWORDS")
        list_to_table(user, bcollections, "BCOLLECTIONS")
        list_to_table(user, bcomments, "BCOMMENTS")
        list_to_table(user, bkudos, "BKUDOS")
        list_to_table(user, bbookmarks, "BBOOKMARKS")
        list_to_table(user, bhits, "BHITS")
        list_to_table(user, bdatesp, "BDATESP")
        list_to_table(user, bdatesbm, "BDATESBM")

        works = requests.get(urlw)                                                     # get works url contents
        wsoup = BeautifulSoup(works.text, "html.parser")                               # formats works results

        fanfics = wsoup.find_all('li', role="article")                                 # stores individual fanfic data
        pages = wsoup.find('ol', class_="pagination actions").find_all('li') \
            if wsoup.find('ol', class_="pagination actions") else [0,0]                # stores page navigation data

        count = 1

        while count < len(pages):
            for fic in fanfics:                                                                            # loop through every fic on the page
                if fic.find('p', text = "This has been deleted, sorry!") is None:                          # make sure fic hasn't been deleted
                    link = fic.div.h4.a['href']                                                            # get work link
                    wlinks.append(link)                                                                    # add work link to list

                    title = fic.div.h4.a.text                                                              # get fanfic title
                    wtitles.append(title)                                                                  # add fanfic title to list

                    authors = fic.div.h4.find_all('a', rel="author") \
                        if fic.div.h4.find('a', rel="author") else 'Anonymous'                             # get author name(s)
                    if authors != 'Anonymous':
                        for a in authors:
                            author = a.text
                            if author in wauthorsd:
                                wauthorsd[author] += 1                                                     # increase that author's count
                            else:
                                wauthorsd[author] = 1                                                      # or add author to dictionary

                    giftee = fic.div.h4.find_all('a', href=re.compile("/gifts")) \
                        if fic.div.h4.find('a', href=re.compile("/gifts")) else 'None'                     # get giftee name
                    if giftee != 'None':
                        for g in giftee:
                            gift = g.text
                            if gift in wgifteesd:
                                wgifteesd[gift] += 1                                                       # increase that giftees's count
                            else:
                                wgifteesd[gift] = 1                                                        # or add giftee to dictionary

                    fandoms = fic.div.h5.find_all('a')                                                     # get list of fandoms
                    for f in fandoms:
                        fandom = f.text
                        if fandom in wfandomsd:
                            wfandomsd[fandom] += 1                                                         # increase that fandom's count
                        else:
                            wfandomsd[fandom] = 1                                                          # or add fandom to dictionary

                    ratings = fic.div.ul.find('span', class_=re.compile("rating")).text.split(", ")        # get list of ratings
                    for r in ratings:                                                                      # add each rating to dictionary count
                        wratingsd[r] += 1

                    warnings = fic.div.ul.find('span', class_=re.compile("warnings")).text.split(", ")     # get list of warnings
                    for w in warnings:                                                                     # add each warning to dictionary count
                        wwarningsd[w] += 1

                    categories = fic.div.ul.find('span', class_=re.compile("category")).text.split(", ")   # get list categories
                    for c in categories:                                                                   # add each category to dictionary count
                        wcategoriesd[c] += 1

                    completion = fic.div.ul.find('span', class_=re.compile("iswip")).text.split(", ")      # get list of statuses
                    for c in completion:                                                                   # add completion statuses to dictionary count
                        wcompletiond[c] += 1

                    relationships = fic.find_all('li', class_='relationships') \
                        if fic.find('li', class_='relationships') else 'None'                              # get relationships
                    if relationships != 'None':
                        for r in relationships:
                            ship = r.text
                            if ship in wrelationshipsd:                                                        # increase that relationship's count
                                wrelationshipsd[ship] += 1
                            else:                                                                              # or add relationship to dictionary
                                wrelationshipsd[ship] = 1

                    characters = fic.find_all('li', class_='characters') \
                        if fic.find('li', class_='characters') else 'None'                                 # get relationships
                    if characters != 'None':
                        for c in characters:
                            character = c.text
                            if character in wcharactersd:                                                      # increase that character's count
                                wcharactersd[character] += 1
                            else:                                                                              # or add character to dictionary
                                wcharactersd[character] = 1

                    tags = fic.find_all('li', class_='freeforms') \
                        if fic.find('li', class_='freeforms') else 'None'                                  # get tags
                    if tags != 'None':
                        for t in tags:
                            tag = t.text
                            if tag in wtagsd:                                                              # increase that tag's count
                                wtagsd[tag] += 1
                            else:                                                                          # or add tag to dictionary
                                wtagsd[tag] = 1

                    languages = fic.find_all('dd', class_="language")                                      # get list of languages
                    for l in languages:
                        language = l.text
                        if language in wlanguagesd:                                                        # increase that language's count
                            wlanguagesd[language] += 1
                        else:                                                                              # or add language to dictionary
                            wlanguagesd[language] = 1

                    words = fic.find('dd', class_="words").text \
                        if fic.find('dd', class_="words") else \
                            fic.dd.text                                                                    # get word count (for works OR series)
                    wwords.append(words)                                                                   # add word count to list

                    collections = fic.find('dd', class_="collections").text \
                        if fic.find('dd', class_="collections") else 0                                     # get collection count
                    wcollections.append(collections)                                                       # add collection count to list

                    comments = fic.find('dd', class_="comments").text \
                        if fic.find('dd', class_="comments") else 0                                        # get comment count
                    wcomments.append(comments)                                                             # add comment count to list

                    kudos = fic.find('dd', class_="kudos").text \
                        if fic.find('dd', class_="kudos") else 0                                           # get kudos count
                    wkudos.append(kudos)                                                                   # add kudos count to list

                    bookmarks = fic.dl.find('a', href=re.compile("/bookmarks")).text \
                        if fic.dl.find('a', href=re.compile("/bookmarks")) else 0                          # get bookmarks count
                    wbookmarks.append(bookmarks)                                                           # add bookmarks count to list

                    hits = fic.find('dd', class_="hits").text \
                        if fic.find('dd', class_="hits") else 0                                            # get kudos count
                    whits.append(hits)                                                                     # add kudos count to list

                    date_posted = fic.div.find('p', class_=("datetime")).text                              # get date posted
                    wdatesp.append(date_posted)                                                            # add date posted to list

            count += 1
            urlw = "https://archiveofourown.org/users/" + user + "/works" + "?page=" + str(count)          # url of user's next bookmarks page
            works = requests.get(urlw)                                                                     # get next bookmarks page contents
            wsoup = BeautifulSoup(works.text, "html.parser")                                               # formats bookmarks results
            fanfics = wsoup.find_all('li', role="article")                                                 # stores individual fanfic data

        # update database tables
        list_to_table(user, wlinks, "WLINKS")
        list_to_table(user, wtitles, "WTITLES")
        dict_to_table(user, wauthorsd, "WAUTHORS")
        dict_to_table(user, wgifteesd, "WGIFTEES")
        dict_to_table(user, wfandomsd, "WFANDOMS")
        dict_to_table(user, wratingsd, "WRATINGS")
        dict_to_table(user, wwarningsd, "WWARNINGS")
        dict_to_table(user, wcategoriesd, "WCATEGORIES")
        dict_to_table(user, wcompletiond, "WCOMPLETION")
        dict_to_table(user, wrelationshipsd, "WRELATIONSHIPS")
        dict_to_table(user, wcharactersd, "WCHARACTERS")
        dict_to_table(user, wtagsd, "WTAGS")
        dict_to_table(user, wlanguagesd, "WLANGUAGES")
        list_to_table(user, wwords, "WWORDS")
        list_to_table(user, wcollections, "WCOLLECTIONS")
        list_to_table(user, wcomments, "WCOMMENTS")
        list_to_table(user, wkudos, "WKUDOS")
        list_to_table(user, wbookmarks, "WBOOKMARKS")
        list_to_table(user, whits, "WHITS")
        list_to_table(user, wdatesp, "WDATESP")

        urlb = "https://archiveofourown.org/users/" + user + "/bookmarks"                                  # change bookmarks link back to first page
        session["urlb"] = urlb
        urlw = "https://archiveofourown.org/users/" + user + "/works"                                      # change works link back to first page
        session["urlw"] = urlw
        session["access"] = "true"                                                                         # confirm the session is active
        return render_template('dash.html', user = user, url = url, urlb = urlb, urlw = urlw, icon = icon, years = years_active)

# renders bookmark information page for given username
@app.route('/bookmarks/')
def bookmark_page():

    if "access" not in session:                                             # check if a username has been entered
        failure = True
        return render_template('index.html',  failure = failure)            # if not return to index

    user = session["user"]

    btitles = table_to_list(user, "BTITLES")

    if len(btitles) == 0:
        empty = True
    else:
        empty = False

    if empty is False:
        btagsd = table_to_dict(user, "BTAGS")
        bcharactersd = table_to_dict(user, "BCHARACTERS")
        brelationshipsd = table_to_dict(user, "BRELATIONSHIPS")
        bcategoriesd = table_to_dict(user, "BCATEGORIES")
        bfandomsd = table_to_dict(user, "BFANDOMS")
        bratingsd = table_to_dict(user, "BRATINGS")

        # generates word clouds:
        clouds = []
        tagcloud = wordcloud_from_dict(btagsd)
        clouds.append(tagcloud)

        charactercloud = wordcloud_from_dict(bcharactersd)
        clouds.append(charactercloud)

        relationshipcloud = wordcloud_from_dict(brelationshipsd)
        clouds.append(relationshipcloud)

        fandomcloud = wordcloud_from_dict(bfandomsd)
        clouds.append(fandomcloud)

        titles = ["Tag", "Character", "Relationship", "Fandom"]

        categorydata = {'Task' : 'Hours per Day'}
        categorydata.update(bcategoriesd)

        ratingdata = {'Task' : 'Hours per Day'}
        ratingdata.update(bratingsd)

    else:
        clouds = []
        titles = []
        btagsd = {}
        bcharactersd = {}
        brelationshipsd = {}
        categorydata = {}
        bfandomsd = {}
        ratingdata = {}

    return render_template('bookmarks.html', user = user, articles = clouds, titles = titles,
    tags = btagsd, characters = bcharactersd, relationships = brelationshipsd,
    fandoms = bfandomsd, categorydata=categorydata, ratingdata = ratingdata, empty = empty)

# renders works information page for given username
@app.route('/works/')
def work_page():

    if "access" not in session:                       # check if a username has been entered
        failure = True
        return render_template('index.html',  failure = failure)    # if not return to index

    user = session["user"]

    wtitles = table_to_list(user, "WTITLES")

    if len(wtitles) == 0:
        empty = True
    else:
        empty = False

    if empty == False:
        wtagsd = table_to_dict(user, "WTAGS")
        wcharactersd = table_to_dict(user, "WCHARACTERS")
        wrelationshipsd = table_to_dict(user, "WRELATIONSHIPS")
        wcategoriesd = table_to_dict(user, "WCATEGORIES")
        wfandomsd = table_to_dict(user, "WFANDOMS")
        wratingsd = table_to_dict(user, "WRATINGS")

        # generates word clouds:
        clouds = []
        tagcloud = wordcloud_from_dict(wtagsd)
        clouds.append(tagcloud)

        charactercloud = wordcloud_from_dict(wcharactersd)
        clouds.append(charactercloud)

        relationshipcloud = wordcloud_from_dict(wrelationshipsd)
        clouds.append(relationshipcloud)

        fandomcloud = wordcloud_from_dict(wfandomsd)
        clouds.append(fandomcloud)

        titles = ["Tag", "Character", "Relationship", "Fandom"]

        categorydata = {'Task' : 'Hours per Day'}
        categorydata.update(wcategoriesd)

        ratingdata = {'Task' : 'Hours per Day'}
        ratingdata.update(wratingsd)

    else:
        clouds = []
        titles = []
        wtagsd = {}
        wcharactersd = {}
        wrelationshipsd = {}
        categorydata = {}
        wfandomsd = {}
        ratingdata = {}

    return render_template('works.html', user = user, articles = clouds, titles = titles,
    tags = wtagsd, characters = wcharactersd, relationships = wrelationshipsd,
    fandoms = wfandomsd, categorydata=categorydata, ratingdata = ratingdata, empty = empty)

# renders contact information page
@app.route('/contact', methods=['GET', 'POST'])
def contact():

    if "access" not in session:                      # check if a username has been entered
        failure = True
        return render_template('index.html',  failure = failure)   # if not return to index

    form = ContactForm()
  
    if request.method == 'POST':
        if form.validate() is False:
            flash('All fields are required.')
            return render_template('contact.html', form=form)
        else:
            msg = Message(form.subject.data, sender='ronia@jerpeter.com', recipients=['ronia.peterson@gmail.com'])
            msg.body = "From: {0} &lt;{1}&gt;{2}".format(form.name.data, form.email.data, form.message.data)
            mail.send(msg)

            return render_template('contact.html', success=True)

    elif request.method == 'GET':
        return render_template('contact.html', form=form)

@app.route('/dash/')
def dashed():
    """ Renders dashboard after a username has already been entered """

    if "access" in session:
        user = session["user"]
        url = session["url"]
        urlb = session["urlb"]
        urlw = session["urlw"]
        icon = session["icon"]
        years_active = session["years"]
        return render_template('dash.html', user = user, url = url, urlb = urlb,
        urlw = urlw, icon = icon, years = years_active)
    else:
        failure = True                             # if user doesn't exist, return to index
        return render_template('index.html',  failure = failure)

@app.route('/achievements/')
def achievements():
    """ Renders achievements page """

    if "access" not in session:                      # check if a username has been entered
        failure = True
        return render_template('index.html',  failure = failure)   # if not return to index

    user = session["user"]
    total_achievements = 0

    # bookmarks-based achievements
    btitles = table_to_list(user, "BTITLES")

    if len(btitles) == 0:
        bookmarks_achievement = "No Bookmarks Yet"
    if len(btitles) >= 10:
        bookmarks_achievement = "Newbie"
        total_achievements += 1
    if len(btitles) >= 100:
        bookmarks_achievement = "Casual"
    if len(btitles) >= 250:
        bookmarks_achievement = "Curator"
    if len(btitles) >= 500:
        bookmarks_achievement = "Bookworm"
    if len(btitles) >= 1000:
        bookmarks_achievement = "Collector"
    if len(btitles) >= 5000:
        bookmarks_achievement = "Rereader Extraordinaire"
    if len(btitles) >= 10000:
        bookmarks_achievement = "Expert"

    # works-based achievements
    wtitles = table_to_list(user, "WTITLES")

    if len(wtitles) == 0:
        works_achievement = "No Works Yet"
    if len(wtitles) >= 1:
        works_achievement = "Not Just a Reader"
        total_achievements += 1
    if len(wtitles) >= 5:
        works_achievement = "Practice Makes Perfect"
    if len(wtitles) >= 20:
        works_achievement = "Hobbyist"
    if len(wtitles) >= 50:
        works_achievement = "No Beta, We Die Like Men"
    if len(wtitles) >= 100:
        works_achievement = "Author"
    if len(wtitles) >= 250:
        works_achievement = "Ao3 Celebrity"
    if len(wtitles) >= 500:
        works_achievement = "Basically a Second Job"
    if len(wtitles) >= 1000:
        works_achievement = "Legendary"

    # completionist achievement
    wcompletiond = table_to_dict(user, "WCOMPLETION")

    completionist = False
    if wcompletiond["Work in Progress"] + wcompletiond["Series in Progress"] == 0:
        if len(wtitles) >= 1:
            completionist = True
            total_achievements += 1

    # ratings-based achievements
    bratingsd = table_to_dict(user, "BRATINGS")
    wratingsd = table_to_dict(user, "WRATINGS")
    gen = bratingsd["General Audiences"] + wratingsd["General Audiences"]
    teen = bratingsd["Teen And Up Audiences"] + wratingsd["Teen And Up Audiences"]
    explicit = bratingsd["Explicit"] + wratingsd["Explicit"]
    mature = bratingsd["Mature"] + wratingsd["Mature"]
    notrated = bratingsd["Not Rated"] + wratingsd["Not Rated"]
    all_ratings = gen + teen + explicit + mature + notrated

    if all_ratings == 0:
        ratings_achievement = "None"
    elif explicit + mature == 0:
        ratings_achievement = "Puritan"
        total_achievements += 1
    elif (explicit + mature) / all_ratings <= 0.33:
        ratings_achievement = "Curious"
        total_achievements += 1
    elif (explicit + mature) / all_ratings <= 0.66:
        ratings_achievement = "Well Rounded"
        total_achievements += 1
    elif (explicit + mature) / all_ratings < 1:
        ratings_achievement = "Here for 'The Plot'"
        total_achievements += 1
    elif (explicit + mature) / all_ratings == 1:
        ratings_achievement = "Pervert"
        total_achievements += 1

    return render_template('achievements.html', user = user, total = total_achievements,
    ratings = ratings_achievement, bookmarks = bookmarks_achievement,
    works = works_achievement, completionist = completionist)

@app.route('/everyachievement/')
def everyachievement():
    """ Renders everyachievement page """
    return render_template('everyachievement.html')

@app.route('/about/')
def about():
    """ Renders about page"""
    return render_template('about.html')

# app.run(host='localhost', port=5000)
