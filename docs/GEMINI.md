# JACKBOT Project: Research & Development

This repository is dedicated to the research and development of **JACKBOT**, a predictive system for sports analytics, with an initial focus on soccer.

## Project Goal

The primary objective is to build and evaluate machine learning models to predict various outcomes in soccer matches. The project aims to explore the feasibility of predicting:

1.  **Match Outcome:** Classifying whether a match will result in a Win, Draw, or Loss.
2.  **Team Performance:** Regressing the total number of shots on goal for a team.
3.  **Player Performance:** Regressing the total number of shots on goal for an individual player.

The initial phase of the project uses a focused dataset from the **FIFA World Cup 2022** to establish a baseline and a rapid development cycle.

## Research Areas

The project encompasses a multi-disciplinary research approach:

*   **Market & User Analysis:** In-depth study of the Brazilian sports betting market, including the socio-economic profile of bettors, psychological motivations, and the societal impact of the industry. This includes analyzing the strategies of major players like **Esportes da Sorte**.
*   **Data Engineering & Feature Engineering:** Investigation of best practices for processing complex, event-based sports data (e.g., StatsBomb JSONs) and engineering meaningful features (e.g., Expected Goals (xG), ELO ratings).
*   **Predictive Modeling:** Exploration and evaluation of various algorithms, from traditional statistical models like Poisson Regression to machine learning ensembles like RandomForest and Gradient Boosting.
*   **Technology & Architecture:** Research into the MLOps lifecycle for sports prediction systems, including data acquisition APIs, model deployment, and managing concept drift.
*   **Explainable AI (XAI):** Analysis of the viability of using local, lightweight Large Language Models (LLMs) to generate human-readable explanations for model predictions on resource-constrained hardware.

## Current Status & Key Findings

*   **Data Processing:** A pipeline (`data_processing.py`) has been created to process raw data into structured CSVs for modeling.
*   **Initial Model Evaluation:**
    *   The **Match Outcome** model shows high promise (75% accuracy).
    *   The **Team Shots on Goal** model is partially viable (R² of 0.25).
    *   The **Player Shots on Goal** model is currently inviable with the existing simple features.

This `GEMINI.md` file serves as a living document to guide the project's direction based on ongoing research and findings.