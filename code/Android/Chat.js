Chat = Component.extend({
    init : function(id) {
      this._super(id);
      var self = this;
      setTimeout(function() { self.checkMessages() }, 1000);
    },
    checkMessages : function() {
      this.call("checkMessages")();  
    }
});

ChatInput = Component.extend({
  init : function(id) {
    var self = this;
    this._super(id);
    this.attach();
  },
  attach : function() {
    var self = this;
    this.el("newmsg").keypress(function(e) { 
      if(e.which==13) {
        e.preventDefault();
        self.addMessage();
      }
    });
    this.el("button").click(function() { 
      self.addMessage() 
    });
  },
  addMessage : function() {
    var self = this;
    var msg = this.el("newmsg");
    this.call("addMessage", null, function() {
      self.el("newmsg").focus();
    })(msg.val());
  }
});