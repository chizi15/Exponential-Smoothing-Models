# coding: utf-8
import pandas as pd
import numpy as np


def clean_with_bizdata(old_path, new_path, new_storage_path, filename, filetp='csv'):
    # old_path: 老数据存储路径, 末尾不带'/'，如2019年数据存储路径
    # new_path: 新数据存储路径, 末尾不带'/'，如2023年数据存储路径
    # new_storage_path: 处理后数据存储路径, 末尾不带'/'，concat后的数据存储路径
    
    # filename 适用于 ['running', 'stock', 'account', 'promotion']
    assert (filename in ['running', 'stock', 'account', 'promotion']), 'filename error'
    
    if filename == 'running':
        datecolumn = 'selldate'
    else:
        datecolumn = 'busdate'
    
    old_tmp_file = f'{old_path}/{filename}.{filetp}'
    
    new_tmp_file = f'{new_path}/{filename}.{filetp}'
    
    store_file_path = f'{new_storage_path}/{filename}.{filetp}'
    
    old_df = pd.read_csv(old_tmp_file, 
                         on_bad_lines='warn', encoding_errors='ignore', low_memory=False, 
                         dtype={'code':str},
                        )
    
    new_df = pd.read_csv(new_tmp_file, 
                         on_bad_lines='warn', encoding_errors='ignore', low_memory=False, 
                         dtype={'code':str},
                        )
    
    print('原文件记录数:', old_df.shape)
    print('新文件记录数:', new_df.shape)
    
    old_df = old_df[old_df['organ'] != '门店A'].copy()
    if filename == 'running':
        old_df = old_df[old_df['sum_disc'] != '单品销售'].copy() # 杂数据
    # 筛选老表新表数据，老表取2019年数据，新表取2023年数据，并concat生成新的组合表
    # old_df = old_df[old_df[datecolumn] <= '2019-12-31'].copy()
    # new_df = new_df[new_df[datecolumn] >= '2023-01-01'].copy()
    if filename == 'promotion':
        if len(new_df.columns) > len(old_df.columns):
            # new_df 多了class字段，可以不要，后期根据commodity自行关联
            new_df = new_df[old_df.columns].copy()

    print('按日期过滤后, 原文件记录数:', old_df.shape)
    print('按日期过滤后, 新文件记录数:', new_df.shape)
    
    new_df = pd.concat([old_df, new_df], ignore_index=True)
    
    new_df.to_csv(store_file_path, index=False, encoding='utf-8-sig')
    
    print('合并后文件记录数:', new_df.shape)
    print(f'clean {filename} ok!','\n')

    
# def clean_with_promotion(old_path, new_path, new_storage_path, filename='promotion', filetp='csv'):
#     # old_path: 老数据存储路径, 末尾不带'/'
#     # new_path: 新数据存储路径, 末尾不带'/'
#     # new_storage_path: 处理后数据存储路径, 末尾不带'/'
    
#     if filename == 'running':
#         datecolumn = 'selldate'
#     else:
#         datecolumn = 'busdate'
    
#     old_tmp_file = f'{old_path}/{filename}.{filetp}'
    
#     new_tmp_file = f'{new_path}/{filename}.{filetp}'
    
#     store_file_path = f'{new_storage_path}/{filename}.{filetp}'
    
#     old_df = pd.read_csv(old_tmp_file, 
#                          on_bad_lines='warn', encoding_errors='ignore', low_memory=False, 
#                          dtype={'code':str},
#                         )
    
#     new_df = pd.read_csv(new_tmp_file, 
#                          on_bad_lines='warn', encoding_errors='ignore', low_memory=False, 
#                          dtype={'code':str},
#                         )
    
#     print('原文件记录数:', old_df.shape)
#     print('新文件记录数:', new_df.shape)
#     # 筛选促销老表新表数据，老表取2019年数据，新表取2023年数据，并concat生成新的组合促销表
#     # old_df = old_df[old_df[datecolumn] <= '2019-12-31'].copy()
#     # new_df = new_df[new_df[datecolumn] >= '2023-01-01'].copy()
    
