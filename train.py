import fasttext
import json
import os


from config import (DATA_DIR,
                    RESULT_DIR,
                    MODEL_DIR, 
                    hyperparameters)
from pathlib import Path


model = fasttext.train_supervised(**hyperparameters)

Path(RESULT_DIR,"model").mkdir(parents=True, exist_ok=True)

model.save_model('soru_cumlesi_classifier/results/model/sentence.model.bin')

with open(str(Path(RESULT_DIR,'params.json')),"w",encoding="utf-8") as file:

        file.write(json.dumps(hyperparameters))

Path(RESULT_DIR,"score").mkdir(parents=True,exist_ok=True)      
with open(Path(f'{RESULT_DIR}/score/fasttext_score.txt'),"w",encoding="utf-8") as file:
        score = str(model.test("soru_cumlesi_classifier/data/test.txt"))
        print(score)
        file.write(score)


with Path(DATA_DIR,"test.txt").open(encoding=("utf-8")) as f, Path(RESULT_DIR,"score","preds.txt").open('w') as fw:
       for i, line in enumerate(f, 1):
           gold = line.strip().split()[0].lstrip('__label__')
           doc = ' '.join(line.strip().split()[1:])
           pred_info = model.predict(doc)
           pred = pred_info[0][0].lstrip('__label__')

           fw.write(' '. join([str(i), gold, pred]) + '\n')
           
os.system(f"python scripts/stats.py {RESULT_DIR}/score/preds.txt > {RESULT_DIR}/score/preds.stats.csv")