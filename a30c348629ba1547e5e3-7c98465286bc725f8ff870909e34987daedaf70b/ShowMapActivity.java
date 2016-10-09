package br.com.metasix.foodtruckapp.ui.activity;

import android.app.Dialog;
import android.app.DialogFragment;
import android.content.Intent;
import android.content.IntentSender;
import android.location.Location;
import android.os.Bundle;
import android.os.Handler;
import android.support.v4.app.FragmentActivity;
import android.view.View;
import android.widget.RelativeLayout;
import android.widget.TextView;

import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.GooglePlayServicesUtil;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.android.gms.location.LocationServices;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.BitmapDescriptorFactory;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.Marker;
import com.google.android.gms.maps.model.MarkerOptions;
import com.parse.FindCallback;
import com.parse.ParseException;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import br.com.metasix.foodtruckapp.util.MapUtil;
import br.com.metasix.foodtruckapp.entity.Place;
import br.com.metasix.foodtruckapp.R;

public class ShowMapActivity extends FragmentActivity
        implements GoogleApiClient.ConnectionCallbacks, GoogleApiClient.OnConnectionFailedListener {

    private static final int REQUEST_ERROR_PLAY_SERVICES = 1;
    private GoogleMap mGoogleMap;
    private GoogleApiClient mGoogleApiClient;
    private LatLng mOrigem;
    private SupportMapFragment fragment;
    private Marker checkedMarker;
    private int mapPreference;
    private static final double LAT_SAO_PAULO = -23.550520;
    private static final double LONG_SAO_PAULO = -46.633309;
    private HashMap<Marker, Place> checkList;
    private List<Place> placeList;
    private UIHelper ui;
    private Marker clickedMarker;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_show_map);
        init();
    }

    private void init() {
        ui = new UIHelper();
        setMap();
        getMapPreferences();
        loadValues();
    }

    private void loadValues() {
        //placeList = Place.getFakePlaces();
    }

    private void setMap() {
        fragment = (SupportMapFragment) getSupportFragmentManager().findFragmentById(R.id.google_maps);
        mGoogleMap = fragment.getMap();
        mGoogleMap.getUiSettings().setMapToolbarEnabled(false);
        mGoogleMap.setMyLocationEnabled(true);

        mGoogleApiClient = new GoogleApiClient.Builder(this)
                .addConnectionCallbacks(this)
                .addOnConnectionFailedListener(this)
                .addApi(LocationServices.API)
                .build();

        mGoogleMap.setOnMarkerClickListener(onMarkerClick());
        mGoogleMap.setOnMapClickListener(onMapClickCustomer());
    }

    private void getMapPreferences() {
        Intent intent = getIntent();
        Bundle params = intent.getExtras();
        if (params != null) {
            mapPreference = params.getInt("mapPreference");
        }
    }

    private void createMarkers() {
        Place.getAll(callbackGetPlace());
    }

    private GoogleMap.OnMapClickListener onMapClickCustomer() {
        return new GoogleMap.OnMapClickListener() {

            @Override
            public void onMapClick(LatLng latLng) {
                removeContentView();
            }
        };
    }

    private GoogleMap.OnMarkerClickListener onMarkerClick() {
        return new GoogleMap.OnMarkerClickListener() {
            @Override
            public boolean onMarkerClick(Marker marker) {
                    clickedMarker = marker;
                    removeContentView();
                    addContentBarDelay();
                    moveCamera(MapUtil.getLatLong(clickedMarker), false);
                return false;
            }
        };
    }

    private void addContentBarDelay() {
        new Handler().postDelayed(new Runnable() {
            @Override
            public void run() {
                addContentBarView();
            }
        }, 500);
    }

    private void addContentBarView() {
        ui.contentLayout.addView(ui.contentBar);
        ui.contentBar.setVisibility(View.VISIBLE);

        for (Map.Entry<Marker, Place> entry : checkList.entrySet()) {
            if (entry.getKey().equals(clickedMarker)) {
                ((TextView) ui.contentBar.findViewById(R.id.content_bar_title)).setText(entry.getValue().getTitle());
                ((TextView) ui.contentBar.findViewById(R.id.content_bar_description)).setText(entry.getValue().getDescription());

            }
        }
    }

    private void removeContentView() {
        ui.contentLayout.removeAllViews();
    }

    private void setEvents() {
        mGoogleMap.setOnMapClickListener(onClickMarkerCheckIn());
    }

    private GoogleMap.OnMapClickListener onClickMarkerCheckIn() {
        return new GoogleMap.OnMapClickListener() {
            @Override
            public void onMapClick(LatLng latLng) {
                checkList = new HashMap<>();
                Place checkPlaces = new Place();

                mGoogleMap.clear();

                checkedMarker = mGoogleMap.addMarker(new MarkerOptions()
                        .title("Meu local")
                        .position(latLng)
                        .icon(BitmapDescriptorFactory.fromResource(R.mipmap.ic_truck_red)));

                checkList.put(checkedMarker, checkPlaces);
                clickedMarker = null;
            }
        };
    }

    @Override
    protected void onStart() {
        super.onStart();
        mGoogleApiClient.connect();

        if (mapPreference == ChooseMapsActivity.MAP_STATIC) {
            zoomSP();
            createMarkers();
            contentBarOnClick();
        } else {
            setEvents();
        }
    }

    private void contentBarOnClick() {
        ui.contentBar.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(ShowMapActivity.this, FoodTruckDataActivity.class);
                startActivity(intent);
            }
        });
    }

    private void zoomSP() {
        mGoogleMap.animateCamera(CameraUpdateFactory.newLatLngZoom(new LatLng(LAT_SAO_PAULO, LONG_SAO_PAULO), 13.0f));
    }

    private void moveCamera(LatLng latlng, boolean isMyLocation) {
        if (isMyLocation) {
            mGoogleMap.animateCamera(CameraUpdateFactory.newLatLngZoom(latlng, 17.0f));
        } else {
            mGoogleMap.animateCamera(CameraUpdateFactory.newLatLng(latlng));
        }
    }

    @Override
    protected void onStop() {
        if (mGoogleApiClient != null && mGoogleApiClient.isConnected()) {
            mGoogleApiClient.disconnect();
        }
        super.onStop();
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == REQUEST_ERROR_PLAY_SERVICES
                && resultCode == RESULT_OK) {
            mGoogleApiClient.connect();
        }
    }

    @Override
    public void onConnected(Bundle bundle) {
        getLastLocation();
        if (mOrigem != null) {
            moveCamera(mOrigem, true);
        }
    }

    @Override
    public void onConnectionSuspended(int i) {
        mGoogleApiClient.connect();
    }

    @Override
    public void onConnectionFailed(ConnectionResult connectionResult) {
        if (connectionResult.hasResolution()) {
            try {
                connectionResult.startResolutionForResult(this, REQUEST_ERROR_PLAY_SERVICES);
            } catch (IntentSender.SendIntentException e) {
                e.printStackTrace();
            }
        } else {
            showErrorMessage(this, connectionResult.getErrorCode());
        }
    }

    private void getLastLocation() {
        Location location = LocationServices.FusedLocationApi.getLastLocation(mGoogleApiClient);

        if (location != null) {
            mOrigem = new LatLng(location.getLatitude(), location.getLongitude());
            //refreshMap();
        }

    }

    private void refreshMap() {
        mGoogleMap.animateCamera(CameraUpdateFactory.newLatLngZoom(mOrigem, 17.0f));
        mGoogleMap.clear();

        mGoogleMap.addMarker(new MarkerOptions()
                .position(mOrigem)
                .title("Meu Atual"))
                .setIcon(BitmapDescriptorFactory.fromResource(R.mipmap.ic_truck_red));
    }

    private void showErrorMessage(FragmentActivity activity, final int errorCode) {
        final String TAG = "DIALOG_ERROR_PLAYSERVICES";
        if (getSupportFragmentManager().findFragmentByTag(TAG) == null) {
            DialogFragment errorFragment = new DialogFragment() {
                @Override
                public Dialog onCreateDialog(Bundle savedInstanceState) {
                    return GooglePlayServicesUtil.getErrorDialog(
                            errorCode, getActivity(), REQUEST_ERROR_PLAY_SERVICES);

                }
            };
        }
    }

    private FindCallback<Place> callbackGetPlace() {
        return new FindCallback<Place>() {
            @Override
            public void done(List<Place> placeListFromParse, ParseException e) {
                if (e == null) {
                    checkList = new HashMap<>();
                    for (Place place : placeListFromParse) {

                        Marker marker = mGoogleMap.addMarker(new MarkerOptions()
                                .title(place.getTitle())
                                .position(place.getLatLong())
                                .icon(BitmapDescriptorFactory
                                        .fromResource(R.mipmap.ic_truck_orange)));

                        checkList.put(marker, place);

                    }
                }
            }
        };
    }

    private class UIHelper {
        private RelativeLayout contentLayout;
        private View contentBar;

        private UIHelper() {
            contentLayout = (RelativeLayout) findViewById(R.id.content_layout);
            contentBar = View.inflate(ShowMapActivity.this, R.layout.content_bar, null);
        }
    }
}
