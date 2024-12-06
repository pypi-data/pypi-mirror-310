def load_conll_data(file_path):
    sentences = []
    sentence = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:  # New sentence
                if sentence:
                    sentences.append(sentence)
                    sentence = []
            else:
                parts = line.split()
                if len(parts) == 4 and parts[0] != "-DOCSTART-":  # Skip DOCSTART
                    word, pos, chunk, ner = parts
                    sentence.append((word, pos, ner))
    return sentences


def word_features(sent, i):
    word = sent[i][0]
    postag = sent[i][1]
    
    features = {
        'word': word.lower(),
        'postag': postag,
        'is_upper': word.isupper(),
        'is_title': word.istitle(),
        'is_digit': word.isdigit(),
    }
    if i > 0:
        prev_word = sent[i-1][0]
        prev_postag = sent[i-1][1]
        features.update({
            '-1:word': prev_word.lower(),
            '-1:postag': prev_postag,
        })
    else:
        features['BOS'] = True  # Beginning of Sentence
    
    if i < len(sent)-1:
        next_word = sent[i+1][0]
        next_postag = sent[i+1][1]
        features.update({
            '+1:word': next_word.lower(),
            '+1:postag': next_postag,
        })
    else:
        features['EOS'] = True  # End of Sentence
    
    return features

from collections import Counter

def extract_entities(words, labels):
    entities = []
    entity = []
    current_label = None

    for word, label in zip(words, labels):
        if label.startswith("B-"):  # Beginning of a new entity
            if entity:
                entities.append((current_label, " ".join(entity)))
            entity = [word]
            current_label = label[2:]
        elif label.startswith("I-") and label[2:] == current_label:  # Continuation of an entity
            entity.append(word)
        else:
            if entity:
                entities.append((current_label, " ".join(entity)))
            entity = []
            current_label = None

    if entity:
        entities.append((current_label, " ".join(entity)))

    return entities


def evaluate_dataset(sentences, y_true, y_pred):
    results = {"PER": Counter(), "LOC": Counter(), "ORG": Counter()}
    for sentence, true_labels, pred_labels in zip(sentences, y_true, y_pred):
        words = [token[0] for token in sentence]
        true_entities = extract_entities(words, true_labels)
        pred_entities = extract_entities(words, pred_labels)

        for entity_type, entity in true_entities:
            if entity_type in results:
                if entity in [e[1] for e in pred_entities if e[0] == entity_type]:
                    results[entity_type]["correct"] += 1
                else:
                    results[entity_type]["missed"] += 1

        for entity_type, entity in pred_entities:
            if entity_type in results:
                if entity not in [e[1] for e in true_entities if e[0] == entity_type]:
                    results[entity_type]["false_positive"] += 1

    return results