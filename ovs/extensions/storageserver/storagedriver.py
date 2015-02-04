# Copyright 2014 CloudFounders NV
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Wrapper class for the storagedriverclient of the voldrv team
"""

from volumedriver.storagerouter.storagerouterclient import StorageRouterClient as SRClient, MDSClient, MDSNodeConfig
from volumedriver.storagerouter.storagerouterclient import ClusterContact, Statistics, VolumeInfo
from ovs.plugin.provider.configuration import Configuration
import json
import os
import copy

client_vpool_cache = {}
client_storagedriver_cache = {}
mdsclient_service_cache = {}


class StorageDriverClient(object):
    """
    Client to access storagedriverclient
    """

    foc_status = {'': 0,
                  'ok_standalone': 10,
                  'ok_sync': 10,
                  'catch_up': 20,
                  'degraded': 30}
    empty_statistics = staticmethod(lambda: Statistics())
    empty_info = staticmethod(lambda: VolumeInfo())
    stat_counters = ['backend_data_read', 'backend_data_written',
                     'backend_read_operations', 'backend_write_operations',
                     'cluster_cache_hits', 'cluster_cache_misses', 'data_read',
                     'data_written', 'metadata_store_hits', 'metadata_store_misses',
                     'read_operations', 'sco_cache_hits', 'sco_cache_misses',
                     'write_operations']
    stat_sums = {'operations': ['write_operations', 'read_operations'],
                 'cache_hits': ['sco_cache_hits', 'cluster_cache_hits'],
                 'data_transferred': ['data_written', 'data_read']}
    stat_keys = stat_counters + stat_sums.keys()

    def __init__(self):
        """
        Dummy init method
        """
        pass

    @staticmethod
    def load(vpool):
        """
        Initializes the wrapper given a vpool name for which it finds the corresponding Storage Driver
        Loads and returns the client
        """

        key = vpool.guid
        if key not in client_vpool_cache:
            cluster_contacts = []
            for storagedriver in vpool.storagedrivers[:3]:
                cluster_contacts.append(ClusterContact(str(storagedriver.cluster_ip), storagedriver.ports[1]))
            client = SRClient(str(vpool.guid), cluster_contacts)
            client_vpool_cache[key] = client
        return client_vpool_cache[key]


class MetadataServerClient(object):
    """
    Builds a MDSClient
    """

    def __init__(self):
        """
        Dummy init method
        """
        pass

    @staticmethod
    def load(service):
        """
        Loads a MDSClient
        """

        key = service.guid
        if key not in mdsclient_service_cache:
            try:
                client = MDSClient(MDSNodeConfig(address=str(service.storagerouter.ip), port=service.ports[0]))
                mdsclient_service_cache[key] = client
            except RuntimeError:
                return None
        return mdsclient_service_cache[key]


class StorageDriverConfiguration(object):
    """
    StorageDriver configuration class
    """

    # The below dictionary is GENERATED by the storagedriver
    # - Specific test generating the output: ConfigurationTest.print_framework_parameter_dict
    # DO NOT MAKE MANUAL CHANGES HERE

    parameters = {
        # hg branch: metadata-server
        # hg revision: afbe1c1a12ab
        # buildTime: Fri Jan 16 10:55:56 CET 2015
        'metadataserver': {
            'metadata_server': {
                'optional': ['mds_db_type', 'mds_cached_pages', 'mds_poll_secs', 'mds_address', ],
                'mandatory': ['mds_port', 'mds_scratch_dir', 'mds_rocksdb_path', ]
            },
            'backend_connection_manager': {
                'optional': ['backend_type', 'rest_connection_host', 'rest_connection_port', 'rest_connection_timeout_secs', 'rest_connection_metadata_format', 'rest_connection_entries_per_chunk', 'rest_connection_verbose_logging', 'rest_connection_user', 'rest_connection_password', 'rest_connection_encryption_policy', 's3_connection_host', 's3_connection_port', 's3_connection_username', 's3_connection_password', 's3_connection_verbose_logging', 's3_connection_use_ssl', 's3_connection_ssl_verify_host', 's3_connection_ssl_cert_file', 's3_connection_flavour', 'alba_connection_host', 'alba_connection_port', 'alba_connection_timeout', ],
                'mandatory': ['rest_connection_policy_id', 'local_connection_path', ]
            },
        },
        'storagedriver': {
            'backend_connection_manager': {
                'optional': ['backend_type', 'rest_connection_host', 'rest_connection_port', 'rest_connection_timeout_secs', 'rest_connection_metadata_format', 'rest_connection_entries_per_chunk', 'rest_connection_verbose_logging', 'rest_connection_user', 'rest_connection_password', 'rest_connection_encryption_policy', 's3_connection_host', 's3_connection_port', 's3_connection_username', 's3_connection_password', 's3_connection_verbose_logging', 's3_connection_use_ssl', 's3_connection_ssl_verify_host', 's3_connection_ssl_cert_file', 's3_connection_flavour', 'alba_connection_host', 'alba_connection_port', 'alba_connection_timeout', ],
                'mandatory': ['rest_connection_policy_id', 'local_connection_path', ]
            },
            'content_addressed_cache': {
                'optional': ['serialize_read_cache', ],
                'mandatory': ['read_cache_serialization_path', 'clustercache_mount_points', ]
            },
            'event_publisher': {
                'optional': ['events_amqp_exchange', 'events_amqp_routing_key', ],
                'mandatory': ['events_amqp_uris', ]
            },
            'failovercache': {
                'optional': [],
                'mandatory': ['failovercache_path', ]
            },
            'file_driver': {
                'optional': ['fd_extent_cache_capacity', ],
                'mandatory': ['fd_cache_path', 'fd_namespace', ]
            },
            'filesystem': {
                'optional': ['fs_ignore_sync', 'fs_raw_disk_suffix', 'fs_max_open_files', 'fs_metadata_backend_type', 'fs_metadata_backend_arakoon_cluster_id', ],
                'mandatory': ['fs_virtual_disk_format', 'fs_file_event_rules', 'fs_metadata_backend_arakoon_cluster_nodes', 'fs_metadata_backend_mds_nodes', ]
            },
            'scocache': {
                'optional': [],
                'mandatory': ['trigger_gap', 'backoff_gap', 'scocache_mount_points', ]
            },
            'threadpool_component': {
                'optional': ['num_threads', ],
                'mandatory': []
            },
            'volume_manager': {
                'optional': ['open_scos_per_volume', 'foc_throttle_usecs', 'foc_queue_depth', 'foc_write_trigger', 'sap_persist_interval', 'failovercache_check_interval_in_seconds', 'read_cache_default_behaviour', 'required_tlog_freespace', 'required_meta_freespace', 'freespace_check_interval', 'number_of_scos_in_tlog', 'non_disposable_scos_factor', 'debug_metadata_path', 'arakoon_metadata_sequence_size', ],
                'mandatory': ['metadata_path', 'tlog_path', 'clean_interval', ]
            },
            'volume_registry': {
                'optional': ['vregistry_arakoon_timeout_ms', ],
                'mandatory': ['vregistry_arakoon_cluster_id', 'vregistry_arakoon_cluster_nodes', ]
            },
            'volume_router': {
                'optional': ['vrouter_local_io_sleep_before_retry_usecs', 'vrouter_local_io_retries', 'vrouter_volume_read_threshold', 'vrouter_volume_write_threshold', 'vrouter_file_read_threshold', 'vrouter_file_write_threshold', 'vrouter_redirect_timeout_ms', 'vrouter_redirect_retries', 'vrouter_sco_multiplier', 'vrouter_routing_retries', 'vrouter_min_workers', 'vrouter_max_workers', ],
                'mandatory': ['vrouter_id', ]
            },
            'volume_router_cluster': {
                'optional': [],
                'mandatory': ['vrouter_cluster_id', ]
            },
        },
    }

    def __init__(self, config_type, vpool_name, number=None):
        """
        Initializes the class
        """

        def make_configure(sct):
            """ section closure """
            return lambda **kwargs: self._add(sct, **kwargs)

        if config_type not in ['storagedriver', 'metadataserver']:
            raise RuntimeError('Invalid configuration type. Allowed: storagedriver, metadataserver')
        self.config_type = config_type
        self.vpool_name = vpool_name
        self.configuration = {}
        self.is_new = True
        self.number = number
        self.params = copy.deepcopy(StorageDriverConfiguration.parameters)  # Never use parameters directly
        self.base_path = '{0}/storagedriver/{1}'.format(Configuration.get('ovs.core.cfgdir'), self.config_type)
        if self.number is None:
            self.path = '{0}/{1}.json'.format(self.base_path, self.vpool_name)
        else:
            self.path = '{0}/{1}_{2}.json'.format(self.base_path, self.vpool_name, self.number)
        # Fix some manual "I know what I'm doing" overrides
        backend_connection_manager = 'backend_connection_manager'
        self.params[self.config_type][backend_connection_manager]['optional'].append('s3_connection_strict_consistency')
        # Generate configure_* methods
        for section in self.params[self.config_type]:
            setattr(self, 'configure_{0}'.format(section), make_configure(section))

    def load(self, client=None):
        """
        Loads the configuration from a given file, optionally a remote one
        """
        contents = '{}'
        if client is None:
            if os.path.isfile(self.path):
                with open(self.path, 'r') as config_file:
                    contents = config_file.readall()
                    self.is_new = False
        else:
            if client.file_exists(self.path):
                contents = client.file_read(self.path)
                self.is_new = False
        self.configuration = json.loads(contents)

    def save(self, client=None):
        """
        Saves the configuration to a given file, optionally a remote one
        """
        self._validate()
        contents = json.dumps(self.configuration, indent=2)
        if client is None:
            os.makedirs(self.base_path)
            with open(self.path, 'w') as config_file:
                config_file.write(contents)
                self.is_new = False
        else:
            client.run('mkdir -p {0}'.format(self.base_path))
            client.file_write(self.path, contents)
            self.is_new = False

    def clean(self):
        """
        Cleans the loaded configuration, removing all obsolete parameters
        """
        for section, entries in self.params[self.config_type].iteritems():
            if section in self.configuration:
                for param in self.configuration[section]:
                    if param not in entries['mandatory'] and param not in entries['optional']:
                        del self.configuration[section][param]

    @staticmethod
    def build_filesystem_by_hypervisor(hypervisor_type):
        """
        Builds a filesystem configuration dict, based on a given hypervisor
        """
        if hypervisor_type == 'VMWARE':
            return {'fs_virtual_disk_format': 'vmdk',
                    'fs_file_event_rules': [{'fs_file_event_rule_calls': ['Mknod', 'Unlink', 'Rename'],
                                             'fs_file_event_rule_path_regex': '.*.vmx'},
                                            {'fs_file_event_rule_calls': ['Rename'],
                                             'fs_file_event_rule_path_regex': '.*.vmx~'}]}
        if hypervisor_type == 'KVM':
            return {'fs_virtual_disk_format': 'raw',
                    'fs_raw_disk_suffix': '.raw',
                    'fs_file_event_rules': [{'fs_file_event_rule_calls': ['Mknod', 'Unlink', 'Rename', 'Write'],
                                             'fs_file_event_rule_path_regex': '(?!vmcasts)(.*.xml)'}]}
        return {}

    def _validate(self):
        """
        Validates the loaded configuration agains the mandatory and optional parameters
        """
        # Fix some manual "I know what I'm doing" overrides
        backend_connection_manager = 'backend_connection_manager'
        backend_type = 'backend_type'
        if self.configuration.get(backend_connection_manager, {}).get(backend_type, '') != 'REST':
            self.params[self.config_type][backend_connection_manager]['mandatory'].remove('rest_connection_policy_id')
            self.params[self.config_type][backend_connection_manager]['optional'].append('rest_connection_policy_id')
        if self.configuration.get(backend_connection_manager, {}).get(backend_type, '') != 'LOCAL':
            self.params[self.config_type][backend_connection_manager]['mandatory'].remove('local_connection_path')
            self.params[self.config_type][backend_connection_manager]['optional'].append('local_connection_path')
        # Validation
        errors = []
        for section, entries in self.params[self.config_type].iteritems():
            if section not in self.configuration:
                if len(entries['mandatory']) > 0:
                    errors.append('Section {0} was not found'.format(section))
            else:
                for param in entries['mandatory']:
                    if param not in self.configuration[section]:
                        errors.append('Key {0} -> {1} missing'.format(section, param))
                for param in self.configuration[section]:
                    if param not in entries['mandatory'] and param not in entries['optional']:
                        errors.append('Key {0} -> {1} is obsolete/invalid'.format(section, param))
        if errors:
            raise RuntimeError('Invalid configuration:\n  {0}'.format('\n  '.join(errors)))

    def _add(self, section, **kwargs):
        """
        Configures a section
        """
        sparams = self.params[self.config_type][section]
        errors = []
        for item in kwargs:
            if item not in sparams['mandatory'] and item not in sparams['optional']:
                errors.append(item)
        if errors:
            raise RuntimeError('Invalid parameters:\n  {0}'.format('\n  '.join(errors)))
        for item, value in kwargs.iteritems():
            if section not in self.configuration:
                self.configuration[section] = {}
            self.configuration[section][item] = value


class GaneshaConfiguration:

    def __init__(self):
        self._config_corefile = os.path.join(Configuration.get('ovs.core.cfgdir'), 'templates', 'ganesha-core.conf')
        self._config_exportfile = os.path.join(Configuration.get('ovs.core.cfgdir'), 'templates', 'ganesha-export.conf')

    def generate_config(self, target_file, params):
        with open(self._config_corefile, 'r') as core_config_file:
            config = core_config_file.read()
        with open(self._config_exportfile, 'r') as export_section_file:
            config += export_section_file.read()

        for key, value in params.iteritems():
            print 'replacing {0} by {1}'.format(key, value)
            config = config.replace(key, value)

        with open(target_file, 'wb') as config_out:
            config_out.write(config)
