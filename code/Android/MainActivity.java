package com.vrin.googlemapdemo;

import java.util.HashMap;
import java.util.Map;

import android.os.Bundle;
import android.support.v4.app.FragmentActivity;

import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.GoogleMap.OnMapLongClickListener;
import com.google.android.gms.maps.GoogleMap.OnMarkerClickListener;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.BitmapDescriptor;
import com.google.android.gms.maps.model.BitmapDescriptorFactory;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.Marker;
import com.google.android.gms.maps.model.MarkerOptions;
import com.vrin.googlemapdemo.util.ICallback;
import com.vrin.googlemapdemo.util.MapUtils;
import com.vrin.googlemapdemo.util.MapUtils.MapInfoVO;
import com.vrin.googlemapdemo.util.MyLocation;

public class MainActivity extends FragmentActivity implements OnMapLongClickListener {

	SupportMapFragment mSupportMapFragment;

	GoogleMap mMap;

	float ZOOM_LEVEL;

	boolean isMapSetForFirst;

	MyLocation myLocation;

	Map<Integer, Marker> markers = new HashMap<Integer, Marker>();

	private static final LatLng LOWER_MANHATTAN = new LatLng(40.722543, -73.998585);
	private static final LatLng TIMES_SQUARE = new LatLng(40.7577, -73.9857);
	private static final LatLng BROOKLYN_BRIDGE = new LatLng(40.7057, -73.9964);


	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);

		mSupportMapFragment = (SupportMapFragment) getSupportFragmentManager().findFragmentById(R.id.mapFragment);
		myLocation = new MyLocation(this);
		myLocation.startServices();
	}

	/**
	 * method is use to set up map
	 */
	public void setUpMapIfNeeded() {
		if (mMap == null) {
			initMap();
		} else {
			if (isMapSetForFirst) {
				ZOOM_LEVEL = 15.0f;
			} else {
				ZOOM_LEVEL = mMap.getCameraPosition().zoom;
			}
		}
		if (mMap != null && myLocation.getLocation() != null) {
			double latitude = myLocation.getLocation().getLatitude();
			double longitude = myLocation.getLocation().getLongitude();
			//double latitude=Double.parseDouble("122.210144");
			//double longitude=Double.parseDouble("17.926874");


			Marker marker = mMap.addMarker(getMarker(latitude, longitude, "I AM", "My Current location", BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_GREEN)));
			addMarker(marker);
			if(isMapSetForFirst)
				zoom(latitude, longitude);
			isMapSetForFirst = false;
		}
	}

	private MarkerOptions getMarker(double lat, double lng, String title, String snippet, BitmapDescriptor resid)
	{
		MarkerOptions markerOptions = new MarkerOptions().position(new LatLng(lat, lng)).title(title).snippet(snippet).icon(resid);

		return markerOptions;
	}

	private void zoom(double lat, double lng){
		if(mMap != null)
		{
			LatLng HAMBURG1 = new LatLng(lat, lng);
			mMap.moveCamera(CameraUpdateFactory.newLatLngZoom(HAMBURG1, ZOOM_LEVEL));
			mMap.animateCamera(CameraUpdateFactory.zoomTo(ZOOM_LEVEL), 2000, null);
		}
	}

	private void initMap(){
		try {
			mMap = mSupportMapFragment.getMap();
			mMap.getUiSettings().setZoomControlsEnabled(false);
			mMap.getUiSettings().setMyLocationButtonEnabled(true);
			mMap.getUiSettings().setZoomGesturesEnabled(true);
			mMap.setMyLocationEnabled(true);
			ZOOM_LEVEL = 15.0f;

			mMap.setOnMapLongClickListener(this);
			mMap.setOnMarkerClickListener(new OnMarkerClickListener() {

				@Override
				public boolean onMarkerClick(Marker arg0) {
					return false;
				}
			});

		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	@Override
	public void onBackPressed() {
		if(isPathDraw)
		{
			isPathDraw = false;
			if(mMap != null)
			{
				mMap.clear();
				setUpMapIfNeeded();
			}
		}else
			super.onBackPressed();
	}


	boolean isPathDraw;

	@Override
	public void onMapLongClick(LatLng arg0) {
		isPathDraw = true;
		if(mMap != null)
		{
			mMap.clear();
			setUpMapIfNeeded();
			LatLng source = new LatLng(myLocation.getLocation().getLatitude(), myLocation.getLocation().getLongitude());
			addLines(source, arg0);
		}
	}

	private void addLines(LatLng source, final LatLng dest) {


		MapUtils.drawPath(this, source, dest, mMap);
		MapUtils.getDistanceTravel(this, source, dest, new ICallback() {

			@Override
			public void result(Object result) {
				if(result != null && result  instanceof MapUtils.MapInfoVO)
				{
					MapInfoVO infoVO = (MapInfoVO)result;
					Marker marker =mMap.addMarker(getMarker(dest.latitude, dest.longitude, infoVO.getAddress()+"", "Distance "+infoVO.getDistance()+" and duration "+infoVO.getDuration(), BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_RED)));
					addMarker(marker);
					zoom(dest.latitude, dest.longitude);
				}
			}
		});

	}

	private void removeMarker(){
		int size = markers.size();

		if((size - 1) > 0)
		{
			Marker marker = markers.get(size - 1);
			if(marker != null )
				marker.remove();
		}
	}

	private void addMarker(Marker marker){
		markers.put(markers.size(), marker);
	}
}
