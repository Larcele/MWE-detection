import numpy as np
from sklearn import svm
from sklearn.preprocessing import MinMaxScaler

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV

from sklearn.metrics import classification_report

import settings as st
import io

''' Provided a .vec file of fastText word vector models, constructs a dictionary of words;
 	each word key paired to a corresponding vector representation (array of floats)'''
def load_vectors(fname):
    fin = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
    n, d = map(int, fin.readline().split())
    data = {}
    for line in fin:
        tokens = line.rstrip().split(' ')
        data[tokens[0]] = [float(i) for i in tokens[1:]]
    return data


''' Based on supplied 'lang' string sets all the needed model/data set variables which will be used in training '''
def get_final_dataset(lang):

	trainfile = ""
	testfile = ""
	modelfile = ""
	if lang == "EN":
		trainfile = st.NEW_FNAME_EN
		testfile = st.TEST_NEW_FNAME_EN
		modelfile = st.BIN_EN

	elif lang == "DE":
		trainfile = st.NEW_FNAME_DE
		testfile = st.TEST_NEW_FNAME_DE
		modelfile = st.BIN_DE

	elif lang == "PL":
		trainfile = st.NEW_FNAME_PL
		testfile = st.TEST_NEW_FNAME_PL
		modelfile = st.BIN_PL

	elif lang == "SL":
		trainfile = st.NEW_FNAME_SL
		testfile = st.TEST_NEW_FNAME_SL
		modelfile = st.BIN_SL

	else:
		raise Exception("Unknown language string")

	model = load_vectors(modelfile)
	X_train, Y_train, vmwe_types = parse_dset(model, trainfile)
	X_test, Y_test, vmwe_types = parse_dset(model, testfile, vmwe_types, False)

	return X_train, Y_train, X_test, Y_test, vmwe_types

''' Translates the data set into number representations. 
	Returns the input set (numpy array), target set (array), and mwe category types (set) '''
def parse_dset(model, trainfile, vmwes=["*"], shouldAppend=True):
	#vmwes = []#"VID", "LVC.full", "LVC.cause", "VPC.full", "VPC.semi", "IAV", "MVC", ]

	#second column of the train file; word labels
	filelines = open(trainfile, encoding='utf-8').read().split('\n')
	print("file- first line (sanity check): {0}".format(filelines[0]))
	print("file- second line (sanity check): {0}".format(filelines[1]))

	#Raw text only; will be used when reconstructing the input, later
	words = [line.split(st.DELIM)[0] for line in filelines if len(line) > 1]

	#filer only the second column, skip empty lines
	col = [line.split(st.DELIM)[1] for line in filelines if len(line) > 1]

	#filter only the third column; get the MWE annotations.
	mwesigns = [line.split(st.DELIM)[2] for line in filelines if len(line) > 1]


	#wordtypes parse
	types_lst = list(set(col))
	wts = [types_lst.index(item) for item in col]

	wordtypes = indices_to_one_hot(wts, len(types_lst))
	#print("final wordtypes: {0}".format(wordtypes))

	#Labels (mwesigns) parse
	#The annotations are translated as follows: when number:MWE is encountered,
	#the number is discarded and only the tag is preserved. When the continued MWE
	#is encountered (-> the number which was discarded), the last seen MWE tag will be 
	#added except of that.

	annots = []
	for item in mwesigns:
		
		if ":" in item:
			n = item.split(":")
			#add only the MWE tag
			mwe = ""
			if ';' in n[1]: #in case of multiple labeling, just take into consideration only the first one
				mwe = n[1].split(";")[0] #for now; might try to change this later
			else: 
				mwe = n[1]

			#check if the label was seen already; if not, add it first
			if not mwe in vmwes:
				if shouldAppend:#unless this is the test set and never saw this MWE
					vmwes.append(mwe)
					print("Adding new tag: {0}".format(mwe))
				else:
					annots.append(0)
					continue
			annots.append(vmwes.index(mwe))

		elif item == "*":
			annots.append(vmwes.index(item))

		else:
			#this is a MWE continuation; append the same MWE sign as the last one seen
			annots.append(annots[len(annots)-1])

	print("final vmwe list: {0}".format(vmwes))

	#reconstruct the word input
	w = []
	for word in words:
		try:
			arr = np.array(list(model[word]))
			if len(arr) == 0:
				raise Exception("nope")

			#print("Adding array: {0}".format(arr))
			w.append(arr)#.get_word_vector(word))
		except:
			#print("ERROR: {0} does not exist".format(word))
			arr = np.array([0 for i in range(300)])
			#print("Adding Empty: {0}".format(arr))
			w.append(arr)#model.get_dimension()) ])

	big_np_array = np.array(w)
	print("Created word representation: {}".format(big_np_array))
	print(big_np_array.shape)
	print(wordtypes.shape)
	final_output = np.concatenate((big_np_array, wordtypes), axis=1)

	#print("This should be the new line/vector")
	#print(final_output[0])

	return big_np_array, annots, vmwes



