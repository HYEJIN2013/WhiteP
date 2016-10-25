private MapFragment frag;
private GoogleMap map;

//Markers
static final LatLng HAMBURG = new LatLng(53.558, 9.927);

@Override
protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    
    setContentView(R.layout.maplayout);
    
    //Create a new MapFragment
    //Google said we should use this method instead of new MapFragment()
    frag = MapFragment.newInstance();
    
    //Add the MapFragment to the view
    FragmentTransaction ft = getFragmentManager().beginTransaction();
    ft.replace(R.id.map, frag).commit();
    
    
    /***************************************************************/
    //We don't always want USA to appear every tinme we open the map
    //Make a timer to wait for the map to initialize
    final Timer t = new Timer();
    t.schedule(new TimerTask() {
    @Override
        public void run() {
            if (frag != null && frag.isVisible()) {
                t.cancel();
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        //Get the Map Object from the MapFragment
                        map = frag.getMap();
                        
                        if (map != null) {
                            //If it is not null
                            //Move the map camera to the Latitude and Longitude provided
                            map.animateCamera(CameraUpdateFactory.newLatLngZoom(new LatLng(22.3d, 114.1667d), 13));
                                                                                            //lat   lng       zoom
                        }
                    }});
            }
        }
      }, 0, 200);
      /***************************************************************/
      
      //Get the map object if you haven't already from above
      map = ((MapFragment) getFragmentManager().findFragmentById(R.id.map)).getMap();
        
      //Set the map type
      GoogleMap.setMapType(GoogleMap.MAP_TYPE_NORMAL);
      //GoogleMap.MAP_TYPE_SATELLITE
      //GoogleMap.MAP_TYPE_TERRAIN
      //GoogleMap.MAP_TYPE_HYBIRD
      
      GoogleMap.setMyLocationEnabled(true)  //Set if my location and my location button will be shown.
      
      //Add markers
      if (map!=null){
        Marker hamburg = map.addMarker(new MarkerOptions().position(HAMBURG).title("Hamburg")snippet("Hamburg is cool")
                                                    .icon(BitmapDescriptorFactory.fromResource(R.drawable.ic_launcher));
      }
      
      //Move the camera instantly to hamburg with a zoom of 15.
      map.moveCamera(CameraUpdateFactory.newLatLngZoom(HAMBURG, 15));
        
      // Zoom in, animating the camera.
      map.animateCamera(CameraUpdateFactory.zoomTo(10), 2000, null); 
        
     //When the user clicks on a marker
     map.setOnMarkerClickListener(new OnMarkerClickListener() {

    @Override
    public boolean onMarkerClick(Marker marker) {
        //Show a Toast
        Toast.makeText(getApplicationContext(), "Title:"+marker.getTitle()+"\nMessage:"+marker.getSnippet(), Toast.LENGTH_SHORT).show();
        return false;
    }
         

}