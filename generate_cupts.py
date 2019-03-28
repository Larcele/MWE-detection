import settings as st

iFnames_train = [st.FNAME_EN, st.FNAME_DE, st.FNAME_PL, st.FNAME_SL]
oFnames_train = [st.NEW_FNAME_EN, st.NEW_FNAME_DE, st.NEW_FNAME_PL, st.NEW_FNAME_SL]

iFnames_test = [st.TEST_FNAME_EN, st.TEST_FNAME_DE, st.TEST_FNAME_PL, st.TEST_FNAME_SL]
oFnames_test = [st.TEST_NEW_FNAME_EN, st.TEST_NEW_FNAME_DE, st.TEST_NEW_FNAME_PL, st.TEST_NEW_FNAME_SL]

def get_lang(string):
	if "_" in string:
		return string.split("_")[1]
	else: return "<unknown>"

''' Filters out specific attributes (columns) from the original .cupt file and creates a new .cupt file with these columns  '''
def generate_cupt_file(iFname, oFname):
	print("Creating new .cupt file for {0}...".format(get_lang(iFname)))

	output = [] #output lines; new structure of the dataset file

	try:
		file = open(iFname, encoding='utf-8')
		for line in file:
			if len(line) > 1:
				if line[0] == "#": #is a comment
					continue


				snip = line.split(st.DELIM)

				#snip here has the structure of the .cupt file from PARSEME task, namely:
				#global.columns = ID FORM LEMMA UPOS XPOS FEATS HEAD DEPREL DEPS MISC PARSEME:MWE
				#example: ['1', 'When', 'when', 'SCONJ', '_', '_', '3', 'mark', '_', '_', '*\n']

				data = snip[1] + st.DELIM + snip[3] + st.DELIM + snip[len(snip)-1]
				output.append(data)
				#raw_sentences.append(snip[1])

	except:
		print("ERROR while parsing file")

	finally:
		#write output to file
		newFile = open(oFname, 'w')
		for d in output:
			newFile.write(d)

		newFile.close()
		file.close()

		print("File generating successfull.")

''' generates .cupt files of multiple files merged into one. '''
def generate_mixed_cupts(file1, file2, train=True):
	try:
		print("Creating new .cupt file for {0}, {1}...".format(get_lang(file1), get_lang(file2)))

		f1 = open(file1, encoding='utf-8').read()
		f2 = open(file2, encoding='utf-8').read()

		tt = "train" if train else "test"
		fname = "{0}_{1}_{2}.cupt".format(tt, get_lang(file1), get_lang(file2))
		newFile = open(fname, 'w')
		newFile.write(f1)
		newFile.write(f2)

		newFile.close()

		print("Creation successfull.")

	except:
		print("ERROR while combining .cupt files {0}, {1}".format(file1,file2))


#generate train files
for i in range(len(iFnames_train)):
	generate_cupt_file(iFnames_train[i], oFnames_train[i])

generate_mixed_cupts(st.NEW_FNAME_EN, st.NEW_FNAME_DE)
generate_mixed_cupts(st.NEW_FNAME_SL, st.NEW_FNAME_PL)

#generate test files
for i in range(len(iFnames_test)):
	generate_cupt_file(iFnames_test[i], oFnames_test[i])

generate_mixed_cupts(st.TEST_NEW_FNAME_EN, st.TEST_NEW_FNAME_DE, False)
generate_mixed_cupts(st.TEST_NEW_FNAME_SL, st.TEST_NEW_FNAME_PL, False)