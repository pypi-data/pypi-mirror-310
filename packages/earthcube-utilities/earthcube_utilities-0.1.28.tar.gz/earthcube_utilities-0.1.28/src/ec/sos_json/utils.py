import json
import logging
from typing import Union, Tuple, Any

from jsonschema import validate
from jsonschema.exceptions import ValidationError
from string import Template

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

from pydash import ends_with, sort
from pyld import jsonld
import ec.sos_json.schemas as schemafiles

jsonld_context = context = {"@vocab": "https://schema.org/"}


def _getSchemaFromResources(filename) :
    """ retrieves json schema file from the  ec.sos_json.schemas directory when in a package"""
    resourcename = f"{filename}.json"
    resource = pkg_resources.read_text(schemafiles, resourcename)
    schema = json.loads(resource)
    return schema


def isValidJSON(jsonData: str)-> bool:
    """Is Json Valid"""
    try:
        json.loads(jsonData)
    except ValueError as err:
        return False
    return True

def listSchemaFilesFromResources() -> str:
    """ retrieves schema file from the schemas folder when in a package"""
    resource = pkg_resources.contents(schemafiles)
    files = filter( lambda f: ends_with(f, ".json"), resource)
    files = sort(list(files))
    return files
def validateJson2Schema(json_data: Any, schemaname='GeoCodes-DatasetSchema') -> Tuple[bool,str]:
    """REF: https://json-schema.org/

    Parameters:
        json_data: JSON Object (aka json.loads())
        schemaname: name of schem in ec.sos_json.shcemas: (GeoCodes-DatasetSchema or GeoCodes-ECRR-DatasetSchema.json)

    Returns:
        bool: is valid
        message: "Given JSON data is Valid" or "Given JSON data is InValid"
        """
    # Describe what kind of json you expect.
    execute_api_schema = _getSchemaFromResources(schemaname)

    try:
        validate(instance=json_data, schema=execute_api_schema)
    except ValidationError as err:
        logging.error(err)
        err = f"Given JSON data is InValid {err}"
        return False, err

    message = "Given JSON data is Valid"
    return True, message


def validateSosDataset(jsonData: str) -> bool:
    """ validates a SOS Dataset"""
    try:
        json_data = json.loads(jsonData)
    except ValueError as err:
        return False
    valid2_schema, err = validateJson2Schema(jsonData)
    return valid2_schema


def validateEcrrTool(jsonData : str) -> bool:
    """
       validated
        Parameters:
            jsonData: jsonld string returns the string
            form: 'compact'--compact form,
                   'frome'--framed usngin schemaType,
                   'jsonld' - passed form
            schemaType: type of the schema default="Dataset"
        Returns:
            bool.

    """
    try:
        json_data = json.loads(jsonData)
    except ValueError as err:
        return False
    valid2_schema, err = validateJson2Schema(jsonData, schemaname="GeoCodes-ECRR-DatasetSchema.json")
    return valid2_schema


def compact_jld_str(jld_str: str) -> str:
    """
       depreciated use formatted_jsonld

    """
    doc = json.loads(jld_str)
    compacted = jsonld.compact(doc, jsonld_context)
    r = json.dumps(compacted, indent=2)
    return r


def formatted_jsonld(jld_str: str, form="compact", schemaType="Dataset") -> str:
    """
       returns a formatted JSONLD string based on the input
        Parameters:
            jld_str: jsonld string returns the string
            form: 'compact'--compact form,
                   'frome'--framed usngin schemaType,
                   'jsonld' - passed form
            schemaType: type of the schema default="Dataset"
        Returns:
            string.

    """
    if (form == 'jsonld'):
        return jld_str

    elif (form == "frame"):
        frame = (' {\n'
                 '              "@context": {\n'
                 '                "@vocab": "https://schema.org/",\n'
                 '                    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",\n'
                 '                    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",\n'
                 '                    "schema": "https://schema.org/",\n'
                 '                    "xsd": "http://www.w3.org/2001/XMLSchema#"\n'
                 '              },\n'
                 '              "@type": "schema:${schemaType}"\n'
                 '  }\n '
                 )
        f_template = Template(frame)
        thsGraphQuery = f_template.substitute(schemaType=schemaType)

        frame_doc = json.loads(thsGraphQuery)
        doc = json.loads(jld_str)
 #       doc = jsonld.flatten(doc)
        # issue where @id on Dataset and @id on Dataset.identifer were the same. If so
        # @type = ['Dataset', 'PropertyValue'] was the conversion.

        framed = jsonld.frame(doc, frame_doc)

        r = json.dumps(framed, indent=2)
        return r
    else:  # compact
        doc = json.loads(jld_str)
        compacted = jsonld.compact(doc, jsonld_context)
        r = json.dumps(compacted, indent=2)
        return r
