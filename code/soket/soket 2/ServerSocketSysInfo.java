package homework11.serverSysInfo;

import java.io.IOException;
import java.net.*;

public class ServerSocketSysInfo {

	private static String printSysInfo() {

		int procInfo = Runtime.getRuntime().availableProcessors();
		long totalMemInfo = Runtime.getRuntime().totalMemory();
		long freeMemInfo = Runtime.getRuntime().freeMemory();

		String sysInfo = "<br> Available Processors: " + procInfo + "<br> Total Memory: " + totalMemInfo
				+ "<br> Free Memory: " + freeMemInfo;

		return sysInfo;
	}

	public static void answer() {

		try (ServerSocket servSocket = new ServerSocket(8080)) {
			for (int i = 0;; i++) {
				Socket clientSoket = servSocket.accept();
				Client client = new Client(clientSoket, "Request #" + i + printSysInfo());
			}
		} catch (IOException e) {
			System.err.println("Unable to open Server socket!");
		}

	}
}
