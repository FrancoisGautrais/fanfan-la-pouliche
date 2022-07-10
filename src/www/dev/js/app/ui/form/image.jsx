module.load("js.react.component.ui.widget.*")
var utils =  module.load("js.react.component.common.utils")
var tag =  module.load(".tag")
var ImageApi = module.load("js.app.model.image")
var {SimpleInput, SimpleFile} = module.load("js.react.component.ui.widget.input_text")
var { MultipleTagSelectInline } = module.load("js.app.ui.widget.tag")
var form_utils = module.load(".utils")
var modal = module.load("js.react.component.ui.modal")
var toast = module.load("js.react.component.ui.toast")
var {TagManage} = module.load("js.app.ui.modal.tag")

class SimpleImageForm extends form_utils.Form {

    constructor(props) {
        super(props, (props.value && props.value.uuid)?[]:["file"] );
    }

    onedit(fct, data){
        return fct?fct(data):null
    }

    handle_send(fct){
        if(this.props.is_tag) return fct(this.state)
        if(this.state.uuid){
            ImageApi.edit(this.state, this.onedit.bind(this,fct))
        }else{
            ImageApi.create(this.state, fct)
        }
    }

    render(){
        var btn = this.props.valide?<a className="btn btn-success" onClick={this.onsend.bind(this)}>Valider</a>:null;
        var tags = [];
        if(this.state.tags){
            for(var i in  this.state.tags){
                tags.push(this.state.tags[i][0]);
            }
        }

        return (
            <form className="container">

                {(!this.props.is_tag)?
                    <SimpleInput name="name" label="Nom" placeholder="Nom"
                            onChange={this.onchange.bind(this, "name")} value={this.state.name} error={this.errors.name}/>
                 :null}

                {(!this.props.is_tag)?
                    <SimpleInput name="description" label="Description" placeholder="Description"
                            onChange={this.onchange.bind(this, "description")}  value={this.state.description} error={this.errors.description}/>
                 :null}



                <MultipleTagSelectInline name="tags"  onChange={this.onchange.bind(this, "tags")}
                                value={tags}/>

                {(this.props.value&&this.props.value.uuid || this.props.is_tag)?null:
                    <SimpleFile name="file" label="Fichier" placeholder="Fichier" onChange={this.onchange.bind(this, "file")}
                         value={this.state.file}  error={this.errors.file} />}
                {btn}
            </form>
        )
    }
}



class SimpleImageEditForm extends SimpleImageForm {

    constructor(props) {
        super(props);
    }

    render(){
        return (
            <div>
                <img src={"/image/"+this.props.value.uuid+"/m"} />
                {super.render()}
            </div>
        )
    }
}

class ImageFragmentForm extends form_utils.Form {
    constructor(props) {
        super(props, ["name"]);
        this.state=props.value?props.value:{};
    }

    onvalid(){
        ImageApi.edit(this.state, function(){});
        this.props.parent.remove(this.props.id);
    }

    __remove(id){
        var self = this;
        ImageApi.remove(this.state.uuid, function(){
            self.props.parent.remove(self.props.id)
        });
        return true;
    }

    onremove(){
        var self = this;
        modal.confirm("Êtes-vous sure ?", "Voulez vous vraiment supprimer cette image ?", this.__remove.bind(this));
    }


    render(){
        return (
            <div className="image-edit-fragment">
                <div className="image-edit-fragment-img">
                    <img src={"/image/"+this.state.uuid+"/xs"} />
                </div>
                <div className="image-edit-fragment-form">
                    <SimpleInput name="name" label="Nom" placeholder="Nom"
                            onChange={this.onchange.bind(this, "name")} value={this.state.name} error={this.errors.name}/>

                    <SimpleInput name="description" label="Description" placeholder="Description"
                            onChange={this.onchange.bind(this, "description")}  value={this.state.description} error={this.errors.description}/>

                    <MultipleTagSelectInline name="tags"  onChange={this.onchange.bind(this, "tags")}
                                    value={this.state.tags}/>
                </div>
                <div className="image-edit-fragment-action">

                    <span className="material-icons" onClick={this.onremove.bind(this)}>delete</span>
                    <span className="material-icons" onClick={this.onvalid.bind(this)}>add</span>
                </div>

            </div>
        )
    }

}

