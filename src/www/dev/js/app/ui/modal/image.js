
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

function SimpleImageEdit(value, onsend){
    var attrs = {
        title: "Modifier une image",
        form: image.SimpleImageEditForm,
        onsend: function(data){
            if(onsend) onsend(data);
            return true;
        },
        value: value
    }
    return (<shortcut.ModalForm {...attrs}/>)
}


window.SimpleImageEditModal=function(props, onsend){ return modal.modal(SimpleImageEdit(props, onsend))}

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



modal.modal(SimpleImage())
modal.modal(ImagesListModal())

module.exports={
    SimpleImage: SimpleImage,
    SimpleImageEdit: SimpleImageEdit,
    ImagesListModal : ImagesListModal
}