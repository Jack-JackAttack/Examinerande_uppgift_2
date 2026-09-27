## Syfte

Syftet med arbetet var att undersöka hur biblioteket spaCy kan användas för att identifiera namngivna entiteter i svensk text. Jag fokuserade på hur modellen känner igen personer, organisationer och platser med fokus på företagsnamn.

Jag ville även undersöka om det fanns skillnader mellan spaCys svenska small, medium och large-modeller. Därefter ville jag testa om medium-modellen kunde bli bättre på att
känna igen vissa organisationer genom att finjustera med en mindre mängd egen träningsdata.

Arbetet avgränsades till Named Entity Recognition. Jag fokuserade därför på hur spaCys svenska modeller identifierar och klassificerar personer, organisationer och platser i text.


## Området och dess relevans

Området jag valde är Natural Language Processing (NLP) med fokus på Named Entity Recognition (NER). NLP handlar om hur datorer kan förstå och jobba med mänskligt språk.
Named Entity Recognition är en del av NLP som används för att hitta och klassificera namngivna entiteter i text t.ex. personer, organisationer och platser.

Om ett företag har stora mängder nyhetsartiklar, pressmeddelanden eller andra texter skulle det ta lång tid att läsa allt manuellt. Med NER kan ett program automatiskt hitta vilka företag, personer och platser som nämns. Resultaten kan sedan sparas som data i en tabell och användas för analys.

I det här projektet används ett pressmeddelande från Volvo Cars som exempel. Modellerna försöker identifiera t.ex. Volvo, Trafikverket, Erik Coelingh och Göteborg.
Entiteterna kan sedan samlas i en DataFrame vilket gör det enklare att jämföra modellernas resultat. På samma sätt skulle NER kunna användas på många texter för att undersöka vilka organisationer som nämns eller vilka personer som förekommer i texten.

Detta är relevant för en data scientist eftersom text ofta behöver omvandlas till ett mer strukturerat format innan den kan analyseras. Det är dock viktigt att kontrollera modellens resultat eftersom den kan klassificera entiteter fel.


## Viktiga begrepp

spaCy är ett pythonbibliotek för NLP. Biblioteket innehåller färdigtränade språkmodeller som kan användas för att analysera text. I det här projektet använder jag spaCys
svenska modeller ``sv_core_news_sm``, ``sv_core_news_md`` och ``sv_core_news_lg``. Förkortningarna ``sm``, ``md`` och ``lg`` står för small, medium och large.

När en text skickas till en spaCy-modell går texten igenom en pipeline. Pipelinen består av flera delar som utför olika uppgifter. En av dessa delar är NER som försöker hitta namngivna entiteter i texten. Resultatet sparas i ett ``Doc``-objekt och de hittade entiteterna kan hämtas med ``doc.ents``.

Varje entitet får en etikett som beskriver vilken typ av entitet modellen tror att den har hittat. Några av etiketterna som förekommer i projektet är:

- ``PRS`` – person
- ``ORG`` – organisation
- ``LOC`` – plats
- ``OBJ`` – namngivet objekt
- ``TME`` – tid
- ``WRK`` – t.ex. en produkt eller ett projekt

En färdigtränad modell har redan tränats på stora mängder text men den känner ändå inte alltid igen alla namn korrekt. Finjustering innebär att fortsätta träna en redan färdig modell med egna exempel. I det här projektet får modellen träningsmeningar där organisationer och platser har markerats med rätt etikett.

Under träningen räknas ett loss-värde ut. Det visar hur stort fel modellen gör på träningsdatan. Ett lägre värde betyder att modellen har blivit bättre på just
träningsexemplen men det betyder inte automatiskt att den fungerar bra på andra texter.

I träningen används även dropout. Förenklat innebär det att en del av det neurala nätverkets neuroner slumpmässigt stängs av tillfälligt. Syftet är att modellen inte ska bli för beroende av enskilda delar av nätverket och bara lära sig träningsmeningarna utantill. I min kod används drop=0.2, vilket innebär en dropout på 20 procent.
Eftersom dropout innehåller slump kan resultatet variera något mellan olika träningskörningar.


## Genomförande