class MultipleImageForm extends React.Component {
    constructor(props){
        super(props);

        this.queue=new utils.Queue();
        this.state={
            is_select: true,
            forms: []
        }
        this.files={}
        this.files_btn=React.createRef();
    }

    remove(id){
        var tmp=[]
        for(var i in this.state.forms){
            if(this.state.forms[i].id!=id){
                tmp.push(this.state.forms[i])
            }
        }
        delete this.files[this.state.forms[i].props.uuid];
        toast.info("L'image a été supprimé déja présent")
        this.setState({forms: tmp});
    }

    add_form(data, x, y, z){
        var self = this;
        var id = utils.new_id();
        var elem = {
            value: data,
            id: id,
            onsend: function(){
                self.remove(id);
            }
        }
        var forms = [...this.state.forms, elem];
        this.setState({forms: forms});
    }

    file_exists(file){
        for(var k in this.files){
            if(this.files[k].name==file.name && this.files[k].lastModified==file.lastModified &&
                this.files[k].size==file.size && this.files[k].type==file.type){
                return true;
            }
        }
        return false;
    }

    onupload(key, value, x, y){
        var self = this;

        for(var i=0; i<this.files_btn.current.files.length; i++){
            var file = this.files_btn.current.files.item(i);
            var fileid = utils.new_id();
            if(!this.file_exists(file)){
                this.queue.enqueue(ImageApi.create.bind(ImageApi), {file: file, fileid: fileid}, function(data){
                    var x = JSON.parse(data);
                    self.add_form(x.data);
                    self.queue.next();
                });
                this.files[fileid]=file;
            }else{
                toast.warning("Le fichier '"+file.name+"' est déja présent")
            }
        }
        this.files_btn.current.value="";
        this.queue.call();
    }

    render(){
        var id = utils.new_id();
        return (
            <div>

                <input
                    type="file"
                    name="files"
                    multiple={true}
                    accept=".jpg,.jpeg"
                    ref={this.files_btn}
                    onChange={this.onupload.bind(this, "files")} />

                {this.render_forms()}
            </div>
        )
    }

    render_forms(){
        var x = [];
        for(var i in this.state.forms){
            x.push(<ImageFragmentForm {...this.state.forms[i]} key={"render_forms."+i} parent={this}/>)
        }
        return (<div> {x}</div>)
    }
}

var listen_escape={};
var listen_escape_index=0;
$(document).keyup(function(e) {
     if (e.key === "Escape") { // escape key maps to keycode `27`
        for(var i in listen_escape){
            listen_escape[i]();
        }
    }
});

class ImageItem extends React.Component {
    constructor(props){
        super(props);
        this.listen_index = listen_escape_index;
        listen_escape_index++;
        this.data = props.data;
        this.parent = props.parent;
        this.parent.register(this);
        this.state={value: props.value, checked: false};
    }

    edit(data, fct){
        Object.assign(this.state.value, data)
        this.setState({});
    }

    url(size="xs"){
        return "/image/"+this.state.value.uuid+"/"+size
    }

    next(){
        return this.parent.after(this.state.value.uuid);
    }

    prev(){
        return this.parent.after(this.state.value.uuid);
    }

    onclick(){
        print("click")
    }

    onedit(evt){
        SimpleImageEditModal(this.state.value, this.edit.bind(this))
    }


    remove(){
        var self = this;
        this.parent.unregister(self);
        ImageApi.remove(self.state.value.uuid, function(){
            self.state.value.deleted=true;
            self.props.parent.notify_remove(self.state.value);
            if(self.props.onremove){
                self.props.onremove(self);
            }
        });
    }

