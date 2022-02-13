import json

from django.conf import settings
import unidecode

from website.common import errors

__TEMPLATE = '''

		

		
		<section id="features" class="features">
			<div class="container">
				<div class="row">
				
					<div class="sec-title text-center mb50 wow bounceInDown animated" data-wow-duration="500ms">
						<h2>Features</h2>
						<div class="devider"><i class="fa fa-heart-o fa-lg"></i></div>
					</div>

					<div class="col-md-4 wow fadeInLeft" data-wow-duration="500ms">
						<div class="service-item">
							<div class="service-icon">
								<i class="fa fa-picture-o fa-2x"></i>
							</div>
							
							<div class="service-desc">
								<h3>Photography</h3>
								<p>Lorem ipsum dolor sit amet, sea ei iuvaret maiorum neglegentur. Ex facilis placerat vulputate duo. Eam tacimates philosophia ne. Eos deleniti maluisset ex, usu etiam dicant repudiandae in.</p>
							</div>
						</div>
					</div>
					

					<div class="col-md-4 wow fadeInUp" data-wow-duration="500ms" data-wow-delay="500ms">
						<div class="service-item">
							<div class="service-icon">
								<i class="fa fa-rocket fa-2x"></i>
							</div>
							
							<div class="service-desc">
								<h3>Development</h3>
								<p>Lorem ipsum dolor sit amet, sea ei iuvaret maiorum neglegentur. Ex facilis placerat vulputate duo. Eam tacimates philosophia ne. Eos deleniti maluisset ex, usu etiam dicant repudiandae in.</p>
							</div>
						</div>
					</div>

					<div class="col-md-4 wow fadeInRight" data-wow-duration="500ms"  data-wow-delay="900ms">
						<div class="service-item">
							<div class="service-icon">
								<i class="fa fa-check fa-2x"></i>
							</div>
							
							<div class="service-desc">
								<h3>Consulting</h3>
								<p>Lorem ipsum dolor sit amet, sea ei iuvaret maiorum neglegentur. Ex facilis placerat vulputate duo. Eam tacimates philosophia ne. Eos deleniti maluisset ex, usu etiam dicant repudiandae in.</p>
							</div>
						</div>
					</div>
						
				</div>
			</div>
		</section>

		
		<section id="works" class="works clearfix">
			<div class="container">
				<div class="row">
				
					<div class="sec-title text-center">
						<h2>Gallery</h2>
						<div class="devider"><i class="fa fa-heart-o fa-lg"></i></div>
					</div>
					
					<div class="sec-sub-title text-center">
						<p>Lorem ipsum dolor sit amet, sea ei iuvaret maiorum neglegentur. Ex facilis placerat vulputate duo. Eam tacimates philosophia ne. Eos deleniti maluisset ex, usu etiam dicant repudiandae in.</p>
					</div>
					
					<div class="work-filter wow fadeInRight animated" data-wow-duration="500ms">
						<ul class="text-center">
							<li><a href="javascript:;" data-filter="all" class="active filter">All</a></li>
							<li><a href="javascript:;" data-filter=".photography" class="filter">Photography</a></li>
							<li><a href="javascript:;" data-filter=".web" class="filter">web</a></li>
							<li><a href="javascript:;" data-filter=".logo-design" class="filter">logo design</a></li>
						</ul>
					</div>
					
				</div>
			</div>
			
			<div class="project-wrapper">
			
				<figure class="mix work-item photography">
					<img src="img/works/item-1.jpg" alt="">
					<figcaption class="overlay">
						<a class="fancybox" rel="works" title="Write Your Image Caption Here" href="img/works/item-1.jpg"><i class="fa fa-eye fa-lg"></i></a>
						<h4>Sea ei iuvaret maiorum neglegentur</h4>
						<p>Photography</p>
					</figcaption>
				</figure>
				
				<figure class="mix work-item web">
					<img src="img/works/item-2.jpg" alt="">
					<figcaption class="overlay">
						<a class="fancybox" rel="works" title="Write Your Image Caption Here" href="img/works/item-2.jpg"><i class="fa fa-eye fa-lg"></i></a>
						<h4>Sea ei iuvaret maiorum neglegentur</h4>
						<p>Photography</p>
					</figcaption>
				</figure>
				
				<figure class="mix work-item logo-design">
					<img src="img/works/item-3.jpg" alt="">
					<figcaption class="overlay">
						<a class="fancybox" rel="works" title="Write Your Image Caption Here" href="img/works/item-3.jpg"><i class="fa fa-eye fa-lg"></i></a>
						<h4>Sea ei iuvaret maiorum neglegentur</h4>
						<p>Photography</p>
					</figcaption>
				</figure>
				
				<figure class="mix work-item photography">
					<img src="img/works/item-4.jpg" alt="">
					<figcaption class="overlay">
						<a class="fancybox" rel="works" title="Write Your Image Caption Here" href="img/works/item-4.jpg"><i class="fa fa-eye fa-lg"></i></a>
						<h4>Sea ei iuvaret maiorum neglegentur</h4>
						<p>Photography</p>
					</figcaption>
				</figure>
			
				<figure class="mix work-item photography">
					<img src="img/works/item-5.jpg" alt="">
					<figcaption class="overlay">
						<a class="fancybox" rel="works" title="Write Your Image Caption Here" href="img/works/item-5.jpg"><i class="fa fa-eye fa-lg"></i></a>
						<h4>Sea ei iuvaret maiorum neglegentur</h4>
						<p>Photography</p>
					</figcaption>
				</figure>
				
				<figure class="mix work-item web">
					<img src="img/works/item-6.jpg" alt="">
					<figcaption class="overlay">
						<a class="fancybox" rel="works" title="Write Your Image Caption Here" href="img/works/item-6.jpg"><i class="fa fa-eye fa-lg"></i></a>
						<h4>Sea ei iuvaret maiorum neglegentur</h4>
						<p>Photography</p>
					</figcaption>
				</figure>
				
				<figure class="mix work-item logo-design">
					<img src="img/works/item-7.jpg" alt="">
					<figcaption class="overlay">
						<a class="fancybox" rel="works" title="Write Your Image Caption Here" href="img/works/item-7.jpg"><i class="fa fa-eye fa-lg"></i></a>
						<h4>Sea ei iuvaret maiorum neglegentur</h4>
						<p>Photography</p>
					</figcaption>
				</figure>
				
				<figure class="mix work-item photography">
					<img src="img/works/item-8.jpg" alt="">
					<figcaption class="overlay">
						<a class="fancybox" rel="works" title="Write Your Image Caption Here" href="img/works/item-8.jpg"><i class="fa fa-eye fa-lg"></i></a>
						<h4>Sea ei iuvaret maiorum neglegentur</h4>
						<p>Photography</p>
					</figcaption>
				</figure>
				
			</div>
		

		</section>

		
		<section id="team" class="team">
			<div class="container">
				<div class="row">
		
					<div class="sec-title text-center wow fadeInUp animated" data-wow-duration="700ms">
						<h2>Our Team</h2>
						<div class="devider"><i class="fa fa-heart-o fa-lg"></i></div>
					</div>
					
					<div class="sec-sub-title text-center wow fadeInRight animated" data-wow-duration="500ms">
						<p>Lorem ipsum dolor sit amet, sea ei iuvaret maiorum neglegentur. Ex facilis placerat vulputate duo. Eam tacimates philosophia ne. Eos deleniti maluisset ex, usu etiam dicant repudiandae in.</p>
					</div>

					<!-- single member -->
					<figure class="team-member col-md-3 col-sm-6 col-xs-12 text-center wow fadeInUp animated" data-wow-duration="500ms">
						<div class="member-thumb">
							<img src="static/page/img/team/member-1.png" alt="Team Member" class="img-responsive">
							<figcaption class="overlay">
								<h5>Ex facilis placerat vulputate </h5>
								<p>Eam tacimates philosophia ne Eos deleniti</p>
								<ul class="social-links text-center">
									<li><a href=""><i class="fa fa-twitter fa-lg"></i></a></li>
									<li><a href=""><i class="fa fa-facebook fa-lg"></i></a></li>
									<li><a href=""><i class="fa fa-google-plus fa-lg"></i></a></li>
								</ul>
							</figcaption>
						</div>
						<h4>John Doe</h4>
						<span>Marketing manager</span>
					</figure>
					<!-- end single member -->
					
					<!-- single member -->
					<figure class="team-member col-md-3 col-sm-6 col-xs-12 text-center wow fadeInUp animated" data-wow-duration="500ms" data-wow-delay="300ms">
						<div class="member-thumb">
							<img src="static/page/img/team/member-2.png" alt="Team Member" class="img-responsive">
							<figcaption class="overlay">
								<h5>Ex facilis placerat vulputate </h5>
								<p>Eam tacimates philosophia ne Eos deleniti</p>
								<ul class="social-links text-center">
									<li><a href=""><i class="fa fa-twitter fa-lg"></i></a></li>
									<li><a href=""><i class="fa fa-facebook fa-lg"></i></a></li>
									<li><a href=""><i class="fa fa-google-plus fa-lg"></i></a></li>
								</ul>
							</figcaption>
						</div>
						<h4>George Smith</h4>
						<span>Web Developer</span>
					</figure>
					<!-- end single member -->
					
					<!-- single member -->
					<figure class="team-member col-md-3 col-sm-6 col-xs-12 text-center wow fadeInUp animated" data-wow-duration="500ms" data-wow-delay="600ms">
						<div class="member-thumb">
							<img src="static/page/img/team/member-3.png" alt="Team Member" class="img-responsive">
							<figcaption class="overlay">
								<h5>Ex facilis placerat vulputate </h5>
								<p>Eam tacimates philosophia ne Eos deleniti</p>
								<ul class="social-links text-center">
									<li><a href=""><i class="fa fa-twitter fa-lg"></i></a></li>
									<li><a href=""><i class="fa fa-facebook fa-lg"></i></a></li>
									<li><a href=""><i class="fa fa-google-plus fa-lg"></i></a></li>
								</ul>
							</figcaption>
						</div>
						<h4>Steven Cavalli</h4>
						<span>Deisgner</span>
					</figure>
					<!-- end single member -->
					
					<!-- single member -->
					<figure class="team-member col-md-3 col-sm-6 col-xs-12 text-center wow fadeInUp animated" data-wow-duration="500ms" data-wow-delay="900ms">
						<div class="member-thumb">
							<img src="static/page/img/team/member-1.png" alt="Team Member" class="img-responsive">
							<figcaption class="overlay">
								<h5>Ex facilis placerat vulputate</h5>
								<p>Eam tacimates philosophia ne Eos deleniti</p>
								<ul class="social-links text-center">
									<li><a href=""><i class="fa fa-twitter fa-lg"></i></a></li>
									<li><a href=""><i class="fa fa-facebook fa-lg"></i></a></li>
									<li><a href=""><i class="fa fa-google-plus fa-lg"></i></a></li>
								</ul>
							</figcaption>
						</div>
						<h4>Mark Jefferson</h4>
						<span>Photographer</span>
					</figure>
					<!-- end single member -->
					
				</div>
			</div>
		</section>

		
		<section id="facts" class="facts">
			<div class="parallax-overlay">
				<div class="container">
					<div class="row number-counters">
						
						<div class="sec-title text-center mb50 wow rubberBand animated" data-wow-duration="1000ms">
							<h2>Our History</h2>
							<div class="devider"><i class="fa fa-heart-o fa-lg"></i></div>
						</div>
						
						<!-- first count item -->
						<div class="col-md-3 col-sm-6 col-xs-12 text-center wow fadeInUp animated" data-wow-duration="500ms">
							<div class="counters-item">
								<i class="fa fa-clock-o fa-3x"></i>
								<strong data-to="3200">0</strong>
								<!-- Set Your Number here. i,e. data-to="56" -->
								<p>Hours of Work</p>
							</div>
						</div>
						<div class="col-md-3 col-sm-6 col-xs-12 text-center wow fadeInUp animated" data-wow-duration="500ms" data-wow-delay="300ms">
							<div class="counters-item">
								<i class="fa fa-users fa-3x"></i>
								<strong data-to="620">0</strong>
								<!-- Set Your Number here. i,e. data-to="56" -->
								<p>Satisfied Customers</p>
							</div>
						</div>
						<div class="col-md-3 col-sm-6 col-xs-12 text-center wow fadeInUp animated" data-wow-duration="500ms" data-wow-delay="600ms">
							<div class="counters-item">
								<i class="fa fa-rocket fa-3x"></i>
								<strong data-to="765">0</strong>
								<!-- Set Your Number here. i,e. data-to="56" -->
								<p> Projects Launched </p>
							</div>
						</div>
						<div class="col-md-3 col-sm-6 col-xs-12 text-center wow fadeInUp animated" data-wow-duration="500ms" data-wow-delay="900ms">
							<div class="counters-item">
								<i class="fa fa-trophy fa-3x"></i>
								<strong data-to="13">0</strong>
								<!-- Set Your Number here. i,e. data-to="56" -->
								<p>Awards</p>
							</div>
						</div>
						<!-- end first count item -->
				
					</div>
				</div>
			</div>
		</section>

		
		<section id="contact" class="contact">
			<div class="container">
				<div class="row mb50">
				
					<div class="sec-title text-center mb50 wow fadeInDown animated" data-wow-duration="500ms">
						<h2>Contact Us</h2>
						<div class="devider"><i class="fa fa-heart-o fa-lg"></i></div>
					</div>
					
					<div class="sec-sub-title text-center wow rubberBand animated" data-wow-duration="1000ms">
						<p>Lorem ipsum dolor sit amet, sea ei iuvaret maiorum neglegentur. Ex facilis placerat vulputate duo. Eam tacimates philosophia ne. Eos deleniti maluisset ex, usu etiam dicant repudiandae in.</p>
					</div>
					

					<div class="col-lg-3 col-md-3 col-sm-4 col-xs-12 wow fadeInLeft animated" data-wow-duration="500ms">
						<div class="contact-address">
							<h3> Eam tacimates philosophia ne</h3>
							<p>1234 Nowhere, 00000,</p>
							<p>Dallas. United States.</p>
							<p>(541) 1234 567</p>
						</div>
					</div>

					<div class="col-lg-8 col-md-8 col-sm-7 col-xs-12 wow fadeInDown animated" data-wow-duration="500ms" data-wow-delay="300ms">
						<div class="contact-form">
							<h3>Send message!</h3>
							<form action="#" id="contact-form">
								<div class="input-group name-email">
									<div class="input-field">
										<input type="text" name="name" id="name" placeholder="Name" class="form-control">
									</div>
									<div class="input-field">
										<input type="email" name="email" id="email" placeholder="Email" class="form-control">
									</div>
								</div>
								<div class="input-group">
									<textarea name="message" id="message" placeholder="Message" class="form-control"></textarea>
								</div>
								<div class="input-group">
									<input type="submit" id="form-submit" class="pull-right" value="Send message">
								</div>
							</form>
						</div>
					</div>


					<div class="col-lg-1 col-md-1 col-sm-1 col-xs-12 wow fadeInRight animated" data-wow-duration="500ms" data-wow-delay="600ms">
						<ul class="footer-social">
							<li><a href="https://www.behance.net/Themefisher"><i class="fa fa-behance fa-2x"></i></a></li>
							<li><a href="https://www.twitter.com/Themefisher"><i class="fa fa-twitter fa-2x"></i></a></li>
							<li><a href="https://dribbble.com/themefisher"><i class="fa fa-dribbble fa-2x"></i></a></li>
							<li><a href="https://www.facebook.com/Themefisher"><i class="fa fa-facebook fa-2x"></i></a></li>
						</ul>
					</div>

					
				</div>
			</div>

			<div id="map_canvas" class="wow bounceInDown animated" data-wow-duration="500ms"></div>

		</section>

		
		
		<footer id="footer" class="footer">
			<div class="container">
				<div class="row">
				
					<div class="col-md-3 col-sm-6 col-xs-12 wow fadeInUp animated" data-wow-duration="500ms">
						<div class="footer-single">
							<img src="static/page/img/footer-logo.png" alt="">
							<p>Lorem ipsum dolor sit amet, sea ei iuvaret maiorum neglegentur. Ex facilis placerat vulputate duo. Eam tacimates philosophia ne. Eos deleniti maluisset ex, usu etiam dicant repudiandae in.</p>
						</div>
					</div>
				
					<div class="col-md-3 col-sm-6 col-xs-12 wow fadeInUp animated" data-wow-duration="500ms" data-wow-delay="300ms">
						<div class="footer-single">
							<h6>Subscribe </h6>
							<form action="#" class="subscribe">
								<input type="text" name="subscribe" id="subscribe">
								<input type="submit" value="&#8594;" id="subs">
							</form>
							<p>Lorem ipsum dolor sit amet, sea ei iuvaret maiorum neglegentur. </p>
						</div>
					</div>
				
					<div class="col-md-3 col-sm-6 col-xs-12 wow fadeInUp animated" data-wow-duration="500ms" data-wow-delay="600ms">
						<div class="footer-single">
							<h6>Explore</h6>
							<ul>
								<li><a href="#">About us</a></li>
								<li><a href="#">Facebook</a></li>
								<li><a href="#">Google</a></li>
								<li><a href="#">Support</a></li>
							</ul>
						</div>
					</div>
				
					<div class="col-md-3 col-sm-6 col-xs-12 wow fadeInUp animated" data-wow-duration="500ms" data-wow-delay="900ms">
						<div class="footer-single">
							<h6>Support</h6>
							<ul>
								<li><a href="#">Contact Us</a></li>
								<li><a href="#">Photos</a></li>
								<li><a href="#">Help Center</a></li>
								<li><a href="#">Newsroom</a></li>
							</ul>
						</div>
					</div>
					
				</div>
				<div class="row">
					<div class="col-md-12">
						<p class="copyright text-center">
							Copyright © 2016 <a href="http://www.gridgum.com/">Gridgum</a>
						</p>
					</div>
				</div>
			</div>
		</footer>

'''