Jag började med att installera spaCy och de svenska modellerna ``sv_core_news_sm``, ``sv_core_news_md`` och ``sv_core_news_lg``. Därefter testade jag small-modellen på egna meningar som innehöll personer, organisationer och platser. Jag ändrade bland annat hur företagsnamnen skrevs och vilket sammanhang de förekom i för att se om modellens resultat förändrades.

Efter de första testerna jämförde jag small, medium och large-modellen på samma meningar. Jag testade både företagsnamn och personnamn. Resultaten sparades i en DataFrame för att göra det enklare att jämföra vilka entiteter modellerna hittade och vilka etiketter de fick.

Modellerna testades även på ett utdrag från ett pressmeddelande från Volvo Cars. Texten sparades i en separat textfil och lästes in i notebooken. Detta test användes för att se hur modellerna fungerade på en längre text med flera olika typer av entiteter. Jag skapade även funktionerna ``find_entities`` och ``compare_models`` i filen
``src/utils.py`` för att kunna återanvända kod.

Utifrån modelljämförelsen valde jag medium-modellen för finjusteringen. Den gav bättre resultat än small-modellen för flera av organisationerna och lyckades bland annat identifiera Volvo som ``ORG``. Den hittade även en del av namnet EC Utbildning, medan large-modellen inte hittade organisationen i det testet.

Träningsdatan bestod av åtta meningar där jag markerade organisationer och platser med rätt etiketter. Varje entitet markerades med startposition, slutposition och etikett. Innan träningen skrev jag ut de markerade delarna av meningarna för att kontrollera att positionerna pekade på rätt ord.

Under finjusteringen stängde jag tillfälligt av de andra delarna i spaCys pipeline och tränade endast NER. Träningsmeningarna blandades inför varje epok och modellen tränades under tio epoker. Jag använde ``drop=0.2`` vilket innebär en dropout på 20 %. Modellen sparades sedan i mappen ``custom_ner_model`` och laddades in igen för att kontrolleras.

Som stöd när jag skrev koden för finjusteringen använde jag en YouTube-video som visar hur en spaCy-modell kan tränas med egen NER-data. I videon användes begin_training() men eftersom jag ville fortsätta träna en redan färdigtränad medium-modell använde jag i stället resume_training(). Jag anpassade sedan koden till den svenska medium-modellen och skapade egna träningsmeningar och tester.

Till sist jämförde jag originalmodellen med den finjusterade modellen. Först använde jag samma pressmeddelande som tidigare. Därefter testade jag nya meningar med
organisationerna från träningsdatan. Jag testade även andra företagsnamn som inte fanns i min egen träningsdata för att undersöka om modellen hade lärt sig något mer än bara de specifika träningsmeningarna.


## Resultat

I första testerna lyckades small-modellen identifiera personer och platser bättre än organisationer. Jack Olofsson identifierades som ``PRS`` och Göteborg som
``LOC`` men EC Utbildning identifierades inte som en organisation. När meningen i stället började med "Skolan EC Utbildning" klassificerades hela uttrycket som ``ORG``. Detta visade att sammanhanget kunde påverka både om modellen hittade en entitet och var den ansåg att entiteten började och slutade.

När företagsnamnen testades med och utan "AB" blev skillnaden tydlig. Spotify och Klarna identifierades inte som organisationer utan "AB" men Spotify AB och Klarna AB
klassificerades som ``ORG``. Volvo klassificerades däremot som ``OBJ`` av small-modellen både när texten handlade om företaget och när Volvo användes som bilmärke.

Jämförelsen mellan small, medium och large-modellen visade att en större modell inte alltid gav bättre resultat. Medium och large-modellen klassificerade Volvo som ``ORG`` medan small-modellen klassificerade namnet som ``OBJ``. Medium-modellen hittade även "EC" som ``ORG`` men inte hela namnet EC Utbildning. Large-modellen fungerade bättre i några av testerna med namn men missade fortfarande Nour El-Refai.

