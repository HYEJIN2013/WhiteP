//In the usual case (avtivity subclass by MapActivity)
//Markers are added on a mapview using overlays.

//For a simple marker (no popups)
//Create an inner class subclassed to ItemizedOverlay<OverlayItem>
//like so:

class MarkerOverlay extends ItemizedOverlay<OverlayItem>{
    
	  private List<OverlayItem> reportlocations = new ArrayList<OverlayItem>();
	  private Context mContext;

	  public MarkerOverlay(Drawable defaultMarker, Context context) 
	  {
		  super(boundCenterBottom(defaultMarker));
		   
		  mContext = context;
	  }
	  
	  public void addOverlay(OverlayItem overlay)
	  {
		  reportlocations.add(overlay);
		  populate();
	  }
	  
	  
	  @Override
	  protected OverlayItem createItem(int i)
	  {
		  return reportlocations.get(i);
	  }

	  @Override
	  public int size() 
	  {
		   return reportlocations.size();
	  }
}


//Adding the marker
MapView mapView = ((MapView) findViewById(R.id.details_mapview));
mapView.getController().setCenter(getPoint(mReport.getLatitude(), mReport.getLongitude()));
mapView.getController().setZoom(17);
mapView.setBuiltInZoomControls(true);
		
// The marker
marker=getResources().getDrawable(R.drawable.marker);
marker.setBounds(0, 0, marker.getIntrinsicWidth(), marker.getIntrinsicHeight());
		
//Initialize our custom overlay item
MarkerOverlay reportMarker = new MarkerOverlay(marker,this);

//Multiply it (* 1000000) that's what 1e6 is in hex
GeoPoint point = new GeoPoint((int) (mReport.getLatitude() * 1E6), (int) (mReport.getLongitude() * 1E6));
		
//Create a new Overlay item
OverlayItem overlayitem = new OverlayItem(point, mReport.getTitle(), mReport.getDescription());
		
//Add it to our custom overlay list
reportMarker.addOverlay(overlayitem);
		
//Add the ReportLocation overlay object (with all our overlays list) to the map
mapView.getOverlays().add(reportMarker);