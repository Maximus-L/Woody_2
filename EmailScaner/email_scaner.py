# -*- coding: utf-8 -*-

import email, imaplib, os
import Lib
from BotWoody import EMAIL_LOGIN
from BotWoody import EMAIL_PASSWORD

log: Lib.AppLogger = Lib.AppLogger(__name__,
                                   output='BOTH',
                                   log_file='./LOGS/email.log',
                                   log_level=Lib.ERROR)


def email_scan(criteria='UNSEEN', file_path='./TEMP'):
    try:
        imap = imaplib.IMAP4_SSL("imap.gmail.com")
    except Exception as e:
        log.error(f'gmail не открывается: {e}')
        return None

    with imap:
        imap.login(EMAIL_LOGIN, EMAIL_PASSWORD)
        # фильтр IMAP правила:(check http://www.example-code.com/csharp/imap-search-critera.asp)
        resp, items = imap.search(None, criteria)
        items = items[0].split()  # getting the mails id
        for emailid in items:
            resp, data = imap.fetch(emailid, "(RFC822)") # fetching the mail, "`(RFC822)`" means "get the whole stuff", but you can ask for headers only, etc
            email_body = data[0][1]  # getting the mail content
            # не сработало:
            # mail = email.message_from_string(email_body) # parsing the mail content to get a mail object
            # вот так сработало:
            mail = email.message_from_bytes(email_body)
            # Check if any attachments at all
            if mail.get_content_maintype() != 'multipart':
                continue
            # we use walk to create a generator so we can iterate on the parts and forget about the recursive headach
            for part in mail.walk():
                # проверка типа контейнера
                if part.get_content_maintype() == 'multipart':
                    continue
                # is this part an attachment ?
                if part.get('Content-Disposition') is None:
                    continue
                filename = part.get_filename()
                # если имя файла определено
                if filename:
                    att_path = os.path.join(file_path, filename)
                    # если такого файла нет
                    if not os.path.isfile(att_path):
                        # запись файла
                        fp = open(att_path, 'wb')
                        fp.write(part.get_payload(decode=True))
                        fp.close()




# Here are examples of different search criteria:
#
# Return all messages. "ALL"
#
# Search for already-answered emails. "ANSWERED"
#
# Search for messages on a specific date.
# The date string is DD-Month-YYYY where Month is
# Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, or Dec.
# "SENTON 05-Mar-2007"
#
# Search for messages between two dates.  SENTBEFORE
# finds emails sent before a date, and SENTSINCE finds
# email sent on or after a date.  The "AND" operation
# is implied by joining criteria, separated by spaces.
# "SENTSINCE 01-Mar-2007 SENTBEFORE 05-Mar-2007"
#
# Another example of AND: find all unanswered emails
# sent after 04-Mar-2007 with "Problem" in the subject:
# "UNANSWERED SENTSINCE 04-Mar-2007 Subject \"Problem\""
#
# Find messages with a specific string in the body:
# "BODY \"problem solved\""
#
# Using OR.  The syntax is OR <criteria1> <criteria2>.
# The "OR" comes first, followed by each criteria.
# For example, to match all emails with "Help" or "Question" in the subject.
# You'll notice that literal strings may be quoted or unquoted.
# If a literal contains SPACE characters, quote it:
# "OR SUBJECT Help SUBJECT Question";
#
# ----------------------------------------------
# Strings are case-insensitive when searching....
# ----------------------------------------------
#
# Find all emails sent from yahoo.com addresses:
# "FROM yahoo.com";
# Find all emails sent from anyone with "John" in their name:
# "FROM John"
#
# Find emails with the RECENT flag set:
# "RECENT"
#
# Find emails that don't have the recent flag set:
# "NOT RECENT"
# This is synonymous with "OLD":
# "OLD"
#
# Find all emails marked for deletion:
# "DELETED"
#
# Find all emails having a specified header field with a value
# containing a substring:
# "HEADER DomainKey-Signature paypal.com";
#
# Find any emails having a specific header field.  If the
# 2nd argument to the "HEADER" criteria is an empty string,
# any email having the header field is returned regardless
# of the header field's content.
# Find any emails with a DomainKey-Signature field:
# "HEADER DomainKey-Signature \"\"";
#
# Find NEW emails: these are emails that have the RECENT flag
# set, but not the SEEN flag:
# "NEW";
#
# Find emails larger than a certain number of bytes:
# "LARGER 500000";
#
# Find emails marked as seen or not already seen:
# "SEEN"
# "NOT SEEN"
#
# Find emails having a given substring in the TO header field:
# "TO support@chilkatsoft.com"
# A more long-winded way to do the same thing:
# "HEADER TO support@chilkatsoft.com"
#
# Find emails smaller than a size in bytes:
# "SMALLER 30000"
#
# Find emails that have a substring anywhere in the header
# or body:
# "TEXT \"Zip Component\"";
