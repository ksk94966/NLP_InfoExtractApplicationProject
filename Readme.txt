To run task1.py:
Language used : Python

Libraries required and instructions:
pip install nltk
pip install spacy
import nltk
nltk.download('punkt')

task2.py, task2part.py, task2work.py and task2buy.py contains the parse functions which are rule-based patterns to extract templates.

task3.py uses above models to get templates when a new input file is given and outputs templates in filename.json.

To run task3.py:
Language used : Python

Libraries required and instructions:
pip install spacy
import nltk
nltk.download('punkt')
To install neuralcoref
	!git clone https://github.com/huggingface/neuralcoref.git
pip install -r requirements.txt
pip install -e .

python -m spacy download en_core_web_sm
pip install spacy-lookup
pip install pandas	

Files Required
titles.csv should be in same folder as task3.py
input file name should be given inside task3.py
	 
