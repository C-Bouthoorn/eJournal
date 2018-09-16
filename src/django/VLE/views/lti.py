from django.conf import settings
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

import VLE.views.responses as response
import VLE.lti_launch as lti

import datetime
import json
import jwt


# VUE ENTRY STATE
BAD_AUTH = '-1'

NO_USER = '0'
LOGGED_IN = '1'

NO_COURSE = '0'
NO_ASSIGN = '1'
NEW_COURSE = '2'
NEW_ASSIGN = '3'
FINISH_T = '4'
FINISH_S = '5'
GRADE_CENTER = '6'


@api_view(['GET'])
def get_lti_params_from_jwt(request, jwt_params):
    """Handle the controlflow for course/assignment create, connect and select.

    Returns the data needed for the correct entry place.
    """
    if not request.user.is_authenticated:
        return response.unauthorized()

    user = request.user
    try:
        lti_params = jwt.decode(jwt_params, settings.LTI_SECRET, algorithms=['HS256'])
    except jwt.exceptions.ExpiredSignatureError:
        return response.forbidden(
            description='The canvas link has expired, 15 minutes have passed. Please retry from canvas.')
    except jwt.exceptions.InvalidSignatureError:
        return response.unauthorized(description='Invalid LTI parameters given. Please retry from canvas.')

    roles = json.load(open('config.json'))
    lti_roles = dict((roles[k], k) for k in roles)
    role = lti_roles[lti_params['roles']]

    payload = dict()
    course = lti.check_course_lti(lti_params, user, role)
    if course is None:
        if role == 'Teacher':
            payload['state'] = NEW_COURSE
            payload['lti_cName'] = lti_params['custom_course_name']
            payload['lti_abbr'] = lti_params['context_label']
            payload['lti_cID'] = lti_params['custom_course_id']
            payload['lti_course_start'] = lti_params['custom_course_start']
            payload['lti_aName'] = lti_params['custom_assignment_title']
            payload['lti_aID'] = lti_params['custom_assignment_id']
            payload['lti_aUnlock'] = lti_params['custom_assignment_unlock']
            payload['lti_aDue'] = lti_params['custom_assignment_due']
            payload['lti_aLock'] = lti_params['custom_assignment_lock']
            payload['lti_points_possible'] = lti_params['custom_assignment_points']

            return response.success({'params': payload})
        else:
            return response.not_found('The course you are looking for cannot be found. \
                Most likely your teacher has not finished setting up the course.')

    assignment = lti.check_assignment_lti(lti_params)
    if assignment is None:
        if role == 'Teacher':
            payload['state'] = NEW_ASSIGN
            payload['cID'] = course.pk
            payload['lti_aName'] = lti_params['custom_assignment_title']
            payload['lti_aID'] = lti_params['custom_assignment_id']
            payload['lti_aUnlock'] = lti_params['custom_assignment_unlock']
            payload['lti_aDue'] = lti_params['custom_assignment_due']
            payload['lti_aLock'] = lti_params['custom_assignment_lock']
            payload['lti_points_possible'] = lti_params['custom_assignment_points']

            return response.success({'params': payload})
        else:
            return response.not_found('The assignment you are looking for cannot be found. \
                Either your teacher has not finished setting up the assignment, or it has been moved to another \
                course. Please contact your course administrator.')

    journal = lti.select_create_journal(lti_params, user, assignment, roles)
    jID = journal.pk if journal is not None else None
    state = FINISH_T if jID is None else FINISH_S

    payload['state'] = state
    payload['cID'] = course.pk
    payload['aID'] = assignment.pk
    payload['jID'] = jID
    return response.success(payload={'params': payload})


@api_view(['POST'])
def lti_launch(request):
    """Django view for the lti post request.

    Verifies the given LTI parameters based on our secret, if a user can be found based on the verified parameters
    a redirection link is send with corresponding JW access and refresh token to allow for a user login. If no user
    can be found on our end, but the LTI parameters were verified nonetheless, we are dealing with a new user and
    redirect with additional parameters that will allow for the creation of a new user.

    If the parameters are not validated a redirection is send with the parameter state set to BAD_AUTH.
    """
    secret = settings.LTI_SECRET
    key = settings.LTI_KEY

    authenticated, err = lti.OAuthRequestValidater.check_signature(
        key, secret, request)

    if authenticated:
        roles = json.load(open('config.json'))
        params = request.POST.dict()

        user = lti.check_user_lti(params, roles)

        params['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
        lti_params = jwt.encode(params, secret, algorithm='HS256').decode('utf-8')

        if user is None:
            q_names = ['state', 'lti_params']
            q_values = [NO_USER, lti_params]

            if 'custom_user_full_name' in params:
                fullname = params['custom_user_full_name']
                splitname = fullname.split(' ')
                firstname = splitname[0]
                lastname = fullname[len(splitname[0])+1:]
                q_names += ['firstname', 'lastname']
                q_values += [firstname, lastname]

            if 'custom_username' in params:
                q_names.append('username')
                q_values.append(params['custom_username'])

            if 'custom_user_email' in params:
                q_names.append('email')
                q_values.append(params['custom_user_email'])

            return redirect(lti.create_lti_query_link(q_names, q_values))

        refresh = TokenObtainPairSerializer.get_token(user)
        access = refresh.access_token
        return redirect(lti.create_lti_query_link(['lti_params', 'jwt_access', 'jwt_refresh', 'state'],
                                                  [lti_params, access, refresh, LOGGED_IN]))

    return redirect(lti.create_lti_query_link(['state'], [BAD_AUTH]))
