import pickle
from textgenrnn import textgenrnn
import markovify
import nltk
import random
import model_helpers

def run_markov(num_sentences):
	"""
	Runs the markov model to produce a speech.
	"""
	# open the markov model file
	with open('model_pickles/markov_model_final.pickle', 'rb') as f:
		markov = pickle.load(f)

	# write the speech with the markov model just downloaded
	paragraph = make_bad_speech(num_sentences, markov)

	return paragraph



def evaluate_text(text):
	"""
	Using the evaluation function, scores the given text. 
	"""
	return grammar_score(text, grammar)



def run_predict(text):
	"""
	Using the pickled models and data transformation 'helpers' (such as the)
	count vectorizer), returns a prediction of if the given commencement address
	was given by a politician, a celebrity, an academic, an author, or a 
	business person.
	"""
	# Unpickles all the models and model helpers needed in the pipeline.
	with open('model_pickles/dict.pkl', 'rb') as f:
		dictionary = pickle.load(f)

	with open('model_pickles/lda_model.pkl', 'rb') as f:
		lda_model = pickle.load(f)

	with open('model_pickles/svd_model.pkl', 'rb') as f:
		svd_model = pickle.load(f)

	with open('model_pickles/count_vectorizer.pkl', 'rb') as f:
		count_vectorizer = pickle.load(f)

	with open('model_pickles/scaler.pkl', 'rb') as f:
		scaler = pickle.load(f)

	with open('model_pickles/knn_classifier.pkl', 'rb') as f:
		classifier = pickle.load(f)

	with open('model_pickles/le.pkl', 'rb') as f:
		label_encoder = pickle.load(f)

	return model_helpers.pipeline(text, dictionary, lda_model, svd_model, 
		count_vectorizer, scaler, classifier, label_encoder)



def make_bad_speech(num_sentences, markov_model):
	"""
	Uses the combined model to make a markov-generated speech of the specified length.
	"""
	# starting sentence
	paragraph = [markov_model.make_sentence()]
	i = 1 # we already have one sentence
	while i < num_sentences:
		start_word = random.choice(paragraph[i-1].split(' ')).title()
		# get a sentence using a word from the last sentence (not always possible with all words
		#, so we use a try-except block to try until it hits upon a possible start word)
		try:
			paragraph.append(markov_model.make_sentence_with_start(start_word))
		except:
			paragraph.append(markov_model.make_sentence())
		i += 1
	return ' '.join(paragraph)



def grammar_score(transcript):
	"""
	This is the evaluation function - it need a grammar and the speech you want 
	to evaluate.
	"""
	cfg_string1 = """
	S -> NPS VP | 'IN' NPS VP | 'DT' NPS VP | 'EX' NPS VP
	NPS -> NP | NP 'CC' NP | 'WRB' NP
	NP -> Pronoun | ProperNoun | Det| Det Nominal | Nominal
	Pronoun -> 'WP' | 'WP$' | 'PRP' | 'PRP$'
	ProperNoun -> 'NNP' | 'NNPS'
	Det -> 'CD' | 'DT' | 'WDT' | 'PDT' | 'TO'
	Nominal -> 'NN' | 'NNS'
	VP -> Verb | Verb NPS | Verb NPS PP | Verb PP | Verb VP | toVerb Adverb | Verb Adj | Verb NPS 'VBG'
	Verb -> 'MD' 'VB' | 'VBD' | 'VBN' | 'VBP' | 'VBZ' | 'VBG'
	Adverb -> 'RB'| 'RBS' | 'RBR'
	toVerb -> 'TO' Verb
	Adj -> 'JJ' | 'JJR' | Det 'JJS'
	PP -> Preposition NPS
	Preposition -> 'IN'
	"""
	grammar = nltk.CFG.fromstring(cfg_string1)

	rdp = nltk.RecursiveDescentParser(grammar)
	correct = 0
	incorrect = 0

	# get the sentences by themselves
	sentences = []
	sentence = []
	for tag in [word_tup[1] for word_tup in nltk.pos_tag(nltk.word_tokenize(transcript))]:
		if tag in [',',"'",'!','?',':', ""'``'"", "\'\'"]:
			pass
		elif tag == 'RP':
			sentence.append('TO')
		elif tag != '.':
			sentence.append(tag)
		else:
			sentences.append(sentence)
			sentence = []
	if len(sentence) != 0:
		sentences.append(sentence)

	for sentence in sentences:
		parsed = rdp.parse(sentence)
		if len(list(parsed)) > 0:
			correct += 1
			for tree in rdp.parse(sentence):
				print(tree)
		else:
			incorrect += 1
	return correct/(correct + incorrect)