from oaipmh import common, error
from oaipmh.datestamp import datestamp_to_datetime
from datetime import datetime
from flask import abort
from dateutil import parser
import requests
import json
import pytz
import logging
import memcache
import redis
import pickle
import urllib3
from ssio_xml_output import *

from oai_auth import auth_info

log = logging.getLogger()



class SharedShelfServerCommon(object):
    def identify(self):
        session = self._ss_init(verb='Identify')
        return common.Identify(
            repositoryName='SharedShelf',
            baseURL='http://%s:9981' % session.hostname,
            protocolVersion="2.0",
            adminEmails=['bogus@artstor.org'],
            earliestDatestamp=datetime(1900, 1, 1),
            deletedRecord='persistent',
            granularity='YYYY-MM-DDThh:mm:ssZ',
            compression=['identity'])

    def listMetadataFormats(self, identifier=None):
        if identifier == "oai_dc":
            return [('oai_dc', 'http://www.openarchives.org/OAI/2.0/oai_dc.xsd',
                     'http://www.openarchives.org/OAI/2.0/oai_dc/')]
        elif identifier == "oai_ssio":
            return [('oai_ssio', NS_XSISSIO, NS_OAISSIO)]
        elif identifier is None:
            return [('oai_dc', 'http://www.openarchives.org/OAI/2.0/oac_dc.xsd',
                     'http://www.openarchives.org/OAI/2.0/oai_dc/'),
                    ('oai_ssio', NS_XSISSIO, NS_OAISSIO)]
        else:
            raise error.IdDoesNotExistError, "Id does not exist: %s" % identifier

    def getRecord(self, metadataPrefix, identifier):
        session = self._ss_init()
        myrecord = None

        myfrom, myuntil = self._MungeDates(None, None)

        projlist = session.SetList[unicode(session.institution)]
        for p, d, x in projlist:
            target = session.Set2OAIDC[int(p)][0]                           # should only be a single target for OAI DC
            # self._ss_GetFieldDefs(p, session.institution)

            if self._ss_DoesProjectContainWork(p):
                # if project has work, then the indentifier is a workid
                disp_ids = self._ss_GetDisplayByWork(identifier)
                # print "any disp_ids come back: ", disp_ids
                if len(disp_ids) == 0:
                    print "trying asset"
                    # no work found, maybe this is an asset id
                    status, asset, ts = self._ss_GetAsset(identifier, p, target)
                    if asset is not None:
                        try:
                            pub_status = asset['assets'][0]['publication_statuses']
                        except:
                            pub_status = None
                        if self.session.work_field in asset['assets'][0]:
                            workid = self._ss_GetWorkByCompositeKey(asset['assets'][0][self.session.work_field]['links'][0]['source_id'])
                            disp_ids = self._ss_GetDisplayByWork(workid)
                            if len(disp_ids) == 0:
                                myrecord = self._ss_BuildSimpleSSIORecord(identifier,
                                                                      p,
                                                                      pub_status,
                                                                      target,
                                                                      status=status,
                                                                      ts=ts)
                            else:
                                myrecord = self._ss_BuildComplexSSIORecord([identifier],
                                                           workid,
                                                           p,
                                                           # pub_status,
                                                           target,
                                                           myfrom=myfrom,
                                                           myuntil=myuntil)
                                                           # status=status,
                                                           # ts=ts)
                        if myrecord is not None:
                            break
                    else:
                        myrecord = None
                else:
                    # disp_ids = [ '96696', '96692' ]
                    # identifier = 'ZGJPCDYAT711132323330234017-OLIVIAIO'
                    myrecord = self._ss_BuildComplexSSIORecord(disp_ids,
                                                           identifier,
                                                           p,
                                                           # pub_status,
                                                           target,
                                                           myfrom=myfrom,
                                                           myuntil=myuntil)
                                                           # status=status,
                                                           # ts=ts)
                    if myrecord is not None:
                        break
            else:
                # need to make sure asset is actually published to OAI
                status, asset, ts = self._ss_GetAsset(identifier, p, target)
                if status != 'NoID':
                    if metadataPrefix == "oai_dc":
                        myrecord = self._ss_BuildSimpleRecord(identifier,
                                                              target,
                                                              status=status,
                                                              ts=ts)
                    elif metadataPrefix == "oai_ssio":
                        try:
                            pub_status = asset['assets'][0]['publication_statuses']
                        except:
                            pub_status = None
                        if self._ss_DoesProjectContainWork(p):
                            if asset is not None and self.session.work_field in asset['assets'][0]:
                                work_id = asset['assets'][0][self.session.work_field]['links'][0]['id']
                                myrecord = self._ss_BuildComplexSSIORecord([identifier],
                                                                       work_id,
                                                                       p,
                                                                       pub_status,
                                                                       target,
                                                                       myfrom=myfrom,
                                                                       myuntil=myuntil,
                                                                       status=status,
                                                                       ts=ts)
                            else:
                                myrecord = self._ss_BuildSimpleSSIORecord(identifier,
                                                                      p,
                                                                      pub_status,
                                                                      target,
                                                                      status=status,
                                                                      ts=ts)
                        else:
                            myrecord = self._ss_BuildSimpleSSIORecord(identifier,
                                                                  p,
                                                                  pub_status,
                                                                  target,
                                                                  status=status,
                                                                  ts=ts)
                    else:
                        raise error.CannotDisseminateFormatError, "Unknown metadata format: %s" % metadataPrefix
                    break
                else:
                    myrecord = None

        if myrecord is not None:
            return myrecord
        else:
            print "getRecord raise error"
            raise error.IdDoesNotExistError, "Id does not exist: %s" % identifier

    def listSets(self, cursor=0, batch_size=10):
        # self.SetList contains a dictionary of valid sets
        ## key is the SS project id
        # value is he list of OAI expected data
        result = []
        session = self._ss_init()

        # future planning for resumption tokens in listSets to use cursor and batch_size
        for inst in session.SetList.keys():
            if unicode(inst) == unicode(self.session.institution):
                for myset in session.SetList[inst]:
                    result.append(myset)
        return result

    def _ss_init(self, verb=None):
        self._ss_newSession()
        env = self._ss_whichEnv()
        if env == 'Unknown':
            print "Environment Unknown, configuration issue"
            abort(404)
        self._ss_seedEnv(env)
        self._memcache_init()
        self._elastic_search_init()
        # self._redis_init()
        # print "is redis alive: ", self.redis_active

        # verb Identify can skip this, all others should build the lists
        # once build in the persistant lists, this can go away
        if verb is None:
            self._ss_BuildLists()
            self.session.project_assets = dict()
            self.session.ssn_token = self._inst_to_ssn_token(self.session.institution,
                                                             self.session.adl_url,
                                                             self.session.ssn_url)
        return self.session

    def _elastic_search_init(self):
        self.session.pool = urllib3.connection_from_url(self.session.es_url, timeout=300, maxsize=10)

    def _cache_init(self):
        self._redis_init()

    def _cache_set(self, key, value, timeout=300):
        # print "cache set: ", key, value, timeout
        return self._redis_set(key, value, timeout=timeout)

    def _cache_get(self, key, timeout=300):
        return self.redis_get(key, timeout=timeout)

    def _redis_init(self):
        self.redis = redis.StrictRedis()  # defaults in use - localhost and port 6379
        self._redis_validate()

    def _memcache_init(self):
        self.memcache = memcache.Client(['127.0.0.1:11211'], debug=1, server_max_value_length=0)
        self._memcache_validate()

    def _redis_get(self, key, timeout=300):
        try:
            value = self.redis.get(key)
            if value:
                self.redis.setex(key, timeout, value)
            return pickle.loads(value)
        except:
            return None

    def _memcache_get(self, key, timeout=300):
        try:
            value = self.memcache.get(key)
            # print "retrieved: ", value
            if value:
                # reset the expiry timer to "timeout" if found
                self.memcache.set(key, value, timeout)
            return value
        except:
            return None

    def _redis_set(self, key, value, timeout=300):
        return self.redis.setex(key, timeout, pickle.dumps(value))

    def _memcache_set(self, key, value, timeout=300):
        # print "setting value: ", value
        status = self.memcache.set(key, value, timeout, 1)
        if not status:

        # if not self.memcache.set(key, value, timeout):
            return False
        else:
            return True

    def _redis_validate(self):
        orig_val = "test that redis is alive"
        key = "oai-redis-validation"
        if self._redis_set(key, orig_val, timeout=5):
            new_val = self._redis_get(key, timeout=5)
            # print "got back: ", new_val
        else:
            new_val = None

        if orig_val == new_val:
            self.redis_active = True
        else:
            log.error("redis is not available")
            abort(503)

    def _memcache_validate(self):
        orig_val = "test that memcache is alive"
        key = "oai-memcache-validation"
        if self._memcache_set(key, orig_val, timeout=5):
            new_val = self._memcache_get(key, timeout=5)
        else:
            new_val = None

        if orig_val == new_val:
            self.memcache_active = True
        else:
            self.memcache_active = False
            log.error("Memcache is not available")
            abort(503)

    def _ss_newSession(self):
        self.session = requests.Session()

    def _ss_seedEnv(self, env):
        self.session.institution = auth_info.inst
        self.session.memcache_master_key = "oai-institution-%s" % self.session.institution

        if env == 'DEV':
            # self.session.host_url = 'http://127.0.0.1:6544'
            # self.session.hostname = 'development.artstor.org'
            # self.session.oai_pub_target = 5
            # self.session.tgn_url = 'http://192.168.11.74:8282/TGNServices/json'
            # self.session.aat_url = 'http://192.168.11.74:8282/AATServices/json'
            # self.session.ssn_url = 'http://192.168.90.188:5050/VWServices'
            # self.session.adl_url = 'http://localhost:8989'
            self.session.host_url = 'http://192.168.11.112:6543'
            self.session.hostname = '63.116.88.39'
            self.session.oai_pub_target = 5
            self.session.tgn_url = 'http://192.168.11.74:8282/TGNServices/json'
            self.session.aat_url = 'http://192.168.11.74:8282/AATServices/json'
            self.session.ssn_url = 'http://192.168.11.112:5050/VWServices'
            self.session.adl_url = 'http://library.qa.artstor.org'
            self.session.wrk_url = 'http://192.168.11.112:5050/service/api/work/json'
            # self.session.wrk2_url = 'http://192.168.11.112:6060/service/api/work/json'
            self.session.es_url = 'http://192.168.11.112:9200'
        if env == 'QA':
            self.session.host_url = 'http://192.168.11.74'
            self.session.hostname = 'qa.artstor.org'
            self.session.oai_pub_target = 8
            self.session.tgn_url = 'http://192.168.11.74:8282/TGNServices/json'
            self.session.aat_url = 'http://192.168.11.74:8282/AATServices/json'
            self.session.ssn_url = 'http://192.168.11.74:9090/VWServices'
            self.session.adl_url = 'http://library.qa.artstor.org'
        if env == 'STAGE':
            self.session.host_url = 'http://192.168.90.189'
            self.session.hostname = 'stage.artstor.org'
            self.session.oai_pub_target = 4
            self.session.tgn_url = 'http://192.168.90.189:8282/TGNServices/json'
            self.session.aat_url = 'http://192.168.90.189:8282/AATServices/json'
            self.session.ssn_url = 'http://192.168.90.189:9090/VWServices'
            self.session.adl_url = 'http://library.qa.artstor.org'
        if env == 'PREQA':
            self.session.host_url = 'http://192.168.11.112:6543'
            self.session.hostname = '63.116.88.39'
            self.session.oai_pub_target = 5
            self.session.tgn_url = 'http://192.168.11.74:8282/TGNServices/json'
            self.session.aat_url = 'http://192.168.11.74:8282/AATServices/json'
            self.session.ssn_url = 'http://192.168.11.112:5050/VWServices'
            self.session.adl_url = 'http://library.qa.artstor.org'
            self.session.wrk_url = 'http://192.168.11.112:5050/service/api/work/json'
            self.session.es_url = 'http://192.168.11.112:9200'

    def _ss_whichEnv(self):
        import socket

        try:
            # get the host info
            host_info = socket.gethostbyaddr(socket.gethostname())
            hname = host_info[1][0]
            ip = host_info[2][0]
            if ip == '127.0.0.1':
                return 'DEV'
            elif ip == '192.168.11.74' or hname == 'spot02':
                return 'QA'
            elif ip == '192.168.90.189' or hname == 'stagess':
                return 'STAGE'
            elif ip == '192.168.11.112' or hname == 'kaltura':
                return 'PREQA'
            else:
                return 'Unknown'
        except:
            # if unable to resolve hostname/ip, then should only be on a dev system
            return 'DEV'

    def _inst_to_ssn_token(self, inst, adl_url, ssn_url):
        key = "OAI-ssn-key-%s" % inst
        value = self._memcache_get(key, 300)
        if value:
            return value
        else:
            try:
                key = "OAI-ssn-key-%s" % inst
                resp = self.session.get('%s/library/secure/user?_method=ssprofiles&instId=%s' % (adl_url, inst))
                user = json.loads(resp.text)[0]['profileId']
            except:
                log.error('ADL Service responded: %s' % resp.text)
                abort(503)
            try:
                resp = requests.get('%s/userManagement/json/authenticate?adlUserid=%s&instituteId=%s&expiry=24' %
                                    (ssn_url, user, inst))
                self._memcache_set(key, json.loads(resp.text)['authToken'], 300)
                return json.loads(resp.text)['authToken']
            except:
                log.error('SSN Service responded: %s' % resp.text)
                abort(503)

    def _CheckIfValidSet(self, inst, oai_set):
        for p, d, x in self.session.SetList[inst]:
            if p == unicode(oai_set):
                return [[p, d, x]]
        raise error.NoRecordsMatchError, "Invalid set %s specified" % oai_set

    def _GetPubTarget(self, session, project, metadataPrefix):
        return session.Set2OAIDC[int(project)]                # should only be a single target for OAI DC

    def _MungeDates(self, from_, until_):
        if from_ is not None:
            from_ = self._ConvertDateFormat(from_)
        else:
            from_ = self._ConvertDateFormat(datetime(1900, 1, 1))

        if until_ is not None:
            until_ = self._ConvertDateFormat(until_)
        else:
            until_ = self._ConvertDateFormat(datetime.utcnow())
        return from_, until_

    def _ConvertDateFormat(self, olddate):
        return pytz.utc.localize(olddate).astimezone(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")

    def _FixDate(self, olddate):
        if '+' in olddate:
            s = olddate.split('+')
            return s[0] + 'Z'
        else:
            return olddate

    def _ss_ListsAvailable(self):
        key = "%s-OAIListDC" % self.session.memcache_master_key
        if self._memcache_get(key):
            return True
        else:
            return False

    def _ss_FetchLists(self):
        self.session.OAIListDC = self._memcache_get("%s-OAIListDC" % self.session.memcache_master_key)
        self.session.OAIListSSIO = self._memcache_get("%s-OAIListSSIO" % self.session.memcache_master_key)
        self.session.SetList = self._memcache_get("%s-SetList" % self.session.memcache_master_key)
        self.session.Set2OAIDC = self._memcache_get("%s-Set2OAIDC" % self.session.memcache_master_key)
        self.session.PubTargets = self._memcache_get("%s-PubTargets" % self.session.memcache_master_key)
        self.session.TargetDefs = self._memcache_get("%s-TargetDefs" % self.session.memcache_master_key)

    def _ss_SaveLists(self):
        self._memcache_set("%s-OAIListDC" % self.session.memcache_master_key, self.session.OAIListDC, timeout=300)
        self._memcache_set("%s-OAIListSSIO" % self.session.memcache_master_key, self.session.OAIListSSIO, timeout=300)
        self._memcache_set("%s-SetList" % self.session.memcache_master_key, self.session.SetList, timeout=300)
        # self._cache_set("%s-SetList" % self.session.memcache_master_key, self.session.SetList, timeout=300)
        self._memcache_set("%s-Set2OAIDC" % self.session.memcache_master_key, self.session.Set2OAIDC, timeout=300)
        self._memcache_set("%s-PubTargets" % self.session.memcache_master_key, self.session.PubTargets, timeout=300)
        self._memcache_set("%s-TargetDefs" % self.session.memcache_master_key, self.session.TargetDefs, timeout=300)

    def _ss_BuildLists(self):
        if self._ss_ListsAvailable():
            self._ss_FetchLists()
        else:
            resp = json.loads(self._fetch_content('%s/institutions' % self.session.host_url))
            self.session.OAIListDC = dict()
            self.session.OAIListSSIO = dict()
            self.session.SetList = dict()
            self.session.Set2OAIDC = dict()
            self.session.PubTargets = dict()

            for inst in resp:
                self.session.OAIListDC[inst['id']] = []
                self.session.SetList[inst['id']] = []
                for proj in inst['children']:
                    pid = proj['id']
                    self.session.Set2OAIDC[pid] = []
                    pname = proj['text']
                    mytargets = json.loads(self._fetch_content('%s/admin/projects/%s/publishing-targets' % (self.session.host_url, proj['id'])))
                    for pubtarget in mytargets['publishing_targets']:
                        if pubtarget['target_id'] == self.session.oai_pub_target:
                            self.session.OAIListDC[inst['id']].append(pubtarget['id'])
                            self.session.SetList[inst['id']].append([unicode(pid), pname, ''])
                            self.session.Set2OAIDC[pid].append(pubtarget['id'])

                        # PubTargets contains all publishing targets for use when generating SSIO records
                        self.session.PubTargets[pubtarget['id']] = pubtarget

            self.session.TargetDefs = self._ss_BuildTargets()
            self._ss_SaveLists()

    def _ss_BuildTargets(self):
        targets = dict()
        # resp = self.session.get('%s/targets' % self.session.host_url)
        alltargets = json.loads(self._fetch_content('%s/targets' % self.session.host_url))
        for target in alltargets['targets']:
            targets[target['id']] = target

        return targets

    def _ss_GetDisplayByWork(self, id):
        ids = []
        counter = 1
        alldisp = json.loads(self._fetch_content('%s/getDisplayRecordsByWork?workIndexID=%s&authToken=123' % (self.session.wrk_url, id)))
        if 'display' in alldisp:
            while counter <= len(alldisp['display']):
                for dr in alldisp['display']:
                    if dr['sequence'] == unicode(counter) and dr['id'] not in ids:
                        ids.append(str(dr['id']))
                counter += 1
        else:
            log.error("getDisplayRecordsByWork failed to return valid results")
            abort(503)
        return ids

    def _ss_GetWorkByCompositeKey(self, id):
        work = json.loads(self._fetch_content('%s/getWorkXmlByCompositeKey?compositeKey=%s&authToken=123' % (self.session.wrk_url, id)))
        if 'workIndexId' in work:
            return work['workIndexId']
        else:
            return None

    def _ss_GetAssetStatus(self, project, target):
        if project not in self.session.project_assets.keys():
            key = "%s-project-%d-target-%d" % (self.session.memcache_master_key, int(project), int(target))
            cached_value = self._memcache_get(key, timeout=300)
            if cached_value:
                self.session.project_assets[project] = cached_value
            else:
                self.session.project_assets[project] = json.loads(self._fetch_content('%s/projects/%s/asset-statuses/%s' % (self.session.host_url, project, int(target))))
                self._memcache_set(key, self.session.project_assets[project], timeout=300)

    def _ss_GetAsset(self, identifier, project, target=None):
        # session = self.session

        identifier = unicode(identifier)
        # check if status of the id, is deleted or suppressed, and return status, otherwise return a record
        self._ss_GetAssetStatus(project, target)
        try:
            ts = self.session.project_assets[project]['assets'][identifier]['updated']
            if self.session.project_assets[project]['assets'][identifier]['deleted']:
                # print "deleted"
                return 'Deleted', None, ts
            elif self.session.project_assets[project]['assets'][identifier]['status'] == 'Suppressed':
                # print "suppressed"
                return 'Suppressed', None, ts
            else:
                # print "check live"
                asset = self._ss_GetLiveAsset(identifier, project, target)
                if asset:
                    return 'Active', asset, ts
                else:
                    return 'NoID', None, None
        except KeyError:
            # print "keyerror?"
            return 'NoID', None, None

    def _ss_GetLiveAsset(self, identifier, project, target=None):
        # print "fetching asset in project: ", project
        if target:
            data = dict(filter='[{"type":"numeric","comparison":"eq","value":%s,"field":"id"},'
                                '{"type":"list","value":["Published"],"field":"publication_statuses.status"}]' %
                                identifier, publishing_target_id=target, with_meta="false")
        else:
            data = dict(filter='[{"type":"numeric","comparison":"eq","value":%s,"field":"id"}]'
                                % identifier, with_meta="false")

        # resp = session.get('%s/projects/%s/assets' % (self.session.host_url, project), params=data)
        pub_results = json.loads(self._fetch_content('%s/projects/%s/assets' % (self.session.host_url, project),
                                                     params=data))
        if pub_results['results'] > 0:
            return pub_results
        else:
            return None

    def _ss_DoesProjectContainWork(self, project):
        key = "%s-field-defs-%d" % (self.session.memcache_master_key, int(project))
        raw = self._memcache_get(key, timeout=300)
        if not raw:
            raw = json.loads(self._fetch_content('%s/admin/projects/%s/definitions' % (self.session.host_url, project)))
            self._memcache_set(key, raw, timeout=300)

        for field in raw['definitions']:
            try:
                # print "field: ", field
                if field['field_type_id'] == 140:
                    self.session.work_field = "fd_" + unicode(field['id']) + "_lookup"
                    return True
            except:
                print "problem looking up fields"
        return False

    def _ss_GetFieldDefs(self, project, work=False):
        key = "%s-field-defs-%d" % (self.session.memcache_master_key, int(project))
        raw = self._memcache_get(key, timeout=300)
        if not raw:
            raw = json.loads(self._fetch_content('%s/admin/projects/%s/definitions' % (self.session.host_url, project)))
            self._memcache_set(key, raw, timeout=300)

        poststr = {
            100: 's',
            101: 'i',
            102: 'dt',
            103: 's',
            104: 'multi_s',
            105: 'b',
            130: 'lookup',
            140: 'lookup'
        }

        typestr = {
            100: 'string',
            101: 'integer',
            102: 'date',
            103: 'string',
            104: 'string',
            105: 'boolean',
            130: 'lookup',
            140: 'lookup'
        }

        converted = dict()
        skip = [
            '_comparable',
            '_remote_ana_link_ana_ids',
            'id',
            'created_by',
            'created_on',
            'updated_by',
            'updated_on',
            'project_id',
            'representation_id',
            'deleted',
            'filename'
        ]

        for field in raw['definitions']:
            try:
                field_name = "fd_" + unicode(field['id']) + "_" + poststr[field['field_type_id']]
                if field['field_type_id'] == 140:
                    self.session.work_field = field_name
                converted[field_name] = dict()
                converted[field_name]['label'] = field['label']
                converted[field_name]['description'] = field['description']
                converted[field_name]['type'] = typestr[field['field_type_id']]
                if self._ssAddSkipForWork(field):
                    skip.append(field_name)
                if poststr[field['field_type_id']] == "lookup":
                    skip.append(str("fd_" + unicode(field['id']) + "_multi_s"))

            except KeyError:
                print "miss on: ", field['field_type_id']

        return converted, skip

    def _ssAddSkipForWork(self, field):
        notSkipped = [
            'Image Repository',
            'Caption note',
            'Sequence Number',
            "Send To Harvard"
        ]

        if field['label'] in notSkipped:
            return False
        else:
            return True

    def _ss_BuildSimpleRecord(self, identifier, proj, outputMetadata=True, status='Active', ts=None):
        session = self.session

        if status == 'Active':
            resp = self._fetch_content('%s/publishing-targets/%s/assets/%s' % (self.session.host_url, proj, identifier))
            try:
                admin = json.loads(resp)['admin']
                data = json.loads(resp)['data']
                newdata = dict()
                for d in data:
                    for k in d.keys():
                        for item in d[k]:
                            if type(item['value']) is dict:
                                if 'display_value' in item['value']:
                                    value = item['value']['display_value']
                                else:
                                    value = item['value']['links'][0]['source_id']
                            else:
                                value = item['value']

                            if not k in newdata:
                                newdata[k] = []

                            if type(value) is list:
                                newdata[k] = newdata[k] + value
                            else:
                                newdata[k].append(unicode(value))

                # need to insert the image and thumbnail url's as identifiers
                url = self._ss_ThumbnailImage(identifier)
                if url:
                    # output_string = 'Thumbnail:' + unicode(url)
                    if not 'identifier' in newdata:
                        newdata['identifier'] = []
                    newdata['identifier'].append('Thumbnail:' + unicode(url))

                url = self._ss_FullSizeImage(identifier)
                if url:
                    # output_string = 'FullSize:' + unicode(url)
                    if not 'identifier' in newdata:
                        newdata['identifier'] = []
                    newdata['identifier'].append('FullSize:' + unicode(url))

                if outputMetadata:
                    return common.Header(str(identifier),
                                         datestamp_to_datetime(self._FixDate(admin['updated_on'])),
                                         '',
                                         False), common.Metadata(newdata), ''
                else:
                    return common.Header(str(identifier),
                                         datestamp_to_datetime(self._FixDate(admin['updated_on'])),
                                         '',
                                         False)
            except:
                return None
        else:
            if outputMetadata:
                return common.Header(str(identifier),
                                     parser.parse(ts).replace(tzinfo=None),
                                     '',
                                     True), None, ''
            else:
                return common.Header(
                    str(identifier),
                    parser.parse(ts).replace(tzinfo=None),
                    '',
                    True)

    def _ss_BuildSimpleSSIORecord(self, identifier, source_project, pub_status, proj, outputMetadata=True, status='Active', ts=None):
        session = self.session

        # capture all names used for extracting name records
        namespaces = dict()

        if status == 'Active':
            defs, skip = self._ss_GetFieldDefs(source_project, work=False)
            resp = self._fetch_content('%s/publishing-targets/%s/assets/%s' % (self.session.host_url, proj, identifier))
            data = dict(filter='[{"type":"numeric","comparison":"eq","value":%s,"field":"id"}]' % identifier, with_meta="false")
            data2 = json.loads(self._fetch_content('%s/projects/%s/assets' % (self.session.host_url, source_project), params=data))['assets']

            try:
                data = json.loads(resp)['data']
                admin = json.loads(resp)['admin']
                sharedshelf = dict()
                display = dict()
                displayrecord = dict()
                myname = dict()
                attributes = dict()
                newdata = dict()

                for d in data2:
                    for k in d.keys():
                        item = d[k]
                        value = None
                        if k not in skip:
                            tag = dict()
                            if k in defs:
                                tag['label'] = defs[k]['label']
                                tag['description'] = defs[k]['description']
                                tag['type'] = defs[k]['type']
                            if type(item) is dict:
                                if 'display_value' in item.keys():
                                    tag['value'] = None
                                    tag['display_value'] = item['display_value']
                                    tag['linkedField'] = self._LinkedField(tag['value'], item['links'])
                                    for link in item['links']:
                                        if not link['source'] in namespaces:
                                            namespaces[link['source']] = []
                                        namespaces[link['source']].append(link['source_id'])
                                else:
                                    value = None
                                    tag['value'] = item
                            else:
                                if k == 'publication_statuses' or k == 'asset_group_id':
                                    value = None
                                else:
                                    tag['value'] = item
                                    value = item

                            if value is not None or 'display_value' in tag:
                                if not hasattr(newdata, k):
                                    newdata[k] = []
                                newdata[k] = tag

                if outputMetadata:
                    # build the attributes for the displayrecord
                    attributes['id'] = identifier
                    attributes['representationId'] = admin['representation_id']
                    attributes['lastUpdateDate'] = admin['updated_on']
                    attributes['projectId'] = admin['project_id']
                    attributes['institutionId'] = self.session.institution
                    attributes['updatedBy'] = data2[0]['updated_by']
                    attributes['createdBy'] = data2[0]['created_by']
                    attributes['createdDate'] = data2[0]['created_on']

                    # build the displayrecord record
                    displayrecord['DisplayRecord'] = newdata
                    displayrecord['attributes'] = attributes

                    # build the targets record
                    displayrecord['targets'] = self._AssetTargets(pub_status)

                    # bulid the assets record
                    assets = dict()
                    assets['assets'] = self._AssetAssets(identifier)
                    if assets['assets']:
                        assets['filename'] = admin['filename']
                        displayrecord['assets'] = assets

                    # build the Publications record
                    if 'publication_statuses' in d:
                        displayrecord['Publications'] = d['publication_statuses']

                    # build the Asset Group record
                    if 'asset_group_id' in d:
                        displayrecord['AssetGroups'] = d['asset_group_id']

                    # build the display record
                    display[identifier] = displayrecord

                    for names in namespaces.keys():
                        for myid in namespaces[names]:
                            namerecord = self._ss_lookup_name(names, myid)
                            if namerecord is not None:
                                namerecord['NameSpace'] = names
                                myname[myid] = namerecord

                    # add to sharedshelf record
                    sharedshelf['display'] = display
                    sharedshelf['name'] = myname

                    return common.Header(str(identifier), datestamp_to_datetime(self._FixDate(admin['updated_on'])), '', False), common.Metadata(sharedshelf), ''
                else:
                    return common.Header(str(identifier), datestamp_to_datetime(self._FixDate(admin['updated_on'])), '', False)
            except:
                print "asset not in project: ", proj
                return None
        else:
            if outputMetadata:
                return common.Header(str(identifier),
                                     parser.parse(ts).replace(tzinfo=None),
                                     '',
                                     True), None, ''
            else:
                return common.Header(str(identifier),
                                     parser.parse(ts).replace(tzinfo=None),
                                     '',
                                     True)

    def _ss_BuildComplexSSIORecord(self, identifier, work_id, source_project, target, myfrom=None, myuntil=None, outputMetadata=True):
        session = self.session

        # print "in complex"
        # capture all names used for extracting name records
        namespaces = dict()

        defs, skip = self._ss_GetFieldDefs(source_project, work=True)

        # need to get comp key from one of the identifiers
        # print "identifier: ", identifier
        if len(identifier) > 0:
            composite_key = None
            counter = 0
            while composite_key is None and counter < len(identifier):
                thisid = identifier[counter]
                status, asset, ts = self._ss_GetAsset(thisid, source_project, target)
                if asset is not None:
                    composite_key = asset['assets'][0][self.session.work_field]['links'][0]['source_id']
                else:
                    counter += 1
            if composite_key is None:
                return None
        else:
            return None

        try:
            work_record = json.loads(self._fetch_content('%s/getWorkByWorkIndexId/?authToken=123&workIndexId=%s' % (self.session.wrk_url, work_id)))
            # work_record = json.loads(self._fetch_content('%s/getWorkXmlByCompositeKey?compositeKey=%s&authToken=123' % (self.session.wrk_url, composite_key)))
            if 'code' in work_record:
                return None

        except:
            log.error("Could not fetch work record when one should exist: %s" % work_id)
            return None
            # abort(503)

        # check if last updated between from and until
        last_update = work_record['work']['lastUpdateDate']
        work_time = pytz.utc.localize(datetime.strptime(last_update, '%m/%d/%Y - %H:%M')).astimezone(pytz.utc).strftime("%Y-%m-%dT%H:%M:%s+00:00")
        if work_time < myfrom or work_time > myuntil:
            return None

        if 'code' not in work_record:
            work = self._BuildWorkRecord(work_record)
        else:
            work = dict()
            work['work'] = dict()
            work['work']['display'] = []

        sharedshelf = dict()
        myname = dict()
        display = dict()

        work_id = work_record['work']['id']

        for dispid in identifier:
            status, asset, ts = self._ss_GetAsset(dispid, source_project, target)
            if asset and 'publication_statuses' in asset['assets'][0]:
                pub_status = asset['assets'][0]['publication_statuses']
            else:
                pub_status = None

            if status == 'Active':
                # defs, skip = self._ss_GetFieldDefs(source_project, work=True)
                resp = self._fetch_content('%s/publishing-targets/%s/assets/%s' % (self.session.host_url, target, dispid))
                data = dict(filter='[{"type":"numeric","comparison":"eq","value":%s,"field":"id"}]' % dispid, with_meta="false")
                data2 = json.loads(self._fetch_content('%s/projects/%s/assets' % (self.session.host_url, source_project), params=data))['assets']

                # try:
                data = json.loads(resp)['data']
                admin = json.loads(resp)['admin']
                displayrecord = dict()
                attributes = dict()
                newdata = dict()

                for d in data2:
                    for k in d.keys():
                        item = d[k]
                        # if k not in skip:
                        tag = dict()
                        if k in defs:
                            tag['description'] = defs[k]['description']
                            tag['label'] = defs[k]['label']
                            tag['type'] = defs[k]['type']
                            value = None
                        else:
                            value = None
                        if type(item) is dict:
                            if 'display_value' in item.keys():
                                tag['value'] = None
                                tag['display_value'] = item['display_value']
                                tag['linkedField'] = self._LinkedField(tag['value'], item['links'])
                                for link in item['links']:
                                    if not link['source'] in namespaces:
                                        namespaces[link['source']] = []
                                    if link['source_id'] not in namespaces[link['source']]:
                                        namespaces[link['source']].append(link['source_id'])
                            else:
                                value = None
                                tag['value'] = item
                        else:
                            if k == 'publication_statuses' or k == 'asset_group_id':
                                value = None
                            else:
                                tag['value'] = item
                                value = item

                        if k not in skip:
                            if value is not None:
                                if not hasattr(newdata, k):
                                    newdata[k] = []
                                newdata[k] = tag

                if outputMetadata:
                    # build the attributes for the displayrecord
                    attributes['id'] = dispid
                    attributes['representationId'] = admin['representation_id']
                    attributes['lastUpdateDate'] = admin['updated_on']
                    attributes['projectId'] = admin['project_id']
                    attributes['institutionId'] = self.session.institution
                    attributes['updatedBy'] = data2[0]['updated_by']
                    attributes['createdBy'] = data2[0]['created_by']
                    attributes['createdDate'] = data2[0]['created_on']

                    # build the displayrecord record
                    displayrecord['DisplayRecord'] = newdata
                    displayrecord['attributes'] = attributes

                    # build the targets record
                    displayrecord['targets'] = self._AssetTargets(pub_status)

                    # bulid the assets record
                    assets = dict()
                    assets['assets'] = self._AssetAssets(dispid)
                    if assets['assets']:
                        assets['filename'] = admin['filename']
                        displayrecord['assets'] = assets

                    # build the Publications record
                    if 'publication_statuses' in d:
                        displayrecord['Publications'] = d['publication_statuses']

                    # build the Asset Group record
                    if 'asset_group_id' in d:
                        displayrecord['AssetGroups'] = d['asset_group_id']

                    # build the display record
                    display[dispid] = displayrecord

                    for names in namespaces.keys():
                        for myid in namespaces[names]:
                            namerecord = self._ss_lookup_name(names, myid)
                            if namerecord is not None:
                                namerecord['NameSpace'] = names
                                myname[myid] = namerecord

            else:
                # make a deleted record here
                displayrecord = dict()
                attributes = dict()
                attributes['id'] = dispid
                attributes['status_lkup'] = 'Deleted'
                attributes['projectId'] = source_project
                attributes['institutionId'] = self.session.institution
                displayrecord['DisplayRecord'] = dict()
                displayrecord['attributes'] = attributes
                display[dispid] = displayrecord

        # build the full record
        work['work']['display'].append(display)
        sharedshelf['name'] = myname
        sharedshelf['work'] = work

        if outputMetadata:
            return common.Header(str(work_id), datestamp_to_datetime(self._FixDate(admin['updated_on'])), '', False), common.Metadata(sharedshelf), ''
        else:
            return common.Header(str(work_id), datestamp_to_datetime(self._FixDate(admin['updated_on'])), '', False)


    def _BuildWorkRecord(self, work_record):
        workrecord = dict()
        work_attr = dict()
        workrecord['work'] = dict()
        # build the attributes for the work record
        for x in work_record['work'].keys():
            if type(work_record['work'][x]) is unicode:
                work_attr[x] = work_record['work'][x]
            elif type(work_record['work'][x]) is dict:
                workrecord['work'][x] = work_record['work'][x]
            elif type(work_record['work'][x]) is list:
                pass
        # handle display at the end
        workrecord['work'][u'display'] = work_record['work']['display']
        work_attr['ssw_id'] = work_record['workIndexId']
        del work_attr['id']
        workrecord['attributes'] = work_attr
        return workrecord

    def _LinkedField(self, display, values):
        # linkedfield = dict()
        links = []
        # linkedfield['display'] = display

        for link in values:
            if '-' in link['id']:
                myid = link['id'].split('-', 2)[1]
            else:
                myid = link['id']
            for k in link.keys():
                allterms = ""
                if k == "allTerms":
                    for v in link[k]:
                        if not allterms:
                            allterms = v
                        else:
                            allterms = allterms + " | " + v
                    link['allTerms'] = allterms
                if k == "data":
                    for v in link[k]:
                        link[v] = link[k][v]
                    link.pop('data', None)
            link['id'] = myid
            links.append(link)
        # linkedfield['linkedField'] = links
        return links

    def _AssetTargets(self, pub_status):
        targets = []
        for pub in pub_status:
            target = dict()
            if pub['status'] == 'Published':
                myid = pub['publishing_target_id']
                # target['id'] = myid
                target['publishDate'] = pub['updated_on']
                target['name'] = self.session.PubTargets[myid]['name']
                target['description'] = self.session.TargetDefs[self.session.PubTargets[myid]['target_id']]['name']
                target['lkup_status'] = pub['status']
                if 'target_url' in self.session.TargetDefs[self.session.PubTargets[myid]['target_id']]:
                    target['url'] = self.session.TargetDefs[self.session.PubTargets[myid]['target_id']]['target_url']
                targets.append(target)
        return targets

    def _AssetAssets(self, myid):
        assets = []

        # Thumbnail Asset
        asset = dict()
        url = self._ss_ThumbnailImage(myid)
        if url:
            asset['id'] = myid
            asset['uri'] = url
            asset['size'] = 'Thumbnail'
            assets.append(asset)

        # FullSize Asset
        asset = dict()
        url = self._ss_FullSizeImage(myid)
        if url:
            asset['id'] = myid
            asset['uri'] = url
            asset['size'] = 'FullSize'
            assets.append(asset)
        return assets

    def _ss_FullSizeImage(self, myid):
        uri = '%s/assets/%s/representation/size/9' % (self.session.host_url, myid)
        return uri

    def _ss_ThumbnailImage(self, myid, size=1):
        uri = '%s/assets/%s/representation/size/%s' % (self.session.host_url, myid, size)
        return uri

    def _ss_lookup_name(self, names, myid):
        if 'TGN' in names:
            return self._ss_constructTGN(myid)
        elif 'AAT' in names:
            return self._ss_constructAAT(myid)
        elif 'SSN' in names:
            return self._ss_constructSSN(myid)
        elif 'SSW' in names:
            return None
        else:
            log.info("_ss_lookup_name: id - %s:  Unknown namespace: %s" % (myid, names))
            return None

    def _ss_constructTGN(self, myid):
        return json.loads(self._fetch_content('%s/subjectDetail?subjectid=%s' % (self.session.tgn_url, myid)))

    def _ss_constructAAT(self, myid):
        return json.loads(self._fetch_content('%s/subjectDetail?subjectid=%s' % (self.session.aat_url, myid)))

    def _ss_constructSSN(self, myid):
        result = json.loads(self._fetch_content('%s/name/json/conceptDetail?authToken=%s&conceptId=%s' % (self.session.ssn_url, self.session.ssn_token, myid)))
        if 'code' in result:
            return None
        else:
            return result

    def _fetch_content(self, url, params=None, debug=False):
        debug = False
        if debug:
            print "-----------------------------------"
            print "fetching: ", url
            print "  params: ", params
            print "    start: ", datetime.now()
        try:
            if params:
                resp = self.session.get(url, params=params)
            else:
                resp = self.session.get(url)
        except:
            log.error('Error Accessing %s' % url)
            abort(503)

        if resp.status_code == 200:
            if debug:
                print "    end:   ", datetime.now()
            return resp.text
        elif resp.status_code == 403:
            log.error('Error Accessing %s' % url)
            abort(403)
        elif resp.status_code == 503:
            log.error('Service Unavailable: %s' % url)
            abort(503)
        else:
            log.error('other code: %s\t from url: %s' % (resp.text,url))


class BatchingSharedShelfServerBase(SharedShelfServerCommon):

    def listIdentifiers(self, metadataPrefix=None, from_=None, until=None, set=None, cursor=0, batch_size=10):
        session = self._ss_init()

         # is no set, use list of sets that belong to institution, otherwise must use set specified
        if set is None:
            projlist = session.SetList[unicode(session.institution)]
        else:
            projlist = self._CheckIfValidSet(unicode(session.institution), set)

        for p, d, x in projlist:
            target = session.Set2OAIDC[int(p)][0]                           # should only be a single target for OAI DC
            # need to make sure asset is actually published to OAI
            if metadataPrefix == 'oai_dc':
                return self._ss_output_nowork(metadataPrefix, from_, until, set, cursor, batch_size, details=False)
            elif metadataPrefix == 'oai_ssio':
                if self._ss_DoesProjectContainWork(p):
                    return self._ss_output_withwork(metadataPrefix, from_, until, p, cursor, batch_size, details=False)
                else:
                    return self._ss_output_nowork(metadataPrefix, from_, until, set, cursor, batch_size, details=False)
            else:
                raise error.CannotDisseminateFormatError, "Unknown metadata format: %s" % metadataPrefix

    def listRecords(self, metadataPrefix=None, from_=None, until=None, set=None, cursor=0, batch_size=10):
        session = self._ss_init()

         # is no set, use list of sets that belong to institution, otherwise must use set specified
        if set is None:
            projlist = session.SetList[unicode(session.institution)]
        else:
            projlist = self._CheckIfValidSet(unicode(session.institution), set)

        for p, d, x in projlist:
            target = session.Set2OAIDC[int(p)][0]                           # should only be a single target for OAI DC
            # need to make sure asset is actually published to OAI
            if metadataPrefix == 'oai_dc':
                return self._ss_output_nowork(metadataPrefix, from_, until, set, cursor, batch_size, details=True)
            elif metadataPrefix == 'oai_ssio':
                if self._ss_DoesProjectContainWork(p):
                    return self._ss_output_withwork(metadataPrefix, from_, until, p, cursor, batch_size, details=True)
                else:
                    return self._ss_output_nowork(metadataPrefix, from_, until, set, cursor, batch_size, details=True)
            else:
                raise error.CannotDisseminateFormatError, "Unknown metadata format: %s" % metadataPrefix
        # return self._ss_output_nowork(metadataPrefix, from_, until, set, cursor, batch_size, details=True)

    def _CountAssets(self, assets, myfrom, myuntil):
        count = 0
        for a in assets:
            if self._FilterAsset(assets[a], myfrom, myuntil):
                count += 1
        return count

    def _FilterAsset(self, asset, myfrom, myuntil):
        if asset['updated'] > myfrom and asset['updated'] < myuntil and asset['status'] != 'Unpublished':
            return True
        else:
            return False

    def _NarrowAssetList(self, assets, myfrom, myuntil, cursor, batch_size):
        assets = self._FixIds(assets)
        filtered_list = []
        counter = 0
        current = 1
        for k in sorted(assets):
            good = self._FilterAsset(assets[k], myfrom, myuntil)
            if good and counter < cursor:
                counter += 1
            elif current > batch_size:
                break
            elif good and current <= batch_size:
                item = dict()
                item[k] = assets[k]
                filtered_list.append(item)
                current += 1
        return filtered_list

    def _FixIds(self, assets):
        new_assets = dict()
        for k in assets:
            new_assets[int(k)] = assets[k]
        return new_assets

    def _ss_output_nowork(self, metadataPrefix=None, from_=None, until=None, set=None, cursor=0, batch_size=10, details=True):
        result = []
        current_list = 0
        remainder = batch_size
        session = self._ss_init()
        prior_assets = 0
        new_cursor = cursor

        myfrom, myuntil = self._MungeDates(from_, until)

        # is no set, use list of sets that belong to institution, otherwise must use set specified
        if set is None:
            projlist = session.SetList[unicode(session.institution)]
        else:
            projlist = self._CheckIfValidSet(unicode(session.institution), set)

        for p, d, x in projlist:
            if current_list < batch_size:
                target = self._GetPubTarget(session, p, metadataPrefix)[0]

                if target is not None:
                    try:
                        self._ss_GetAssetStatus(p, target)
                    except:
                        abort(503)

                    project_size = self._CountAssets(self.session.project_assets[p]['assets'], myfrom, myuntil)
                    if cursor < project_size:
                        asset_list = self._NarrowAssetList(self.session.project_assets[p]['assets'], myfrom, myuntil, new_cursor, remainder)
                        if len(asset_list) < batch_size:
                            remainder = batch_size - len(asset_list)
                        else:
                            remainder = 0

                        for a in asset_list:
                            myid = a.keys()[0]
                            status, asset, ts = self._ss_GetAsset(myid, p, target)

                            if metadataPrefix == "oai_dc":
                                myrecord = self._ss_BuildSimpleRecord(myid, target, outputMetadata=details, status=status, ts=ts)
                            elif metadataPrefix == "oai_ssio":
                                if status != 'Active':
                                    pub_stat = None
                                else:
                                    pub_stat = asset['assets'][0]['publication_statuses']
                                myrecord = self._ss_BuildSimpleSSIORecord(myid, p, pub_stat, target, outputMetadata=details, status=status, ts=ts)
                            else:
                                raise error.CannotDisseminateFormatError, "Unknown metadata format: %s" % metadataPrefix
                            result.append(myrecord)
                            current_list = current_list + 1

                        if remainder > 0:
                            new_cursor = 0
                    else:
                        new_cursor = (batch_size - 1) - (prior_assets % (batch_size - 1))
                    prior_assets += project_size


        return result

    def _ss_output_withwork(self, metadataPrefix=None, from_=None, until=None, p=None, cursor=0, batch_size=10, details=True):
        # get batch of work records based on from/until, cursor, etc
        session = self._ss_init()
        # projlist = session.SetList[unicode(self.session.institution)]
        # batch_size from oai is always 1 larger than I need
        fetch_size = batch_size
        result = []
        found_records = []

        myfrom, myuntil = self._MungeDates(from_, until)

        # for p, d, x in set:
        start = cursor
        target = session.Set2OAIDC[int(p)][0]                           # should only be a single target for OAI DC
        # need to make sure asset is actually published to OAI
        if self._ss_DoesProjectContainWork(p):
            # new_work, start, end_work = self.build_work_list(fetch_size, start, self.session.institution)
            # counter = 0
            found = 0
            while found < fetch_size:
                new_work, start, end_work = self.build_work_list(fetch_size - found, start, self.session.institution, p)
                sequence = 0
                while sequence < len(new_work.keys()):
                    for work_info in new_work:
                        if new_work[work_info]['sequence'] == sequence:
                            pub_status = status = ts = ''
                            if work_info not in found_records:
                                myrecord = self._ss_BuildComplexSSIORecord(new_work[work_info]['display_records'], work_info, p, target, myfrom=myfrom, myuntil=myuntil, outputMetadata=details)
                                if myrecord is not None:
                                    found += 1
                                    result.append(myrecord)
                                    found_records.append(work_info)
                    sequence += 1
                if end_work:
                    break
        else:
            print "no work here"
        # print "returning upward: ", result
        return result


    def build_work_list(self, batch_size, start, inst, proj):
        work_found = 0
        work_batch = 100
        end_reached = 0
        dr_found = 0
        new_work = dict()

        orphans = self.get_orphans(inst)
        allwork = self.get_allwork(inst)

        while work_found <= batch_size and not end_reached:
            count = 0
            mydata=self. get_work_info(start, proj)
            start += work_batch
            if len(mydata['hits']['hits']) < work_batch:
                end_reached = 1
            for record in mydata['hits']['hits']:
                count += 1
                myid = record['_id']
                try:
                    # work = record['fields']['fd_41_lookup']['links'][0]['source_id']
                    work = record['fields'][self.session.work_field]['links'][0]['source_id']
                    if work not in new_work:
                        if work not in allwork:
                            #allwork[work] = []
                            allwork.append(work)
                            new_work[work] = dict()
                            new_work[work]['display_records'] = []
                            new_work[work]['sequence'] = work_found
                            work_found += 1
                            last_work = work

                    if work in new_work:
                        new_work[work]['display_records'].append(myid)
                        dr_found += 1
                        if work_found > batch_size:
                            start -= work_batch
                            end_reached = 0
                            #popped = allwork.pop(last_work, None)
                            allwork.remove(last_work)
                            # if last_work in allwork:
                            #     print "last work still here"
                            break
                except:
                    orphans.append(myid)
        self._memcache_set('oai-work-%s-orphans' % inst, orphans, timeout=300)
        self._memcache_set('oai-work-%s-allwork' % inst, allwork, timeout=300)
        return new_work, start, end_reached



    def get_work_info(self, start, proj):
        # print "batch start: ", start
        fullquery = dict()
        sort = dict()
        sort_field = self.session.work_field
        # print "sort field: ", sort_field
        sort[sort_field] = 'desc'
        # sort['_comparable.fd_41_lookup'] = 'desc'
        # sort['_comparable.%s' % self.session.work_field] = 'desc'
        fullquery['sort'] = sort
        fullquery['from'] = start
        fullquery['size'] = 100
        # fullquery['fields'] = [ "fd_41_lookup" ]
        fullquery['fields'] = [self.session.work_field]
        query = dict()
        query['match_all'] = dict()
        fullquery['query'] = query

        # pool = es_connector()
        resp = self.session.pool.urlopen("GET", "/project_%s/assets/_search " % proj, json.dumps(fullquery))
        # print "gwi return: ", resp.data

        return json.loads(resp.data)

    def get_orphans(self, inst):
        orphans = self._memcache_get('oai-work-%s-orphans' % inst)
        if orphans is None:
                self._memcache_set('oai-work-%s-orphans' % inst, [])
                orphans = self._memcache_get('oai-work-%s-orphans' % inst)
        return orphans

    def get_allwork(self, inst):
        allwork = self._memcache_get('oai-work-%s-allwork' % inst)
        if allwork is None:
                self._memcache_set('oai-work-%s-allwork' % inst, [])
                allwork = self._memcache_get('oai-work-%s-allwork' % inst)
        return allwork


class BatchingSharedShelfServer(BatchingSharedShelfServerBase):
    def __init__(self):
        pass


def nsoaissio(name):
    return '{%s}%s' % (NS_OAISSIO, name)
