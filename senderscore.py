#!/usr/bin/python
#
# Here is a plugin I get on munin-monitoring and port this to nagios 
# I change some things to work on nagios 
# The oficial file of this plugin is here : https://github.com/munin-monitoring/contrib/blob/master/plugins/senderscore/senderscore


import socket
import sys
import os

def get_senderscores(ip):
    tmp = ip.split(".")
    backwards = "%s.%s.%s.%s" % (tmp[3], tmp[2], tmp[1], tmp[0])
    # replists = ['cmplt.rating.senderscore.com', 'score.senderscore.com', 'uus.rating.senderscore.com', 'vol.rating.senderscore.com', 'filtered.rating.senderscore.com']
    replists = ['score.senderscore.com']
    lookup_results = {}
    for rl in replists:
            try:
                    host = '%s.%s' % (backwards, rl)
                    ret = socket.gethostbyname(host)
                    if ret:
                            lookup_results[rl] = ret
            except Exception, e:
                    print >> sys.stderr,e
                    # sys.exit(1)
    scores = {}
    for k in lookup_results.keys():
        v = lookup_results[k].split('.')[3]
        k = k.split(".")[0]
        scores[k] = v
    return scores

def print_stats(ip):
    scores = get_senderscores(ip)
    for key in scores.keys():
        print key+".value "  +scores[key]

def print_config():
    print """
graph_title senderscore reputation
graph_info This graph shows senderscore.org reputation metrics
graphs_args --upper-limit 100 -u 100 -l 0
graph_category senderscore
graph_vlabel score
graph_scale no

score.label sender score
score.info score represents the overall health of your email programs as they appear to receiving systems.
score.warning 95:
score.critical 90:
"""

unused = """cmplt.label complaints
cmplt.infocomplaint scores are a rank based on your complaint rates.
cmplt.warning 95
cmplt.critical 90

uus.label unknown users
uus.info ratio of unknown users, or invalid email addresses, compared to the amount of email seen by our receiving sources

vol.label volume
vol.info rank of ip address by volume of email monitored

filtered.label filtered
filtered.info how often messages are rejected (bounced due to some policy reason, usually spam filtering or blacklisting) compared to other IP addresses seen in the Sender Score Reputation Network
filtered.warning 95
filtered.critical 90
"""

if __name__ == "__main__":
     
    ip = '184.107.179.50'
    print_stats(ip)

