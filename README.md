# Delbot™

It understands your voice commands, searches news and knowledge sources, and summarizes and reads out content to you.

Check out the demo [video](https://youtu.be/iVmj1gHOF0w). Also read my Delbot article published in [Chatbots Magazine](https://chatbotsmagazine.com/delbot-nlp-python-bot-1a46d865e38b).

# How to Run
1. Install the required [packages](https://github.com/shaildeliwala/delbot#libraries).
2. Open a command prompt and navigate to root folder of project.
3. Enter `python app.py` in command prompt to launch web service.
4. Go to http://localhost:5000 (or whichever IP and port you specified).

# Roadmap
1. Statistical model to determine category such as _who_, _why_, _what_, and _when_ of knowledge questions.
2. Headlines-only news request.
3. Better UI!

# Index
1. [Introduction](https://github.com/shaildeliwala/delbot#introduction)
2. [Overview](https://github.com/shaildeliwala/delbot#overview)
    1. [News](https://github.com/shaildeliwala/delbot#news)
    2. [Knowledge](https://github.com/shaildeliwala/delbot#knowledge)
3. [How It Works](https://github.com/shaildeliwala/delbot#how-it-works)
    1. [News Queries](https://github.com/shaildeliwala/delbot#news-queries)
        1. [Parts of speech and tags](https://github.com/shaildeliwala/delbot#parts-of-speech-and-tags)
        2. [Noun chunks](https://github.com/shaildeliwala/delbot#noun-chunks)
        3. [Adpositions? Did you mean prepositions?](https://github.com/shaildeliwala/delbot#adpositions-did-you-mean-prepositions)
        4. [Implementation](https://github.com/shaildeliwala/delbot#implementation)
    2. [Knowledge Queries](https://github.com/shaildeliwala/delbot#knowledge-queries)
        1. [Parts of speech and tags](https://github.com/shaildeliwala/delbot#parts-of-speech-and-tags-1)
        2. [Noun chunks](https://github.com/shaildeliwala/delbot#noun-chunks-1)
        3. [Auxiliary verbs (or their absence)](https://github.com/shaildeliwala/delbot#auxiliary-verbs-or-their-absence)
        4. [Implementation](https://github.com/shaildeliwala/delbot#implementation-1)
4. [Summarization](https://github.com/shaildeliwala/delbot#summarization)
5. [Libraries](https://github.com/shaildeliwala/delbot#libraries)
6. [Web App](https://github.com/shaildeliwala/delbot#web-app-optional)
7. [Limitations](https://github.com/shaildeliwala/delbot#limitations)
8. [Conclusion and Future Work](https://github.com/shaildeliwala/delbot#conclusion-and-future-work)
9. [Demo](https://github.com/shaildeliwala/delbot#demo)
10. [References and Links](https://github.com/shaildeliwala/delbot#references-and-links)

# Introduction
Bots remain a hot topic. Everyone is talking about them.

How about building one from scratch? The simple one we will build today will understand and answer questions like:
- What is the latest news on Star Wars in the New York Times?
- Who is Donald Trump?
- Read me the latest on Brexit.
- What are RDF triples?
- Who was Joan of Arc?
- Give me news about the UK government from the Guardian.

Our goal is to code a bot from the ground up and use [nature language processing (NLP)](https://en.wikipedia.org/wiki/Natural_language_processing) while doing so.

In addition, our bot will be voice-enabled and web-based if you complete the web app section as well. The best part is we do not need to do anything fancy for speech recognition and synthesis: we will use a [built-in](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API) capability of modern web browsers.

# Overview
At a high level, we want to be able to understand two broad types of queries. Following is the flowchart.

![Delbot flow diagram](flowdiagram.png "Delbot flow diagram")


## News

We might ask for **news**. E.g.:
>What is the latest on Fantastic Beasts in the Guardian?

The bot will query the API of the requested news source (New York Times if none is specified) and summarize the results:<br>
>[...] Comparing the first Harry Potter film (2001’s Harry Potter and the Philosopher’s Stone) with the last (2011’s Harry Potter and the Deathly Hallows Part Two) is somewhat akin to comparing Bambi with Reservoir Dogs. We first meet him in 1920s New York – almost 60 years before Harry is even born – where he is [...]<br>
(source: https://www.theguardian.com/books/2016/nov/25/jk-rowling-fantastic-beasts-screenplay)

## Knowledge

We might ask a **knowledge** question. E.g.:
>What are RDF triples?

And the bot will answer:<br>
>A semantic triple, or simply triple, is the atomic data entity in the Resource Description Framework .\nThis format enables knowledge to be represented in a machine-readable way. Particularly, every part of an RDF triple is individually addressable via unique URIs \u2014 for example, the second statement above might be represented in RDF as http://example.name#BobSmith12 http://xmlns.com/foaf/0.1/knows http://example.name#JohnDoe34.<br>
(source: https://en.wikipedia.org/wiki/Semantic_triple)

# How It Works
We define a simple rule to categorize inputs: if the query contains either of the words _news_ or _latest_, it is a _news query_. Otherwise, it is a _knowledge query_.

The [`predict`](resources/query_service.py#L38) function of the [`QueryAnalyzer`](resources/query_service.py#L34) class is the main entry point for our bot. It performs the above categorization. It calls other functions to

1. Extract the _query_ and, if applicable, the _source_ from the input
2. Make necessary API calls
3. Summarize lengthy content

Finally, it returns the output and a flag indicating if there was any error.

## News Queries
We assume input to be of one of the following forms.

_What is the latest news **on** Star Wars **in** the New York Times?_<br>
_Read me the latest **on** Brexit._<br>
_Give me news **about** Marvel Cinematic Universe movies in 2017 **from** the Guardian._<br>

### Parts of speech and tags
<table border="1" class="dataframe">
  <tbody>
    <tr>
      <th>Token</th>      <td>Give</td>      <td>me</td>      <td>the</td>      <td>latest</td>
      <td>news</td>      <td>on</td>      <td>Donald</td>      <td>Trump</td>      <td>from</td>
      <td>the</td>      <td>New</td>      <td>York</td>      <td>Times</td>      <td>.</td>
    </tr>
    <tr>
      <th>POS</th>      <td>VERB</td>      <td>PRON</td>      <td>DET</td>      <td>ADJ</td>
      <td>NOUN</td>      <td><b>ADP</b></td>      <td>PROPN</td>      <td>PROPN</td>      <td><b>ADP</b></td>
      <td>DET</td>      <td>PROPN</td>      <td>PROPN</td>      <td>PROPN</td>      <td>PUNCT</td>
    </tr>
    <tr>
      <th>TAG</th>      <td>VB</td>      <td>PRP</td>      <td>DT</td>      <td>JJS</td>
      <td>NN</td>      <td>IN</td>      <td>NNP</td>      <td>NNP</td>      <td>IN</td>
      <td>DT</td>      <td>NNP</td>      <td>NNP</td>      <td>NNP</td>      <td>.</td>
    </tr>
  </tbody>
</table>

### Noun chunks
1. the latest news
2. Donald Trump
3. the New York Times

### Adpositions? Did you mean _prepositions_?
There is a pattern in sentences structured as above. And prepositions are key.

The topic of search is between the first and the last prepositions. The requested source is at the end after the last preposition. The last noun chunk is the source.

In case a source is not specified, as in the second example, everything after the first preposition is assumed to be the topic of search.

_Adpositions_, simply put, are [prepositions and postpositions](https://en.wikipedia.org/wiki/Preposition_and_postposition).

In a [head-initial](https://en.wikipedia.org/wiki/Head_(linguistics)) language like English, adpositions usually precede the noun phrase. E.g. characters _from_ the Marvel Cinematic Universe. While in a head-final language like Gujarati, adpositions follow the noun phrase. These are postpositions. E.g. માર્વેલ ચલચિત્ર જગત_ના_ પાત્રો, which translates word by word to: Marvel Cinematic Universe of characters.

### Implementation
We invoke [`get_news_tokens`](query_extractor.py#L40) from the [`QueryExtractor`](query_extractor.py#L28) class, which extracts the _source_ and the _query_ from the input. Internally, it calls `_split_text` to extract noun chunks, parts of speech, and the fully parsed text from the input. We lemmatize terms in the query.

Next, we invoke the [`get_news`](media_aggregator.py#L67) function using _query_ on one of the `Aggregator` classes in [media_aggregator.py](media_aggregator.py) based on the _source_. This returns a list of news articles that were sent as a response by the news API. We currently support [The Guardian API](http://open-platform.theguardian.com/) and [The New York Times API](https://developer.nytimes.com/).

Finally, we pick the first item (by default) from the _response_ list and summarize it using the [`shorten_news`](https://github.com/shaildeliwala/delbot/blob/master/media_aggregator.py#L76) function.

## Knowledge Queries
We assume input to be of one of the following forms.

_John Deere_<br>
_Joan of Arc_<br>
_Who **is** Donald Trump?_<br>
_Who **was** JRR Tolkien?_<br>
_What **is** subject predicate object?_<br>
_Tell **me** about particle physics._

### Parts of speech and tags
#### Example 1
<table border="1" class="dataframe">
  <tbody>
    <tr>
      <th>Token</th>      <td>What</td>      <td>is</td>      <td>an</td>      <td>RDF</td>      <td>triple</td>      <td>?</td>
    </tr>
    <tr>
      <th>POS</th>      <td>NOUN</td>      <td>VERB</td>      <td>DET</td>      <td>PROPN</td>      <td>NOUN</td> <td>PUNCT</td>
    </tr>
    <tr>
    <th>TAG</th>      <td>WP</td>      <td><b>VBZ</b></td>      <td>DT</td>      <td>NNP</td>      <td>NN</td>     <td>.</td>
    </tr>
  </tbody>
</table>

#### Example 2

<table border="1" class="dataframe">
  <tbody>
    <tr>
      <th>Token</th>      <td>Tell</td>      <td>me</td>      <td>about</td>      <td>he</td>      <td>-</td>      <td>man</td>
      <td>and</td>      <td>the</td>      <td>masters</td>      <td>of</td>      <td>the</td>      <td>universe</td> <td>.</td>
    </tr>
    <tr>
    <th>POS</th>      <td>VERB</td>      <td><b>PRON</b></td>      <td>ADP</td>      <td>PRON</td>      <td>PUNCT</td>
      <td>NOUN</td>      <td>CONJ</td>      <td>DET</td>      <td>NOUN</td>      <td>ADP</td>      <td>DET</td>
      <td>NOUN</td>      <td>PUNCT</td>
    </tr>
    <tr>
      <th>TAG</th>      <td>VB</td>      <td>PRP</td>      <td>IN</td>      <td>PRP</td>      <td>HYPH</td>      <td>NN</td>
      <td>CC</td>      <td>DT</td>      <td>NNS</td>      <td>IN</td>      <td>DT</td>      <td>NN</td>      <td>.</td>
    </tr>
  </tbody>
</table>

### Noun chunks
#### Example 1
1. What
2. an RDF triple

#### Example 2
1. me
2. he-man
3. the masters
4. the universe

### Auxiliary verbs (or their absence)
If we find an [auxiliary verb](https://www.ego4u.com/en/cram-up/grammar/auxiliary-verbs), we treat everything after its first occurrence as the query. Thus, in **Example 1**, the query is _RDF triple_.

Otherwise, we treat all noun chunks after the first as the query. Thus, in **Example 2**, the query is _he-man the masters the universe_.

### Implementation
We invoke [`get_knowledge_tokens`](query_extractor.py#L50) from the [`QueryExtractor`](query_extractor.py#L28) class, which extracts the _query_.

We pass this to the [`get_gkg`](media_aggregator.py#L89) function, which queries the Wikipedia API through the _wikipedia_ Python package and returns a 5-sentence summary of the top result.

# Summarization
I used the [`FrequencySummarizer`](summarizer.py#L29) class from [Text summarization with NLTK](http://glowingpython.blogspot.in/2014/09/text-summarization-with-nltk.html). Alternatively, you could use [sumy](https://pypi.python.org/pypi/sumy).

# Libraries
In addition to the packages _re_, _bs4_, _requests_, _operator_, _collections_, _heapq_, _string_ and _nltk_, we will use the following.

1. **spaCy**: Please set it up as given in the [Install spaCy docs](https://spacy.io/docs/usage/). spaCy will help us do some quick NLP. We could use NLTK but spaCy will get you going faster. We use spaCy in this project.

2. **Wikipedia**: This helps query the Wikipedia API. You can read the docs of the _wikipedia_ Python package [here](https://pypi.python.org/pypi/wikipedia/).

3. **Summarizer**: The one I used was borrowed from [The Glowing Python](http://glowingpython.blogspot.in/2014/09/text-summarization-with-nltk.html) blog written by [JustGlowing](https://www.blogger.com/profile/17212021288715206641). It summarizes lengthy content. Alternatively, you could use [sumy](https://pypi.python.org/pypi/sumy).

4. **Flask-RESTful, Flask (Optional)**: These are for building a web app and operationalizing our bot through a RESTful web service.

# Web App (Optional)
We add a cool webpage from which you can fire off voice queries and have the browser read out the response content. We make use of the [Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API) for this.

## Web Service
We get our Flask-based REST web service up and running in under 20 lines of code. The [`QueryService`](resources/query_service.py#L27) class handles requests.

As of now, we only need one service call to send input from our web app to our bot. This is done through the [`post`](resources/query_service.py#L28) function of the `QueryService` class. `post`, in turn, calls the `predict` function, which is the main entry point as mentioned [above](https://github.com/shaildeliwala/delbot#how-it-works).

## Web Site
I built a basic webpage to demonstrate the bot. It uses the [Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API) to receive voice input and read out content. You can find the [index.html](templates/index.html) file in the templates folder. Make sure you have installed all the required packages and libraries, and that the web service is up and running before you open the website.

# Limitations
Our simple bot understands a limited range of requests. It cannot understand other kinds of requests such as follows.

1. **Knowledge requests with a different structure**<br>
_Explain to me what bootstrap aggregation is._<br>
_Tell me something about computational neuroscience._<br>

2. **News requests with a different structure**<br>
_What does the New York Times say about Roger Federer's latest match?_<br>
_What's happening in the world of tennis?_<br>

3. **Knowledge requests of other types**<br>
_How is cheese made?_<br>
_Where was JK Rowling born?_<br>
_Can we build a sky city on Venus?_<br>
_When did the French Revolution take place?_<br>
_Why does Jupiter have The Great Red Spot?_<br>

4. **Follow-up questions and context**<br>
_Explain to me what bootstrap aggregation is._<br>
and then: _How does it relate to random forests?_<br>

Understanding what _it_ refers to in the follow-up question comes under what is known as [anaphora resolution](https://en.wikipedia.org/wiki/Anaphora_(linguistics)). It is all a part of understanding context. Different words mean different things in different contexts. While humans have a nuanced understanding of these, it is significantly more difficult to teach machines the same.

# Conclusion and Future Work
We achieved our goal of building a bot based on some rules we defined. We also made use of some NLP techniques. Finally, we deployed our bot onto a web application. However, our bot is limited in the kinds of queries it can understand and answer. Why is its scope of understanding so narrow?

In general, making computers really _understand_ language is an [AI-hard](https://en.wikipedia.org/wiki/AI-complete) problem. There is a field known as [NLU](https://en.wikipedia.org/wiki/Natural_language_understanding) (Natural Language Understanding) within NLP dedicated to this.

We could implement a machine learning-based solution so our bot could potentially understand a much wider range of requests.

# References and Links
1. [Alphabetical list of part-of-speech tags used in the Penn Treebank Project](https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html)
2. [Stanford typed dependencies manual](http://nlp.stanford.edu/software/dependencies_manual.pdf)
3. Wikipedia articles
    1. [Head-directionality parameter](https://en.wikipedia.org/wiki/Head-directionality_parameter)
    2. [AI-hard](https://en.wikipedia.org/wiki/AI-complete)
    3. [NLU](https://en.wikipedia.org/wiki/Natural_language_understanding) (Natural Language Understanding)
    4. [anaphora resolution](https://en.wikipedia.org/wiki/Anaphora_(linguistics))
    5. [prepositions and postpositions](https://en.wikipedia.org/wiki/Preposition_and_postposition)
    6. [head-initial](https://en.wikipedia.org/wiki/Head_(linguistics))
4. [Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API)
5. [Text summarization with NLTK](http://glowingpython.blogspot.in/2014/09/text-summarization-with-nltk.html)
6. [New York Times Developer API](https://developer.nytimes.com/)
7. [The Guardian Open Platform](http://open-platform.theguardian.com/)
8. [Quora thread: What makes natural language processing difficult?](https://www.quora.com/What-makes-natural-language-processing-difficult)

Please make sure to read the terms of use of the APIs used here.
<hr>
Check out the demo [video](https://youtu.be/iVmj1gHOF0w) or read my Delbot article published in [Chatbots Magazine](https://chatbotsmagazine.com/delbot-nlp-python-bot-1a46d865e38b).
