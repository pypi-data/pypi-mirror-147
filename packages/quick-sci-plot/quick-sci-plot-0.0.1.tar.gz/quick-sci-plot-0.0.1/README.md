## Quick Scientific Plot
The toolkit aims to plot neat charts and figures given datasets for scientific publications.

### Examples

Example 1: Word frequency stat
```python
from quick_sci_plot import *
import pickle
# load a dictionary (term, count)
dict_tags_count=pickle.load(open("datasets/dict_tags_count.pickle","rb"))
plot_bar(dict_tags_count)
```

Example 2: Performance change
```python
from quick_sci_plot import *
metrics = ['UMass', 'C_V', 'NPMI', 'UCI']
sub_fig = ['(a)', '(b)', '(c)', '(d)']
csv_path="datasets/topic model performance.csv"
plot_reg(csv_path,sub_fig=sub_fig,metrics=metrics,x_label='Number of topics')
```


### License

The `quick-sci-plot` toolkit is provided by [Donghua Chen](https://github.com/dhchenx) with MIT License.

