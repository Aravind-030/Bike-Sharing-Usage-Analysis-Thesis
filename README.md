Descriptive Analysis of Bike Rental Usage Patterns
Author:

Context: Master's Thesis in Data Science, 2025

Project Overview
This repository contains the analytical codebase for my Master's thesis, which investigates the operational dynamics of urban bike-sharing systems. The study focuses on disaggregating usage patterns to understand how temporal factors (time of day, seasonality) and environmental constraints (weather) influence different user segments.

The core objective is to move beyond simple aggregate counts and identify actionable "heartbeats" in the city's mobility network—specifically distinguishing between the rigid demand of commuters and the elastic demand of casual users.

Data Source
The analysis relies on the Bike Sharing Dataset from the UCI Machine Learning Repository.

hour.csv: Primary dataset containing 17,379 hourly records with normalized weather features.

day.csv: Daily aggregates used for seasonal trend analysis.

Note on Spatial Analysis: The publicly available UCI dataset aggregates trips to preserve anonymity, removing specific Start/End station IDs. The code includes a module run_spatial_analysis designed to ingest raw transaction logs (e.g., trips.csv from Capital Bikeshare's system data) to demonstrate the methodology for calculating station net flow, should that raw data be available.

Methodology
The analysis pipeline (thesis_analysis.py) is built using Python for data processing and SQLite for structured querying.

ETL Process: Raw data is ingested, and cryptic column names are mapped to semantic identifiers. Meteorological data (temp, wind, humidity) is denormalized from scaled 0-1 values back to metric units for interpretability.

Temporal Profiling: SQL window functions and aggregations are used to isolate peak usage windows.

Segmentation: We statistically compare "Registered" (subscriber) vs. "Casual" (single-trip) users to validate the hypothesis that these groups have distinct usage behaviors.

Key Findings
The Commuter Bimodality: Analysis confirms a strict bimodal distribution on working days with peaks at 08:00 and 17:00. This pattern collapses into a single midday peak on weekends.

Weather Elasticity: Casual users show high elasticity to weather changes (rentals drop sharply with rain), whereas Registered users exhibit inelastic demand, likely due to lack of substitution transport modes for their commute.

Usage
To replicate this analysis:

Install dependencies: pip install -r requirements.txt

Ensure hour.csv is in the root directory.

Run the script: python thesis_analysis.py# Bike-Sharing-Usage-Analysis-Thesis
Master's Thesis code analyzing temporal and spatial patterns in bike sharing data.
