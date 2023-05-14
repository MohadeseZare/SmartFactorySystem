import traceback
from datetime import datetime
from dateutil import parser
from django.utils.dateparse import parse_datetime
from django.http import HttpResponse, FileResponse
from django.views.decorators.gzip import gzip_page
import json
import requests
from rest_framework import generics, renderers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
import os
import pandas as pd
import xlsxwriter
from ast import literal_eval

from device.api.serializers import *
from device.models import DeviceType, Device, HistoryData, ErrorLine
from .gatewayApis import inlocal_local_getLogs, inlocal_server_getLogs, inserver_getLogs
from .gatewayApis import inlocal_server_live, inlocal_local_live, inserver_live, inserver_line_live
from .gatewayApis import inlocal_local_getLogsData, inserver_line_error
from .gatewayApis import inlocal_Line_daily_static, inlocal_Line_stoppage_time, inlocal_Line_log_data
from .gatewayApis import inlocal_Line_error_frequency, inlocal_Line_cumulativeChart
from factory.models import *


def cal_logs(start_time, end_time, mac_address, pin, position, device_type):
    URL = inlocal_local_getLogsData()
    BODY = {
        "start_time": start_time,
        "end_time": end_time,
        "mac_address": mac_address,
        "pin": pin,
        "position": position,
        "type_data": device_type
    }
    logs_datas = requests.post(url=URL, data=BODY)
    print("body:", BODY)
    print("url", URL)
    print("logs return data:", logs_datas)
    data = logs_datas.json()

    return data


def cal_logs_aggrate(start_time, end_time, dur_time, mac_address, pin, position, device_type, report_id):
    BODY = {
        "start_time": start_time,
        "end_time": end_time,
        "dur_time": dur_time,
        "mac_address": mac_address,
        "pin": pin,
        "position": position,
        "type_data": device_type,
        "report_id": report_id
    }
    URL = inserver_getLogs()
    logs_datas = requests.post(url=URL, data=BODY)
    print("body:", BODY)
    print("url", URL)
    print("logs return data:", logs_datas)
    data = logs_datas.json()

    return data


def cal_logs_aggrate_special(start_time, end_time, dur_time, mac_address, pin, position, device_type, report_id,
                             p_start, p_end):
    URL = inserver_getLogs()
    BODY = {
        "start_time": start_time,
        "end_time": end_time,
        "dur_time": dur_time,
        "mac_address": mac_address,
        "pin": pin,
        "position": position,
        "type_data": device_type,
        "report_id": report_id,
        "p_start_time": p_start,
        "p_end_time": p_end
    }
    logs_datas = requests.post(url=URL, data=BODY)
    print("body:", BODY)
    print("url", URL)
    print("logs return data:", logs_datas)
    data = logs_datas.json()

    return data


def cal_tile_degree(start_time, end_time, dur_time, mac_address, degree, report_id):
    if report_id == '1':
        URL = inlocal_Line_daily_static()
    elif report_id == '2':
        URL = inlocal_Line_cumulativeChart()

    BODY = {
        "start_time": start_time,
        "end_time": end_time,
        "dur_time": dur_time,
        "mac_addr": mac_address,
        "degree": list(degree),
    }
    logs_datas = requests.post(url=URL, json=BODY)
    print("body:", BODY)
    print("url", URL)
    print("logs return data:", logs_datas)
    data = logs_datas.json()

    return data


def cal_tile_stoppage(start_time, end_time, dur_time, mac_address):
    URL = inlocal_Line_stoppage_time()
    BODY = {
        "start_time": start_time,
        "end_time": end_time,
        "dur_time": dur_time,
        "mac_addr": mac_address,
    }
    logs_datas = requests.post(url=URL, json=BODY)
    print("body:", BODY)
    print("url", URL)
    print("logs return data:", logs_datas)
    data = logs_datas.json()

    return data


def cal_line_log(start_time, end_time, mac_address):
    URL = inlocal_Line_log_data()

    BODY = {
        "start_time": start_time,
        "end_time": end_time,
        "mac_addr": mac_address,
    }
    logs_datas = requests.post(url=URL, json=BODY)
    print("body:", BODY)
    print("url", URL)
    print("logs return data:", logs_datas)
    data = logs_datas.json()

    return data


