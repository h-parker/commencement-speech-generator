import streamlit as st
import pandas as pd
import numpy as np
import project_functions

def main():
	# Render the readme as markdown using st.markdown.
	with open('opening.md', 'r') as f: 
		opening = f.read() 

	readme_text = st.markdown(opening)

	# add a selector for the app mode on the sidebar.
	st.sidebar.title("What would you like to do?")
	app_mode = st.sidebar.selectbox("Choose what you'd like to do:", 
		['Read about this project', "Generate text - Markov Model", 
		 "Classify the type of speaker", "Evaluate text"])

	if app_mode == "Read about this project":
		st.sidebar.success("""To explore this project, select any 
			option in the dropdown menu.""")

	elif app_mode == "Generate text - Markov Model":
		readme_text.empty()
		with st.spinner('Getting a new speech ready...'):
			markov_text_label = """How many sentences would you like to generate?"""
			text = st.text_input(markov_text_label, value=int('3'))
			generated = project_functions.run_markov(int(text))
			st.success('Got it!')		
		st.write(generated)

	elif app_mode == "Classify the type of speaker":
		with st.spinner('Getting your prediction...'):
			readme_text.empty()
			classify_text_label = """Enter the speech you'd like to classify the speaker-type of."""
			text = st.text_area(classify_text_label, value="""I am the president of the United States.""")
			prediction = project_functions.run_predict(text)[0]

			# 'business person' reads better, event thought "business" was the label.
			if prediction == 'business':
				prediction = 'business person'
				print(prediction)
			st.success('Got the prediction!')
		st.write('The speaker seems like a(n)', prediction, '.')
		

	elif app_mode == "Evaluate text":
		readme_text.empty()
		with st.spinner('Evaluating the text...'):
			eval_text_label = "Enter the text you want to evaluate."
			text = st.text_area(eval_text_label, value="""These sentences are correct. They have a score of 1.""")
			# generated = project_functions.run_markov()
			score = project_functions.grammar_score(text)
			st.success('Got it!')
		st.write('The score is:', score)

if __name__ == "__main__":
	main()