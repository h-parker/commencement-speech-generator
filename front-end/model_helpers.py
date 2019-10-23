import spacy
import re
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.neighbors import KNeighborsClassifier
from gensim.corpora import Dictionary
from wordcloud import WordCloud
from gensim.models import LdaMulticore
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import MaxAbsScaler


def preprocess(text):
	"""
	Process the text by removing punctuation, stop words, lowercasing,
	lemmatizing, etc. Returns a list of lemmatized tokens.
	"""

	# remove punctuation
	punctuation = ['.', ',', '?', '/', "'", '"', 
					':', ';', ')', '(', '*', '&',
					'^', '%', '$', '#', '!', '`', 
					'-', '_', '[', ']', '<', '>',
					'\n', '\r', '’', '~', '|']
	for punc in punctuation:
		text = text.replace(punc, ' ')
		
	# replace years with 'year'
	text = re.sub(r'(19|20)\d{2}\s', 'year ', text)
		
	# lowercase
	text = text.lower()

	# remove stopwords
	# adding 'applause' to nltk's list, since it
	# occurs a lot & is unhelpful 
	wordsFiltered = '' # collect non-stop-words
	stopWords = set(stopwords.words('english'))
	stopWords.add('applause')
	for w in word_tokenize(text):
		if w not in stopWords:
			wordsFiltered += w + ' '

	# lemmatize  
	# nltk's lemmatizer was garbage 
	# lemmatizer = WordNetLemmatizer() 
	# lemmatized = [lemmatizer.lemmatize(word) for word in wordsFiltered] 

	# Initialize spacy 'en' model, keeping only tagger component needed for lemmatization
	sp = spacy.load('en')

	# Parse the sentence using the loaded 'en' model object `nlp`
	lemmatized = sp(wordsFiltered)

	return [word.lemma_ for word in lemmatized]



def get_svd_features(count_vectorizer, svd_model, processed_transcript):
	"""
	Using the tokenized transcript, gets the count vectorized version and 
	uses SVD to reduce the dimension of the feature space.
	"""
	bow = count_vectorizer.transform([' '.join(processed_transcript)])
	return svd_model.transform(bow)



def get_top_topic(processed_transcript, dictionary, lda_model):
	"""
	Get lda topic for tokenized transcript, then sort topics by probability and 
	choose the topic with the greatest probability
	"""
	doc_bow = dictionary.doc2bow(processed_transcript)
	topics = [x for x in lda_model.get_document_topics(doc_bow)]
	#We need to select the 0th element of that topic (it's a tuple -- 
	#(index, probability) -- and we only want the topic, not the probability)
	if len(topics) > 1:
		return sorted(topics, key=lambda x:x[1])[-1][0]
	else:
		return topics[0][0]



def get_dummy_topic_cols(processed_transcript, dictionary, lda_model):
	"""
	From the tokenized transcript, using the dictionary created from the 
	LDA model and the LDA model, gets the most probable topic for the 
	transcript. Then, returns the dummified version, as is used in
	prediction.  
	"""
	top_topic = get_top_topic(processed_transcript, dictionary, lda_model)
	dummy_cols = []
	for topic in range(0,9):
		if top_topic == topic:
			dummy_cols.append(1)
		else:
			dummy_cols.append(0)
	return dummy_cols



def pipeline(transcript, dictionary, lda_model, svd_model, count_vectorizer, scaler, 
	classifier, label_encoder):
	"""
	Starting with the raw transcript, runs the transcript through the
	cleaning, vectorizing, feature engineering (including vectorizing),
	sclaing, and finally, classifying. Returns the prediction of what
	kind of person gave the commencement address -- a politician, an
	author, an academic, a celebrity, or a business person.
	"""
	tokens = preprocess(transcript)
	svd_features = get_svd_features(count_vectorizer, svd_model, tokens)
	dummy_cols = get_dummy_topic_cols(tokens, dictionary, lda_model)
	features = list(svd_features[0])
	features.extend(dummy_cols)
	scaled_features = scaler.transform(np.array(features).reshape(1, -1))
	prediction = classifier.predict(scaled_features)
	return list(label_encoder.inverse_transform(prediction))