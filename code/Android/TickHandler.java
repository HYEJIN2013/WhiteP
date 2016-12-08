package springcraft.spellchecker;

import java.util.EnumSet;

import net.minecraft.client.Minecraft;
import net.minecraft.src.GuiChat;
import net.minecraft.src.GuiScreen;
import cpw.mods.fml.common.ITickHandler;
import cpw.mods.fml.common.TickType;
import cpw.mods.fml.relauncher.ReflectionHelper;

public class TickHandler implements ITickHandler {

	public static final TickHandler INSTANCE = new TickHandler();

	volatile static boolean ticked = false;
	private static final int TEXTBOX_INDEX = 7;

	// Make consctructor not be visible.
	private TickHandler() {
	};

	@Override
	public void tickStart(EnumSet<TickType> type, Object... tickData) {
	}

	@Override
	public void tickEnd(EnumSet<TickType> type, Object... tickData) {
		Minecraft mc = Minecraft.getMinecraft();
		GuiScreen screen = mc.currentScreen;
		if (screen != null && screen instanceof GuiChat) {
			if (!ticked) {
				ticked = true;
				GuiChat chatGui = (GuiChat) screen;
				SpellcheckingTextbox box = new SpellcheckingTextbox(mc.fontRenderer, 4, chatGui.height - 12, chatGui.width - 4, 12);
				box.setMaxStringLength(100);
				box.setEnableBackgroundDrawing(false);
				box.setFocused(true);
				box.setText("");
				box.setCanLoseFocus(false);
				ReflectionHelper.setPrivateValue(GuiChat.class, chatGui, box, TEXTBOX_INDEX);
			}
		} else ticked = false;
	}

	@Override
	public EnumSet<TickType> ticks() {
		return EnumSet.of(TickType.CLIENT);
	}

	@Override
	public String getLabel() {
		return "Spellchecker";
	}

}
