Clearmob : Practice assignment

This script scrapes all articles from techcruch[dot]com, read each article and determine which company (if any) is the primary subject matter of the article.

To run the above tool, create a virtual env. I'm using Anaconda(py 2.7).

First, to install all dependencies:

```
conda env create -f requirements.yml
```

Then activate the environment with `source activate clearmob`. After which you can run `python run_spider.py`. I'm using scrapy which asyncronously scrapes, processes and writes to a file. This will create an output file, just like `output.csv` in the directory. 
