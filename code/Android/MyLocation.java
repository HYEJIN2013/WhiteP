package com.vrin.googlemapdemo.util;


import android.app.Activity;
import android.app.Dialog;
import android.content.IntentSender;
import android.location.Location;
import android.os.Bundle;
import android.support.v4.app.FragmentActivity;
import android.util.Log;

import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.GooglePlayServicesClient;
import com.google.android.gms.common.GooglePlayServicesUtil;
import com.google.android.gms.location.LocationClient;
import com.google.android.gms.location.LocationListener;
import com.google.android.gms.location.LocationRequest;
import com.vrin.googlemapdemo.MainActivity;

public class MyLocation implements LocationListener, GooglePlayServicesClient.ConnectionCallbacks, GooglePlayServicesClient.OnConnectionFailedListener
{
	// A request to connect to Location Services
	private LocationRequest mLocationRequest;

	// Stores the current instantiation of the location client in this object
	private LocationClient mLocationClient;

	/**
	 * Note if updates have been turned on. Starts out as "false"; is set to "true" in the
	 * method handleRequestSuccess of LocationUpdateReceiver.
	 *
	 */
	boolean mUpdatesRequested = false;

	private FragmentActivity fragmentActivity;
	private Activity mActivity;
	public static MyLocation myLocationClass;

	public MyLocation(){

	}
	public MyLocation(FragmentActivity fragment)
	{
		if(fragment != null)
		{
			this.fragmentActivity = fragment;
		}
		initializeLocationServices(fragmentActivity);
	}

	public MyLocation(Activity fragment)
	{
		if(fragment != null)
		{
			this.mActivity = fragment;
		}
		initializeLocationServices(mActivity);
	}

	//	public static MyLocation getInstance (Activity activity,Fragment fragment,Intent mIntentService)
	//	{
	//		if (myLocationClass == null)
	//		{
	//			myLocationClass = new MyLocation(activity,fragment,mIntentService);
	//		}
	//		return myLocationClass;
	//	}

	/**
	 * method to initilize the location service. 
	 * @param activity
	 */

	private void initializeLocationServices(Activity activity) 
	{
		// Create a new global location parameters object
		mLocationRequest = LocationRequest.create();

		/*
		 * Set the update interval
		 */
		mLocationRequest.setInterval(LocationUtils.UPDATE_INTERVAL_IN_MILLISECONDS);


		// Use high accuracy
		mLocationRequest.setPriority(LocationRequest.PRIORITY_HIGH_ACCURACY);

		// Set the interval ceiling to one minute
		mLocationRequest.setFastestInterval(LocationUtils.FAST_INTERVAL_CEILING_IN_MILLISECONDS);
		
		mLocationRequest.setSmallestDisplacement(LocationUtils.UPDATE_INTERVAL_IN_MILES);

		// Note that location updates are off until the user turns them on
		mUpdatesRequested = true;

		/*
		 * Create a new location client, using the enclosing class to
		 * handle callbacks.
		 */
		mLocationClient = new LocationClient(activity, this, this);

	}

	/**
	 * method to start the service.
	 */

	public void startServices()
	{
		/*
		 * Connect the client. Don't re-start any requests here;
		 * instead, wait for onResume()
		 */

		if(!mLocationClient.isConnected())
		{
			mLocationClient.connect();
			Log.e("#MyLocation#", "Location client is connected");
		}
		//	
		if(getLocation()!=null)
		{
			updateLocation();
		}
		//		
	}

	public void stopServices()
	{
		// If the client is connected
		if (mLocationClient.isConnected())
		{
			stopPeriodicUpdates();
		}

		// After disconnect() is called, the client is considered "dead".
		mLocationClient.disconnect();
	}

	/**
	 * In response to a request to start updates, send a request
	 * to Location Services
	 */
	private void startPeriodicUpdates() 
	{
		mLocationClient.requestLocationUpdates(mLocationRequest, this);
	}

	/**
	 * In response to a request to stop updates, send a request to
	 * Location Services
	 */
	private void stopPeriodicUpdates()
	{
		mLocationClient.removeLocationUpdates(this);
	}

	/**
	 * Verify that Google Play services is available before making a request.
	 *
	 * @return true if Google Play services is available, otherwise false
	 */
	public boolean servicesConnected()
	{
		boolean check;
		int resultCode=-1;
		// Check that Google Play services is available
		if(fragmentActivity!=null){
			resultCode = GooglePlayServicesUtil.isGooglePlayServicesAvailable(fragmentActivity);
		}else{
			resultCode = GooglePlayServicesUtil.isGooglePlayServicesAvailable(mActivity);
		}


		// If Google Play services is available
		if (ConnectionResult.SUCCESS == resultCode) 
		{
			// In debug mode, log the status

			// Continue
			if (mLocationClient.isConnected())
				check = true;
			else
				check = false;

		}
		// Google Play services was not available for some reason
		else 
		{
			// Display an error dialog
			Log.e("", "result"+"services not connected");
			check = false;
		}
		return check;
	}

