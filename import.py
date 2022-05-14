#import pandas as pd
import json
import numpy as np
from tqdm import tqdm_notebook as tqdm
import uuid
import weaviate 
from weaviate.batch import Batch 
import helper
import weaviate

# initiate the Weaviate client
client = weaviate.Client("http://localhost:8081")
client.timeout_config = (3, 200)


# load all metadata
productData = []
with open('data/sample_meta_Home_and_Kitchen.json', 'r') as f:
    for l in tqdm(f):
        productData.append(json.loads(l))


client.schema.delete_all() # delete all classes

# skipped product "brand", it can be it's own class, for simplicity, skip it for now 
# skipped product "category" list of strings (text?) not sure how to type it yet, or if category should be it's own class?
# skipped "similar_item"

schema = {
    "classes": [
     {
            # name of the class
            "class": "Product",
            # class properties
            "properties": [
                {
                    "name": "asin",
                    "dataType": ["string"],
                },
                {
                    "name": "title",
                    "dataType": ["text"],
                }
            ]
        }
            ]
}

client.schema.create(schema)


# so far i only got to successfully import 'asin', 'title'

def add_product(batch: Batch, product_data: dict) -> str:
    product_object = {
        'asin': product_data['asin'] if 'asin' in product_data else '',
        'title': product_data['title'] if 'title' in product_data else '',
        #'main_cat': product_data['main_cat'] if 'main_cat' in product_data else '',
        #'description':product_data['description'] if 'description' in product_data else '',               
        #'feature': product_data['feature'] if 'feature' in product_data else '',
        #'price': float(product_data['price'].replace("$","").replace(",","")) if 'price' in product_data else float("NaN")
    }
    # generate an UUID for the Author
    product_id = helper.generate_uuid('product', product_data['title']+product_data['asin'])
   
    # add article to the batch
    batch.add_data_object(  # old way was batch.add(...)
        data_object=product_object,
        class_name='Product',
        uuid=product_id
    )
    
    return product_id

from tqdm import trange

# just to test a small number to see if it works 

for i in trange(2000, 2500):
    product_id = add_product(client.batch, productData[i])    
    if i % 20 == 0:
        # submit the objects from the batch to weaviate
        client.batch.create_objects()
status_objects = client.batch.create_objects()
client.batch.flush()