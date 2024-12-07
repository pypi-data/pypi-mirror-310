# -*- coding: utf-8 -*-

import json
import os

from collections import OrderedDict

# 3-rd party modules

from icecream import ic
import numpy as np
import pandas as pd

# local

from . config import setup_config
from . constants import (
    FILE_FIELD,
    INPUT_FIELD,
    STAGING_FIELD,
)
from . functions.assign_id import (
    assign_id,
    create_id_context_map,
    setup_assign_ids,
)
from . functions.get_field_value import get_field_value
from . functions.set_field_value import set_field_value

dict_loaders: dict[str, callable] = {}
def register_loader(
    ext: str,
):
    def decorator(loader):
        dict_loaders[ext] = loader
        return loader
    return decorator

dict_savers: dict[str, callable] = {}
def register_saver(
    ext: str,
):
    def decorator(saver):
        dict_savers[ext] = saver
        return saver
    return decorator

@register_loader('.xlsx')
def load_excel(
    input_file: str,
):
    df = pd.read_excel(input_file)
    return df

@register_loader('.json')
def load_json(
    input_file: str,
):
    with open(input_file, 'r') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    return df

@register_saver('.json')
def save_json(
    df: pd.DataFrame,
    output_file: str,
):
    # NOTE: この方法だとスラッシュがすべてエスケープされてしまった
    #df.to_json(
    #    output_file,
    #    orient='records',
    #    force_ascii=False,
    #    indent=2,
    #    escape_forward_slashes=False,
    #)
    #ic(df.iloc[0])
    data = df.to_dict(orient='records')
    with open(output_file, 'w') as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False,
        )

@register_saver('.jsonl')
def save_jsonl(
    df: pd.DataFrame,
    output_file: str,
):
    # NOTE: この方法だとスラッシュがすべてエスケープされてしまった
    #df.to_json(
    #    output_file,
    #    orient='records',
    #    lines=True,
    #    force_ascii=False,
    #)
    with open(output_file, 'w') as f:
        for index, row in df.iterrows():
            data = row.to_dict()
            json.dump(
                data,
                f,
                ensure_ascii=False,
            )
            f.write('\n')

def search_column_value(
    row: OrderedDict,
    column: str,
):
    if STAGING_FIELD in row:
        value, found = get_field_value(row[STAGING_FIELD], column)
        if found:
            return value, True
    value, found = get_field_value(row[STAGING_FIELD], column)
    original, found = get_field_value(row, f'{STAGING_FIELD}.{INPUT_FIELD}')
    if found:
        value, found = get_field_value(original, column)
        if found:
            return value, True
    value, found = get_field_value(row, column)
    if found:
        set_field_value(row, column, value)
        return value, True
    return None, False

def map_constants(
    row: OrderedDict,
    dict_constants: OrderedDict,
):
    new_row = OrderedDict(row)
    for column in dict_constants.keys():
        #set_field_value(new_row, column, dict_constants[column])
        set_field_value(new_row, f'{STAGING_FIELD}.{column}', dict_constants[column])
    return new_row

def map_formats(
    row: OrderedDict,
    dict_formats: OrderedDict,
):
    new_row = OrderedDict(row)
    for column in dict_formats.keys():
        template = dict_formats[column]
        params = {}
        params.update(row[STAGING_FIELD])
        params.update(row)
        formatted = None
        while formatted is None:
            try:
                formatted = template.format(**params)
            except KeyError as e:
                #ic(e)
                #ic(e.args)
                #ic(e.args[0])
                key = e.args[0]
                params[key] = f'__{key}__undefined__'
            except:
                raise
        set_field_value(new_row, f'{STAGING_FIELD}.{column}', formatted)
    return new_row

def remap_columns(
    row: OrderedDict,
    dict_remap: OrderedDict,
):
    new_row = OrderedDict()
    for column in dict_remap.keys():
        value, found = search_column_value(row, dict_remap[column])
        if found:
            set_field_value(new_row, column, value)
    for column in row.keys():
        if column == STAGING_FIELD:
            # NOTE: Ignore debug fields
            set_field_value(new_row, column, row[column])
    return new_row

