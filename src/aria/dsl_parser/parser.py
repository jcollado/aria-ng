
from aria.parser import DefaultParser

def parse_from_path(dsl_file_path,
                    resources_base_url=None,
                    resolver=None,
                    validate_version=True,
                    additional_resource_sources=()):
    print '!!! parse_from_path'
    print dsl_file_path
    #print resources_base_url
    #print resolver
    #print validate_version
    #print additional_resource_sources
    
    parser = DefaultParser(dsl_file_path)
    #presentation = parser.parse()
    presentation, issues = parser.validate()
    if issues:
        print 'Validation issues:'
        for i in issues:
            print ' ', str(i)
    return presentation
    
def parse(dsl_string,
          resources_base_url=None,
          resolver=None,
          validate_version=True):
    print '!!! parse'
    print dsl_string
    print resources_base_url
    print resolver
    print validate_version
