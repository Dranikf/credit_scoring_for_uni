from itertools import combinations;
import pandas as pd;
from statsmodels.tools.tools import add_constant;
from statsmodels.api import Logit;
from sklearn import metrics;
import numpy as np;


def preds_combinat_AUC_Logit(train_X, train_Y, test_X, test_Y, disp = False):
    ''' функция для логистической регрессии выберет наилучшие комбинации предикторов в смысле высочайшего AUC'''
    # входные данные:
    # train_X - pandas.DataFrame содержащий исследуемые предикторы
    # train_Y - предсказываемый параметр для обучения
    # test_X - pandas.DataFrame кусок данных используемый для валидации
    # train_Y - предсказваемый параметр для валидации
    # disp - показывать ли информацию о текущей итерации

    # на выходе - pandas.DataFrame в которой содержиться информация о переранных комбинациях и соотвествующих AUC

    test_cols = train_X.columns.to_list()
    combinations_result = pd.DataFrame(columns=test_cols + ['AUC'])

    for i in range(1,len(test_cols) + 1):
        for comb in combinations(test_cols, i):
            X_preds = list(comb)

            if disp:
                print('обрабатываемая комбинация')
                print(X_preds)

            # получаем какие из колонок обрабатывались на этой итерации в виде
            # листа из boolean
            new_line = pd.Series(test_cols).isin(X_preds).to_list()
            # преобразуем в словарь, который просто проще использовать
            new_line  = {test_cols[i]: new_line[i] for i in range(len(test_cols))}

            
            # создаем модель при этой комбинации предикторов
            try:
                model = Logit(train_Y, train_X.loc[:,X_preds]).fit(disp = 0)
                pred_probs = model.predict(test_X.loc[:, X_preds])
                new_line['AUC'] = metrics.roc_auc_score( test_Y,pred_probs)
            except:
                new_line['AUC'] = np.NaN
            
            combinations_result = combinations_result.append(new_line, ignore_index=True)
    
    return combinations_result;