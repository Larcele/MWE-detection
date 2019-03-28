import settings as st
import word2vec

def generate_cupt_file(iFname, oFname):
	output = [] #output lines; new structure of the dataset file
	raw_sentences = [] #only the words; this will be passed to word2vec

	try:
		file = open(iFname, encoding='utf-8')

		for line in file:

			if len(line) > 1:

				if line[0] == "#": #is a comment
					if "text =" in line:
						index = line.find("=")
						raw_sentences.append(line[index+1:])
					continue


				snip = line.split(st.DELIM)

				#snip here has the structure of the .cupt file from PARSEME task, namely:
				#global.columns = ID FORM LEMMA UPOS XPOS FEATS HEAD DEPREL DEPS MISC PARSEME:MWE
				#example: ['1', 'When', 'when', 'SCONJ', '_', '_', '3', 'mark', '_', '_', '*\n']

				data = snip[1] + st.DELIM + snip[3] + st.DELIM + snip[len(snip)-1]
				output.append(data)
				#raw_sentences.append(snip[1])

	except:
		print("ERROR")
	finally:
		#write output to file
		newFile = open(oFname, 'w')
		for d in output:
			newFile.write(d)

		newFile.close()
		file.close()


		print("File generating successfull. Creating raw text file...")

		string = ''.join(raw_sentences)

		#write the raw text to separate file
		rawFile = open(st.RAW_FNAME, 'w')
		for d in raw_sentences:
			rawFile.write(d)

		rawFile.close()

		print("Raw file created successfully.")

def generate_w2vbin(words):

	print("Creating word2vec model...")
	word2vec.word2vec(words, st.W2VBIN_EN, size=200, verbose=True)
	print(".bin file with word embeddings created successfully.")



generate_cupt_file(st.FNAME, st.NEW_FNAME)
generate_w2vbin(st.RAW_FNAME)

