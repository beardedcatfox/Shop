# Dropshipping Shop & Warehouse project (Books)
### Used: 
>Python + Django, Celery (+Beat) with Flower lib, Redis, DRF (Django REST Framework), PostgreSQL, S3 bucket (at DigitalOcean), Mailhog

## About:
>Scalable Warehouse-Shop project. Main DB at Warehouse, local DBs at Shop's
> sides. At Warehouse admin can create Books and Authors, or refresh those
> data. Also - changing Order's statuses. By adding one field in Warehouse models 
> we can make any count of Shops.
> 
> By Celery task we send Order from Shop to Warehouse (via API)
> By Celery Beat we check Order's statuses and data about Books and Authors (via API)

> Basic functionality in SHop: Register, Login, Cart, Order detail, Order list,
> Home page with Book list and sorting by Genres, Author's page, Book detail,
> Profile, Profile edit. 
> 
> Cart table entries deleting after confirming and creating
> Order. In Shop DB we have relations to id in Warehouse DB. 
> 
> Simple FrontEnd added.