import logging
import json
import datetime
import socket

REMOVE_ATTR = ["filename", "module", "exc_text", "stack_info", "created", "", "relativeCreated", "exc_info", "msg"]


class HostIp(object):
    host_name = None
    host_ip = None

    @classmethod
    def get_host_ip(cls):
        if not cls.host_name or not cls.host_ip:
            try:
                cls.host_name = socket.gethostname()
                cls.host_ip = socket.gethostbyname(cls.host_name)
            except Exception as err:
                cls.host_name = "unknown hostname"
                cls.host_ip = "unknow hostip"

        return cls.host_name,cls.host_ip


class JSONFormatter(logging.Formatter):
    host_name, host_ip = HostIp.get_host_ip()

    def format(self, record):
        extra = self.build_record(record)
        self.set_format_time(extra)  # set time
        self.set_host_ip(extra)  # set host name and host ip
        extra['message'] = record.msg  # set message

        # if record.exc_info:
        #    extra['exc_info'] = self.formatException(record.exc_info)

        if self._fmt == 'pretty':
            return json.dumps(extra, indent=1, ensure_ascii=False)
        else:
            return json.dumps(extra, ensure_ascii=False)

    @classmethod
    def build_record(cls, record):
        return {
            attr_name: record.__dict__[attr_name]
            for attr_name in record.__dict__
            if attr_name not in REMOVE_ATTR
        }

    @classmethod
    def set_format_time(cls, extra):
        now = datetime.datetime.utcnow()
        format_time = now.strftime("%Y-%m-%dT%H:%M:%S" + ".%03d" % (now.microsecond / 1000) + "Z")
        extra['@timestamp'] = format_time
        return format_time

    @classmethod
    def set_host_ip(cls, extra):
        extra['host_name'] = JSONFormatter.host_name
        extra['host_ip'] = JSONFormatter.host_ip
