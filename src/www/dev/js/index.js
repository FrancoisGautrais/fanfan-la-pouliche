module.load(".third-party.*")
module.load(".react.*")
module.load(".react.component.ui.widget.*")
var tools = module.load("js.react.tools")
var modal = module.load("js.app.ui.modal.modal")
var model = module.load("js.app.model.*")
var tag = module.load("js.app.ui.form.tag")

var print = console.log;


function on_post(){
    var data = {}
    $("[name^=data-]").each( function(i,e){
        e=$(e)
        data[e.attr("name").substr(5)] = e.val()
    })
}
