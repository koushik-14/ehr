
import sqlite3

def insert_disease_data():
    conn = sqlite3.connect('../database/ehr.db')
    cursor = conn.cursor()

    diseases = [
        ("fever", "Body pain, High temperature, Weakness", "Take Dolo 650 twice a day, Drink plenty of water"),
        ("cold", "Runny nose, Sneezing, Sore throat", "Take Cetrizine, Drink warm liquids"),
        ("headache", "Pain in head, Sensitivity to light", "Take Paracetamol, Rest in a quiet place"),
        ("flu", "Cough, Chills, Fatigue", "Rest, Stay hydrated, Take Ibuprofen if needed"),
        ("diabetes", "Increased thirst, Frequent urination, Fatigue", "Monitor blood sugar, Follow a healthy diet, Exercise regularly"),
        ("hypertension", "High blood pressure, Headaches, Dizziness", "Reduce salt intake, Exercise regularly, Take prescribed medication"),
        ("asthma", "Shortness of breath, Wheezing, Chest tightness", "Use an inhaler, Avoid triggers, Seek medical advice if severe"),
        ("migraine", "Severe headache, Nausea, Sensitivity to light", "Take pain relievers, Rest in a dark room, Stay hydrated"),
        ("bronchitis", "Cough with mucus, Chest discomfort, Fatigue", "Drink warm fluids, Avoid smoke, Take prescribed antibiotics if bacterial"),
        ("pneumonia", "Fever, Cough, Difficulty breathing", "Take antibiotics (if bacterial), Rest, Drink warm fluids"),
        ("anemia", "Fatigue, Pale skin, Shortness of breath", "Eat iron-rich foods, Take iron supplements if needed"),
        ("stomach ulcer", "Burning stomach pain, Nausea, Weight loss", "Avoid spicy foods, Take antacids, Consult a doctor"),
        ("food poisoning", "Vomiting, Diarrhea, Abdominal pain", "Stay hydrated, Eat bland foods, Take probiotics if needed"),
        ("covid-19", "Fever, Dry cough, Loss of taste or smell", "Isolate, Stay hydrated, Seek medical attention if breathing difficulty occurs"),
        ("arthritis", "Joint pain, Swelling, Stiffness", "Exercise, Use pain relievers, Apply warm compresses")
    ]

    cursor.executemany('''
        INSERT OR IGNORE INTO disease_info (disease, symptoms, suggestions)
        VALUES (?, ?, ?)
    ''', diseases)

    conn.commit()
    conn.close()
    print("Disease data inserted successfully.")

# Run the function to insert data
insert_disease_data()
