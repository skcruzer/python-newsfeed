# update format of date
def format_date(date):
  return date.strftime('%m/%d/%y')

from datetime import datetime
print(format_date(datetime.now()))


# update format of url using replace() and split()
def format_url(url):
  return url.replace('http://', '').replace('https://', '').replace('www.', '').split('/')[0].split('?')[0]


# correctly pluralize words
def format_plural(amount, word):
  if amount != 1:
    return word + 's'

  return word