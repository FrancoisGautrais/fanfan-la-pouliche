module.load("js.react.component.ui.widget.*")
var utils = module.load("js.common.utils")
var {api} = module.load("js.common.api")
var {SimpleInput, SimpleFile} = module.load("js.react.component.ui.widget.input_text")


class SimpleImageForm extends React.Component {
  constructor(props) {
    super(props);
    this.attr = Object.assign({}, {
        id: utils.new_id(),
        placeholder: "",
        label: "",
        type: "text"
    }, props)
    this.state = { };
    this.onchangelistener= props.onChange?props.onChange:null;
    this.onchangevalidate= props.onValidate?props.onValidate:null;

  }

  onsend(){
        api.image_create_x(this.state, print, print)
  }

  onchange(data, value){
    this.setState({ [data.props.name] : value})
    print(this.state)
  }

  render(){
    return (
        <form>
            <SimpleInput name="name" label="Nom" placeholder="Nom" onChange={this.onchange.bind(this)}/>
            <SimpleInput name="description" label="Description" placeholder="Description" onChange={this.onchange.bind(this)}/>
            <SimpleFile name="file" label="Fichier" placeholder="Fichier" onChange={this.onchange.bind(this)}/>
            <a className="btn btn-success" onClick={this.onsend.bind(this)}>Valider</a>
        </form>
    )
  }

}

module.exports=SimpleImageForm;