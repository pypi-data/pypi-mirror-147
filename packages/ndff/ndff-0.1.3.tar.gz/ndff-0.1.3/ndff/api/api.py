
import requests
import tempfile
import os
import pickle
import json
import logging
import time

from ..api.object import (
    NdffResult,
)
from pathlib import Path

from ..utils import is_uri


class NdffApiException(Exception):

    def __init__(self, message, errors=None):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
        # custom code, list of errors?
        self.errors = errors


class Api:

    # pickled tokens are in OS-tempdir
    PICKLED_TOKENS = '{}{}{}'.format(tempfile.gettempdir(), os.sep, 'ndff_tokens')

    def __init__(self, config: dict):
        if config is None or config == {} or not isinstance(config, dict):
            raise NdffApiException('Trying to create an Api connection without any configuration!', errors=[1])
        self.config = config

        self.user = config.get('user', 'user_from_ndff_api.csv_settings')
        self.password = config.get('password', 'password_from_ndff_api.csv_settings')
        if self.user is None or len(self.user) < 2 or self.password is None or len(self.password) < 5:
            raise NdffApiException('Trying to create an Api connection without user or password, is your configuration OK?', errors=[2])

        self.api_url = config.get('api_url', 'api_url_from_ndff_api.csv_settings')
        self.token_url = config.get('token_url', 'token_url_from_ndff_api.csv_settings')
        if not is_uri(self.api_url) or not is_uri(self.token_url):
            raise NdffApiException('Trying to create an Api connection without valid api_url or token_url, is your configuration OK?', errors=[3])

        # HACK, create code url like: https://accapi.ndff.nl/codes/v2/ from api_url https://accapi.ndff.nl/api/v2/domains
        # TODO decide if this should be a setting or not...
        self.codes_url = self.api_url.replace('/api/', '/codes/').replace('/domains', '')
        # we DO want a trailing slash in api_url and codes_url
        if not self.api_url.endswith('/'):
            self.api_url += '/'
        if not self.codes_url.endswith('/'):
            self.codes_url += '/'

        self.domain = config.get('domain', 'domain_from_ndff_api.csv_settings')
        self.client_id = config.get('client_id', 'client_id_from_ndff_api.csv_settings')
        self.client_secret = config.get('client_secret', 'client_secret_from_ndff_api.csv_settings')
        if self.domain is None or len(self.domain) < 2 or self.client_id is None or len(self.client_id) < 2 or self.client_secret is None or len(self.client_secret) < 2:
            raise NdffApiException('Trying to create an Api connection without domain, client_id or client_secret, is your configuration OK?', errors=[4])

        self.access_token = False

        """
        - look for a pickled token-set in the users temp dir
        - if there: try the 'access_token':
            if it works: done, 
               just use it, but keep testing it before every call ??
            if not try the 'refresh-token' to get a fresh 'access_token'
                and pickle it to a token-set in the users temp dir
        - if still here that is either No pickles, 
            OR no working access or refresh: 
            do a token call to get fresh tokens and pickle them
        """

        if os.path.isfile(self.PICKLED_TOKENS):
            logging.debug('Found pickled tokens on disk, checking if working...')
            with open(self.PICKLED_TOKENS, 'rb') as f:
                tokens = pickle.load(f)
            if self.token_ok(tokens['access_token']):
                return  # done
            else:
                tokens = self.refresh_access_token(tokens['refresh_token'])
                if tokens and 'access_token' in tokens and self.token_ok(tokens['access_token']):
                    return  # done
        # no pickled token found OR refresh failed: just get new ones
        tokens = self.get_new_tokens()
        if tokens and 'access_token' in tokens and self.token_ok(tokens['access_token']):
            return  # done
        # if still not OK, we did all we can to either get or refresh tokens, throw an exception
        if tokens:
            raise NdffApiException(f'Failed to get or refresh NDFF Api tokens, message info: {tokens}')
        else:
            raise NdffApiException('Failed to get or refresh NDFF Api tokens, but further information not available...')

    def get_new_tokens(self):
        logging.debug('Calling api to get NEW tokens...')
        payload = {'client_id': self.client_id,
                   'client_secret': self.client_secret,
                   'grant_type': 'password',
                   'username': self.user,
                   'password': self.password}
        return self.post_save_tokens(payload)

    def refresh_access_token(self, refresh_token):
        logging.debug('Calling api to REFRESH tokens...')
        payload = {'client_id': self.client_id,
                   'client_secret': self.client_secret,
                   'grant_type': 'refresh_token',
                   'refresh_token': refresh_token}
        return self.post_save_tokens(payload)

    @staticmethod
    def remove_saved_tokens():
        """
        Remove the so called 'self.PICKLED_TOKENS' file, which is actually an
        json file like, but (python) pickled:
        {
            'access_token': 'gbBSEQBz0lb21CbJcHzYt2YPB1W35V',
            'expires_in': 86400,
            'token_type': 'Bearer',
            'scope': 'read write groups',
            'refresh_token': 'f1C3iLmVC2nmvh6Mg2FaQwK8yNiqUN'
        }
        containing an access_token to be used as valid key for authentication...

        This should be removed in case there is trouble with it (like you are
        sending an access token for a domain you do not have access to)...

        :return: True in case something is successfully removed OR there was nothing to remove
        or False in case there WAS a file but we were unable to remove...
        """
        token = Path(Api.PICKLED_TOKENS)
        if token.exists() and token.is_file():
            try:
                # try to remove it, return False in case of failing
                token.unlink(missing_ok=True)
            except Exception as e:
                logging.debug(f'Failing to unlink/remove the ndff _tokens file {e}')
                return False
            return True
        else:
            return False  # missing or non existing file

    def post_save_tokens(self, payload):
        """
        Either return valid tokens, json like:
        {
            'access_token': 'gbBSEQBz0lb21CbJcHzYt2YPB1W35V',
            'expires_in': 86400,
            'token_type': 'Bearer',
            'scope': 'read write groups',
            'refresh_token': 'f1C3iLmVC2nmvh6Mg2FaQwK8yNiqUN'
        }
        containing an access_token to be used as valid key for authentication...

        OR return an empty dict
        """
        logging.debug(f'POST to {self.token_url} data: {payload}')
        r = requests.post(self.token_url, data=payload)
        if r.status_code == 200:
            tokens = r.json()
            if True:
                with open(self.PICKLED_TOKENS, 'wb') as f:
                    pickle.dump(tokens, f)
            return tokens
        elif r.status_code == 400:
            message = f'Status = {r.status_code}, wrong credentials, or check if you are maybe using an old or wrong saved api token. Remove {self.PICKLED_TOKENS} file ??'
            logging.warning(message)
        elif r.status_code == 401:  # 401 == Unauthorized
            message = f'Status = {r.status_code} Unauthorized, did you offer the right credentials? Error message = {r.json()["error"]}'
            logging.warning(message)
        else:
            message = f'Status = {r.status_code}, r.text={r.text} r = {r}'
            logging.info(message)
        # https://stackoverflow.com/questions/2052390/manually-raising-throwing-an-exception-in-python
        raise NdffApiException(message)

    def token_ok(self, access_token):
        logging.debug("access_token/bearer: {}".format(access_token))
        headers = {'content-type': 'application/hal+json',
                   'authorization': 'Bearer {}'.format(access_token)}
        params = {'limit': 1}
        # https://accapi.ndff.nl/api/v2/domains/{domain}/observations/?limit=1
        r = requests.get(f'{self.api_url}{self.domain}/observations',
                         headers=headers, params=params)
        if r.status_code == 200:  # and r.encoding == 'application/hal+json':
            logging.info(f'OK checked access_token, seems to work: {access_token}')
            self.access_token = access_token
            return True
        else:
            logging.warning(f'Checked access_token for domain {self.domain}, seems NOT to work?')
            # detail is giving wrong info, only showing title
            # r.json()['detail']
            logging.warning('{}'.format(r.json()['title']))
            return False

    def test_connection(self) -> NdffResult:
        # https://accapi.ndff.nl/api/v2/domains/{domain}
        uri = f'{self.api_url}{self.domain}'
        headers = {'content-type': 'json',
                   'authorization': 'Bearer {}'.format(self.access_token)}
        response = requests.get(uri, headers=headers)
        return self.handle_response(response, 200, 'test_connection')

    def get_waarneming(self, ndff_id) -> NdffResult:
        if f'{ndff_id}'.upper().startswith('HTTP'):
            uri = ndff_id
        else:
            uri = '{}{}/observations/{}'.format(self.api_url,
                                                 self.domain, ndff_id)
        headers = {'content-type': 'application/json',
                   'authorization': 'Bearer {}'.format(self.access_token)}
        response = requests.get(uri, headers=headers)
        return self.handle_response(response, 200)

    def get_datasettypes(self):
        uri = f'{self.api_url}{self.domain}/datasettypes/'
        headers = {'content-type': 'json',
                   'authorization': 'Bearer {}'.format(self.access_token)}
        response = requests.get(uri, headers=headers)
        return self.handle_response(response, 200, 'test_connection')

    def get_datasets(self, uri=None):
        """
        Get all dataset from current Api user/domain.
        The idea of the 'uri' parameter is that the user checks IF there is a
        ['_links']['next'] object in the result, and IF so, that it can be
        used to get the next set/page of datasets.
        The api is NOT responsible for the aggregation of the pages, the api-user itself is.

        :param uri: potential 'next'-href to get the next page
        :return:
        """
        if uri:
            # use that one
            pass
        else:
            uri = f'{self.api_url}{self.domain}/datasets/'
        headers = {'content-type': 'json',
                   'authorization': 'Bearer {}'.format(self.access_token)}
        response = requests.get(uri, headers=headers)
        return self.handle_response(response, 200, 'test_connection')

    def search_waarneming(self, waarneming_identity) -> NdffResult:
        headers = {'content-type': 'application/hal+json',
                   'authorization': 'Bearer {}'.format(self.access_token)}
        parameters = {'identity': f'{waarneming_identity}',
                      'format': 'json'}
        response = requests.get('{}{}/observations/'
                                .format(self.api_url, self.domain),
                                headers=headers, params=parameters)
        return self.handle_response(response, 200, waarneming_identity)

    # DELETE kan nog niet worden gebruikt
    # omdat dan wel de observation resource wordt verwijderd, maar niet de
    # bijbehorende identity uri, waarmee het onmogelijk wordt om dezelfde
    # resource NOG een keer aan te maken met dezelfde identity uri
    # NEE: zie API handleiding:
    #     Wanneer een waarneming inhoudelijk wijzigt of wordt gekoppeld aan een andere
    #     waarnemer of in uw database wordt verwijderd, is het van belang dat deze mutatie ook
    #     in de NDFF terecht komt. Het is dan wel van belang dat u de juiste waarneming in de
    #     NDFF kunt verwijderen of wijzigen en daarvoor is de resource-URI of eventueel een door
    #     u opgegeven identity van belang!
    #     In de NDFF wordt een verwijderde waarneming nooit hard verwijderd. Er is altijd sprake
    #     van een soft-delete; de waarneming komt dan op een verwijder status. Wanneer
    #     dezelfde waarneming toch weer van waarde blijkt kan deze middels een wijziging met de
    #     API weer in de NDFF worden gezet. Datasets en personen kunnen niet worden verwijderd
    #     uit de NDFF met de API.
    # delete gebeurt met de volledige (voor acc en prd unieke) ndff waarneming URL
    def delete_waarneming(self, ndff_waarneming_url) -> NdffResult:
        headers = {'content-type': 'application/hal+json',
                   'authorization': 'Bearer {}'.format(self.access_token)}
        response = requests.delete(ndff_waarneming_url, headers=headers)
        return self.handle_response(response, 204, ndff_waarneming_url)

    def post_waarneming(self, ndff_waarneming_json, waarneming_id, epsg='EPSG:4326') -> NdffResult:
        headers = {'Content-Crs': f'{epsg}',
                   'content-type': 'application/json',
                   'authorization': 'Bearer {}'.format(self.access_token)}
        response = requests.post('{}{}/observations/'
                                 .format(self.api_url, self.domain),
                                 headers=headers, data=ndff_waarneming_json)
        return self.handle_response(response, 201, waarneming_id)

    def put_waarneming(self, ndff_waarneming_json, ndff_uri, waarneming_id, epsg='EPSG:4326') -> NdffResult:
        headers = {'Content-Crs': f'{epsg}',
                   'content-type': 'application/json',
                   'authorization': 'Bearer {}'.format(self.access_token)}
        # response = requests.put('{}{}/observations/{}/'
        #                         .format(self.api_url, self.domain, ndff_id),
        response = requests.put(ndff_uri,
                                headers=headers, data=ndff_waarneming_json)
        return self.handle_response(response, 200, waarneming_id)


    def search_name(self, search_text: str, search_type: str= 'taxa')  -> NdffResult:
        """
        For now ONLY search for search-text in name, like:
        https://accapi.ndff.nl/codes/v2/taxa/?name=pipi&ordering=-indexvalue
        OR search for the object via the identity uri like:
        https://accapi.ndff.nl/codes/v2/taxa/?identity=[IDENTITYURI]&ordering=-indexvalue
        :param search_text:
        :return: NdffResult
        """
        # We order on index value?? giving best result first?
        if is_uri(search_text):
            # we try to find a code based on identity
            # mmm, not url encoding needed???
            search_url = f'{self.codes_url}{search_type}/?identity={search_text}&ordering=-indexvalue'
        else:
            # try to find based on name
            search_url = f'{self.codes_url}{search_type}/?name={search_text}&ordering=-indexvalue'
        headers = {'content-type': 'application/json'}
        response = requests.get(search_url, headers=headers)
        return self.handle_response(response, ok_http_status=200)


    def search_code(self, search_text: str, search_type: str= 'extrainfo') -> NdffResult:
        """
        Search for search-text using the 'search' endpoint
        https://accapi.ndff.nl/codes/v2/extrainfo/?search=location_id
        OR search for the object via the identity uri like:
        https://accapi.ndff.nl/codes/v2/extrainfo/?identity=[IDENTITYURI]&ordering=-indexvalue
        :param search_text:
        :return: NdffResult
        """
        # We order on index value?? giving best result first?
        if is_uri(search_text):
            # we try to find a code based on identity
            # mmm, not url encoding needed???
            search_url = f'{self.codes_url}{search_type}/?identity={search_text}&ordering=-indexvalue'
        else:
            # try to find based on name
            search_url = f'{self.codes_url}{search_type}/?search={search_text}&ordering=-indexvalue'
        headers = {'content-type': 'application/json'}
        response = requests.get(search_url, headers=headers)
        return self.handle_response(response, ok_http_status=200)


    def handle_response(self, response, ok_http_status, waarneming_id='') -> NdffResult:
        json_data = {}
        ndff_uri = ''
        object_id = ''
        if response.text != '':  # there is probably a text/json content (http 204/DELETE has NO content)
            json_data = response.json()
            logging.debug('handle_response:\n{}'
                          .format(json.dumps(json_data,
                          indent=4, sort_keys=False)))
        else:
            # a DELETE does not get a json object returned, so we only have an NDFF uri to log
            waarneming_id = '0'
            ndff_uri = response.url
        http_status = response.status_code
        headers = response.headers

        if 'X-Rate-Limit-Limit' in headers.keys():
            # Willy-Bas: Wat ik kan aanraden is om de status 429 af te handelen door een wait
            #   van X-Rate-Limit-Reset+1 uit te voeren.
            # De +1 is omdat X-Rate-Limit-Reset al op 0 staat in de laatste seconde."
            logging.debug(headers['X-Rate-Limit-Limit'])
            logging.debug(headers['X-Rate-Limit-Remaining'])
            logging.debug(headers['X-Rate-Limit-Reset'])
            X_Rate_Limit_Remaining = int(headers['X-Rate-Limit-Remaining'])
            if X_Rate_Limit_Remaining < 3:
                X_Rate_Limit_Reset = 15+int(headers['X-Rate-Limit-Reset'])
                logging.debug("Hitting 'X-Rate-Limit-Limit', waiting for {} seconds...".format(X_Rate_Limit_Reset))
                print("Hitting 'X-Rate-Limit-Limit', waiting for {} seconds...".format(X_Rate_Limit_Reset))
                time.sleep(X_Rate_Limit_Reset)

        if http_status == ok_http_status:
            # in search results, the data is 'embedded'
            if '_embedded' in json_data:
                if len(json_data['_embedded']['items']) > 0:
                    # 20220413 RD: NOT going to only sent the items back, as
                    # then we are missing out on 'next' links etc etc
                    #json_data = json_data['_embedded']['items']
                    pass
                else:
                    # resetting http_status to 404 (as we received a 200)
                    http_status = 404
            if 'identity' in json_data:
                object_id = json_data['identity']
                ndff_uri = json_data['_links']['self']['href']
        else:
            logging.debug("Response NOT OK:\n{}".format(json_data))
            # Statuscodes:
            # https://acc-web02.ndff.nl/api/statuscodes/
            if response.status_code == 404:
                # a 404 is returned when trying to GET a NON-existing object
                ndff_uri = response.request.url
            elif response.status_code in (400, 409):
                # 409 is returned trying to POST an already existing object
                # 400 is returned on a PUT/POST with wrong params values
                # Try extracting the internal uri/id from the failing body:
                body = json.loads(response.request.body)
                object_id = body['identity']
            elif response.status_code == 429:
                # a 429 means too many requests in short time
                pass

        logging.debug('handle_response:\n{}'
                      .format(json.dumps(json_data,
                              indent=4, sort_keys=False)))
        ndff_result = NdffResult(
                    waarneming_id=waarneming_id,
                    object_type='observation',
                    object_id=object_id,
                    ndff_uri=ndff_uri,
                    http_method=response.request.method,
                    http_status=http_status,
                    http_response=json_data,
                    id=None,
                    tstamp=None
        )
        return ndff_result

    def print_headers(self, headers_dict):
        for header, value in headers_dict.items():
            print('{:20}: {}'.format(header, value))


if __name__ == '__main__':
    Api()
