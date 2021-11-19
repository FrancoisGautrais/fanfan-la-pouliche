var utils =  module.load("js.common.utils")



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
  }

  static toast(text, level="info"){
    utils.react_append(<Toast text={text} level={level}/>, document.querySelector('#app-toast-host'))
    }

    static info(text){ Toast.toast(text, "info"); }
    static warning(text){ Toast.toast(text, "warning"); }
    static error(text){ Toast.toast(text, "error"); }

  onclick(){
    $(this.root.current).remove()
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

Toast.info("Une premire information")
Toast.warning("Une deuxieme information", "warning")
Toast.error("Une troisieme information", "error")

module.exports = Toast;