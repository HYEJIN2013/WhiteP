import java.util.Calendar;

public class MonthlyCalendar {
	private int year;
	private int month;
	private int[][] calendarMatrix = new int[6][7];
	private int startDay;
	private int lastDate;

	/**
	 * カレンダー表オブジェクトを作成します。
	 * 
	 * @param year
	 *            西暦年(..., 2005, 2006, 2007, ...)
	 * @param month
	 *            月(1, 2, 3, ..., 10, 11, 12)
	 */
	public MonthlyCalendar(int year, int month) {
		this.year = year;
		this.month = month;
		calcFields();
	}

	private void calcFields() {
		Calendar calendar = Calendar.getInstance();
		calendar.clear();
		// 月の初めの曜日を求めます。
		calendar.set(year, month - 1, 1); // 引数: 1月: 0, 2月: 1, ...
		startDay = calendar.get(Calendar.DAY_OF_WEEK); // DAY_OF_WEEK: 曜日
		// 月末の日付を求めます。
		calendar.add(Calendar.MONTH, 1);
		calendar.add(Calendar.DATE, -1);
		lastDate = calendar.get(Calendar.DATE);
		// カレンダー表を作成します。
		int row = 0;
		int column = startDay - 1; // startDay: 日曜日 = 1, 月曜日 = 2, ...
		for (int date = 1; date <= lastDate; date++) {
			calendarMatrix[row][column] = date;
			if (column == 6) {
				row++;
				column = 0;
			} else {
				column++;
			}
		}
	}

	@Override
	public String toString() {
		StringBuffer sb = new StringBuffer();
		loop: for (int i = 0; i < calendarMatrix.length; i++) {
			for (int j = 0; j < calendarMatrix[i].length; j++) {
				int day = calendarMatrix[i][j];
				if (day == 0) {
					if (i != 0) {
						// カレンダー表内の月末以降のセルに到達
						break loop;
					}
					sb.append("   ");
				} else if (day < 10) {
					sb.append("  ").append(day);
				} else {
					sb.append(" ").append(day);
				}
			}
			sb.append("\r\n");
		}
		return sb.toString();
	}

	public static void main(String[] args) {
		int currentYear = Calendar.getInstance().get(Calendar.YEAR);
		for (int month = 1; month <= 12; month++) {
			System.out.println("--------");
			System.out.println(currentYear + "年" + month + "月");
			System.out.println(new MonthlyCalendar(currentYear, month));
		}
	}
}
