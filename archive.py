
"""


OLD CODE ARCHIVE JUST IN CASE!!





# Create Database:

conn = sqlite3.connect('database.db')                                           # open database

# create tables
conn.execute('CREATE TABLE BLINKS (username TEXT, col1 TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE BTITLES (username TEXT, col1 TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE BAUTHORS (username TEXT, col1 TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE BGIFTEES (username TEXT, col1 TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE BFANDOMS (username TEXT, col1 TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE BRATINGS (username TEXT, col1 TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE BWARNINGS (username TEXT, col1 TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE BCATEGORIES (username TEXT, col1 TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE BCOMPLETION (username TEXT, col1 TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE BRELATIONSHIPS (username TEXT, col1 TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE BCHARACTERS (username TEXT, col1 TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE BTAGS (username TEXT, col1 TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE BLANGUAGES (username TEXT, col1 TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE BWORDS (username TEXT, col1 TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE BCOLLECTIONS (username TEXT, col1 TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE BCOMMENTS (username TEXT, col1 TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE BKUDOS (username TEXT, col1 TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE BBOOKMARKS (username TEXT, col1 TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE BHITS (username TEXT, col1 TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE BDATESP (username TEXT, col1 TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE BDATESBM (username TEXT, col1 TEXT, UNIQUE(username))')

conn.close










# renders bookmark information page for given username
@app.route('/bookmarks/')
def bookmark_page():
    user = session["user"]
    urlb = session["urlb"]

    # initialize bookmarks data storage:
    blinks = []
    btitles = []
    bauthors = []
    bgiftees = []
    bfandoms = []
    bratings = []
    bratingsd = {
        "General Audiences": 0,
        "Teen And Up Audiences": 0,
        "Explicit": 0,
        "Mature": 0,
        "Not Rated": 0
    }
    bwarnings = []
    bwarningsd = {
        "No Archive Warnings Apply": 0,
        "Choose Not To Use Archive Warnings": 0,
        "Major Character Death": 0,
        "Graphic Depictions Of Violence": 0,
        "Rape/Non-Con": 0,
        "Underage": 0
    }
    bcategories = []
    bcategoriesd = {
        "F/M": 0,
        "F/F": 0,
        "M/M": 0,
        "Gen": 0,
        "Multi": 0,
        "Other": 0,
        "No category": 0
    }
    bcompletion = []
    bcompletiond = {
        "Complete Work": 0,
        "Work in Progress": 0,
        "Series in Progress": 0,
        "Complete Series": 0
    }
    brelationships = []
    brelationshipsd = {}
    bcharacters = []
    bcharactersd = {}
    btags = []
    btagsd = {}
    blanguages = []
    blanguagesd = {}
    bwords = []
    bcollections = []
    bcomments = []
    bkudos = []
    bbookmarks = []
    bhits = []
    bdatesp = []
    bdatesbm = []

    bookmarks = requests.get(urlb)                                                 # get bookmarks url contents
    bsoup = BeautifulSoup(bookmarks.text, "html.parser")                           # formats bookmarks results

    fanfics = bsoup.find_all('li', role="article")                                 # stores individual fanfic data
    pages = bsoup.find('ol', class_="pagination actions").find_all('li') \
        if bsoup.find('ol', class_="pagination actions") else [0,0]                # stores page navigation data

    count = 1

    while count < len(pages):
        for fic in fanfics:                                                        # loop through every fic on the page
            if fic.find('p', text = "This has been deleted, sorry!") == None:      # make sure fic hasn't been deleted
                link = fic.div.h4.a['href']                                        # get work link
                blinks.append(link)                                                # add work link to list

                title = fic.div.h4.a.text                                          # get fanfic title
                btitles.append(title)                                              # add fanfic title to list

                author = fic.div.h4.find_all('a', rel="author") \
                    if fic.div.h4.find('a', rel="author") else 'Anonymous'         # get author name(s)
                if author != 'Anonymous':
                    if len(author) > 1:                                            # if there's more than one author...
                        temp_list = []
                        for a in author:
                            temp_list.append(a.text)                               # add author names to temp list so they stay together
                        bauthors.append(temp_list)                                 # then put that whole list into the authors list
                    else:
                        for a in author:
                            bauthors.append(a.text)                                # otherwise just add the single author
                else:
                    bauthors.append(author)                                        # if there's no author, add "Anonymous" to the authors list

                giftee = fic.div.h4.find_all('a', href=re.compile("/gifts")) \
                    if fic.div.h4.find('a', href=re.compile("/gifts")) else 'None'     # get giftee name
                if giftee != 'None':
                    if len(giftee) > 1:                                            # if there's more than one giftee...
                        temp_list = []
                        for g in giftee:
                            temp_list.append(g.text)                               # add giftee names to temp list so they stay together
                        bgiftees.append(temp_list)                                 # then put that whole list into the giftees list
                    else:
                        for g in giftee:
                            bgiftees.append(g.text)                                # otherwise just add the single giftee
                else:
                    bgiftees.append(giftee)                                        # if there's no giftee, add "None" to the giftees list

                fandoms = fic.div.h5.find_all('a')                                 # get list of fandoms
                if len(fandoms) > 1:                                                  
                    temp_list = []
                    for f in fandoms:
                        temp_list.append(f.text)                                   # add fandoms to temp list so they stay together
                    bfandoms.append(temp_list)                                     # then put that whole list into the relationship list
                else: 
                    for f in fandoms:
                        bfandoms.append(f.text)                                    # or just add the single fandom right into the fandom list

                ratings = fic.div.ul.find('span', class_=re.compile("rating")).text.split(", ")        # get list of ratings
                for r in ratings:                                                                      # add each rating to dictionary count
                    bratingsd[r] += 1
                if len(ratings) > 1:
                    bratings.append(ratings)                                                           # add list of ratings to list
                else:
                    bratings.extend(ratings)                                                           # or add single rating to list

                warnings = fic.div.ul.find('span', class_=re.compile("warnings")).text.split(", ")     # get list of warnings
                for w in warnings:                                                                     # add each warning to dictionary count
                    bwarningsd[w] += 1
                if len(warnings) > 1:
                    bwarnings.append(warnings)                                                         # add list of warnings to list
                else:
                    bwarnings.extend(warnings)                                                         # or add single warning to list

                categories = fic.div.ul.find('span', class_=re.compile("category")).text.split(", ")   # get list categories
                for c in categories:                                                                   # add each category to dictionary count
                    bcategoriesd[c] += 1
                if len(categories) > 1:
                    bcategories.append(categories)                                                     # add list of categories to list
                else:
                    bcategories.extend(categories)                                                     # or add single category to list

                completion = fic.div.ul.find('span', class_=re.compile("iswip")).text.split(", ")      # get list of statuses
                for c in completion:                                                                   # add completion statuses to dictionary count
                    bcompletiond[c] += 1
                if len(completion) > 1:
                    bcompletion.append(completion)                                                     # add list of completion statuses to list
                else:
                    bcompletion.extend(completion)                                                     # or add single completion status to list

                relationships = fic.find_all('li', class_='relationships')                             # get list of relationships
                temp_list = []
                for r in relationships:
                    ship = r.text
                    if ship in brelationshipsd:                                                        # increase that relationship's count
                        brelationshipsd[ship] += 1
                    else:                                                                              # or add relationship to dictionary
                        brelationshipsd[ship] = 1
                    temp_list.append(ship)                                                             # add relationships to temp list so they stay together
                brelationships.append(temp_list)                                                       # then put that whole list into the relationship list

                characters = fic.find_all('li', class_='characters')                                   # get list of characters
                temp_list = []
                for c in characters:
                    character = c.text
                    if character in bcharactersd:                                                      # increase that character's count
                        bcharactersd[character] += 1
                    else:                                                                              # or add character to dictionary
                        bcharactersd[character] = 1
                    temp_list.append(character)                                                        # add characters to temp list so they stay together
                bcharacters.append(temp_list)                                                          # then put that whole list into the character list

                tags = fic.find_all('li', class_='freeforms')                                          # get list of tags
                temp_list = []
                for t in tags:
                    tag = t.text
                    if tag in btagsd:                                                                  # increase that tag's count
                        btagsd[tag] += 1
                    else:                                                                              # or add tag to dictionary
                        btagsd[tag] = 1
                    temp_list.append(tag)                                                              # add tags to temp list so they stay together
                btags.append(temp_list)                                                                # then put that whole list into the tag list

                languages = fic.find_all('dd', class_="language")                                      # get list of languages
                temp_list = []
                for l in languages:
                    language = l.text
                    if language in blanguagesd:                                                        # increase that language's count
                        blanguagesd[language] += 1
                    else:                                                                              # or add language to dictionary
                        blanguagesd[language] = 1
                    temp_list.append(language)
                blanguages.append(temp_list)

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
        urlb = "https://archiveofourown.org/users/" + user + "/bookmarks" + "?page=" + str(count)      # url of user's next bookmarks page
        bookmarks = requests.get(urlb)                                                                 # get next bookmarks page contents
        bsoup = BeautifulSoup(bookmarks.text, "html.parser")                                           # formats bookmarks results
        fanfics = bsoup.find_all('li', role="article")                                                 # stores individual fanfic data

    # generates word cloud of tags in bookmarked works:
    clouds = []
    wc=WordCloud(width=800, height=400, background_color='white', colormap="gist_heat", stopwords=STOPWORDS).generate_from_frequencies(btagsd).to_image()
    img = io.BytesIO()
    wc.save(img, "PNG")
    img.seek(0)
    img_b64 = base64.b64encode(img.getvalue()).decode()
    clouds.append(img_b64)

    return render_template('bookmarks.html', blinks = blinks, btitles = btitles, bauthors = bauthors, bgiftees = bgiftees, bfandoms = bfandoms, 
    bratings = bratings, bratingsd = bratingsd, bwarnings = bwarnings, bwarningsd = bwarningsd, bcategories = bcategories, bcategoriesd = bcategoriesd,
    bcompletion = bcompletion, bcompletiond = bcompletiond, brelationships = brelationships, brelationshipsd = brelationshipsd, bcharacters = bcharacters,
    bcharactersd = bcharactersd, btags = btags, btagsd = btagsd, blanguages = blanguages, blanguagesd = blanguagesd, bwords = bwords, bkudos = bkudos, 
    bbookmarks = bbookmarks, bhits = bhits, bdatesp = bdatesp, bdatesbm = bdatesbm, user = user, articles = clouds)














conn = sqlite3.connect("database.db")
c = conn.cursor()

#BLINKS

c.execute("INSERT OR IGNORE INTO BLINKS (username) VALUES (:name)", {'name': user})

count = 1                                                                                                                       # counter for loops
column_title = 'col1'

c.execute("SELECT COUNT(*) FROM pragma_table_info('BLINKS')")
blinks_colcount = c.fetchone()

for i in blinks:
    c.execute("UPDATE BLINKS SET {} = :new_value WHERE username=:user".format(column_title), {'new_value': i, 'user': user})    # put link in table
    if count != len(blinks):                                                                                                    
        count += 1
        column_title = 'col' + str(count)
        if count >= blinks_colcount[0]:
            c.execute("ALTER TABLE BLINKS ADD COLUMN {} TEXT".format(column_title))                                             # add new column to table

#BTITLES

c.execute("INSERT OR IGNORE INTO BTITLES (username) VALUES (:name)", {'name': user})

count = 1
column_title = 'col1'

c.execute("SELECT COUNT(*) FROM pragma_table_info('BTITLES')")
btitles_colcount = c.fetchone()

for i in btitles:
    c.execute("UPDATE BTITLES SET {} = :new_value WHERE username=:user".format(column_title), {'new_value': i, 'user': user})
    if count != len(btitles):                                                                                                    
        count += 1
        column_title = 'col' + str(count)
        if count >= btitles_colcount[0]:
            c.execute("ALTER TABLE BTITLES ADD COLUMN {} TEXT".format(column_title))

conn.commit()
conn.close()



"""