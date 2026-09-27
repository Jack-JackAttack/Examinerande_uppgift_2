# Named Entity Recognition med spaCy

## Vad projektet gör

Projektet undersöker hur spaCy kan användas för att identifiera namngivna entiteter i svensk text, t.ex. personer, organisationer och platser.

I notebooken jämförs de svenska modellerna small, medium och large. Modellerna testas på egna meningar och på ett utdrag från ett pressmeddelande. Medium-modellen finjusteras även med egen träningsdata för att undersöka om den kan bli bättre på att känna igen företagsnamn som organisationer.

## Installation och bibliotek

För att köra projektet behövs Python samt följande paket:

- spaCy
- pandas

Paketen spaCy och pandas kan installeras med:

```text
pip install spacy pandas
```

De svenska spaCy-modellerna installeras med:

```text
python -m spacy download sv_core_news_sm
python -m spacy download sv_core_news_md
python -m spacy download sv_core_news_lg
```

Om notebooken öppnas i VS Code behövs även Jupyter läggas till.

## Så körs projektet

Öppna filen ``ner_analysis.ipynb``. Välj en Pythonmiljö där biblioteken är installerade och kör sedan cellerna uppifrån och ned.

När träningsdelen körs sparas den finjusterade modellen i mappen ``custom_ner_model``. Modellen laddas sedan in igen i notebooken för att jämföras med originalmodellen.

## Filer och data

- ``ner_analysis.ipynb`` innehåller testerna, modelljämförelsen och finjusteringen.
- ``src/utils.py`` innehåller funktioner som används för att hitta entiteter och jämföra modeller.
- ``data/volvo_pressmeddelande.txt`` innehåller texten som används i testet med en verklig text.
- ``custom_ner_model`` skapas när träningsdelen körs och innehåller den sparade finjusterade modellen.

Texten i ``volvo_pressmeddelande.txt`` kommer från ett pressmeddelande från Volvo Cars:

https://www.volvocars.com/se/media/press-releases/CA90C6F155FAEA0A/