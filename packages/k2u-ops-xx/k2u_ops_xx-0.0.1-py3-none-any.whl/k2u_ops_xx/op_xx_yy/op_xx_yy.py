
def run(input_dict: dict, params: dict, iterations: dict) -> dict:
    '''
    :input_dict:
        only one dataframe as input (name = 'input')
    :params: No use here
    :iterations: No use here
    :return:
        the dataframe (name = 'output') after filling nan of input dataframe
    '''

    # 获取输入变量input
    df_in = input_dict['input']
    # 构建输出结果
    result = {"output": df_in}
    return result