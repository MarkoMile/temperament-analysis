from sklearn.preprocessing import OneHotEncoder

enc = OneHotEncoder()
X = [['male', 'from US', 'uses Safari','female', 'that is', 'from Europe', 'uses Firefox']]
enc.fit(X)
print(enc.transform([['female', 'from US', 'uses Safari'],['male', 'from Europe', 'uses Safari']]).toarray())