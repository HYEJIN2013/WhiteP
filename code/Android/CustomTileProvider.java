import android.content.res.AssetManager;
import android.graphics.Rect;
import android.util.SparseArray;

import com.google.android.gms.maps.model.Tile;
import com.google.android.gms.maps.model.TileProvider;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;

public class CustomMapTileProvider implements TileProvider {
    private static final int TILE_WIDTH = 256;
    private static final int TILE_HEIGHT = 256;
    private static final int BUFFER_SIZE = 16 * 1024;

    private static final SparseArray<Rect> TILE_ZOOMS = new SparseArray<Rect>() {{
        put(10, new Rect(487, 382, 487, 383));
        put(11, new Rect(974, 765, 975, 767));
        put(12, new Rect(1948, 1531, 1950, 1534));
        put(13, new Rect(3897, 3063, 3901, 3068));
        put(14, new Rect(7794, 6126, 7802, 6136));
        put(15, new Rect(15589, 12253, 15604, 12272));
        put(16, new Rect(31178, 24506, 31208, 24544));
        put(17, new Rect(62357, 49012, 62417, 49089));
    }};

    private AssetManager mAssets;

    public CustomMapTileProvider(AssetManager assets) {
        mAssets = assets;
    }

    @Override
    public Tile getTile(int x, int y, int zoom) {

        if (hasTile(x, y, zoom)) {
            byte[] image = readTileImage(x, y, zoom);
            return image == null ? null : new Tile(TILE_WIDTH, TILE_HEIGHT, image);
        } else {
            return NO_TILE;
        }
    }

    private boolean hasTile(int x, int y, int zoom) {
        Rect b = TILE_ZOOMS.get(zoom);
        return b != null && (b.left <= x && x <= b.right && b.top <= y && y <= b.bottom);
    }



    private byte[] readTileImage(int x, int y, int zoom) {
        InputStream in = null;
        ByteArrayOutputStream buffer = null;

        try {
            in = mAssets.open(getTileFilename(x, y, zoom));
            buffer = new ByteArrayOutputStream();

            int nRead;
            byte[] data = new byte[BUFFER_SIZE];

            while ((nRead = in.read(data, 0, BUFFER_SIZE)) != -1) {
                buffer.write(data, 0, nRead);
            }
            buffer.flush();

            return buffer.toByteArray();
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        } catch (OutOfMemoryError e) {
            e.printStackTrace();
            return null;
        } finally {
            if (in != null) try { in.close(); } catch (Exception ignored) {}
            if (buffer != null) try { buffer.close(); } catch (Exception ignored) {}
        }
    }

    private String getTileFilename(int x, int y, int zoom) {
        return "tiles" + "/" + zoom + '/' + x + '/' + y + ".png";
    }
}
