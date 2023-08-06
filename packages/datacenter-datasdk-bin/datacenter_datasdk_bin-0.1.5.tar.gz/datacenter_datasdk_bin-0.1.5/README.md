# datacenter_datasdk_bin

### INSTALL

```
pip install datacenter-datasdk-bin
```


### USAGE

```
from datacenter_datasdk_bin import get_price, auth

auth('xxx', 0, 'xxx','xxx')
data = get_price('600033.XSHG', 'cn', 'm1', start_date='2010-01-01', end_date='2021-01-01')
```

### API

#### *get_price()*
get kline data, include daily, minute and tick

**params**

code: str or list, single code or multi code as list

region: str, 'cn' or 'us'

frequency: str, represent frequency of kline, 'd1', 'm1', 'm5', 'm15', 'm30', 'm60', 'tick'(only in cn), 'd1_post'(only in cn), 'd1_raw'(only in cn)

start_date: datetime.datetime or datetime.date or str, start time of data, default '2005-01-01'

end_date: datetime.datetime or datetime.date or str, end time of data, default 0 o'clock of today

columns: list, set the data columns of return, default None

limit: int, set the rows of return from start_date, default None

connect: taos connect object, default the connect object after 'auth()'

**return**

dataframe


#### *auth()*
authorization of api, and get the taos connect object

**params**

host: str

port: int

user: str

password: str

**return**

taos connect object