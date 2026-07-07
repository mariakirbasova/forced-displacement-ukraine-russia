## Introduction 

Ce répertoire rassemble les notebooks et scripts développés dans le cadre d’un mémoire consacré aux **déplacements forcés d’Ukraine vers la Russie depuis 2022**. À partir des traces numériques produites autour de cette migration, le projet étudie à la fois sa mise en récit institutionnelle et ses formes de discussion dans des espaces numériques d’entraide.

Deux corpus principaux sont mobilisés. Le premier est constitué d’**articles de l’agence de presse russe TASS**. 

Le second corpus réunit des messages publiés dans des **chats Telegram** crées en réponse à cette migration forcée. 

L’objectif du dépôt est donc de documenter les différentes étapes de constitution, de traitement et d’analyse de ces corpus. 

## Corpus TASS. 

#### Etape 1. 

##### Constitution de corpus. 

Dossier de l'étape : https://github.com/mariakirbasova/forced-displacement-ukraine-russia/tree/main/TASS/1_Scrapping%2Bclassification

Cette étape vise à constituer le corpus TASS utilisé pour l’analyse du discours institutionnel russe sur les déplacements forcés d’Ukraine vers la Russie. Le corpus est composé d’articles publiés par l’agence TASS à partir de février 2022 et portant sur l’« évacuation », l’accueil, la prise en charge administrative et humanitaire, ainsi que les trajectoires des personnes déplacées depuis l’Ukraine vers la Russie.

La constitution du corpus s’est faite en plusieurs temps : 

1. Scraping large des métadonnées (Nt1) ; 
2. Entraînement d’un classificateur permettant de sélectionner les articles pertinents (Nt2) ;
3. Récupération du texte intégral des articles retenus (Nt3) ; 
4. Classification supervisé finale par LLM, évaluation de modèle effectué sur un sous-corpus annoté (Nt4).

#### Etape 2. 

##### Analyse de discours - Comment l’accueil des migrants forcés venus d’Ukraine est-il mis en discours par l’État ? 

Dossier de l'étape : https://github.com/mariakirbasova/forced-displacement-ukraine-russia/tree/main/TASS/2_discours_analysis_LLM

Cette étape vise à analyser la manière dont l’agence TASS met en récit les déplacements forcés d’Ukraine vers la Russie.

Le méthode a suivi le pipeline suivant :  

1. Construction des catégories narratives selon une démarche de *Reflexive Thematic Analysis* : les labels ont d’abord été élaborés à partir du cadre théorique, puis ajustés lors de l’annotation manuelle d’un sous-corpus de 200 articles TASS, sur la base de ce sous-corpus preannoté plusieurs modèles ont été tesrés, afin d’évaluer leur capacité à reproduire l’annotation humaine et de sélectionner le modèle le plus performant (Nt1) ; 

2. Annotation automatique de l’ensemble du corpus TASS à l’aide du modèle retenu, chaque article pouvant être associé à un ou plusieurs récits (Nt2) ; 

3. Préparation d’une version nettoyée du corpus pour la publication dans le dépôt, sans les champs de travail internes comme les labels ou les textes lemmatisés (Nt3) ; 

5. Analyse statistique des récits identifiés : fréquences, poids relatif des catégories narratives et évolution temporelle des récits dans le corpus (Nt4) ; 

6. Analyse lexicale complémentaire menée à titre exploratoire, à partir des cooccurrences, des contextes d’apparition des termes et des proximités lexicales dans le corpus (Nt5).

#### Etape 3.

##### Modelisation thématique : De quoi parle le discours officiel lorsqu’il traite de l’accueil ?

Dossier de l'étape : https://github.com/mariakirbasova/forced-displacement-ukraine-russia/tree/main/TASS/3_Topic_Modelling_BERTopic

#### Etape 3. 

##### Topic modelling avec BERTopic. 

Dossier de l'étape : https://github.com/mariakirbasova/forced-displacement-ukraine-russia/tree/main/TASS/3_Topic_Modelling_BERTopic

Cette étape mobilise le *topic modelling* afin d’explorer les grandes thématiques présentes dans le corpus TASS. Ce methode permet d’identifier des regroupements thématiques récurrents dans les articles et de naviguer plus facilement dans le corpus.

L’étape se compose de deux notebooks principaux :

1. Construction du modèle BERTopic et comparaison de plusieurs configurations de topics : notamment avec différents nombres de topics, afin de comparer le niveau de granularité des résultats. Le notebook produit aussi des visualisations permettant d’examiner les topics, les mots les plus représentatifs, les documents associés et l’évolution temporelle des thèmes. Les résultats obtenus servent ensuite de base au travail d’interprétation dans le notebook suivant (Nt1) ;  

2. Analyse des thématiques. Ce notebook prend la classification thématique comme base de navigation dans le corpus, afin d’étudier ensuite ce qui est dit concrètement sur chaque thème. Par exemple, les topics liés aux transports permettent d’analyser les itinéraires, les moyens de déplacement et les acteurs chargés de l’organisation des trajets ; les topics liés aux régions russes permettent d’examiner la géographie de l’accueil et la répartition territoriale des dispositifs ; les topics liés aux points d’hébergement temporaire permettent d’étudier la manière dont les lieux d’accueil sont décrits ; enfin, les mentions chiffrées permettent d’observer comment TASS formule l’ampleur des déplacements (Nt2).










===============================================================

####  Remarque concernant la paternité des textes et l’utilisation d’outils d’IA générative

Pour les notebooks disponibles dans ce répertoire, des outils d’IA générative, notamment Copilot fondé sur GPT-5, ont été utilisés uniquement comme assistants à la rédaction, à la correction et à la documentation du code.

La révision du texte en français a été effectuée à l’aide de DeepL Translate, un algorithme non génératif.
