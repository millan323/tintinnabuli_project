# StyleFinder (Millner AI Music Project)

This repository contains tools for analyzing and clustering musical scores based on extracted features. It supports the AIMystica project by visually comparing stylistic relationships between the works of Anthony Millner and selected inspirational composers.

## Tools

- **stylefinder_dataset.py**  
  Extracts key musical features from a folder of MusicXML files and stores them in `stylefinder_features.csv`.

- **stylefinder_visualizer.py**  
  Uses PCA and unsupervised clustering (k-means) to project and visualize stylistic distances and groupings between works.

## Current Status
- Total works analyzed: 39
- Groupings manually labeled: 7
- Next targets: More Messiaen and Pärt orchestral works (e.g. *Tabula Rasa*, *Et exspecto*, *Des canyons aux étoiles*)

## Project Goals
- Identify stylistic archetypes
- Map signature vs aspirational styles
- Support development of AIMystica (sacred music AI engine)

---

> Developed by Anthony Millner, June 2025
