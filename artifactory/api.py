import requests, json
from six.moves.urllib.parse import quote, urlencode, urljoin
from .exceptions import ArtifactoryException, NotFoundException, EmptyResponseException, BadHTTPException, TimeoutException

class Artifactory(object):
    #Endpoint
    USERSLIST = 'api/security/users'
    USERINFO = 'api/security/users/%(userName)s'
    
    #default http headers 
    #DEFAULT_HEADERS = {'Content-Type': 'text/xml; charset=utf-8'}
    DEFAULT_HEADERS = {'Content-Type': 'text/xml'}
    
    def __init__(self, url, username = None, password = None, timeout = 10):
        '''Create handle to Artifactory instance.
        All methods will raise :class:`ArtifactoryException` on failure.
        
        :param username(str): Server username
        :param password(str): Server password
        :param url(str): URL of Artifactory server
        :param timeout(int): Server connection timeout in secs (default: 10)
        '''
        self._timeout = timeout
        self._session = requests.Session()
        if url[-1] == '/':
            self._server = url
        else:
            self._server = url + '/'
        if username is not None and password is not None:
            self._session.auth = username, password
        else:
            self._session.auth = None

    
    def _build_url(self, endpoint, variables=None):
        '''Return the complete url including server url for a given endpoint.

        :param endpoint(str): service endpoint
        :return(str): complete url (including server url)
        '''
        if variables:
            url_path = endpoint % variables
        else:
            url_path = endpoint

        return urljoin(self._server, url_path)
    

    def _make_call(self, method, full_url, headers = {}, **data):
        '''Make the call to the service with the given method, queryset and data,
        using the initial session.

        :param method(str): http method (get, post, put, patch, delete)
        :param full_url(str): full url to make the call
        :param data(dict): http body
        :return(str): response
        '''
        #set session header info
        self._session.headers = headers or self.DEFAULT_HEADERS
        
        # Get method and make the call
        call = getattr(self._session, method.lower())

        #get timeout error
        try:
            if 'Content-Type' in self._session.headers and self._session.headers['Content-Type'] == 'application/json':
                response = call(full_url, timeout = self._timeout, data=json.dumps(data or {}))
            else:
                response = call(full_url, timeout = self._timeout, data=data or {})
        except requests.exceptions.ConnectTimeout:
            raise TimeoutException('the server connection timed out[%s]' % full_url)            

        # Analyse response status and return or raise exception
        if response.ok is False:
            if response.status_code == 400:
                #Bad Request
                raise BadHTTPException("Error communicating with server[%s]: %s"% (
                    response.url, response.reason))
            
            elif response.status_code in (401, 403):
                #Auth error
                raise ArtifactoryException(
                    'Possibly authentication failed [%s]: %s' % (
                        response.url, response.reason))

            elif response.status_code == 404:
                #Not Found
                raise NotFoundException('Error in request[%s]: can not found the page' % response.url)

            else:
                #other error
                raise ArtifactoryException('Error in request[%s]: %s' % (
                    response.url, response.reason))
        else:
            if method.lower() == 'get':
                if not response.text.strip():
                    raise EmptyResponseException(
                        'Error communicating with server[%s]: '
                        'empty response' % response.url)
            
        return response.text
        
        
    def get_users_list(self):
        '''Get the users list

        :return(list): Contains a list of all users
        '''
        response  = self._make_call(
            'get',
            self._build_url(self.USERSLIST, locals()),
            self.DEFAULT_HEADERS
            )
        return [i['name'] for i in json.loads(response)]


    def get_user_name(self, userName):
        '''Return the name of a user using the API.
        That is roughly an identity method which can be used to quickly verify
        a user exist or is accessible without causing too much stress on the
        server side.
        
        :param userName(str): user name
        :return(str): Name of user or None
        '''
        try:
            response = self._make_call(
                'get',
                self._build_url(self.USERINFO, locals()),
                self.DEFAULT_HEADERS
                )
        except NotFoundException:
            return None
        else:
            return userName

        
    def user_exists(self, name):
        '''Check whether a user exists

        :param userName(str): user name
        :return(boolean): if user exists then return True else return False
        '''
        if self.get_user_name(name):
            return True
        else:
            return False
    
        
    def get_user_info(self, userName):
        '''Get the user detail info

        :param userName(str): user name
        :return(dict): Contains a list of all users 
        '''
        #if user does not exists then raise error
        if not self.user_exists(userName):
            raise ArtifactoryException('user [%s] does not exist.' % userName)
        
        response = self._make_call(
            'get',
            self._build_url(self.USERINFO, locals()),
            self.DEFAULT_HEADERS
            )
        return json.loads(response)


    def create_user(self, userName, password, mail):
        '''Create a new artifactory user

        :param userName(str): user name
        :param password(str): password for user
        :param mail(str): mail for user
        :return(boolean): if create user success then return true or return false
        '''
        #determine whether the user exists, if user exists then raise error
        if self.user_exists(userName):
            raise ArtifactoryException('the user [%s] already exists' % userName)

        #http body data
        post_data = {
            'realm': 'internal',
            'name': userName,
            'password': password,
            'admin': False,
            'lastLoggedInMillis': 0,
            'disableUIAccess': False,
            'profileUpdatable': True,
            'internalPasswordDisabled': False,
            'offlineMode': False,
            'email': mail
            }

        #http headers data
        headers = {
            'Content-Type': 'application/json'
            }
        
        response = self._make_call(
            'put',
            self._build_url(self.USERINFO, locals()),
            headers,
            **post_data
            )

        #verify that the user was created successfully
        if self.user_exists(userName):
            return True
        else:
            raise ArtifactoryException('the user [%s] create Failed' % userName)        






        


