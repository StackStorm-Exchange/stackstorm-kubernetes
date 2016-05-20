import sys
from st2actions.runners.pythonrunner import Action
from boto.route53.connection import Route53Connection
from boto.route53.record import ResourceRecordSets


class Route53Alias(Action):

    def run(
            self,
            cmd,
            hosted_zone_name=None,
            name=None,
            alias_dns_name=None,
            payload=None,
            config=None):

        try:
            if payload:
                name_prefix = payload['labels']['name_prefix']
                alias_dns_name = payload['labels']['alias_dns_name']
                hosted_zone_name = payload['labels']['hosted_zone_name']
                name = name_prefix + '.' + hosted_zone_name

        except:
            self.logger.exception(
                'Cannot validate kubernetes payload request for route53 alias!')
            raise

        try:
            conn = Route53Connection()
            zone = conn.get_hosted_zone_by_name(hosted_zone_name)
            hosted_zone_id = zone.Id.split("/")[2]
            changes = ResourceRecordSets(conn, hosted_zone_id)
            change = changes.add_change(
                cmd,
                name,
                "A",
                alias_hosted_zone_id=hosted_zone_id,
                alias_dns_name=alias_dns_name,
                alias_evaluate_target_health=False)
            result = changes.commit()

        except Exception as err:
            sys.stderr.write('ERROR: %s\n' % str(err))
            raise
