var utils =  module.load("js.react.component.common.utils")
var modal = module.load("js.react.component.ui.modal")

class MetaForm extends React.Component{
    /*
    props:{
        form: classe de formulaire à utiliser, [obligatoire]
        onsend: données envoyée au formulaire dans onsend
        title: titre de la modal,
        value: value du formulaire à utiliser

        label: label du bouton valider,
        cancel: objet cancel ou null ou vide,
        form_attr: attrs de formulaire à utiliser,
    }
    */

    constructor(props){
        super(props);
        this.form=React.createRef();
        this.attr={
            label: props.label?props.label:"Valider",
            title: props.title?props.title:"",
            cancel: props.cancel?props.cancel:{},
            close: props.close?props.close:true,
            id: props.id?props.id:utils.new_id(),
            form_attr: props.form_attr?props.form_attr:{},
            value: props.value
        }

        //this.props.innerRef declared
    }

    onclick(){
        var obj=null;
        var self=this;
        var fct = function(...args){
            if(self.props.onsend) self.props.onsend(...args, self.attr.id);
            if(self.attr.close){
                modal.remove(self.attr.id);
            }
        }
        if(!this.props.onsend || typeof this.props.onsend === "function"){
            obj=fct;
        }else if(this.props.onsend){
            var obj = utils.assign({}, this.props.onsend);
            obj.success=fct;
        }
        this.form.current.onsend(obj);
    }

    prepare(data){
        if(this.attr.prepare) this.attr.prepare(this, data);
    }

    render(){
        this.prepare(this.attr);
        return (
            <modal.OkCancelDialog id={this.attr.id}
                title={this.attr.title}
                title_btn={this.attr.title_btn}
                size={this.attr.size}
                yes={{label: this.attr.label,
                click: this.onclick.bind(this)}}
                attrs={this.props.modal}>
                <this.props.form value={this.attr.value} ref={this.form} {...this.attr.form_attr}/>
            </modal.OkCancelDialog>
        )
    }

    static show(data){
        modal.modal(<MetaForm value={data} attrs={modal}/>)
    }
}

module.exports={
    ModalForm: MetaForm
}