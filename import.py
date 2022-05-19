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


# initiate the Weaviate client
client = weaviate.Client("http://localhost:8081")
client.timeout_config = (3, 200)


# load all metadata
count = 0
data = []
with open('data/sample_meta_Home_and_Kitchen.json', 'r') as f:
    for l in tqdm(f):
        data.append(json.loads(l))
        count = count + 1
        if count >= 3000:
          break

# data cleaning, weaviate would run into issues if a property is missing in instance of data
 
productData = []

for i in range(0, 3000):
    hasprice="price" in data[i]
    hastitle="title" in data[i]
    hasdescription="description" in data[i]
    hasmaincat='main_cat' in data[i]

    if (hasprice and hastitle and hasdescription and hasmaincat)==True:
        if len(data[i]['title'])<200:
            productData.append(data[i])
    else:
        continue


for i in range(0, len(productData)): 
   productData[i]['description']=" ".join(productData[i]['description'])
   cleaned_text = productData[i]['description'].replace("\\", "")
   productData[i]['description']=cleaned_text
   productData[i]['price']=productData[i]['price'].replace("$","").replace(",","")
   productData[i]['price']=float(productData[i]['price'])



# delete all classes
client.schema.delete_all() 
# create schema 
schema = {
    "classes": [
        {
            # name of the class
            "class": "Product",
            # class properties
            "properties": [
                {
                    "name": "asin",
                    "dataType": ["string"]
                },
                {
                    "name": "title",
                    "dataType": ["text"]
                },
                {
                    "dataType": ["number"],
                    "description": "The price product in dollars",
                    "name": "price"
                },
                {
                    "dataType": ["text"],
                    "name": "productDescription",
                    "description": "description of product"

                },
                {
                    "dataType": ["string"],
                    "name": "mainCat",
                    "description": "main category of the product in amazon "
                }
            ]
        }
    ]
}
client.schema.create(schema)


# ignoring features and categories for now 
from weaviate.batch import Batch # for the typing purposes
def add_product(batch: Batch, product_data: dict) -> str:
    product_object = {
        'asin': product_data['asin'],
        'title': product_data['title'],
        'main_cat': product_data['main_cat'],
        'description': product_data['description'],             
        'price': product_data['price']
    }
    # generate an UUID for the Author
    product_id = helper.generate_uuid('product', product_data['title']+product_data['asin'])
   
    # add article to the batch
    batch.add_data_object(  
        data_object=product_object,
        class_name='Product',
        uuid=product_id
    ) 
    return product_id


def add_product(batch: Batch, product_data: dict) -> str:
    product_object = {
        'asin': product_data['asin'],
        'title': product_data['title'],
        'main_cat': product_data['main_cat'],
        'description': product_data['description'],             
        #'feature': product_data['feature'] if 'feature' in product_data else '',
        'price': product_data['price']
    }
    # generate an UUID for the Author
    product_id = helper.generate_uuid('product', product_data['title']+product_data['asin'])
   
    # add article to the batch
    batch.add_data_object(  
        data_object=product_object,
        class_name='Product',
        uuid=product_id
    ) 
    return product_id




# just to test a small number to see if it works 
# this can take about 5 mins 
from tqdm import trange
for i in trange(0, 500):
    product_id = add_product(client.batch, productData[i])    
    if i % 20 == 0:
        # submit the objects from the batch to weaviate
        client.batch.create_objects()
status_objects = client.batch.create_objects()
client.batch.flush()



# show totle of items imported 
result = client.query.get(class_name='Product', properties="title")\
    .do()
print(f"Number of reviews returned: {len(result['data']['Get']['Product'])}")
#result