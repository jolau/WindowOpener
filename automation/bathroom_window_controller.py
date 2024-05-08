import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

HUMIDITY_LOWER_THRESHOLD_OFFSET = 6
HUMIDITY_UPPER_THRESHOLD_OFFSET = 9
#HUMIDITY_LOWER_THRESHOLD = 63
#HUMIDITY_UPPER_THRESHOLD = 70
HUMIDITY_HIGH_HOLD_SECONDS = 0
HUMIDITY_LOW_HOLD_SECONDS = 5*60
MANUALLY_OPEN_SECONDS = 15*60
MANUALLY_CLOSED_SECONDS = 10*60

from enum import Enum
class OperationMode:
    MANUAL = 1
    AUTO = 2
    AUTO_SUSPENDED = 3


operation_mode = OperationMode.AUTO
auto_mode_open_window = False


@time_trigger
def on_startup():
    input_boolean.bathroom_window_opener_automatically = 'on'


def actuate_window(open_window):
    if open_window:
        cover.bathroom_window_opener.open_cover()
    else:
        cover.bathroom_window_opener.close_cover()


@state_trigger("float(sensor.bathroom_air_sensor_humidity) > (float(sensor.avg_humidity) + HUMIDITY_UPPER_THRESHOLD_OFFSET)", state_hold=HUMIDITY_HIGH_HOLD_SECONDS)
def humidity_high_trigger(value=None, old_value=None):
    global operation_mode
    global auto_mode_open_window

#    humidity = float(value)
    log.debug(f"humidity high: {value}")
    
    auto_mode_open_window = True
    if operation_mode == OperationMode.AUTO:
        actuate_window(auto_mode_open_window)
        
        
@state_trigger("float(sensor.bathroom_air_sensor_humidity) < (float(sensor.avg_humidity) + HUMIDITY_LOWER_THRESHOLD_OFFSET)", state_hold=HUMIDITY_LOW_HOLD_SECONDS)
def humidity_low_trigger(value=None, old_value=None):
    global operation_mode
    global auto_mode_open_window

#    humidity = float(value)
    log.debug(f"humidity low: {value}")
    
    auto_mode_open_window = False
    if operation_mode == OperationMode.AUTO:
        actuate_window(auto_mode_open_window)


@service("bathroom_window_controller.open_window_manually")
def open_window_manually():
    global operation_mode
    global auto_mode_open_window

    task.unique("window_manually")

    log.info("Open Window Manually")
    if operation_mode == OperationMode.MANUAL:
        actuate_window(True)
    else:
        operation_mode = OperationMode.AUTO_SUSPENDED
        actuate_window(True)
        task.sleep(MANUALLY_OPEN_SECONDS)
        operation_mode = OperationMode.AUTO
        actuate_window(auto_mode_open_window)
    
    
@service("bathroom_window_controller.close_window_manually")
def close_window_manually():
    global operation_mode
    global auto_mode_open_window

    task.unique("window_manually")

    log.info("Close Window Manually")
    if operation_mode == OperationMode.MANUAL:
        actuate_window(False)
    else:
        operation_mode = OperationMode.AUTO_SUSPENDED
        actuate_window(False)
        task.sleep(MANUALLY_CLOSED_SECONDS)
        operation_mode = OperationMode.AUTO
        actuate_window(auto_mode_open_window)
    
    
#@service("bathroom_window_controller.disable_auto_mode")
@state_trigger("input_boolean.bathroom_window_opener_automatically == 'off'")
def disable_auto_mode():
    global operation_mode
    global auto_mode_open_window

    task.unique("window_manually")

    log.info("Disable auto mode")
    operation_mode = OperationMode.MANUAL
    
    
#@service("bathroom_window_controller.enable_auto_mode")
@state_trigger("input_boolean.bathroom_window_opener_automatically == 'on'")
def enable_auto_mode():
    global operation_mode
    global auto_mode_open_window

    task.unique("window_manually")

    log.info("Enable auto mode")
    operation_mode = OperationMode.AUTO
    actuate_window(auto_mode_open_window)

