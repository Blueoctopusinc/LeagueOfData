League of legends API project for my undergraduate dissertation.

apiHandlers.py - Custom API handler, keeps within rate limits for unverified riot developer accounts

ChampionGGScraper.py - Selenium based webscraper for getting latest meta-statistics regarding champions

dataCollector.py - Collects raw match data from the League of Legends API, uses a seed account ID and adds unique ID's and matches from it's match history into a list and runs the same process on each. 

Match processor.py - Feature engineering for ML models

Logistic regression, Random Forest and Naive Bayes models utilizing Sci-Kit-Learn all found within the models directory
