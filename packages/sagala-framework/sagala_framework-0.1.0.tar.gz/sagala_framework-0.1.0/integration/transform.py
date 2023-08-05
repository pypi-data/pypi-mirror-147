

def convert():
    # get tipe data dari metadata
    pass


def filter():
    # get filter data dari metadata
    pass


# --------------OTHER-----------------
def convert_float(df):
    for i, j in zip(df.columns, df.dtypes):
        if 'float' in str(j):
            df[i] = df[i].apply(lambda x: '{:.0f}'.format(x)).str.replace("nan", '')
    return df
