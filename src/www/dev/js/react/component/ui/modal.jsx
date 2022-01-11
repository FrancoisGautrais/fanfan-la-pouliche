var utils =  module.load("js.react.component.common.utils")

function find_dialog_root(elem){
    var curr=$(elem);
    while(!curr.hasClass("modal")){
        curr=curr.parent();
    }
    return curr.parent();
}

class ModalStack extends React.Component {
    constructor(props) {
        super(props);
        this.root = React.createRef();
        this.background = React.createRef();
        this.modal = this.props.children;
        this.modal_div=null;
    }

    close(){
        $(this.root.current).remove()
    }

    componentDidMount(){
        this.modal_div = $(this.background.current).next();
        this.modal_div.css("z-index", this.props.index)
    }

    render(){
        var style={
            zIndex: this.props.index
        }

        return (
            <div ref={this.root}>
                <div className="modal-background"
                     style={style}
                     onClick={this.close.bind(this)}
                     ref={this.background}
                     id={this.props.id}>
                </div>
                {this.props.children}
            </div>
        )
    }

}



class ModalManager extends React.Component {
    constructor(props){
        super(props);
        this.start_z_index=100;
        this.state={ stack: new utils.Stack(), z_index: this.start_z_index };
        this.indexes={} // id => z_index
    }

    modal(modal){
        var z_index = this.state.z_index;
        var id = modal.props.id?modal.props.id:utils.new_id();

        this.setState({
            z_index: z_index+1,
            stack: this.state.stack.push(
                <ModalStack uuid={id} key={"key_"+id}>
                    {modal}
                </ModalStack>
            )
        })
        this.indexes[id]=z_index+1;
        return id;
    }

    remove(id){
        return this.pop(id);
    }

    pop(id=null){
        if(id){
            this.state.stack.pop();
        }else{
            this.state.stack.remove(id, e => e.props.uuid);
        }
        var index;
        if(this.state.stack.length()){
            index=this.indexes[this.state.stack.at(-1).props.id]+1;
        }else{
            index==this.start_z_index;
        }
        this.setState({z_index: index})
    }

    render(){
        return (
            <div className="modal-host">
                {this.state.stack.as_array()}
            </div>
        )
    }
}

var manager = React.createRef();

var x = <ModalManager ref={manager}/>;
ReactDOM.render(x, document.querySelector("#app-modal-host"))
manager=manager.current;


class ModalBase extends React.Component {
    constructor(props) {
        super(props);
        this.attr = Object.assign({}, {
            id: utils.new_id(),
            className: "",
            modal_type: "base",
            modal_size: props.size?props.size:"s"
        }, props)
        this.root = React.createRef();
        this.observer=null;

    }

    static modal(modal){
        return manager.modal(modal);
    }

    componentWillUnmount(){

    }

    close(){
    }

    componentDidMount(){

    }

    render(){
        var className="modal modal-"+this.attr.modal_type+" "+this.attr.className+" modal-size-"+this.attr.modal_size
        var ret = (
            <div    className={className}
                    ref={this.root}
                    id={this.attr.id}
                    onClick={() => false}>
                {this.props.children}
            </div>
        )
        return ret;
    }
}


function DialogModal(props){
    return (
        <ModalBase className={"modal-dialog "+props.className} {...props.attrs}>
            <div className="modal-dialog-title">
                <h1>
                    {props.title}
                </h1>
            </div>
            <div className="modal-content">
                {props.children}
            </div>
            <div className="modal-action-bar">
                {props.actions}
            </div>
        </ModalBase>
    )
}

class ButtonDialog extends React.Component {
    constructor(props){
        super(props);
        this.attr=utils.assign(
        {
            buttons: {
                yes: {
                    label: "Oui",
                    click:  e => true,
                    className: "btn bg-color-yes modal-action-yes"
                },
                no: {
                    label: "Non",
                    click: e => true,
                    className: "btn bg-color-no modal-action-no"
                },
                cancel: {
                    label: "Annuler",
                    click: e => true,
                    className: "btn bg-color-cancel modal-action-cancel"
                }
            }
        }, props)
    }

