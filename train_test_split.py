import pandas as pd
import csv
from config import DATA_DIR,DATA_NAME
from sklearn.model_selection import train_test_split
from pathlib import Path

df = pd.read_csv(str(DATA_DIR) + "/" + DATA_NAME)
df['label'] = df['label'].apply(lambda x:'__label__' + str(x))


X_train, X_test, y_train, y_test = train_test_split(df['tweet'].values.tolist(),
                                                    df['label'].values.tolist(),
                                                    test_size = 0.2,
                                                    random_state=42)

train_df = pd.DataFrame({'tweet':X_train,'label':y_train})
test_df = pd.DataFrame({'tweet':X_test,'label':y_test})


train_df[['label', 'tweet']].to_csv(Path(DATA_DIR,'train.txt'),
                                     index = False,
                                     sep = ' ',
                                     header = None,
                                     quoting = csv.QUOTE_NONE,
                                     quotechar = "",
                                     escapechar = " ")

test_df[['label', 'tweet']].to_csv(Path(DATA_DIR,'test.txt'),
                                     index = False,
                                     sep = ' ',
                                     header = None,
                                     quoting = csv.QUOTE_NONE,
                                     quotechar = "",
                                     escapechar = " ")
