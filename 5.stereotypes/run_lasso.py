from sklearn.model_selection import train_test_split
import pandas as pd
pd.set_option('display.max_rows', 500)
import numpy as np
import datetime as dt

import re
import unicodedata
import string
import emoji
import pickle

import nltk
#nltk.download()
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

from sklearn.feature_extraction.text import  TfidfVectorizer, CountVectorizer 
from sklearn.decomposition import NMF

from collections import Counter
from sklearn.linear_model import Lasso, Ridge, LassoCV, RidgeCV, LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold

tweets = pd.read_csv('tweets_for_stm.csv')
tweets = tweets[tweets.target_precision == 'High']
tweets['gender'] = tweets.directed_at_gender.apply(lambda x: 1 if x == 'F' else 0)

names = ['ana',
 'claudia',
 'jose',
 'jorge',
 'roberto',
 'gustavo',
 'ines',
 'imelda',
 'nestor',
 'pedro',
 'olga',
 'ines',
 'esteban',
 'jose',
 'carlos',
 'alberto',
 'oscar',
 'anibal',
 'maria',
 'eugenia',
 'maurice',
 'fabian',
 'julio',
 'cesar',
 'cleto',
 'eduardo',
 'raul',
 'norma',
 'haydee',
 'silvia',
 'beatriz',
 'carlos',
 'mauricio',
 'anabel',
 'mario',
 'raymundo',
 'silvia',
 'del',
 'rosario',
 'gladys',
 'esther',
 'nancy',
 'susana',
 'ana',
 'maria',
 'alfredo',
 'hector',
 'juan',
 'carlos',
 'julio',
 'cesar',
 'carlos',
 'saul',
 'dalmacio',
 'beatriz',
 'graciela',
 'juan',
 'mario',
 'omar',
 'angel',
 'luis',
 'carlos',
 'claudio',
 'javier',
 'carlos',
 'alberto',
 'laura',
 'elena',
 'adolfo',
 'maria',
 'de',
 'los',
 'angeles',
 'humberto',
 'luis',
 'arturo',
 'magdalena',
 'maria',
 'belen',
 'pamela',
 'fernanda',
 'maria',
 'cristina',
 'diego',
 'felipe',
 'domingo',
 'luis',
 'federico',
 'alicia',
 'noemi',
 'alberto',
 'emilio',
 'karina',
 'veronica',
 'luis',
 'eugenio',
 'miguel',
 'angel',
 'martin',
 'antonio',
 'alejandro',
 'daniel',
 'rosana',
 'andrea',
 'maria',
 'cristina',
 'ricardo',
 'alejandro',
 'graciela',
 'mabel',
 'luisa',
 'nilda',
 'mabel',
 'marcelo',
 'pablo',
 'graciela',
 'maria',
 'carlos',
 'daniel',
 'marcos',
 'alfredo',
 'victor',
 'virginia',
 'maria',
 'camila',
 'alvaro',
 'hector',
 'omar',
 'bruno',
 'eduardo',
 'enrique',
 'luis',
 'victoria',
 'analia',
 'soher',
 'gabriela',
 'beatriz',
 'monica',
 'edith',
 'federico',
 'raul',
 'sebastian',
 'ximena',
 'jose',
 'luis',
 'alvaro',
 'gustavo',
 'leonardo',
 'carlos',
 'mario',
 'carlos',
 'ramiro',
 'itai',
 'estela',
 'beatriz',
 'ingrid',
 'maria',
 'de',
 'las',
 'mercedes',
 'luis',
 'alfredo',
 'maximo',
 'carlos',
 'florencia',
 'susana',
 'graciela',
 'andres',
 'jimena',
 'hebe',
 'mario',
 'alberto',
 'aldo',
 'adolfo',
 'gabriela',
 'mabel',
 'silvia',
 'gabriela',
 'ruben',
 'juan',
 'leonor',
 'maria',
 'german',
 'pedro',
 'maria',
 'dolores',
 'maria',
 'rosa',
 'norman',
 'dario',
 'maria',
 'lucila',
 'sergio',
 'tomas',
 'vanesa',
 'laura',
 'maria',
 'carolina',
 'victoria',
 'cecilia',
 'juan',
 'facundo',
 'miguel',
 'mario',
 'raul',
 'jose',
 'carlos',
 'alejandra',
 'del',
 'huerto',
 'claudia',
 'beatriz',
 'paula',
 'andrea',
 'hernan',
 'carlos',
 'ybrhain',
 'maria',
 'lujan',
 'dina',
 'esther',
 'cristian',
 'adrian',
 'jorge',
 'hugo',
 'adriana',
 'noemi',
 'sebastian',
 'nicolas',
 'diego',
 'horacio',
 'alfredo',
 'oscar',
 'carlos',
 'americo',
 'martin',
 'ignacio',
 'mariana',
 'luis',
 'rodolfo',
 'pablo',
 'gabriel',
 'pablo',
 'ignacio',
 'marisa',
 'eduardo',
 'jorge',
 'daniela',
 'luana',
 'mariana',
 'de',
 'jesus',
 'juan',
 'laura',
 'v.',
 'mario',
 'horacio',
 'daniel',
 'fernando',
 'brenda',
 'lis',
 'beatriz',
 'luisa',
 'aida',
 'beatriz',
 'maxima',
 'juan',
 'jose',
 'hector',
 'hernan',
 'sofia',
 'eduardo',
 'segundo',
 'eduardo',
 'maria',
 'gabriela',
 'juan',
 'eduardo',
 'augusto',
 'marcela',
 'albor',
 'angel',
 'antonio',
 'jose',
 'elisa',
 'maria',
 'avelina',
 'ana',
 'carla',
 'maria',
 'soledad',
 'pablo',
 'paulo',
 'leonardo',
 'sandra',
 'daniela',
 'gabriela',
 'luis',
 'gustavo',
 'walter',
 'mayda',
 'nicolas',
 'gonzalo',
 'pedro',
 'antonio',
 'romina',
 'melina',
 'aida',
 'fernando',
 'omar',
 'chafi',
 'ezequiel',
 'carlos',
 'alberto',
 'daniel',
 'danilo',
 'adrian',
 'hector',
 'alicia',
 'gabriel',
 'alberto',
 'alejandro',
 'silvana',
 'micaela',
 'martin',
 'fernando',
 'adolfo',
 'jorge',
 'enrique',
 'luciano',
 'andres',
 'maria',
 'lucila',
 'martin',
 'miguel',
 'juan',
 'manuel',
 'monica',
 'martin',
 'jose',
 'luis',
 'lorena',
 'gladys',
 'martin',
 'nicolas',
 'josefina',
 'gustavo',
 'diego',
 'matias',
 'osmar',
 'antonio',
 'guillermo',
 'tristan',
 'flavia',
 'leopoldo',
 'raul',
 'guido',
 'juan',
 'rosa',
 'rosario',
 'claudia',
 'maria',
 'graciela',
 'paula',
 'mariana',
 'luis',
 'mario',
 'martin',
 'alejandro',
 'elda',
 'luis',
 'alfonso',
 'maria',
 'carla',
 'horacio',
 'carmen',
 'fabio',
 'jose',
 'jose',
 'luis',
 'ariel',
 'estela',
 'mercedes',
 'roxana',
 'nahir',
 'jose',
 'luis',
 'alejandra',
 'jorge',
 'antonio',
 'agustin',
 'oscar',
 'victoria',
 'laura',
 'julio',
 'enrique',
 'roberto',
 'alma',
 'liliana',
 'gisela',
 'david',
 'pablo',
 'daniel',
 'magdalena',
 'vanesa',
 'felipe',
 'carlos',
 'hector',
 'antonio',
 'facundo',
 'alicia',
 'mirta',
 'fernanda',
 'juan',
 'benedicto',
 'alejandra',
 'maria',
 'natalia',
 'soledad',
 'ricardo',
 'hugo',
 'pablo',
 'raul',
 'federico',
 'raul',
 'claudia',
 'andres',
 'lucila',
 'alfredo',
 'maria',
 'ines',
 'juan',
 'carlos',
 'cristina',
 'mauricio',
 'maria',
 'eugenia',
 'alberto',
 'ofelia',
 'horacio',
 'elizabeth',
 'santiago',
 'gines',
 'axel',
 'gabi',
'pau',
'viki',
'paulita',
'cerruti',
'gracielita',
'vicky',
'lila',
'ocana',
'marianita',
'dalessio',
'pauli',
'gabrielita',
'dalesio',
'cerrutti',
'vallejos',
'lospennato',
'ocampo',
'leleta',
'dra',
'alessio',
'marcelito',
'gra',
'donda',
'olivetto',
'viky',
'grace',
'marian',
'gabu',
'zuvic',
'vicki',
'lilita',
'wado',
'rodo',
'marito',
'nico',
'toty',
'fernandito',
'fede',
'wadito',
'mestre',
'noca',
'sergito',
'facundito',
'guille',
'katz',
'massarasa',
'cano',
'hormiga',
'oliveto',
'gaby',
'alperovich',
'mili',
'mily',
'tailhade',
'yamil',
'solano',
'llaryora',
'petri',
'rossi',
'ercolini',
'moreau',
'maders',
'ritondo',
'massita',
'queijeiro',
'ugl',
'laspina',
'longobardi',
'menna',
'masita',
'filmus',
'arroyo',
'iglesias',
'regino',
'üì≤üìª',
'marijuan',
'lastra',
'hormiguita']
# Delete " ' '" in words
def elimina_tildes(cadena):
    s = ''.join((c for c in unicodedata.normalize('NFD',cadena) if unicodedata.category(c) != 'Mn'))
    return s


def custom_tokenizer(text):

    # remove punctuation
    remove_punct = str.maketrans('', '', string.punctuation)
    text = re.sub(r"(?:\@|https?\://|\#)\S+", "", text)
    text = text.translate(remove_punct)

    # remove digits and convert to lower case
    remove_digits = str.maketrans('', '', string.digits)
    text = text.lower().translate(remove_digits)

    # remove 'tildes'
    text = elimina_tildes(text)

    # tokenize
    tokens = word_tokenize(text)

    # remove stop words
    stop_words = stopwords.words('spanish')# + names
    tokens_stop = [y for y in tokens if y not in stop_words]

    return tokens_stop


X = tweets.text
y = tweets.gender

cv = CountVectorizer(tokenizer=custom_tokenizer, min_df = 10)
X = cv.fit_transform(X)#.toarray()
lr_model = LogisticRegression(penalty='l1', solver='liblinear')
lr_model.fit(X,y)

results = pd.DataFrame({"words":cv.get_feature_names(), "coefs":lr_model.coef_[0]}).sort_values(by='coefs')
results.to_csv('lasso_results.csv')
