import scipy.stats as stats
import pandas as pd


def get_Chi_sq_for_cross_tab(tab,  alpha = 0.05):

    # находим сколько уровней для каждой переменной имеется
    rows = tab.shape[0]
    columns = tab.shape[1]

    # чило хороших/плохих клиентов
    total_good_clients = tab.iloc[0,:].sum()
    total_bad_clients = tab.iloc[1,:].sum()
    total_clients = tab.sum().sum()

    # доля плохих/хороших клиентов
    p_good = total_good_clients/total_clients
    p_bad = total_bad_clients/total_clients


    # вычисление теоритических объемов выборок
    def get_theory(x):
        return([x.sum()*p_good, x.sum()*p_bad])

    theory_counts = tab.apply(get_theory)
    stat_value = (((theory_counts - tab)**2)/theory_counts).sum().sum()

    degrees_of_freedom = (rows-1)*(columns-1)


    p_value = 1 - stats.chi2.cdf(stat_value, degrees_of_freedom)

    return stat_value, p_value , stats.chi2.ppf(1 - alpha, degrees_of_freedom)


def simple_chi_sq_test(test_column, pred_column, cond_values = [], levels_print = True):

    # быстро получить результаты критерия прирсона на равенсво долей двух групп
    # test_column - столбец в котором содержаться уровни
    # cond_values - те имена по которым проводить тест или [] для того чтобы взять все

    my_test_column = test_column
    my_pred_column = pred_column

    if (cond_values != []):
        my_test_column = test_column[test_column.isin(cond_values)]
        my_pred_column = pred_column[test_column.isin(cond_values)]
   

    cross_tab2 = pd.crosstab(my_pred_column, my_test_column)

    stat_value, p_value, crit_val = get_Chi_sq_for_cross_tab(cross_tab2)

    conclusion = "Нельзя отклонить нулевую гипотезу. (о равенстве долей в группах)"
    if p_value <= 0.05:
        conclusion = "Нулевую гипотезу следует отклонить. (о равенстве долей в группах)"

    print(conclusion)

    if levels_print:
        print('сравниваемые уровни ' + str(cond_values))
        
    print("p значение: " + str(p_value))
    print("значение статистики: " + str(stat_value))
    print("критический уровень: " + str(crit_val))
    return(cross_tab2)