# Con-grad-ulations! 
Commencement Speeches: Generation, Classification, and Evaluation

Picture it -- May 15, 2020, you're a week away from Famous University's commencement and you just have _no idea_ what you're going to say. I mean, you want to give a classic speech, but you don't want to sound just like everyone else! Cue this project -- with this commencement speech generator, you'll be delivering brand new insight to the masses, such as "No one remembers people like Quentin Tarintino" or "The important point here is that you dont even think you deserve a historic commencement address. The greatest successes come from having the freedom to continue to cultivate in yourselves as citizens. The crumbs Im talking about are the choice we make that make us have to worry about Grizzlies breaking into the kitchen." Then, run through the classifier and you'll get an instant idea of what kind of person you'll sound like; that last quote apparently sounds like an author. Finally, just to get an idea of how grammatically correct you are, you'll run that paragraph through the evaluator, only to find that your grammar could be better. But, with that, you're armed with bold, new, authorly, semi-grammatically correct advice to give to hung-over, sleepy, fresh college grads who most likely won't even remember who you were in 5 years anyway!

In all seriousness, this project produces what I like to call a good "first draft" of a commencement address. You most likely wouldn't want to read any of this stuff in front of people you're trying to impress, but it was a good exercise in text generation and, more interestingly, how we can start to evaluate the grammar of text. Nearly no research I've seen has addressed the evaluation of grammar in generated text, so I sought to devise a way to score an algorithmically generated speech, in an effort to improve the commencement speech generated. Read on to see how! 

