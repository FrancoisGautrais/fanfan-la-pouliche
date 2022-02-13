

var _id=0;

class Page extends React.Component {
    constructor(props) {
        super(props);
        this.uuid = _id++;
        this.state={
            pages: props.pages,
            current: Object.keys(props.pages)[0]
        }
    }

    page_headers(){
        var out=[];
        for(var k in this.state.pages){
            out.push(<li
                        className="nav-bar-item btn page-header"
                        key={k}
                        onClick={this.set_page.bind(this, this.state.current)}>
                            {this.state.current}
                        </li>)
        }
        return out;
    }

    set_page(x){
        this.state.current = x;
        this.setState({})
    }

    get_id(current) {
        if(!current) current = this.state.current;
        return "page-"+this.uuid+"-"+current
    }


    render(){
        var page = this.state.pages[this.state.current];
        return (
            <div className="page-holder">
                <nav className="nav-bar page-header-dock">
                    <ul className="nav-bar-root">
                        {this.page_headers()}
                    </ul>
                </nav>
                <div className="page-content" id={this.get_id(this.state.current)}>
                    {page}
                </div>
            </div>
        )
    }

}
module.exports = Page
