import time
import json
import nltk
import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification
from flask import Flask, request, Response

nltk.download('punkt')

app = Flask(__name__)

MODEL_NAME = "CyberPeace-Institute/SecureBERT-NER"
MAX_CONTENT_LENGTH = 1048576  # 1MB in bytes

# Inititalize tokenizer and model
secure_bert_ner_tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path=MODEL_NAME)
secure_bert_ner_model = AutoModelForTokenClassification.from_pretrained(MODEL_NAME)


def get_predictions(model, tokenizer, text):
    """
    Get SecureBERT-NER model predictions for given text

    model (RobertaForTokenClassification pre trained on SecureBERT-NER model): SecureBERT-NER model
    tokenizer (RobertaTokenizer pre trained on SecureBERT-NER model): Text tokenizer
    text (str): Text to be tokenized in the form of a long single string.

    returns (list): List of normalized predications and model latency
    """
    inputs = tokenize_data(text, tokenizer)

    start_time = time.time()
    with torch.no_grad():
        outputs = model(**inputs)
    end_time = time.time()
    latency = end_time - start_time
    print(f'SecureBERT-NER model predictions latency: {latency}')

    # Convert predictions to label strings:
    predictions = []
    for i, sentence in enumerate(nltk.sent_tokenize(text)):
        tokens = tokenizer.convert_ids_to_tokens(inputs.input_ids[i])
        preds = outputs.logits[i].argmax(dim=-1)

        sentence = []
        for j, token in enumerate(tokens):
            if token in ['<s>', '</s>', '<pad>']:
                continue
            entity_label = model.config.id2label[preds[j].item()]
            sentence.append({'word': token, 'entity': entity_label})
        predictions.append(sentence)

    return predictions, latency


def tokenize_data(text: str, tokenizer):
    """
    Tokenize and prepare inputs for the model

    text (str): Text to be tokenized in the form of a long single string.
    tokenizer (RobertaTokenizer pre trained on SecureBERT-NER model): Text tokenizer

    returns (transformers.tokenization_utils_base.BatchEncoding): Tokenized inputs for SecureBERT-NER model
    """

    # Convert text to list of sentences
    input_sentences = nltk.sent_tokenize(text)

    inputs = tokenizer(input_sentences,
                       return_tensors="pt",
                       padding=True,
                       truncation=True
                       )

    return inputs


def remove_g_char(preds):
    """
    Remove Ġ character from predictions for improved readability
    
    preds (list): SecureBERT-NER model predictions
    
    returns (list): Normalized SecureBERT-NER model predictions (without the Ġ char)
    """
    normalized_preds = []
    for sent in preds:
        norm_sent = [{"word": pred["word"].replace('Ġ', ' ').strip(),
                      "entity": pred["entity"]} for pred in sent]
        normalized_preds.append(norm_sent)

    return normalized_preds


@app.route('/ner', methods=['POST'])
def predict_ner_classes():
    try:
        # Check for large text
        if request.content_length > MAX_CONTENT_LENGTH:
            response = Response(json.dumps({"error": "Payload to large: Text size exceeds limit (1MB)",
                                            "error_code": 413,
                                            "Content-Type": "application/json"}))
            return response

        data = request.json
        text = data.get('text', '')

        # Check for missing text
        if not text:
            response = Response(json.dumps({"error": "Bad Request: No text provided",
                                            "error_code": 400,
                                            "Content-Type": "application/json"}))
            return response

        predictions, latency = get_predictions(model=secure_bert_ner_model,
                                               tokenizer=secure_bert_ner_tokenizer,
                                               text=text)

        # Remove 'Ġ' character
        normalized_preds = remove_g_char(predictions)

        response = Response(json.dumps({"predictions": normalized_preds,
                                        "latency": latency,
                                        "Content-Type": "application/json"}))
    except Exception as e:
        # Unexpected error
        return Response(json.dumps({"error": str(e),
                                    "error_code": 500,
                                    "Content-Type": "application/json"}))

    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
