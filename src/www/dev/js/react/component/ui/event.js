
class EventEntry {
    constructor(id, type, callback, opts){
        this.id = id;
        this.type = type;
        this.callback = callback;
        this.opts=opts;
    }

    on_event(e, type){
        if(type!=this.type) return;
        return this["handle_"+type](e)
    }
}

class EventEntryClick extends EventEntry{
    handle_click(e){
        var elem = (typeof this.opts.element === 'function')?this.opts.element():this.opts.element
        if(elem==null){return}
        var val = elem.contains(e.target)
        return (this.opts.outside!=val)?this.callback():null;
    }
}


class EventEntryKeyUp extends EventEntry{
    handle_keyup(e){
        var val = this.opts.element.contains(e.target)
        return this.opts.outside!=val;
    }
}

class _Event {
    constructor(){
        this.listeners={}
        document.addEventListener('click', this.onclick.bind(this));
        document.addEventListener('keyup', this.onkeyup.bind(this));
    }

    onclick(e){
        for(var key in this.listeners){
            this.listeners[key].on_event(e, "click")
        }
    }

    onkeyup(e){
        for(var key in this.listeners.keyup){
            this.listeners[key].on_event(e, "keyup")
        }
    }

    remove(id){
        delete this.listeners[id];
    }

    addOnClickOutside(id, e, fct){
        this.listeners[id]= new EventEntryClick(id, "click", fct, { outside: true, element: e})
    }

    addOnKeyUp(id, key, fct){
        this.listeners[id]= new EventEntryKeyUp(id, "keyup", fct, { key: key})
    }
}

module.exports = new _Event();