#     if len(new_df.columns) > len(old_df.columns):
#         # new_df 多了class字段，可以不要，后期根据commodity自行关联
#         new_df = new_df[old_df.columns].copy()
        
#     print('按日期过滤后, 原文件记录数:', old_df.shape)
#     print('按日期过滤后, 新文件记录数:', new_df.shape)
    
#     new_df = pd.concat([old_df, new_df], ignore_index=True)
    
#     new_df.to_csv(store_file_path, index=False, encoding='utf-8-sig')
    
#     print('合并后文件记录数:', new_df.shape)
#     print(f'clean {filename} ok!')


def clean_with_commodity(old_path, new_path, new_storage_path, filename='commodity', filetp='csv'):
    # 筛选commodity数据，将新老资料表合并去重后，生成更新的资料表
    # old_path: 老数据存储路径, 末尾不带'/'，例如老资料表存储路径
    # new_path: 新数据存储路径, 末尾不带'/'，例如新资料表存储路径
    # new_storage_path: 处理后数据存储路径, 末尾不带'/'，合并去重后资料表存储路径
    
    old_tmp_file = f'{old_path}/{filename}.{filetp}'
    
    new_tmp_file = f'{new_path}/{filename}.{filetp}'
    
    store_file_path = f'{new_storage_path}/{filename}.{filetp}'
    
    old_df = pd.read_csv(old_tmp_file, 
                         on_bad_lines='warn', encoding_errors='ignore', low_memory=False, 
                         dtype={'code':str, 'sm_sort':str, 'md_sort':str, 'bg_sort':str},
                        )
    
    try:
        new_df = pd.read_csv(new_tmp_file, 
                             on_bad_lines='warn', encoding_errors='ignore', low_memory=False, 
                             dtype={'code':str, 'sm_sort':str, 'md_sort':str, 'bg_sort':str},
                            )
    except:
        filetp = 'xlsx'
        new_tmp_file = f'{new_path}/{filename}.{filetp}'
        
        new_df = pd.read_excel(new_tmp_file, 
                               dtype={'coe':str, 'sml_sort':str, 'mi_sort':str, 'big_sort':str},
                              )

        new_df.rename(columns={'cls_name':'class', 'coe':'code', 'sml_sort':'sm_sort', 'smlsort_name':'sm_sort_name', 
                           'mi_sort':'md_sort', 'miort_name':'md_sort_name', 'big_sort':'bg_sort', 
                           'bigsort_name':'bg_sort_name'}, inplace=True)

        new_df['md_sort'] = new_df['sm_sort'].str[:6]

        new_df = new_df[['class', 'code', 'name', 'sm_sort', 'sm_sort_name', 'md_sort',
                         'md_sort_name', 'bg_sort', 'bg_sort_name']].copy()
    
    print('原文件记录数:', old_df.shape)
    print('新文件记录数:', new_df.shape)
    
    new_df = pd.concat([old_df, new_df], ignore_index=True)

    new_df = new_df[new_df['code']!='06970935750001'] # 非正常

    new_df.drop_duplicates(subset=['code'], keep='last', inplace=True)
    
    new_df.to_csv(store_file_path, index=False, encoding='utf-8-sig')
    
    print('合并去重后文件记录数:', new_df.shape)
    print(f'clean {filename} ok!', '\n')
    
    
