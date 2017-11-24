import time
import traceback
import codecs
import datetime

from dateutil import parser


class Press(object):
    def __init__(self, title, url, venue, date):
        self.title = title
        self.url = url
        self.venue = venue
        self.date = date
        self.date_str = date.strftime("%B %d, %Y")

        # XXX: hardcoded :/
        self.type = 'news'

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        s = u'- Press: [%s](%s) by **%s** on %s' % (self.title, self.url, self.venue, self.date_str)
        return s.encode('utf-8')


def _read_events_from_csv(filename):
    press_items = []
    with codecs.open(filename, 'r', encoding='utf-8') as infile:
        for line in reversed(infile.readlines()):
            try:
                comps = line.split(';')
                url = comps[0].strip('"')
                venue = comps[1].strip('"')
                date = parser.parse(comps[2]).date()
                title = comps[3].strip().strip('"')
                press_items.append(Press(title, url, venue, date))
            except Exception as e:
                print 'Error in processing %s...' % line[:100]
                traceback.print_exc()

    return sorted(press_items, key=lambda x: x.date, reverse=True)


def get_all_press():
    return _read_events_from_csv('content/press/pressroll-all.csv')


def get_featured_press(expire_in_days):
    """
    :return: a list of press items with a 'featured' tag
    """
    press_featured = _read_events_from_csv('content/press/pressroll-featured.csv')

    today = datetime.date.today()

    def not_expired(item):
        delta = today - item.date
        return delta.days <= expire_in_days

    press_featured = filter(not_expired, press_featured)
    return sorted(press_featured, key=lambda x: x.date, reverse=True)
