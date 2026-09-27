def find_entities(text, model):
    doc = model(text)

    result = []

    for ent in doc.ents:
        result.append({
            "Entity": ent.text,
            "Label": ent.label_
        })

    return result



def compare_models(text, models):
    result = []

    for name, model in models:
        doc = model(text)

        for ent in doc.ents:
            result.append({
                "Model": name,
                "Entity": ent.text,
                "Label": ent.label_
            })

    return result