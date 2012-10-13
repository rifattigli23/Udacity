import cgi
def escape_html(s):
    return cgi.escape(s, quote = True)