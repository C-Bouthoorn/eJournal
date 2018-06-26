"""
permissions.py.

All the permission functions.
"""
from VLE.models import Participation

from django.forms.models import model_to_dict


def get_role(user, cID):
    """Get the role (with permissions) of the given user in the given course.

    Arguments:
    user -- user that did the request.
    cID -- course ID used to validate the request.
    """
    # First get the role ID of the user participation.
    try:
        return Participation.objects.get(user=user, course=cID).role
    except Participation.DoesNotExist:
        return None


def get_permissions(user, cID=-1):
    """Get permissions given a user.

    Get the permissions of the given user in the given course. The
    permissions are returned in dictionary format. For site-wide permissions
    when the user is not within a course, use cID == -1.

    Arguments:
    user -- user that did the request.
    cID -- course ID used to retrieve the permissions. -1 for permissions
    outside of a course.
    """
    roleDict = {}

    if user.is_admin:
        # For system wide permissions, not course specific.
        # Administrators should not be able to view grades.
        roleDict = {
            "is_admin": True,
            "can_edit_institute": True,

            "can_edit_course_roles": True,
            "can_add_course": True,
            "can_view_course_participants": True,
            "can_edit_course": True,
            "can_delete_course": True,

            "can_add_assignment": True,
            "can_view_assignment_participants": True,
            "can_delete_assignment": True,
            "can_publish_assigment_grades": False,

            "can_grade_journal": False,
            "can_publish_journal_grades": False,
            "can_edit_journal": False,
            "can_comment_journal": False
        }
    elif cID == -1:
        # No course ID was given. The user has no permissions.
        roleDict = {
            "is_admin": False,
            "can_edit_institute": False,

            "can_edit_course_roles": False,
            "can_add_course": False,
            "can_view_course_participants": False,
            "can_edit_course": False,
            "can_delete_course": False,

            "can_add_assignment": False,
            "can_view_assignment_participants": False,
            "can_delete_assignment": False,
            "can_publish_assigment_grades": False,

            "can_grade_journal": False,
            "can_publish_journal_grades": False,
            "can_edit_journal": False,
            "can_comment_journal": False
        }

        # If the user is not in a specific course, but he is a teacher, he is
        # allowed to create courses on the platform.
        if user.is_teacher:
            roleDict["can_add_course"] = True
    else:
        # The course ID was given. Return the permissions of the user as dictionary.
        role = get_role(user, cID)
        if not role:
            return {}

        roleDict = model_to_dict(role)
        roleDict['is_admin'] = False

    return roleDict


def get_assignment_permissions(user, assignment):
    """ Merge permissions from all courses that are linked to the assignment.

    If the user has the permission in any of the courses, it will have the permission
    for this assignment.
    """
    result = {}
    for course in assignment.courses.all():
        result = {key: value or (result[key] if key in result else False)
                  for key, value in get_permissions(user, course.pk).items()}
    return result


def has_permissions(user, cID, permission_list):
    """Check if the user has the needed permissions.

    Do this by checking every permission, and returning False once a permission
    is insufficient.

    Arguments:
    user -- user that did the request.
    cID -- course ID used to validate the request.
    permission_list -- the list of permissions to check.
    """
    permissions = get_permissions(user, cID)

    for permission in permission_list:
        if permission not in permissions or not permissions[permission]:
            return False

    return True


def has_permission(user, cID, permission):
    """Check if the user has the needed permissions.

    Do this by checking every permission, and returning False once a permission
    is insufficient.

    Arguments:
    user -- user that did the request.
    cID -- course ID used to validate the request.
    permission -- the permission to check.
    """
    permissions = get_permissions(user, cID)
    return permission in permissions and permissions[permission]


def has_assignment_permissions(user, assignment, permission_list):
    """Check if the user has the needed permissions.

    Do this by checking every permission, and returning False once a permission
    is insufficient.

    Arguments:
    user -- user that did the request.
    assignment -- the assignment used to validate the request.
    permissionList -- the list of permissions to check.
    """
    permissions = get_assignment_permissions(user, assignment)

    for permission in permission_list:
        if permission not in permissions or not permissions[permission]:
            return False

    return True


def has_assignment_permission(user, assignment, permission):
    """Check if the user has the assignment permission.

    Arguments:
    user -- user that did the request.
    assignment -- the assignment used to validate the request.
    permission -- the permissions to check.
    """

    permissions = get_assignment_permissions(user, assignment)
    return permission in permissions and permissions[permission]
