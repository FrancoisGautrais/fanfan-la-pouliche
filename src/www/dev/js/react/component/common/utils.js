
function _assign(x, y){
    for(var key in y){
        if(x[key]!=undefined && x[key].constructor == Object && y[key] && y[key].constructor == Object){
            _assign(x[key], y[key]);
        }else if(y[key]!=undefined){
            x[key] = y[key];
        }
    }
}

function assign(x, ...args){
    for(var i in args){
        _assign(x, args[i]);
    }
    return x;
}

var default_key_fct = e => e.props.id;
class Stack {
    constructor(x=null){
        this.data=x?x:[]
    }

    length(){
        return this.data.length;
    }

    is_empty(){
        return !this.data.length;
    }

    at(i){
        var len = this.data.length;
        i=i%len;
        i=(i<0)?(len+i):(i);
        return this.data[i];
    }

    push(x){
        this.data.push(x)
        return this;
    }

    as_array(){
        return this.data;
    }

    pop(){
        return this.data.pop();
    }

    remove(data, key=default_key_fct){
        var d=this.data
        for(var i in this.data){
            if(key(d[i]) == data){
                this.data=d.slice(0, i).concat(d.slice(parseInt(i)+1, d.length));
            }
        }
        return this;
    }
}

module.exports = {
    new_id: function(){
        return Math.random().toString(36).substr(2, 8)+Math.random().toString(36).substr(2, 8)+Math.random().toString(36).substr(2, 8);
    },

    react_append: function(elem, root_id){
        var root = $("<div></div>")
        $(root_id).append(root)
        var data = ReactDOM.render(elem, root[0]);
    },
    Queue : module.load(".queue"),
    assign: assign,

    Stack: Stack,

    RawHTML : ({children, className = ""}) =>
        <div className={className} id="----"
          dangerouslySetInnerHTML={{ __html: children}} />

}


