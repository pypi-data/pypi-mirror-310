from typing import List

class DeviceMeasurementGroup:
    def __init__(self, device_code, device_name, measurement_group_code, measurement_group_name, device_type_code, schema):
        self.device_code = device_code
        self.device_name = device_name
        self.measurement_group_code = measurement_group_code
        self.measurement_group_name = measurement_group_name
        self.device_type_code = device_type_code
        self.schema = schema

    def __repr__(self):
        return f"DeviceMeasurementGroup(device_code={self.device_code}, device_type_code={self.device_type_code}, measurement_group_code={self.measurement_group_code}, schema={self.schema})"

class InstanceMeasurement:
    def __init__(self, device_code, device_type_code, schema, schema_column, schema_column_name, repo_code, repo_name, 
                 repo_column, unit, lower_bound, upper_bound, type, measurement_group_code, measurement_group_name, measurement, measurement_name):
        self.device_code = device_code
        self.device_type_code = device_type_code
        self.schema = schema
        self.schema_column = schema_column
        self.schema_column_name = schema_column_name
        self.schema = schema
        self.repo_code = repo_code
        self.repo_name = repo_name
        self.repo_column = repo_column
        self.unit = unit
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.type = type
        self.measurement = measurement
        self.measurement_group_code = measurement_group_code
        self.measurement_group_name = measurement_group_name
        self.measurement_name = measurement_name
    def __repr__(self):
        return f"InstanceMeasurement(device_code={self.device_code}, measurement={self.measurement}, repo_code={self.repo_code}, repo_column={self.repo_column})"
    
class AlarmInstancePointsConfig:
    def __init__(self, device_code, device_type, events, related):
        self.device_code = device_code
        self.device_type = device_type
        self.events = events
        self.related = related

    def __repr__(self):
        return f"AlarmInstancePointsConfig(device_code={self.device_code}, events={self.events}, related={self.related})"

class AlarmInstancePointsStatistics:
    def __init__(self, device_code, alarm_code, measurements:List[str]):
        self.device_code = device_code
        self.alarm_code = alarm_code
        self.measurements = measurements

    def __repr__(self):
        return f"AlarmInstancePointsStatistics(device_code={self.device_code}, alarm_code={self.alarm_code}, measurements={self.measurements})"
    
