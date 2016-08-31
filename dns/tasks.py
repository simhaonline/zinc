from django.core.exceptions import ObjectDoesNotExist
from requests.exceptions import HTTPError

from celery.utils.log import get_task_logger
from celery import shared_task
from celery.exceptions import MaxRetriesExceededError
from celery_once import QueueOnce

from django.conf import settings

from dns.models import IP, Zone
from dns.utils import route53
from dns.utils.generic import list_overlap
from zinc.vendors.lattice import lattice

logger = get_task_logger(__name__)


@shared_task(base=QueueOnce, default_retry_delay=30, max_retries=3,
             soft_time_limit=600, once={'key': [], 'graceful': True})
def lattice_ip_retriever():
    try:
        servers = [server for server in lattice.servers() if
                   list_overlap(server['roles'], settings.LATTICE_ROLES) and
                   server['state'] not in ['unconfigured', 'decommissioned']]
        locations = {d['id']: d['location'] for d in lattice.datacenters()}
    except HTTPError as e:
        logger.exception(e)
        return

    lattice_ips = set()
    for server in servers:
        for ip in server.ips:
            enabled = server['state'] == 'configured'

            datacenter_id = int(server['datacenter_url'].split('/')[-1])
            location = locations.get(datacenter_id, 'fake_location')

            friendly_name = '{} {} {}'.format(server['hostname'],
                                              server['datacenter_name'],
                                              location)
            cron_ip = IP(ip=ip['ip'], hostname=server['hostname'],
                         friendly_name=friendly_name, enabled=enabled)

            try:
                cron_ip.save()
                lattice_ips.add(ip['ip'])
            except Exception as e:
                logger.info('{} - {}'.format(ip, e))

    ips_to_remove = set(IP.objects.values_list('ip', flat=True)) - lattice_ips
    IP.objects.filter(ip__in=ips_to_remove).delete()


@shared_task(bind=True, ignore_result=True, default_retry_delay=60)
def aws_delete_zone(self, zone_id, root):
    aws_zone = route53.Zone(id=zone_id, root=root)

    try:
        aws_zone.delete()
    except Exception as e:
        logger.exception(e)
        try:
            self.retry()
        except MaxRetriesExceededError:
            logger.error('Failed to remove zone {}'.format(zone_id))