def cal_line_error_frequency(error_id, start_time, end_time, mac_address):
    URL = inlocal_Line_error_frequency()

    BODY = {
        "error": error_id,
        "start_time": start_time,
        "end_time": end_time,
        "mac_addr": mac_address,
    }
    logs_datas = requests.post(url=URL, json=BODY)
    print("body:", BODY)
    print("url", URL)
    print("logs return data:", logs_datas)
    data = logs_datas.json()

    return data


class DeviceView(generics.ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [AllowAny, IsAuthenticated]

    def get_queryset(self):
        product_line_part = self.request.query_params.get('product_line_part')
        product_line = self.request.query_params.get('product_line')
        device_type = self.request.query_params.get('device_type')

        queryset = Device.objects.all()
        if product_line_part:
            queryset = queryset.filter(product_line_part=product_line_part)
        if product_line:
            queryset = queryset.filter(product_line_part__product_line=product_line)
        if device_type:
            queryset = queryset.filter(device_type=device_type)
        return queryset


class DetailDeviceView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [AllowAny, IsAuthenticated]
    lookup_field = 'id'


class ReportDeviceView(generics.RetrieveAPIView):  # get the data for show report
    queryset = Device.objects.all()
    permission_classes = [AllowAny, IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        try:
            # sensorInLines = Device.objects.all()
            report_id = self.request.query_params.get('report_id')
            if report_id == "1":
                response = []
                device_id = self.request.query_params.get('device_id').split(",")
                for device_e in device_id:
                    device = Device.objects.get(id=device_e)
                    if self.request.query_params.get('dur_time'):
                        print("yes")
                        live_datas = cal_logs_aggrate(self.request.query_params.get('start_time'),
                                                      self.request.query_params.get('end_time'),
                                                      self.request.query_params.get('dur_time'),
                                                      device.mac_address, device.port, device.position,
                                                      device.device_type.id, report_id)
                    else:
                        live_datas = cal_logs(self.request.query_params.get('start_time'),
                                              self.request.query_params.get('end_time'), device.mac_address, device
                                              .port, device.position, device.device_type.id)
                    # print("lives_data", live_datas)
                    sensorInLines = Device.objects.get(id=device_e)
                    # for sensor in sensorInLines:
                    sensorRes = []
                    mac = sensorInLines.mac_address
                    # print(mac)
                    pin = sensorInLines.port
                    position = sensorInLines.position
                    sensor_data = -1
                    # sensorRes.append(SensorSerializer(sensor).data)
                    sensorDataRes = []
                    for gateway_data in live_datas:
                        # print("in other for")
                        # print(live_datas)
                        if gateway_data['mac_addr'] == mac and gateway_data['pin'] == pin and gateway_data[
                            'position'] == str(position):
                            if sensor_data == "None":
                                sensor_data = -1
                            else:
                                sensor_data = gateway_data['data']

                            sensorDataRes.append({"time": gateway_data['sendDataTime'], "sensor_data": sensor_data})
                            # print("sesnsor", SensorSerializer(sensor).data)
                    sensorRes = [{"id": sensorInLines.id, "name": sensorInLines.name, "pin": sensorInLines.port,
                                  "position": sensorInLines.position, "data": sensorDataRes}]
                    # sensorRes.append(sensorDataRes)
                    response.append((sensorRes))
                return Response((response), status=status.HTTP_200_OK)
            elif report_id == "2":
                response = []
                device_id = self.request.query_params.get('device_id').split(",")
                step_pin = 11
                time_pin = 12
                device_type_id = 1
                for device_e in device_id:
                    device = Device.objects.get(id=device_e)
                    if self.request.query_params.get('dur_time'):
                        print("yes")
                        live_datas = cal_logs_aggrate(self.request.query_params.get('start_time'),
                                                      self.request.query_params.get('end_time'),
                                                      self.request.query_params.get('dur_time'),
                                                      device.mac_address, device.port, device.position,
                                                      device.device_type.id, report_id)
                    else:
                        live_datas = cal_logs(self.request.query_params.get('start_time'),
                                              self.request.query_params.get('end_time'), device.mac_address, device
                                              .port, device.position, device.device_type.id)
                    # print("lives_data", live_datas)
                    sensorInLines = Device.objects.get(id=device_e)
                    # for sensor in sensorInLines:
                    sensorRes = []
                    mac = sensorInLines.mac_address
                    # print(mac)
                    pin = sensorInLines.port
                    position = sensorInLines.position
                    sensor_data = -1
                    # sensorRes.append(SensorSerializer(sensor).data)
                    sensorDataRes = []
                    for gateway_data in live_datas:
                        # print("in other for")
                        if gateway_data['mac_addr'] == mac and gateway_data['pin'] == "1" and gateway_data[
                            'position'] == str(position):
                            if sensor_data == "None":
                                sensor_data = -1
                            else:
                                sensor_data = gateway_data['data']

                            sensorDataRes.append({"time": gateway_data['sendDataTime'], "sensor_data": sensor_data})
                            # print("sesnsor", SensorSerializer(sensor).data)
                    sensorRes = [{"id": sensorInLines.id, "name": sensorInLines.name, "pin": sensorInLines.port,
                                  "position": sensorInLines.position, "data": sensorDataRes}]
                    # sensorRes.append(sensorDataRes)
                    response.append((sensorRes))
                return Response((response), status=status.HTTP_200_OK)
            elif report_id == "3":
                response = []
                setting_time = Settings.objects.filter(factory=1).last()
                input = json.loads(setting_time.inputs)
                p_start = parse_datetime(input['peek_barq'][0])
                p_end = parse_datetime(input['peek_barq'][1])
                print(p_start, type(p_start), p_start.time())
                device_id = self.request.query_params.get('device_id').split(",")
                for device_e in device_id:
                    device = Device.objects.get(id=device_e)
                    if self.request.query_params.get('dur_time'):

                        live_datas = cal_logs_aggrate_special(self.request.query_params.get('start_time'),
                                                              self.request.query_params.get('end_time'),
                                                              self.request.query_params.get('dur_time'),
                                                              device.mac_address, device.port, device.position,
                                                              device.device_type.id, report_id, p_start, p_end)
                    else:
                        live_datas = cal_logs(self.request.query_params.get('start_time'),
                                              self.request.query_params.get('end_time'), device.mac_address, device
                                              .port, device.position, device.device_type.id)
                    # print("lives_data", live_datas)
                    sensorInLines = Device.objects.get(id=device_e)
                    sensorRes = []
                    mac = sensorInLines.mac_address
                    pin = sensorInLines.port
                    position = sensorInLines.position
                    sensor_data = -1
                    sensorDataRes = []
                    for gateway_data in live_datas:
                        if gateway_data['mac_addr'] == mac and gateway_data['pin'] == "1" and gateway_data[
                            'position'] == str(position):
                            if sensor_data == "None":
                                sensor_data = -1
                            else:
                                sensor_data = gateway_data['data']

                            sensorDataRes.append({"time": gateway_data['sendDataTime'], "sensor_data": sensor_data})
                            # print("sesnsor", SensorSerializer(sensor).data)
                    sensorRes = [{"id": sensorInLines.id, "name": sensorInLines.name, "pin": sensorInLines.port,
                                  "position": sensorInLines.position, "data": sensorDataRes}]
                    response.append((sensorRes))
                return Response((response), status=status.HTTP_200_OK)
            return Response(status=status.HTTP_200_OK)
        except Device.DoesNotExist:
            return Response({"detail": "Sensor Not found."}, status=status.HTTP_404_NOT_FOUND)
        except:
            traceback.print_exc()
            return Response({"problem"}, status=status.HTTP_404_NOT_FOUND)


class LiveDataView(generics.RetrieveAPIView):
    permission_classes = [AllowAny, IsAuthenticated]

    def get_queryset(self):
        pass

    def retrieve(self, *args, **kwargs):
        product_line = self.request.query_params.get('device_id')
        sensorInLines = Device.objects.filter(product_line_part=product_line)
        response = []
        try:
            live_datas = requests.get(inserver_live())
            live_datas = live_datas.json()
            # print(live_datas)
            for sensor in sensorInLines:
                mac = sensor.mac_address
                pin = sensor.port
                position = sensor.position
                device_type = sensor.device_type
                sensor_data = "no data"
                for gateway_data in live_datas:
                    if gateway_data['mac_addr'] == mac and gateway_data['pin'] == pin and gateway_data[
                        'position'] == str(position) and gateway_data['type_data'] == device_type.id:
                        sensor_data = gateway_data['data']
                        # print("aaaaaaaaaaaaaaa", sensor_data)
                        if sensor_data == "None":
                            sensor_data = "no data"
                sensorRes = {"live_data": sensor_data}
                # print("bbbbbbbbbbbbbbbb", sensorRes)
                sensorRes.update(DeviceSerializer(sensor).data)
                # print(DeviceSerializer(sensor).data)
                response.append((sensorRes))
            return Response((response), status=status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)


class PackageLiveView(generics.RetrieveAPIView):
    permission_classes = [AllowAny, IsAuthenticated]

    def get_queryset(self):
        pass

    @gzip_page
    def retrieve(self, request, *args, **kwargs):
        try:
            device_id = self.request.query_params.get('device_id')
            sensorInLines = Device.objects.get(id=device_id)
        except:
            return Response({'error': 'Line Not Found!'}, status=status.HTTP_404_NOT_FOUND)

        try:
            live_datas = requests.get(inserver_line_live())
            live_datas = live_datas.json()
            mac = sensorInLines.mac_address
            id = sensorInLines.id
            name = sensorInLines.name
            for gateway_data in live_datas:
                if gateway_data['mac_addr'] == mac:
                    live_data = {'device_id': id, 'line_name': name,
                                 'time': datetime.isoformat(datetime.fromtimestamp(gateway_data['datatime'] - 12600)),
                                 'degree1': gateway_data['degree1'], 'degree2': gateway_data['degree2'],
                                 'degree3': gateway_data['degree3'], 'degree4': gateway_data['degree4'],
                                 'degree5': gateway_data['degree5'], 'degree6': gateway_data['degree6'],
                                 'alarm_flag': gateway_data['alarm_flag']
                                 }
                    json_live = json.dumps(live_data)
                    json_live_loaded = json.loads(json_live)

            return Response(json_live_loaded, headers={'Content-Encoding': 'gzip'}, status=status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)


'''Tile degree json and excel file views for dailyStatic and cumulativeChart reports.'''


class PackageDegreeView(generics.RetrieveAPIView):
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        pass

    @gzip_page
    def retrieve(self, request, *args, **kwargs):
        try:
            device_id = self.request.query_params.get('device_id')
            sensorInLines = Device.objects.get(id=device_id)
        except:
            return Response({'error': 'Line Not Found!'}, status=status.HTTP_404_NOT_FOUND)

        start_time = datetime.timestamp(
            parser.parse(self.request.query_params.get('start_time')))

        end_time = datetime.timestamp(
            parser.parse(self.request.query_params.get('end_time')))

        degree = literal_eval(self.request.query_params.get('degree'))

        # try:
        data = cal_tile_degree(int(start_time), int(end_time),
                               int(self.request.query_params.get('duration')),
                               sensorInLines.mac_address,
                               degree,
                               self.request.query_params.get('report'))
        # except:
        # return Response({"detail": "Server No Respond!"}, status=status.HTTP_404_NOT_FOUND)

        report_response = []
        for log in data:
            sum = 0
            report_json = {'device_id': sensorInLines.id, 'line_name': sensorInLines.name, 'time': log['DataTime']}
            for degree_id in degree:
                report_json[f'degree{degree_id}'] = log[f'degree{degree_id}']
                # print(log[f'degree{degree_id}'])
                if log[f'degree{degree_id}']:
                    sum += log[f'degree{degree_id}']
                else:
                    pass
            report_json['Sum'] = sum
            json_live = json.dumps(report_json)
            json_live_loaded = json.loads(json_live)
            report_response.append(json_live_loaded)
        return Response(report_response, headers={'Content-Encoding': 'gzip'}, status=status.HTTP_200_OK)


class PackageDegreeGetExcelView(generics.RetrieveAPIView):
    permission_classes = [AllowAny, IsAuthenticated]

    def get_queryset(self):
        pass

    def retrieve(self, request, *args, **kwargs):
        try:
            device_id = self.request.query_params.get('device_id')
            sensorInLines = Device.objects.get(id=device_id)
        except:
            return Response({'error': 'Line Not Found!'}, status=status.HTTP_404_NOT_FOUND)

        start_time = datetime.timestamp(
            parser.parse(self.request.query_params.get('start_time')))

        end_time = datetime.timestamp(
            parser.parse(self.request.query_params.get('end_time')))

        degree = literal_eval(self.request.query_params.get('degree'))

        try:
            data = cal_tile_degree(int(start_time), int(end_time),
                                   int(self.request.query_params.get('duration')),
                                   sensorInLines.mac_address,
                                   degree,
                                   self.request.query_params.get('report'))
        except:
            return Response({"detail": "Server No Respond!"}, status=status.HTTP_404_NOT_FOUND)

        report_file_name = 'Degree' + str(self.request.query_params.get('start_time')).replace(':', '-') + '--' + str(
            self.request.query_params.get('end_time')).replace(':', '-') + '.xlsx'
        if os.path.exists(report_file_name):
            os.remove(report_file_name)

        report_response = []
        sum_dict = {'degree1': 0, 'degree2': 0, 'degree3': 0, 'degree4': 0, 'degree5': 0, 'degree6': 0, }
        for log in data:
            report_json = {'device_id': sensorInLines.id, 'line_name': sensorInLines.name, 'time': log['DataTime']}
            degree_sum = 0
            for degree_id in degree:
                report_json[f'degree{degree_id}'] = log[f'degree{degree_id}']
                sum_dict[f'degree{degree_id}'] += log[f'degree{degree_id}']
                degree_sum += log[f'degree{degree_id}']

            report_json['sum'] = degree_sum
            report_response.append(report_json)
        total = {'device_id': 'TOTAL', 'line_name': None, 'time': None, 'Sum': 0}
        for degree_id in degree:
            if sum_dict[f'degree{degree_id}']:
                total[f'degree{degree_id}'] = sum_dict[f'degree{degree_id}']
                total['Sum'] += sum_dict[f'degree{degree_id}']
        report_response.append(total)

        df = pd.DataFrame(data=report_response)
        df.to_excel(report_file_name, index=False)

        response = FileResponse(open(report_file_name, 'rb'))
        return response


'''stoppageTime json and excel file view '''


class StoppageTimeView(generics.RetrieveAPIView):
    permission_classes = [AllowAny, IsAuthenticated]

    def get_queryset(self):
        pass

    @gzip_page
    def retrieve(self, request, *args, **kwargs):
        try:
            sensorInLines = Device.objects.get(id=self.request.query_params.get('device_id'))
        except:
            return Response({'Error': 'Sensor Not Found!'}, status=status.HTTP_404_NOT_FOUND)

        start_time = datetime.timestamp(
            parser.parse(self.request.query_params.get('start_time')))

        end_time = datetime.timestamp(
            parser.parse(self.request.query_params.get('end_time')))

        # try:
        data = cal_tile_stoppage(int(start_time),
                                 int(end_time),
                                 int(self.request.query_params.get('duration')),
                                 sensorInLines.mac_address)
        # except:
        #     return Response({"detail": "Server No Respond!"}, status=status.HTTP_404_NOT_FOUND)

        report_response = []
        for report in data:
            report_json = {'device_id': sensorInLines.id,
                           'line_name': sensorInLines.name,
                           'data_time': report['DataTime'],
                           'stacker_stoppage_time': report['stoppage_time_stacker'],
                           'packaging_stoppage_time': report['stoppage_time_packaging']
                           }

            json_live = json.dumps(report_json)
            json_live_loaded = json.loads(json_live)
            report_response.append(json_live_loaded)
        return Response(report_response, headers={'Content-Encoding': 'gzip'}, status=status.HTTP_200_OK)


class StoppageTimeGetExcelView(generics.RetrieveAPIView):
    permission_classes = [AllowAny, IsAuthenticated]

    def get_queryset(self):
        pass

    def retrieve(self, request, *args, **kwargs):
        sensorInLines = Device.objects.get(id=self.request.query_params.get('device_id'))

        start_time = datetime.timestamp(
            parser.parse(self.request.query_params.get('start_time')))

        end_time = datetime.timestamp(
            parser.parse(self.request.query_params.get('end_time')))

        try:
            data = cal_tile_stoppage(int(start_time),
                                     int(end_time),
                                     int(self.request.query_params.get('duration')),
                                     sensorInLines.mac_address)
        except:
            return Response({"detail": "Server No Respond!"}, status=status.HTTP_404_NOT_FOUND)

        report_file_name = 'StoppageTime' + str(self.request.query_params.get('start_time')).replace(':',
                                                                                                     '-') + '--' + str(
            self.request.query_params.get('end_time')).replace(':', '-') + '.xlsx'
        if os.path.exists(report_file_name):
            os.remove(report_file_name)

        report_response = []
        for report in data:
            report_json = {'device_id': sensorInLines.id,
                           'line_name': sensorInLines.name,
                           'data_time': report['DataTime'],
                           'stacker_stoppage_time': report['stoppage_time_stacker'],
                           'packaging_stoppage_time': report['stoppage_time_packaging']
                           }

            report_response.append(report_json)

        df = pd.DataFrame(data=report_response)
        df.to_excel(report_file_name, index=False)

        response = FileResponse(open(report_file_name, 'rb'))
        return response


'''logData json and excel file view '''


class LogDataView(generics.RetrieveAPIView):
    permission_classes = [AllowAny, IsAuthenticated]

    def get_queryset(self):
        pass

    @gzip_page
    def retrieve(self, request, *args, **kwargs):
        try:
            sensorInLines = Device.objects.get(id=self.request.query_params.get('device_id'))
        except:
            return Response({'Error': 'Sensor Not Found!'}, status=status.HTTP_404_NOT_FOUND)
        start_time = datetime.timestamp(
            parser.parse(self.request.query_params.get('start_time')))

        end_time = datetime.timestamp(
            parser.parse(self.request.query_params.get('end_time')))

        # try:
        data = cal_line_log(int(start_time),
                            int(end_time),
                            sensorInLines.mac_address)
        # except:
        # return Response({"detail": "Server No Respond!"}, status=status.HTTP_404_NOT_FOUND)

        report_response = []
        for log in data:
            # error = ErrorLine.objects.get(code=log['code'])
            # error = ErrorDeviceSerializer(error)
            report_json = {'device_id': sensorInLines.id,
                           'line_name': sensorInLines.name,
                           'start_time': str(datetime.fromtimestamp(log['start_time'])),
                           'end_time': str(datetime.fromtimestamp(log['end_time'])),
                           'error_id': log['code'],
                           'error_section': log['section'],
                           'error_description': log['description'],
                           'stoppage_time': log['diff_time']
                           }

            json_live = json.dumps(report_json)
            json_live_loaded = json.loads(json_live)
            report_response.append(json_live_loaded)
        return Response(report_response, headers={'Content-Encoding': 'gzip'}, status=status.HTTP_200_OK)


class LogDataGetExcelView(generics.RetrieveAPIView):
    permission_classes = [AllowAny, IsAuthenticated]

    def get_queryset(self):
        pass

    def retrieve(self, request, *args, **kwargs):
        try:
            sensorInLines = Device.objects.get(id=self.request.query_params.get('device_id'))
        except:
            return Response({'Error': 'Sensor Not Found!'}, status=status.HTTP_404_NOT_FOUND)
        start_time = datetime.timestamp(
            parser.parse(self.request.query_params.get('start_time')))

        end_time = datetime.timestamp(
            parser.parse(self.request.query_params.get('end_time')))

        try:
            data = cal_line_log(int(start_time),
                                int(end_time),
                                sensorInLines.mac_address)
        except:
            return Response({"detail": "Server No Respond!"}, status=status.HTTP_404_NOT_FOUND)

        report_file_name = 'LogData' + str(self.request.query_params.get('start_time')).replace(':',
                                                                                                '-') + '--' + str(
            self.request.query_params.get('end_time')).replace(':', '-') + '.xlsx'
        if os.path.exists(report_file_name):
            os.remove(report_file_name)

        report_response = []
        for report in data:
            report_json = {'device_id': sensorInLines.id,
                           'line_name': sensorInLines.name,
                           'start_time': str(datetime.isoformat(datetime.fromtimestamp(report['start_time'])) + 'Z'),
                           'end_time': str(datetime.isoformat(datetime.fromtimestamp(report['end_time'])) + 'Z'),
                           'error_id': report['code'],
                           'error_section': report['section'],
                           'error_description': report['description'],
                           'stoppage_time': report['diff_time']
                           }

            report_response.append(report_json)

        df = pd.DataFrame(data=report_response)
        df.to_excel(report_file_name, index=False)

        response = FileResponse(open(report_file_name, 'rb'))
        return response


'''ErrorFrequency json and excel file view '''


class ErrorFrequencyView(generics.RetrieveAPIView):
    permission_classes = [AllowAny, IsAuthenticated]

    def get_queryset(self):
        pass

    @gzip_page
    def retrieve(self, request, *args, **kwargs):
        try:
            sensorInLines = Device.objects.get(id=self.request.query_params.get('device_id'))
        except:
            return Response({'Error': 'Sensor Not Found!'}, status=status.HTTP_404_NOT_FOUND)
        start_time = datetime.timestamp(
            parser.parse(self.request.query_params.get('start_time')))

        end_time = datetime.timestamp(
            parser.parse(self.request.query_params.get('end_time')))

        error = literal_eval(self.request.query_params.get('error'))
        try:
            data = cal_line_error_frequency(error,
                                            int(start_time),
                                            int(end_time),
                                            sensorInLines.mac_address)
        except:
            return Response({"detail": "Server No Respond!"}, status=status.HTTP_404_NOT_FOUND)

        report_response = []
        for report in data:
            # error = ErrorLine.objects.get(code=report['code'])
            # error = ErrorDeviceSerializer(error)
            report_json = {'device_id': sensorInLines.id,
                           'line_name': sensorInLines.name,
                           'error_id': report['code'],
                           'error_section': report['section'],
                           'error_description': report['description'],
                           'stoppage_time': report['diff_time']
                           }

            json_live = json.dumps(report_json)
            json_live_loaded = json.loads(json_live)
            report_response.append(json_live_loaded)
        return Response(report_response, headers={'Content-Encoding': 'gzip'}, status=status.HTTP_200_OK)


class ErrorFrequencyGetExcelView(generics.RetrieveAPIView):
    permission_classes = [AllowAny, IsAuthenticated]

    def get_queryset(self):
        pass

    def retrieve(self, request, *args, **kwargs):
        try:
            sensorInLines = Device.objects.get(id=self.request.query_params.get('device_id'))
        except:
            return Response({'Error': 'Sensor Not Found!'}, status=status.HTTP_404_NOT_FOUND)
        start_time = datetime.timestamp(
            parser.parse(self.request.query_params.get('start_time')))

        end_time = datetime.timestamp(
            parser.parse(self.request.query_params.get('end_time')))

        error = literal_eval(self.request.query_prams.get('error'))
        try:
            data = cal_line_error_frequency(error,
                                            int(start_time),
                                            int(end_time),
                                            sensorInLines.mac_address)
        except:
            return Response({"detail": "Server No Respond!"}, status=status.HTTP_404_NOT_FOUND)

        report_file_name = 'ErrorFrequency' + str(self.request.query_params.get('start_time')).replace(':',
                                                                                                       '-') + '--' + str(
            self.request.query_params.get('end_time')).replace(':', '-') + '.xlsx'
        if os.path.exists(report_file_name):
            os.remove(report_file_name)

        report_response = []
        for report in data:
            report_json = {'device_id': sensorInLines.id,
                           'line_name': sensorInLines.name,
                           'error_id': report['code'],
                           'error_section': report['section'],
                           'error_description': report['description'],
                           'stoppage_time': report['diff_time']
                           }

            report_response.append(report_json)

        df = pd.DataFrame(data=report_response)
        df.to_excel(report_file_name, index=False)

        response = FileResponse(open(report_file_name, 'rb'))
        return response


class AddErrorView(generics.RetrieveAPIView):
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        pass

    @gzip_page
    def retrieve(self, request, *args, **kwargs):
        try:
            URL = inserver_line_error()
            errors = requests.get(URL)
        except:
            return Response({'error': 'no respond from server.'})
        error_json = errors.json()

        response = []
        for error in error_json:
            if not ErrorLine.objects.filter(id=error['id']):
                error_create = ErrorDeviceSerializer().create(error)
        errors_all = ErrorLine.objects.all()
        errors_ser = ErrorDeviceSerializer(errors_all, many=True)
        return Response(errors_ser.data, headers={'Content-Encoding': 'gzip'}, status=status.HTTP_201_CREATED)
