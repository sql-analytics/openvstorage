# license see http://www.openvstorage.com/licenses/opensource/
"""
Statistics module
"""
import re
import datetime
import ConfigParser
from backend.serializers.memcached import MemcacheSerializer
from backend.decorators import required_roles, expose
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ovs.extensions.storage.volatilefactory import VolatileFactory


class MemcacheViewSet(viewsets.ViewSet):
    """
    Information about memcache instances
    """
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def _get_memcachelocation():
        """
        Reads the memcache location out of the configuration files
        """
        parser = ConfigParser.RawConfigParser()
        parser.read('/opt/OpenvStorage/config/memcacheclient.cfg')
        local_node = parser.get('main', 'local_node')
        return parser.get(local_node, 'location')

    @staticmethod
    def _get_instance(host):
        """
        Returns a class with more information about a given memcache instance
        """
        class Stats:
            """
            Placeholder class for statistics
            """
            pass

        import memcache
        host = memcache._Host(host)
        host.connect()
        host.send_cmd("stats")
        stats = Stats()
        while 1:
            line = host.readline().split(None, 2)
            if line[0] == "END":
                break
            stat, key, value = line
            try:
                # Convert to native type, if possible
                value = int(value)
                if key == "uptime":
                    value = datetime.timedelta(seconds=value)
                elif key == "time":
                    value = datetime.datetime.fromtimestamp(value)
            except ValueError:
                pass
            setattr(stats, key, value)
        host.close_socket()
        return stats

    @staticmethod
    def _add_dal_stats(stats):
        """
        Adds ovs dal statistics to the stats object
        """
        volatile = VolatileFactory.get_client()
        setattr(stats, 'ovs_dal', {})
        keys = ['datalist', 'object_load', 'descriptor', 'relations']
        for key in keys:
            for hittype in ['hit', 'miss']:
                cachekey = 'ovs_stats_cache_%s_%s' % (key, hittype)
                stats.ovs_dal['%s_%s' % (key, hittype)] = volatile.get(cachekey) or 0

    @expose(internal=True)
    @required_roles(['view'])
    def list(self, request, format=None):
        """
        Returns statistics information
        """
        _ = request, format
        match = re.match("([.\w]+:\d+)", MemcacheViewSet._get_memcachelocation())
        if not match:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        stats = MemcacheViewSet._get_instance(match.group(1))
        MemcacheViewSet._add_dal_stats(stats)
        serializer = MemcacheSerializer(stats)
        return Response(serializer.data)

    @expose(internal=True)
    @required_roles(['view'])
    def retrieve(self, request, pk=None, format=None):
        """
        Returns statistics information
        """
        _ = request, format, pk
        match = re.match("([.\w]+:\d+)", MemcacheViewSet._get_memcachelocation())
        if not match:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        stats = MemcacheViewSet._get_instance(match.group(1))
        MemcacheViewSet._add_dal_stats(stats)
        serializer = MemcacheSerializer(stats)
        return Response(serializer.data)
