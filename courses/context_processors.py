from .models import Subject


def active_categories(request):
    return {
        'all_categories': Subject.ordered_active_subjects()
    }
