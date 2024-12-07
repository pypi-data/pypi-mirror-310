def TokenizeStopwordPOS():
    code = '''
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import pos_tag

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

file_path = '/Users/hr/DYPIU/Sem 3/Advance AI/Exams/dataset/Text dataset/textfile(3).txt'
file = open(file_path, mode='r', encoding='UTF-8')
text = file.read()

# for i in text:
#     print(text)

# sentences tokonize
sentences = sent_tokenize(text)
print(f"Tokenized Sentences:\n" )
for sent in sentences:
    print(sent)

# words tokenize
word_tokens = [word_tokenize(sentence) for sentence in sentences]
print(f"Word Tokens: \n")

for sent in word_tokens:
    for word in sent:
        print(word)
    print("-------------------\n\n")

# stopwords

stop_words = set(stopwords.words('english'))

filtered_words = []
for tokens in word_tokens:
    sentence_filtered = []
    for word in tokens:
        if word.lower() not in stop_words:
            sentence_filtered.append(word)
    filtered_words.append(sentence_filtered)

print("Filtered Words (Stopwords Removed): \n")
for words in filtered_words:
    print(words)
    print("---------------\n\n")

# Part of speech

pos_tags = [pos_tag(tokens) for tokens in filtered_words[:10]] # 10 stands for only 10 sentences
print(f"POS Tags: \n")
for toks in pos_tags:
    print(toks)
    print("---------------\n\n")
'''
    print(code)

def LemmatizeText():
    print("This is my new function created by Rahul Shinde 2566")