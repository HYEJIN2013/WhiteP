public class SplashActivity extends AppCompatActivity {
  
  @Override
  protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.activity_splash);
    
    if (mLastSyncTimestamp == Constants.INITIAL_TIMESTAMP) {
      initGoogleMap();
    }
  }
    
  private void initGoogleMap() {
  
    // Do a null check to confirm that we have not already instantiated the map.
    if (mMap == null) {
        // Try to obtain the map from the SupportMapFragment.
  
        // Find map fragment
        mMapFragment = (SupportMapFragment) getSupportFragmentManager().findFragmentById(R.id.map);
  
        mMap = mMapFragment.getMap();
    }
  
  }

}