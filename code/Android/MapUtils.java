package com.vrin.googlemapdemo.util;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import android.app.Activity;
import android.app.ProgressDialog;
import android.content.Context;
import android.graphics.Color;
import android.location.Location;
import android.os.AsyncTask;
import android.util.Log;

import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.LatLngBounds;
import com.google.android.gms.maps.model.PolylineOptions;

@SuppressWarnings("unused")
public class MapUtils {

	private static final float METERS_PER_FEET = 0.3048f;
	private static final double OFFSET_CALCULATION_INIT_DIFF = 1.0;
	private static final float OFFSET_CALCULATION_ACCURACY = 0.01f;

	private Context mContext;

	public MapUtils(Context context){
		this.mContext = context;
	}


	public static void drawPath(Activity mActivity, LatLng srcLatLng, LatLng destLatLng, GoogleMap map) {

		try {
			String url = LocationUtils.getMapsApiDirectionsUrl(srcLatLng, destLatLng);
			(new ReadTask(mActivity, map)).execute(url);
		}catch (Exception e) {

		}
	} 

	public static double findDistanceTwoLatLng(LatLng latLngCurrent, LatLng latLngMarker) {
		float[] distances = new float[1];
		Location.distanceBetween(latLngCurrent.latitude, latLngCurrent.longitude,
				latLngMarker.latitude, latLngMarker.longitude, distances);
		double distance = distances[0];
		return distance;
	}

	/** A method to download json data from url */
	public static String loadURL(String strUrl) throws IOException {
		String response = "";
		InputStream iStream = null;
		HttpURLConnection urlConnection = null;
		try {
			URL url = new URL(strUrl);

			urlConnection = (HttpURLConnection) url.openConnection();
			urlConnection.connect();
			iStream = urlConnection.getInputStream();
			BufferedReader br = new BufferedReader(new InputStreamReader(
					iStream));

			StringBuffer sb = new StringBuffer();

			String line = "";
			while ((line = br.readLine()) != null) {
				sb.append(line);
			}
			response = sb.toString();
			br.close();
			iStream.close();
			urlConnection.disconnect();
		} catch (Exception e) {
			Log.e("#DownloadURL#","Exception while downloading url" + e.toString());
		}
		return response;
	}


	public static void getDistanceTravel(final Activity activity, final LatLng origins, final LatLng destinations, final ICallback iCallback) {
		if (origins == null)
			return;
		new AsyncTask<Void, Void, MapInfoVO>() {

			@Override
			protected void onPreExecute() {
				showProgress(activity);
			}

			@Override
			protected MapInfoVO doInBackground(Void... params) {
				try {
					double latOrigins = origins.latitude; 
					double longOrigins = origins.longitude; 
					double latDestinations = destinations.latitude; 
					double longDestinations = destinations.longitude;
					//					String URL = "http://maps.googleapis.com/maps/api/distancematrix/json?origins=" +latOrigins + "," + longOrigins  + "&destinations=" 
					//								+ latDestinations + "," + longDestinations + "&mode=bicycling&language=en-EN&sensor=false";
					String URL = "http://maps.googleapis.com/maps/api/directions/json?origin=" +latOrigins + "," + longOrigins  + "&destination=" 
							+ latDestinations + "," + longDestinations + "&sensor=false&mode=Bicycling";
					
					URL = LocationUtils.getMapsApiDirectionsUrl(origins, destinations);
					Log.d("#DistancdDuration#", "Response URL="+URL);
					String strResponse = loadURL(URL);
					
					MapInfoVO mapInfoVO = parseDistanceAndDuration(new JSONObject(strResponse));
					return mapInfoVO;
				} catch (IOException e) {
					e.printStackTrace();
				} catch (JSONException e) {
					e.printStackTrace();
				}
				return null;
			}

			@Override
			protected void onPostExecute(MapInfoVO result) {
				dismissDialog();
				iCallback.result(result);
			}
		}.execute();
	}


	private static String endAddress;
	public static String getEndAddress(){
		return endAddress;
	}

	private static void setEndAddress(String address){
		MapUtils.endAddress = address;
	}
	/*
	 * Helper method to calculate the bounds for map zooming
	 */
	public LatLngBounds calculateBoundsWithCenter(LatLng myLatLng) {
		// Create a bounds
		LatLngBounds.Builder builder = LatLngBounds.builder();

		// Calculate east/west points that should to be included
		// in the bounds
		double lngDifference = calculateLatLngOffset(myLatLng, false);
		LatLng east = new LatLng(myLatLng.latitude, myLatLng.longitude + lngDifference);
		builder.include(east);
		LatLng west = new LatLng(myLatLng.latitude, myLatLng.longitude - lngDifference);
		builder.include(west);

		// Calculate north/south points that should to be included
		// in the bounds
		double latDifference = calculateLatLngOffset(myLatLng, true);
		LatLng north = new LatLng(myLatLng.latitude + latDifference, myLatLng.longitude);
		builder.include(north);
		LatLng south = new LatLng(myLatLng.latitude - latDifference, myLatLng.longitude);
		builder.include(south);

		return builder.build();
	}

