
def parse_from_path(dsl_file_path,
                    resources_base_url=None,
                    resolver=None,
                    validate_version=True,
                    additional_resource_sources=()):
    pass
    
def parse(dsl_string,
          resources_base_url=None,
          resolver=None,
          validate_version=True):
    return _parse(dsl_string,
                  resources_base_url=resources_base_url,
                  resolver=resolver,
                  validate_version=validate_version)
