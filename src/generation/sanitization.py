import re
import html


def unescape_html(text):
    """
    https://stackoverflow.com/questions/2360598/how-do-i-unescape-html-entities-in-a-texting-in-python-3-1
    """
    return html.unescape(text)


def remove_special_characters(text):
    """
    https://en.wikipedia.org/wiki/Specials_(Unicode_block)
    """
    return re.sub(r'[\uFFF0-\uFFFF]', "", text)


def remove_html_xml_tags(text):
    """
    This function should always be called after unescape_html(),
    so the valid HTML tags can be unescaped into plain text first before being removed
    """
    return re.sub('<[^<]+>', "", text)


def remove_urls(text):
    """
    https://stackoverflow.com/questions/24399820/expression-to-remove-url-links-from-twitter-tweet
    """
    return re.sub(r"http\S+", "", text)


def convert_and_remove_punctuation(text):
    """
    remove punctuation that are not allowed, e.g. / \
    convert Chinese punctuation into English punctuation, e.g.  from「 to "
    """
    # removal
    text = text.replace("\\", "")
    text = text.replace("\\", "")
    text = text.replace("[", "")
    text = text.replace("]", "")
    text = text.replace("【", "")
    text = text.replace("】", "")
    text = text.replace("{", "")
    text = text.replace("}", "")
    # conversion
    text = text.replace(u"\u201C", "\"")
    text = text.replace(u"\u201D", "\"")
    text = text.replace(u"\u2018", "'")
    text = text.replace(u"\u2019", "'")
    text = text.replace("「", "\"")
    text = text.replace("」", "\"")
    text = text.replace("『", "\"")
    text = text.replace("』", "\"")
    text = text.replace("quot;", "\"")
    return text


def remove_nonchinese_characters(text):
    """
    https://blog.csdn.net/bailixuance/article/details/89555580
    https://zhidao.baidu.com/question/439748031.html
    """
    return re.sub(r'[^\u4e00-\u9fa5\u0000-\u007F\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b]', "", text)


def remove_discord_emojis(text):
    return re.sub(r'<:\w*:\d*>', "", text)
