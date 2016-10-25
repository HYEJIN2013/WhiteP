/**
 * Copyright 2014 Luigi Pasotti
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
 
package com.mypackage
 
public class DealerMapActivity {
    private DrawerLayout mDrawerLayout;
    
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // setup your map
        setUpMapIfNeeded();
        
        // This code bring your NavigationDrawer in front of any other element inside the DrawerLayout
        mDrawerLayout = (DrawerLayout) findViewById(R.id.drawer_layout);
        if(Build.VERSION.SDK_INT < Build.VERSION_CODES.HONEYCOMB){
         mDrawerLayout.setDrawerListener(new DrawerLayout.SimpleDrawerListener() {
             @Override
             public void onDrawerSlide(View drawerView, float slideOffset) {
                 mDrawerLayout.bringChildToFront(drawerView);
                 mDrawerLayout.requestLayout();
             }
         });
        }
        
        /**
         * Other code like NavigationDrawer contents, ecc
         */
    }
    
    private void setUpMapIfNeeded() { /* map setup */ }
}