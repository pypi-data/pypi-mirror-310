import csv
import functools
import os
import click
import logging
import json
import sys

from pydash import is_empty
from pydash.collections import find
import pandas as pd
from ec.gleanerio.gleaner import getSitemapSourcesFromGleaner, getGleaner
from ec.objects.utils import parts_from_urn
from ec.datastore import s3
from ec.logger import config_app
import datetime
import pytz

log = config_app()

class EcConfig(object):
    """ Parameters that might be common to commands"""
    def __init__(self, cfgfile=None, s3server=None, s3bucket=None, upload=None, output=None,debug=False):
        if cfgfile:
            s3endpoint, bucket, glnr = getGleaner(cfgfile)
            minio = glnr.get("minio")
            # passed paramters override the config parameters
            self.s3server = s3server if s3server else s3endpoint
            self.bucket = s3bucket if s3bucket else bucket
            self.glnr = glnr
        else:
            self.s3server = s3server
            self.bucket = s3bucket
        self.output= output
        self.upload = upload
        self.debug = debug

    # lets put checks as methods in here.
    # that way some checks if we can connect can be done in one place
    def hasS3(self) -> bool:
         if   ( is_empty(self.s3server) or is_empty(self.bucket) ):
             log.fatal(f" must provide a gleaner config or (s3endpoint and s3bucket)]")
             raise Exception("must provide a gleaner config or (s3endpoint and s3bucket)]")
         return True
    def hasS3Upload(self) -> bool:
         if  not self.upload and ( is_empty(self.s3server) or is_empty(self.bucket) ):
             log.fatal(f" must provide a gleaner config or (s3endpoint and s3bucket)]")
             raise Exception("must provide a gleaner config or (s3endpoint and s3bucket)]")
         return True

def common_params(func):
    @click.option('--cfgfile', help='gleaner config file', type=click.Path(exists=True))
    @click.option('--s3server', help='s3 server address')
    @click.option('--s3bucket', help='s3 bucket')
    @click.option('--upload', help='upload to s3 bucket', default=True)
    @click.option('--output', help='dump to file', type=click.File('wb'))
    @click.option('--debug', default=False, envvar='REPO_DEBUG')
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@click.group()
@common_params
def cli(cfgfile, s3server, s3bucket, upload, output, debug):
    obj = EcConfig(cfgfile, s3server, s3bucket, upload, output, debug)

@cli.command()
@click.option('--path', help='Path to source',)
@click.option('--source', help='One or more repositories (--source a --source b)', multiple=True)
@common_params
def count(cfgfile, s3server, s3bucket, upload, output, debug, source, path):
    ctx = EcConfig(cfgfile, s3server, s3bucket, upload, output, debug)
    s3Minio = s3.MinioDatastore(ctx.s3server, None)
    ctx.hasS3()

    if path:
        count = s3Minio.countPath(ctx.bucket, path)
        res = f"Count for path {path}: {count}"
        sys.stdout.write(json.dumps(res, sort_keys=True, indent=4))
    elif source:
        counts = list()
        for s in source:
            path = f"/{s3Minio.paths.get('summon')}/{s}"
            count = s3Minio.countPath(ctx.bucket, path)
            res = f"Count for source {s}: {count}"
            counts.append(res)
        sys.stdout.write(json.dumps(counts, sort_keys=True, indent=4))
    elif cfgfile:
        sources = getSitemapSourcesFromGleaner(cfgfile)
        counts = list()
        for s in sources:
            path = f"/{s3Minio.paths.get('summon')}/{s.get('name')}"
            count = s3Minio.countPath(ctx.bucket, path)
            res = f"Count for source {s.get('name')}: {count}"
            counts.append(res)
        sys.stdout.write(json.dumps(counts, sort_keys=True, indent=4))
    else:
        message = "Please provide path to source. E.g. --path milled/iris or a config and optional sources"
        log.fatal(message)
        raise Exception(message)
    return

