# Evaluating Generated Text
There's been work done to evaluate machine translations of text, but dramatically less (read: none that I can find!) done on the evaluation of generated text in general. If you have nothing to compare your generated text to (for example, comparing the machine translation to human translation), literature is pretty much silent on how to decide if your text is any good, besides just comparing random samples by hand, and deciding yourself. Note: This project seeks to address this issue using a Context Free Grammar to score generated text. Since CFGs are meant to be used with formal languages, and English is not a formal language, this is really only an approximation/first guess at a good scoring mechanism. It was an attempt to see how far I could get in evaluating generated text in roughly 3 days! Better versions to come :)

## Evaluating the Evaluation Metric
In order to understand the usefulness (or not so usefulness!) of this evaluation metric, I created a Markov model that generate commencement speech snippets. This model is known to be only  so-so in generating data, since it only 'remembers' the last word it produced. Nevertheless, with quality data, it can come up with interesting results! 

### To get started, click the menu button on the upper left-hand corner to choose what you'd like to do! Or, continue reading to explore an analysis of the data. 

## 