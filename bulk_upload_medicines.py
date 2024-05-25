# import os
# import django
# import random

# # Set up Django environment
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cchc.settings')
# django.setup()

# from patient.models import Medicine

# # Sample data for 12 heart or cardio-related medicines
# medicine_data = [
#     {
#         'name': 'Lisinopril',
#         'manufacturer': 'Merck',
#         'medicine_type': 'Antihypertensive',
#         'dosage_form': 'Tablet',
#         'dosage_strength': '10 mg',
#         'description': 'Lisinopril is an ACE inhibitor used to treat high blood pressure and heart failure, and to improve survival after a heart attack.',
#         'side_effect': 'Common side effects include dizziness, headache, and cough. Serious side effects can include high potassium levels, kidney problems, and severe allergic reactions.'
#     },
#     {
#         'name': 'Amlodipine',
#         'manufacturer': 'Pfizer',
#         'medicine_type': 'Antihypertensive',
#         'dosage_form': 'Tablet',
#         'dosage_strength': '5 mg',
#         'description': 'Amlodipine is used to treat high blood pressure and chest pain (angina). Lowering high blood pressure helps prevent strokes, heart attacks, and kidney problems.',
#         'side_effect': 'Common side effects include swelling, dizziness, and flushing. Serious side effects can include worsening chest pain, severe allergic reactions, and very low blood pressure.'
#     },
#     {
#         'name': 'Atorvastatin',
#         'manufacturer': 'Pfizer',
#         'medicine_type': 'Statin',
#         'dosage_form': 'Tablet',
#         'dosage_strength': '20 mg',
#         'description': 'Atorvastatin is used to lower cholesterol and triglycerides in the blood. It can help reduce the risk of heart attack, stroke, and other heart-related complications.',
#         'side_effect': 'Common side effects include muscle pain, diarrhea, and upset stomach. Serious side effects can include liver problems and severe muscle breakdown (rhabdomyolysis).'
#     },
#     {
#         'name': 'Losartan',
#         'manufacturer': 'Merck',
#         'medicine_type': 'Antihypertensive',
#         'dosage_form': 'Tablet',
#         'dosage_strength': '50 mg',
#         'description': 'Losartan is used to treat high blood pressure and to help protect the kidneys from damage due to diabetes. It is also used to lower the risk of stroke in patients with high blood pressure and an enlarged heart.',
#         'side_effect': 'Common side effects include dizziness, back pain, and nasal congestion. Serious side effects can include high potassium levels, kidney problems, and severe allergic reactions.'
#     },
#     {
#         'name': 'Metoprolol',
#         'manufacturer': 'AstraZeneca',
#         'medicine_type': 'Beta Blocker',
#         'dosage_form': 'Tablet',
#         'dosage_strength': '25 mg',
#         'description': 'Metoprolol is used to treat high blood pressure, chest pain (angina), and heart failure. It helps prevent strokes, heart attacks, and kidney problems.',
#         'side_effect': 'Common side effects include dizziness, fatigue, and depression. Serious side effects can include shortness of breath, very slow heartbeat, and severe allergic reactions.'
#     },
#     {
#         'name': 'Carvedilol',
#         'manufacturer': 'GlaxoSmithKline',
#         'medicine_type': 'Beta Blocker',
#         'dosage_form': 'Tablet',
#         'dosage_strength': '6.25 mg',
#         'description': 'Carvedilol is used to treat high blood pressure and heart failure. It is also used after a heart attack to improve survival if your heart is not pumping well.',
#         'side_effect': 'Common side effects include dizziness, fatigue, and low blood pressure. Serious side effects can include severe allergic reactions, very slow heartbeat, and liver problems.'
#     },
#     {
#         'name': 'Clopidogrel',
#         'manufacturer': 'Sanofi',
#         'medicine_type': 'Antiplatelet',
#         'dosage_form': 'Tablet',
#         'dosage_strength': '75 mg',
#         'description': 'Clopidogrel is used to prevent heart attacks and strokes in persons with heart disease, recent stroke, or blood circulation disease (peripheral vascular disease).',
#         'side_effect': 'Common side effects include easy bleeding and bruising, stomach pain, and diarrhea. Serious side effects can include severe allergic reactions, unusual tiredness, and signs of infection (e.g., fever, persistent sore throat).'
#     },
#     {
#         'name': 'Hydrochlorothiazide',
#         'manufacturer': 'Teva Pharmaceuticals',
#         'medicine_type': 'Diuretic',
#         'dosage_form': 'Tablet',
#         'dosage_strength': '25 mg',
#         'description': 'Hydrochlorothiazide is used to treat high blood pressure. It helps prevent strokes, heart attacks, and kidney problems. It is also used to reduce swelling (edema) caused by certain conditions.',
#         'side_effect': 'Common side effects include dizziness, lightheadedness, and headache. Serious side effects can include severe dehydration, kidney problems, and severe allergic reactions.'
#     },
#     {
#         'name': 'Warfarin',
#         'manufacturer': 'Bristol-Myers Squibb',
#         'medicine_type': 'Anticoagulant',
#         'dosage_form': 'Tablet',
#         'dosage_strength': '5 mg',
#         'description': 'Warfarin is used to treat blood clots (such as in deep vein thrombosis-DVT or pulmonary embolus-PE) and/or to prevent new clots from forming in your body.',
#         'side_effect': 'Common side effects include nausea, loss of appetite, and stomach/abdominal pain. Serious side effects can include severe bleeding, purple toes syndrome, and severe allergic reactions.'
#     },
#     {
#         'name': 'Digoxin',
#         'manufacturer': 'GlaxoSmithKline',
#         'medicine_type': 'Cardiac Glycoside',
#         'dosage_form': 'Tablet',
#         'dosage_strength': '0.25 mg',
#         'description': 'Digoxin is used to treat heart failure, usually along with other medications. It is also used to treat certain types of irregular heartbeat (such as chronic atrial fibrillation).',
#         'side_effect': 'Common side effects include nausea, dizziness, and headache. Serious side effects can include vision changes, mental/mood changes, and signs of serious allergic reaction.'
#     },
#     {
#         'name': 'Isosorbide Mononitrate',
#         'manufacturer': 'Teva Pharmaceuticals',
#         'medicine_type': 'Nitrate',
#         'dosage_form': 'Tablet',
#         'dosage_strength': '30 mg',
#         'description': 'Isosorbide Mononitrate is used to prevent chest pain (angina) in patients with a certain heart condition (coronary artery disease).',
#         'side_effect': 'Common side effects include headache, dizziness, and lightheadedness. Serious side effects can include severe allergic reactions and very low blood pressure.'
#     },
#     {
#         'name': 'Verapamil',
#         'manufacturer': 'Abbott Laboratories',
#         'medicine_type': 'Calcium Channel Blocker',
#         'dosage_form': 'Tablet',
#         'dosage_strength': '80 mg',
#         'description': 'Verapamil is used to treat high blood pressure, chest pain (angina), and certain heart rhythm disorders. It works by relaxing blood vessels and slowing the heart rate.',
#         'side_effect': 'Common side effects include constipation, dizziness, and nausea. Serious side effects can include slow/irregular heartbeat, severe allergic reactions, and liver problems.'
#     },
#     {
#         'name': 'Diltiazem',
#         'manufacturer': 'Pfizer',
#         'medicine_type': 'Calcium Channel Blocker',
#         'dosage_form': 'Tablet',
#         'dosage_strength': '120 mg',
#         'description': 'Diltiazem is used to prevent chest pain (angina). It may help to increase your ability to exercise and decrease how often you get angina attacks.',
#         'side_effect': 'Common side effects include dizziness, lightheadedness, and flushing. Serious side effects can include very slow heartbeat, severe allergic reactions, and liver problems.'
#     }
# ]

