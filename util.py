import datetime

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except:
        return False

def unix_time(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()

def normalize_text(text):
	return text.lower()