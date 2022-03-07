from website.pagebuilder.pagebuilder import PageElement, register


@register("Text")
class HeaderElement(PageElement):
    FIELDS = ["label", "titre", "texte"]
    TEMPLATE = f"""
    <section id="%(label)s" class="section-texte">
        <div class="container">
            <div class="row mb50">
            
                <div class="sec-title text-center mb50 wow fadeInDown animated" data-wow-duration="500ms">
                    <h2>%(titre)s</h2>
                    <div class="devider"><i class="fa fa-heart-o fa-lg"></i></div>
                </div>
                
                <div class="sec-sub-title text-center wow rubberBand animated" data-wow-duration="1000ms">
                    <p class="texte">%(texte)s</p>
                </div>                
            </div>
        </div>
    </section>
    """