* [Data](#data)
* [EDA](#eda)
* [Speech Generation](#generation)
* [Text Evaluation](#evaluation)
* [Speaker-Type Classification](#classification)
* [Front-end](#frontend)
* [Next Steps](#nextsteps)


## Data <a name="data"></a>
The data came from Youtube, the US Presidency Project, and Graduation Wisdom. From Youtube, 786 transcripts were gotten from a playlist I compiled, using the [youtube_transcript_api](https://pypi.org/project/youtube-transcript-api/). Then, the US Presidency Project was scraped to get all commencement addresses given by presidents and vice presidents (where the title contained the word "commencement"), along with graduationwisdom.com. 

## EDA <a name="eda"></a>
### Word Frequency
After processing the transcripts, removing punctuation, stopwords, and the like, I count vectorized the transcripts and got the most frequent words and n-grams. Below are the most frequent words and bigrams. 
![Most frequent words - distribution](https://github.com/h-parker/commencement-speech-generator/blob/master/readme_images/word_freq_1_word.png)

It seems a lot like the speakers are talking about what you would expect in a commencement speech -- life after college, what to do with your life, and finding your place in the world -- using words like "work", "life", "time", "make", "go", "world".

![Most frequent bi-grams - distribution](https://github.com/h-parker/commencement-speech-generator/blob/master/readme_images/word_freq_2_gram.png)

The two common threads I found here supported the idea that commencement speakers love telling stories and giving advice, using phrases like "tell story", "one thing", "come back", "anything possible", "every day", and "year old".

### Sentiment
Then, using Textblob, I got the sentiment of each transcript. Because sentiment analysis is really meant for shorter texts, I broke up each text into five segments. I chose five segments since the mean length of the transcripts was roughly 20,000 characters, which translates into roughly 3300 words (if we assume every word is around 6 characters). This translates into around 22 minutes (if we assume people talk at 150WPM), making each chunk around 5 minutes long -- long enough to get a single point across (source: https://www.visualthesaurus.com/cm/wc/seven-ways-to-write-a-better-speech/). Then, I averaged the sentiment scores to get an overall score for the speech. Below, we see the distribution of polarity -- how positive or negative a speech is -- and subjectivity -- how biased from the speaker's perspective a speech is. We can see that overall, speeches tend to be relatively neutral, tending towards positive, and fairly subjective. This makes sense, since commencement speakers generally like to 'tell it like it is' with the (usually somewhat negative) truth, and then give their own personal advice and life story. So, we get some negative parts of the story (such as during 2008-2012, when commencement speakers were very outright with their assessment of the job market during the recession) with an overall message of hope, which averages out to a somewhat positive, but more neutral polarity. And, since all advice and storytelling is told from the speaker's perspective, it makes sense that the speeches are relatively subjective!
![Sentiment distribution](https://github.com/h-parker/commencement-speech-generator/blob/master/readme_images/sentiment.png)

### Topic Generation
Then, I looked at the common topics using LDA. I ultimately chose to go with 12 topics because this number gave the most specific topics that applied to the transcripts, without being overly specific. With a number like 25, we got topics that were clearly only applicable to one or two commencement addresses, and thus were not overly illuminating when it came to understanding the corpus as a whole. 

Below is the distribution of the most probable topics given by LDA. The word clouds associated with the most common of these topics are below that, along with the name I gave to the topic, based on the words in the word cloud, and the speeches associated with that topic. 

<img src="https://github.com/h-parker/commencement-speech-generator/blob/master/readme_images/most_probable_topics.png" alt="Most probable topics - distribution" width="400"/>

<img src="https://github.com/h-parker/commencement-speech-generator/blob/master/readme_images/topics1.png" alt="topics image 1 of 2 - word cloud" width="400"/>

Similar to above, we have the distribution of the second most probable topic amongst speeches, and the word clouds of the more common topics in this distribution that aren't included above.

<img src="https://github.com/h-parker/commencement-speech-generator/blob/master/readme_images/second_most_probably_topics.png" alt="Second most probable topics - distribution" width="400"/>

<img src="https://github.com/h-parker/commencement-speech-generator/blob/master/readme_images/topics2.png" alt="topics image 2 of 2 - word cloud" width="400"/>


## Speech Generation <a name="generation"></a>
Using [Markovify](https://github.com/jsvine/markovify), I made a Markov Model that generates commencement speeches. Markov models only generate sentences, starting with a "start word" (or phrase), and ending with stopping punctuation, so I generated paragraphs by seeding the next sentence with a random word from the previous sentence. Because only some transcripts (roughly half) were punctuated and the others were autogenerated by YouTube, the initial, plain vanilla model had some lengthy run-on sentences. As a result, I made a combined model, combining a model trained on punctuated transcripts, and another model trained on non-punctuated transcripts. I weighted the punctuated model twice as much as the non-punctuated model. This resulted in the interesting results you read in the intro, which tended to be funny, and sometimes unintelligible. The more nonsense sentences generally were nonsense because they lacked any sort of grammar. After all, Markov models are state-based, and proper grammar depends on the whole sentence, not just the current word. This naturally lead me to look into how I could evaluate the grammar of generated text.  If I could come up with a way to say "yes, this is grammatically correct", or "no, this is not correct", I could keep the "good" sentences, and throw away the bad ones. So, off I set! 

## Text Evaluation <a name="evaluation"></a>
The idea of evaluating a sentence as "valid" English or not reminded me of context free grammars (CFGs). While they're used to evaluate the validity of a statement/program written in a formal language, I thought it could be an interesting experiment to try and fit English into that mold. I knew it wouldn't be perfectly comprehensive, but it was a fun place to start, since I was already interested in learning more about CFGs! I used the library spaCy to get the part of speech (POS) tags and wrote a CFG around independent and dependent clauses, and all the ways you can form them and combine them to get a valid English sentence. It ended up evaluated basic sentences as valid English, such as "This is a good sentence." or "I like snow, but I don't like rain." But, it struggled with more complex, longer sentences. Overall, I learned that a CFG was not going to get us where we needed to be! Moving forward, I'd like to use an LSTM with all sorts of speeches used as training data (the grammar of spoken language is not specific to commencement addresses, but is common across all language!) to learn valid POS tag orders and predict new ones! 

## Speaker-Type Classification <a name="classification"></a>
Finally, just because I love creating classifiers, I decided to classify the type of speaker delivering the address. Using the 5 main types of speakers -- politicians (presidents, mayors, etc.), celebrities (actors, comedians, etc.), business people (CEOs and CFOs, etc.), academics (faculty of the college, scientists, etc.), and authors (writers, journalists, etc.) -- I used LSA (latent semantic analysis) to reduce the dimension of the feature space made up of the count vectorization of all the transcripts. I also used the most probable topic predicted as a feature using LDA. Then, to account for class imbalance, I undersampled the majority classes using the Random Undersampler method from the library, imblearn. Of KNN, Random Forest, SVM, and Logistic Regression, KNN performed the best, with twice the accuracy of random guessing.

## Front-End <a name="frontend"></a>
Ultimately, I pickled the Markov model and the KNN classifier and wrote python modules containing the necessary functions for generating, evaluating, and classifying commencement addresses. I used the modules in the user interface I created using Streamlit, which you can run by navigating into the front-end folder in the terminal, then using the command `streamlit run user-interface.py`. On it you can generate a new commencement paragraph, evaluate the grammar of that paragraph, and classify the sort of speaker that it sounds like. Below are examples of these features:

Generating text:
![Generating text gif](https://github.com/h-parker/commencement-speech-generator/blob/master/readme_images/demo_markov.gif)

Evaluating grammar:
![Evaluating grammar gif](https://github.com/h-parker/commencement-speech-generator/blob/master/readme_images/demo_eval.gif)

Classifying text:
![Classifying text gif](https://github.com/h-parker/commencement-speech-generator/blob/master/readme_images/demo_classify.gif)


## Next Steps <a name="nextsteps"></a>
- Create an LSTM to learn and create new proper POS tag orders in order to evaluate the grammar of evaluated texts.
- Create an RNN to generate new commencement addresses; compare this to the Markov model 
- Host the front-end on a live website
