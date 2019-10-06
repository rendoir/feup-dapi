# Scripts

## Merge Dataset
To build a single dataset file, merging the products with the reviews use the `merge_dataset.py` script.

```bash
python3 merge_dataset.py
```

This usage will result in the following default values:
```
dataset_file=output/dataset.jl
products_file=output/products.jl
reviews_file=output/reviews.jl
```

To use different files, use the command-line arguments:  
[ (`-d` | `--dataset`)  dataset_file  ]  
[ (`-p` | `--products`) products_file ]  
[ (`-r` | `--reviews`)  reviews_file  ]  

Example:
```bash
python3 merge_dataset.py -p output/prod.jl -r output/rev.jl -d output/data.jl
```


## Statistics
To generate simple statistics and plots use the `statistics.py` script.
```bash
python3 statistics.py
```

This usage will result in the following default values:
```
dataset_file=output/dataset.jl
```

To use different files, use the command-line arguments:  
[ (`-d` | `--dataset`) dataset_file ]  

Example:
```bash
python3 statistics.py -d output/data.jl
```
