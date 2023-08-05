# -*- coding: utf-8 -*-
# Copyright 2015 John Reese
# Modifications copyright (C) 2022 Hai Liang W.
# Licensed under the MIT license

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import re
import sys

from markup.Module import Module
from markup.Transform import Transform

# language code for headline 1: c(zh_CN); e(en_US)
tocre = re.compile(r"^!TOC(\s+[1-6])?(\s+\w+)?\s*$")
atxre = re.compile(r"^(#+)\s*(.+)$")
setextre = re.compile(r"^(=+|-+)\s*$")
fencedcodere = re.compile(r"^```[ \w]*$")
linkre = re.compile(r"(\[(.*?)\][\(\[].*?[\)\]])")
cn_digits = dict({
    "1": "一",
    "2":"二",
    "3":"三",
    "4":"四",
    "5":"五",
    "6":"六",
    "7":"七",
    "8":"八",
    "9":"九",
    "10":"十",
    "11":"十一",
    "12":"十二",
    "13":"十三",
    "14":"十四",
    "15":"十五",
    "16":"十六",
    "17":"十七",
    "18":"十八",
    "19":"十九",
    "20":"二十",
    "21":"二十一",
    "22":"二十二",
    "23":"二十三"
})


class TableOfContents(Module):
    """
    Module for auto-generating a table of contents based on the Markdown
    headers in the document.  The table of contents is inserted in the document
    wherever a `!TOC` marker is found at the beginning of a line.
    """

    @staticmethod
    def clean_html_string(string):
        replacements = [
            ("&", "&amp;"),
            ("<", "&lt;"),
            (">", "&gt;"),
            ("\"", "&quot;"),
            ("'", "&#39;"),
        ]
        for to_replace, with_what in replacements:
            string = string.replace(to_replace, with_what)
        return string

    @staticmethod
    def clean_title(title):
        for link in re.findall(linkre, title):
            title = title.replace(link[0], link[1])
        return title


    def fix_section_with_lang(self, section, lang):
        if section.count(".") == 1 and lang == "cn":
            section = section.strip().replace(".", "").replace("\\", "").strip()

            if not section in cn_digits:
                print("Key not found in cn_digits: %s" % section)
                sys.exit(1)

            return "第"+ cn_digits[section] + "章、"
        else:
            return section
            

    def transform(self, data):
        transforms = []

        lowestdepth = 10

        tocfound = False
        toclines = []
        tocdepth = 0
        tocdata = ""
        toch1lang = "en"

        headers = {}

        infencedcodeblock = False

        # iterate through the document looking for markers and headers
        linenum = 0
        lastline = ''
        for line in data:

            striped = line.strip()
            '''
            Bypass page breaker
            https://pandoc.org/MANUAL.html#extension-raw_attribute
            ```{=openxml}
            <w:p>
            <w:r>
                <w:br w:type="page"/>
            </w:r>
            </w:p>
            ```
            '''
            if striped.startswith("```") or striped.startswith("<w:") or striped.startswith("</w:"):
                linenum = linenum + 1
                continue

            # Fenced code blocks (Github-flavored markdown)
            match = fencedcodere.search(line)
            if match:
                if infencedcodeblock:
                    infencedcodeblock = False
                else:
                    infencedcodeblock = True

            # !TOC markers
            match = tocre.search(line)
            if match:
                tocfound = True
                depth = match.group(1)
                if depth is not None:
                    depth = int(depth)
                    tocdepth = max(depth, tocdepth)
                toclines.append(linenum)

                h1lang = match.group(2)
                if h1lang is not None:
                    h1lang = h1lang.strip().lower()
                    print("h1lang %s" %  h1lang)
                    if h1lang in ["en", "cn"]:
                        toch1lang = h1lang
                    else:
                        print("Unexpected lang code for toc, avaiable code: en, cn")
                        sys.exit(1)

                # print("TOC langcode %s" % toch1lang)

            # hash headers
            match = atxre.search(line)
            if match and not infencedcodeblock:
                depth = len(match.group(1))
                title = match.group(2).strip()
                headers[linenum] = (depth, title)

                if tocfound:
                    lowestdepth = min(depth, lowestdepth)

            # underlined headers
            match = setextre.search(line)
            if match and not infencedcodeblock and lastline.strip():
                depth = 1 if match.group(1)[0] == "=" else 2
                title = lastline.strip()
                headers[linenum-1] = (depth, title)

                if tocfound:
                    lowestdepth = min(depth, lowestdepth)

            lastline = line
            linenum += 1

        # short circuit if no !TOC directive
        if not tocfound:
            return []

        if tocdepth == 0:
            tocdepth = 6

        stack = []
        headernum = 0

        lastdepth = 1
        depthoffset = 1 - lowestdepth

        keys = sorted(headers.keys())

        short_titles = []

        # interate through the list of headers, generating the nested table
        # of contents data, and creating the appropriate transforms
        for linenum in keys:
            if linenum < toclines[0]:
                continue

            (depth, title) = headers[linenum]
            depth += depthoffset
            short = re.sub(r"([\s,-,\(,\)]+)", "",
                           TableOfContents.clean_title(title)).lower()

            if short in short_titles:
                i = 1
                short_i = short
                while short_i in short_titles:
                    short_i = short + "-" + str(i)
                    i += 1
                short = short_i
            short_titles.append(short)

            while depth > lastdepth:
                stack.append(headernum)
                headernum = 0
                lastdepth += 1

            while depth < lastdepth:
                headernum = stack.pop()
                lastdepth -= 1

            headernum += 1

            if depth > tocdepth:
                continue

            if depth == 1:
                section = "%d\\. " % headernum
            else:
                section = (".".join([str(x) for x in stack]) +
                           ".%d\\. " % headernum)

            short = TableOfContents.clean_html_string(short)
            title = TableOfContents.clean_html_string(title).strip()

            tocdata += ("%s [%s](#%s)  \n" %
                        (self.fix_section_with_lang(section, h1lang), TableOfContents.clean_title(title), short))

            transforms.append(Transform(linenum, "swap",
                              data[linenum].replace(title, self.fix_section_with_lang(section, h1lang) + title)))
            transforms.append(Transform(linenum, "prepend",
                              "<a name=\"%s\"></a>\n\n" % short))

        # create transforms for the !TOC markers
        for linenum in toclines:
            transforms.append(Transform(linenum, "swap", tocdata))

        return transforms
