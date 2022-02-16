from website.pagebuilder.pagebuilder import PageElement, register


@register("Footer")
class HeaderElement(PageElement):
    FIELDS = ["texte"]
    TEMPLATE = """
        <footer id="footer" class="footer">
           <div class="container">
               <div class="row">

                   <div class="col-md-9 col-sm-9 col-xs-12 wow fadeInUp animated" data-wow-duration="500ms">
                       <div class="footer-single">
                           <img src="static/page/img/footer-logo.png" alt="">
                           <p>%(texte)s</p>
                       </div>
                   </div>

                   <div class="col-md-3 col-sm-3 col-xs-12 wow fadeInUp animated" data-wow-duration="500ms" data-wow-delay="900ms">
                       <div class="footer-single">
                           <h6>Informations</h6>
                           <ul>
                               <li><a href="#">Mention légales</a></li>
                               <li><a href="#">Données personelles</a></li>
                           </ul>
                       </div>
                   </div>

               </div>
           </div>
       </footer>

    """