# # Bulk insert data into the database
# medicines = [Medicine(**data) for data in medicine_data]
# Medicine.objects.bulk_create(medicines)

# print("Bulk upload of heart or cardio-related medicine data completed.")
print("Test Run Successful!")
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cchc.settings')
django.setup()

from patient.models import TestForm

# Sample data for new test names
test_data = [
    {'name': 'CHEST X-RAY'},
    {'name': 'HOLTER MONITOR'},
    {'name': 'NUCLEAR STRESS TEST'},
    {'name': 'CARDIAC MRI'},
    {'name': 'STRESS ECHOCARDIOGRAPHY'},
    {'name': 'PET SCAN (POSITRON EMISSION TOMOGRAPHY)'},
    {'name': 'CARDIAC BIOMARKER TEST'},
    {'name': 'CORONARY CALCIUM SCAN'},
    {'name': 'TILT TABLE TEST'},
    {'name': 'MYOCARDIAL PERFUSION IMAGING'},
    {'name': 'TRANSESOPHAGEAL ECHOCARDIOGRAM (TEE)'},
    {'name': 'ANKLE-BRACHIAL INDEX TEST'}
]

# Bulk insert data into the database
tests = [TestForm(**data) for data in test_data]
TestForm.objects.bulk_create(tests)

print("Bulk upload of test data completed.")
