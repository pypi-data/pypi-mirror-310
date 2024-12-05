
__version__='0.0.16'

import pkg_resources
import pandas as pd

# pkg_resources로 설치된 패키지 안의 절대 경로 가져오기
csv_path = pkg_resources.resource_filename('Metamorphic', 'data/표준정규분포표.csv')

# CSV 파일 읽기
df = pd.read_csv(csv_path)
print(df)