    onremove(evt){
        var self = this;
        modal.confirm("Supprimer ?", "Voulez-vous vraiment supprimer l'image '"+this.state.value.name
            +"' ("+this.state.value.uuid+") définitivement ?", function(x){
                self.remove()
                return true;
            });
        this.onhide()
    }

    ondownload(){
        location.href="/image/"+this.state.value.uuid+"/original"
        this.onhide()
    }

    onshow(e){
        this.dropdown = $(e.target).parent().find(".custom-dropdown");
        this.dropdown.show()
        this.background=$("<div class=\"dropdown-background\"></div>")
        this.background.on("click", this.onhide.bind(this));
        $("body").append(this.background)
        listen_escape[this.listen_index]=this.onhide.bind(this);
    }

    onhide(){
        this.dropdown.hide()
        $(".dropdown-background").remove()
        delete listen_escape[this.listen_index];
    }

    onselect(){
        this.setState({checked: true});
        this.parent.onselected(this);
    }

    onunselect(){
        this.setState({checked: false});
        this.parent.onunselected(this);
    }


    render(){
        var check;
        if(this.state.checked){
            check=(<span
                    className="material-icons image-item-action image-item-action-select hide"
                    onClick={this.onunselect.bind(this)}>
                    check_box
                </span>);
        }
        else{
            check=(<span
                    className="material-icons image-item-action image-item-action-select hide"
                    onClick={this.onselect.bind(this)}>
                    check_box_outline_blank
                </span>);
        }

        return (
            <div
                className={"image-item "+(this.state.checked?'image-item-selected':'')}>
                <img src={ "/image/"+this.state.value.uuid+"/xs"}
                    onClick={this.onclick.bind(this)}/>
                {check}
                <span
                    className="material-icons image-item-action image-item-action-options hide"
                    onClick={this.onshow.bind(this)}>
                        more_horiz
                </span>
                <div className="custom-dropdown" aria-labelledby="">
                    <a className="dropdown-item" onClick={this.onremove.bind(this)}>Supprimer</a>
                    <a className="dropdown-item" onClick={this.ondownload.bind(this)}>Télécharger</a>
                </div>
                <span className="material-icons image-item-action image-item-action-edit hide"
                            onClick={this.onedit.bind(this)}>
                    edit
                </span>
            </div>
        )
    }

}

class ImageList extends React.Component {
    constructor(props){
        super(props);
        window.ImageListInstance=this;
        var self = this;
        this.state={
            images: props.images,
            selection: []
        }
        if(!this.state.images){
            ImageApi.list(function(data){
                self.setState({images: data});
            });
        }
        this.items=[];

    }

    select_all(){
        for(var i=0; i<this.items.length; i++)
            this.items[i].onselect()
    }

    unselect_all(){
        for(var i=0; i<this.items.length; i++)
            this.items[i].setState({checked: false})
        this.setState({selection: []})
    }

    onselected(x){
        if(this.state.selection.indexOf(x)<0)
            this.state.selection.push(x)
        this.setState({})
    }

    onunselected(x){
        for(var i=0; i<this.state.selection.length; i++){
            if(this.state.selection[i]==x){
                this.state.selection.pop(i);
                i--;
            }
        }
        this.setState({})
    }

    notify_remove(uuid){
        var n_images=[];
        for(var i in this.state.images){
            var img = this.state.images[i];
            if(uuid!=img){
                n_images.push(img)
            }
        }
        this.setState({})
    }

    on_images_add(a, b ,d, e, f){
        var data = JSON.parse(a);
        this.state.images.push(data.data);
        this.setState({})
    }



    add_image(){
        modal.modal(SimpleImage(this.on_images_add.bind(this)))
    }

    add_images(){
        modal.modal(MultipleImage(this.on_images_add.bind(this)))
    }

