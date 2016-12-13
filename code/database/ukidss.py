import cookielib,urllib2,urllib,htmllib,formatter,os,sys
import pyfits
from math import cos,radians
import multiprocessing as mp
import time

class LinksExtractor(htmllib.HTMLParser): # derive new HTML parser

    def __init__(self, formatter) :        # class constructor
        htmllib.HTMLParser.__init__(self, formatter)  # base class constructor
        self.links = []        # create an empty list for storing hyperlinks

    def start_a(self, attrs):  # override handler of <A ...>...</A> tags
        # process the attributes
        if len(attrs) > 0 :
            for attr in attrs :
                if attr[0] == "href" :         # ignore all non HREF attributes
                    self.links.append(attr[1]) # save the link info in the list

    def get_links(self):
        return self.links

url_login      = "http://surveys.roe.ac.uk:8080/wsa/DBLogin"
url_getimage   = "http://surveys.roe.ac.uk:8080/wsa/GetImage"
url_getimages  = "http://surveys.roe.ac.uk:8080/wsa/ImageList"
url_getcatalog = "http://surveys.roe.ac.uk:8080/wsa/WSASQL?"

class Request():

    def __init__(self):
        self.opener = ""
        self.database = 'UKIDSSDR8PLUS'
        self.programmeID = 102  # GPS
        self.filters = {'all':'all','J':'3','H':'4','K':'5'}

    def login(self,username,password,community):

        # Construct cookie holder, URL openenr, and retrieve login page
        self.cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        credentials = {'user':username,'passwd':password,'community':' ','community2':community}
        page = self.opener.open(url_login,urllib.urlencode(credentials))

    def logged_in(self):
        for c in self.cj:
            if c.is_expired():
                return False
        return True

        # Teporary - write out login result page to HTML
##        f = file('login.html','wb')
##        f.write(page.read())
##        f.close()

    def get_image_gal(self,name,glon,glat,filter,frametype,directory,size=1.0):

        # Construct request
        request = {}
        request['database']    = self.database
        request['programmeID'] = self.programmeID
        request['ra']          = glon
        request['dec']         = glat
        request['sys']         = 'G'
        request['filterID']    = self.filters[filter]
        request['xsize']       = size
        request['ysize']       = size
        request['obsType']     = 'object'
        request['frameType']   = frametype
        request['mfid']        = ''

        # Retrieve page
        page = self.opener.open(url_getimage,urllib.urlencode(request))
        results = page.read()

        # Parse results for links
        format = formatter.NullFormatter()
        htmlparser = LinksExtractor(format)
        htmlparser.feed(results)
        htmlparser.close()
        links = htmlparser.get_links()

        # Loop through links and retrieve FITS images
        for link in links:

            if not os.path.exists(directory):
                os.mkdir(directory)
            if not os.path.exists(directory+'/'+frametype):
                os.mkdir(directory+'/'+frametype)

            # Get image filename
            basename = os.path.basename(link.split("&")[0]).replace('.fit','.fits.gz')
            temp_file  = directory+'/'+frametype+'/'+basename

            # Get the file, and store temporarily
            urllib.urlretrieve(link.replace("getImage","getFImage"),temp_file)

            # Get Multiframe ID from the header
            h0 = pyfits.getheader(temp_file)
            filt = str(h0['FILTER']).strip()
            obj = filt+"_"+str(h0['OBJECT']).strip().replace(":",".")

            # Set final directory and file names
            final_dir  = directory+'/'+frametype+'/'+obj
            final_file = final_dir+'/'+basename

            # Create MFID directory if not existent
            if not os.path.exists(final_dir):
                os.mkdir(final_dir)

            # Check that the final file doesn't already exist
            if os.path.exists(final_file):
                sys.exit("File exists : "+final_file)

            os.rename(temp_file,final_file)

        # Temporary - write out search results page to HTML
