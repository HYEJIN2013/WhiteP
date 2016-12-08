public class Chat extends Component implements ChatServiceClient {

    @Inject
    private ChatService service;
    
    private long lastAccess = -1;
    
    @Element
    public List<ChatMsg> messages() {
    	return service.getMessages();
    }
    
    @AfterBuild
    public void afterBuild() {
        lastAccess = service.getLastAccess();
    }
    
    @Attribute
    public boolean changed() {
    	return service.getLastAccess() > lastAccess;
    }
    
    @Remoted
    @Delayed(ChatService.class)
    public void checkMessages() {
        System.out.println("Checking messages");
        refresh();
    }
    
    @ScriptElement(onCreate=false)
    public Script jsUpdate() {
      return new JsUpdate(this, "checkMessages");
    }
    
    @ScriptElement(onUpdate=false)
    public Script jsInit() {
    	return new JsInit(this);
    }
}