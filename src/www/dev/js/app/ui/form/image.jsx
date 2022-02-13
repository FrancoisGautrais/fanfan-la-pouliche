module.load("js.react.component.ui.widget.*")
var utils =  module.load("js.react.component.common.utils")
var tag =  module.load(".tag")
var ImageApi = module.load("js.app.model.image")
var {SimpleInput, SimpleFile} = module.load("js.react.component.ui.widget.input_text")
var { MultipleTagSelectInline } = module.load("js.app.ui.widget.tag")
var form_utils = module.load(".utils")
var modal = module.load("js.react.component.ui.modal")
var toast = module.load("js.react.component.ui.toast")

class SimpleImageForm extends form_utils.Form {

    constructor(props) {
        super(props, (props.value && props.value.uuid)?[]:["file"] );
    }

    onedit(fct, data){
        return fct?fct(data):null
    }

    handle_send(fct){
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
                <SimpleInput name="name" label="Nom" placeholder="Nom"
                        onChange={this.onchange.bind(this, "name")} value={this.state.name} error={this.errors.name}/>

                <SimpleInput name="description" label="Description" placeholder="Description"
                        onChange={this.onchange.bind(this, "description")}  value={this.state.description} error={this.errors.description}/>

                <MultipleTagSelectInline name="tags"  onChange={this.onchange.bind(this, "tags")}
                                value={tags}/>

                {(this.props.value&&this.props.value.uuid)?null:
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

class ImageItem extends React.Component {
    constructor(props){
        super(props);
        this.data = props.data;
        this.parent = props.parent;
        this.state={value: props.value};
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
        var img_form=SimpleImageEditModal(this.state.value, this.edit.bind(this))

    }

    onremove(evt){
        var self = this;
        modal.confirm("Supprimer ?", "Voulez-vous vraiment supprimer l'image '"+this.state.value.name
            +"' ("+this.state.value.uuid+") définitivement ?", function(x){
                ImageApi.remove(self.state.value.uuid, function(){
                    self.state.value.deleted=true;
                    self.props.parent.notify_remove(self.state.value);
                    if(self.props.onremove){
                        self.props.onremove(self);
                    }
                });
                return true;
            });
    }

    ondownload(){
        location.href="/image/"+this.state.value.uuid+"/original"
    }

    render(){
        return (
            <div
                className="image-item">
                <img src={ "/image/"+this.state.value.uuid+"/xs"}
                    onClick={this.onclick.bind(this)}/>
                <span
                    className="material-icons image-item-action image-item-action-delete hide"
                    onClick={this.onremove.bind(this)}>
                        more_horiz
                    </span>
                <span className="material-icons image-item-action image-item-action-edit hide"
                    onClick={this.onedit.bind(this)}>
                    edit
                </span>
                <span className="material-icons image-item-action image-item-action-download hide"
                    onClick={this.ondownload.bind(this)}>
                    download
                </span>
            </div>
        )
    }

}


class ImageList extends React.Component {
    constructor(props){
        super(props);
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

    render(){
        var imgs = []
        for(var i in this.state.images){
            if(!this.state.images[i].deleted)imgs.push(<ImageItem value={this.state.images[i]} key={"image-item."+i} parent={this}/>)
        }

        return (
            <div className="image-list-root">
                <a className="btn" onClick={this.add_image.bind(this)}>Ajouter une image</a>
                <a className="btn" onClick={this.add_images.bind(this)}>Ajouter des images</a>
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