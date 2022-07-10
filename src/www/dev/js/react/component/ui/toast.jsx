var utils =  module.load("js.react.component.common.utils")
var manager = React.createRef();

class ToastManager extends React.Component {
    constructor(props){
        super(props);
        this.state={toasts: new utils.Stack()}
    }

    remove(id){
        this.setState({toasts: this.state.toasts.remove(id, e => e.props.id)})
    }

    append(text, level, classe=null){
        if(!classe) classe=Toast;
        var id = utils.new_id();
        var toast = <Toast text={text} level={level} id={id} parent={this} key={"key_"+id}></Toast>
        this.setState({toasts: this.state.toasts.push(toast)})
    }

    render(){
        return (
            <div className="toast-host">
                {this.state.toasts.as_array()}
            </div>
        )
    }

}

var x = <ToastManager ref={manager}/>;
ReactDOM.render(x, document.querySelector("#app-toast-host"))
manager=manager.current;

class Toast extends React.Component {
    constructor(props) {
        super(props);
        this.attr = Object.assign({}, {
            id: utils.new_id(),
            placeholder: "",
            label: "",
            type: "text"
        }, props)
        this.state = { };
        this.root = React.createRef();
        this.state = {id: null}
    }

    static toast(text, level="info"){
        manager.append(text, level, Toast);
    }

    static info(text){ Toast.toast(text, "info"); }
    static warning(text){ Toast.toast(text, "warning"); }
    static error(text){ Toast.toast(text, "error"); }

    onclick(){
        manager.remove(this.props.id)
    }

    render(){
        if(this.props.level=="info"){
            setTimeout(this.onclick.bind(this), 5000);
        }else if(this.props.level=="warning"){
            setTimeout(this.onclick.bind(this), 10000);
        }
        console.log(this.props.text)
        return (
            <div className={"toast toast-"+this.props.level} onClick={this.onclick.bind(this)} ref={this.root}>
                <utils.RawHTML>{this.props.text}</utils.RawHTML>
            </div>
        )
    }

}
/*
Toast.info("Une premire information")
Toast.warning("Une deuxieme information", "warning")
Toast.warning("Une deuxieme information", "warning")
Toast.warning("Une deuxieme information", "warning")
Toast.error("Une troisieme information", "error")*/

module.exports = Toast;