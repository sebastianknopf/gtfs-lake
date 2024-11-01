import json
import polars as pl
import time
import yaml

from fastapi import APIRouter
from fastapi import FastAPI
from fastapi import Request
from fastapi import Response

from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import ParseDict

from gtfslake.lake import GtfsLake

class GtfsLakeRealtimeServer:

    def __init__(self, database_filename: str, config_filename: str|None):

		# connect to GTFS lake database
        self._lake = GtfsLake(database_filename)

        # load config and set default values
        if config_filename is not None:
            with open(config_filename, 'r') as config_file:
                self._config = yaml.safe_load(config_file)

        self._config = dict()
        self._config['app'] = dict()
        self._config['app']['caching_enabled'] = False
        self._config['app']['caching_server_endpoint'] = ''
        self._config['app']['caching_service_alerts_ttl_seconds'] = 60
        self._config['app']['caching_trip_updates_ttl_seconds'] = 30
        self._config['app']['caching_vehicle_positions_ttl_seconds'] = 15

        self._config['app']['routing'] = dict()
        self._config['app']['routing']['service_alerts_endpoint'] = '/gtfs/realtime/service-alerts.pbf'
        self._config['app']['routing']['trip_updates_endpoint'] = '/gtfs/realtime/trip-updates.pbf'
        self._config['app']['routing']['vehicle_positions_endpoint'] = '/gtfs/realtime/vehicle-positions.pbf'

        # create routes
        self._fastapi = FastAPI()
        self._api_router = APIRouter()

        self._api_router.add_api_route(self._config['app']['routing']['service_alerts_endpoint'], endpoint=self._service_alerts, methods=['GET'], name='service_alerts')
        self._api_router.add_api_route(self._config['app']['routing']['trip_updates_endpoint'], endpoint=self._trip_updates, methods=['GET'], name='trip_updates')
        self._api_router.add_api_route(self._config['app']['routing']['vehicle_positions_endpoint'], endpoint=self._vehicle_positions, methods=['GET'], name='vehicle_positions')

        # enable chaching if configured
        if 'caching_enabled' in self._config['app'] and self._config['app']['caching_enabled'] == True:
            import memcache

            self._cache = memcache.Client([self._config['caching']['caching_server_endpoint']], debug=0)
            self._cache_ttl = self._config['caching']['caching_server_ttl_seconds']
        else:
            self._cache = None

    async def _service_alerts(self, request: Request) -> Response:
        service_alerts, alert_active_periods, alert_informed_entities = self._lake.fetch_realtime_service_alerts()

        objects = list()
        for service_alert in service_alerts.iter_rows(named=True):

            obj = dict()
            obj['id'] = service_alert['service_alert_id']

            obj['alert'] = dict()
            obj['alert']['cause'] = service_alert['cause']
            obj['alert']['effect'] = service_alert['effect']

            obj['alert']['header_text'] = dict()
            obj['alert']['header_text']['translation'] = list()
            obj['alert']['header_text']['translation'].append({
                'text': service_alert['header_text'],
                'language': 'de-DE'
            })

            obj['alert']['description_text'] = dict()
            obj['alert']['description_text']['translation'] = list()
            obj['alert']['description_text']['translation'].append({
                'text': service_alert['description_text'],
                'language': 'de-DE'
            })

            obj['alert']['active_period'] = list()
            obj['alert']['informed_entity'] = list()

            for active_period in alert_active_periods.filter(pl.col('service_alert_id') == service_alert['service_alert_id']).iter_rows(named=True):
                obj['alert']['active_period'].append({
                    'start': active_period['start_timestamp'],
                    'end': active_period['end_timestamp']
                })

            for informed_entity in alert_informed_entities.filter(pl.col('service_alert_id') == service_alert['service_alert_id']).iter_rows(named=True):
                ie = dict()

                if informed_entity['agency_id'] is not None:
                    ie['agency_id'] = informed_entity['agency_id']

                if informed_entity['route_id'] is not None:
                    ie['route_id'] = informed_entity['route_id']    

                if informed_entity['route_type'] is not None:
                    ie['route_type'] = informed_entity['route_type']

                if informed_entity['stop_id'] is not None:
                    ie['stop_id'] = informed_entity['stop_id']    

                # TODO: implement trip descriptor here ...
                
                obj['alert']['informed_entity'].append(ie)

            objects.append(obj)

        # send response
        feed_message = self._create_feed_message(objects)
        if 'f' in request.query_params and request.query_params['f'] == 'json':
            return self._send_json_response(feed_message)
        else:
            return self._send_pbf_response(feed_message)

    async def _trip_updates(self, request: Request) -> Response:
        return 'Test'

    async def _vehicle_positions(self, request: Request) -> Response:
        return 'Test'
    
    def _send_json_response(self, feed_message):
        json_result = json.dumps(feed_message)
        return Response(content=json_result, media_type='application/json')

    def _send_pbf_response(self, feed_message):
        pbf_result = ParseDict(feed_message, gtfs_realtime_pb2.FeedMessage()).SerializeToString()
        return Response(content=pbf_result, media_type='application/protobuf')
    
    def _create_feed_message(self, entities):
        return {
            'header': {
                'gtfs_realtime_version': '2.0',
                'incrementality': 'FULL_DATASET',
                'timestamp': time.time()
            },
            'entity': entities
        }

    def create(self):
        self._fastapi.include_router(self._api_router)

        return self._fastapi
