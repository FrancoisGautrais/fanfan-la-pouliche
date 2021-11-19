var utils =  module.load("js.common.utils")

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
            <div ref={this.root}><div className="modal-background"
                 style={style}
                 onClick={this.close.bind(this)}
                 ref={this.background}>
            </div>
                {this.props.children}
            </div>
        )
    }

}

class ModalEntry {
    constructor(modal, index){
        this.modal = modal;
        this.index = index;
        this.root = <ModalStack index={index}>{modal}</ModalStack>
    }
}

class ModalManager {
    constructor(){
        this.stack=[];
        this.start_z_index=10000;
        this.current_z_index=this.start_z_index;
        this.root=document.querySelector("#app-modal-host");
    }

    modal(modal){
        var elem = new ModalEntry(modal, ++this.current_z_index);
        utils.react_append(elem.root, this.root)
    }

    pop(){
        this.stack.pop();
        if(this.stack.length){
            this.current_z_index==this.stack[this.stack.length-1].index+1;
        }else{
            this.current_z_index=this.start_z_index;
        }
    }
}



var manager = new ModalManager();


window["_modal_manager"]=manager;
class ModalBase extends React.Component {
    constructor(props) {
        super(props);
        this.attr = Object.assign({}, {
            id: utils.new_id(),
            className: "",
            modal_type: "base",
            modal_size: "s"
        }, props)
        this.root = React.createRef();
        this.observer=null;

    }

    static modal(modal){
        manager.modal(modal);
    }

    onclose(){
        manager.pop();
        $(document).unbind('DOMNodeRemoved', this._bind_fct)
    }

    componentWillUnmount(){
    }

    close(){
        $(this.root.current).parent().remove()
        this.onclose()
    }

    componentDidMount(){
        var self = this;
        this._bind_fct=function(e) {
            if($(self.root.current).parent()[0] == e.target){
                self.onclose();
            }
        }
        $(document).bind('DOMNodeRemoved', this._bind_fct)

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
        <ModalBase>

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
                    click:  e => e.close(),
                    className: "btn modal-action-yes"
                },
                no: {
                    label: "Non",
                    click: e => e.close(),
                    className: "btn modal-action-no"
                },
                cancel: {
                    label: "Annuler",
                    click: e => e.close(),
                    className: "btn modal-action-cancel"
                }
            }
        }, props)
        print(this.props)
        this.root=React.createRef();
    }

    close(){
        find_dialog_root(this.root.current).remove();
    }


    render(){
        var buttons=[];
        var self = this;
        var wrapper =  function(self, button){
            return function(){
                if(button.click) button.click(self);
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

        return (
            <DialogModal actions={buttons}>
                <div ref={this.root} className="hidden"></div>
                {this.props.children}
            </DialogModal>
        )
    }

}

function YesNoCancelDialog(props){
    var data = {
    };

    return <ButtonDialog buttons={data}>{props.children}</ButtonDialog>
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
    return <ButtonDialog buttons={data}>{props.children}</ButtonDialog>
}

ModalBase.modal(<OkCancelDialog >Salut !</OkCancelDialog>)


module.exports = ModalBase;