    close(){
        manager.remove(this.props.id);
    }


    render(){
        var buttons=[];
        var self = this;
        var wrapper =  function(self, button){
            return function(){
                var ret = button.click?button.click(self, self.props.id):true;
                if(ret) self.close();
            }
        }

        for(var i in this.attr.buttons){
            var b = this.attr.buttons[i];
            if(!b) continue;
            buttons.push(
                <a className={b.className} onClick={wrapper(self, b)} key={i}>
                    {b.label}
                </a>
            )
        }

        var content=this.props.children;
        if(this.props.content || this.props.title){
            content=(<div>
                <div className="modal-dialog-content">
                    <p>
                        {this.props.content?this.props.content:""}
                    </p>
                </div>
                {content}
            </div>)
        }


        return (
            <DialogModal  actions={buttons}
                            className={this.props.className}
                            title={this.props.title}
                            attrs={this.props.attrs}>
                {content}
            </DialogModal>
        )
    }

}



function YesNoCancelDialog(props){
    return (
        <ButtonDialog
            buttons={data}
            title={props.title}
            content={props.content}
            id={utils.new_id()}
            className={props.className}
            attrs={props.attrs}>
            {props.children}
        </ButtonDialog>
    )
}

function OkCancelDialog(props){
    var data = utils.assign({
            yes : {label: "OK"},
            no: null
        },
        {
            yes: props.yes?props.yes:(props.ok?props.ok:{}),
            cancel: props.cancel?props.cancel:{}
        }, props)
    return (
        <ButtonDialog
            buttons={data}
            title={props.title}
            content={props.content}
            id={utils.new_id()}
            className={props.className}
            attrs={props.attrs}>

            {props.children}
        </ButtonDialog>
    )
}


function WarningDialog(props){

    var data = utils.assign({
            yes : {label: "OK"},
            no: null
        },
        {
            yes: props.yes?props.yes:(props.ok?props.ok:{}),
            cancel: props.cancel?props.cancel:{}
        }, props)
    return (
        <ButtonDialog
            buttons={data}
            title={props.title}
            content={props.content}
            id={utils.new_id()}
            className={"modal-dialog-"+props.level}
            {...props.attrs}>

            {props.children}
        </ButtonDialog>
    )
}

function _warning_dialog(title, content, onyes, oncancel, level, label, cancel=false){
    var p = {
        yes: {click: onyes, label: label},
        cancel: cancel?{click: oncancel}:null
    }
    return ModalBase.modal(<WarningDialog title={title} content={content} level={level} yes={p.yes} cancel={p.cancel}/>)
}


function _warning_dialog_html(content, yes, cancel, level, label){
    return ModalBase.modal(<WarningDialog
                            yes={{click: yes, label: label?label:"OK"}}
                            cancel={cancel?{label: "Annuler"}:null}
                            level={level}
                            label>{content}</WarningDialog>)
}

module.exports = {
    OkCancelDialog: OkCancelDialog,
    YesNoCancelDialog: YesNoCancelDialog,
    ButtonDialog: ButtonDialog,
    DialogModal: DialogModal,
    ModalBase: ModalBase,
    error: (t,c,y,cancel) => _warning_dialog(t,c,y,cancel, "error", "Ok", false),
    warning: (t,c,y,cancel) => _warning_dialog(t,c,y,cancel, "warning", "Ok", false),
    confirm: (t,c,y,cancel) => _warning_dialog(t,c,y,cancel, "confirm", "Confirmer", true),
    validate: (c,y,cancel) => _warning_dialog_html(c,y,cancel, "validate", "Valider", true),
    error_html: (c,y,cancel) => _warning_dialog_html(<utils.RawHTML>{c}</utils.RawHTML>,y,cancel, "error", "Ok", false),
    WarningDialog: WarningDialog,
    ModalManager: manager,
    remove: id=>manager.remove(id),
    pop: ()=>manager.pop(),
    modal: ModalBase.modal
};