# -*- coding: utf-8 -*-
import pandas as pd
from os import listdir
from os.path import isfile, join

def read_csv(csv_path, separator, header_index, util_col_indexes):
    df_tmp = pd.read_csv(csv_path, sep=separator, header=header_index,
                           index_col=False, usecols=util_col_indexes)
    return df_tmp


def extract_rows_from_df(df, start_index, number_of_rows):
    df_sliced = df._slice(slice(start_index, number_of_rows))
    return df_sliced


def get_views_from_pages_filtered(df_urls_base, df_all_urls, fields_name_for_join):
    # Search the list the urls selected (df_url_selected) in the all urls dataframe
    # and the get the number of page's visualizations
    df_result_tmp = pd.merge(df_urls_base, df_all_urls, on=fields_name_for_join, how='left')
    df_result_tmp.fillna(0, inplace=True)
    return df_result_tmp


def write_csv(df, path_name, separator, encoding):
    # Write the result as csv file
    df.to_csv(path_name, sep=separator, encoding=encoding)


def write_excel(df, path_name, encoding):
    # Write the result as excel file
    df.to_excel(path_name, encoding=encoding)

def get_pagesviews(urls_csv_file_path, ga_csv_file_path, separator, header_index,
                   urls_util_col_indexes, ga_util_col_indexes,
                   fields_name_for_join, encoding,
                   report_file_excel_path, report_file_csv_path):
    #
    df_url_selected = pd.read_csv(urls_csv_file_path, sep=separator, header=0,
                                  index_col=False, usecols=urls_util_col_indexes)
    #
    df_tmp = read_csv(ga_csv_file_path, separator, header_index, ga_util_col_indexes)
    #
    file_name = get_file_name(ga_csv_file_path)
    # Rename column 'pageviews'
    df_tmp = df_tmp.rename(index=str, columns={"Page": fields_name_for_join[0], "Pageviews": file_name})
    # Convert the pageviews column to a numeric type
    #df_tmp[file_name] = df_tmp[file_name].convert_objects(convert_numeric=True)

    df_tmp[file_name] = pd.to_numeric(df_tmp[file_name], errors='coerce')
    #
    number_of_lines = df_tmp.shape[0]
    number_of_urls = number_of_lines - header_index
    #
    df_all_urls = extract_rows_from_df(df_tmp, 0, number_of_urls)
    df_result = get_views_from_pages_filtered(df_url_selected, df_all_urls, fields_name_for_join)

    #
    write_csv(df_result, report_file_csv_path, separator, encoding)
    write_excel(df_result, report_file_excel_path, encoding)
    return df_result


def join_df(df_1, df_2, fields_name_for_join):
    df_join_tmp = pd.merge(df_1, df_2, on=fields_name_for_join, how='inner')
    return df_join_tmp


def get_file_name(url_path_name):
    """
    Get the file name without extension
    :param url_path_name: path where the csv file is located.
    For example: ganalytics-files/20160716-20160816.csv
    :return: csv file name without extension. For example: 20160716-20160816.csv
    """

    fragments = url_path_name.split("/")
    # For example name.csv
    csv_file_name_with_ext = fragments[len(fragments)-1]
    csv_file_name_list = csv_file_name_with_ext.split(".")
    csv_file_name = csv_file_name_list[0]

    return csv_file_name


def list_of_csv_files(csv_directory_path):
    csv_files_list = [f for f in listdir(csv_directory_path) if isfile(join(csv_directory_path, f))]
    return csv_files_list


_url_selected_file_path = 'urls/urls_terraview_social_policy.csv'
_final_report = 'reports/final_report.xlsx'
_fields_name_for_join = ['URL']
_separator = ','
_encoding = 'UTF-8'
_header_index = 5  # the blank line is not considered a row
_urls_util_col_indexes = [1]
_ga_util_col_indexes = [0,1]
_csv_directory_path = 'ganalytics-files'
_reports_directory_path = 'reports'


def create_final_report(csv_directory_path, reports_directory_path):
    csv_files_list = list_of_csv_files(csv_directory_path)
    df_url_selected = pd.read_csv(_url_selected_file_path, sep=_separator, header=0,
                                  index_col=False, usecols=_urls_util_col_indexes)
    _df_final_result_tmp = df_url_selected

    for csv_file_name_with_ext in csv_files_list:
        _ga_csv_file_path = csv_directory_path+'/'+csv_file_name_with_ext
        csv_file_name_without_ext = csv_file_name_with_ext.split(".")[0]
        _report_file_excel_path = reports_directory_path+'/'+'report-'+csv_file_name_without_ext+'.xlsx'
        _report_file_csv_path = reports_directory_path + '/' + 'report-' + csv_file_name_without_ext + '.csv'
        _df_result = get_pagesviews(_url_selected_file_path, _ga_csv_file_path, _separator, _header_index,
                                   _urls_util_col_indexes, _ga_util_col_indexes,
                                    _fields_name_for_join, _encoding,
                                   _report_file_excel_path, _report_file_csv_path)
        _df_final_result_tmp = join_df(_df_final_result_tmp, _df_result, _fields_name_for_join)
    write_excel(_df_final_result_tmp, _final_report, _encoding)

    print _df_final_result_tmp

create_final_report(_csv_directory_path, _reports_directory_path)
