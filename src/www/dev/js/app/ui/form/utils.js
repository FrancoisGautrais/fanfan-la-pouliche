
function default_validator(data, required=[]){
    var errors = {}
    for(var i in required){
        var name = required[name];
        if(!data[nam]){
            errors[name]="Champ '"+name+"' requis"
        }
    }
    return errors;
}

class Form extends React.Component {
    constructor(props, required){
        super(props);
        this.required=required;
        this.state = props.value?props.value:{};
        this.onchangelistener= props.onChange?props.onChange:null;
        this.onchangevalidate= props.onValidate?props.onValidate:null;
        this.validator=props.validator?props.validator:form_utils.default_validator;
    }

    onchange(key, data, value){
        this.setState({ [key] : value})
    }

    handle_errors(errors){
        print(errors)
        alert("Erreur !")
    }

    onsend(fct){
        var errors = this.validator(this, this.state)
        if(errors && Object.keys(errors).length){
            this.handle_errors(errors);
        }
        else{
            this.handle_send();
        }
    }

}

module.exports={
    default_validator: default_validator
}