

class Page extends React.Component {
    constructor(props) {
        super(props);
        this.state={
            pages: props.pages,
            current: Object.values(props.pages)[0]
        }
    }

    page_headers(){
        var out=[];
        for(var k in this.state.pages){
            out.append(<div className="page-header" key={k}>{this.state.pages[k]}</div>)
        }
    }

    render(){
        return (
            <div className="page-holder">
                <div className="page-header-dock">
                    {this.page_headers()}
                </div>
                <div className="page-content">
                    {this.state.pages[this.state.current]}
                </div>
            </div>
        )
    }

}

module.exports = Page
