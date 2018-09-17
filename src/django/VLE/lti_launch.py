from django.conf import settings
import oauth2
"""Package for oauth authentication in python"""

from VLE.models import User, Role, Journal, Lti_ids
import VLE.factory as factory
from datetime import datetime, timezone


class OAuthRequestValidater(object):
    """OAuth request validater class for Django Requests"""

    def __init__(self, key, secret):
        """
        Constructor which creates a consumer object with the given key and
        secret.
        """
        super(OAuthRequestValidater, self).__init__()
        self.consumer_key = key
        self.consumer_secret = secret

        self.oauth_server = oauth2.Server()
        signature_method = oauth2.SignatureMethod_HMAC_SHA1()
        self.oauth_server.add_signature_method(signature_method)
        self.oauth_consumer = oauth2.Consumer(
            self.consumer_key, self.consumer_secret
        )

    def parse_request(self, request):
        """
        Parses een django request om de method, url header en post data terug
        te geven.
        """
        headers = dict([(k, request.META[k])
                        for k in request.META if
                        k.upper().startswith('HTTP_') or
                        k.upper().startswith('CONTENT_')])

        return request.method, request.build_absolute_uri(), headers, \
            request.POST

    def is_valid(self, request):
        """
        Checks if the signature of the given request is valid based on the
        consumers secret en key
        """
        try:
            method, url, head, param = self.parse_request(request)

            oauth_request = oauth2.Request.from_request(
                method, url, headers=head, parameters=(param))

            oauth_request = oauth2.Request.from_request(
                request.method, request.build_absolute_uri(),
                headers=request.META, parameters=request.POST.dict()
            )
            self.oauth_server.verify_request(oauth_request,
                                             self.oauth_consumer, {})

        except (oauth2.Error, ValueError) as err:
            oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(),
                                       self.oauth_consumer, {})
            return False, err
        # Signature was valid
        return True, None

    @classmethod
    def check_signature(cls, key, secret, request):
        """Validate OAuth request using the python-oauth2 library.

        https://github.com/simplegeo/python-oauth2.
        """
        validator = OAuthRequestValidater(key, secret)
        return validator.is_valid(request)


def check_user_lti(request, roles):
    """Check is an user with the lti_id exists"""
    lti_user_id = request['user_id']

    users = User.objects.filter(lti_id=lti_user_id)
    if users.count() > 0:
        user = users[0]
        if 'custom_user_image' in request:
            user.profile_picture = request['custom_user_image']
            user.save()

        if roles['Teacher'] in request:
            user.is_teacher = True
            user.save()
        return user
    return None


def create_lti_query_link(names, values):
    """
    Creates link to lti page with the given parameters

    Arguments
    names -- names of the query variables
    values -- values correnspanding to the names

    returns the link
    """
    link = settings.BASELINK
    link += '/LtiLogin'
    start = '?'
    for i, name in enumerate(names):
        link += start + name + '={0}'.format(values[i])
        start = '&'
    return link


def check_course_lti(request, user, role):
    """Check is an course with the lti_id exists"""
    course_id = request['custom_course_id']
    courses = Lti_ids.objects.filter(lti_id=course_id, for_model='Course')

    if courses.count() > 0:
        course = courses[0].course
        if user not in course.users.all():
            factory.make_participation(user, course, Role.objects.get(name=role, course=course))
        return course
    return None


def check_assignment_lti(request):
    """Check is an assignment with the lti_id exists"""
    assign_id = request['custom_assignment_id']
    assignments = Lti_ids.objects.filter(lti_id=assign_id, for_model='Assignment')
    if assignments.count() > 0:
        return assignments[0].assignment
    return None


def select_create_journal(request, user, assignment, roles):
    """
    Select or create the requested journal.
    """
    if roles['Student'] in request['roles'] and assignment is not None and user is not None:
        journals = Journal.objects.filter(user=user, assignment=assignment)
        if journals.count() > 0:
            journal = journals[0]
        else:
            journal = factory.make_journal(assignment, user)

        try:
            begin = datetime.strptime(request['custom_assignment_unlock'], '%Y-%m-%d %X %z')
            end = datetime.strptime(request['custom_assignment_due'], '%Y-%m-%d %X %z')
            now = datetime.now(timezone.utc)
        except Exception as e:
            if 'custom_assignment_unlock' in request:
                print(e)

        if journal.grade_url is None or begin < now < end:
            if 'lis_outcome_service_url' in request:
                journal.grade_url = request['lis_outcome_service_url']
                journal.save()
            if 'lis_result_sourcedid' in request:
                journal.sourcedid = request['lis_result_sourcedid']
                journal.save()
    else:
        journal = None
    return journal
