import json

from django.conf import settings
import unidecode

from website.common import errors

TEMPLATE="""<!DOCTYPE html>
<!--[if lt IE 7]>      <html lang="en" class="no-js lt-ie9 lt-ie8 lt-ie7"> <![endif]-->
<!--[if IE 7]>         <html lang="en" class="no-js lt-ie9 lt-ie8"> <![endif]-->
<!--[if IE 8]>         <html lang="en" class="no-js lt-ie9"> <![endif]-->
<!--[if gt IE 8]><!--> <html lang="en" class="no-js"> <!--<![endif]-->
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <title>%(title)s</title>
        <meta name="description" content="%(title)s">
        <meta name="viewport" content="width=device-width, initial-scale=1">
		<link href='http://fonts.googleapis.com/css?family=Open+Sans:400,300,600,700,800' rel='stylesheet' type='text/css'>
        <link rel="stylesheet" href="static/page/css/font-awesome.min.css">
        <link rel="stylesheet" href="static/page/css/bootstrap.min.css">
        <link rel="stylesheet" href="static/page/css/jquery.fancybox.css">
        <link rel="stylesheet" href="static/page/css/animate.css">
        <link rel="stylesheet" href="static/page/css/main.css">
        <link rel="stylesheet" href="static/page/css/media-queries.css">
        <link rel="stylesheet" href="static/page/css/common.css">
        <script src="static/page/js/modernizr-2.6.2.min.js"></script>

    </head>
	
    <body id="body">

		<div id="preloader">
			<img src="static/page/img/preloader.gif" alt="Preloader">
		</div>
        
        %(headers)s
        %(sections)s
		%(footers)s
		
		<a href="javascript:void(0);" id="back-top"><i class="fa fa-angle-up fa-3x"></i></a>
        <div class="viewer hidden" onclick="viewer.hide()">
            <div class="viewer-modal">
                <center class="viewer-img"></center>
                <center class="viewer-footer">
                    <a class="viewer-prev" onclick="viewer.show_prev()"><i class="fa fa-angle-left fa-lg"></i></a>
                    <span class="viewer-title"></span>
                    <a class="viewer-next" onclick="viewer.show_next()"><i class="fa fa-angle-right fa-lg"></i></a>
                </center>
            </div>
        </div>

        <script src="static/page/js/jquery-1.11.1.min.js"></script>
        <script src="static/page/js/jquery.singlePageNav.min.js"></script>
        <script src="static/page/js/bootstrap.min.js"></script>
        <script src="static/page/js/jquery.mixitup.min.js"></script>
        <script src="static/page/js/jquery.fancybox.pack.js"></script>
        <script src="static/page/js/jquery.parallax-1.1.3.js"></script>
        <script src="static/page/js/jquery-countTo.js"></script>
        <script src="static/page/js/jquery.appear.js"></script>
		<script src="http://cdnjs.cloudflare.com/ajax/libs/jquery.form/3.32/jquery.form.js"></script>
		<script src="http://cdnjs.cloudflare.com/ajax/libs/jquery-validate/1.11.1/jquery.validate.min.js"></script>
        <script src="static/page/js/jquery.easing.min.js"></script>
        <script src="static/page/js/wow.min.js"></script>
		<script>
			var wow = new WOW ({
				boxClass:     'wow',      // animated element css class (default is wow)
				animateClass: 'animated', // animation css class (default is animated)
				offset:       120,          // distance to the element when triggering the animation (default is 0)
				mobile:       false,       // trigger animations on mobile devices (default is true)
				live:         true        // act on asynchronously loaded content (default is true)
			  }
			);
			wow.init();
		</script>
        <script src="static/page/js/viewer.js"></script>
        <script src="static/page/js/custom.js"></script>
		
    </body>
</html>
"""

from website.models.pagebuilder import Page

def register(key):
    def wrapper(func):
        PageElement.ELEMENTS[key]=func
        return func
    return wrapper


_CHARS="abcdefghijklmnopqrstuvxyz-_123456789"
def to_html_id(x):
    x = unidecode.unidecode(x.lower())
    return "".join(c for c in x if c in _CHARS )