I testet med pressmeddelandet hittade alla modellerna Erik Coelingh som person och Göteborg som plats. Volvo Car Group klassificerades däremot som ``OBJ`` i stället för
``ORG``. Modellerna gav även olika resultat för bland annat Trafikverket och Göteborgs Stad. Testet visade att samma text kan ge olika resultat beroende på vilken modell som används.

Efter finjusteringen identifierade medium-modellen Volvo Car Group som ``ORG`` i pressmeddelandet. Den identifierade även Spotify AB, Klarna AB, Volvo och hela namnet EC Utbildning som organisationer i de nya testmeningarna. Originalmodellen missade flera av dessa organisationer eller gav dem en annan etikett.

Den finjusterade modellen testades även på företagsnamn som inte fanns i min egen träningsdata. Bower och Funnel identifierades som ``ORG``. Volumental och Elastisys identifierades inte utan "AB" men Volumental AB och Elastisys AB klassificerades som ``ORG``. Detta tyder på att modellen hade lärt sig vissa mönster som kunde hjälpa den att hitta nya organisationer men resultatet påverkades fortfarande av hur företagsnamnet skrevs.

Resultatet från finjusteringen varierade något mellan olika träningskörningar. I vissa körningar identifierades exempelvis projektnamnet "Drive Me" som ``WRK`` medan det inte hittades i andra körningar. Finjusteringen förbättrade flera av resultaten i mina tester men förbättringarna var inte stabila i alla exempel.


## Begränsningar och möjliga förbättringar

En tydlig begränsning är att träningsdatan endast bestod av åtta meningar. Flera av meningarna hade nästan samma struktur och innehöll samma företagsnamn med eller utan "AB". Modellen fick därför få exempel att träna på. Att loss snabbt sjönk till 0 innebär att modellen lärde sig träningsmeningarna bra men också en risk att modellen blev överanpassad till den lilla träningsdatan.

Testerna gjordes också på ett litet antal meningar som jag själv valde. Jag använde inte någon separat testdata med rätta etiketter och beräknade inte precision, recall eller F1. Resultaten bygger därför på att jag manuellt jämförde vilka entiteter originalmodellen och den finjusterade modellen hittade. Företagen i sista testet fanns inte med i min egen träningsdata dock vet jag inte om de förekom i den data som spaCys ursprungliga modell tränades på.

En annan begränsning är att resultatet kunde variera mellan olika körningar. I vissa körningar hittades "Drive Me" som ``WRK`` medan det inte hittades i andra. Modellen gjorde också ibland fel på entitetens gränser t.ex. när den klassificerade hela uttrycket "Organisationen Spotify" som ``ORG`` i stället för endast "Spotify".

En möjlig förbättring skulle kunna vara att använda mer träningsmeningar med flera organisationer där formuleringarna varierade. Träningsdatan skulle kunna innehålla företagsnamn både med och utan "AB" och företag som förekommer på olika platser i meningarna. Det skulle även vara bra att dela upp datan i separat träningsdata och testdata. Då skulle modellen kunna utvärderas på meningar som inte har använts under träningen.

Med fler texter som modellen inte tränats på skulle det även vara möjligt att beräkna precision, recall och F1. Det skulle ge en tydligare bild av om finjusteringen faktiskt förbättrade modellen. Träningen skulle också kunna upprepas med olika inställningar för antal epoker och dropout för att undersöka vilka inställningar som ger stabilast resultat.


## Koppling till yrkesrollen

En data scientist kan använda NER för att analysera stora mängder text från exempelvis forum, nyhetsartiklar eller sociala medier. Om man vill undersöka vad människor skriver om olika företag kan NER användas för att automatiskt hitta företagsnamnen i inläggen. Man kan sedan räkna hur ofta ett visst företag nämns och undersöka om antalet förändras över tid.

NER skulle även kunna kombineras med sentimentanalys. NER-modellen identifierar vilket företag ett inlägg handlar om medan en annan modell undersöker om texten verkar vara positiv eller negativ. Detta skulle kunna användas för att få en bild av hur människor diskuterar om ett företag eller en aktie. Resultatet skulle kunna visa om antalet positiva eller negativa inlägg ökar eller minskar under en viss period. T.ex. ett företag som vill följa hur deras varumärke diskuteras på internet.


## Källor

