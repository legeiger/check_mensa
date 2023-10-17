## get json from mensa json


# write last check and meals inside "json" and get diff

# only notify if request did not fail and stuff
# %%
from icalendar import Calendar, Event, vCalAddress, vText
from datetime import datetime
from pathlib import Path

import json
import requests
import smtplib


# %% email stuff
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header



# %% read in config file
with open('config.json') as f:
    config = json.load(f)

EMAIL = config['EMAIL']
PASSWORD = config['PASSWORD']
smtp_endpoint = config['SmtpEndPoint']
smtp_endpoint_port = config['SmtpEndPointPort']
organizer_address = config['organizer_address']
IntrestMeals = config['IntrestMeals']  # part of the meal that needs to be inside the meal string of the mensa json

JSON_URL = "https://sws.maxmanager.xyz/extern/mensa_stuttgart-vaihingen.json"
# FutureDays = 1 # days we add to instred dates # : int

# %%
def send_email(Subject, recipient, html_text, ical_file):
    # set up the SMTP server
    s = smtplib.SMTP_SSL(host=smtp_endpoint, port=smtp_endpoint_port)
    # s.starttls()
    s.login(EMAIL, PASSWORD)


    msg = MIMEMultipart()       # create a message
    # setup the parameters of the message
    msg['From'] = str(Header('Mensa Checker <leandergeiger@t-online.de>'))
    msg['To'] = recipient
    msg['Subject'] = "Mensa Speiseplan update {}".format(Subject)

    # add in the message body
    msg.attach(MIMEText(html_text, 'html'))

    # attach ical calender entry
    part = MIMEApplication(ical_file, Name="mensa.ics")
    # After the file is closed
    part['Content-Disposition'] = 'attachment; filename="mensa.ics"'
    msg.attach(part)

    # send the message via the server set up earlier.
    s.send_message(msg)

    # Terminate the SMTP session and close the connection
    s.quit()


# %%
def prepair_email(entries):
    #     html_text = df.to_html()
    #     send_email(Subject=IntrestDates[0], html_text=html_text)

    #print(entries)
    for entry in entries:
        ical = generate_ical(entry, entries[entry]['meal'])
        html_text = "<b>find calender entry attached</b>"
        print(ical, entries[entry]['recipient'])
        send_email(Subject=entries[entry]['meal'] + " am " + entry, recipient=entries[entry]['recipient'], html_text=html_text, ical_file=ical)
    return


def generate_ical(date, meal):
    format = "%Y-%m-%d-%H-%M"

    cal = Calendar()    
    event = Event()

    event.add('summary', meal + " in der Mensa Vaihingen.")
    event.add('dtstart', datetime.strptime(date + "-11-30", format))
    event.add('dtend', datetime.strptime(date + "-12-00", format))
    event.add('dtstamp',  datetime.strptime(date + "-11-30", format))
    event['location'] = vText('Mensa Stuttgart Vaihingen')

    organizer = vCalAddress(organizer_address)
    organizer.params['cn'] = vText('Leander Geiger')
    event['organizer'] = organizer

    # Adding events to calendar
    cal.add_component(event)
    ical = cal.to_ical()

    # with open("entry.ics", "wb") as file:
    #     file.write(ical)
    return ical


# %%
def check_for_new_meals():
    session = requests.session()
    response = session.get(JSON_URL)

    #print(response.text)
    print(response.status_code)
    data = response.json()

    # %%
    with open("response.json", "w") as file:
        json.dump(data, file, indent=4)#, sort_keys=True)

    #print(data)
    # %%
    # check for entries where class name is not blocked or blocked-0 so we can find available appointments in json
    entries = {}
    # %%
    for dates in data['Mensa Stuttgart-Vaihingen']:
        for day in data['Mensa Stuttgart-Vaihingen'][dates]:
            #print(dates, day['meal'])
            for Meals, recipient in IntrestMeals.items():
                if Meals in day['meal']:
                    # found matching meal!
                    # collect all and create email with all dates
                    print("match!", dates, day['meal'], recipient)
                    entries.update({dates: {"recipient": recipient, "meal": day['meal']}})

    #print(entries)
    # %% load old entries
    with open('entries.json', 'r') as f:
        entries_lastrun = json.load(f)

    # compare diffs
    # %%
    if entries == entries_lastrun:
        print("no diff")
    else:
        print("diff! → send out emails")
        prepair_email(entries)
        # %% save current entries to json
        with open('entries.json', 'w', encoding='utf-8') as f:
            json.dump(entries, f, indent=4, sort_keys=True)

# %%
if __name__ == '__main__': # noqa
    check_for_new_meals()
    #pass