	/*
	 * Helper method to calculate the offset for the bounds used in map zooming
	 */
	private double calculateLatLngOffset(LatLng myLatLng, boolean bLatOffset) {
		// The return offset, initialized to the default difference
		double latLngOffset = OFFSET_CALCULATION_INIT_DIFF;
		// Set up the desired offset distance in meters
		float desiredOffsetInMeters = LocationUtils.UPDATE_INTERVAL_IN_MILES * 100;
		// Variables for the distance calculation
		float[] distance = new float[1];
		boolean foundMax = false;
		double foundMinDiff = 0;
		// Loop through and get the offset
		do {
			// Calculate the distance between the point of interest
			// and the current offset in the latitude or longitude direction
			if (bLatOffset) {
				Location.distanceBetween(myLatLng.latitude, myLatLng.longitude, myLatLng.latitude
						+ latLngOffset, myLatLng.longitude, distance);
			} else {
				Location.distanceBetween(myLatLng.latitude, myLatLng.longitude, myLatLng.latitude,
						myLatLng.longitude + latLngOffset, distance);
			}
			// Compare the current difference with the desired one
			float distanceDiff = distance[0] - desiredOffsetInMeters;
			if (distanceDiff < 0) {
				// Need to catch up to the desired distance
				if (!foundMax) {
					foundMinDiff = latLngOffset;
					// Increase the calculated offset
					latLngOffset *= 2;
				} else {
					double tmp = latLngOffset;
					// Increase the calculated offset, at a slower pace
					latLngOffset += (latLngOffset - foundMinDiff) / 2;
					foundMinDiff = tmp;
				}
			} else {
				// Overshot the desired distance
				// Decrease the calculated offset
				latLngOffset -= (latLngOffset - foundMinDiff) / 2;
				foundMax = true;
			}
		} while (Math.abs(distance[0] - desiredOffsetInMeters) > OFFSET_CALCULATION_ACCURACY);
		return latLngOffset;
	}

