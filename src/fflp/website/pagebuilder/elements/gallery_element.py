import json

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
							%(tags_header)s
						</ul>
					</div>
					
				</div>
			</div>
			
			<div class="project-wrapper">
			    %(content)s
			</div>
			
			<script>var IMAGES = %(images)s</script>
		
		</section>"""


    def _figure(self, x):
        tags = " ".join([f"tag-{tag.uuid[:6]}" for tag in x.tags.all()])
        return f"""<figure class="mix work-item {tags} tile-image" data-image-id="{x.uuid}">
					<img src="/image/{x.uuid}/m" alt="">
					<figcaption class="overlay">
						<a class="preview-btn" title="{x.name}" onclick="viewer.show('{x.uuid}')"><i class="fa fa-eye fa-lg"></i></a>
						<a title="{x.name}" href="/image/{x.uuid}/l?download=true"><i class="fa fa-download fa-lg"></i></a>
						<h4>{x.description}</h4>
						<p>Fanfan la Pouliche</p>
					</figcaption>
				</figure>"""

    def _tag_header(self, id, name):
        return  f'<li><a href="javascript:;" data-filter=".tag-{id}" class="filter">{name}</a></li>'

    def get_data(self):
        try:
            tags = [ Tag.objects.get(name="public")]
        except Tag.DoesNotExist:
            tags = None
        all_tags = {}
        images = Image.objects.filter(tags__in=tags)[:8] if tags else []
        images_data = json.dumps({ img.uuid : img.as_dict() for img in images})
        for img in images:
            for tag in img.tags.all():
                id = tag.uuid[:6]
                if id not in all_tags and tag.name!="public":
                    all_tags[id]=tag.name

        print("images=", images)
        return {
            "label": self.label,
            "content" : "\n".join([ self._figure(x) for x in images]),
            "tags_header" : "\n".join([ self._tag_header(k,v) for k, v in all_tags.items()]),
            "introduction" : self.introduction,
            "titre" : self.titre,
            "images" : images_data,

        }