def apply_fields_split_by_newline(
    row: OrderedDict,
    dict_fields: OrderedDict,
):
    new_row = OrderedDict(row)
    for column in dict_fields:
        value, found = search_column_value(row, dict_fields[column])
        #ic(value, found)
        if found:
            if isinstance(value, str):
                new_value = value.split('\n')
                set_field_value(new_row, f'{STAGING_FIELD}.{column}', new_value)
            else:
                set_field_value(new_row, f'{STAGING_FIELD}.{column}', value)
    return new_row

def convert(
    input_files: list[str],
    output_file: str | None = None,
    config_path: str | None = None,
    assign_constants: str | None = None,
    assign_formats: str | None = None,
    pickup_columns: str | None = None,
    fields_to_split_by_newline: str | None = None,
    fields_to_assign_ids: str | None = None,
    output_debug: bool = False,
):
    ic.enable()
    ic()
    ic(input_files)
    df_list = []
    id_context_map = create_id_context_map()
    config = setup_config(config_path)
    ic(config)
    if assign_constants:
        fields = assign_constants.split(',')
        for field in fields:
            if '=' in field:
                dst, src = field.split('=')
                config.process.assign_constants[dst] = src
            else:
                raise ValueError(f'Invalid constant assignment: {field}')
    if assign_formats:
        fields = assign_formats.split(',')
        for field in fields:
            if '=' in field:
                dst, src = field.split('=')
                config.process.assign_formats[dst] = src
            else:
                raise ValueError(f'Invalid template assignment: {field}')
    if pickup_columns:
        fields = pickup_columns.split(',')
        for field in fields:
            if '=' in field:
                dst, value = field.split('=')
                config.map[dst] = value
            else:
                config.map[field] = field
    if fields_to_split_by_newline:
        fields = fields_to_split_by_newline.split(',')
        for field in fields:
            if '=' in field:
                dst, src = field.split('=')
                config.process.split_by_newline[dst] = src
            else:
                raise ValueError(f'Invalid split by newline: {field}')
    if fields_to_assign_ids:
        setup_assign_ids(config, fields_to_assign_ids)
    if output_file:
        ext = os.path.splitext(output_file)[1]
        if ext not in dict_savers:
            raise ValueError(f'Unsupported file type: {ext}')
        saver = dict_savers[ext]
    ic(config)
    #return # debug return
    for input_file in input_files:
        ic(input_file)
        if not os.path.exists(input_file):
            raise FileNotFoundError(f'File not found: {input_file}')
        ext = os.path.splitext(input_file)[1]
        ic(ext)
        if ext not in dict_loaders:
            raise ValueError(f'Unsupported file type: {ext}')
        df = dict_loaders[ext](input_file)
        # NOTE: NaN を None に変換しておかないと厄介
        df = df.replace([np.nan], [None])
        #ic(df)
        ic(len(df))
        ic(df.columns)
        ic(df.iloc[0])
        new_rows = []
        for index, row in df.iterrows():
            orig = OrderedDict(row)
            new_row = OrderedDict(row)
            if STAGING_FIELD not in new_row:
                set_field_value(new_row, f'{STAGING_FIELD}.{INPUT_FIELD}', orig)
                set_field_value(new_row, f'{STAGING_FIELD}.{FILE_FIELD}', input_file)
            if config.process.assign_constants:
                new_row = map_constants(new_row, config.process.assign_constants)
            if config.map:
                new_row = remap_columns(new_row, config.map)
            if config.process.split_by_newline:
                new_row = apply_fields_split_by_newline(new_row, config.process.split_by_newline)
            if config.process.assign_ids:
                new_row = assign_id(new_row, config.process.assign_ids, id_context_map)
            if config.process.assign_formats:
                new_row = map_formats(new_row, config.process.assign_formats)
            if config.map:
                new_row = remap_columns(new_row, config.map)
            if not output_debug:
                new_row.pop(STAGING_FIELD, None)
            new_rows.append(new_row)
        new_df = pd.DataFrame(new_rows)
        df_list.append(new_df)
    all_df = pd.concat(df_list)
    #ic(all_df)
    ic(len(all_df))
    ic(all_df.columns)
    ic(all_df.iloc[0])
    if output_file:
        ic('Saing to: ', output_file)
        saver(all_df, output_file)
