#!/usr/bin/env python3

import argparse
import errno

import logging
import os

from ec.graph.manageGraph import ManageBlazegraph as mg
from ec.summarize.summarize_materializedview import summaryDF2ttl, get_summary4repo
from ec.gleanerio.gleaner import endpointUpdateNamespace, getNabu, reviseNabuConfGraph, runNabu, getNabuFromFile
from urllib.parse import urlparse



def dumpToFile(repo,summaryttl ):
    filename = os.path.join("output", f"{repo}.ttl")
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    with open(filename, 'w') as f:
        f.write(summaryttl)
    return
def isValidURL(toValidate):
    o = urlparse(toValidate)
    if o.scheme and o.netloc:
        return True
    else:
        return False


def summarizeRepo():
    """ Summarize a repository using a temporary graph namespace

    Description:
        * read nabu config,

        * uploading to a graph namespace

        * building summarize triples

        * loading to a summarized namespace

    """
    parser = argparse.ArgumentParser()

    parser.add_argument("repo", help='repository name')
    parser.add_argument('nabufile', type=argparse.FileType('r'),
                        help='nabu configuration file')
    parser.add_argument('--graphendpoint', dest='graphendpoint',
                        help='use this endpoint (full url:https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/earthcube/sparql"). overrides nabu endpoint')
    parser.add_argument('--glcon', dest='glcon',
                        help='override path to glcon', default="~/indexing/glcon")
    parser.add_argument('--nographsummary', action='store_true', dest='nographsummary',
                        help='send triples to file', default=False)
    parser.add_argument('--keeptemp', dest='graphtemp',
                        help='do not delete the temp namespace. a namespace "{repo}_temp" will be created', default=True)
    parser.add_argument('--summary_namespace', dest='summary_namespace',
                        help='summary_namespace. just the namepsace defaults to "{repo}_temp_summary"')
    args = parser.parse_args()

    repo = args.repo
    if args.summary_namespace:
        if isValidURL(args.summary_namespace):
            msg = 'For summary_namespace, Please enter the namespace only.'
            print(msg)
            logging.error(msg)
            return 1
        summary = args.summary_namespace
    else:
        summary = f"{repo}__temp_summary"
    nabucfg = args.nabufile
    endpoint, cfg = getNabuFromFile(nabucfg)
    graphendpoint = mg.graphFromEndpoint(endpoint)
    tempnsgraph = mg(graphendpoint, f'{repo}_temp')
    try:  # temp has been created
        created = tempnsgraph.createNamespace()
        if ( created=='Failed'):
            logging.fatal("coould not create namespace")
        sumnsgraph = mg(graphendpoint, summary)
        created = sumnsgraph.createNamespace()
        if ( created=='Failed'):
            logging.fatal("coould not create summary namespace")
        # endpoints for file
        tempendpoint =endpointUpdateNamespace(endpoint,f"{repo}_temp")
        summaryendpoint =endpointUpdateNamespace(endpoint,summary)
        newNabucfg = reviseNabuConfGraph(cfg, tempendpoint)
        runNabu(newNabucfg,repo, args.glcon )

        summarydf = get_summary4repo(tempendpoint)
        nt,g = summaryDF2ttl(summarydf,repo) # let's try the new generator
        summaryttl = g.serialize(format='longturtle')
        # write to s3  in future
        dumpToFile(repo, summaryttl)
        if not args.nographsummary:
            inserted = sumnsgraph.insert(bytes(summaryttl, 'utf-8'),content_type="application/x-turtle" )
            if inserted:
                logging.info(f"Inserted into graph store{sumnsgraph.namespace}" )
            else:
                logging.error(f" dumping file {repo}_dumped.ttl  Repo {repo} not inserted into {sumnsgraph.namespace}")
                dumpToFile(f"{repo}_dumped", summaryttl)
                return 1
    except Exception as ex:
        logging.error(f"error {ex}")
        print(f"Error: {ex}")
        return 1
    finally:
        # need to figure out is this is run after return, I think it is.
        if not args.graphtemp :
            logging.debug(f"Deleting Temp namespace {tempnsgraph.namespace}")
            deleted = tempnsgraph.deleteNamespace()
        return 0

if __name__ == '__main__':
    logging.info("Not Ready")
    exitcode= summarizeRepo()
    exit(exitcode)
