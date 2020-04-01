#!/usr/bin/env python
# encoding: utf-8
"""
@version: 0.1
@author: zhangwb
导出字段排序
"""
from scrapy.conf import settings
from scrapy.exporters import CsvItemExporter


class AmacItemExporter(CsvItemExporter):

    def __init__(self, *args, **kwargs):
        delimiter = settings.get('CSV_DELIMITER', ',')
        kwargs['delimiter'] = delimiter

        fields_to_export = settings.get('FIELDS_TO_EXPORT', [])
        if fields_to_export:
            kwargs['fields_to_export'] = fields_to_export

        super(AmacItemExporter, self).__init__(*args, **kwargs)
