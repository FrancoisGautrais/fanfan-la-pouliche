module.load("js.react.component.ui.widget.*")
var utils =  module.load("js.react.component.common.utils")
var tag =  module.load(".tag")
var ImageApi = module.load("js.app.model.image")
var {SimpleInput, SimpleFile} = module.load("js.react.component.ui.widget.input_text")
var { MultipleTagSelectInline } = module.load("js.app.ui.widget.tag")
var form_utils = module.load(".utils")

class SimpleImageForm extends React.Component {
  constructor(props) {
    super(props);
    this.required = ["file"]
    this.attr = Object.assign({}, {
        id: utils.new_id(),
        placeholder: "",
        label: "",
        type: "text"
    }, props)
    this.state = { uuid: props.value?props.value.uuid:null };
    this.onchangelistener= props.onChange?props.onChange:null;
    this.onchangevalidate= props.onValidate?props.onValidate:null;
    this.validator=props.validator?props.validator:form_utils.default_validator;
    this.errors = {};
  }

  onsend(fct){
        var errors = this.validator?this.validator(this, this.state):form_utils.default;
        if(errors && Object.keys(errors).length){

        }
        else{
            if(this.state.uuid){
                //edit
            }else{
                ImageApi.create(this.state, fct)
            }
        }
  }

  onchange(key, data, value){
    this.setState({ [key] : value})
  }

  render(){
    var btn = this.props.valide?<a className="btn btn-success" onClick={this.onsend.bind(this)}>Valider</a>:null;
    return (
        <form className="container">
            <SimpleInput name="name" label="Nom" placeholder="Nom"
                    onChange={this.onchange.bind(this, "name")} value={this.state.name} error={this.errors.name}/>

            <SimpleInput name="description" label="Description" placeholder="Description"
                    onChange={this.onchange.bind(this, "description")}  value={this.state.description} error={this.errors.description}/>

            <MultipleTagSelectInline name="tags"  onChange={this.onchange.bind(this, "tags")}
                            value={this.state.tags}/>

            {(this.props.value&&this.props.value.uuid)?null:
                <SimpleFile name="file" label="Fichier" placeholder="Fichier" onChange={this.onchange.bind(this, "file")}
                     value={this.state.file}  error={this.errors.file} />}

            {btn}
        </form>
    )
  }
}

module.exports={
    SimpleImageForm: SimpleImageForm
}