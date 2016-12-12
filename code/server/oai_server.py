#from lxml import etree
from flask import Flask, request, Response, render_template, abort
from oaipmh import server, metadata
from oai_auth import auth_info, ip_check_init, ip_to_inst, set_auth, get_ip
import logging

import ss_server

def getServer():
    myserver = ss_server.BatchingSharedShelfServerBase()
    metadata_registry = metadata.MetadataRegistry()
    metadata_registry.registerWriter('oai_dc', server.oai_dc_writer)
    metadata_registry.registerWriter('oai_ssio', ss_server.oai_ssio_writer)
    return server.BatchingServer(myserver, metadata_registry, resumption_batch_size=10)


def buildLogging():
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    fh = logging.FileHandler('oai.log')
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    log.addHandler(fh)


app = Flask(__name__)

oai_server = getServer()
ip_list = ip_check_init()
buildLogging()


@app.route('/')
def cai_server():
    log = logging.getLogger()
    request_params = dict()
    ip = get_ip(request)
    inst = ip_to_inst(ip_list, ip)
    if inst is None:
        log.error("%s is not an authorized ip" % ip)
        abort(403)
    set_auth(inst, ip)
    for key in request.args.keys():
        request_params[key] = request.args[key]
    tree = oai_server.handleRequest(request_params)
    return Response(tree, mimetype='text/xml')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=9981)
