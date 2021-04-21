from flask import Flask,render_template,request,redirect,url_for
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
nltk.download('stopwords')
import pickle
app = Flask(__name__)
@app.route('/',methods=['POST','GET'])
def hello_world():
	if(request.method=='POST'):
		text=str(request.form['message'])
		with open("model.pkl",'rb') as file:
			model = pickle.load(file)
		with open('get_feature_name.pkl', 'rb') as f:
			t=pickle.load(f)
		cor=[]
		cor.append(' '.join([word.lower() for word in text.split()]))
		alpha_cor=[]
		for i in range(len(cor)):
		   alpha_cor.append(' '.join([word for word in cor[i].split() if word.isalpha()]))
		remove_stop=[]
		for i in range(len(alpha_cor)):
		   remove_stop.append(' '.join([word for word in alpha_cor[i].split() if word not in stopwords.words('english')]))
		Stemed_cor=[]
		
		ps=PorterStemmer()
		for i in range(len(remove_stop)):
		  Stemed_cor.append(' '.join([ps.stem(word) for word in remove_stop[i].split()]))
		a1=np.zeros((1,9414))
		a1.shape
		d1=pd.DataFrame(a1,columns=t)
		for i in Stemed_cor[0].split():
		  if i in t:
		    d1[i][0]=d1[i][0]+1.0
		pred=model.predict(d1)
		s1=""
		if(pred==1):

		  s1="The Customer is very happy "

		elif(pred==0):
		  s1="The Customer is Satisfied"

		else:
		  s1="The Customer does not like it"
		print(s1)
		return render_template('predict.html',value=s1)



	return render_template('index.html')
# @app.route('/predict/')
# def fun():
# 	return render_template('predict.html',value=s1)
if __name__ == '__main__':
  app.run(debug=True)
