# How to use

1 Start up Weaviate: docker-compose up -d. Once completed, Weaviate is running on http://localhost:8081.

2 Install requirements: pip install -r requirements.txt

3 Run python import.py or use schema_import.ipynb to import 500 item of product id ('asin') and title to Weaviate. ( under construction. )

4 Navigate to console.semi.technology, connect to http://localhost:8081, navigate to the query module

5 Query example : get list of product title and id 

{
      Get {
        Product (
          limit:1
        ) {
          title 
          description
          asin
          price
          }
        }
}


6 To do semantic search on finding product that is useful for pet hair : 

    {
      Get {
        Product (
          limit:2
          nearText:{
            concepts:["good for pet hair"]
          }
        ) {
          title 
          description
          asin
          price
          }
        }
      
    }


# search-product-reviews-weaviate
Semantic search through amazon product utilizing reviews and descriptions

### Datasets Used ###

[Amazon Products Review Dataset](https://jmcauley.ucsd.edu/data/amazon/)

### User Query Parsing ###

[POS Tagging](https://spacy.io/usage/linguistic-features)

[Concise Concepts](https://github.com/Pandora-Intelligence/concise-concepts)

[Spacy Span Categorizer (detecting entities within entities)](https://spacy.io/api/spancategorizer)

[Spacy HealthSea - Making sense of user reviews](https://explosion.ai/blog/healthsea)

The colab notebook "cap_proj_NER_mvp.ipynb" demonstrates an approach for identifying Product, Vendor or
Category info in a user query.

### Data Indexing Pipeline ###

[Haystack from Deepset](https://haystack.deepset.ai/overview/intro)

### Vector Database ###

[Weaviate](https://weaviate.io/ )

### Ranking of Search Results Pipeline ###

[Haystack Retriever / Reader Nodes]( https://haystack.deepset.ai/components/ready-made-pipelines#documentsearchpipeline )