def cut_desens_commodity(storage_path, desens_path, filename='commodity', filetp='csv'):
    # 资料表脱敏
    # storage_path: 拼接后数据存放路径, 末尾不带'/'
    # desens_path: 处理后存储路径, 末尾不带'/'
    
    # 脱敏规则
    # code + 10
    # sort + 10
    # 中文 转小写后 去掉 "好邻居，悦活里，悦活荟，hlj, 悦丰硕" 文字
    
    old_tmp_file = f'{storage_path}/{filename}.{filetp}'
    
    desens_file_path = f'{desens_path}/{filename}.{filetp}'

    df = pd.read_csv(old_tmp_file, 
                     on_bad_lines='warn', encoding_errors='ignore', low_memory=False, 
                     dtype={'code':str, 'sm_sort':str, 'md_sort':str, 'bg_sort':str},
                    )
    print('df shape:', df.shape)
    
    assert set(['sm_sort', 'md_sort', 'bg_sort']) < set(df.columns), 'column error'

    df['code'] = df['code'].apply(lambda x: '10'+ x)
    df['sm_sort'] = df['sm_sort'].apply(lambda x: '10' + x)
    df['bg_sort'] = df['sm_sort'].str[:6]
    df['md_sort'] = df['sm_sort'].str[:8]

    df['sm_sort_name'] = df['sm_sort_name'].fillna('')
    df['md_sort_name'] = df['md_sort_name'].fillna('')
    df['bg_sort_name'] = df['bg_sort_name'].fillna('')

    df['name'] = df['name'].apply(lambda x: x.lower())
    df['name'] = df['name'].apply(lambda x: x.replace('hlj', ''))
    df['name'] = df['name'].apply(lambda x: x.replace('好邻居', ''))
    df['name'] = df['name'].apply(lambda x: x.replace('悦活里', ''))
    df['name'] = df['name'].apply(lambda x: x.replace('悦活荟', ''))
    df['name'] = df['name'].apply(lambda x: x.replace('悦丰硕', ''))

    df['sm_sort_name'] = df['sm_sort_name'].apply(lambda x: x.replace('好邻居', ''))
    df['sm_sort_name'] = df['sm_sort_name'].apply(lambda x: x.replace('悦活里', ''))

    df['md_sort_name'] = df['md_sort_name'].apply(lambda x: x.replace('好邻居', ''))
    df['md_sort_name'] = df['md_sort_name'].apply(lambda x: x.replace('悦活里', ''))

    df['bg_sort_name'] = df['bg_sort_name'].apply(lambda x: x.replace('好邻居', ''))
    df['bg_sort_name'] = df['bg_sort_name'].apply(lambda x: x.replace('悦活里', ''))
    
    df.to_csv(desens_file_path, index=False, encoding='utf-8-sig')

    print('new df shape:', df.shape)
    print(f'desens {filename} ok', '\n')
    
    
