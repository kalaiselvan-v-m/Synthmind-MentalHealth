import json
from sqlalchemy.orm import Session
from backend.models.onboarding import OnboardingQuestion


def seed_onboarding_questions(db: Session):
    existing = db.query(OnboardingQuestion).first()

    if existing:
        return

    questions = [
        {
            "question_text": "Which pronouns do you use?",
            "question_type": "single_choice",
            "category": "pronouns",
            "options": ["She / Her", "He / Him", "They / Them"],
        },
        {
            "question_text": "How old are you?",
            "question_type": "single_choice",
            "category": "age",
            "options": ["Under 18", "18-24", "25-34", "35-44", "45-54", "55-64", "65 and over"],
        },
        {
            "question_text": "What's taking up most of your headspace right now?",
            "question_type": "multi_choice",
            "category": "headspace",
            "options": [
                "A person",
                "A decision",
                "My future",
                "My career",
                "My health",
                "A mistake I made",
                "Someone I miss",
                "Someone who hurt me",
                "Getting my life together",
                "Whether I’m on the right path",
                "Something I can’t name",
                "Nothing specific",
            ],
        },
        {
            "question_text": "How has your energy been lately?",
            "question_type": "single_choice",
            "category": "energy",
            "options": ["Running on empty", "Up and down", "Steady enough", "I am feeling good"],
        },
        {
            "question_text": "Are you going through something difficult right now?",
            "question_type": "single_choice",
            "category": "difficulty",
            "options": ["Yes, something big", "Some things weighing on me", "Nothing major", "I'd rather not say"],
        },
        {
            "question_text": "Who do you have to talk to when something is on your mind?",
            "question_type": "single_choice",
            "category": "support",
            "options": [
                "Plenty of people",
                "A few close people",
                "My partner",
                "My family",
                "I talk to AI",
                "No one, really",
                "I don’t reach out",
            ],
        },
        {
            "question_text": "How are you feeling about love and connection?",
            "question_type": "single_choice",
            "category": "connection",
            "options": [
                "Happily in love",
                "Searching for something real",
                "Hoping it finds me",
                "Loving someone who doesn’t know",
                "It’s complicated",
                "Healing from something",
                "Not even sure anymore",
                "Not a priority right now",
                "I’d rather not say",
            ],
        },
        {
            "question_text": "What are you most proud of about yourself?",
            "question_type": "multi_choice",
            "category": "strengths",
            "options": [
                "That I never give up",
                "How I think",
                "What I create",
                "How I treat people",
                "My independence",
                "How much love I have to give",
                "That I keep going no matter what",
                "That I stay true to myself",
                "I'm still figuring that out",
            ],
        },
        {
            "question_text": "What are you afraid of not getting right?",
            "question_type": "multi_choice",
            "category": "fears",
            "options": [
                "Saying what I actually think",
                "Working less and living more",
                "Nurturing my friendships",
                "Being fully present for the moments that matter",
                "Finding true love",
                "Being happy",
                "Living my own dreams",
                "Feeling alive in my body",
                "Making something wonderful",
                "Being a good person",
            ],
        },
    ]

    for index, q in enumerate(questions, start=1):
        new_question = OnboardingQuestion(
            question_text=q["question_text"],
            question_type=q["question_type"],
            category=q["category"],
            options_json=json.dumps(q["options"]),
            order_index=index,
        )
        db.add(new_question)

    db.commit()