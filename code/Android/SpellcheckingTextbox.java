package springcraft.spellchecker;

import java.awt.Point;
import java.util.ArrayList;
import java.util.List;
import java.util.Vector;

import net.minecraft.client.Minecraft;
import net.minecraft.src.FontRenderer;
import net.minecraft.src.GuiTextField;

import com.inet.jortho.SpellChecker;

public class SpellcheckingTextbox extends GuiTextField {

	int x;
	int y;

	public SpellcheckingTextbox(FontRenderer par1FontRenderer, int par2, int par3, int par4, int par5) {
		super(par1FontRenderer, par2, par3, par4, par5);
		x = par2;
		y = par3;
	}

	public void renderSpellchecking() {
		FontRenderer renderer = Minecraft.getMinecraft().fontRenderer;
		StringAndPoint[] snps = spellCheck(getText(), renderer, y);
		for (StringAndPoint snp : snps)
			renderer.drawStringWithShadow(snp.string, snp.point.x + x, snp.point.y, 0xFFFFFF);
	}

	@Override
	public void drawTextBox() {
		super.drawTextBox();
		renderSpellchecking();
	}

	public StringAndPoint[] spellCheck(String str, FontRenderer renderer, int height) {
		Vector<StringAndPoint> strings = new Vector();
		String str1 = str.toLowerCase();
		int i = 0;
		int lastSpace = 0;
		for (char c : str1.toCharArray()) {
			if (c == ' ' || i == str1.length() - 1) {
				if (i == str1.length() - 1) ++i;
				String allBefore = str.substring(0, lastSpace);
				strings.add(new StringAndPoint(str.substring(lastSpace, i), new Point(renderer.getStringWidth(allBefore), height)));
				lastSpace = i + 1;
			}
			++i;
		}
		int j = 0;
		for (StringAndPoint s : strings) {
			String parsed = parseToBeRead(s.string);
			if (parsed.length() > 1 && !SpellChecker.getCurrentDictionary().exist(parsed)) strings.set(j, new StringAndPoint("§c" + s.string, s.point));
			++j;
		}

		return strings.toArray(new StringAndPoint[strings.size()]);
	}

	String validValues = "qwertyuiopasdfghjklzxcvbnm-'";

	public String parseToBeRead(String s) {
		List<Character> valid = new ArrayList();
		for (char c : validValues.toCharArray())
			valid.add(Character.valueOf(c));
				StringBuffer buffer = new StringBuffer();
				new Vector();
				for (char c : s.toCharArray())
					if (valid.contains(c)) buffer.append(Character.toLowerCase(c));
						return buffer.toString();
	}

	public class StringAndPoint {

		public final String string;
		public final Point point;

		public StringAndPoint(String string, Point point) {
			this.string = string;
			this.point = point;
		}
	}

}
