from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
import uvicorn
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from pydantic import BaseModel, Field, validator

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Télécharger les stopwords
nltk.download('stopwords')

# Initialiser le stemmer et les stop words
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Charger le modèle et le tokenizer depuis les fichiers
model_path = 'E:/Document/WorkSpace/Formation/Project5-API/my_model_trans_1/checkpoint-5470'

# Charger le modèle
model = BertForSequenceClassification.from_pretrained(model_path)
tokenizer = BertTokenizer.from_pretrained(model_path)

id2label = model.config.id2label

# Définir la fonction de prétraitement
def preprocess_text(text):
    tokens = text.split()
    tokens = [stemmer.stem(token) for token in tokens if token.lower() not in stop_words]
    return ' '.join(tokens)

# Définir la fonction de prédiction multi-label
def predict(texts, threshold=0.2):
    # Appliquer le prétraitement
    print(texts)
    processed_texts = [preprocess_text(text) for text in texts]
    # Tokenizer les entrées
    print(processed_texts)
    inputs = tokenizer(processed_texts, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    # Appliquer la fonction sigmoïde pour obtenir les probabilités
    probabilities = torch.sigmoid(outputs.logits).cpu().numpy()
    # Convertir les probabilités en labels
    predictions = []
    for probs in probabilities:
        labels = [id2label[idx] for idx, prob in enumerate(probs) if prob > threshold]
        predictions.append(labels)
    print(predictions)
    return predictions

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})

@app.get('/favicon.ico')
async def favicon():
    file_name = 'favicon.ico'
    file_path = './static/' + file_name
    return FileResponse(path=file_path, headers={'mimetype': 'image/vnd.microsoft.icon'})

@app.get('/hello', response_class=HTMLResponse)
async def hello(request: Request, title: str = Query(...)):
    return templates.TemplateResponse('hello.html', {"request": request, 'title': title})

# Définir la fonction de prédiction pour un titre (single label)
def get_tags_api(title: str, threshold: float = 0.4):
    predictions = predict([title], threshold)
    return predictions[0]

# Définir un modèle de données pour les requêtes
class TitleRequest(BaseModel):
    title: str
    threshold: float = Field(default=0.4, ge=0, le=1)

    @validator('title')
    def validate_title(cls, v):
        if not v or v.strip() == "":
            raise ValueError('Le titre ne peut pas être vide.')
        return v

    @validator('threshold')
    def validate_threshold(cls, v):
        if not (0 <= v <= 1):
            raise ValueError('Le seuil doit être compris entre 0 et 1.')
        return v

# Définir le point de terminaison pour les prédictions de titre
@app.post("/get_tags_api")
async def get_tags_api_endpoint(request: TitleRequest):
    print("CALLING ===================================> get_tags_api")
    print(request.title)
    title = request.title
    threshold = request.threshold
    tags = get_tags_api(title, threshold)
    return {"tags": tags}

@app.get("/get_tags", response_class=HTMLResponse)
async def get_tags(request: Request, title: str = Query(...)):
    predictions = predict([title])
    return templates.TemplateResponse('hello.html', {"request": request, "predictions": predictions[0], 'title': title})

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000)
