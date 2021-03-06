
var taost = module.load("js.react.component.ui.toast")
var modal = module.load("js.react.component.ui.modal")
var image = module.load("js.app.ui.form.image")
var shortcut = module.load("js.app.ui.modal.shortcut")

function SimpleImage(onsend){
    var attrs = {
        title: "Ajouter une image",
        form: image.SimpleImageForm,
        onsend: onsend
    }
    return (<shortcut.ModalForm {...attrs}/>)
}

function SimpleImageEdit(value, onsend, is_tag){
    var attrs = {
        title: "Modifier une image",
        form: image.SimpleImageEditForm,
        form_attr : {
            is_tag: is_tag
        },
        onsend: function(data){
            if(onsend) onsend(data);
            return true;
        },
        value: value
    }
    return (<shortcut.ModalForm {...attrs}/>)
}


window.SimpleImageEditModal=function(props, onsend, is_tag){ return modal.modal(SimpleImageEdit(props, onsend, is_tag))}

function MultipleImage(onsend){
    var attrs = {
        title: "Ajouter des images",
        form: image.MultipleImageForm,
        modal: {
            size: "l"
        },
        onsend: onsend
    }
    return (<shortcut.ModalForm {...attrs}/>)
}

function ImagesListModal(onsend){

    var attrs = {
        title: "Images",
        form: image.ImageList,
        modal: {
            size: "l"
        },
        onsend: onsend,

    }
    return (<shortcut.ModalForm {...attrs}/>)
}



//modal.modal(SimpleImage())
//modal.modal(MultipleImage())
//modal.modal(ImagesListModal())
window.SimpleImage = SimpleImage;
window.MultipleImage = MultipleImage;

module.exports={
    SimpleImage: SimpleImage,
    SimpleImageEdit: SimpleImageEdit,
    ImagesListModal : ImagesListModal,
    MultipleImage : MultipleImage
}