##        f = file('results.html','wb')
##        f.write(results)
##        f.close()

    def get_images_gal(self,ra,dec,radius,filter,frametype,directory,n_concurrent=1):

        # Construct request
        request = {}

        request['database']    = self.database
        request['programmeID'] = self.programmeID
        request['userSelect'] = 'default'

        request['obsType']     = 'object'
        request['frameType']   = frametype
        request['filterID']    = self.filters[filter]

        request['minRA']       = str(round(ra - radius / cos(radians(dec)),2))
        request['maxRA']       = str(round(ra + radius / cos(radians(dec)),2))
        request['formatRA']    = 'degrees'

        request['minDec']       = str(dec - radius)
        request['maxDec']       = str(dec + radius)
        request['formatDec']    = 'degrees'

        request['startDay'] = 0
        request['startMonth'] = 0
        request['startYear'] = 0

        request['endDay'] = 0
        request['endMonth'] = 0
        request['endYear'] = 0

        request['dep'] = 0

        request['mfid'] = ''
        request['lmfid'] = ''
        request['fsid'] = ''

        request['rows'] = 1000

        # Retrieve page
        page = self.opener.open(url_getimages,urllib.urlencode(request))
        results = page.read()

        # Parse results for links
        format = formatter.NullFormatter()
        htmlparser = LinksExtractor(format)
        htmlparser.feed(results)
        htmlparser.close()
        links = htmlparser.get_links()

        # Loop through links and retrieve FITS images
        for link in links:

            if not os.path.exists(directory):
                os.mkdir(directory)
            if not os.path.exists(directory+'/'+frametype):
                os.mkdir(directory+'/'+frametype)

            if 'fits_download' in link and '_cat.fits' not in link and '_two.fit' not in link:

                # Get image filename
                basename = os.path.basename(link.split("&")[0])
                temp_file  = directory+'/'+frametype+'/'+basename

                print "Downloading %s..." % basename

                p = mp.Process(target=urllib.urlretrieve, args=(link, temp_file))
                p.start()

                while True:
                    if len(mp.active_children()) < n_concurrent:
                        break
                    time.sleep(0.1)

                # urllib.urlretrieve(link, temp_file)

                # # Get Multiframe ID from the header
                # h0 = pyfits.getheader(temp_file)
                # filt = str(h0['FILTER']).strip()
                # obj = filt+"_"+str(h0['OBJECT']).strip().replace(":",".")
                #
                # # Set final directory and file names
                # final_dir  = directory+'/'+frametype+'/'+obj
                # final_file = final_dir+'/'+basename
                #
                # # Create MFID directory if not existent
                # if not os.path.exists(final_dir):
                #     os.mkdir(final_dir)
                #
                # # Check that the final file doesn't already exist
                # if os.path.exists(final_file):
                #     sys.exit("File exists : "+final_file)
                #
                # os.rename(temp_file,final_file)


    def get_catalog_gal(self,name,glon,glat,directory,radius=1):

        # Construct request
        request = {}
        request['database']    = self.database
        request['programmeID'] = self.programmeID
        request['from'] = 'source'
        request['formaction'] = 'region'
        request['ra'] = glon
        request['dec'] = glat
        request['sys'] = 'G'
        request['radius'] = radius
        request['xSize'] = ''
        request['ySize'] = ''
        request['boxAlignment']='RADec'
        request['emailAddress'] = ''
        request['format'] = 'FITS'
        request['compress'] = 'GZIP'
        request['rows'] = 1
        request['select'] = '*'
        request['where'] = ''

        # Retrieve page
        page = self.opener.open(url_getcatalog+urllib.urlencode(request))
        results = page.read()

        # Parse results for links
        format = formatter.NullFormatter()           # create default formatter
        htmlparser = LinksExtractor(format)        # create new parser object
        htmlparser.feed(results)
        htmlparser.close()
        links = list(set(htmlparser.get_links()))

        # Loop through links and retrieve FITS tables
        c = 0
        for link in links:
            if not "8080" in link:
                c = c + 1

                if not os.path.exists(directory):
                    os.mkdir(directory)

                filename = directory+"/catalog_"+str(c)+".fits.gz"
                urllib.urlretrieve(link,filename)

        # Temporary - write out search results page to HTML
        f = file('results.html','wb')
        f.write(results)
        f.close()
