
from ..pagebuilder import register, PageElement
from ...models import Tag, Image


@register("Title")
class TitleElement(PageElement):
    FIELDS = ["label", "images"]

    TEMPLATE = """
        <section id="%(label)s" class="elt-slider">
           <div id="carousel-example-generic" class="carousel slide" data-ride="carousel">

               <ol class="carousel-indicators">
                   %(points)s
               </ol>

               <div class="carousel-inner" role="listbox">
                    %(content)s
               </div>

           </div>
       </section>
    """

    # def _image(self, i, x):
    #     return f"""
    #         <div class="item {"active" if not i else ""}" style="background-image: url({attr(x, "image")});">
    #             <div class="carousel-caption">
    #                 <h2 data-wow-duration="700ms" data-wow-delay="500ms" class="wow bounceInDown animated"><span>{attr(x, "title", "")}</span>!</h2>
    #                 <h3 data-wow-duration="1000ms" class="wow slideInLeft animated">{attr(x, "sub_title", "")}</h3>
    #             </div>
    #         </div>
    #     """

    def _image(self, i, x):
        return f"""
            <div class="item {"active" if not i else ""}" style="background-image: url(/image/{x.uuid}/l);">
                <div class="carousel-caption">
                    <h2 data-wow-duration="700ms" data-wow-delay="500ms" class="wow bounceInDown animated"><span>{x.name}</span></h2>
                    <h3 data-wow-duration="1000ms" class="wow slideInLeft animated">{x.description}</h3>
                </div>
            </div>
        """

    def _point(self, i):
        return f"""
                   <li data-target="#carousel-example-generic" data-slide-to="{i}" {'class="active"'if not i else ''}></li>
"""

    def get_data(self):
        try:
            tags = [ Tag.objects.get(name="accueil")]
        except Tag.DoesNotExist:
            tags = None
        images = [] if not tags else Image.objects.filter(tags__in=tags)[:8]
        return {
            "label": self.label,
            "content": "\n".join([self._image(i, x) for i, x in enumerate(images)]),
            "points" : "\n".join([self._point(i) for i, x in enumerate(images)]),
        }
