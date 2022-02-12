from website.pagebuilder.pagebuilder import PageElement, register


@register("Contact")
class HeaderElement(PageElement):
    FIELDS = ["label", "texte"]
    TEMPLATE = """
<section id="%(label)s" class="contact">
        <div class="container">
            <div class="row mb50">
            
                <div class="sec-title text-center mb50 wow fadeInDown animated" data-wow-duration="500ms">
                    <h2>Contactez-nous !</h2>
                    <div class="devider"><i class="fa fa-heart-o fa-lg"></i></div>
                </div>
                
                <div class="sec-sub-title text-center wow rubberBand animated" data-wow-duration="1000ms">
                    <p>%(texte)s</p>
                </div>
                

                <!--<div class="col-lg-3 col-md-3 col-sm-4 col-xs-12 wow fadeInLeft animated" data-wow-duration="500ms">
                    <div class="contact-address">
                        <h3> Eam tacimates philosophia ne</h3>
                        <p>1234 Nowhere, 00000,</p>
                        <p>Dallas. United States.</p>
                        <p>(541) 1234 567</p>
                    </div>
                </div> -->

                <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12 wow fadeInDown animated" data-wow-duration="500ms" data-wow-delay="300ms">
                    <div class="contact-form">
                        <h3>Votre message</h3>
                        <form action="#" id="contact-form">
                            <div class="input-group name-email">
                                <div class="input-field">
                                    <input type="text" name="name" id="contact-name" placeholder="Name" class="form-control">
                                </div>
                                <div class="input-field">
                                    <input type="email" name="email" id="contact-email" placeholder="Email" class="form-control">
                                </div>
                            </div>
                            <div class="input-group">
                                <textarea name="message" id="contact-message" placeholder="Message" class="form-control"></textarea>
                            </div>
                            <div class="input-group">
                                <a onclick="send_mail()" class="pull-right">Envoyer !</a>
                            </div>
                        </form>
                    </div>
                </div>


                <!--<div class="col-lg-1 col-md-1 col-sm-1 col-xs-12 wow fadeInRight animated" data-wow-duration="500ms" data-wow-delay="600ms">
                    <ul class="footer-social">
                        <li><a href="https://www.twitter.com/Themefisher"><i class="fa fa-twitter fa-2x"></i></a></li>
                        <li><a href="https://dribbble.com/themefisher"><i class="fa fa-dribbble fa-2x"></i></a></li>
                        <li><a href="https://www.facebook.com/Themefisher"><i class="fa fa-facebook fa-2x"></i></a></li>
                    </ul>
                </div>-->

                
            </div>
        </div>
    </section>
    """

