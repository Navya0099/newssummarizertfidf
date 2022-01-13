from nltk import sent_tokenize, word_tokenize, PorterStemmer
from nltk.corpus import stopwords
import math

def create_Frequency_matrix(sentences):
    frequency_matrix = {}
    stopwrds = set(stopwords.words('english'))
    ps = PorterStemmer()
    
    for sent in sentences:
        freq_table = {}
        words = word_tokenize(sent)
        
        for word in words:
            word = word.lower()
            word = ps.stem(word)
            if word in stopwrds:
                continue
            if word in freq_table:
                freq_table[word] += 1
            else:
                freq_table[word] = 1
                
        frequency_matrix[sent[:15]] = freq_table
        
    return frequency_matrix



def create_tf_matrix(freq_matrix):
    tf_matrix = {}
    
    for sent, f_table in freq_matrix.items():
        tf_table = {}
        
        countwords_in_sent =  len(f_table)
        
        for word,count in f_table.items():
            tf_table[word] = count/countwords_in_sent
        
        tf_matrix[sent] = tf_table
        
    return tf_matrix
        

def createdocumentsperwords(freq_matrix):
    
    words_per_doc_table = {}
    
    for sent,f_table in freq_matrix.items():
        
        for word,count in f_table.items():
            
            if word in words_per_doc_table:
                words_per_doc_table[word] += 1
            else:
                words_per_doc_table[word] = 1
            
    return words_per_doc_table


def create_idf_matrix(freq_matrix, count_doc_perwords, total_doc):
    idf_matrix = {}
    
    for sent,f_table in freq_matrix.items():
        idf_table = {}
        
        for word in f_table.keys():
            idf_table[word] = math.log10(total_doc/ float(count_doc_perwords[word]))
            
        idf_matrix[sent] = idf_table
        
    return idf_matrix



def create_tf_idf_matrix(tf_matrix,idf_matrix):
    
    tf_idf_matrix = {}
    
    for (Sent1,f_table1), (Sent2,f_table2) in zip(tf_matrix.items(), idf_matrix.items()):
        
        tf_idf_table = {}
        
        for (word1,value1),(word2,value2) in zip(f_table1.items(),
                                                f_table2.items()):
            tf_idf_table[word1] = float(value1*value2)
            
        tf_idf_matrix[Sent1] = tf_idf_table
        
    return tf_idf_matrix


def sent_scores(tf_idf_matrix) -> dict:
    
    sentencevalue = {}
    
    for sent,f_table in tf_idf_matrix.items():
        total_score_per_Sentence = 0
        
        count_words_in_Sentence = len(f_table)
        
        for word, score in f_table.items():
            total_score_per_Sentence += score
            
        sentencevalue[sent] = total_score_per_Sentence/count_words_in_Sentence
        
    return sentencevalue


def find_avgscore(sentencevalue) -> int:
    
    sumvalues = 0
    
    for entry in sentencevalue:
        sumvalues += sentencevalue[entry]
        
    average = (sumvalues / len(sentencevalue))
    
    return average


def generate_summary(sentences, sentencevalues, threshold):
    
    sentence_count = 0
    summary = " "
    
    for sentence in sentences:
        if sentence[:15] in sentencevalues and sentencevalues[sentence[:15]] >= (threshold):
            summary += " " +sentence
            
            sentence_count += 1
            
    return summary


def summarizer_tfidf(text):
    sentences = sent_tokenize(text)
    total_doc = len(sentences)
    
    # frequency matrix of words in each sentence    
    freq_matrix = create_Frequency_matrix(sentences)
    
    # calculate term frequency and generate matrix
    tf_matrix = create_tf_matrix(freq_matrix)
    
    # creating table for documents per words
    count_doc_per_words = createdocumentsperwords(freq_matrix)
    
    # calculate IDF and generate matrix
    idf_matrix = create_idf_matrix(freq_matrix,count_doc_per_words,total_doc)
    
    # calculate tf-idf 
    tf_idf = create_tf_idf_matrix(tf_matrix,idf_matrix)
    
    # score the sentences
    sentence_scores = sent_scores(tf_idf)
    
    # find threshold
    threshold = find_avgscore(sentence_scores)
    
    summary = generate_summary(sentences, sentence_scores, 1.3*threshold)
    
    return(summary)



