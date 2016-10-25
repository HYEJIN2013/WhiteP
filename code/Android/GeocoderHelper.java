package com.vrin.googlemapdemo.util;

import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.BasicResponseHandler;
import org.json.JSONArray;
import org.json.JSONObject;

import android.app.Activity;
import android.net.http.AndroidHttpClient;
import android.os.AsyncTask;
import android.util.Log;

public class GeocoderHelper {

	private static final AndroidHttpClient ANDROID_HTTP_CLIENT = AndroidHttpClient.newInstance(GeocoderHelper.class.getName());

	private static boolean running = false;

	
	
	public static void getAddress(final Activity contex, final double LATITUDE, final double LONGITUDE, final ICallback iCallback) {

		if (running)
			return ;

		new AsyncTask<Void, Void, String>() {
			protected void onPreExecute() {
				running = true;
				MapUtils.showProgress(contex);
			};

			@Override
			protected String doInBackground(Void... params) {
				return fetchCityNameUsingGoogleMap();
			}

			// Geocoder failed :-(
			// Our B Plan : Google Map
			@SuppressWarnings("unused")
			private String fetchCityNameUsingGoogleMap()
			{
				String googleMapUrl = "http://maps.googleapis.com/maps/api/geocode/json?latlng=" + LATITUDE + ","
						+ LONGITUDE + "&sensor=false&language=en";
				
				try {
					JSONObject googleMapResponse = new JSONObject(ANDROID_HTTP_CLIENT.execute(new HttpGet(
							googleMapUrl), new BasicResponseHandler()));

					JSONArray results = (JSONArray) googleMapResponse.get("results");

					for (int i = 0; i < results.length(); i++) {
						// loop among all addresses within this result
						JSONObject result = results.getJSONObject(i);

						return result.getString("formatted_address");
					}
				} catch (Exception ignored) {
					ignored.printStackTrace();
				}
				return "";
			}

			protected void onPostExecute(String cityName) {
				running = false;
				MapUtils.dismissDialog();
				if (cityName != null) {
					Log.i("GeocoderHelper#", cityName);
					iCallback.result(cityName.toString());
				}
			};
		}.execute();
	}
}