from django.core.management.base import BaseCommand
from quiz.models import Course, Subject

class Command(BaseCommand):
    help = 'Sets up initial courses and subjects'

    def handle(self, *args, **kwargs):
        # Create courses
        courses_data = [
            ('10_KERALA', '10th Kerala Syllabus'),
            ('10_CBSE', '10th CBSE'),
            ('PLUS_ONE', '+1'),
            ('PLUS_TWO', '+2'),
        ]

        for course_name, course_display in courses_data:
            course, created = Course.objects.get_or_create(
                name=course_name,
                defaults={'description': f'Quiz questions for {course_display}'}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created course: {course_display}'))

            # Create subjects for each course
            subjects_data = [
                ('English', 'LANGUAGE'),
                ('Malayalam', 'LANGUAGE'),
                ('Hindi', 'LANGUAGE'),
                ('Physics', 'SCIENCE'),
                ('Chemistry', 'SCIENCE'),
                ('Biology', 'SCIENCE'),
                ('Mathematics', 'MATHEMATICS'),
            ]

            for subject_name, subject_type in subjects_data:
                subject, created = Subject.objects.get_or_create(
                    name=subject_name,
                    course=course,
                    defaults={
                        'subject_type': subject_type,
                        'description': f'{subject_name} for {course_display}'
                    }
                )
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f'Created subject: {subject_name} for {course_display}')
                    )
