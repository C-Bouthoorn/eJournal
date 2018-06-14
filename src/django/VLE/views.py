from rest_framework.decorators import api_view
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse
from VLE.serializers import *


def hex_to_dec(hex):
    return int(hex, 16)


def dec_to_hex(dec):
    return hex(dec).split('x')[-1]


@api_view(['GET'])
def get_user_courses(request):
    """
    Returns the courses for an user.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'error': '401 Authentication Error'}, status=401)

    response = {'result': 'success', 'courses': []}
    for course in request.user.participant.all():
        course_obj = {
            'name': str(course.name),
            'auth': [str(u) for u in course.authors.all()],
            'date': str(course.startdate),
            'abbr': str(course.abbreviation),
            'cID': str(dec_to_hex(course.id))
        }
        response['courses'].append(course_obj)
    return JsonResponse(response)


@api_view(['GET'])
def get_course_assignments(request, cID):
    """
    Get the participants of a course.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'error': '401 Authentication Error'}, status=401)

    response = {'result': 'success', 'assignments': []}
    # TODO: check permission
    course = Course.objects.get(pk=hex_to_dec(cID))
    for assignment in course.assignment_set.all():
        assignment_obj = {
            'name': str(assignment.name),
            'auth': str(assignment.author),
            'progress': 0,
            'aID': str(dec_to_hex(assignment.id))
        }
        response['assignments'].append(assignment_obj)
    return JsonResponse(response)


@api_view(['GET'])
def get_assignment_journals(request, aID):
    """
    Get the journals of one assignment. (As teacher)
    """
    if not request.user.is_authenticated:
        return JsonResponse({'error': '401 Authentication Error'}, status=401)

    response = {'result': 'success', 'journals': []}
    # TODO: check permission
    assignment = Assignment.objects.get(pk=hex_to_dec(aID))
    for journal in assignment.journal_set.all():
        journal_obj = {
            'student': str(journal.user.username),
            'studentnumber': str("00000000"),
            'progress': {'acquired': str(10), 'total': str(10)},
            'studentPortraitPath': str('../assets/logo.png'),
            'entrieStats': {'graded': 1, 'total': 1},
            'uid': dec_to_hex(journal.id)
        }
        response['journals'].append(journal_obj)
    return JsonResponse(response)

@api_view(['GET'])
def get_student_course_journals(request, cID):
    """
    Get the student's journals of a given course.
    """
    if not request.user.is_authenticated:
       return JsonResponse({'error': '401 Authentication Error'}, status=401)

    response = {'result': 'success', 'journals': []}

    course = Course.objects.get(pk=hex_to_dec(cID))
    assignments = Assignment.objects.find(course=course)
    for assignment in assignments.all():
        journal = Journal.objects.get(assignment=assignment, user=request.user)
        journal_obj = {
            'aID': dec_to_hex(assignment.pk)
            'assignmentName': assignment.name
            'progress': {'acquired': 10, 'total': 10},
            'stats': {'graded': 1, 'total': 1},
            'jID': dec_to_hex(journal.id)
        }
        response['journals'].append(journal_obj)
    return JsonResponse(response)
