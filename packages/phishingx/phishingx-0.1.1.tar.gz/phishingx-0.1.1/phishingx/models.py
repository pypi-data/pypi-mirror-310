import pandas as pd

def preprocess_data(df):
    # 불필요한 열 제거
    columns_to_drop = ['URL', 'IP Address', 'Country', 'User Country', 'Countries Match', 'Creation Date', 'Expiration Date', 'Registrant Name', 'Final URL', 'redirection_count', 'external_domain_requests', 'malicious_file_downloads']
    df = df.drop(columns=columns_to_drop, errors='ignore')

    # 문자열 데이터를 숫자로 변환 (예: 'Yes' -> 1, 'No' -> 0)
    # df['Countries Match'] = df['Countries Match'].replace({'Yes': 1, 'No': 0})

    # 불리언 값을 1과 0으로 변환
    bool_columns = ['Is Obfuscated', 'Window Location Redirect', 'SSL Used', 'Cookie Access', 'iframe_present', 'favicon', 'x frame option', 'spf', 'txt', 'lang']
    df[bool_columns] = df[bool_columns].replace({True: 1, False: 0})

    # 특정 열의 NaN 처리
    nan_columns = ['Hidden Iframe Count', 'Content Size (bytes)', 'Domain Age (days)']
    df[nan_columns] = df[nan_columns].apply(pd.to_numeric, errors='coerce')

    return df
