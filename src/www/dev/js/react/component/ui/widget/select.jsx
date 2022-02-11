var utils =  module.load("js.react.component.common.utils")
var events = module.load("js.react.component.ui.event")



function get_options(i, data){
    return Array.isArray(data)?data:[i, data];
}

class Select extends React.Component {
    constructor(props){
        super(props)

        this.state={options: props.options?props.options:[], selected: props.value?props.value:""}
        this.get_option_key=props.getkey?props.getkey:get_options
        this.label=props.label?props.label:" "
    }

    onchange(e){
        this.setState({selected: e.target.value})
        this.props.onChange && this.props.onChange(this, e.target.value)
    }

    render(){
        var opts = []
        if(this.label){
            opts.push(<option value="" key="default_key-1">{this.label}</option>)
        }

        for(var i in this.props.options){
            var opt = this.get_option_key(i, this.props.options[i]);
            opts.push(<option value={opt[0]} key={opt[0]+i}>{opt[1]}</option> )
        }
        return (
            <select
                className="form-select"
                value={this.state.selected}
                onChange={this.onchange.bind(this)}>

                {opts}
            </select>
        )
    }
}




class MultipleSelect extends React.Component {
    constructor(props){
        super(props);
        var opts=props.options?props.options:[]
        this.id=props.id?props.id:utils.new_id();
        this.root=React.createRef();
        var sel={};
        if(props.selecteds || props.value){
            var value = props.selecteds || props.value
            if(Array.isArray(value)){
                value.map((e,i)=>sel[e]=true);
            }else{
                sel=props.selecteds;
            }
        }
        if(!Object.keys(sel).length){
            Object.keys(opts).map((e,i)=>sel[e]=false);
        }
        this.state={
            options: opts,
            selecteds: sel,
            shown: false,
            filter: ""
        }
        this.get_option_key=props.getkey?props.getkey:get_options
        this.label=props.label?props.label:" "
    }

    on_cb_changed(key, e){
        var x = this.state.selecteds;
        x[key]=e.target.checked;
        this.setState({selecteds : x})
        var out=[]
        Object.keys(this.state.selecteds).map((e,i)=>this.state.selecteds[e] && out.push(e));
        print("changed : ", out)
        this.props.onChange && this.props.onChange(self, out)
    }

    _get_fragment(i, k){
        var opt = this.get_option_key(i,k);
        var key=opt[0], value=opt[1];
        if(this.state.shown){
            var filtered=true;
            if(this.state.filter.length){
                var l = this.state.filter.toLowerCase().split(" ");
                for(var n in l){
                    if(value.toLowerCase().indexOf(l[n])<0){
                        filtered=false;
                    }
                }
            }

            return filtered?( <div className="form-check" key={"key__"+this.id+"_"+i} >
                    <input className="form-check-input"
                            type="checkbox"
                            checked={this.state.selecteds[key]}
                            id={"__"+this.id+"_"+i}
                            onChange={this.on_cb_changed.bind(this, key)}/>
                    <label className="form-check-label" htmlFor={"__"+this.id+"_"+i}>
                        {value}
                    </label>
                </div>):null;
        }
        else{
            return this.state.selecteds[key]?(value):null;
        }

    }

    get_fragment(){
        var out = []
        for(var k in this.props.options){
            var tmp = this._get_fragment(k, this.props.options[k]);
            if(tmp) out.push(tmp);
        }
        return out;
    }

    onexpand(){
        this.setState({shown: true})
        var self = this;
        events.addOnClickOutside(this.id+"_click_outside", e => self.root.current, e=> self.unexpand());
    }

    ontextchange(e){
        this.setState({ filter: e.target.value});
    }

    ontextclean(){
        this.setState({ filter: ""});
    }

    unexpand(){
        this.setState({shown: false})
        events.remove(this.id+"_click_outside");
    }

    componentDidMount(){
    }
    componentWillUnmount() { }

    render(){
        var input = (
            <div>
                <span className="material-icons" onClick={this.ontextclean.bind(this)}>delete</span>
                <input type="text"
                        value={this.state.filter}
                        onChange={this.ontextchange.bind(this)} />
            </div>
        );
        var opts = this.get_fragment();
        return (
            <div className="custom-select form-select" ref={this.root}
                onClick={this.onexpand.bind(this)}>
                {this.state.shown?input:null}
                {this.state.shown?opts:(opts.join(", "))}
            </div>
        )
    }
}

var options = {
    "Var": "ok",
    "Var2": "ok2",
    "Var1": "ok3"
}
window.test=React.createRef();
//ReactDOM.render( <MultipleSelect options={options} ref={window.test}/>, $("#root-test")[0])

module.exports={
    Select: Select,
    MultipleSelect: MultipleSelect
}

