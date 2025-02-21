from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum, Prefetch
from .models import Question, Option, UserSubmission, Subject, Course, UserProfile
from rest_framework import viewsets
from .serializers import QuestionSerializer, OptionSerializer, UserSubmissionSerializer, QuestionDetailAdminSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action

@login_required
def subject_questions(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    
    # Get all questions with their options and user submissions
    questions = Question.objects.filter(subject=subject).prefetch_related(
        'options',
        Prefetch(
            'usersubmission_set',
            queryset=UserSubmission.objects.filter(user=request.user),
            to_attr='user_submissions'
        )
    )
    
    # Attach user submission to each question for easy access in template
    for question in questions:
        question.user_submission = question.user_submissions[0] if question.user_submissions else None
    
    # Calculate total score
    total_score = UserSubmission.objects.filter(
        user=request.user,
        question__subject=subject
    ).aggregate(total=Sum('score'))['total'] or 0
    
    return render(request, 'quiz/subject_questions.html', {
        'subject': subject,
        'questions': questions,
        'total_score': total_score
    })

@login_required
def quiz_question(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    
    # Check if specific question is requested
    question_id = request.GET.get('question')
    if question_id:
        question = get_object_or_404(Question, id=question_id, subject=subject)
        
        # Check if question was already answered
        if UserSubmission.objects.filter(user=request.user, question=question).exists():
            messages.error(request, 'You have already answered this question.')
            return redirect('subject_questions', subject_id=subject_id)
    else:
        # Get first unanswered question
        answered_questions = UserSubmission.objects.filter(
            user=request.user,
            question__subject=subject
        ).values_list('question_id', flat=True)
        
        question = Question.objects.filter(
            subject=subject
        ).exclude(
            id__in=answered_questions
        ).first()
        
        if not question:
            messages.info(request, 'You have answered all questions in this subject.')
            return redirect('subject_questions', subject_id=subject_id)
    
    return render(request, 'quiz/quiz.html', {
        'subject': subject,
        'question': question,
        'total_questions': Question.objects.filter(subject=subject).count(),
        'current_question_no': UserSubmission.objects.filter(
            user=request.user,
            question__subject=subject
        ).count() + 1
    })

@login_required
def submit_answer(request, subject_id, question_id):
    if request.method != 'POST':
        return redirect('quiz_question', subject_id=subject_id)
    
    # Get the question and selected option
    question = get_object_or_404(Question, id=question_id, subject_id=subject_id)
    subject = question.subject
    selected_option_id = request.POST.get('selected_option')
    
    # Check if question was already answered
    if UserSubmission.objects.filter(user=request.user, question=question).exists():
        messages.error(request, 'You have already answered this question.')
        return redirect('subject_questions', subject_id=subject_id)
    
    if not selected_option_id:
        messages.error(request, 'Please select an answer.')
        return redirect('quiz_question', subject_id=subject_id)
    
    selected_option = get_object_or_404(Option, id=selected_option_id)
    
    # Create submission
    points = question.positive_points if selected_option.is_correct else -question.negative_points
    UserSubmission.objects.create(
        user=request.user,
        question=question,
        selected_option=selected_option,
        score=points
    )
    
    # Get the correct answer for display
    correct_option = question.options.get(is_correct=True)
    
    # Render result page
    return render(request, 'quiz/answer_result.html', {
        'subject': subject,
        'is_correct': selected_option.is_correct,
        'points': abs(points),
        'total_score': UserSubmission.objects.filter(
            user=request.user,
            question__subject=subject
        ).aggregate(total=Sum('score'))['total'] or 0,
        'correct_answer': correct_option.text if not selected_option.is_correct else None
    })

@login_required
def home(request):
    courses = Course.objects.all().order_by('name')
    
    return render(request, 'quiz/home.html', {
        'courses': courses,
        'is_admin': request.user.groups.filter(name='admin').exists()
    })

@login_required
def course_subjects(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    subjects = Subject.objects.filter(course=course).order_by('name')
    
    return render(request, 'quiz/course_subjects.html', {
        'course': course,
        'subjects': subjects,
        'is_admin': request.user.groups.filter(name='admin').exists()
    })

@login_required
def register_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        
        # Create or get user
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User.objects.create_user(username=username, password=password)
            user.first_name = name
            user.save()
            
            # Create profile with phone number
            profile = UserProfile.objects.create(
                user=user,
                phone_number=phone
            )
        
        login(request, user)
        return redirect('home')
        
    return render(request, 'registration/login.html')

@login_required
def profile(request):
    # Ensure user has a profile
    try:
        user_profile = request.user.profile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)
    
    # Get user's submissions and calculate total score
    user_submissions = UserSubmission.objects.filter(user=request.user).select_related('question', 'question__subject')
    total_score = sum(submission.score for submission in user_submissions)
    
    # Get subjects where user has answered questions
    subjects_with_answers = Subject.objects.filter(
        questions__usersubmission__user=request.user
    ).distinct()
    
    # Get performance data for each subject
    subjects_data = []
    for subject in subjects_with_answers:
        subject_submissions = user_submissions.filter(question__subject=subject)
        correct_submissions = subject_submissions.filter(score__gt=0).count()
        total_questions = subject_submissions.count()
        
        subjects_data.append({
            'subject': subject,
            'correct_answers': correct_submissions,
            'total_questions': total_questions,
            'score': sum(submission.score for submission in subject_submissions)
        })
    
    return render(request, 'quiz/profile.html', {
        'user_profile': user_profile,
        'total_score': total_score,
        'subjects_data': subjects_data,
        'total_questions_answered': user_submissions.count(),
        'is_admin': request.user.groups.filter(name='admin').exists()
    })

from django.shortcuts import render, redirect
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import Group
from .models import Question, Option, UserSubmission, Course, Subject
from .serializers import (
    QuestionSerializer,
    OptionSerializer,
    UserSubmissionSerializer,
    QuestionDetailAdminSerializer
)

def is_admin_group(user):
    return user.groups.filter(name='admin').exists()

@login_required
@user_passes_test(is_admin_group)
def add_question(request):
    if not request.user.groups.filter(name='admin').exists():
        messages.error(request, "You don't have permission to add questions.")
        return redirect('home')
    
    subjects = Subject.objects.all().order_by('course__name', 'name')
    
    if request.method == 'POST':
        # Get form data
        subject_id = request.POST.get('subject')
        question_text = request.POST.get('question_text')
        positive_points = request.POST.get('positive_points')
        negative_points = request.POST.get('negative_points')
        correct_option = request.POST.get('correct_option')
        
        # Validate required fields
        if not all([subject_id, question_text, positive_points, negative_points, correct_option]):
            messages.error(request, 'All fields are required. Please ensure you have selected a correct answer.')
            return render(request, 'quiz/add_question.html', {
                'subjects': subjects,
                'form_data': request.POST  # Send back the form data to preserve user input
            })
        
        try:
            # Create question
            subject = get_object_or_404(Subject, id=subject_id)
            question = Question.objects.create(
                subject=subject,
                text=question_text,
                positive_points=int(positive_points),
                negative_points=int(negative_points)
            )
            
            # Create options
            has_correct_option = False
            for i in range(1, 5):
                option_text = request.POST.get(f'option_text_{i}')
                if not option_text:
                    messages.error(request, f'Option {i} text is required')
                    question.delete()  # Clean up the created question
                    return render(request, 'quiz/add_question.html', {
                        'subjects': subjects,
                        'form_data': request.POST
                    })
                
                is_correct = str(i) == str(correct_option)
                if is_correct:
                    has_correct_option = True
                
                Option.objects.create(
                    question=question,
                    text=option_text,
                    is_correct=is_correct
                )
            
            if not has_correct_option:
                messages.error(request, 'Please select one correct answer')
                question.delete()
                return render(request, 'quiz/add_question.html', {
                    'subjects': subjects,
                    'form_data': request.POST
                })
            
            messages.success(request, 'Question added successfully!')
            return redirect('add_question')
            
        except Exception as e:
            messages.error(request, f'Error adding question: {str(e)}')
            return render(request, 'quiz/add_question.html', {
                'subjects': subjects,
                'form_data': request.POST
            })
    
    return render(request, 'quiz/add_question.html', {'subjects': subjects})

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return QuestionDetailAdminSerializer
        return QuestionSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

class UserSubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = UserSubmissionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return UserSubmission.objects.all()
        return UserSubmission.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        question = serializer.validated_data['question']
        selected_option = serializer.validated_data['selected_option']
        
        # Verify the selected option belongs to the question
        if selected_option.question != question:
            raise serializers.ValidationError({"selected_option": "This option does not belong to the selected question"})
        
        # Calculate score based on correct/incorrect answer
        score = question.positive_points if selected_option.is_correct else -question.negative_points
        
        serializer.save(user=self.request.user, score=score)

    def create(self, request, *args, **kwargs):
        # Check if user has already submitted an answer for this question
        question_id = request.data.get('question')
        if UserSubmission.objects.filter(user=request.user, question_id=question_id).exists():
            return Response(
                {"detail": "You have already submitted an answer for this question"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().create(request, *args, **kwargs)
def user_logout(request):
        logout(request)
        return render(request, 'quiz/logout.html')   