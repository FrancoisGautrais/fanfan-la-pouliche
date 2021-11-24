var { Api } = module.load("js.common.api")

class _Images extends Api{
    constructor(){
        super();
    }

    create(form, handlers) {
        return this.send_form_data("POST", "/image/add", form, handlers)
    }

    edit(form, handlers) {
        return this.send_form_data("POST", "/image/"+form.uuid+"/", form, handlers)
    }

    remove(uuid, handlers) {
        return this.json_delete("/"+uuid, null, handlers)
    }
    info(uuid, handlers) {
        return this.json_get("/"+uuid+"/info", null, handlers)
    }


}

var images = new _Images();
module.exports=images;