    register(x){
        for(var i  in this.items){
            if(this.items[i]==x) return
        }
        this.items.push(x);
    }

    unregister(x){
        this.onunselected(x)
        for(var i=0; i<this.items.length; i++){
            if(this.items[i]==x){
                this.items.pop(i);
                return
            }
        }
    }

    remove_all(){
        var self = this;
        modal.confirm("Supprimer ?", "Voulez-vous vraiment supprimer toutes ces images?", function(x){
                for(var i=self.state.selection.length-1; i>=0; i--){
                    self.state.selection[i].remove();

                }
                return true;
            });
    }

    add_tag(){
        var value = {
            uuid: "ok"
        }
        var img_form=SimpleImageEditModal(value, this.on_add_tag.bind(this), true)
    }

    remove_tag(){
        var value = {
            uuid: "ok"
        }
        var img_form=SimpleImageEditModal(value, this.on_remove_tag.bind(this), true)
    }

    on_remove_tag(list){
        list = list.tags;
        for(var i in this.state.selection){
            var x=this.state.selection[i];
            x.setState({})
            var item;
            for(var i in this.state.images){
                if(this.state.images[i].uuid == x.state.value.uuid){
                    item=this.state.images[i];
                    break;
                }
            }

            print('ImageApi.add_tags(',x.state.value.uuid, list, ');')
            ImageApi.remove_tags(x.state.value.uuid, list, function(data){
                x.state.value.tags=data;
                x.setState({})
                item.tags=data;
            });
        }
    }

    on_add_tag(list){
        list = list.tags;
        for(var i in this.state.selection){
            var x=this.state.selection[i];
            x.setState({})
            var item;
            for(var i in this.state.images){
                if(this.state.images[i].uuid == x.state.value.uuid){
                    item=this.state.images[i];
                    break;
                }
            }

            print('ImageApi.add_tags(',x.state.value.uuid, list, ');')
            ImageApi.add_tags(x.state.value.uuid, list, function(data){
                x.state.value.tags=data;
                x.setState({})
                item.tags=data;
            });
        }
    }

    add_category(){
        modal.modal(TagManage())
    }


    render(){

        var imgs = []
        for(var i in this.state.images){
            if(!this.state.images[i].deleted)imgs.push(<ImageItem value={this.state.images[i]} key={"image-item."+i} parent={this}/>)
        }
        var actions=[];
        if(this.state.selection.length){
            actions.push(<a className="btn btn-image-list-selection-red" key="1" onClick={this.remove_all.bind(this)}>Supprimer</a>)
            actions.push(<a className="btn btn-image-list-selection" key="2" onClick={this.add_tag.bind(this)}>Ajouter des tags</a>)
            actions.push(<a className="btn btn-image-list-selection-red" key="3" onClick={this.remove_tag.bind(this)}>Enlever des tags</a>)
        }

        return (
            <div className="image-list-root">
                <div className="image-list-action-line">
                    <a className="btn btn-image-list" onClick={this.add_image.bind(this)}>Ajouter une image</a>
                    <a className="btn btn-image-list" onClick={this.add_images.bind(this)}>Ajouter des images</a>
                    <a className="btn btn-image-list" onClick={this.add_category.bind(this)}>Ajouter des catégories</a>
                </div>

                <div className="image-list-action-line">
                    <a className="btn btn-image-list-selection" onClick={this.select_all.bind(this)}>Tout selectionner</a>
                    <a className="btn btn-image-list-selection" onClick={this.unselect_all.bind(this)}>Tout déselectionner</a>
                </div>
                <div className="image-list-action-line">
                    {actions}
                </div>
                <div className="image-list">
                    {imgs}
                </div>
            </div>

        )
    }
}



module.exports={
    SimpleImageForm: SimpleImageForm,
    MultipleImageForm: MultipleImageForm,
    SimpleImageEditForm: SimpleImageEditForm,
    ImageList: ImageList
}