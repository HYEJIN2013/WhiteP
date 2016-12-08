@Singleton
public class ChatService implements DelayedUpdateHandler<ChatServiceClient>, Runnable {

    private final LinkedList<ChatMsg> messages = new LinkedList<ChatMsg>();

    private final static long expiration = 1000 * 25;

    private long lastAccess = System.currentTimeMillis();

    private final Set<Continuation> continuations = new HashSet<Continuation>();

    private ScheduledThreadPoolExecutor invoker = new ScheduledThreadPoolExecutor(1);

    public List<ChatMsg> getMessages() {
        return Collections.unmodifiableList(messages);
    }

    private void schedule(ChatMsg msg) {
        invoker.schedule(this, msg.getExpires().getMillis() - System.currentTimeMillis(),
                TimeUnit.MILLISECONDS);
    }

    public void addMessage(String value) {

        ChatMsg msg = new ChatMsg(
                new DateTime(System.currentTimeMillis()),
                new DateTime(System.currentTimeMillis() + expiration),
                value);

        synchronized (continuations) {

            if (messages.size() > 9) {
                invoker.remove(this);
                messages.removeFirst();
            }
            messages.add(msg);
            schedule(messages.getFirst());
            notifyChats();
        }

    }

    private void notifyChats() {
        lastAccess = System.currentTimeMillis();

        synchronized (continuations) {  
            Iterator<Continuation> iter = continuations.iterator();
            while (iter.hasNext()) {
                // System.out.println("Has next");

                try {
                    iter.next().resume();
                } catch (Exception e) {
                    // Just swallow it
                } finally {
                    iter.remove();
                }
            }
        }
    }

    @Override
    public boolean isUpdateDelayed(ChatServiceClient chat, HttpServletRequest request) {

        Continuation continuation = ContinuationSupport
                .getContinuation(request);
        synchronized (continuations) {
            if (continuations.contains(continuation)) {
                continuations.remove(continuation);
                return false;
            } else {
                if (chat.changed()) {
                    return false;
                } else {
                    continuations.add(continuation);
                    continuation.suspend();
                    return true;
                }
            }
        }
    }

    public long getLastAccess() {
        return lastAccess;
    }

    @Override
    public void run() {
        synchronized (continuations) {
            if (messages.size() > 0) {
                while (messages.size() > 0
                        && messages.getFirst().getExpires().getMillis() <= System
                                .currentTimeMillis()) {
                    messages.removeFirst();
                }
                notifyChats();
            }
            if (messages.size() > 0) {
                schedule(messages.getFirst());
            }
        }
    }
}
