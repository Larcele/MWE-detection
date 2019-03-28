import settings as st

iFnames = [st.FNAME_EN, st.FNAME_DE, st.FNAME_PL, st.FNAME_SL]
oFnames = [st.RAW_FNAME_EN, st.RAW_FNAME_DE, st.RAW_FNAME_PL, st.RAW_FNAME_SL]

''' Extracts only raw text sentences form the .cupt file '''
def generate_RAWS(iFname, oFname):
	raw_sentences = [] 
	try:
		file = open(iFname, encoding='utf-8')

		for line in file:
			if len(line) > 1:
				if line[0] == "#": #is a comment
					if "text =" in line:
						index = line.find("=")
						raw_sentences.append(line[index+1:])
					continue

	finally:
		string = ''.join(raw_sentences)

		#write the raw text to separate file
		rawFile = open(oFname, 'w')
		for d in raw_sentences:
			rawFile.write(d)

		rawFile.close()

		print("Raw file created successfully.")


#generate train files
for i in range(len(iFnames)):
	generate_RAWS(iFnames[i], oFnames[i])
