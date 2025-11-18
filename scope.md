1. Data Collection ✅

- Create 100-150 sample complaints
- Label each with:
    Category (6 types)
    Emotion (4 types: Neutral, Frustrated, Angry, Urgent)
    Department name
- Save as CSV

2. Train TWO ML Models

- Model 1: Category Classifier

    Input: Complaint text
    Output: Category (Municipality/Electricity/Water/Tax/Safety/Food)
    Method: TF-IDF + Logistic Regression
    Target Accuracy: >85%

- Model 2: Emotion Classifier

    Input: Complaint text
    Output: Emotion (Neutral/Frustrated/Angry/Urgent)
    Method: TF-IDF + Logistic Regression OR use pre-trained sentiment model
    Target Accuracy: >80%

3. NLP Processing

- Text preprocessing (clean, normalize)
- Entity extraction using spaCy:

    Locations (GPE, LOC)
    Dates
    Person names
    Phone numbers (regex)
    Email addresses (regex)



4. LLM Integration

- Download quantized LLaMA model (llama.cpp)
- Create prompt template:

    Given:
    - Complaint: "{text}"
    - Category: "{category}"
    - Emotion: "{emotion}"
    - Entities: "{locations, dates}"

    Generate:
    1. Confirmed department name
    2. Email subject line
    3. Email body (formal, structured)
    4. Manual steps (if email not possible)

    Output as JSON.

5. Department Mapping

- Create mapping dictionary:
    Category → Department → Email
    Municipality → Municipality Office → muni@city.gov
    Electricity → Electricity Board → elec@board.gov
    Water → Water Board → water@board.gov
    Tax → Tax Department → tax@city.gov
    Safety → Police Department → police@city.gov
    Food → Food Safety Dept → food@city.gov
