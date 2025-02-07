from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Question, Option, UserSubmission, Course, Subject, UserProfile

class OptionInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        has_correct_answer = False
        for form in self.forms:
            if not form.is_valid():
                return
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_correct', False):
                    has_correct_answer = True
        
        if not has_correct_answer:
            raise ValidationError('You must mark at least one option as correct.')

class OptionInline(admin.TabularInline):
    model = Option
    formset = OptionInlineFormSet
    extra = 4
    min_num = 4
    max_num = 4
    can_delete = True
    fields = ('text', 'is_correct')
    validate_min = True
    validate_max = True
    verbose_name = "Answer Option"
    verbose_name_plural = "Answer Options"

class SubjectInline(admin.TabularInline):
    model = Subject
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('get_name_display', 'description', 'created_at')
    inlines = [SubjectInline]
    search_fields = ('name', 'description')
    list_filter = ('created_at',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject_type', 'course', 'created_at')
    list_filter = ('subject_type', 'course', 'created_at')
    search_fields = ('name', 'description')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'subject', 'positive_points', 'negative_points', 'created_at', 'get_options_display')
    list_filter = ('subject__course', 'subject', 'created_at')
    search_fields = ('text',)
    inlines = [OptionInline]
    fieldsets = (
        (None, {
            'fields': ('subject', 'text')
        }),
        ('Scoring', {
            'fields': ('positive_points', 'negative_points'),
            'classes': ('collapse',)
        }),
    )

    def get_options_display(self, obj):
        options = obj.options.all()
        return ", ".join([f"{opt.text} ({'✓' if opt.is_correct else '✗'})" for opt in options])
    get_options_display.short_description = 'Options'

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        
        # Check for deletions and delete them first
        for obj in formset.deleted_objects:
            obj.delete()
        
        # Get all forms that are not marked for deletion
        valid_forms = [f for f in formset.forms if f.is_valid() and not f.cleaned_data.get('DELETE', False)]
        
        # Count correct options among valid forms
        correct_count = sum(1 for f in valid_forms if f.cleaned_data.get('is_correct', False))
        
        if correct_count != 1:
            raise ValidationError('Exactly one option must be marked as correct.')
        
        # Save all instances
        for instance in instances:
            instance.save()
        formset.save_m2m()

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('question', 'text', 'is_correct')
    list_filter = ('is_correct', 'question__subject')
    search_fields = ('text', 'question__text')
    raw_id_fields = ('question',)

    def get_model_perms(self, request):
        """
        Hide this model from the main admin index page.
        Options should primarily be managed through the Question admin.
        """
        return {}

@admin.register(UserSubmission)
class UserSubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'selected_option', 'score', 'created_at')
    list_filter = ('user', 'created_at', 'question__subject')
    search_fields = ('user__username', 'question__text')
    raw_id_fields = ('user', 'question', 'selected_option')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username',)
    raw_id_fields = ('user',)
