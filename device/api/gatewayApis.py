def inlocal_server_live():
    return 'http://178.22.124.147:9017/gateway/livedata/'


def inlocal_local_live():
    return 'http://localhost:8080/gateway/livedata/'


def inserver_live():
    return 'http://localhost:7000/gatewaya/gateway/livedata/'


def inlocal_server_getLogs():
    return 'http://localhost:7000/gatewaya/gateway/api/getLogs/inPeriod/'


def inlocal_local_getLogs():
    return 'http://localhost:8080/gateway/api/getLogs/inPeriod/'


def inserver_getLogs():
    return 'http://localhost:7000/gatewaya/gateway/api/getLogs/inPeriod/'


def inlocal_local_getLogsData():
    return 'http://localhost:7000/gatewaya/gateway/api/getLogs/inPeriod/data/'


def inlocal_Line_daily_static():
    return 'http://localhost:7000/gatewaya/packaging/dailyStatic/'


def inlocal_Line_stoppage_time():
    return 'http://localhost:7000/gatewaya/packaging/stoppageTime/'


def inlocal_Line_log_data():
    return 'http://localhost:7000/gatewaya/packaging/logData/'


def inlocal_Line_error_frequency():
    return 'http://localhost:7000/gatewaya/packaging/errorFrequency/'


def inlocal_Line_cumulativeChart():
    return 'http://localhost:7000/gatewaya/packaging/cumulativeChart/'


# def inserver_getLogs():
    # return 'http://localhost:7000/gatewaya/gateway/api/getLogs/inPeriod/'
    
def inserver_line_live():
    return 'http://localhost:7000/gatewaya/packaging/liveData/'

def inserver_line_error():
    return 'http://localhost:7000/gatewaya/packaging/errorList/'


def get_charge_for_balmil_as_date_status():
    return 'http://localhost:7000/gatewaya/gateway/api/getLogs/chargecounts/get_charges/'
