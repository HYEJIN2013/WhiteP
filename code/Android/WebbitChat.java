package co.ntier.pg.webbit;

import java.io.IOException;
import java.util.HashSet;
import java.util.Set;

import org.webbitserver.WebServer;
import org.webbitserver.WebSocketConnection;
import org.webbitserver.WebSocketHandler;
import org.webbitserver.handler.StaticFileHandler;
import org.webbitserver.handler.logging.LoggingHandler;
import org.webbitserver.handler.logging.SimpleLogSink;
import org.webbitserver.netty.NettyWebServer;

public class WebbitChat {
  public static void main(String[] args) throws IOException {
		WebServer server = new NettyWebServer(8080);
		server.add(new LoggingHandler(new SimpleLogSink()));
		server.add(new StaticFileHandler("src/main/resources/web"));
		server.add("/chat", new WebSocketHandler() {
			public Set<WebSocketConnection> connections = new HashSet<WebSocketConnection>();

			public void onOpen(WebSocketConnection connection) throws Exception {
				connections.add(connection);
			}

			public void onClose(WebSocketConnection connection)
					throws Exception {
				connections.remove(connection);
			}

			public void onMessage(WebSocketConnection connection, String msg)
					throws Throwable {
				for (WebSocketConnection ws : connections) {
					ws.send(msg);
				}
			}

			public void onMessage(WebSocketConnection connection, byte[] msg)
					throws Throwable {
				throw new UnsupportedOperationException();
			}

			public void onPing(WebSocketConnection connection, byte[] msg)
					throws Throwable {
				throw new UnsupportedOperationException();
			}

			public void onPong(WebSocketConnection connection, byte[] msg)
					throws Throwable {
				throw new UnsupportedOperationException();
			}
		});

		server.start();
	}
}