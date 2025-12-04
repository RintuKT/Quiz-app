import os
import django
import random

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_project.settings')
django.setup()

from quiz.models import Subject, Question, Option

def add_questions():
    # Define questions for each subject
    questions_data = {
        'Biology': [
            {
                'text': 'Which is the longest part of the alimentary canal?',
                'options': [
                    {'text': 'Small intestine', 'is_correct': True},
                    {'text': 'Large intestine', 'is_correct': False},
                    {'text': 'Stomach', 'is_correct': False},
                    {'text': 'Oesophagus', 'is_correct': False}
                ]
            },
            {
                'text': 'The breakdown of pyruvate to give carbon dioxide, water and energy takes place in:',
                'options': [
                    {'text': 'Cytoplasm', 'is_correct': False},
                    {'text': 'Mitochondria', 'is_correct': True},
                    {'text': 'Chloroplast', 'is_correct': False},
                    {'text': 'Nucleus', 'is_correct': False}
                ]
            },
            {
                'text': 'Which plant hormone promotes cell division?',
                'options': [
                    {'text': 'Auxin', 'is_correct': False},
                    {'text': 'Gibberellin', 'is_correct': False},
                    {'text': 'Cytokinin', 'is_correct': True},
                    {'text': 'Abscisic acid', 'is_correct': False}
                ]
            },
            {
                'text': 'The gap between two neurons is called a:',
                'options': [
                    {'text': 'Dendrite', 'is_correct': False},
                    {'text': 'Synapse', 'is_correct': True},
                    {'text': 'Axon', 'is_correct': False},
                    {'text': 'Impulse', 'is_correct': False}
                ]
            },
            {
                'text': 'Which of the following is a plant hormone?',
                'options': [
                    {'text': 'Insulin', 'is_correct': False},
                    {'text': 'Thyroxin', 'is_correct': False},
                    {'text': 'Oestrogen', 'is_correct': False},
                    {'text': 'Cytokinin', 'is_correct': True}
                ]
            }
        ],
        'Chemistry': [
            {
                'text': 'Which of the following is a displacement reaction?',
                'options': [
                    {'text': 'MgCO3 → MgO + CO2', 'is_correct': False},
                    {'text': '2Na + 2H2O → 2NaOH + H2', 'is_correct': True},
                    {'text': '2H2 + O2 → 2H2O', 'is_correct': False},
                    {'text': '2Pb(NO3)2 → 2PbO + 4NO2 + O2', 'is_correct': False}
                ]
            },
            {
                'text': 'Which acid is present in tomato?',
                'options': [
                    {'text': 'Acetic acid', 'is_correct': False},
                    {'text': 'Oxalic acid', 'is_correct': True},
                    {'text': 'Citric acid', 'is_correct': False},
                    {'text': 'Tartaric acid', 'is_correct': False}
                ]
            },
            {
                'text': 'Which metal is liquid at room temperature?',
                'options': [
                    {'text': 'Sodium', 'is_correct': False},
                    {'text': 'Mercury', 'is_correct': True},
                    {'text': 'Zinc', 'is_correct': False},
                    {'text': 'Aluminum', 'is_correct': False}
                ]
            },
            {
                'text': 'The functional group of ketones is:',
                'options': [
                    {'text': '-OH', 'is_correct': False},
                    {'text': '-CHO', 'is_correct': False},
                    {'text': '-COOH', 'is_correct': False},
                    {'text': '>C=O', 'is_correct': True}
                ]
            },
            {
                'text': 'Which element has the electronic configuration 2, 8, 2?',
                'options': [
                    {'text': 'Sodium', 'is_correct': False},
                    {'text': 'Magnesium', 'is_correct': True},
                    {'text': 'Aluminum', 'is_correct': False},
                    {'text': 'Silicon', 'is_correct': False}
                ]
            }
        ],
        'Physics': [
            {
                'text': 'The SI unit of electric current is:',
                'options': [
                    {'text': 'Volt', 'is_correct': False},
                    {'text': 'Ampere', 'is_correct': True},
                    {'text': 'Ohm', 'is_correct': False},
                    {'text': 'Joule', 'is_correct': False}
                ]
            },
            {
                'text': 'The focal length of a spherical mirror of radius of curvature 30 cm is:',
                'options': [
                    {'text': '10 cm', 'is_correct': False},
                    {'text': '15 cm', 'is_correct': True},
                    {'text': '20 cm', 'is_correct': False},
                    {'text': '30 cm', 'is_correct': False}
                ]
            },
            {
                'text': 'Which of the following materials cannot be used to make a lens?',
                'options': [
                    {'text': 'Water', 'is_correct': False},
                    {'text': 'Glass', 'is_correct': False},
                    {'text': 'Plastic', 'is_correct': False},
                    {'text': 'Clay', 'is_correct': True}
                ]
            },
            {
                'text': 'The human eye forms the image of an object at its:',
                'options': [
                    {'text': 'Cornea', 'is_correct': False},
                    {'text': 'Iris', 'is_correct': False},
                    {'text': 'Pupil', 'is_correct': False},
                    {'text': 'Retina', 'is_correct': True}
                ]
            },
            {
                'text': 'Device used to measure potential difference is:',
                'options': [
                    {'text': 'Ammeter', 'is_correct': False},
                    {'text': 'Voltmeter', 'is_correct': True},
                    {'text': 'Galvanometer', 'is_correct': False},
                    {'text': 'Potentiometer', 'is_correct': False}
                ]
            }
        ],
        'Mathematics': [
            {
                'text': 'The nth term of an A.P. is given by an = 3 + 4n. The common difference is:',
                'options': [
                    {'text': '7', 'is_correct': False},
                    {'text': '3', 'is_correct': False},
                    {'text': '4', 'is_correct': True},
                    {'text': '1', 'is_correct': False}
                ]
            },
            {
                'text': 'The distance of the point P(2, 3) from the x-axis is:',
                'options': [
                    {'text': '2', 'is_correct': False},
                    {'text': '3', 'is_correct': True},
                    {'text': '1', 'is_correct': False},
                    {'text': '5', 'is_correct': False}
                ]
            },
            {
                'text': 'If tan A = 4/3, then sin A is:',
                'options': [
                    {'text': '3/5', 'is_correct': False},
                    {'text': '4/5', 'is_correct': True},
                    {'text': '3/4', 'is_correct': False},
                    {'text': '5/3', 'is_correct': False}
                ]
            },
            {
                'text': 'The probability of getting a prime number in a single throw of a die is:',
                'options': [
                    {'text': '1/2', 'is_correct': True},
                    {'text': '1/3', 'is_correct': False},
                    {'text': '1/6', 'is_correct': False},
                    {'text': '2/3', 'is_correct': False}
                ]
            },
            {
                'text': 'The roots of the quadratic equation x² - 3x - 10 = 0 are:',
                'options': [
                    {'text': '5, -2', 'is_correct': True},
                    {'text': '-5, 2', 'is_correct': False},
                    {'text': '5, 2', 'is_correct': False},
                    {'text': '-5, -2', 'is_correct': False}
                ]
            }
        ],
        'English': [
            {
                'text': 'Who is the poet of the poem "Dust of Snow"?',
                'options': [
                    {'text': 'Leslie Norris', 'is_correct': False},
                    {'text': 'Robert Frost', 'is_correct': True},
                    {'text': 'Carolyn Wells', 'is_correct': False},
                    {'text': 'Robin Klein', 'is_correct': False}
                ]
            },
            {
                'text': 'What did Lencho hope for?',
                'options': [
                    {'text': 'A good shower of rain', 'is_correct': True},
                    {'text': 'A new tractor', 'is_correct': False},
                    {'text': 'A sack of corn', 'is_correct': False},
                    {'text': 'New clothes', 'is_correct': False}
                ]
            },
            {
                'text': 'Why was the young seagull afraid to fly?',
                'options': [
                    {'text': 'He was lazy', 'is_correct': False},
                    {'text': 'He was injured', 'is_correct': False},
                    {'text': 'He thought his wings would not support him', 'is_correct': True},
                    {'text': 'He was afraid of other birds', 'is_correct': False}
                ]
            },
            {
                'text': 'Who was Tricki?',
                'options': [
                    {'text': 'A cat', 'is_correct': False},
                    {'text': 'A monkey', 'is_correct': False},
                    {'text': 'A dog', 'is_correct': True},
                    {'text': 'A rabbit', 'is_correct': False}
                ]
            },
            {
                'text': 'What was the name of the scientist in "The Invisible Man"?',
                'options': [
                    {'text': 'Griffin', 'is_correct': True},
                    {'text': 'Mrs. Hall', 'is_correct': False},
                    {'text': 'Jaffers', 'is_correct': False},
                    {'text': 'Kemp', 'is_correct': False}
                ]
            }
        ],
        'Hindi': [
            {
                'text': 'नेताजी का चश्मा पाठ के लेखक कौन हैं?',
                'options': [
                    {'text': 'स्वयं प्रकाश', 'is_correct': True},
                    {'text': 'रामवृक्ष बेनीपुरी', 'is_correct': False},
                    {'text': 'यशपाल', 'is_correct': False},
                    {'text': 'मन्नू भंडारी', 'is_correct': False}
                ]
            },
            {
                'text': 'बालगोबिन भगत क्या काम करते थे?',
                'options': [
                    {'text': 'अध्यापक', 'is_correct': False},
                    {'text': 'खेतीबारी', 'is_correct': True},
                    {'text': 'दुकानदार', 'is_correct': False},
                    {'text': 'वकील', 'is_correct': False}
                ]
            },
            {
                'text': 'लक्ष्मण ने परशुराम को क्या कहा?',
                'options': [
                    {'text': 'वीर योद्धा', 'is_correct': False},
                    {'text': 'महामुनि', 'is_correct': False},
                    {'text': 'धनुष तोड़ने वाला', 'is_correct': False},
                    {'text': 'बहुत बोलने वाला', 'is_correct': True}
                ]
            },
            {
                'text': 'उत्साह कविता में बादल किसका प्रतीक है?',
                'options': [
                    {'text': 'शांति का', 'is_correct': False},
                    {'text': 'क्रांति का', 'is_correct': True},
                    {'text': 'प्रेम का', 'is_correct': False},
                    {'text': 'दुःख का', 'is_correct': False}
                ]
            },
            {
                'text': 'माता का अंचल पाठ में भोलानाथ का वास्तविक नाम क्या था?',
                'options': [
                    {'text': 'तारकेश्वर नाथ', 'is_correct': True},
                    {'text': 'भोलानाथ', 'is_correct': False},
                    {'text': 'बैजनाथ', 'is_correct': False},
                    {'text': 'दीनानाथ', 'is_correct': False}
                ]
            }
        ],
        'Malayalam': [
            {
                'text': 'കേരളത്തിലെ ആദ്യത്തെ വർത്തമാനപത്രം ഏതാണ്?',
                'options': [
                    {'text': 'രാജ്യസമാചാരം', 'is_correct': True},
                    {'text': 'പശ്ചിമോദയം', 'is_correct': False},
                    {'text': 'ദീപിക', 'is_correct': False},
                    {'text': 'മലയാള മനോരമ', 'is_correct': False}
                ]
            },
            {
                'text': 'മലയാള ഭാഷയുടെ പിതാവ് എന്നറിയപ്പെടുന്നത് ആര്?',
                'options': [
                    {'text': 'കുഞ്ചൻ നമ്പ്യാർ', 'is_correct': False},
                    {'text': 'തുഞ്ചത്തെഴുത്തച്ഛൻ', 'is_correct': True},
                    {'text': 'ചെറുശ്ശേരി', 'is_correct': False},
                    {'text': 'വള്ളത്തോൾ', 'is_correct': False}
                ]
            },
            {
                'text': 'ജ്ഞാനപീഠം നേടിയ ആദ്യ മലയാള കവി ആര്?',
                'options': [
                    {'text': 'ജി. ശങ്കരക്കുറുപ്പ്', 'is_correct': True},
                    {'text': 'എസ്.കെ. പൊറ്റക്കാട്', 'is_correct': False},
                    {'text': 'തകഴി ശിവശങ്കരപ്പിള്ള', 'is_correct': False},
                    {'text': 'എം.ടി. വാസുദേവൻ നായർ', 'is_correct': False}
                ]
            },
            {
                'text': 'കേരള സാഹിത്യ അക്കാദമി സ്ഥിതി ചെയ്യുന്നത് എവിടെ?',
                'options': [
                    {'text': 'തിരുവനന്തപുരം', 'is_correct': False},
                    {'text': 'തൃശ്ശൂർ', 'is_correct': True},
                    {'text': 'കോഴിക്കോട്', 'is_correct': False},
                    {'text': 'കോട്ടയം', 'is_correct': False}
                ]
            },
            {
                'text': 'ഓടക്കുഴൽ പുരസ്കാരം സ്ഥാപിച്ചത് ആര്?',
                'options': [
                    {'text': 'ബാലാമണിയമ്മ', 'is_correct': False},
                    {'text': 'ജി. ശങ്കരക്കുറുപ്പ്', 'is_correct': True},
                    {'text': 'ഒ.എൻ.വി. കുറുപ്പ്', 'is_correct': False},
                    {'text': 'സുഗതകുമാരി', 'is_correct': False}
                ]
            }
        ]
    }

    print("Starting to add questions...")
    
    for subject_name, questions in questions_data.items():
        # Find subjects with this name (could be in different courses)
        subjects = Subject.objects.filter(name__icontains=subject_name)
        
        if not subjects.exists():
            print(f"Warning: Subject '{subject_name}' not found in database. Skipping.")
            continue
            
        for subject in subjects:
            print(f"Adding questions to {subject.name} ({subject.course.get_name_display()})...")
            
            for q_data in questions:
                # Check if question already exists to avoid duplicates
                if Question.objects.filter(subject=subject, text=q_data['text']).exists():
                    print(f"  Question '{q_data['text'][:30]}...' already exists. Skipping.")
                    continue
                
                # Create question
                question = Question.objects.create(
                    subject=subject,
                    text=q_data['text'],
                    positive_points=4,
                    negative_points=1
                )
                
                # Create options
                for opt_data in q_data['options']:
                    Option.objects.create(
                        question=question,
                        text=opt_data['text'],
                        is_correct=opt_data['is_correct']
                    )
                
                print(f"  Added question: {q_data['text'][:50]}...")

    print("Done!")

if __name__ == '__main__':
    add_questions()
