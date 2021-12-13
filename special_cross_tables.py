import pandas as pd;

def part_conf_table(table):
    # pandas умеет строить таблички сопряженности только в абсолютных величинах
    # эта функция позволит сделать в относительных
    s = table.sum(axis = 1)
    return table.apply(lambda col: col / s)


def get_conv_table(data_frame, predictor_name, predicate_name):
    # для скоринга позволяет сделать табличку, где по столбцам 'Абс не дефолт', 'Абс дефолт', 'Доля не дефолт%', 'Доля дефолт%'
    # а по строкам возможные значения переменной по которой ислледуюится взаимосвязи

    cross_tab = pd.crosstab( data_frame[predictor_name], data_frame[predicate_name],)
    part_tab = part_conf_table(cross_tab)


    part_tab = part_tab*100;


    cross_tab.columns = ['Абс не дефолт', 'Абс дефолт']
    part_tab.columns = ['Доля не дефолт%', 'Доля дефолт%']
    result_table  = pd.concat([cross_tab, part_tab], axis= 1)

    return result_table

def get_conv_table_by_columns(predictor_col, predicate_col):
    # налогично функции выше но использует только входящие столбцы

    cross_tab = pd.crosstab( predictor_col, predicate_col)
    part_tab = part_conf_table(cross_tab)


    part_tab[0] = part_tab[0]*100;
    part_tab[1] = part_tab[1]*100;

    cross_tab.columns = ['Абс не дефолт', 'Абс дефолт']
    part_tab.columns = ['Доля не дефолт%', 'Доля дефолт%']
    result_table  = pd.concat([cross_tab, part_tab], axis= 1)

    return result_table


def relative_cross_tab_by_rows(rows_data, columns_data):
    '''Простая функция для того чтобы раядом показать таблицу 
    сопраженности в абсолуюных и относительных числах. Доли беруться по строкам.'''
    ct = pd.crosstab( rows_data, columns_data);
    sum_by_rows = ct.sum(axis = 1)
    rel_cross_tab = ct.apply(lambda x: x/sum_by_rows, axis = 0)
    rel_cross_tab.columns = [str(i) + '%' for i in rel_cross_tab.columns]

    return pd.concat([ct, rel_cross_tab], axis = 1)