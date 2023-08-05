# Markup-Markdown

<!-- Readme is updated with `markup README.m.md -o README.md`, modify README.m.md in first place. -->

Stack up markdown files with `include` directives.

Previous, Markdown Preprocessor ([MarkdownPP](https://github.com/jreese/markdown-pp)).

**NOTICE: MarkdownPP is no longer actively maintained. MarkdownPP will not receive any future releases.**

The Markup-Markdown is a Python module designed to add extended features
on top of the excellent Markdown syntax defined by John Gruber. These additions
are mainly focused on creating larger technical documents without needing to use
something as heavy and syntactically complex as Docbook.

MarkdownPP uses a set of selectable modules to apply a series of transforms to
the original document, with the end goal of generating a new Markdown document
that contains sections or features that would be laborious to generate or
maintain by hand.

Documents designed to be preprocessed by Markup-Markdown should try to follow the
convention of naming files with a .m.md extension(m.md is Markup Markdown for short, ".md" as end so we can leverage Editor's highlight), so that Markup-Markdown can
generate a document with the same name, but with the standard .md extension.
As an example, this document in raw format is named "readme.m.md", and the
generated document from Markup-Markdown is named "readme.md" so that GitHub can find
and process that document when viewing the repository.

[![Build Status](https://travis-ci.org/jreese/markdown-pp.svg?branch=master)](https://travis-ci.org/jreese/markdown-pp)

0.1\.  [Installation and Usage](#installationandusage)  
0.2\.  [Modules](#modules)  
0.2.1\.  [Includes](#includes)  
0.2.2\.  [IncludeURLs](#includeurls)  
0.2.3\.  [IncludeCode](#includecode)  
0.2.4\.  [Table of Contents](#tableofcontents)  
0.2.5\.  [Reference](#reference)  
0.2.6\.  [LaTeX Rendering](#latexrendering)  
0.2.7\.  [YouTube Embeds](#youtubeembeds)  
0.3\.  [Examples](#examples)  
1\.  [Document Title](#documenttitle)  
1.1\.  [Header 1](#header1)  
1.1.1\.  [Header 1.a](#header1.a)  
1.2\.  [Header 2](#header2)  
2\.  [Document Title](#documenttitle-1)  
2.1\.  [Header 1](#header1-1)  
2.1.1\.  [Header 1.a](#header1.a-1)  
2.2\.  [Header 2](#header2-1)  
2.3\.  [Contribute](#contribute)  
2.3.1\.  [Publish new readme](#publishnewreadme)  
2.3.2\.  [Install locally and watch](#installlocallyandwatch)  
2.3.3\.  [Publish new version](#publishnewversion)  
2.4\.  [Support](#support)  
2.5\.  [References](#references)  

<a name="installationandusage"></a>

## 0.1\. Installation and Usage

Currently, you'll need to download the source code from [GitHub][repo] or clone
the repository, and the run the installation script manually.

    pip install markup-markdown

There are two components to the project: a Python module, `markup`, and a
Python script that acts as a simple command line interface to the module,
`markup`.

Assuming you have a file named `foo.m.md`, you can generate the preprocessed
file `foo.md` by running the following command:

    markup foo.m.md -o foo.md

If you do not specify an output file name, the results will be printed to
stdout, enabling them to be piped to another command.

By default, all available modules are enabled. You can specify a list of
modules to exclude:

    markup foo.m.md -o foo.md -e latexrender,youtubembed

To watch directory and subdirectories:

    markup -w PATH

Where PATH is a directory path, e.g. `.`, `/home/user`.

To see usage instructions, including a list of enabled modules, supply the
-h or --help arguments:

    markup --help

<a name="modules"></a>

## 0.2\. Modules

<a name="includes"></a>

### 0.2.1\. Includes

In order to facilitate large documentation projects, MarkdownPP has an Include
module that will replace a line of the form `!INCLUDE "path/to/filename"` with
the contents of that file, recursively including other files as needed.

File `foo.m.md`:

Hello

File `bar.m.md`:

World!

File `index.m.md`:


Compiling `index.m.md` with the Include module will produce the following:

Hello
World!

Furthermore, the Include module supports the shifting of headers in the
file to be included. For example,

File `foo.m.md`:

    # Foo
    ## Bar

File `index.m.md`:

    # Title
    ## Subtitle
    !INCLUDE "foo.m.md", 2

Compiling `index.m.md` with the Include module and using `2` as shift
parameter will yield:

    # Title
    ## Subtitle
    ### Foo
    #### Bar

<a name="includeurls"></a>

### 0.2.2\. IncludeURLs

Facilitates the inclusion of remote files, such as files kept in a subversion
or GitHub repository. Like Include, the IncludeURL module can replace a line of
the form `!INCLUDEURL "http://your.domain/path/to/filename"` with the contents
returned from that url, recursively including additional remote urls as needed.

IncludeURL runs immediately after the Include module finishes executing. This
means that is it possible to include local files that then require remote files,
but impossible parse !INCLUDE statements found in remote files. This is prevent
ambiguity as to where the file would be located.

Remote file `http://your.domain/foo.m.md`:

    Hello

Remote file `http://your.domain/bar.m.md`:

    Remote World!

Local file `index.m.md`:

    !INCLUDEURL "http://your.domain/foo.m.md"
    !INCLUDEURL "http://your.domain/bar.m.md"

Compiling `index.m.md` with the IncludeURL module will produce the following:

    Hello
    Remote World!

<a name="includecode"></a>

### 0.2.3\. IncludeCode

Facilitates the inclusion of local code files. GFM fences will be added
around the included code.

Local code file `hello.py`:

    def main():
        print "Hello World"


    if __name__ == '__main__':
        main()

Local file `index.m.md`:

    # My Code

    !INCLUDECODE "hello.py"
    Easy as that!

Compiling `index.m.md` with IncludeCode module wil produce the following:

    # My Code

    ```
    def main():
        print "Hello World"


    if __name__ == '__main__':
        main()
    ```
    Easy as that!

Furthermore the IncludeCode module supports line extraction and language
specification. The line extraction is like python list slicing (e.g. 3:6; lines
three to six). Please note that line counting starts at one, not at zero.

Local file `index.m.md`:

    # My Code

    !INCLUDECODE "hello.py" (python), 1:2
    Easy as that!

Compiling `index.m.md` with IncludeCode module will produce the following:

    # My Code

    ```python
    def main():
        print "Hello World"
    ```
    Easy as that!

<a name="tableofcontents"></a>

### 0.2.4\. Table of Contents

The biggest feature provided by MarkdownPP is the generation of a table of
contents for a document, with each item linked to the appropriate section of the
markup. The table is inserted into the document wherever the preprocessor finds
`!TOC` at the beginning of a line. Named `<a>` tags are inserted above each
Markdown header, and the headings are numbered hierarchically based on the
heading tag that Markdown would generate.

```
!TOC DEPTH H1_LANG
```

Where DEPTH is [1-6], H1_LANG is language for h1 header in TOC, [en|cn] , e.g. `!TOC 5 cn`.

<a name="reference"></a>

### 0.2.5\. Reference

Similarly, MarkdownPP can generate a list of references that follow Markdown's
alternate link syntax, eg `[name]: <url> "Title"`. A list of links will be
inserted wherever the preprocessor finds a line beginning with `!REF`. The
generated reference list follows the same alternate linking method to ensure
consistency in your document, but the link need not be referenced anywhere in
the document to be included in the list.

<a name="latexrendering"></a>

### 0.2.6\. LaTeX Rendering

Lines and blocks of lines beginning and ending with $ are rendered as LaTeX,
using [QuickLaTeX](http://www.holoborodko.com/pavel/quicklatex/).

For example,

![\displaystyle \int x^2 = \frac{x^3}{3} + C](<html>
<head><title>405 Not Allowed</title></head>
<body bgcolor="white">
<center><h1>405 Not Allowed</h1></center>
</body>
</html> "\displaystyle \int x^2 = \frac{x^3}{3} + C")


becomes

![\displaystyle \int x^2 = \frac{x^3}{3} + C](http://quicklatex.com/cache3/ea/ql_0f9331171ded7fa9ef38e57fccf74aea_l3.png "\\displaystyle \int x^2 = \frac{x^3}{3} + C")

<a name="youtubeembeds"></a>

### 0.2.7\. YouTube Embeds

As GitHub-flavored Markdown does not allow embed tags, each line of the form
`!VIDEO "[youtube url]"` is converted into a screenshot that links to the video,
roughly simulating the look of an embedded video player.

For example,

    !VIDEO "http://www.youtube.com/embed/7aEYoP5-duY"

becomes

[![Link to Youtube video](images/youtube/7aEYoP5-duY.png)](http://www.youtube.com/watch?v=7aEYoP5-duY)

<a name="examples"></a>

## 0.3\. Examples

Example file.m.md:

<a name="documenttitle"></a>

# 1\. Document Title

0.1\.  [Installation and Usage](#installationandusage)  
0.2\.  [Modules](#modules)  
0.2.1\.  [Includes](#includes)  
0.2.2\.  [IncludeURLs](#includeurls)  
0.2.3\.  [IncludeCode](#includecode)  
0.2.4\.  [Table of Contents](#tableofcontents)  
0.2.5\.  [Reference](#reference)  
0.2.6\.  [LaTeX Rendering](#latexrendering)  
0.2.7\.  [YouTube Embeds](#youtubeembeds)  
0.3\.  [Examples](#examples)  
1\.  [Document Title](#documenttitle)  
1.1\.  [Header 1](#header1)  
1.1.1\.  [Header 1.a](#header1.a)  
1.2\.  [Header 2](#header2)  
2\.  [Document Title](#documenttitle-1)  
2.1\.  [Header 1](#header1-1)  
2.1.1\.  [Header 1.a](#header1.a-1)  
2.2\.  [Header 2](#header2-1)  
2.3\.  [Contribute](#contribute)  
2.3.1\.  [Publish new readme](#publishnewreadme)  
2.3.2\.  [Install locally and watch](#installlocallyandwatch)  
2.3.3\.  [Publish new version](#publishnewversion)  
2.4\.  [Support](#support)  
2.5\.  [References](#references)  

<a name="header1"></a>

## 1.1\. Header 1

<a name="header1.a"></a>

### 1.1.1\. Header 1.a

<a name="header2"></a>

## 1.2\. Header 2

*	[GitHub][github]
*	[GitHub][github]
*	[Markdown Preprocessor on GitHub][repo]

[github]: http://github.com "GitHub"

The preprocessor would generate the following Markdown-ready document file.md:

<a name="documenttitle-1"></a>

# 2\. Document Title

1\. [Header 1](#header1)
1.1\. [Header 1.a](#header1a)
2\. [Header 2](#header2)

<a name="header1"></a>

<a name="header1-1"></a>

## 2.1\. Header 1

<a name="header1a"></a>

<a name="header1.a-1"></a>

### 2.1.1\. Header 1.a

<a name="header2"></a>

<a name="header2-1"></a>

## 2.2\. Header 2

- [GitHub][github]

[github]: http://github.com "GitHub"

<a name="contribute"></a>

## 2.3\. Contribute

<a name="publishnewreadme"></a>

### 2.3.1\. Publish new readme

Generate file.

```
cd ROOT_DIR
markup README.m.md -o README.md
```

<a name="installlocallyandwatch"></a>

### 2.3.2\. Install locally and watch

Watch dirs.

```
python setup.py sdist && pip install -U dist/markup-1.0.3.tar.gz && markup -w .
```

<a name="publishnewversion"></a>

### 2.3.3\. Publish new version

```
./scripts/publish.sh
```

<a name="support"></a>

## 2.4\. Support

If you find any problems with MarkdownPP, or have any feature requests, please
report them to [GitHub][repo], and I will respond when possible. Code
contributions are _always_ welcome, and ideas for new modules, or additions to
existing modules, are also appreciated.

<a name="references"></a>

## 2.5\. References

*	[GitHub][github]
*	[GitHub][github]
*	[Markdown Preprocessor on GitHub][repo]

[repo]: http://github.com/jreese/markdown-pp "Markdown Preprocessor on GitHub"
