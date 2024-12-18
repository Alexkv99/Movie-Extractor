# Movie-Extractor
This project was done as part of the course of "Data acquisition, extraction, and storage", IASD, 2024-2025.
It aims at extracting movies that won specific awards in a variety of events, and storing them in a coherent Database.

## Content
You will find in this repo the spiders, the clean up functions, the merging functions, as well as the SQL code and the final database. Additionnaly, slides of the presentation held in class are provided.

### Scrapers
It contains the spiders adapted to each Award Ceremony sites (BAFTA, Oscars, Golden globes, Cannes' Palme d'or, Berlin Bear).

### Cleanup
This repository contains two Python scripts designed to clean, standardize, and consolidate data.
The first script consolidates raw movie data by grouping multiple entries under a single film title, resolving duplicate or missing years, and merging scattered details. It produces a consistent JSON file in which each film has one canonical year, one title, and one unified list of details.

The second script further refines the dataset by normalizing film titles, assigning invalid years to an “Uncategorized” award category, merging scattered nominees under their respective awards, and removing duplicates, into a single clean JSON file.

### Merging
After standardizing the individual datasets, this script merges all the cleaned entries into a single list. This consolidated list is then deduplicated so that each unique combination of Year, Film, and Award appears only once. The final output is a single, unified JSON file, effectively serving as a single movie Database.

### SQL-Database
The codes aim at producing a SQL Database from the clean JSON files, from which it is possible to query specific information.

### Slides
The slides of the presentation held in class.

### Remarks on the final database and future work
We could have structured the database in several different ways depending on our priorities. For example, we might have organized tables around specific award ceremonies (e.g., Oscars, BAFTAs), focused on awards themselves (Best Picture, Best Director), or centered around the people involved (actors, directors, and so forth). Each approach would emphasize different connections and relationships in the data. In this case, we chose to structure the data by movies and their associated awards. This decision is somewhat arbitrary—it doesn’t imply that this particular design is superior. It simply reflects one reasonable way to organize the information without losing the generality needed to explore the dataset from multiple angles later.

As future experimentations we thought of the following points :
- We may want to add supplementary sources to enrich our database, even though it already contains roughly 4000 films. In particular, we focused on European and USA movies and awards, thus neglegting a massive amount of data from Asia, Africa, etc.
- One other idea could be to scrap all information on all films ever shot beforeheand, so that we have a clean reference that can be used to normalize titles and years of all databases with respect to that gold standard. Another advantage would be to ensure that the database outputs something (e.g. "No know Award"), whatever the queried film would be. However it would imply to work with a much larger database.
- We may also want to refine the merging, so that different prices from different ceremonies, or for different years, would be merged together. As shown during the presentation, there are inconsistency in the award titles through years as well as between ceremonies, and it would make sense sometimes to regroup them. For instance, Oscars' "Best Original story", a title discontinued in 1956, could be merged with "Best original scenario" and "best original screenplay". Sometimes it can be more open to discussion. Similarly, from one ceremony to the other, some merges are pretty trivial ("Best leading actor" from the BAFTA and "Actor in a leading role" from the Oscars"), others depends more on arbitrary choices (Silver Bear for Outstanding Artistic Contribution from the Berlin Ceremony and Production design from the Oscars?).


## Credits
Aymeric Behaegel, Alexandros Kouvatseas, Lucas Rousselet
