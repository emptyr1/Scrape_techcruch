Clearmob:

This script scrapes all articles from techcruch[dot]com, read each article and determine which company (if any) is the primary subject matter of the article.

To run the above tool, create a virtual env. I'm using Anaconda(py 2.7).

First, to install all dependencies:

```
conda env create -f requirements.yml
```

Then activate the environment with `source activate clearmob`. After which you can run `python run_spider.py`. I'm using scrapy which asyncronously scrapes, processes and writes to a file. This will create an output file, just like `output.csv` in the directory. 

The 2 main files are [pipeline.py](https://github.com/modqhx/Scrape_techcruch/blob/master/clearmobtest/pipelines.py) and [quotes_spider.py](https://github.com/modqhx/Scrape_techcruch/blob/master/clearmobtest/spiders/quotes_spider.py) file which uses NLTK python package to do POS tagging and find entities within a corpus of text. This entities can represent names/organizations, hence includes both. For sake of time, multiple 'strong' names were included in those fields. 