	/**
	 * Invoked by the "Get Location" button.
	 *
	 * Calls getLastLocation() to get the current location
	 *
	 * @param v The view object associated with this method, in this case a Button.
	 */
	public Location getLocation() 
	{
		Location currentLocation = null;
		// If Google Play Services is available
		if (servicesConnected()) 
		{
			currentLocation = mLocationClient.getLastLocation();
		}
		return currentLocation;
	}

	/**
	 *  Invoked by the "Start Updates" button
	 * Sends a request to start location updates
	 *
	 * @param v The view object associated with this method, in this case a Button.
	 */
	public void startUpdates() 
	{
		//		mUpdatesRequested = true;
		//
		//		if (servicesConnected()) 
		//		{
		startPeriodicUpdates();
		//		}
	}

	/**
	 * Invoked by the "Stop Updates" button
	 * Sends a request to remove location updates
	 * request them.
	 *
	 * @param v The view object associated with this method, in this case a Button.
	 */
	public void stopUpdates() 
	{
		mUpdatesRequested = false;

		if (servicesConnected()) 
		{
			stopPeriodicUpdates();
		}
	}

	/**
    /*
	 * Called by Location Services when the request to connect the
	 * client finishes successfully. At this point, you can
	 * request the current location or start periodic updates
	 */
	@Override
	public void onConnected(Bundle bundle)
	{
		startUpdates();
		if(getLocation()!=null)
		{
			updateLocation();
		}
	}

	/**
	 * Called by Location Services if the connection to the
	 * location client drops because of an error.
	 */
	@Override
	public void onDisconnected() 
	{
		stopUpdates();
	}

	/**
	 * Called by Location Services if the attempt to
	 * Location Services fails.
	 */
	@Override
	public void onConnectionFailed(ConnectionResult connectionResult) 
	{

		/**
		 * Google Play services can resolve some errors it detects.
		 * If the error has a resolution, try sending an Intent to
		 * start a Google Play services activity that can resolve
		 * error.
		 */
		if (connectionResult.hasResolution())
		{
			try 
			{

				// Start an Activity that tries to resolve the error
				connectionResult.startResolutionForResult(fragmentActivity,	LocationUtils.CONNECTION_FAILURE_RESOLUTION_REQUEST);

				/**
				 * Thrown if Google Play services canceled the original
				 * PendingIntent
				 */

			} 
			catch (IntentSender.SendIntentException e) 
			{

				// Log the error
				e.printStackTrace();
			}
		} 
		else
		{

			// If no resolution is available, display a dialog to the user with the error.
			showErrorDialog(connectionResult.getErrorCode());
		}
	}

	/**
	 * Show a dialog returned by Google Play services for the
	 * connection error code
	 *
	 * @param errorCode An error code returned from onConnectionFailed
	 */
	private void showErrorDialog(int errorCode) 
	{
		if(fragmentActivity!=null){
			// Get the error dialog from Google Play services
			Dialog errorDialog = GooglePlayServicesUtil.getErrorDialog(errorCode, fragmentActivity, LocationUtils.CONNECTION_FAILURE_RESOLUTION_REQUEST);

			// If Google Play services can provide an error dialog
			if (errorDialog != null) {

				// Create a new DialogFragment in which to show the error dialog
				ErrorDialog mErrorDialog  = new ErrorDialog(fragmentActivity);

				// Set the dialog in the DialogFragment
				if(mErrorDialog!=null){
					mErrorDialog.setDialog(errorDialog);

					// Show the error dialog in the DialogFragment
					mErrorDialog.show();
				}
			}
		}
	}

	/**
	 * Define a DialogFragment to display the error dialog generated in
	 * showErrorDialog.
	 */
	public static class ErrorDialog extends Dialog 
	{
		@SuppressWarnings("unused")
		private Dialog mDialog;

		public ErrorDialog(Activity activity)
		{
			super(activity);
		}

		/**
		 * Set the dialog to display
		 *
		 * @param dialog An error dialog
		 */
		public void setDialog(Dialog dialog)
		{
			mDialog = dialog;
		}
	}

	/**
	 * Report location updates to the UI.
	 *
	 * @param location The updated location.
	 */
	@Override
	public void onLocationChanged(Location location)
	{
		updateLocation();
	}

	public void stopService() 
	{
		stopServices();
	}
	
	private void updateLocation(){
		Log.e("#MyLocation#", "update location :: "+LocationUtils.getLatLng(getLocation()));
		if(fragmentActivity instanceof MainActivity)
		{
			((MainActivity)fragmentActivity).setUpMapIfNeeded();
		}
	}

}