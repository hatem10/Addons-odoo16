{
    "name":"Cine Star Peliculas",
    "description":"""
        Este modulo consiste en almacenar y llevar el control de consumo de peliculas
        por el cliente
    """,
    "author":"Johao Marcos Maldonado Roman",
    "version":"16.0.0.1",
    "category":"Peliculas",
    "depends":[
        "base",
        "mail",
        "account"
    ],
    "data":[
        #data
        "data/movie_author.xml",
        "data/movie_genero.xml",
        "data/movie_presupuesto.xml",
        #"data/movie.xml",
        #views
        "views/movie_view.xml",
        "views/movie_author_view.xml",
        "views/movie_presupuesto.xml",
        "views/menu.xml"
    ],
    "assets":{
        "web.assets_backend":[],
        "web.assets_frontend":[]
    }

}