''' Convert an iterable of indices to one-hot encoded labels. '''
def indices_to_one_hot(data, nb_classes):
	
	#print("DATA is : {0}".format(data))
	#print("CLASSES are : {0}".format(nb_classes))
	targets = np.array(data).reshape(-1)
	return np.eye(nb_classes)[targets]


def trainSVM(X_train, Y_train, X_test, Y_test, labels):

	c, g = select_best_params(X_train, Y_train)
	
	print("Initializing SVC with best params.")
	clf = svm.SVC(gamma=g, C=c, cache_size=2000, max_iter=300, kernel='rbf')
	print("SVC training in progress...")
	clf.fit(X_train, Y_train)

	print("Calculating predictions...")

	# Make predictions on unseen test data
	y_predict = clf.predict(X_test)

	print("Training Accuracy: {}%".format(clf.score(X_train, Y_train) * 100 ))
	print("Test Accuracy: {}%".format(clf.score(X_test, Y_test) * 100 ))

	score_train = accuracy_score(y_train, clf.predict(x_train))
	score_test = accuracy_score(y_valid, y_predict)
	print("Training Accuracy: {}%".format(score_train * 100) )
	print("Test Accuracyy: {}%".format(score_test * 100) )

	
	print (classification_report(Y_test, y_predict, target_names=labels))



def trainRFC(X_train, Y_train, X_test, Y_test, labels):

	print("Initializing RFC.")
	model = RandomForestClassifier(n_estimators=200, max_features=10)
	print("RFC training in progress...")
	model.fit(X_train, Y_train)
	print("Calculating predictions...")

	y_predict = model.predict(X_test)
	print("Training Accuracy: {}%".format(accuracy_score(Y_train, model.predict(X_train)) * 100 ))
	print("Test Accuracyy: {}%".format(accuracy_score(Y_test, y_predict) * 100))

	print (classification_report(Y_test, y_predict, target_names=labels))


''' Performs SVM training for various parameters, on the split of a training set. 
	Returns the parameters with which best accuracy was achieved'''
def select_best_params(X_train, Y_train):
	best_score = 0
	G, C = 0, 0

	#split the training dataset
	split = int(len(X_train) * 0.8)

	x_train = X_train[:split]
	y_train = Y_train[:split]

	x_valid = X_train[split:]
	y_valid = Y_train[split:]

	param_grid = {'C': [10,50,100], 'gamma': [0.1, 0.01, 0.001]}

	print("[SVM] Best parameter selection out of params gamma={0}, C={1}".format(param_grid['gamma'], param_grid['C']))

	for c in param_grid['C']:
		for g in param_grid['gamma']:
			print("Training SVM on gamma={0}, C={1}".format(g, c))
			clf = svm.SVC(gamma=g, C=c, cache_size=2000, max_iter=50, kernel='rbf')

			print("SVC training in progress...")
			clf.fit(x_train, y_train)

			print("Calculating predictions...")

			# Make predictions on unseen test data
			y_predict = clf.predict(x_valid)

			score_train = accuracy_score(y_train, clf.predict(x_train))
			score_test = accuracy_score(y_valid, y_predict)
			print("Training Accuracy: {}%".format(score_train * 100) )
			print("Test Accuracyy: {}%".format(score_test * 100) )

			if best_score < score_test:
				best_score = score_test
				C = c
				G = g


	return C, G

	
#prepare the datasets format in which it will be fed to the classifiers
print("Training start. Creating final dataset...")
X_train, Y_train, X_test, Y_test, labels = get_final_dataset("PL") #Change the label here depending on deired language,
#provided there are all the files and variables set up.

#SVM
trainSVM(X_train, Y_train, X_test, Y_test, labels)


#RANDOM FOREST
trainRFC(X_train, Y_train, X_test, Y_test, labels)