
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



modal.modal(SimpleImage())

module.exports={
    SimpleImage: SimpleImage
}