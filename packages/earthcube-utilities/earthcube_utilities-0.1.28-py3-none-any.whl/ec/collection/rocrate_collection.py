import hashlib
import tempfile
from os import path
import uuid

import uuid as uuid
from rocrate.rocrate import ROCrate
from rocrate.model.person import Person
from rocrate.model.softwareapplication import SoftwareApplication
from rocrate.model.contextentity import ContextEntity
from rocrate.model.data_entity import DataEntity
from rocrate.model.computationalworkflow import ComputationalWorkflow

from rocrate.model.dataset import Dataset
from rocrate.model.metadata import Metadata
from rocrate.model.file import File
from rocrate.model.file_or_dir import FileOrDir

from rocrateValidator import validate
from ec.datastore.s3 import MinioDatastore

## Fair Signposting
# https://pypi.org/project/signposting/
# https://signposting.org/FAIR/
# https://fair-impact.eu/enabling-fair-signposting-and-ro-crate-contentmetadata-discovery-and-consumption
#######

# issue https://github.com/earthcube/GeoCODES-Metadata/issues/5
# logic that might be utilize
# https://github.com/MBcode/ec/blob/8255d7c1312faca721000535b85cd1e22470a73e/ec.py#L2472

##### THOUGHTS #####
# creating a crate
# it will have multiple objects that are in a collection.
# for a collection on the client, we will ask the user to select the distribution to be utilize
# that will be added to the rocrate

# create named crate
# add creator
# for each 'dataset' add to crate as dietibution
# for each tool add to create a worklflow

# then create a friggin tool that read the firrig crate from frigging s3,
# now, that it is downloaded, head the distribitions.
# create tool to download the frigging links from the firring distributions.
# then tell the tool where the files are, and execute the tool
#  how frigging hard can that workflow be to understand.
#  linking tool to the datasets to the tool will be the fun part



#####
# add distribution... up here to prevent some linting errors
######
"""
 web etities: https://www.researchobject.org/ro-crate/1.1/data-entities.html#web-based-data-entities
 {
     "@id": "https://zenodo.org/record/3541888/files/ro-crate-1.0.0.pdf",
     "@type": "File",
     "name": "RO-Crate specification",
     "contentSize": "310691",
     "description": "RO-Crate specification",
     "encodingFormat": "application/pdf"
   }
 """

# option 2: it's a dataset frament

"""
  {
    "@id": "lots_of_little_files/",
    "@type": "Dataset",
    "name": "Too many files",
    "description": "This directory contains many small files, that we're not going to describe in detail.",
    "distribution": {"@id": "http://example.com/downloads/2020/lots_of_little_files.zip"}
  }
"""

# option 3: it's a data download

"""
 {
    "@id": "http://example.com/downloads/2020/lots_of_little_files.zip",
    "@type": "DataDownload",
    "encodingFormat": "application/zip",
    "contentSize": "82818928"
  }
"""



# this tool will read information from an s3 bucket, or a local zip crate
def readDecoderRoCrate(crate, bucket="gleaner", s3endpoint=None) -> ROCrate:
    if (s3endpoint is not None):
        client = MinioDatastore(s3endpoint)
        data = client.getRoCrateFile(crate, bucket=bucket)
        p = path.join(tempfile.gettempdir(), crate)
        with open(p, mode='wb') as f:
            f.write(crate)
        crate = p
    crate = ROCrate(crate)  # or ROCrate('exp_crate.zip')
    return crate


def RoCrateToGraph(crate, endpoint=None):
    crate = ROCrate(crate)  # or ROCrate('exp_crate.zip')
    # convert to graph
    # upload to blazegraph, ignore... but let us search for what is being linked to
    pass


## routines that should accept the Schema.org JSONLd object for RO Crate api's
## and do some courtesy conversion.
### really thiw will need to be done on the javascript side, but
## prototype it here
def _createIdentifier(proposedid):
    if proposedid is not None and isinstance(proposedid, str):

        m = hashlib.md5(proposedid.encode(encoding='UTF-8', errors='strict')).hexdigest()
    else:
        # random id
        m = uuid.uuid4().hex
    return f"uuid:{m}"

DATASET__DATA_DOWNLOAD = '@DataDownload'  # distribution
DATASET__DATASET = '@Dataset'  # Dataset
DATASET__WEB_ENTITY = '@File'  # url, aka web link
# DATASET__WEB_SERVICE = '@SERVICE'   #how do we do a service?

## we do not want to override the methods, we want to add methods
# crates are a bit of a pain because they use disk layout, rather than just metadata file

class SosRocrate(ROCrate):
    """ Science on Schema(SOS) ROCrate Object.
    ROCrate plus methods to easily add SOS information to an ROCrate

    USE:
     [Consuming an RO-Crate](https://github.com/ResearchObject/ro-crate-py#consuming-an-ro-crate):
    use SosRocrate instead of RoCrate

    """
    def nameCrate(self, aName):
        self.nameCrate(aName)

    # this is the creator of the crate, it should be a sos_person
    # probably not correct, but it's a start
    def addSosCreator(self, crate, username):
        properties = {"name": username}

        creator = Person(crate, identifier=_createIdentifier(username), properties=properties)
        self.creator=creator

    # we are  of the crate, it should be a sos_person
    # probably not correct, but it's a start
    def addSosPublisher(self, crate, identifier=None, name=None):
        properties = {"name": name}
        if identifier is None:
            identifier = name
        creator = Person(crate, identifier=_createIdentifier(identifier), properties=properties)
        self.publisher = creator

        # pption 1 it's a file




    def addSosDistribution(self, crate, dataset_jsonld, distribution_to_add=None, distType=DATASET__DATA_DOWNLOAD):
        aurl = dataset_jsonld.get('url')
        name = dataset_jsonld.get('name')
        if distribution_to_add is None:
            #kw = {"fetch_remote": fetch_remote, "validate_url": validate_url}
            kw = {"name": name}
            self.add_file(aurl, properties=kw)
        elif distType == DATASET__DATA_DOWNLOAD :
            pass
        elif distType == DATASET__DATASET:
            self.add_dataset(source=dataset_jsonld)

    def addSosServicesAsEntity(self,crate, url=None, name=None):
        kw = {"name": name}
        self.add_file(source=url, properties=kw)
        pass

    def addSosURL(self, url=None, name=None):
        properties = {"name":name}
        self.add_file(source=url, properties=properties)
        #self.add_file(url, identifier=CreateIdentifier(url), properties=kw)

# two possible ways to add the whole JSONLD.
    # 1. File: url plus the jsonld
    # 2. Dataset (aka directory): url to geocodes, plus jsonld

    # these need to check that these are datasets ;)
    def addSosDatasetAsFile(self, dataset_jsonld,  url):
        properties = dataset_jsonld
        self.add_file(source=url, properties=properties)
### humm https://github.com/ResearchObject/ro-crate-py#adding-entities-with-an-arbitrary-type
    def addSosDatasetAsDataset(self, dataset_jsonld, urn, distType=DATASET__DATASET):
        self.add_dataset(dest_path=urn, properties=dataset_jsonld)


    # this does not get added to hasParts... aka does not get Identifieed as a Dataset
    def addSosDatasetAsCtxEntity(self, dataset_jsonld, urn, distType=DATASET__DATASET):
        """Not useful. this does not get added to hasParts... aka does not get Identifieed as a Dataset """
        datasetCtxEntity =ContextEntity(self, identifier=urn, properties=dataset_jsonld)

        self.add(datasetCtxEntity)
    def addSosContact(self, sos_contact):
            pass
