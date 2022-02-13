from website.pagebuilder.pagebuilder import PageElement, register


@register("Presentation")
class HeaderElement(PageElement):
    FIELDS = ["label", "texte"]
    TEMPLATE = f"""
    <section id="%(label)s" class="contact">
        <div class="container">
            <div class="row mb50">
            
                <div class="sec-title text-center mb50 wow fadeInDown animated" data-wow-duration="500ms">
                    <h2>Présentation</h2>
                    <div class="devider"><i class="fa fa-heart-o fa-lg"></i></div>
                </div>
                
                <div class="sec-sub-title text-center wow rubberBand animated" data-wow-duration="1000ms">
                    <p>%(texte)s</p>
                </div>                
            </div>
        </div>
    </section>
    """