def cut_desens_bizdata(storage_path, desens_path, filename, filetp='csv', ratio=1.05):
    # 销售表、running表脱敏
    # storage_path: 拼接后数据存放路径, 末尾不带'/'
    # desens_path: 处理后存储路径, 末尾不带'/'
    
    # 脱敏规则
    # code + 10
    # sort + 10
    # 中文 转小写后 去掉 "好邻居，悦活里，悦活荟，hlj, 悦丰硕" 文字
    # 数字字段 * ratio
    
    assert (filename in ['running', 'account', "订货数据"]), 'filename error'
    
    old_tmp_file = f'{storage_path}/{filename}.{filetp}'
    
    desens_file_path = f'{desens_path}/{filename}.{filetp}'

    if filename in ['running', 'account']:
        df = pd.read_csv(old_tmp_file, 
                        on_bad_lines='warn', encoding_errors='ignore', low_memory=False, 
                        dtype={'code':str, 'sm_sort':str, 'md_sort':str, 'bg_sort':str},
                        )
    elif filename == '订货数据':
        df = pd.read_csv(old_tmp_file,
                        on_bad_lines='warn', encoding_errors='ignore', low_memory=False,
                        dtype={'code': str},
                        names=['organ', 'class', 'code', 'name', 'busdate', 'order_pred', 'order_real', 'loss_real', 'loss_theory'], header=0
                                )
        df
    print('df shape:', df.shape)
    
    if filename == 'account':
        assert set(['amount', 'sum_cost', 'sum_price', 'sum_disc']) < set(df.columns), f'{filename} column error'
    
        df['code'] = df['code'].apply(lambda x: '10' + x)
        df['amount'] = df['amount'].apply(lambda x: round(x * ratio, 3))
        df['sum_cost'] = df['sum_cost'].apply(lambda x: round(x * ratio, 2))
        df['sum_price'] = df['sum_price'].apply(lambda x: round(x * ratio, 2))
        df['sum_disc'] = df['sum_disc'].apply(lambda x: round(x * ratio, 2))
    
    elif filename == 'running':
        assert set(['amount', 'sum_sell', 'sum_disc']) < set(df.columns), f'{filename} column error'
    
        df['code'] = df['code'].apply(lambda x: '10' + x)
        df['amount'] = df['amount'].apply(lambda x: round(x * ratio, 3))
        df['sum_sell'] = df['sum_sell'].apply(lambda x: round(x * ratio, 2))
        df['sum_disc'] = df['sum_disc'].apply(lambda x: round(x * ratio, 2))
    
    elif filename == '订货数据':
        assert set(['code', 'order_pred', 'order_real', 'loss_real', 'loss_theory']) < set(df.columns), f'{filename} column error'
    
        df['code'] = df['code'].apply(lambda x: '10' + x)
        df['order_pred'] = df['order_pred'].apply(lambda x: round(x * ratio, 3))
        df['order_real'] = df['order_real'].apply(lambda x: round(x * ratio, 3))
        df['loss_real'] = df['loss_real'].apply(lambda x: round(x * ratio, 3))
        df['loss_theory'] = df['loss_theory'].apply(lambda x: round(x * ratio, 3))
        
    df.to_csv(desens_file_path, index=False, encoding='utf-8-sig')

    print('new df shape:', df.shape)
    print(f'desens {filename} ok', '\n')


def sample_choose(filepath, output_path, filetp='csv'):
    # 筛选样本数据：传入脱敏后的数据，输出指定种类数据
    # filepath: 源数据存放路径, 末尾不带'/'
    
    # 样本类别
    sample_sort = ['12010101', '11010101', '11010201', '11010301', '11010402',
                    '11010501', '11010502', '11010503', '11010504', '11010601',
                    '11010602', '11010603', '11010801', '13010101', '13010102',
                    '13090101', '13090102', '13040102', '13040202', '13040203'
                   ]
    # 查看sample_sort是否有重复元素
    assert len(sample_sort) == len(set(sample_sort)), 'sample_sort error'

    sample_df = pd.DataFrame({'sm_sort': sample_sort})
    sample_df['sm_sort'] = sample_df['sm_sort'].apply(lambda x: '10' + x)
    
    # 商品资料表筛选
    filename = 'commodity'
    tmp_file = f'{filepath}/{filename}.{filetp}'
    sample_file_path = f'{output_path}/{filename}.{filetp}'
    
    df = pd.read_csv(tmp_file, 
                     on_bad_lines='warn', encoding_errors='ignore', low_memory=False, 
                     dtype={'code':str, 'sm_sort':str, 'md_sort':str, 'bg_sort':str},
                    )
    print(f'{filename} df shape, before merge:', df.shape)
    
    df = pd.merge(df, sample_df, on=['sm_sort'], how='inner')
    
    df.to_csv(sample_file_path, index=False, encoding='utf-8-sig')
    
    print(f'{filename} df shape, after merge:', df.shape, '\n')
    
    
    # 样本包含的单品留下来
    tmp_code = df[['code']].copy()
    

    # 销售表筛选
    filename = 'account'
    tmp_file = f'{filepath}/{filename}.{filetp}'
    sample_file_path = f'{output_path}/{filename}.{filetp}'
    
    df = pd.read_csv(tmp_file, 
                     on_bad_lines='warn', encoding_errors='ignore', low_memory=False, 
                     dtype={'code':str, 'sm_sort':str, 'md_sort':str, 'bg_sort':str},
                    )
    print(f'{filename} df shape, before screen:', df.shape)
    
    df = pd.merge(df, tmp_code, on=['code'], how='inner')
    df = df[df['organ']=='门店B'].copy()
    
    df.to_csv(sample_file_path, index=False, encoding='utf-8-sig')
    
    print(f'{filename} df shape, after screen:', df.shape, '\n')
    

    # running筛选
    filename = 'running'
    tmp_file = f'{filepath}/{filename}.{filetp}'
    sample_file_path = f'{output_path}/{filename}.{filetp}'
    
    df = pd.read_csv(tmp_file, 
                     on_bad_lines='warn', encoding_errors='ignore', low_memory=False, 
                     dtype={'code':str, 'sm_sort':str, 'md_sort':str, 'bg_sort':str},
                    )
    print(f'{filename} df shape, before screen:', df.shape)
    
    df = pd.merge(df, tmp_code, on=['code'], how='inner')
    df = df[df['organ']=='门店B'].copy()
    
    df.to_csv(sample_file_path, index=False)
    
    print(f'{filename} df shape, after screen:', df.shape, '\n')
    

    # 订货数据表样本筛选
    filename = '订货数据'
    tmp_file = f'{filepath}/{filename}.{filetp}'
    sample_file_path = f'{output_path}/{filename}.{filetp}'
    # 读取订货数据，同时重命名列名
    df = pd.read_csv(tmp_file,
                        on_bad_lines='warn', encoding_errors='ignore', low_memory=False,
                        dtype={'code': str},
                        names=['organ', 'class', 'code', 'name', 'busdate', 'order_pred', 'order_real', 'loss_real', 'loss_theory'], header=0
                        )
    print(f'{filename} df shape, before screen:', df.shape)
    # 筛选出样本数据
    df = pd.merge(df, tmp_code, on=['code'], how='inner')
    df = df[df['organ'] == '门店B'].copy()
    # 保存样本数据
    df.to_csv(sample_file_path, index=False)
    print(f'{filename} df shape, after screen:', df.shape, '\n')
    
    print('sample data ok', '\n')

    
