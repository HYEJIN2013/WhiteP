@Override
protected void onStart() {
    super.onStart();
    
    //Get the LocationManager reference (usually inside the onCreate method)
    LocationManager locationManager = (LocationManager) this.getSystemService(Context.LOCATION_SERVICE);
    
    //Check if GPS is enabled
    final boolean gpsEnabled = locationManager.isProviderEnabled(LocationManager.GPS_PROVIDER);

    if (!gpsEnabled) {
        // BPromt the user to enable GPS, or whatever
    }
    
    //Pick a location provider
    LocationProvider provider =  locationManager.getProvider(LocationManager.GPS_PROVIDER);
    
    //OR
    
    // Retrieve a list of location providers that have fine accuracy, no monetary cost, etc
    Criteria criteria = new Criteria();
    criteria.setAccuracy(Criteria.ACCURACY_FINE);
    criteria.setCostAllowed(false);
    ...
    String providerName = locationManager.getBestProvider(criteria, true);
    
    // If no suitable provider is found, null is returned.
    if (providerName != null) {
       //too bad
    }
}


//We 're all done initializing let's get some location updates
private final LocationListener listener = new LocationListener() {

    @Override
    public void onLocationChanged(Location location) {
        // A new location update is received.  Do something useful with it.  In this case,
        // we're sending the update to a handler which then updates the UI with the new
        // location.
        Message.obtain(mHandler,
                UPDATE_LATLNG,
                location.getLatitude() + ", " +
                location.getLongitude()).sendToTarget();

            ...
        }
    ...
};

locationManager.requestLocationUpdates(LocationManager.GPS_PROVIDER,
        10000,          // 10-second interval.
        10,             // 10 meters.
        listener);
        
        
        
/**************************************************************/
//Handle Multiple Sources of Location Updates

private static final int TWO_MINUTES = 1000 * 60 * 2;

/** Determines whether one Location reading is better than the current Location fix
  * @param location  The new Location that you want to evaluate
  * @param currentBestLocation  The current Location fix, to which you want to compare the new one
  */
  
protected boolean isBetterLocation(Location location, Location currentBestLocation) {
  
    if (currentBestLocation == null) {
        // A new location is always better than no location
        return true;
    }



    // Check whether the new location fix is newer or older
    long timeDelta = location.getTime() - currentBestLocation.getTime();
    boolean isSignificantlyNewer = timeDelta > TWO_MINUTES;
    boolean isSignificantlyOlder = timeDelta < -TWO_MINUTES;
    boolean isNewer = timeDelta > 0;

    // If it's been more than two minutes since the current location, use the new location
    // because the user has likely moved
    if (isSignificantlyNewer) {
        return true;
    // If the new location is more than two minutes older, it must be worse
    } else if (isSignificantlyOlder) {
        return false;
    }

    // Check whether the new location fix is more or less accurate
    int accuracyDelta = (int) (location.getAccuracy() - currentBestLocation.getAccuracy());
    boolean isLessAccurate = accuracyDelta > 0;
    boolean isMoreAccurate = accuracyDelta < 0;
    boolean isSignificantlyLessAccurate = accuracyDelta > 200;

    // Check if the old and new location are from the same provider
    boolean isFromSameProvider = isSameProvider(location.getProvider(),
            currentBestLocation.getProvider());

    // Determine location quality using a combination of timeliness and accuracy
    if (isMoreAccurate) {
        return true;
    } else if (isNewer && !isLessAccurate) {
        return true;
    } else if (isNewer && !isSignificantlyLessAccurate && isFromSameProvider) {
        return true;
    }
    return false;
}

/** Checks whether two providers are the same */
private boolean isSameProvider(String provider1, String provider2) {
    if (provider1 == null) {
      return provider2 == null;
    }
    return provider1.equals(provider2);
}

/**************************************************************/


//Terminate location updates
protected void onStop() {
    super.onStop();
    locationManager.removeUpdates(listener);
}