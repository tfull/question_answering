import re
import Property

RE_COMMENT    = re.compile(r"<!--.*?-->", re.DOTALL)
RE_NOWIKI     = re.compile(r"<nowiki>.*?</nowiki>", re.DOTALL)
RE_BRACKET    = re.compile(r"\{[^\{]*?\}")
RE_REF_SINGLE = re.compile(r"<ref[^>]*/>")
RE_REF_PAIR   = re.compile(r"<ref[^>]*>.*?</ref>", re.DOTALL)
RE_MATH       = re.compile(r"<math>.*?</math>", re.DOTALL)
RE_CODE       = re.compile(r"<code>.*?</code>", re.DOTALL)
RE_PRIME      = re.compile(r"\'{2,}")
RE_DIV        = re.compile(r"<div(?: .*?)?>(.*?)</div>")
RE_SPAN       = re.compile(r"<span(?: .*?)?>(.*?)</span>")
RE_SUB        = re.compile(r"<sub>(.*?)</sub>")
RE_SUP        = re.compile(r"<sup>(.*?)</sup>")
RE_TAG        = re.compile(r"<([a-z]+)(?: .*?)?>.*?</\1>")
RE_LINK_I     = re.compile(r"\[\[[^\[]*?\]\]")
RE_LINK_S     = re.compile(r"\[\[(.*?)\|(.*?)\]\]")
RE_SQ         = re.compile(r"\[[^\[]*?\]")

NAMESPACES = [ "Media", "Special", "Talk", "User", "User talk", "Wikipedia",
    "Wikipedia talk", "File", "File talk", "MediaWiki", "MediaWiki talk",
    "Template", "Template talk", "Help", "Help talk", "Category", "Category talk",
    "Portal", "Portal talk", "Book", "Book talk", "Draft", "Draft talk",
    "Education Program", "Education Program talk", "TimedText", "TimedText talk",
    "Module", "Module talk", "Image" ]

def get_plain_text(text):
    text = re.sub(RE_COMMENT, "", text)
    text = re.sub(RE_NOWIKI, "", text)
    for i in range(5):
        text = re.sub(RE_BRACKET, "", text)
    text = re.sub(RE_REF_SINGLE, "", text)
    text = re.sub(RE_REF_PAIR, "", text)
    text = re.sub(RE_MATH, "", text)
    text = re.sub(RE_CODE, "", text)
    text = re.sub(RE_PRIME, "", text)

    while True:
        match = re.search(RE_TAG, text)
        if match is None:
            break
        m = re.match(RE_DIV, match.group())
        if m:
            text = text[:match.start()] + m.group(1) + text[match.end():]
            continue
        m = re.match(RE_SPAN, match.group())
        if m:
            text = text[:match.start()] + m.group(1) + text[match.end():]
            continue
        m = re.match(RE_SUB, match.group()) or re.match(RE_SUP, match.group())
        if m:
            text = text[:match.start()] + m.group(1) + text[match.end():]
            continue
        text = text[:match.start()] + match.group(1) +  text[match.end():]

    while True:
        match = re.search(RE_LINK_I, text)
        if match is None:
            break
        inlink = re.match(RE_LINK_S, match.group())
        surface = None
        link = None
        if inlink is not None:
            surface = inlink.group(2)
            link = inlink.group(1)
        else:
            surface = match.group()[2:-2]
            link = surface
        flag = True
        if link[:9] == "Category:":
            flag = False
        else:
            for ns in Property.get("extra_titles"):
                if link[:len(ns) + 1] == ns + ":":
                    flag = False
        if flag:
            text = text[:match.start()] + surface + text[match.end():]
        else:
            text = text[:match.start()] + text[match.end():]

    while True:
        match = re.search(RE_SQ, text)
        if match is None:
            break
        text = text[:match.start()] + text[match.end():]

    return text

def get_sentences(text):
    RE_NL = re.compile(r"\s+")
    text = get_plain_text(text)
    text = re.sub(RE_NL, "", text)
    return text