@cli.command()
@click.option('--source', help='A repository', required=True)
@common_params
def urls(cfgfile, s3server, s3bucket, upload, output, debug, source):
    """Retreive the URL harvested for a give bucket. T
    There may be duplicate URL's, if an HTML has more than one JSONLD"""
    ctx = EcConfig(cfgfile, s3server, s3bucket, upload, output, debug)
    s3Minio = s3.MinioDatastore(ctx.s3server, None)
    ctx.hasS3()

    res = s3Minio.listSummonedUrls(ctx.bucket, source)
    res = pd.DataFrame(res).to_csv(index=False, quoting=csv.QUOTE_NONNUMERIC)
    sys.stdout.write(res)
    if output:
        log.info(f"report for {source} appended to file")
        output.write(bytes(res, 'utf-8'))
    if upload:
        s3Minio.putReportFile(ctx.bucket, source, "bucketutil_urls.csv", res)
    return

@cli.command()
@click.option('--urn', help='One or more urns (--urn a --urn b)', multiple=True, required=True)
@common_params
def download(cfgfile, s3server, s3bucket, upload, output, debug, urn):
    """For a given URN(s), download the files and the Metadata"""
    ctx = EcConfig(cfgfile, s3server, s3bucket, upload, output, debug)
    s3Minio = s3.MinioDatastore(ctx.s3server, None)
    ctx.hasS3()

    for sha in urn:
        # need to parse the source and actual sha/id out of the urn
        # and then do the path and creat path
        parts = parts_from_urn(sha)
        mypath = parts.get('source')
        id = parts.get('id')
        if not os.path.isdir(mypath):
            os.makedirs(mypath)
        outFileName = f"{mypath}/{id}.jsonld"
        log.info(outFileName)
        outFile = open(outFileName, "wb")
        o = s3Minio.getJsonLD(ctx.bucket, mypath, id)
        outFile.write(o)
        outFile.close()
        outFileName = f"{mypath}/{id}.jsonld.meta.txt"
        log.info(outFileName)
        outFile = open(outFileName, "wb")
        o = s3Minio.getJsonLDMetadata(ctx.bucket, mypath, id)
        outFile.write( bytes(json.dumps(o), 'utf8'))
        outFile.close()
    return

@cli.command()
@click.option('--url', help='the X-Amz-Meta-Url in metadata', required=True)
@click.option('--milled', help='include milled', default=False)
@click.option('--summoned', help='include summon only', default=True)
@common_params
def sourceurl(cfgfile, s3server, s3bucket, upload, output, debug, url, summon, milled):
    """ for a given url, find the sha of the file"""
    ctx = EcConfig(cfgfile, s3server, s3bucket, upload, output, debug)
    ctx.hasS3()
    s3Minio = s3.MinioDatastore(ctx.s3server, None)
    paths = list()
    o_list = list()
    if summon:
        paths = list(s3Minio.listPath(ctx.bucket, 'summoned/', recursive=False))
    if milled:
        paths.extend(list(s3Minio.listPath(ctx.bucket, 'milled/', recursive=False)))
    for path in paths:
        try:
            jsonlds = s3Minio.listPath(ctx.bucket, path.object_name, include_user_meta=True)
            objs = map(lambda f: s3Minio.s3client.stat_object(f.bucket_name, f.object_name), jsonlds)
            o_list.extend(list(filter(lambda f: f.metadata.get('X-Amz-Meta-Url') == url, objs)))
        except Exception as e:
            logging.error(e)

    if len(o_list)>0:
        for o in o_list:
            outFileName = f"{o.metadata.get('X-Amz-Meta-Uniqueid')}.jsonld"
            log.info(outFileName)
            outFile = open(outFileName, "wb")
            s3ObjectInfo = {"bucket_name": ctx.bucket, "object_name": o.object_name}
            resp = s3Minio.getFileFromStore(s3ObjectInfo)
            outFile.write(resp)
            outFile.close()
            outFileName = f"{o.metadata.get('X-Amz-Meta-Uniqueid')}.jsonld.meta.txt"
            log.info(outFileName)
            outFile = open(outFileName, "wb")
            s3ObjectInfo = {"bucket_name": ctx.bucket, "object_name": o.object_name}
            tags = s3Minio.getFileMetadataFromStore(s3ObjectInfo)
            outFile.write(bytes(json.dumps(tags, indent=4), 'utf8'))
            outFile.close()
    else:
        log.info(f"Nothing has been found for url: ", url)
    return


