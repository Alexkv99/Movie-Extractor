# Movie-Extractor
This project was done as part of the course of "Data acquisition, extraction, and storage", IASD, 2024-2025.
It aims at extracting movies that won specific awards in a variety of events, and storing of them in a coherent Database.

## Content
You will find in the repo the spiders, the clean up functions, the merging functions, as well as the final database.

### Scrapers
It contains the spiders adapted to each Award Ceremony sites (BAFTA, Oscars, Golden globes, Cannes' Palme d'or, Berlin Bear).

### Cleanup
This repository contains two Python scripts designed to clean, standardize, and consolidate data.
The first script consolidates raw movie data by grouping multiple entries under a single film title, resolving duplicate or missing years, and merging scattered details. It produces a consistent JSON file in which each film has one canonical year, one title, and one unified list of details.

The second script further refines the dataset by normalizing film titles, assigning invalid years to an “Uncategorized” award category, merging scattered nominees under their respective awards, and removing duplicates, into a single clean JSON file.

### Merging
After standardizing the individual datasets, this script merges all the cleaned entries into a single list. This consolidated list is then deduplicated so that each unique combination of Year, Film, and Award appears only once. The final output is a single, unified JSON file, effectively serving as a single Database.

### SQL-Database
The codes aim at producing a SQL Database from the clean JSON files, from which it is possible to query specific information.

### Slides
The slides of the presentation held in class.

## Credits
Aymeric Behaegel, Alexandros Kouvatseas, Lucas Rousselet
