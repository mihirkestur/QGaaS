#!pip install yake
#import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import OrderedDict

# init Steps Yake
import yake
kw_extractor = yake.KeywordExtractor()
language = "en"
# u can tinker with this to decrease number of keywords, words per keyword
max_ngram_size = 2
# u can tinker with this to increase number of keywords
deduplication_threshold = 0.3
numOfKeywords = 20
custom_kw_extractor = yake.KeywordExtractor(
    lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, top=numOfKeywords, features=None)

#contexts=["Abd retired", "rcb is damar", "virat left captaincy", "dravid is amazing", "india won series" ,"Long sentences are made up of many words and thus may pose a threat to keyword extractors"]


stop_words = set(stopwords.words('english'))


def CombineContexts(contexts):
    wholeText = ""
    reducedContexts = list()
    for context in contexts:
        ConText = context.strip().lower()+".\n"
        word_tokens = word_tokenize(ConText)
        newContext = ""
        for word in word_tokens:
            if not word.lower() in stop_words:
                wholeText += word+" "
                newContext += word+" "
        reducedContexts.append(newContext.strip())
    # print(wholeText)
    return wholeText, reducedContexts


def GetRankedKeywords(wholeText):
    keyWordsYake = custom_kw_extractor.extract_keywords(wholeText)
    # print(keyWordsYake)
    return keyWordsYake


def RankContexts(contexts):

    wholeText, redContexts = CombineContexts(contexts)
    RankedKw = dict(GetRankedKeywords(wholeText))
    # print(RankedKw)
    # print(redContexts)
    votesContexts = dict.fromkeys(redContexts, 0)
    mappings = dict(zip(redContexts, contexts))
    # print(mappings)
    # for context in range(len(redContexts)):
    #   contextWt=0

    #   for word in redContexts[context].replace(".","").split():
    #     #print(word.lower())
    #     if word in RankedKw:
    #       print(word)
    #       contextWt+=1/(RankedKw[word]+0.00000000001)

    #   votesContexts[contexts[context]]=contextWt

    for keywds in RankedKw:
        for cont in votesContexts:
            if keywds in cont:
                votesContexts[cont] += (1/RankedKw[keywds])

    weightedContexts = list()

    for context in dict(sorted(votesContexts.items(), key=lambda item: item[1], reverse=True)).keys():
        weightedContexts.append(mappings[context])
    # print(weightedContexts)
    return weightedContexts

# print(contexts)
# print(RankContexts(contexts))
# call rankedCOntexts fn py passing a list of strings
# returns new weighted contexts list