@cli.command()
@click.option('--source', help='One or more repositories (--source a --source b)', multiple=True)
@common_params
def duplicateurls(cfgfile, s3server, s3bucket, upload, output, debug, source):
    """ Find Possible Duplicates based on the URL that was used to summon JSONLD.
    Note, the may be ok, if a given URL has more than one JSONLD in the HTML.
    """
    ctx = EcConfig(cfgfile, s3server, s3bucket, upload, output, debug)
    ctx.hasS3()
    s3Minio = s3.MinioDatastore(ctx.s3server, None)
    df = s3Minio.listDuplicateUrls(ctx.bucket, source)
    try:
        if len(df) <= 0:
            logging.info(f"No object has been found")
            return

        df = df[df['Url Duplicates'] > 1]
        if len(df) <= 0:
            logging.info(f"No duplicate has been found")
            return

        df['Example'] = df.apply(lambda f: f['Name'] + ', ' + str(f['Date']), axis=1)
        df = df.groupby(['Source', 'Url'], group_keys=True, dropna=False) \
            .agg({'Name': 'count', 'Example': lambda x: x.iloc[0:5].tolist()}).reset_index()
        df = df.rename(columns={'Name': 'Duplicates'})

        res = df.to_csv(index=False)
        sys.stdout.write(res)
        if output:
            output.write(bytes(res, 'utf-8'))
        if upload:
            s3Minio.putReportFile(ctx.bucket, "all", "bucketutil_dupliactes.csv", res)
    except Exception as e:
        logging.info(e)
    return 0

@cli.command()
@click.option('--source', help='One or more repositories (--source a --source b)', multiple=True)
@common_params
def stats(cfgfile, s3server, s3bucket, upload, output, debug, source):
    ctx = EcConfig(cfgfile, s3server, s3bucket, upload, output, debug)
    ctx.hasS3()
    s3Minio = s3.MinioDatastore(ctx.s3server, None)
    sources = getSitemapSourcesFromGleaner(cfgfile)
    sources = list(filter(lambda source: source.get('active'), sources))
    sources = list(map(lambda r: r.get('name'), sources))
    sources_to_run = source  # optional if null, run all

    pathMilled = f"/{s3Minio.paths.get('milled')}/"
    pathSummon = f"/{s3Minio.paths.get('summon')}/"
    stats = {'milled': {'total': 0, 'repo': {}}, 'summon': {'total': 0, 'repo': {}}}
    for repo in sources:
        if sources_to_run is not None and len(sources_to_run) > 0:
            if not find(sources_to_run, lambda x: x == repo):
                continue
        countMilled = s3Minio.countPath(ctx.bucket, pathMilled + repo)
        countSummon = s3Minio.countPath(ctx.bucket, pathSummon + repo)
        if countMilled > 0:
            stats['milled']['repo'] |= {repo: countMilled}
            stats['milled']['total'] += countMilled
        if countSummon > 0:
            stats['summon']['repo'] |= {repo: countSummon}
            stats['summon']['total'] += countSummon
    res = json.dumps(stats, sort_keys = True, indent = 4)
    sys.stdout.write(res)
    if output:  # just append the json files to one filem, for now.
        output.write(bytes(res, 'utf-8'))
    if upload:
        s3Minio.putReportFile(ctx.bucket, "all", "bucketutil_stats.json", res)

@cli.command()
@click.option('--source', help='One or more repositories (--source a --source b)', multiple=True)
@common_params
def cullurls(cfgfile, s3server, s3bucket, upload, output, debug, source):
    """ for a given url, find the sha of the file"""
    ctx = EcConfig(cfgfile, s3server, s3bucket, upload, output, debug)
    ctx.hasS3()
    s3Minio = s3.MinioDatastore(ctx.s3server, None)
    utc = pytz.UTC
    df = s3Minio.listDuplicateUrls(ctx.bucket, source)
    try:
        if len(df) <= 0:
            logging.info(f"No object has been found")
            return

        df = df[df['Url Duplicates'] > 1]
        if len(df) <= 0:
            logging.info(f" Nothing to cull")
            return
        # delete duplicated objects that are older than 7 days ago
        df = df[df['Date'] < utc.localize(datetime.datetime.now() - datetime.timedelta(days=7))]
        removeObjectList = df.get('Name').values.tolist()
        for r in removeObjectList:
            s3Minio.removeObject(ctx.bucket, str(r))
            logging.info('Removed object: ' + str(r))
    except Exception as e:
        logging.info(e)
    return

if __name__ == '__main__':
    res = cli()
