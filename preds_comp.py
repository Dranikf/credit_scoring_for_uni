import pandas as pd;
from preds_combinat_AUC_Logit import preds_combinat_AUC_Logit;

test_data = pd.read_csv('test_data.csv', index_col=0)
train_data = pd.read_csv('train_data.csv', index_col =0)


res_df = preds_combinat_AUC_Logit(train_data.loc[:, train_data.columns != 'default_60+'], train_data.loc[:, train_data.columns == 'default_60+'],
test_data.loc[:, test_data.columns != 'default_60+'], test_data.loc[:, test_data.columns == 'default_60+'], disp = True)

res_df.to_excel('preds_combinations.xlsx')