if __name__ == '__main__':

    old_path = 'D:\Work info\WestUnion\data\origin\HLJ'
    new_path = 'D:\Work info\WestUnion\data\origin\HLJ销售数据20221101-20230420'

    order_path_old = "D:\Work info\WestUnion\data\origin\HLJ-订货数据"
    new_storage_path = 'D:\Work info\WestUnion\data\processed\HLJ\合并后数据'
    desens_path = 'D:\Work info\WestUnion\data\processed\HLJ\脱敏及筛选后样本数据'

    output_path = 'D:\Work info\WestUnion\data\processed\HLJ\脱敏及筛选后样本数据\output'

    print('******** 开始合并不同时间提取的新老表 ********')

    # 资料表合并
    clean_with_commodity(old_path, new_path, new_storage_path, filename='commodity')

    # 账表合并
    clean_with_bizdata(old_path, new_path, new_storage_path, filename='account')

    # 结存表合并
    # clean_with_bizdata(old_path, new_path, new_storage_path, filename='stock')

    # running表合并
    clean_with_bizdata(old_path, new_path, new_storage_path, filename='running')

    # 促销表合并
    # clean_with_promotion(old_path, new_path, new_storage_path, filename='promotion')
    # clean_with_bizdata(old_path, new_path, new_storage_path, filename='promotion')

    print('******** 合并数据完成 * 准备降敏 ********')

    # 资料表脱敏
    cut_desens_commodity(new_storage_path, desens_path, filename='commodity')

    # 账表脱敏
    cut_desens_bizdata(new_storage_path, desens_path, filename='account', ratio=1.05)

    # running表脱敏
    cut_desens_bizdata(new_storage_path, desens_path, filename='running', ratio=1.05)

    # 订货数据表脱敏
    cut_desens_bizdata(order_path_old, desens_path, filename='订货数据', ratio=1.05)

    print('******** 准备筛选样本数据 ********')

    # 筛选出指定种类的样本数据
    sample_choose(desens_path, output_path)

    print('******** 数据处理完成 ********')