class PageElement:
    ELEMENTS={}
    FIELDS=[]
    TEMPLATE=""
    def __init__(self, content, page):
        self._content= content
        self._page = page
        for f in self.FIELDS:
            val=None
            if f in self._content:
                val = to_html_id(self._content[f]) if f=="label" else self._content[f]

            setattr(self, f, val)


    @staticmethod
    def instanciate(content, page):
        type = content["type"] if "type" in content else "default"
        if type in PageElement.ELEMENTS:
            return PageElement.ELEMENTS[type](content, page)
        raise errors.ElementNotFoundException("Type de section '%s' introuvable" % type)

    def get_data(self):
        return {
            k: getattr(self, k) for k in self.FIELDS
        }

    def generate(self):
        return self.TEMPLATE % self.get_data()

@register("section")
class Section:
    pass

class PageInfo:

    def __init__(self, pagecontent):
        pagecontent = json.loads(pagecontent)
        self.headers = pagecontent["headers"] if "headers" in pagecontent else []
        self.sections = [PageElement.instanciate(x, pagecontent) for x in  (pagecontent["sections"] if "sections" in pagecontent else [])]
        self.footers =  pagecontent["footers"] if "footers" in pagecontent else []
        self.title =  pagecontent.get("title")


    def generate(self):
        data = {
            "title" : self.title,
            "sections": " ".join([x.generate() for x in self.sections]),
            "headers": " ".join([x.generate() for x in self.headers]),
            "footers": " ".join([x.generate() for x in self.footers])
        }
        return TEMPLATE % data

CONTENT={
    "title" : "Fanfan la Pouliche",
    "headers" :[],
    "sections" :[
        {
            "type" : "Header"
        },
        {
            "type" : "Title",
            "label" : "Accueil",
            "images" : [
                {
                    "title" : "Premier titre",
                    "sub_title" : "Premier sous titre",
                    "image" : "static/page/img/banner.jpg"
                },
                {
                    "title" : "Deuxieme titre",
                    "sub_title" : "Deuxieme sous titre",
                    "image" : "static/page/img/banner.jpg"
                }
            ]
        },
        {
            "type" : "Text",
            "label" : "Qui sommes-nous ?",
            "texte": "Nous sommes nous..."

        },
        {
            "type" : "Gallery",
            "label" : "Gallerie",
            "titre" : "Gallerie",
            "introduction" : "Venez découvrir les clichés de Fanfan la pouliche !"

        },
        {
            "type" : "Text",
            "label" : "Utilisation des clichés",
            "texte": "Nous sommes nous..."

        },
        {
            "type" : "Contact",
            "label" : "Contact",
            "texte": "..."

        },
        {
            "type" : "Footer",
            "texte": 'Le site <a href="#">Fanfan la Pouliche</a> est développé, édité et hébergé (en Bretagne) par nos soins est es basé sur le template'
                     ' <a href="https://gridgum.com/themes/photography-bootstrap-responsive-theme/">Photography - Bootstrap responsive theme</a> disponible sur '
                     '<a href="https://gridgum.com">gridgum.com</a>'
        }
    ],
    "footers" :[],

}

CONTENT_MENTIONS={
    "title" : "Fanfan la Pouliche - mentions légales",
    "headers" :[],
    "sections" :[
        {
            "type" : "Header"
        },
        {
            "type" : "Text",
            "label" : "Mentions légales",
            "texte": "Nous sommes nous..."

        },
        {
            "type" : "Text",
            "label" : "Gestion des données personnelles",
            "texte": "Nous sommes nous..."

        },
        {
            "type" : "Footer",
            "texte": 'Le site <a href="#">Fanfan la Pouliche</a> est développé, édité et hébergé (en Bretagne) par nos soins est es basé sur le template'
                     ' <a href="https://gridgum.com/themes/photography-bootstrap-responsive-theme/">Photography - Bootstrap responsive theme</a> disponible sur '
                     '<a href="https://gridgum.com">gridgum.com</a>'
        }
    ],
    "footers" :[],

}



class PageBuilder:
    def __init__(self, page):
        self.page = page
        #self.content = PageInfo(self.page.content)
        self.content = PageInfo(json.dumps(CONTENT if page=="/" else CONTENT_MENTIONS))

    @staticmethod
    def from_url(url):
        page = Page.get_page(url)
        if not page:
            Page.set_page(url, {})

        if page: return PageBuilder(page)
        return None

    def generate(self):
        return self.content.generate()


