
window.print = console.log

function _assign(x, y){
    for(var key in y){
        if(x[key]!=undefined && x[key].constructor == Object && y[key] && y[key].constructor == Object){
            _assign(x[key], y[key]);
        }else{
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

module.exports={
    new_id: function(){
        return Math.random().toString(36).substr(2, 8)+Math.random().toString(36).substr(2, 8)+Math.random().toString(36).substr(2, 8);
    },

    react_append: function(elem, root_id){
        var root = $("<div></div>")
        $(root_id).append(root)
        var data = ReactDOM.render(elem, root[0]);
    },

    assign: assign,

    RawHTML : ({children, className = ""}) =>
        <div className={className}
          dangerouslySetInnerHTML={{ __html: children}} />

}