module.load("js.third-party.*")
module.load("js.react.*")
module.load("js.react.component.ui.widget.*")
var tools = module.load("js.react.tools")
var modal = module.load("js.react.component.ui.modal")
var model = module.load("js.app.model.*")
var tag = module.load("js.app.ui.form.tag")
var {TagManage} = module.load("js.app.ui.modal.tag")
var {ImagesListModal, SimpleImage} = module.load("js.app.ui.modal.image")
var Page = module.load("js.react.component.ui.page")
var print = console.log;


function show(name){
    if(name == "images"){
        modal.modal(ImagesListModal())
    }else if(name == "tags"){
        modal.modal(TagManage())
    }else if(name == "add_image"){
        modal.modal(SimpleImage())
    }else if(name == "add_images"){
        modal.modal(SimpleImage())
    }
}

window.show=show;