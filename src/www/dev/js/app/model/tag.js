var { Api } = module.load("js.common.api")
var utils =  module.load("js.react.component.common.utils")


class _Tag extends Api{
    constructor(){
        super();
        this.tags=null;
        this.init(DATA.tags);
    }

    init(tags){
        this.tags=tags;
    }

    update(){
        var self = this;
        this.json_get("/tag/enumerate", null, this.init.bind(this));
    }

    create(data, handlers=null){
        var self = this;
        handlers=this.set_handler(handlers, function(d){
            self.tags[d.uuid]=d;
        });
        this.json_post("/tag/add", data, handlers);
    }

    edit(data, handlers){
        if(!data.uuid){
            throw "Erreur il faut un uuid pour editer le tag : "
        }
        var self = this;
        handlers=this.set_handler(handlers, function(d){
            self.tags[d.uuid]=d;
        });
        this.json_post("/tag/"+data.uuid+"/", data, handlers);
    }

    set_handler(handler, fct){
        if(typeof fct === "function") handler={success: handler}
        if(!handler) handler={}
        var tmp = handler.success;
        handler.success = function(d){
            if(fct) fct(d);
            if(tmp){
                tmp(d);
            }
        }
        return handler;
    }

    remove(id, handlers=null){
        var self = this;
        handlers=this.set_handler(handlers, function(){
            delete self.tags[id]}
        )
        this.json_get("/tag/"+id+"/remove", null, handlers);
    }

    list(){
        return this.tags;
    }

    select_list(){

        return this.tags;
    }


    tree(){
        var out = utils.assign({}, this.tags)
        Object.keys(out).map((e,i) => out[e].children=[])
        for(var i in out){
            var node = out[i], parent= out[out[i].parent];
            if(parent){
                parent.children.push(node)
            }
        }
        for(var i in out){
            if(out[i].parent){
                out[i]=null
                delete out[i]
            }

        }
        return out
    }
}


var tags = new _Tag();


window.tags=tags;
module.exports=tags;