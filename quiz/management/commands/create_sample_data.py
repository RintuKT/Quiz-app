from django.core.management.base import BaseCommand
from quiz.models import Course, Subject, Question, Option
from django.contrib.auth.models import User, Group

class Command(BaseCommand):
    help = 'Creates sample data for the quiz app'

    def handle(self, *args, **kwargs):
        # Create admin group if it doesn't exist
        admin_group, _ = Group.objects.get_or_create(name='admin')

        # Create courses
        self.stdout.write('Creating courses...')
        courses = {
            'MATH': 'Mathematics',
            'SCI': 'Science',
            'ENG': 'English',
            'HIS': 'History'
        }
        
        for code, name in courses.items():
            course, created = Course.objects.get_or_create(
                name=code,
                defaults={
                    'description': f'{name} course with various topics'
                }
            )
            if created:
                self.stdout.write(f'Created course: {name}')

            # Create subjects for each course
            subjects = []
            if code == 'MATH':
                subjects = ['Algebra', 'Geometry', 'Calculus']
            elif code == 'SCI':
                subjects = ['Physics', 'Chemistry', 'Biology']
            elif code == 'ENG':
                subjects = ['Grammar', 'Literature', 'Vocabulary']
            elif code == 'HIS':
                subjects = ['World History', 'Geography', 'Civics']

            for subject_name in subjects:
                subject, created = Subject.objects.get_or_create(
                    name=subject_name,
                    course=course,
                    defaults={
                        'subject_type': 'theory'
                    }
                )
                if created:
                    self.stdout.write(f'Created subject: {subject_name}')

                    # Create sample questions for each subject
                    question = Question.objects.create(
                        subject=subject,
                        text=f'Sample question for {subject_name}?',
                        positive_points=1,
                        negative_points=0
                    )

                    # Create options for the question
                    options = [
                        ('Option A', True),
                        ('Option B', False),
                        ('Option C', False),
                        ('Option D', False)
                    ]

                    for text, is_correct in options:
                        Option.objects.create(
                            question=question,
                            text=text,
                            is_correct=is_correct
                        )

        self.stdout.write(self.style.SUCCESS('Successfully created sample data'))