	public static void getAddress(Activity activity, LatLng latLng, final  ICallback iCallback){
		try {
			GeocoderHelper.getAddress(activity, latLng.latitude, latLng.longitude, new ICallback() {

				@Override
				public void result(Object result) {
					if (result != null) {
						try {
							final String strAddress = result.toString().trim();
							iCallback.result(strAddress);
						} catch (Exception e) {
							e.printStackTrace();
						}
					}
				}
			});

		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	public static class ReadTask extends AsyncTask<String, String, List<List<HashMap<String, String>>>> {
		Activity mActivity;
		
		GoogleMap googleMap;
		
		private ReadTask(Activity activity, GoogleMap googleMap){
			this.mActivity = activity;
			this.googleMap = googleMap;
		}
		
		@Override
		protected void onPreExecute() {
			showProgress(mActivity);
		}
		
		@Override
		protected List<List<HashMap<String, String>>> doInBackground(String... url) {
			String data = "";
			try {
				data = loadURL(url[0]);
				JSONObject jObject = new JSONObject(data);
				@SuppressWarnings("unchecked")
				List<List<HashMap<String, String>>> routes = (List<List<HashMap<String, String>>>) parseRoute(jObject);
				return routes;
			} catch (Exception e) {
				Log.d("Background Task", e.toString());
			}
			return null;
		}

		@Override
		@SuppressWarnings("unchecked")
		protected void onPostExecute(List<List<HashMap<String, String>>> routes) {
			if(routes != null)
			{
				try {
					ArrayList points = null;
					PolylineOptions polyLineOptions = null;

					// traversing through routes
					for (int i = 0; i < routes.size(); i++) {
						points = new ArrayList();
						polyLineOptions = new PolylineOptions();
						List<?> path = routes.get(i);

						for (int j = 0; j < path.size(); j++) {
							HashMap<String, String> point = (HashMap<String, String>) path.get(j);

							double lat = Double.parseDouble(point.get("lat"));
							double lng = Double.parseDouble(point.get("lng"));
							LatLng position = new LatLng(lat, lng);

							points.add(position);
						}

						polyLineOptions.addAll(points);
						polyLineOptions.width(2);
						polyLineOptions.color(Color.BLUE);
					}

					googleMap.addPolyline(polyLineOptions);
				} catch (Exception e) {
					e.printStackTrace();
				}finally{
					dismissDialog();
				}
			}else
			{
				dismissDialog();
			}
		}

	}
	
	public static List<?> parseRoute(JSONObject jObject) {
		List<List<HashMap<String, String>>> routes = new ArrayList<List<HashMap<String, String>>>();
		MapInfoVO  infoVO = new MapInfoVO();
		JSONArray jRoutes = null;
		JSONArray jLegs = null;
		JSONArray jSteps = null;
		try {
			jRoutes = jObject.getJSONArray("routes");
			/** Traversing all routes */
			for (int i = 0; i < jRoutes.length(); i++) {
				jLegs = ((JSONObject) jRoutes.get(i)).getJSONArray("legs");
				List<HashMap<String, String>> path = new ArrayList<HashMap<String, String>>();

				/** Traversing all legs */
				for (int j = 0; j < jLegs.length(); j++) {
					JSONObject jsonObjectEle = jLegs.getJSONObject(j);
					jSteps = (jsonObjectEle).getJSONArray("steps");

					JSONObject jsonObjectDistance = jsonObjectEle.getJSONObject("distance");
					JSONObject jsonObjectDuration = jsonObjectEle.getJSONObject("duration");
					infoVO.setDistance(jsonObjectDistance.optString("text"));
					infoVO.setDuration(jsonObjectDuration.optString("text"));
					/** Traversing all steps */
					for (int k = 0; k < jSteps.length(); k++) {
						String polyline = "";
						polyline = (String) ((JSONObject) ((JSONObject) jSteps.get(k)).get("polyline")).get("points");
						List<LatLng> list = decodePoly(polyline);

						/** Traversing all points */
						for (int l = 0; l < list.size(); l++) {
							HashMap<String, String> hm = new HashMap<String, String>();
							hm.put("lat",
									Double.toString(((LatLng) list.get(l)).latitude));
							hm.put("lng",
									Double.toString(((LatLng) list.get(l)).longitude));
							path.add(hm);
						}
						routes.add(path);
					}
				}
			}

		} catch (JSONException e) {
			e.printStackTrace();
		} catch (Exception e) {
		}
		return routes;
	}

	private static List<LatLng> decodePoly(String encoded) {

		List<LatLng> poly = new ArrayList<LatLng>();
		int index = 0, len = encoded.length();
		int lat = 0, lng = 0;

		while (index < len) {
			int b, shift = 0, result = 0;
			do {
				b = encoded.charAt(index++) - 63;
				result |= (b & 0x1f) << shift;
				shift += 5;
			} while (b >= 0x20);
			int dlat = ((result & 1) != 0 ? ~(result >> 1) : (result >> 1));
			lat += dlat;

			shift = 0;
			result = 0;
			do {
				b = encoded.charAt(index++) - 63;
				result |= (b & 0x1f) << shift;
				shift += 5;
			} while (b >= 0x20);
			int dlng = ((result & 1) != 0 ? ~(result >> 1) : (result >> 1));
			lng += dlng;

			LatLng p = new LatLng( (((double) lat / 1E5)),
					(((double) lng / 1E5) ));
			poly.add(p);
		}

		return poly;
	}

	static ProgressDialog mProgressDialog;

	public static void showProgress(Activity activity){
		try {
			if(mProgressDialog ==null)
			{
				mProgressDialog = new ProgressDialog(activity);
				mProgressDialog.setCancelable(true);
				mProgressDialog.setCanceledOnTouchOutside(false);
				mProgressDialog.setMessage("Please wait...");
			}
			
			if(!mProgressDialog.isShowing())
			mProgressDialog.show();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	public static void dismissDialog(){
		if(mProgressDialog != null)
			mProgressDialog.dismiss();
	}
	
	public static class MapInfoVO{
		private String duration;
		private String distance;
		private String address;
		public String getDuration() {
			return duration;
		}
		public void setDuration(String duration) {
			this.duration = duration;
		}
		public String getDistance() {
			return distance;
		}
		public void setDistance(String distance) {
			this.distance = distance;
		}
		public String getAddress() {
			return address;
		}
		public void setAddress(String address) {
			this.address = address;
		}
	} 
	
	public static MapInfoVO parseDistanceAndDuration(JSONObject jObject) {
		MapInfoVO  infoVO = null;
		JSONArray jRoutes = null;
		JSONArray jLegs = null;
		JSONArray jSteps = null;
		try {
			jRoutes = jObject.getJSONArray("routes");
			 infoVO = new MapInfoVO();
			/** Traversing all routes */
			for (int i = 0; i < jRoutes.length(); i++) {
				jLegs = ((JSONObject) jRoutes.get(i)).getJSONArray("legs");
				List<HashMap<String, String>> path = new ArrayList<HashMap<String, String>>();

				/** Traversing all legs */
				for (int j = 0; j < jLegs.length(); j++) {
					JSONObject jsonObjectEle = jLegs.getJSONObject(j);
					jSteps = (jsonObjectEle).getJSONArray("steps");

					JSONObject jsonObjectDistance = jsonObjectEle.getJSONObject("distance");
					JSONObject jsonObjectDuration = jsonObjectEle.getJSONObject("duration");
					infoVO.setDistance(jsonObjectDistance.optString("text"));
					infoVO.setDuration(jsonObjectDuration.optString("text"));
					
					if(jsonObjectEle.has("end_address"))
					{
						String address = jsonObjectEle.getString("end_address");
						setEndAddress(address);
						infoVO.setAddress(address);
					}
					
				}
			}

		} catch (JSONException e) {
			e.printStackTrace();
		} catch (Exception e) {
		}
		return infoVO;
	}

}