TEMPLATE="""<!DOCTYPE html>
<!--[if lt IE 7]>      <html lang="en" class="no-js lt-ie9 lt-ie8 lt-ie7"> <![endif]-->
<!--[if IE 7]>         <html lang="en" class="no-js lt-ie9 lt-ie8"> <![endif]-->
<!--[if IE 8]>         <html lang="en" class="no-js lt-ie9"> <![endif]-->
<!--[if gt IE 8]><!--> <html lang="en" class="no-js"> <!--<![endif]-->
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <title>Photography One Page Bootstrap theme | Gridgum</title>
        <meta name="description" content="Photography One Page Bootstrap Template">
        <meta name="viewport" content="width=device-width, initial-scale=1">
		<link href='http://fonts.googleapis.com/css?family=Open+Sans:400,300,600,700,800' rel='stylesheet' type='text/css'>
        <link rel="stylesheet" href="static/page/css/font-awesome.min.css">
        <link rel="stylesheet" href="static/page/css/bootstrap.min.css">
        <link rel="stylesheet" href="static/page/css/jquery.fancybox.css">
        <link rel="stylesheet" href="static/page/css/animate.css">
        <link rel="stylesheet" href="static/page/css/main.css">
        <link rel="stylesheet" href="static/page/css/media-queries.css">
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


        <script src="static/page/js/jquery-1.11.1.min.js"></script>
        <script src="static/page/js/jquery.singlePageNav.min.js"></script>
        <script src="static/page/js/bootstrap.min.js"></script>
        <script src="static/page/js/jquery.fancybox.pack.js"></script>
        <script src="static/page/js/jquery.mixitup.min.js"></script>
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
		</script>cus
        <script src="static/page/js/custom.js"></script>
		
		<script type="text/javascript">
			$(function(){
				
				$('#contact-form').validate({
					rules: {
						name: {
							required: true,
							minlength: 2
						},
						email: {
							required: true,
							email: true
						},
						message: {
							required: true
						}
					},
					messages: {
						name: {
							required: "Please enter your name",
							minlength: "Your name must consist of at least 2 characters"
						},
						email: {
							required: "Please enter your email"
						},
						message: {
							required: "You have to enter something to send the form",
							minlength: "Not enough characters"
						}
					},
					submitHandler: function(form) {
						$(form).ajaxSubmit({
							type:"POST",
							data: $(form).serialize(),
							url:"process.php",
							success: function() {
								$('#contact-form :input').attr('disabled', 'disabled');
								$('#contact-form').fadeTo( "slow", 0.15, function() {
									$(this).find(':input').attr('disabled', 'disabled');
									$(this).find('label').css('cursor','default');
									$('#success').fadeIn();
								});
							},
							error: function() {
								$('#contact-form').fadeTo( "slow", 0.15, function() {
									$('#error').fadeIn();
								});
							}
						});
					}
				});
			});
		</script>
    </body>
</html>
"""

from website.models.pagebuilder import Page

def register(key):
    def wrapper(func):
        PageElement.ELEMENTS[key]=func
        return func
    return wrapper


_CHARS=["abcdefghijklmnopqrstuvxyz-_123456789"]
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


    def generate(self):
        data = {
            "sections": " ".join([x.generate() for x in self.sections]),
            "headers": " ".join([x.generate() for x in self.headers]),
            "footers": " ".join([x.generate() for x in self.footers])
        }
        return TEMPLATE % data

CONTENT={
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
            "type" : "Presentation",
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
            "type" : "Contact",
            "label" : "Contact",
            "texte": "..."

        }
    ],
    "footers" :[],

}



class PageBuilder:
    def __init__(self, page):
        self.page = page
        #self.content = PageInfo(self.page.content)
        self.content = PageInfo(json.dumps(CONTENT))

    @staticmethod
    def from_url(url):
        page = Page.get_page(url)
        if not page:
            Page.set_page(url, {})

        if page: return PageBuilder(page)
        return None

    def generate(self):
        return self.content.generate()
