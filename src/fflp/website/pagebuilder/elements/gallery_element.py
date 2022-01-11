from ..pagebuilder import register, PageElement
from ...models import Image, Tag


@register("Gallery")
class HeaderElement(PageElement):
    FIELDS = ["label", "introduction", "titre"]
    TEMPLATE = """<section id="%(label)s" class="works clearfix">
			<div class="container">
				<div class="row">
					<div class="sec-title text-center">
						<h2>%(titre)s</h2>
						<div class="devider"><i class="fa fa-heart-o fa-lg"></i></div>
					</div>
					
					<div class="sec-sub-title text-center">
						<p>%(introduction)s</p>
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
			    %(content)s
			</div>
		
		</section>"""

    def _figure(self, x):
        return f"""<figure class="mix work-item">
					<img src="/image/{x.uuid}/m" alt="">
					<figcaption class="overlay">
						<a class="fancybox" rel="works" title="{x.name}" href="/image/{x.uuid}/original"><i class="fa fa-eye fa-lg"></i></a>
						<a class="fancybox" rel="works" title="{x.name}" href="/image/{x.uuid}/original"><i class="fa fa-download fa-lg"></i></a>
						<h4>{x.description}</h4>
						<p>Fanfan la Pouliche</p>
					</figcaption>
				</figure>"""



    def get_data(self):
        tags = [ Tag.objects.get(name="public")]
        images = Image.objects.filter(tags__in=tags)[:8]
        
        print("images=", images)
        return {
            "label": self.label,
            "content" : "\n".join([ self._figure(x) for x in images]),
            "introduction" : self.introduction,
            "titre" : self.titre
        }
