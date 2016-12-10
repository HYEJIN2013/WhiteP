#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate emails for the London Analysis Seminar ML and saves them on GMail Drafts."""

# TODO: Implement send the mail to the mailing-list
#import smtplib

try:
  from colorama import Fore, init

  # pylint: disable=E1101, C0103
  print_red = lambda t: print(Fore.RED + t)
  print_green = lambda t: print(Fore.GREEN + t)
  print_yellow = lambda t: print(Fore.YELLOW + t)

  init(autoreset=True)
except ImportError:
  print("Colorama not present, reverting to b/w output")
  # pylint: disable=E1101, C0103
  print_red = print_green = print_yellow = print

from collections import namedtuple
# we need datetime.now
from datetime import datetime
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from markdown import markdown
from requests import get

import click
import imaplib
import json
import re
import time

URLS = {
  "las": "http://mathcal-mseri.rhcloud.com/json/las", 
  "kcl": "http://mathcal-mseri.rhcloud.com/json/gcal/gkij4q9m1249c2osijddav6dig%40group.calendar.google.com"
  }

NAMES = {
  "las": "London", 
  "kcl": "KCL"
  }

MORE = {
  "las": "Directions at http://www.london-analysis-seminar.org.uk",
  "kcl": "Additional informations can be found at the following url: https://www.kcl.ac.uk/nms/depts/mathematics/research/analysis/events/seminars.aspx"
  }

EMAIL = # add email here
PASSWORD = # add password here

Seminar = namedtuple("Seminar", "title location description start end")
Seminars = namedtuple("Seminars", "sid events")

def get_seminar_info(url):
  """Takes the _url_ to the scraping service and extract this week's 
  seminars out of it, returning _[Seminar]_. 
  If no seminar is present it returns _None_."""

  now = datetime.now()
  data = get(url)
  if data.status_code == 200:
    seminars = [Seminar(title=s_["title"], 
                        location=s_["location"], 
                        description=s_["description"],
                        start=parse(s_["start"]),
                        end=parse(s_["end"])
                       ) 
                for s_ in json.loads(data.content.decode("utf-8"))
                if less_than_a_week_from(now, parse(s_["start"]))
               ]
    if len(seminars) > 0:
      return seminars
  return None

def get_seminars_from_urls(urls):
  """Takes a dict('sid':'url') and returns an instance of _Seminars_
  containing events that will happen in the next 7 days. 
  If no seminar is planned, it returns _None_."""

  print("Processing seminars. This may take a while...", end=" ")
  
  for key, url in urls.items():
    seminars = get_seminar_info(url)
    if seminars:
      print_green("Seminars acquired!")
      return Seminars(sid=key, events=seminars)

  print_red("No suitable seminar found.")
  return None

def less_than_a_week_from(reference, event):
  """Takes two dates and tells if they are less than a week apart."""
  return 0 <= relativedelta(event, reference).days < 7 and relativedelta(event, reference).months == 0 and relativedelta(event, reference).years == 0

def gen_mail_body_with_seminar(seminars, notes):
  """Takes an instance of Seminars and returns a compiled email, ready to be
  sent to the analysis seminar mailing-list."""

  print("Generating email content...", end=" ")

  notes = notes or ""
  location_info = seminars.events[0].location
  place = location_info.split(",")[0].replace("London", "").strip()
  day = seminars.events[0].start.strftime("%A %d %B")
  start_time = seminars.events[0].start
  end_time = seminars.events[-1].end
  time_short = "{}-{}".format(start_time.strftime("%I"), end_time.strftime("%I:%M %p").lower())

  # Create message container - the correct MIME type is multipart/alternative.
  # Thanks http://stackoverflow.com/questions/882712/sending-html-email-using-python
  msg = MIMEMultipart('alternative')
  msg['Subject'] = "{} Analysis Seminar, {}, {}".format(NAMES[seminars.sid], day, place)
  msg['From'] = EMAIL
  # When I figure out how to get all adressee in the Analysis ML, 
  # I will implement the direct send method
  #msg['To'] = you

  seminars_text = "".join([format_seminar(seminar) for seminar in seminars.events])

  # Create the body of the message (a plain-text and an HTML version).
  text = """Dear All,
the next session of the London Analysis Seminar will be on **{day}, {start} at {place}. {notes}**
**{day}, {time_short}**, {location}:
{seminars}
{more}
With best regards,
Marcello
""".format(day=day, place=place, start=start_time.strftime("%I:%M %p").lower(), 
           time_short=time_short, location=location_info, seminars=seminars_text, 
           notes=notes, more=MORE[seminars.sid])
  html = markdown(text)

  # Record the MIME types of both parts - text/plain and text/html.
  part1 = MIMEText(text, 'plain')
  part2 = MIMEText(html, 'html')

  # Attach parts into message container.
  # According to RFC 2046, the last part of a multipart message, in this case
  # the HTML message, is best and preferred.
  msg.attach(part1)
  msg.attach(part2)

  print_green("e-mail generated!")
  return msg

def format_seminar(seminar):
  """Takes a Seminar and returns a markdown string with its description."""

  start_hour = seminar.start.strftime("%I:%M %p").lower()
  rex_aut = r"(.*)\((.*)\)\s?-?\s?(.*)"
  author, uni, title = re.match(rex_aut, seminar.title).groups()
  abstract = re.sub(r"\n", " ", seminar.description[9:]).strip()

  txt = """
- **{hour} {author}** ({uni}) _{title}_
    Abstract: _{abstract}_
""".format(hour=start_hour, author=author.strip(), uni=uni.strip(), 
           title=title.strip(), abstract=abstract)

  return txt

def save_draft_on_gmail(email):
  """Takes an email and saves it (via imap) in GMail Drafts folder.
  In a future version this could be replaced by an actual 'send_email_to_ml'."""

  print("Saving draft...", end=" ")
  # To use this one needs to enable the lesssecureapp settings
  # https://www.google.com/settings/security/lesssecureapps
  conn = imaplib.IMAP4_SSL("imap.gmail.com", port=993)
  conn.login(EMAIL, PASSWORD)
  conn.select("[Gmail]/Drafts")
  conn.append("[Gmail]/Drafts", r"Draft", time.time(), email.as_string().encode("utf-8"))
  conn.close()
  print_green("Draft successfully saved!")

@click.command()
@click.option("--seminar", default="any", type=click.Choice(["any", "las", "kcl"]))
@click.option("--notes", default=None)
def lasmailer(seminar, notes):
  """London Analysis Seminar Mailer. Relies on the London Maths Event calendar
  backend to obtain info on the upcoming analysis seminars, generate an email 
  body and send the email."""

  if seminar == "any":
    urls = URLS
  else:
    urls = {seminar: URLS[seminar]}

  seminars = get_seminars_from_urls(urls)

  if seminars:
    email = gen_mail_body_with_seminar(seminars, notes)
    save_draft_on_gmail(email)
  else:
    print_yellow("No seminar to advertise this week")

if __name__ == "__main__":
  # pylint: disable=E1120
  lasmailer()
