var { Api } = module.load("js.common.api")

class _Images extends Api{
    constructor(){
        super();
    }

    create(form, handlers) {
        return this.send_form_data("POST", "/image/add", form, handlers)
    }

    edit(form, handlers) {
        return this.json_post("/image/"+form.uuid, form, handlers)
    }

    remove(uuid, handlers) {
        return this.json_delete("/image/"+uuid, null, handlers)
    }

    info(uuid, handlers) {
        return this.json_get("/image/"+uuid+"/info", null, handlers)
    }

    list(handlers) {
        return this.json_get("/image", null, handlers)
    }


}

var images = new _Images();
module.exports=images;