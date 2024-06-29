# df = pd.read_csv(filepath_or_buffer="./csv_files/df_spojeni.csv")
# df=df.drop([3559])
# df = pd.read_pickle(filepath_or_buffer="./pickle_files/df_odvojeni.pkl")
# df = df.reset_index().drop('index', axis=1)

# freq_comm = pd.Series(' '.join(df['posts'].tolist()).split()).value_counts()
# f20= freq_comm[:1]

# rare= freq_comm[freq_comm.values==1]

# df['posts'] = df['posts'].apply(lambda x: ' '.join([t for t in x.split() if t not in f20]))
# df['posts'] = df['posts'].apply(lambda x: ' '.join([t for t in x.split() if t not in rare]))

########## spojeni_NN_RECENICE_VEKTORI ########## 

# %time
# #do the nlp word2vec with spaCy

# def word2vec(posts):
#   docs = nlp(posts)
#   return docs.vector

# #for the dataframe:
# df['vectors'] = df['posts'].apply(lambda x: word2vec(x))
# df

#################################################

############ odvojeni_NN_RECI_VEKTORI ########### 

# %time
# #do the nlp word2vec with spaCy

# def word2vec(posts):
#   vecList = []
#   docs = nlp(posts)
#   for doc in docs:
#     vecList.append(doc.vector)
#   return np.array(vecList)

# #for the dataframe:
# df['vectors'] = df['posts'].apply(lambda x: word2vec(x))
# df

#################################################

############# spojeni_NN_RECI_VEKTORI ########### 

# %time
# #do the nlp word2vec with spaCy

# def word2vec(posts):
#   vecList = []
#   docs = nlp(posts)
#   for doc in docs:
#     vecList.append(doc.vector)
#   return np.array(vecList)

# #for the dataframe:
# df['vectors'] = df['posts'].apply(lambda x: word2vec(x))
# df

#################################################