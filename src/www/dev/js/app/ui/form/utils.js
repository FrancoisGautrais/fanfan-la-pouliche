
function default_validator(self, data){
    var errors = {}
    for(var i in self.required){
        var name = self.required[i];
        if(!data[name]){
            errors[name]="Champ '"+name+"' requis"
        }
    }
    return errors;
}

class Form extends React.Component {
    /*
        props={
            onChange: ...
            onValidate: ... // a gérer par la classe héritée
            validator: ...
        }
    */
    constructor(props, required=[]){
        super(props);
        this.required=required;
        this.state = props.value?props.value:{};
        this.onchangelistener= props.onChange?props.onChange:(()=>false);
        this.onchangevalidate= props.onValidate?props.onValidate:(()=>false);
        this.validator=props.validator?props.validator:default_validator;
        this.errors={}
    }

    validate(){
        return this.validator(this, this.state)
    }

    onchange(key, data, value){
        print("key:", key," value:", value)
        this.setState({ [key] : value})
    }

    _setState(fct, ...args){
        var self = this;
        return function(){
            self.setState({});
            if(fct){
                fct(...args);
            }
        }
    }

    handle_errors(errors){

        print("Error:", errors, this.state)
        for(var i in errors){
            print(i, errors[i])
        }

    }

    handle_send(fct){
        alert("Methode non implémentée !")
        throw "Methode non implémentée !"
    }

    onsend(fct){
        this.errors = this.validate();
        if(this.errors && Object.keys(this.errors).length){
            this.handle_errors(this.errors);
        }
        else{
            print("onsend=", fct)
            this.handle_send(fct);
        }
    }

}

module.exports={
    Form: Form
}