package springcraft.spellchecker;

import java.net.MalformedURLException;

import net.minecraft.client.Minecraft;

import com.inet.jortho.SpellChecker;

import cpw.mods.fml.common.Mod;
import cpw.mods.fml.common.Mod.Init;
import cpw.mods.fml.common.Side;
import cpw.mods.fml.common.event.FMLInitializationEvent;
import cpw.mods.fml.common.registry.TickRegistry;

@Mod(modid = "sc_Spellchecker", version = "[1.0] for 1.3.2")
public class mod_Spellchecker {

	@Init
	public void init(FMLInitializationEvent event) {
		try {
			SpellChecker.registerDictionaries(Minecraft.getAppDir("minecraft/dict").toURI().toURL(), "en");
		} catch (MalformedURLException e) {
			e.printStackTrace();
		}
		TickRegistry.registerTickHandler(TickHandler.INSTANCE, Side.CLIENT);
	}

}
