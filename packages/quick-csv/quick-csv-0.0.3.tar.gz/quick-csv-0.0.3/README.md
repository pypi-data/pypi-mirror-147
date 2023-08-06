## Quick CSV

Read and write CSV or TXT files in a simple manner

### Installation
```pip
pip install quick-csv
```

### Usage
Example 1: read and write csv or txt files
```python
from quickcsv.file import *
# read a csv file
list_model=read_csv('data/test.csv')
for idx,model in enumerate(list_model):
    print(model)
    list_model[idx]['id']=idx
# save a csv file
write_csv('data/test1.csv',list_model)

# write a text file
write_text('data/text1.txt',"Hello World!")
# read a text file
print(read_text('data/text1.txt'))
```
Example 2: create dataframe from a list of models
```python
from quickcsv.file import *
# read a csv file
list_model=read_csv('data/test.csv')
# create a dataframe from list_model
df=create_df(list_model)
# print
print(df)
```

### License

The `quick-csv` project is provided by [Donghua Chen](https://github.com/dhchenx). 

