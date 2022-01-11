
class CQEntry {
    constructor(fct, ...args){
        this.fct=fct;
        this.args=args;
    }

    call(...args){
        this.fct(...this.args, ...args);
    }

}

class CallbackQueue {
    constructor(){
        this.queue=[]
        this.started=false;
    }

    enqueue(fct, ...args){
        this.queue.push(new CQEntry(fct, ...args));
    }

    next(...args){
        if(this.queue.length>0) {
            var current = this.queue[0];
            this.queue = this.queue.slice(1, this.queue.length);
            this.started=true;
            current.call(...args);
        }
        else {
            this.started=false;
        }
    }

    call(...args){
        if(!this.started){
            this.next(...args);
        }
    }

    length(){
        return this.queue.length;
    }

}

module.exports=CallbackQueue;