

class Throwable {
    constructor(type, message, ...data){
        this.type=type;
        this.trace=console.trace();
        this.name = this.constructor.name;
        this.message = message;
        this.data=data;
    }
}

class Interruption extends Throwable{
    constructor(message, ...data){
        super("interruption", message, ...data);
    }
}

class Exception extends Throwable{
    constructor(message, ...data){
        super("exception", message, ...data);
    }
    toString(){ return this.name+": "+message+" "; }
}

class ImportException extends Exception {
    constructor(path, ...data){
        super("Unable to import '"+path+"' ", ...data)
    }
}

class _Module {

    constructor(path=null, init=true){
        this.path = path?path:"";
        this.name = this.path.split('.').slice(-1)[0]
        this.exports={ __module__: this}
        if(this.path && init)
            this._prepare_export()
    }

    toString(){ return "Module "+this.path; }

    root() {
        return window["Module"];
    }

    resolve(path, src=null, as_string=true) {
        if(path[0]==".") path=(this.path+"."+path)
        src=((src)?src:path).split(".");
        var liste = path.split('.');
        var out = (liste.length && liste[0]!="")?[liste[0]]:liste;
        for(var i=1; i<liste.length; i++){
            if(liste[i]==""){
                out.pop();
            }else{
                out.push(liste[i]);
            }
        }
        return as_string?out.join("."):out
    }

    load(path){
        path = this.resolve(path, null, false);
        var curr = this.root();
        var as_str = "";

        for(var i in path){
            var attr = path[i];
            as_str = (as_str.length)?(as_str+"."+attr):attr;
            if(attr=="*") {
                return curr.exports;
            }
            if(curr.exports[attr]==undefined){
                throw new ImportException(as_str);
            }
            curr=curr.exports[attr];
        }

        return curr.exports;
    }

    _prepare_export(){
        var curr = this.root();
        var path = null;
        var path_array = this.path.split('.')
        for(var i in path_array){
            var name = path_array[i];
            path = (path)?(path+"."+name):name;
            if(i==path_array.length-1){
                curr.exports[name]=this;
            }else{
                 if(curr.exports[name]==undefined){
                    curr.exports[name]=new _Module(path, false, this);
                }
                curr=curr.exports[name];
            }
        }
    }

    register(name){
        var ret = new _Module(name)
        return ret
    }
}

window["Module"]=new _Module(null, false);
window["global"]={};
window["print"] = console.log;
