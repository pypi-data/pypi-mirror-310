
def filtering_features_with_one_value():
    pass
    # one_value_feature_list = []
    # for i in auto_tqdm(ALL_FEAS):
    #     if len(train_df[i].unique()) == 1:
    #         if i not in one_value_feature_list:
    #             one_value_feature_list.append(i)
    # print(len(one_value_feature_list), one_value_feature_list[:10])

def filtering_features_with_small_var():
    pass
    # lvar_thres = 0.1  # 1
    # lvar_value_drop_col = []  # 低方差需要删除的列
    # _lvar_list = []  # 低方差元素列表：(列, 方差)
    # for i in auto_tqdm(ALL_FEAS):
    #     _var = train_df[i].var()
    #     if _var < lvar_thres:
    #         _lvar_list.append((i, _var))
    #         lvar_value_drop_col.append(i)
    # print(len(lvar_value_drop_col), lvar_value_drop_col[:10])

def get_dup_feas_list(df):
    train_data_drop_dup = df.T.drop_duplicates(keep='last').T
    dup_feas_list = df.columns.difference(train_data_drop_dup.columns).tolist()
    return dup_feas_list

def filtering_features_with_low_corr_to_target():
    pass
    # lcorr_thres = 0.01
    # lcorr_value_drop_col2 = []  # 低相关性需要删除的列
    # _lcorr_list2 = []  # 低相关性元素列表：(列, 相关性)
    # for i in auto_tqdm(ALL_FEAS):
    #     _corr = train_df['power'].astype(float).corr(train_df[i])
    #     if abs(_corr) < lcorr_thres:
    #         _lcorr_list2.append((i, _corr))
    #         lcorr_value_drop_col2.append(i)
    # print(len(lcorr_value_drop_col2), lcorr_value_drop_col2[:10])
