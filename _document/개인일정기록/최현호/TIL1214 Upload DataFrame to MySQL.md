# TIL1214

## (1) Upload DataFrame to MySQL

> Pandas DataFrame을 MySQL에 저장하기 위해 먼저 `Connector`가 필요하다. 파이썬3에서는 `MySQLdb`를 지원하지 않기 때문에, `pymysql`로 불러와야한다. 꼭 pymysql이 아니어도 상관없지만, 사용해보면 `mysql-connector`보다 빠르다는 것을 체감할 수 있다.

```bash
# putty 가상환경에 패키지 설치하기
# conda activate awsvenv

pip install pymysql
pip install sqlalchemy # sqlalchemy를 통해 DB에 연결 가능
```

```python
# MySQL에 저장
import pandas as pd
from sqlalchemy import create_engine

# Credentials to database connection
hostname = "kf99database.cu3wxbwt4src.ap-northeast-2.rds.amazonaws.com"
dbname = "kf99"
user = "admin"
pwd = "qjtwlaktmzm"

# Create dataframe
corona_status_df = corona_df.loc[:, ['statedt', 'decidecnt', 'decidecnt_day']]

# Create SQLAlchemy engine to connect to MySQL Database
engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}".format(host=hostname, db=dbname, user=user, pw=pwd))

# Convert dataframe to sql table                                   
corona_status_df.to_sql(name='tablename', con=engine, index=False) # 새로 'table' 테이블을 만들어서 알아서 DataFrame을 DB에 적재(이미 있으면 불가 --> if_exists='append')
```

