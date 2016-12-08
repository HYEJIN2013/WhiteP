public class ChatInput extends Component {

    @Inject
    private ChatService service;

    @Remoted
    public void addMessage(String msg) {
        service.addMessage(msg);
        refresh();
    }

    @ScriptElement
    public Script init() {
    	return new ComponentFunctionCall(this, "init");
    }
}
