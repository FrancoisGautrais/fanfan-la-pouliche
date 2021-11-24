'use strict';
var utils =  module.load("js.react.component.common.utils")

var prop=null;
class SimpleInput extends React.Component {
  constructor(props) {
    super(props);
    this.attr = Object.assign({}, {
        id: utils.new_id(),
        placeholder: "",
        label: "",
        type: "text"
    }, props)
    this.state = { value: props.value?props.value:"" };
    this.onchangelistener= props.onChange?props.onChange:null;
    this.onchangevalidate= props.onValidate?props.onValidate:null;
  }

  onchange(event){
    var elem = event.target;
    var value = elem.value;
    if(this.attr.type=="file") value=elem.files[0]
    this.setState({value: value})
    if(this.onchangelistener){
        this.onchangelistener(this, value)
    }
  }

  onkeyup(event){
    if(event.keyCode==13 && this.onchangevalidate){
        this.onchangevalidate(this)
    }
  }

  render() {
        var file_accept=this.props.accept?this.props.accept:""
        var multiple=this.props.multiple?this.props.multiple:false;
       return (
            <div className={"input-group mb-2"+(this.attr.className?this.attr.className:"")}>
              {this.props.type!="file"?
                <label className="input-group-text" htmlFor={this.attr.id+".input"}>{this.attr.label}</label>:null}
              <input type={this.attr.type}
                    className="form-control"
                    placeholder={this.attr.placeholder}
                    name={this.attr.name}
                    onChange={this.onchange.bind(this)}
                    onKeyUp={this.onkeyup.bind(this)}
                    accept={file_accept}
                    multiple={multiple}
                    value={(this.attr.type!="file")?this.state.value:undefined}
                    id={this.attr.id+".input"}/>
              {this.props.children}
            </div>
       )
  }
}


module.exports={
    SimpleFile: function(props){

        return (
            <SimpleInput
                name={props.name}
                type="file"
                label={props.label}
                className={props.className}
                onChange={props.onChange}
                accept={props.accept?props.accept:".jpg,.jpeg"}
                multiple={props.multiple?props.multiple:false}
                value={props.props?props.props:null}
                id={props.id}/>
        )
    },
    SimpleInput: SimpleInput
}