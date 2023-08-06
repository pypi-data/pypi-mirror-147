from ..op_xx_yy import op_xx_yy

"""
    参考样例
"""
def test_run():

    import pandas as pd
    df = pd.DataFrame(
        {

            "k_ts":['2022-04-20 12:12:12', '2022-04-20 12:12:13', '2022-04-20 12:12:14'],
            "Name": [
                "Braund, Mr. Owen Harris",
                "Allen, Mr. William Henry",
                "Bonnell, Miss. Elizabeth",
            ],
        }
    )
    print(df)

    input_dict = {'input': df}
    op_xx_yy(input_dict=input_dict, params={}, iterations={})

if __name__ == '__main__':
    test_run()
