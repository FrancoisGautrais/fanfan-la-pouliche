
module.load(".timer")
module.load("js.app.model.api")
function complete_wrapper(func){
    return function(data){
        if(func) func(data.loaded, data.total, data)
    }
}

function error_wrapper(func){
    return function(data){
        if(func) func(data)
    }
}

class Api {
    constructor(){

    }


    image_create(form, complete=null, update=null, error=null) {
        var formData = new FormData();
        var self = this;
        form.find("[name]").each(function(i,e){
            var je=$(e)
            var tag = e.tagName;
            var type = je.attr("type")
            var name = je.attr("name")
            if(tag=="INPUT"){
                if(type=="file")
                    formData.append(name, e.files[0])
                else
                    formData.append(name, je.val())
            }

        })


        var request = new XMLHttpRequest();
        request.addEventListener("loadend", complete_wrapper(complete))
        request.addEventListener("error", error_wrapper(error))
        request.addEventListener("abort", error_wrapper(null))
        request.upload.onprogress=function(x){
           if(update){
                update(x.loaded, x.total, x)
           }
        }
        request.open("POST", "/image/add");
        request.send(formData);
        return request
    }

    image_create_x(form, complete=null, update=null, error=null) {
        var formData = new FormData();
        var self = this;
        for(var key in form){
            formData.append(key, form[key])
        }

        var request = new XMLHttpRequest();
        request.addEventListener("loadend", complete_wrapper(complete))
        request.addEventListener("error", error_wrapper(error))
        request.addEventListener("abort", error_wrapper(null))
        request.upload.onprogress=function(x){
           if(update){
                update(x.loaded, x.total, x)
           }
        }
        request.open("POST", "/image/add");
        request.send(formData);
        return request
    }

    image_list(){

    }
}



module.exports={
    api: new Api()
}