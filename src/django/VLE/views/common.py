"""
common.py.

In this file are all the extra api requests.
This includes:
    /names/ -- to get the names belonging to the ids
"""
from rest_framework.decorators import api_view

import VLE.views.responses as response
from VLE.models import Course, Journal, Assignment, Template
import VLE.permissions as permissions


@api_view(['GET'])
def names(request, course_id, assignment_id, journal_id):
    """Get names of course, assignment, journal.

    Arguments:
    request -- the request that was sent
        course_id -- optionally the course id
        assignment_id -- optionally the assignment id
        journal_id -- optionally the journal id

    Returns a json string containing the names of the set fields.
    course_id populates 'course', assignment_id populates 'assignment', tID populates
    'template' and journal_id populates 'journal' with the users' name.
    """
    print(assignment_id)
    if not request.user.is_authenticated:
        return response.unauthorized()

    result = {}
    try:
        if course_id:
            course = Course.objects.get(pk=course_id)
            role = permissions.get_role(request.user, course)
            if role is None:
                return response.forbidden('You are not allowed to view this course.')
            result['course'] = course.name
        if assignment_id:
            if assignment_id == '-1':
                result['assignment'] = 'New Assignment'
            else:
                assignment = Assignment.objects.get(pk=assignment_id)
                if not (assignment.courses.all() & request.user.participations.all()):
                    return response.forbidden('You are not allowed to view this assignment.')
                result['assignment'] = assignment.name
        if journal_id:
            journal = Journal.objects.get(pk=journal_id)
            if not (journal.user == request.user or permissions.has_assignment_permission(request.user,
                    journal.assignment, 'can_view_assignment_participants')):
                return response.forbidden('You are not allowed to view journals of other participants.')
            result['journal'] = journal.user.first_name + " " + journal.user.last_name

    except (Course.DoesNotExist, Assignment.DoesNotExist, Journal.DoesNotExist, Template.DoesNotExist):
        return response.not_found('Course, Assignment, Journal or Template does not exist.')

    return response.success({'names': result})
