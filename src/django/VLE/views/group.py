"""
group.py.

In this file are all the group api requests.
"""
from rest_framework import viewsets

import VLE.factory as factory
import VLE.utils.generic_utils as utils
import VLE.utils.responses as response
from VLE.models import Course, Group
from VLE.serializers import GroupSerializer


class GroupView(viewsets.ViewSet):
    def list(self, request):
        """Get the groups from a course for the user.

        Arguments:
        request -- request data
            course_id -- course ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not found -- when the course does not exists
            forbidden -- when the user is not part of the course
        On succes:
            success -- with the group data

        """
        course_id, = utils.required_typed_params(request.query_params, (int, 'course_id'))

        course = Course.objects.get(pk=course_id)

        if not (request.user.has_permission('can_view_course_users', course) or
                request.user.has_permission('can_edit_course_user_group', course) or
                request.user.has_permission('can_add_course_user_group', course) or
                request.user.has_permission('can_delete_course_user_group', course)):
            return response.forbidden('You are not allowed to view or manage the user groups of this course.')

        queryset = Group.objects.filter(course=course)
        serializer = GroupSerializer(queryset, many=True, context={'user': request.user, 'course': course})

        return response.success({'groups': serializer.data})

    def create(self, request):
        """Create a new course group.

        Arguments:
        request -- the request that was send with
            name -- name of the course group
            course_id -- course ID of the course
            lti_id -- (optional) lti_id to link the course to

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            forbidden -- when the user has no permission to create new groups
        On success, with the course group.
        """
        name, course_id = utils.required_params(request.data, "name", "course_id")
        lti_id = utils.optional_params(request.data, 'lti_id')

        course = Course.objects.get(pk=course_id)

        request.user.check_permission('can_add_course_user_group', course)

        if Group.objects.filter(name=name, course=course).exists():
            return response.bad_request('Course group with that name already exists.')

        course_group = factory.make_course_group(name, course, lti_id)
        serializer = GroupSerializer(course_group, many=False)
        return response.created({'group': serializer.data})

    def partial_update(self, request, *args, **kwargs):
        """Update an existing course group.

        Arguments:
        request -- request data
        data -- the new data for the course group
        pk -- course ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not found -- when the course does not exists
            forbidden -- when the user is not in the course
            unauthorized -- when the user is unauthorized to edit the course
            bad_request -- when there is invalid data in the request
        On success:
            success -- with the new course data
        """
        old_group_name, new_group_name = utils.required_params(request.data, 'old_group_name', 'new_group_name')

        course_id, = utils.required_typed_params(kwargs, (int, 'pk'))
        course = Course.objects.get(pk=course_id)
        group = Group.objects.get(name=old_group_name, course=course)

        request.user.check_permission('can_edit_course_user_group', course)

        if not new_group_name:
            return response.bad_request('Group name is not allowed to be empty.')

        if Group.objects.filter(name=new_group_name, course=course).exists():
            return response.bad_request('Course group with that name already exists.')

        serializer = GroupSerializer(group, data=request.data, partial=True)
        if not serializer.is_valid():
            response.bad_request()

        serializer.save()
        return response.success({'group': serializer.data})

    def destroy(self, request, *args, **kwargs):
        """Delete an existing course group.

        Arguments:
        request -- request data
            group_name -- name of the course
        pk -- course ID

        Returns:
        On failure:
            not found -- when the course does not exists
            unauthorized -- when the user is not logged in
            forbidden -- when the user is not in the course
        On success:
            success -- with a message that the course group was deleted
        """
        course_id, = utils.required_typed_params(kwargs, (int, 'pk'))
        name, = utils.required_typed_params(request.query_params, (str, 'group_name'))

        course = Course.objects.get(pk=course_id)

        request.user.check_permission('can_delete_course_user_group', course)

        group = Group.objects.get(name=name, course=course)
        group.delete()
        return response.success(description='Successfully deleted course group.')
