var utils =  module.load("js.react.component.common.utils")
var tags = module.load("js.app.model.tag")
var {SimpleInput, SimpleFile} = module.load("js.react.component.ui.widget.input_text")
var select = module.load("js.react.component.ui.widget.select")
var {SimpleInput} = module.load("js.react.component.ui.widget.input_text")
var modal = module.load("js.react.component.ui.modal")
var form_utils = module.load(".utils")


class TagAddForm extends React.Component {
    constructor(props){
        super(props);
        this.state = props.value?props.value:{};
        this.onchangelistener= props.onChange?props.onChange:null;
        this.onchangevalidate= props.onValidate?props.onValidate:null;
        this.validator=props.validator?props.validator:form_utils.default_validator;
        this.errors = {};
    }


    onsend(fct){
        var errors = this.validator(this, this.state)
        if(errors && Object.keys(errors).length){

        }
        else{
            var self=this;
            tags.create(this.state, function(e) {self.setState({do_update : true}); fct && fct(e) })
        }
    }

    onchange(key, data, value){
        this.setState({ [key] : value})
    }

    render(){
        var btn = this.props.valide?<a className="btn btn-success" onClick={this.onsend.bind(this)}>Valider</a>:null;
        this.state.do_update=false;
        return (
            <form className="container">
                <SimpleInput name="name" label="Nom" placeholder="Nom"
                        onChange={this.onchange.bind(this, "name")} value={this.state.name} error={this.errors.name}/>

                <SimpleInput name="description" label="Description" placeholder="Description"
                        onChange={this.onchange.bind(this, "description")}  value={this.state.description} error={this.errors.description}/>

                <select.Select name="parent" options={tags.list()} getkey={(k,v)=>[k, v.name]} label="Parent"
                        onChange={this.onchange.bind(this, "parent")} value={this.state.parent}/>
                {btn}
            </form>
        );
    }
}

class TagManageForm extends React.Component {
    constructor(props){
        super(props)
        this.state={opened: {}}
        this.root=React.createRef();
        this.form=React.createRef();
    }


    fold(node) {
        var tmp = this.state.opened;
        tmp[node.uuid]=true;
        this.setState({opened: tmp})
    }

    unfold(node){
        var tmp = this.state.opened;
        tmp[node.uuid]=false;
        this.setState({opened: tmp})
    }

    onedit(node){
        var self = this;
        modal.validate(<TagAddForm ref={this.form} value={node}/>, function(mod, id){
            tags.edit(self.form.current.state, function(){
                self.setState({ __update: true});
                modal.remove(id);
            });
        }, "Annuler")
    }


    onadd(node){

        var self = this;
        modal.validate(<TagAddForm ref={this.form} value={{parent: node.uuid}}/>, function(mod, id){
            tags.create(self.form.current.state, function(){
                self.setState({ __update: true});
                modal.remove(id);
            });
        }, "Annuler")
    }


    onremove(node){
        modal.confirm("Êtes-vous sûr ?",
            "Voulez vous vraiment supprimer le tag '"+node.path+"' "+(node.children.length?"et se sous-tags ?":""),
            this.onremove_validate.bind(this, node));
    }

    onremove_validate(node, mod, id){
        var self = this;
        tags.remove(node.uuid, function(){
            self.setState({});
            modal.remove(id);
        })
    }

    render_node(node){
        var children = []
        for(var i in node.children){
            children.push(this.render_node(node.children[i]))
        }

        children=children.length?<ul>{children}</ul>:null
        var isopen=(this.state.opened[node.uuid]!=false);

        var arrow=isopen?<span className="material-icons tree-tag-arrow" onClick={this.unfold.bind(this, node)}>keyboard_arrow_down</span>
                        :<span className="material-icons tree-tag-arrow"  onClick={this.fold.bind(this, node)}>keyboard_arrow_right</span>;
        return (
                <li
                    key={node.path+" "+node.uuid}
                    className={"tree-tag "+(children?"tree-tag-node":"tree-tag-leaf")}>

                    <span className="tree-tag-label">
                        {children?(arrow):null}
                        {node.name}
                        <span
                            className="material-icons tree-tag-action tree-tag-action-add"
                            onClick={this.onadd.bind(this, node)}>
                                add
                        </span>
                        <span
                            className="material-icons tree-tag-action tree-tag-action-edit"
                            onClick={this.onedit.bind(this, node)}>
                                edit
                        </span>
                        <span
                            className="material-icons tree-tag-action tree-tag-action-remove"
                            onClick={this.onremove.bind(this, node)}>
                                remove
                        </span>

                    </span>

                    {isopen?children:null}
                </li>
        )
    }

    render(){
        var tmp = {name: "Tags", path: "", children: Object.values(tags.tree())}
        return <div ref={this.root}>{this.render_node(tmp)}</div>;
    }
}

ReactDOM.render(<TagAddForm valide={true}/>, $("#root-test2")[0])
ReactDOM.render(<TagManageForm />, $("#root-test3")[0])

module.exports={
    TagAddForm: TagAddForm,
}