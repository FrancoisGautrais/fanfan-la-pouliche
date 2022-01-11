from attr import attr

from .utils import attr
from ..pagebuilder import register, PageElement


@register("Title")
class TitleElement(PageElement):
    FIELDS = ["label", "images"]

    TEMPLATE = """
        <section id="%(label)s" class="elt-slider">
           <div id="carousel-example-generic" class="carousel slide" data-ride="carousel">

               <ol class="carousel-indicators">
                   <li data-target="#carousel-example-generic" data-slide-to="0" class="active"></li>
                   <li data-target="#carousel-example-generic" data-slide-to="1"></li>
               </ol>


               <div class="carousel-inner" role="listbox">
                    %(content)s
               </div>

           </div>
       </section>
    """

    def _image(self, i, x):
        return f"""
            <div class="item {"active" if not i else ""}" style="background-image: url({attr(x, "image")});">
                <div class="carousel-caption">
                    <h2 data-wow-duration="700ms" data-wow-delay="500ms" class="wow bounceInDown animated"><span>{attr(x, "title", "")}</span>!</h2>
                    <h3 data-wow-duration="1000ms" class="wow slideInLeft animated">{attr(x, "sub_title", "")}</h3>
                    
                </div>
            </div>
        """

    def get_data(self):
        return {
            "label": self.label,
            "content": "\n".join([self._image(i, x) for i, x in enumerate(self.images)])
        }
