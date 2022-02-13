from ..pagebuilder import register, PageElement, to_html_id
import unidecode



@register("Header")
class HeaderElement(PageElement):
    FIELDS = []
    TEMPLATE = """<header id="navigation" class="navbar-fixed-top navbar">
            <div class="container">
                <div class="navbar-header">
					<button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                        <span class="sr-only">Toggle navigation</span>
                        <i class="fa fa-bars fa-2x"></i>
                    </button>

                    <a class="navbar-brand" href="#body">
						<h1 id="logo">
							<img src="static/page/img/logo.png" alt="Photography">
						</h1>
					</a>
                </div>

                <nav class="collapse navbar-collapse navbar-right" role="navigation">
                    <ul id="nav" class="nav navbar-nav">
                        %(elements)s
                    </ul>
                </nav>
				
            </div>
        </header>
        """

    def _li(self, i, x):
        if "label" not in x:
            return ""
        name = x["label"]
        print(f"i={i}")
        classe='classe="current"' if i==1 else ""
        id =to_html_id(name)
        return f'<li><a href="#{id}" {classe}>{name}</a></li>\n'

    def get_data(self):
        return {
            "elements": "".join([self._li(i, x) for i, x in enumerate(self._page["sections"])])
        }
