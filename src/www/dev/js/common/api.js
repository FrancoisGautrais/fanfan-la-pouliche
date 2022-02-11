var Toast = module.load("js.react.component.ui.toast");
var modal = module.load("js.react.component.ui.modal")


function _complete_wrapper(func){
    return function(data){
        if(func) func(data.target.responseText)
    }
}

function _error_wrapper(func){
    return function(data){
        if(func) func(data)
    }
}

function _json__http_error_wrapper(fct){
    return function(data){
        if(!fct){

            Toast.error(data);
        }
    }
}
const regex = /<body>(?<content>.*)<\/body>/gm;
function _json_error_wrapper(fct, error_http, opts){
    return function(data, x, y){
        var is_http_error = false;
        var json_data = null;
        try{
            json_data = JSON.parse(data.responseText);
        }catch(e){
            if(e instanceof SyntaxError){
                is_http_error=true;
            }else{
                throw e;
            }

        }
        if(is_http_error){
            if(error_http){
                if(typeof error_http === "function"){
                    error_http(data);
                }else if(error_http == "modal"){
                    var text = data.responseText.replaceAll("\n", "");
                    var content = regex.exec(text)
                    modal.error("Erreur HTTP:<br>"+content[0]);
                }else if(error_http == "toast"){
                    var text = data.responseText.replaceAll("\n", "");
                    var content = regex.exec(text)
                    Toast.error("Erreur HTTP:<br>"+content[0]);
                }else{
                    throw "Parametre d'erreur http incomprehnsible"+error_http
                }

            } else { // default handling
                var text = data.responseText.replaceAll("\n", "");
                var content = regex.exec(text)
                modal.error_html("Erreur HTTP:<br>"+content[0]);
            }
        }else{
            if(fct){
                fct(json_data);
            }else{
                var err="<br>Code: "+json_data.code+"<br>Message: "+json_data.message+"<br>Data:"+json_data.data;
                modal.error_html("Erreur sur '"+opts.url+"' "+err);
            }
        }
        console.log("ERROR=", data, x, y)

    }
}

function _json_success_wrapper(fct, opts){
    return function(data, x, y, z){
        if(fct)fct(data.data);
    }
}

function _json_to_urlencoded(data){
    return Object.entries(data).map(e => e.join('=')).join('&');
}

class ApiBase {
    constructor(){}

    send_form_data(method, path, data, opts){
        if(typeof opts === "function") opts={success: opts}
        opts = Object.assign({
            method: method,
            headers: null,
            success: null,
            error: null,
            abort: null,
            update: null
        }, opts)
        var formData = new FormData();
        var request = new XMLHttpRequest();
        for(var key in data){
            formData.append(key, data[key])
        }
        request.addEventListener("loadend", _complete_wrapper(opts.success))
        request.addEventListener("error", _error_wrapper(opts.error))
        request.addEventListener("abort", _error_wrapper(opts.abort?opts.abort:opts.error))
        request.upload.onprogress=function(x){
           if(opts.update){
                opts.update(x.loaded, x.total, x)
           }
        }
        request.open(method, path);
        request.send(formData);

        return request
    }



    _ajax(ajax, is_json){
        ajax=Object.assign({
            headers: {},
            method: "GET"
        },
        ajax)
        return $.ajax(ajax)
    }

    _ajx_url(url, opts, is_json){
        opts.url=url;
        return this._ajax(opts, is_json);
    }

    _json(method, url, data, opts){
        var is_get = (method.toLowerCase()=="get");
        if(typeof opts === 'function') opts={success: opts}
        var def_args = {
            method: method,
            url: url+((is_get&&data)?("?"+_json_to_urlencoded(data)):""),
            data: is_get?null:JSON.stringify(data),
            headers: {
                "Content-Type" : "application/json"
            }
        }
        opts.success=_json_success_wrapper(opts.success, def_args);
        opts.error=_json_error_wrapper(opts.error, opts.error_http, def_args);
        opts=Object.assign(def_args, opts)
        print(opts)
        return this._ajx_url(url, opts, true);
    }

    json_get(url, data={}, opts={}){
        return this._json("GET", url, data, opts)
    }
    json_post(url, data={}, opts={}){
        return this._json("POST", url, data, opts)
    }
    json_put(url, data={}, opts={}){
        return this._json("PUT", url, data, opts)
    }
    json_delete(url, data={}, opts={}){
        return this._json("DELETE", url, data, opts)
    }


}


module.exports={
    Api: ApiBase,
    Request: Request
};


