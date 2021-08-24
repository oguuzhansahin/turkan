from pathlib import Path

PROJECT_DIR = Path(__file__).parent
DATA_DIR    = Path(PROJECT_DIR,"soru_cumlesi_classifier","data")
RESULT_DIR  = Path(PROJECT_DIR,"soru_cumlesi_classifier","results")
MODEL_DIR   = Path(RESULT_DIR,"soru_cumlesi_classifier","model")
DATA_NAME = "sorucümlesi.csv"

hyperparameters = {'input':"soru_cumlesi_classifier/data/train.txt",
                   'epoch':100,
                   'dim':50,
                   'wordNgrams':2}