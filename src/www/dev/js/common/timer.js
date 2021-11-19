
class Timer {
    constructor(func, data=null, t=100, start=false){
        this.func=func;
        this.data=data;
        this.started=false;
        this.time = t;
        if(start) this.start()
    }

    start(){
        this.started=true;
        this.run()
    }

    run(){
        var self = this;
        if(this.started){
            if(this.func) this.func(this.data)
            setTimeout(function(){self.run();}, self.time)
        }
    }

    stop(){
        this.started=false;
    }
}

class _TimerManager {

    constructor(){
        this.timers={}
    }

    add(func, data, time=100, start=true){
        var id = Math.random().toString(36).substr(2, 8)+Math.random().toString(36).substr(2, 8)+Math.random().toString(36).substr(2, 8);
        this.timers[id]=new Timer(func, data, time, start)
        return id;
    }

    start(id){
        var x = this.timers[id]
        if(!x) return
        x.start()
    }

    stop(id, remove=true){
        var x = this.timers[id]
        if(!x){
            return
        }
        x.stop()
        if(remove)
            delete this.timers[id]
    }
}

var TimerManager = new _TimerManager()