- https://spacy.io/usage/spacy-101#whats-spacy
- https://spacy.io/usage/linguistic-features#named-entities
- https://spacy.io/models
- https://spacy.io/models/sv
- https://www.youtube.com/watch?v=JIz-hiRrZ2g&t=753s
- https://www.volvocars.com/se/media/press-releases/CA90C6F155FAEA0A/



## Självreflektion

### 1. Vad lärde jag mig som jag inte kunde innan?

Innan projektet hade jag aldrig hört tals om NLP, NER eller spaCy. Jag har lärt mig hur en färdigtränad modell kan användas för att hitta personer, organisationer och platser i text. Jag har även lärt mig hur ``doc.ents``, ``ent.text`` och ``ent.label_`` används för att hämta de entiteter som modellen har hittat.

Jag har också lärt mig att olika modeller kan ge olika resultat på samma text. En större modell behöver inte alltid ge ett bättre resultat. Jag har även fått en förståelse för hur en färdigtränad modell kan finjusteras med egen träningsdata och sedan sparas och laddas igen.

### 2. Vad var svårast att förstå eller genomföra?

Det svåraste var att förstå koden för att finjustera en redan färdigtränad modell. Modellen skulle först laddas, de andra delarna förutom "NER" skulle stängas av i pipelinen och träningen skulle fortsätta med resume_training(). Sedan skulle träningsdatan göras om till Example och skickas till modellen med update() under flera epoker.

YouTube-videon hjälpte mig att förstå grunderna i hur koden kunde skrivas. Jag behövde dock anpassa exemplet eftersom videon använde begin_training() medan jag använde resume_training() för att fortsätta träna en befintlig modell. Det tog tid att förstå i vilken ordning de olika delarna skulle köras och vilken uppgift de hade i träningen.


### 3. Vilket tekniskt val är jag mest nöjd med och varför?

Jag är nöjd med att jag först jämförde small, medium och large-modellen innan jag valde vilken modell som skulle finjusteras. Jag valde medium-modellen eftersom den fungerade bättre än small-modellen på flera av organisationerna och hittade en del av namnet EC Utbildning vilket large-modellen inte gjorde i samma test.


### 4. Vad hade jag gjort annorlunda om jag började om?

Om jag började om hade jag använt fler och mer varierade meningar. De åtta meningarna som användes hade liknande struktur och innehöll bara ett fåtal organisationer.

Jag hade även delat upp exempelmeningarna i träningsdata och testdata redan från början. Då hade det blivit tydligare vilka meningar modellen hade tränats på och vilka som endast användes för utvärdering.

### 5. Vad skulle vara ett naturligt nästa steg?

Ett naturligt nästa steg skulle vara att skapa en större mängd träningsdata med fler företag och mer varierade texter. Jag skulle även vilja testa modellen på fler nya texter och beräkna precision, recall och F1 för att kunna utvärdera modellen.

Ett annat nästa steg skulle också kunna vara att använda NER på texter från t.ex. ett forum . Modellen skulle då kunna identifiera vilka företag som nämns och hur ofta de förekommer. Resultatet skulle kunna kombineras med en sentimentanalys för att undersöka om diskussionen om ett företag verkar vara positiv eller negativ.

### 6. Vilket betyg tycker jag att arbetet motsvarar?

Jag tycker att arbetet motsvarar VG.

### 7. Motivering av min bedömning

Jag har byggt en fungerande lösning som använder spaCy för NER och jämfört tre olika modeller. Jag har inte bara visat resultaten utan även undersökt hur resultaten påverkas av hur företagsnamnet skrivs, sammanhang och vilken modell som används.

Jag har gjort egna tekniska val t.ex. att använda medium-modellen för finjusteringen och att fortsätta träningen med resume_training(). Jag skapade egen träningsdata, sparade och laddade den finjusterade modellen och testade den både på företag från träningsdatan och på andra företag.

Jag har även diskuterat arbetets begränsningar. Träningsdatan var liten, resultaten varierade mellan körningar och jag beräknade inte några mått som precision, recall och F1. Jag tycker att jag har visat att jag förstår både hur tekniken används och vilka problem som finns med min lösning.