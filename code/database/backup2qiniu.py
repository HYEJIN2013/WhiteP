#!/usr/bin/env python

import os
import sys
import hmac
import json
import time
import hashlib
import datetime
import requests
import mimetypes
from requests.compat import urlencode, bytes
from base64 import urlsafe_b64encode
from subprocess import Popen, PIPE


def to_bytes(text):
    if isinstance(text, bytes):
        return text
    return text.encode('utf-8')


def to_unicode(text):
    if isinstance(text, bytes):
        return text.decode('utf-8')
    return text


def hmac_sha1_b64encode(data, secret):
    data = to_bytes(data)
    secret = to_bytes(secret)
    signature = hmac.new(secret, data, hashlib.sha1)
    encoded_signature = urlsafe_b64encode(signature.digest())
    return to_unicode(encoded_signature)


class Qiniu(object):
    def __init__(self, bucket, access_key, secret_key):
        self.bucket = bucket
        self.access_key = access_key
        self.secret_key = secret_key

    def upload(self, src, dest):
        """Upload to qiniu bucket"""
        deadline = int(time.time()) + 3600
        rv = json.dumps({
            'scope': '%s:%s' % (self.bucket, dest),
            'deadline': deadline,
        })
        encoded_data = urlsafe_b64encode(rv)
        signature = hmac_sha1_b64encode(encoded_data, self.secret_key)
        token = '%s:%s:%s' % (self.access_key, signature, encoded_data)

        url = 'http://up.qiniu.com/'
        default = 'application/octet-stream'
        content_type = mimetypes.guess_type(dest)[0] or default
        with open(src) as f:
            data = f.read()
        files = {'file': (dest, data, content_type)}
        payload = {
            'key': dest,
            'token': token,
        }
        resp = requests.post(url, files=files, data=payload)
        return resp.text

    def sign(self, signstr, body=''):
        signing = '%s\n%s' % (signstr, body)
        signature = hmac_sha1_b64encode(signing, self.secret_key)
        return '%s:%s' % (self.access_key, signature)

    def list(self, prefix=None, delimiter=None, marker=None, limit=None):
        query = {'bucket': self.bucket}
        if prefix:
            query['prefix'] = prefix
        if delimiter:
            query['delimiter'] = delimiter
        if marker:
            query['marker'] = marker
        if limit:
            query['limit'] = limit
        signstr = '/list?' + urlencode(query)
        url = 'http://rsf.qbox.me' + signstr
        headers = {
            'Authorization': 'QBox %s' % self.sign(signstr)
        }
        resp = requests.post(url, headers=headers)
        data = resp.json()
        return data['items']

    def batch(self, ops):
        body = '&'.join(map(lambda o: 'op=%s' % o, ops))
        token = self.sign('/batch', body)
        headers = {
            'Authorization': 'QBox %s' % token
        }
        url = 'http://rs.qiniu.com/batch'
        resp = requests.post(url, headers=headers, data=body)
        return resp.json()

    def encode_entry_url(self, name):
        key = urlsafe_b64encode(to_bytes('%s:%s' % (self.bucket, name)))
        return to_unicode(key)

    def move(self, src, dest):
        op = '/move/{0}/{1}'.format(
            self.encode_entry_url(src),
            self.encode_entry_url(dest)
        )
        headers = {
            'Authorization': 'QBox %s' % self.sign(op)
        }
        url = 'http://rs.qiniu.com' + op
        resp = requests.post(url, headers=headers)
        return resp.status_code == 200

    def delete(self, filename):
        if isinstance(filename, (list, tuple)):
            ops = []
            for name in filename:
                ops.append('/delete/%s' % self.encode_entry_url(name))
            return self.batch(ops)
        op = '/delete/%s' % self.encode_entry_url(filename)
        headers = {
            'Authorization': 'QBox %s' % self.sign(op)
        }
        url = 'http://rs.qiniu.com' + op
        resp = requests.post(url, headers=headers)
        return resp.status_code == 200

    def clean(self, basename):
        today = datetime.date.today()

        to_delete = []
        week_file = None
        month_file = None

        # keep one week daily backup
        prefix = 'daily/{0}'.format(basename)
        dateformat = '{0}.%Y-%m-%d.tar.gz'.format(prefix)
        for item in self.list(prefix=prefix):
            key = item['key']
            puttime = datetime.datetime.strptime(key, dateformat)
            delta = today - puttime.date()
            if puttime.day == 1:
                month_file = key
            elif delta.days > 7:
                to_delete.append(key)
            elif delta.days == 7:
                week_file = key

        # clean weekly backup
        prefix = 'weekly/{0}'.format(basename)
        dateformat = '{0}.%Y-%m-%d.tar.gz'.format(prefix)
        for item in self.list(prefix=prefix):
            key = item['key']
            puttime = datetime.datetime.strptime(key, dateformat)
            delta = today - puttime.date()
            if delta.days > 30:
                to_delete.append(key)

        # weekly backup at Sunday
        if today.weekday() == 6 and week_file:
            dest = week_file.replace('daily/', 'weekly/')
            self.move(week_file, dest)

        # monthly backup at 1st
        if today.day == 1 and month_file:
            dest = month_file.replace('daily/', 'monthly/')
            self.move(month_file, dest)

        # clean useless backup
        self.delete(to_delete)

    def backup(self, tarfile, basename):
        today = datetime.date.today()
        self.upload(tarfile, 'daily/{0}.{1}.tar.gz'.format(basename, today))


def shell(command, output=None, mode='w', cwd=None):
    """Run a shell command."""
    if not output:
        output = os.devnull
    else:
        folder = os.path.dirname(output)
        if folder and not os.path.isdir(folder):
            os.makedirs(folder)

    if isinstance(command, (list, tuple)):
        cmd = command
    else:
        cmd = command.split()

    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=cwd)
    stdout, stderr = p.communicate()
    if stderr:
        sys.stderr.write(stderr)
    #: stdout is bytes, decode for python3
    if sys.version_info[0] == 3:
        stdout = stdout.decode()
    with open(output, mode) as f:
        f.write(stdout)


def backup(name, **kwargs):
    folder = os.path.expanduser('~/dump')
    datadir = os.path.join(folder, 'data')
    if not os.path.isdir(datadir):
        os.makedirs(datadir)

    now = datetime.datetime.now()
    print("Backup %s at %s" % (name, now))

    print("Executing commands...")
    for cmd in kwargs.get('commands', []):
        shell(cmd, cwd=datadir)

    print("Starting compression...")
    today = datetime.date.today()
    filename = '%s.%s.tar.gz' % (name, today)
    tarfile = os.path.join(folder, filename)
    shell(['tar', 'czf', tarfile, 'data'], cwd=folder)

    qiniu = Qiniu(kwargs['bucket'], kwargs['access_key'], kwargs['secret_key'])
    print("Clean backup in Qiniu...")
    qiniu.clean(name)

    print("Uploading to Qiniu...")
    qiniu.backup(tarfile, name)

    shell(['rm', tarfile])


def main(config):
    with open(config) as f:
        data = json.load(f)
    backup(**data)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: backup.py config.json')
    else:
        main(sys.argv[1])
