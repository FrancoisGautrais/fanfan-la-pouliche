
var taost = module.load("js.react.component.ui.toast")
var modal = module.load("js.react.component.ui.modal")
var tag = module.load("js.app.ui.form.tag")
var shortcut = module.load("js.app.ui.modal.shortcut")

function TagEdit(value, onsend){
    var attrs = {
        title: "Editer le tag '"+tag.name+"'",
        form: tag.TagAddForm,
        onsend: onsend,
        value: value
    }
    return (<shortcut.ModalForm {...attrs}/>)
}

function TagCreate(onsend){
    var attrs = {
        title: "Créer un tag",
        form: tag.TagAddForm,
        onsend: onsend
    }
    return (<shortcut.ModalForm {...attrs}/>)
}


module.exports={
    TagEdit: TagEdit,
    TagCreate: TagCreate
}